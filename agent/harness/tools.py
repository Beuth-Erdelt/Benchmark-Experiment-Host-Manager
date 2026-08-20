"""The tools the design-phase agent may call, and the path policy bounding them.

The whitelist in :class:`Workspace` is the contract boundary. The agent can only
write where this module lets it, so "the run stayed inside the contract" is a
property the harness enforces rather than a rule the prompt asks for. The model
gets no shell, network, or direct cluster access; ``submit`` can only launch the
validated specification through the fixed experiment entry point.

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from agent.harness import validation

__all__ = [
    "ToolError", "Workspace", "DESIGN_TOOLS", "INTERPRET_TOOLS",
    "FOLLOWUP_DECISION_TOOLS", "FOLLOWUP_AUTHOR_TOOLS",
]

#: Suffixes a written specification may carry. The write tool exists to produce
#: an experiment.yml and nothing else, so anything else is refused rather than
#: silently accepted and then rejected by the YAML loader.
_SPEC_SUFFIXES = (".yml", ".yaml")

#: How long submit waits for bexhoma to create its preassigned result folder.
#: The run itself continues long after this.
_CODE_WAIT_SECONDS = 120
_RUN_LOCK = ".bexhoma-agent.lock"
_SUBMITTED_SPEC = "submitted-experiment.yml"

#: Largest slice of a single file handed back by :meth:`Workspace.read_file`.
#: bexhoma's report is written for a human with a scrollbar: its six pages come
#: to roughly 700k tokens, more than ten times what the model can hold. Reading
#: one of the big pages whole ends the run with a context-length error, so a
#: read is capped and the agent is told in the payload that it was cut.
_READ_CHARACTER_LIMIT = 24_000
#: A section is already a targeted read, so keep it smaller than a whole-file
#: read. The agent can request a more specific nested heading when necessary.
_SECTION_CHARACTER_LIMIT = 12_000
#: Contracts and specifications are semantic units: return them complete or
#: reject them, never silently remove their tail.
_AUTHORITATIVE_CHARACTER_LIMIT = 48_000
_AUTHORITATIVE_FILENAMES = {
    "contract_catalog.yml", "contract_result.yml", "environment.yml",
    "experiment.yml", "submitted-experiment.yml",
}
#: Hard ceiling on file text returned during one agent invocation. This bounds
#: prompt growth even when the model keeps opening large evidence pages.
_READ_CONTEXT_CHARACTER_LIMIT = 80_000

_MARKDOWN_HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*$", re.MULTILINE)


class ToolError(Exception):
    """Raised when a tool call is refused, most often for leaving the write scope."""


class Workspace:
    """Filesystem scope for one agent run.

    :ivar root: Directory every relative path is resolved against.
    :ivar inbox: The only directory the agent may write into.
    :ivar catalog_path: Path to ``contract_catalog.yml``, used by ``validate``.
    :ivar environment_path: Path to ``environment.yml``, or ``None`` to skip the
        cluster-fit checks.
    """

    def __init__(
        self,
        root: str,
        inbox: str,
        catalog_path: str,
        environment_path: str | None = None,
        results_root: str | None = None,
        status_dir: str = "status",
        run_directory: Path | None = None,
    ) -> None:
        self.root = Path(root).resolve()
        self.inbox = (self.root / inbox).resolve()
        self.catalog_path = str((self.root / catalog_path).resolve())
        self.environment_path = (
            str((self.root / environment_path).resolve()) if environment_path else None
        )
        self.results_root = Path(results_root).resolve() if results_root else None
        self.status_dir = (self.root / status_dir).resolve()
        self.run_directory = run_directory
        self._validated: dict[Path, tuple[str, ...]] = {}
        self._returned_read_characters = 0
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.status_dir.mkdir(parents=True, exist_ok=True)
        # The architecture permits contracts, the environment descriptor, and
        # the agent's drafts. Results join this list during interpretation.
        self._readable_roots = [(self.root / "contracts").resolve(), self.inbox]
        if self.results_root:
            self._readable_roots.append(self.results_root)
        self._readable_files = {self.catalog_path}
        if self.environment_path:
            self._readable_files.add(self.environment_path)

    def reset_read_context(self) -> None:
        """Start a fresh model context with a fresh cumulative read allowance.

        Validation state deliberately survives this reset. A staged interpretation
        uses separate model conversations for evidence, follow-up selection, and
        authoring, so text returned to an earlier conversation must not consume the
        next conversation's allowance.
        """
        self._returned_read_characters = 0

    def _resolve_in_inbox(self, path: str) -> Path:
        """Resolve an agent-supplied path, refusing anything outside the inbox.

        Resolution happens before the check so that ``..`` segments and symlinks
        cannot walk out of the scope.

        :param path: Path as the agent wrote it, relative to :attr:`root`.
        :return: The resolved absolute path.
        :rtype: Path
        :raises ToolError: When the path leaves the inbox or is not a spec file.
        """
        candidate = (self.root / path).resolve()
        if candidate.parent != self.inbox:
            raise ToolError(
                f"path {path!r} is outside the write scope; "
                f"write specifications directly into {self.inbox.name}/"
            )
        if candidate.suffix not in _SPEC_SUFFIXES:
            raise ToolError(f"path {path!r} must end in {' or '.join(_SPEC_SUFFIXES)}")
        return candidate

    def _resolve_readable(self, path: str) -> Path:
        """Resolve an agent-supplied path, refusing anything outside the read scope.

        :param path: Path as the agent wrote it, relative to :attr:`root`.
        :return: The resolved absolute path.
        :rtype: Path
        :raises ToolError: When the path is not inside the read scope.
        """
        candidate = (self.root / path).resolve()
        if str(candidate) in self._readable_files:
            return candidate
        if any(candidate.is_relative_to(root) for root in self._readable_roots):
            return candidate
        raise ToolError(
            f"path {path!r} is outside the read scope; you may read the contract "
            "files you were pointed at and your own drafts, and nothing else"
        )

    def read_file(
        self, path: str, section: str | None = None, offset: int = 0,
    ) -> dict[str, Any]:
        """Read a file the agent is allowed to see.

        :param path: Path to read, relative to :attr:`root`.
        :param section: Optional exact Markdown heading. When supplied, return
            that heading and its contents instead of the beginning of the file.
        :param offset: Character offset within the selected Markdown section.
            Use the ``next_offset`` returned by a truncated section read.
        :return: ``{"path": path, "bytes": n, "text": contents}``, plus a
            ``"truncated"`` note when the file was too long to return whole.
        :rtype: dict[str, Any]
        """
        source = self._resolve_readable(path)
        text = source.read_text(encoding="utf-8")
        payload = {"path": path, "bytes": len(text.encode("utf-8"))}
        suffix = source.suffix.lower()
        authoritative = (
            str(source) in self._readable_files
            or source.parent == self.inbox
            or source.name in _AUTHORITATIVE_FILENAMES
        )

        if section is not None and suffix != ".md":
            return {"error": "section is only supported for Markdown files", "path": path}
        if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
            return {"error": "offset must be a non-negative integer", "path": path}
        if offset and section is None:
            return {
                "error": "offset is only supported together with a Markdown section",
                "path": path,
            }
        if section is None and suffix == ".md" and len(text) > _READ_CHARACTER_LIMIT:
            headings = [match.group(0) for match in _MARKDOWN_HEADING.finditer(text)]
            return {
                "error": "this Markdown file is too large for a whole-file read; request a section",
                "path": path,
                "available_sections": headings[:40],
                "more_sections": max(0, len(headings) - 40),
            }
        if authoritative and len(text) > _AUTHORITATIVE_CHARACTER_LIMIT:
            return {
                "error": (
                    f"authoritative file has {len(text)} characters, above the "
                    f"{_AUTHORITATIVE_CHARACTER_LIMIT}-character whole-file limit"
                ),
                "path": path,
            }

        limit = _READ_CHARACTER_LIMIT
        if section is not None:
            selected = _markdown_section(text, section)
            if selected is None:
                headings = [match.group(0) for match in _MARKDOWN_HEADING.finditer(text)]
                return {
                    "error": f"no Markdown section named {section!r} in {path}",
                    "available_sections": headings[:40],
                    "more_sections": max(0, len(headings) - 40),
                }
            text = selected
            payload["section"] = section
            limit = _SECTION_CHARACTER_LIMIT
            if offset > len(text):
                return {
                    "error": (
                        f"offset {offset} is past the selected section's "
                        f"{len(text)} characters"
                    ),
                    "path": path,
                    "section": section,
                }
            payload["offset"] = offset
            payload["selected_characters"] = len(text)
            text = text[offset:]
        elif authoritative:
            limit = len(text)

        remaining = _READ_CONTEXT_CHARACTER_LIMIT - self._returned_read_characters
        if remaining <= 0:
            return {
                "error": "file-reading context budget is exhausted; answer from the evidence already read",
                "path": path,
            }
        if authoritative and len(text) > remaining:
            return {
                "error": (
                    "authoritative file does not fit the remaining file-reading context budget; "
                    "no partial content was returned"
                ),
                "path": path,
            }
        shown = min(limit, remaining)
        if len(text) > shown:
            if section is not None:
                payload["next_offset"] = offset + shown
                payload["truncated"] = (
                    f"the selected content has more characters; {shown} characters are "
                    f"shown from offset {offset}. Continue with offset={offset + shown}"
                )
            else:
                payload["truncated"] = (
                    f"the selected content holds {len(text)} characters; only the first "
                    f"{shown} are shown"
                )
            text = text[:shown]
        payload["text"] = text
        payload["returned_characters"] = len(text)
        self._returned_read_characters += len(text)
        payload["context_characters_remaining"] = (
            _READ_CONTEXT_CHARACTER_LIMIT - self._returned_read_characters
        )
        return payload

    def write_file(self, path: str, text: str) -> dict[str, Any]:
        """Write an experiment specification into the inbox.

        :param path: Destination path, relative to :attr:`root`.
        :param text: Full file contents; any previous version is replaced.
        :return: ``{"written": path, "bytes": n}``.
        :rtype: dict[str, Any]
        """
        destination = self._resolve_in_inbox(path)
        destination.write_text(text, encoding="utf-8")
        return {"written": path, "bytes": len(text.encode("utf-8"))}

    def compare_query_latency(
        self,
        left_path: str,
        right_path: str,
        left_label: str = "left",
        right_label: str = "right",
    ) -> dict[str, Any]:
        """Compactly compare TPC-H latency tables from two execution reports.

        Each parallel connection is first averaged within its experiment-run
        and client phase. The reported point estimate is then the median of
        those phase means across experiment repetitions. This prevents an
        eight-stream phase from receiving eight times the weight of a
        one-stream phase and keeps 1,000+ table cells out of model context.
        """
        left = _parse_query_latency(
            self._resolve_readable(left_path).read_text(encoding="utf-8")
        )
        right = _parse_query_latency(
            self._resolve_readable(right_path).read_text(encoding="utf-8")
        )
        if "error" in left:
            return {"error": f"{left_path}: {left['error']}"}
        if "error" in right:
            return {"error": f"{right_path}: {right['error']}"}
        if set(left["queries"]) != set(right["queries"]):
            return {"error": "the reports do not contain the same query set"}

        queries: list[dict[str, Any]] = []
        clients = sorted({client for phases in left["queries"].values()
                          for _, client in phases})
        winner_counts: dict[str, dict[str, Any]] = {}
        for client in clients:
            counts = {left_label: [], right_label: [], "tie": []}
            for query_number in sorted(left["queries"]):
                left_phases = left["queries"][query_number]
                right_phases = right["queries"][query_number]
                left_runs = {run: value for (run, phase_client), value in left_phases.items()
                             if phase_client == client}
                right_runs = {run: value for (run, phase_client), value in right_phases.items()
                              if phase_client == client}
                if not left_runs or set(left_runs) != set(right_runs):
                    return {
                        "error": (
                            f"Q{query_number} client {client} lacks matched experiment runs"
                        )
                    }
                left_values = [left_runs[run] for run in sorted(left_runs)]
                right_values = [right_runs[run] for run in sorted(right_runs)]
                left_median = statistics.median(left_values)
                right_median = statistics.median(right_values)
                if right_median < left_median:
                    winner = right_label
                elif left_median < right_median:
                    winner = left_label
                else:
                    winner = "tie"
                counts[winner].append(f"Q{query_number}")
                queries.append({
                    "query": f"Q{query_number}",
                    "name": left["names"][query_number],
                    "client": client,
                    "parallel_connections": max(
                        left["phase_widths"].get((run, client), 0) for run in left_runs
                    ),
                    f"{left_label}_median_ms": round(left_median, 2),
                    f"{right_label}_median_ms": round(right_median, 2),
                    f"{right_label}_change_pct": round(
                        (right_median / left_median - 1) * 100, 1
                    ),
                    "winner": winner,
                    f"{left_label}_range_ms": [
                        round(min(left_values), 2), round(max(left_values), 2)
                    ],
                    f"{right_label}_range_ms": [
                        round(min(right_values), 2), round(max(right_values), 2)
                    ],
                    f"{right_label}_faster_matched_runs": sum(
                        right_runs[run] < left_runs[run] for run in left_runs
                    ),
                    "matched_runs": len(left_runs),
                })
            winner_counts[str(client)] = {
                "parallel_connections": max(
                    width for (run, phase_client), width in left["phase_widths"].items()
                    if phase_client == client
                ),
                f"{left_label}_faster_queries": counts[left_label],
                f"{right_label}_faster_queries": counts[right_label],
                "ties": counts["tie"],
            }
        return {
            "metric": "Latency of Timer Execution [ms]",
            "lower_is_better": True,
            "method": (
                "mean across parallel connections within each experiment-run/client "
                "phase, then median and range across matched experiment runs"
            ),
            "left": {"label": left_label, "path": left_path},
            "right": {"label": right_label, "path": right_path},
            "winner_counts": winner_counts,
            "queries": queries,
        }

    def validate(self, path: str) -> dict[str, Any]:
        """Dry-run validate a written specification.

        :param path: Path of the specification, relative to :attr:`root`.
        :return: The verdict from :func:`agent.harness.validation.validate_spec`.
        :rtype: dict[str, Any]
        """
        target = self._resolve_in_inbox(path)
        result = validation.validate_spec(str(target), self.catalog_path, self.environment_path)
        if result.get("valid"):
            self._validated[target] = self._fingerprint(target)
        else:
            self._validated.pop(target, None)
        return result

    def submit(self, path: str) -> dict[str, Any]:
        """Hand a validated specification to bexhoma and return its experiment code.

        bexhoma is launched detached, so the run outlives this process and the
        agent can exit rather than sit through twenty minutes of benchmarking.
        Submission is allowed only for the exact bytes that passed validation.
        The detached child inherits a lock on the shared result root, preventing
        agent-started benchmark runs from overlapping.

        :param path: Path of the specification to submit.
        :return: ``{"code": ..., "log": ...}``, or ``{"error": ...}``.
        :rtype: dict[str, Any]
        """
        specification = self._resolve_in_inbox(path)
        if self.results_root is None:
            raise ToolError("no result folder configured, so a run cannot be tracked")
        contents = specification.read_bytes()
        if self._validated.get(specification) != self._fingerprint(specification, contents):
            raise ToolError("submit refused: specification or validation inputs changed since validate")

        lock_fd = os.open(self.results_root / _RUN_LOCK, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(lock_fd)
            raise ToolError("submit refused: another agent-started experiment is still running") from error

        code = self._new_code()
        submitted = (self.run_directory or self.inbox) / _SUBMITTED_SPEC
        submitted.write_bytes(contents)
        log_path = (self.run_directory or self.root) / "bexhoma.log"
        try:
            with log_path.open("w", encoding="utf-8") as log:
                process = subprocess.Popen(
                    [sys.executable, "-m", "agent.harness.submit", str(submitted),
                     "--catalog", self.catalog_path, "--experiment-code", code],
                    cwd=self.root, stdout=log, stderr=subprocess.STDOUT,
                    start_new_session=True, pass_fds=(lock_fd,),
                )
        except Exception:
            os.close(lock_fd)
            raise
        os.close(lock_fd)  # the detached child now holds the run lock
        self._write_status(code, submitted, process.pid)

        if not self._await_result_folder(code, process):
            raise ToolError(f"bexhoma created no result folder within {_CODE_WAIT_SECONDS}s; see {log_path}")
        self._archive_provenance(code, submitted)
        return {"code": code, "log": str(log_path), "spec": str(submitted)}

    def _fingerprint(self, specification: Path, contents: bytes | None = None) -> tuple[str, ...]:
        """Bind approval to the specification and both validation inputs."""
        paths = [Path(self.catalog_path)]
        if self.environment_path:
            paths.append(Path(self.environment_path))
        spec_hash = hashlib.sha256(contents).hexdigest() if contents is not None else _sha256(specification)
        return (spec_hash, *(_sha256(path) for path in paths))

    def _new_code(self) -> str:
        """Allocate the exact experiment code before launch."""
        code = round(time.time())
        while (self.results_root / str(code)).exists():
            code += 1
        return str(code)

    def _await_result_folder(self, code: str, process: subprocess.Popen[Any]) -> bool:
        """Wait briefly for the exact result folder assigned to the child."""
        deadline = time.monotonic() + _CODE_WAIT_SECONDS
        while time.monotonic() < deadline:
            if (self.results_root / code).is_dir():
                return True
            if process.poll() is not None:
                return False
            time.sleep(2)
        return False

    def _archive_provenance(self, code: str, submitted: Path) -> None:
        """Copy the exact agent inputs into the result folder."""
        result = self.results_root / code
        shutil.copyfile(submitted, result / "experiment.yml")
        shutil.copyfile(self.catalog_path, result / "contract_catalog.yml")
        result_contract = self.root / "contracts" / "contract_result.yml"
        if result_contract.is_file():
            shutil.copyfile(result_contract, result / result_contract.name)
        if self.environment_path:
            shutil.copyfile(self.environment_path, result / "environment.yml")

    def _write_status(self, code: str, specification: Path, pid: int) -> None:
        """Record a submitted experiment so a later run can find it."""
        (self.status_dir / f"{code}.json").write_text(json.dumps({
            "code": code,
            "state": "running",
            "spec": str(specification),
            "results": str(self.results_root / code),
            "pid": pid,
        }, indent=2), encoding="utf-8")

    def list_results(self) -> dict[str, Any]:
        """List experiments submitted from this workspace, newest first.

        State is derived from the result folder, then a changed terminal state
        is persisted so both this API and direct status-file readers agree.
        No background watcher is required.

        :return: ``{"experiments": [...]}``.
        :rtype: dict[str, Any]
        """
        experiments = []
        for status_file in sorted(self.status_dir.glob("*.json"), reverse=True):
            entry = json.loads(status_file.read_text(encoding="utf-8"))
            stored_state = entry.get("state")
            report = Path(entry["results"]) / "report" / "index.md"
            if report.is_file():
                entry["state"] = "finished"
            elif entry.get("pid") and not _pid_alive(entry["pid"]):
                entry["state"] = "failed"
            if entry.get("state") != stored_state:
                # Persist the derived terminal state. The harness does not need
                # a separate watcher, and status files stop misleading humans
                # and tools that inspect them directly.
                status_file.write_text(json.dumps(entry, indent=2), encoding="utf-8")
            entry["report"] = str(report) if report.is_file() else None
            experiments.append(entry)
        return {"experiments": experiments}

    def call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Dispatch one tool call by name.

        A refused or malformed call comes back as an ``error`` result rather than
        an exception, so the model can correct itself instead of the run dying.

        :param name: Tool name as the model emitted it.
        :param arguments: Decoded tool arguments.
        :return: The tool's result, or ``{"error": message}``.
        :rtype: dict[str, Any]
        """
        try:
            if name == "read_file":
                return self.read_file(
                    arguments["path"], arguments.get("section"), arguments.get("offset", 0)
                )
            if name == "compare_query_latency":
                return self.compare_query_latency(
                    arguments["left_path"], arguments["right_path"],
                    arguments.get("left_label", "left"),
                    arguments.get("right_label", "right"),
                )
            if name == "write_file":
                return self.write_file(arguments["path"], arguments["text"])
            if name == "validate":
                return self.validate(arguments["path"])
            if name == "submit":
                return self.submit(arguments["path"])
            if name == "list_results":
                return self.list_results()
            return {
                "error": f"unknown tool {name!r}; check the tools you were given"
            }
        except (ToolError, KeyError, OSError) as error:
            return {"error": str(error)}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _markdown_section(text: str, requested: str) -> str | None:
    """Return one exact Markdown section, including its heading."""
    query = requested.strip()
    query_match = re.fullmatch(r"(#{1,6})[ \t]+(.+)", query)
    wanted_level = len(query_match.group(1)) if query_match else None
    wanted_title = (query_match.group(2) if query_match else query).strip().casefold()
    headings = list(_MARKDOWN_HEADING.finditer(text))
    matches = [
        (index, heading) for index, heading in enumerate(headings)
        if heading.group(2).strip().casefold() == wanted_title
        and (wanted_level is None or len(heading.group(1)) == wanted_level)
    ]
    if len(matches) != 1:
        return None
    index, heading = matches[0]
    level = len(heading.group(1))
    end = len(text)
    for following in headings[index + 1:]:
        if len(following.group(1)) <= level:
            end = following.start()
            break
    return text[heading.start():end].rstrip() + "\n"


