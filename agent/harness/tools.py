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

import ast
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
    "ToolError", "Workspace", "default_result_root", "without_submit",
    "DESIGN_TOOLS", "INTERPRET_TOOLS", "FOLLOWUP_AUTHOR_TOOLS",
]

#: Bexhoma reads its settings from this file in the working directory, and the
#: experiment path the agent submits through does not let a caller choose
#: another one. Reading the same file is therefore how the agent and Bexhoma
#: agree on where results land, on any cluster, without a second setting.
_CLUSTER_CONFIG = "cluster.config"

#: Suffixes a written specification may carry. The write tool exists to produce
#: an experiment.yml and nothing else, so anything else is refused rather than
#: silently accepted and then rejected by the YAML loader.
_SPEC_SUFFIXES = (".yml", ".yaml")

#: How long submit waits for bexhoma to create its preassigned result folder.
#: The run itself continues long after this.
_CODE_WAIT_SECONDS = 120
_RUN_LOCK = ".bexhoma-agent.lock"
_SUBMITTED_SPEC = "submitted-experiment.yml"
_STAGED_CATALOG = "submitted-contract_catalog.yml"
_STAGED_RESULT_CONTRACT = "submitted-contract_result.yml"
_STAGED_ENVIRONMENT = "submitted-environment.yml"

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

#: A phase is suspicious when its aggregate latency differs by at least this
#: factor from the median of the other repetitions at the same concurrency.
#: The result remains usable; this is a disclosure gate, not an invalidation.
_REPETITION_ANOMALY_RATIO = 3.0

_MARKDOWN_HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*$", re.MULTILINE)
_MARKDOWN_LINK = re.compile(r"!?\[[^]]*]\(([^)]+)\)")


class ToolError(Exception):
    """Raised when a tool call is refused, most often for leaving the write scope."""


def default_result_root(
    root: Path, cluster_config: str = _CLUSTER_CONFIG,
) -> Path | None:
    """Return the result folder Bexhoma is configured to write into.

    The agent waits for the exact directory Bexhoma creates, so this is read
    from Bexhoma's own configuration rather than defaulted to a path this
    package invented. A relative value resolves against the repository, which
    lets a checkout keep its results beside itself; an absolute one is used as
    given.

    :param root: Repository root, for resolving relative paths.
    :param cluster_config: Bexhoma's cluster configuration file.
    :return: The configured result folder, or ``None`` when the file is absent
        or does not declare one.
    :rtype: Path | None
    """
    source = Path(cluster_config)
    if not source.is_absolute():
        source = root / source
    try:
        configured = ast.literal_eval(
            source.read_text(encoding="utf-8"))["benchmarker"]["resultfolder"]
    except (OSError, SyntaxError, ValueError, KeyError, TypeError):
        return None
    if not isinstance(configured, str) or not configured.strip():
        return None
    # Bexhoma normalises Windows paths this way before using the value, so the
    # two sides would otherwise disagree on a Windows-authored configuration.
    folder = Path(configured.replace("\\", "/").replace("C:", ""))
    return folder if folder.is_absolute() else (root / folder)


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
        self._result_directory: Path | None = None
        self._reachable_result_files: set[Path] | None = None
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

        Validation state deliberately survives this reset. Interpretation and
        follow-up authoring use separate model conversations, so evidence returned
        to the first must not consume the second conversation's allowance.
        """
        self._returned_read_characters = 0

    def restrict_to_result(self, report_path: str, result_contract_path: str) -> None:
        """Restrict reads to one result and files reachable from its report.

        The report index, its archived experiment, and the exact result
        contract are the initial interface. Reading a Markdown file adds only
        the local files it links to; unrelated experiments never become
        readable merely because they share a result root.

        :param report_path: Exact ``report/index.md`` entry point.
        :param result_contract_path: Exact contract governing that result.
        """
        report = self._resolve_path(report_path)
        if self.results_root is None or not report.is_relative_to(self.results_root):
            raise ToolError("the report is outside the configured result root")
        self._result_directory = report.parent.parent
        contract = self._resolve_path(result_contract_path)
        self._reachable_result_files = {report, contract}
        experiment = self._result_directory / "experiment.yml"
        if experiment.is_file():
            self._reachable_result_files.add(experiment)
        self.reset_read_context()

    def restore_design_reads(self) -> None:
        """Restore the catalog, environment, and inbox read boundary."""
        self._result_directory = None
        self._reachable_result_files = None
        self.reset_read_context()

    def _resolve_path(self, path: str) -> Path:
        """Resolve one model-visible path against the workspace root."""
        source = Path(path)
        return source.resolve() if source.is_absolute() else (self.root / source).resolve()

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
        candidate = self._resolve_path(path)
        if self._reachable_result_files is not None:
            if candidate in self._reachable_result_files:
                return candidate
            raise ToolError(
                f"path {path!r} is not reachable from the selected report"
            )
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
        self._discover_result_links(source)
        return payload

    def _discover_result_links(self, source: Path) -> None:
        """Authorize local result files linked from one read Markdown page."""
        if (
            self._reachable_result_files is None
            or self._result_directory is None
            or source.suffix.lower() != ".md"
        ):
            return
        text = source.read_text(encoding="utf-8")
        for match in _MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://")):
                continue
            target = target.split("#", 1)[0]
            resolved = (source.parent / target).resolve()
            if resolved.is_relative_to(self._result_directory) and resolved.is_file():
                self._reachable_result_files.add(resolved)

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

    def invalidate_validation(self, path: str) -> None:
        """Forget any earlier validation approval for one inbox file.

        :param path: Specification path relative to :attr:`root`.
        """
        self._validated.pop(self._resolve_in_inbox(path), None)

    def assess_comparison_quality(self, path: str) -> dict[str, Any]:
        """Summarize query coverage, throughput validity, and repeat anomalies.

        :param path: Path to a TPC-H ``benchmarking.md`` evidence page.
        :return: Deterministic quality assessment for the interpretation gate.
        :rtype: dict[str, Any]
        """
        source = self._resolve_readable(path)
        result = _assess_comparison_quality(source.read_text(encoding="utf-8"))
        if "error" not in result:
            result["path"] = path
        return result

    def validate(self, path: str) -> dict[str, Any]:
        """Dry-run validate a written specification.

        :param path: Path of the specification, relative to :attr:`root`.
        :return: The verdict from :func:`agent.harness.validation.validate_spec`.
        :rtype: dict[str, Any]
        """
        target = self._resolve_in_inbox(path)
        result = validation.validate_spec(str(target), self.catalog_path, self.environment_path)
        if result.get("valid") and result.get("environment_checked"):
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
        approved = self._validated.get(specification)
        if approved is None:
            raise ToolError(
                "submit refused: specification has not passed full catalog and "
                "environment validation"
            )
        if approved != self._fingerprint(specification, contents):
            raise ToolError(
                "submit refused: specification or validation inputs changed "
                "since validate"
            )

        lock_fd = os.open(self.results_root / _RUN_LOCK, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(lock_fd)
            raise ToolError("submit refused: another agent-started experiment is still running") from error

        try:
            code = self._new_code()
            submitted = (self.run_directory or self.inbox) / _SUBMITTED_SPEC
            submitted.write_bytes(contents)
            provenance = self._stage_provenance(submitted)
            log_path = (self.run_directory or self.root) / "bexhoma.log"
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
        self._write_status(
            code, submitted, process.pid, provenance, str(log_path), "starting"
        )

        launch = self._await_result_folder(code, process)
        if launch == "exited":
            self._write_status(
                code, submitted, process.pid, provenance, str(log_path), "failed"
            )
            raise ToolError(
                f"bexhoma exited with status {process.returncode} before creating "
                f"result folder {code}; see {log_path}"
            )
        if launch == "timeout":
            # The child is deliberately left alone. It is still benchmarking, and
            # killing it would discard real cluster work over a slow start. Name
            # the run instead, so it can be followed or stopped on purpose rather
            # than found later by accident.
            return {
                "code": code,
                "state": "starting",
                "pid": process.pid,
                "log": str(log_path),
                "spec": str(submitted),
                "message": (
                    f"bexhoma has not created result folder {code} within "
                    f"{_CODE_WAIT_SECONDS}s but is still running and holds the "
                    "run lock"
                ),
            }
        self._archive_provenance(code, provenance)
        self._write_status(
            code, submitted, process.pid, provenance, str(log_path), "running"
        )
        return {
            "code": code,
            "state": "running",
            "pid": process.pid,
            "log": str(log_path),
            "spec": str(submitted),
        }

    def _fingerprint(
        self, specification: Path, contents: bytes | None = None,
    ) -> tuple[str, ...]:
        """Bind approval to the specification and both validation inputs."""
        paths = [Path(self.catalog_path)]
        if self.environment_path:
            paths.append(Path(self.environment_path))
        spec_hash = (
            hashlib.sha256(contents).hexdigest()
            if contents is not None else _sha256(specification)
        )
        return (spec_hash, *(_sha256(path) for path in paths))

    def _new_code(self) -> str:
        """Allocate the exact experiment code before launch."""
        code = round(time.time())
        while (self.results_root / str(code)).exists():
            code += 1
        return str(code)

    def _await_result_folder(self, code: str, process: subprocess.Popen[Any]) -> str:
        """Wait briefly for the exact result folder assigned to the child.

        :param code: Experiment code preassigned to the detached run.
        :param process: The detached bexhoma process.
        :return: ``"started"`` once the folder exists, ``"exited"`` when the
            child stopped without creating one, or ``"timeout"`` when it is
            still running and has not created one yet.
        :rtype: str
        """
        deadline = time.monotonic() + _CODE_WAIT_SECONDS
        while time.monotonic() < deadline:
            if (self.results_root / code).is_dir():
                return "started"
            if process.poll() is not None:
                return "exited"
            time.sleep(2)
        return "timeout"

    def _stage_provenance(self, submitted: Path) -> dict[str, str]:
        """Snapshot the exact inputs before the detached process starts."""
        staging_directory = self.run_directory or self.inbox
        sources = {
            "experiment.yml": submitted,
            "contract_catalog.yml": Path(self.catalog_path),
        }
        result_contract = self.root / "contracts" / "contract_result.yml"
        if result_contract.is_file():
            sources["contract_result.yml"] = result_contract
        if self.environment_path:
            sources["environment.yml"] = Path(self.environment_path)

        staged_paths = {
            "experiment.yml": submitted,
            "contract_catalog.yml": staging_directory / _STAGED_CATALOG,
            "contract_result.yml": staging_directory / _STAGED_RESULT_CONTRACT,
            "environment.yml": staging_directory / _STAGED_ENVIRONMENT,
        }
        for destination, source in sources.items():
            staged = staged_paths[destination]
            if staged != source:
                shutil.copyfile(source, staged)
        return {destination: str(staged_paths[destination]) for destination in sources}

    def _archive_provenance(self, code: str, provenance: dict[str, str]) -> None:
        """Copy staged agent inputs into an available result folder."""
        result = self.results_root / code
        for destination, source in provenance.items():
            shutil.copyfile(source, result / destination)

    def _write_status(
        self,
        code: str,
        specification: Path,
        pid: int,
        provenance: dict[str, str],
        log: str,
        state: str,
    ) -> None:
        """Record a submitted experiment so a later run can find it."""
        (self.status_dir / f"{code}.json").write_text(json.dumps({
            "code": code,
            "state": state,
            "spec": str(specification),
            "results": str(self.results_root / code),
            "pid": pid,
            "log": log,
            "provenance": provenance,
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
            result_directory = Path(entry["results"])
            provenance = entry.get("provenance")
            if result_directory.is_dir() and isinstance(provenance, dict):
                self._archive_provenance(str(entry["code"]), provenance)
            report = result_directory / "report" / "index.md"
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
            if name == "assess_comparison_quality":
                return self.assess_comparison_quality(arguments["path"])
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


def _markdown_table(text: str, heading: str) -> tuple[list[str], list[list[str]]] | None:
    """Parse the first Markdown table under one exact heading."""
    section = _markdown_section(text, heading)
    if section is None:
        return None
    lines = section.splitlines()
    table_start = next(
        (index for index, line in enumerate(lines) if line.startswith("|")), None
    )
    if table_start is None or table_start + 2 >= len(lines):
        return None
    headers = [cell.strip() for cell in lines[table_start].strip("|").split("|")]
    rows: list[list[str]] = []
    for line in lines[table_start + 2:]:
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(cells)
    return headers, rows


def _plain_markdown_cell(value: str) -> str:
    """Return a Markdown link's label, or the unchanged plain cell."""
    match = re.fullmatch(r"\[([^]]+)]\([^)]+\)", value.strip())
    return match.group(1) if match else value.strip()