def _parse_query_latency(text: str) -> dict[str, Any]:
    """Parse the report's per-query timer table into phase-level means."""
    section = _markdown_section(text, "### Latency of Timer Execution [ms]")
    if section is None:
        return {"error": "latency section is missing or ambiguous"}
    lines = section.splitlines()
    if len(lines) < 4:
        return {"error": "latency section has no Markdown table"}
    headers = [cell.strip() for cell in lines[1].strip("|").split("|")]
    groups: list[tuple[int, int]] = []
    for connection in headers[1:]:
        parts = connection.split("-")
        try:
            experiment_run, client = int(parts[-4]), int(parts[-3])
        except (IndexError, ValueError):
            return {"error": f"cannot decode connection heading {connection!r}"}
        groups.append((experiment_run, client))

    queries: dict[int, dict[tuple[int, int], float]] = {}
    names: dict[int, str] = {}
    phase_widths: dict[tuple[int, int], int] = {}
    for line in lines[3:]:
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        match = re.search(r"\(TPC-H Q(\d+)\)", cells[0])
        if match is None:
            continue
        if len(cells) - 1 != len(groups):
            return {"error": f"Q{match.group(1)} has a different column count"}
        phase_values: dict[tuple[int, int], list[float]] = {}
        try:
            values = [float(value) for value in cells[1:]]
        except ValueError:
            return {"error": f"Q{match.group(1)} contains a non-numeric latency"}
        for group, value in zip(groups, values):
            phase_values.setdefault(group, []).append(value)
        query_number = int(match.group(1))
        names[query_number] = cells[0]
        queries[query_number] = {
            group: statistics.mean(values) for group, values in phase_values.items()
        }
        for group, values in phase_values.items():
            phase_widths[group] = len(values)
    if not queries:
        return {"error": "latency table contains no TPC-H query rows"}
    return {"queries": queries, "names": names, "phase_widths": phase_widths}


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


#: Tool definitions in the OpenAI function-calling shape, which is what the
#: self-hosted server speaks. Descriptions are deliberately short: what a good
#: experiment looks like belongs in the catalog and the system prompt, not here.
TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": (
                "Read an allowed contract, draft, or result file. For large "
                "Markdown reports, an exact heading with section is required. "
                "If a section is truncated, continue it with the returned next_offset. "
                "Contracts and specifications are returned whole or not at all."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to read, e.g. contracts/contract_catalog.yml",
                    },
                    "section": {
                        "type": "string",
                        "description": (
                            "Optional exact Markdown heading, e.g. '### Errors (failed queries)'. "
                            "Use this for large report pages instead of reading their beginning."
                        ),
                    },
                    "offset": {
                        "type": "integer",
                        "minimum": 0,
                        "description": (
                            "Character offset within a selected Markdown section. Only use "
                            "the next_offset returned by an earlier truncated section read."
                        ),
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": (
                "Write an experiment specification into the inbox directory. "
                "Always write the complete file; there is no partial edit."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Destination path inside the inbox, e.g. inbox/join-study.yml",
                    },
                    "text": {"type": "string", "description": "Full YAML contents of the file."},
                },
                "required": ["path", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "validate",
            "description": (
                "Dry-run check a written specification against the catalog and the "
                "cluster environment. Runs nothing and costs no cluster time."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the specification to check.",
                    },
                },
                "required": ["path"],
            },
        },
    },
]