def _query_number(value: str) -> int | None:
    """Extract a TPC-H query number from one report label."""
    match = re.search(r"\(TPC-H Q(\d+)\)", value)
    return int(match.group(1)) if match else None


def _phase_quality(text: str) -> tuple[set[str], list[dict[str, Any]]]:
    """Return configurations and suspicious aggregate-latency repetitions."""
    table = _markdown_table(text, "#### Per Phase")
    if table is None:
        return set(), []
    headers, rows = table
    required = {"phase", "experiment_run", "client", "Geo Times [s]"}
    if not required.issubset(headers):
        return set(), []
    positions = {name: headers.index(name) for name in required}
    groups: dict[tuple[str, int], list[tuple[int, float, str]]] = {}
    configurations: set[str] = set()
    for row in rows:
        phase = _plain_markdown_cell(row[positions["phase"]])
        try:
            experiment_run = int(row[positions["experiment_run"]])
            client = int(row[positions["client"]])
            latency = float(row[positions["Geo Times [s]"]])
        except ValueError:
            continue
        configuration = phase.rsplit("-", 2)[0]
        configurations.add(configuration)
        groups.setdefault((configuration, client), []).append(
            (experiment_run, latency, phase)
        )

    anomalies: list[dict[str, Any]] = []
    for (configuration, client), repetitions in sorted(groups.items()):
        if len(repetitions) < 3:
            continue
        for experiment_run, latency, phase in repetitions:
            peers = [value for run, value, _ in repetitions if run != experiment_run]
            if latency <= 0 or not peers or any(value <= 0 for value in peers):
                continue
            peer_median = statistics.median(peers)
            ratio = max(latency / peer_median, peer_median / latency)
            if ratio >= _REPETITION_ANOMALY_RATIO:
                anomalies.append({
                    "phase": phase,
                    "configuration": configuration,
                    "client": client,
                    "experiment_run": experiment_run,
                    "metric": "Geo Times [s]",
                    "value": latency,
                    "peer_median": round(peer_median, 2),
                    "ratio": round(ratio, 2),
                    "status": "suspect_not_invalid",
                })
    return configurations, anomalies


def _error_coverage(text: str) -> tuple[set[int], dict[str, set[int]], int]:
    """Return planned queries, errored queries by configuration, and error count."""
    table = _markdown_table(text, "### Errors (failed queries)")
    if table is None:
        return set(), {}, 0
    headers, rows = table
    query_columns = {
        index: query_number for index, header in enumerate(headers)
        if (query_number := _query_number(header)) is not None
    }
    errors: dict[str, set[int]] = {}
    total = 0
    for row in rows:
        connection = _plain_markdown_cell(row[0])
        parts = connection.rsplit("-", 4)
        if len(parts) != 5:
            continue
        configuration = parts[0]
        for index, query_number in query_columns.items():
            try:
                count = int(float(row[index]))
            except ValueError:
                continue
            if count > 0:
                errors.setdefault(configuration, set()).add(query_number)
                total += count
    return set(query_columns.values()), errors, total


def _assess_comparison_quality(text: str) -> dict[str, Any]:
    """Build the deterministic quality record used by the interpretation gate."""
    latency = _parse_query_latency(text)
    common_queries = set(latency.get("queries", {})) if "error" not in latency else set()
    configurations, anomalies = _phase_quality(text)
    planned_queries, errors, error_count = _error_coverage(text)
    planned_queries.update(common_queries)
    configurations.update(errors)
    if not planned_queries and not configurations:
        return {"error": "the report has no recognizable TPC-H comparison tables"}

    coverage = {}
    for configuration in sorted(configurations):
        errored = errors.get(configuration, set())
        coverage[configuration] = {
            "completed_queries": sorted(planned_queries - errored),
            "errored_queries": sorted(errored),
            "completed_count": len(planned_queries - errored),
            "planned_count": len(planned_queries),
        }
    coverage_status = "partial" if error_count else "complete"
    throughput_status = "not_comparable" if error_count else "comparable"
    return {
        "query_coverage": coverage_status,
        "planned_queries": sorted(planned_queries),
        "common_successful_queries": sorted(common_queries),
        "unresolved_queries": sorted({query for values in errors.values() for query in values}),
        "systems": coverage,
        "error_count": error_count,
        "whole_workload_throughput": throughput_status,
        "whole_workload_throughput_reason": (
            "At least one planned query errored, so wall time and completed-query "
            "counts do not represent the same whole workload across systems."
            if error_count else
            "Every planned query completed, so whole-workload throughput is comparable."
        ),
        "suspect_repetitions": anomalies,
        "anomaly_policy": (
            f"Warn when Geo Times differs by at least {_REPETITION_ANOMALY_RATIO:g}x "
            "from the median of peer repetitions at the same concurrency; do not "
            "invalidate it automatically."
        ),
    }


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