_SUBMIT = {
    "type": "function",
    "function": {
        "name": "submit",
        "description": (
            "Hand a validated specification to the cluster to run. Returns the "
            "experiment code the results will be filed under. Only call this "
            "once, on a specification that has already validated."
        ),
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Specification to run."}},
            "required": ["path"],
        },
    },
}

_LIST_RESULTS = {
    "type": "function",
    "function": {
        "name": "list_results",
        "description": (
            "List the experiments submitted from here, newest first, with their "
            "state and the path of the report to read when one has finished."
        ),
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
}

_COMPARE_QUERY_LATENCY = {
    "type": "function",
    "function": {
        "name": "compare_query_latency",
        "description": (
            "Deterministically compare the TPC-H per-query latency tables in two "
            "execution.md reports. Use this instead of manually summing the table. "
            "Returns per-phase medians/ranges, matched-run wins, and compact query winners."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "left_path": {"type": "string"},
                "right_path": {"type": "string"},
                "left_label": {"type": "string"},
                "right_label": {"type": "string"},
            },
            "required": ["left_path", "right_path", "left_label", "right_label"],
        },
    },
}

_RECORD_INTERPRETATION = {
    "type": "function",
    "function": {
        "name": "record_interpretation",
        "description": (
            "Record whether every explicit part of the user's question is settled "
            "before writing the closing interpretation. This does not start a run."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "status": {
                                "type": "string",
                                "enum": ["settled", "partial", "unresolved"],
                            },
                            "conclusion": {"type": "string"},
                            "evidence": {"type": "string"},
                            "missing": {"type": "string"},
                        },
                        "required": [
                            "question", "status", "conclusion", "evidence", "missing",
                        ],
                    },
                    "minItems": 1,
                },
            },
            "required": ["questions"],
        },
    },
}