_ASSESS_COMPARISON_QUALITY = {
    "type": "function",
    "function": {
        "name": "assess_comparison_quality",
        "description": (
            "Deterministically assess one TPC-H benchmarking.md page for query "
            "coverage, whole-workload throughput comparability, and suspicious "
            "repetitions. Call this before recording a comparative interpretation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the report's benchmarking.md page.",
                },
            },
            "required": ["path"],
        },
    },
}

_RECORD_INTERPRETATION = {
    "type": "function",
    "function": {
        "name": "record_interpretation",
        "description": (
            "Record whether every explicit part of the user's question is settled "
            "before writing the closing study report. This does not start a run."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "hypothesis_verdict": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": [
                                "supported", "refuted", "inconclusive", "invalid",
                            ],
                        },
                        "conclusion": {"type": "string"},
                        "evidence_paths": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        },
                    },
                    "required": ["status", "conclusion", "evidence_paths"],
                },
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
                            "validity": {
                                "type": "string",
                                "enum": ["supported", "limited", "invalid"],
                            },
                            "conclusion": {"type": "string"},
                            "evidence": {"type": "string"},
                            "evidence_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 1,
                            },
                            "missing": {"type": "string"},
                        },
                        "required": [
                            "question", "status", "validity", "conclusion",
                            "evidence", "evidence_paths", "missing",
                        ],
                    },
                    "minItems": 1,
                },
                "validity": {
                    "type": "object",
                    "properties": {
                        "failed_checks": {"type": "integer", "minimum": 0},
                        "scope": {"type": "string"},
                        "evidence_paths": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        },
                    },
                    "required": ["failed_checks", "scope", "evidence_paths"],
                },
                "comparison_quality": {
                    "type": "object",
                    "properties": {
                        "query_coverage": {
                            "type": "string",
                            "enum": ["complete", "partial", "not_applicable"],
                        },
                        "whole_workload_throughput": {
                            "type": "string",
                            "enum": ["comparable", "not_comparable", "not_applicable"],
                        },
                        "suspect_repetitions": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": [
                        "query_coverage", "whole_workload_throughput",
                        "suspect_repetitions",
                    ],
                },
                "follow_up": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "enum": ["finish", "followup"]},
                        "rationale": {"type": "string"},
                        "unresolved_question": {"type": "string"},
                        "experiment_goal": {"type": "string"},
                        "target_queries": {
                            "type": "array",
                            "items": {"type": "integer", "minimum": 1},
                        },
                        "full_workload_required": {"type": "boolean"},
                        "cost_rationale": {"type": "string"},
                    },
                    "required": [
                        "action", "rationale", "unresolved_question",
                        "experiment_goal", "target_queries",
                        "full_workload_required", "cost_rationale",
                    ],
                },
            },
            "required": [
                "hypothesis_verdict", "validity", "comparison_quality",
                "questions", "follow_up",
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
] + [
    _ASSESS_COMPARISON_QUALITY, _RECORD_INTERPRETATION,
]

#: If the decision is to continue, authoring gets another fresh context and the
#: normal write/validate/submit boundary. A copy, not an alias: two names for
#: one list would let a change meant for one phase reach the other silently.
FOLLOWUP_AUTHOR_TOOLS: list[dict[str, Any]] = list(DESIGN_TOOLS)


def without_submit(schemas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the same tools with ``submit`` withheld, for a dry run.

    Returns a new list rather than editing the caller's: these schema lists are
    module-level and shared between phases, so an in-place edit would outlive
    the run that asked for it.

    :param schemas: Tool schemas a phase would normally offer.
    :return: The same schemas without the submission tool.
    :rtype: list[dict[str, Any]]
    """
    return [schema for schema in schemas if schema["function"]["name"] != "submit"]