_RECORD_FOLLOWUP_DECISION = {
    "type": "function",
    "function": {
        "name": "record_followup_decision",
        "description": (
            "Record the informed decision to finish or run one follow-up after "
            "consulting the available design space. This does not start a run."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["finish", "followup"]},
                "rationale": {"type": "string"},
                "unresolved_question": {"type": "string"},
                "experiment_goal": {"type": "string"},
            },
            "required": [
                "action", "rationale", "unresolved_question", "experiment_goal",
            ],
        },
    },
}

#: Tools for the design phase: read the contracts, write a specification, check
#: it, and hand it over.
DESIGN_TOOLS: list[dict[str, Any]] = TOOL_SCHEMAS + [_SUBMIT]

#: Tools for the interpretation phase. There is nothing to write: the agent
#: finds what finished and reads its way through the result folder.
INTERPRET_TOOLS: list[dict[str, Any]] = [
    schema for schema in TOOL_SCHEMAS if schema["function"]["name"] == "read_file"
] + [_COMPARE_QUERY_LATENCY, _LIST_RESULTS, _RECORD_INTERPRETATION]

#: A fresh, read-only context consults the design space before choosing whether
#: another experiment is worth its budget.
FOLLOWUP_DECISION_TOOLS: list[dict[str, Any]] = [TOOL_SCHEMAS[0], _RECORD_FOLLOWUP_DECISION]

#: If the decision is to continue, authoring gets another fresh context and the
#: normal write/validate/submit boundary.
FOLLOWUP_AUTHOR_TOOLS: list[dict[str, Any]] = DESIGN_TOOLS
