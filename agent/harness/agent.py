"""The agent loop: design an experiment, submit it, then interpret what came back.

One reusable tool-calling loop drives bounded contexts with different prompts,
tools, and stopping rules. Each invocation is one phase of an investigation.
Every phase appends to the investigation's single trajectory; separate phase
reports preserve local detail and each completed interpretation answers for
exactly one result folder. Durable state is rebuilt from the event log rather
than from model memory.

    python -m agent.harness.agent --task "..."          # design and submit
    python -m agent.harness.agent --phase interpret --report .../report/index.md

Authors: Leonhard Liu
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

import yaml
from dotenv import load_dotenv

from agent.harness import model_client, prompts, tools

__all__ = ["Trajectory", "run_design", "run_interpret"]

_DEFAULT_INBOX = "inbox"
_DEFAULT_CATALOG = os.path.join("contracts", "contract_catalog.yml")
_DEFAULT_RESULT_CONTRACT = os.path.join("contracts", "contract_result.yml")
_DEFAULT_ENVIRONMENT = os.path.join("dev", "catalog", "environment.yml")
_DEFAULT_TRAJECTORIES = os.path.join("agent", "trajectories")
_DEFAULT_BASE_URL = "http://localhost:8000/v1"
_AGENT_SUMMARY_NAME = "agent_summary.yml"
_AGENT_SUMMARY_VERSION = "1.0.0"

#: Validate calls allowed per run: one first attempt plus two repairs.
_DEFAULT_ATTEMPTS = 3
#: Follow-up experiments the agent is told it will be offered.
_DEFAULT_FOLLOWUPS = 1
#: Tokens a single turn may generate, thinking included. A reasoning model
#: reading a large report needs room to think and still write its answer.
_DEFAULT_MAX_TOKENS = 16384

#: Turns allowed per validation attempt. Four cover read, read, write, validate;
#: the slack absorbs a model that narrates or rewrites before validating.
_TURNS_PER_ATTEMPT = 6
#: Turns allowed for reading a result folder, which is many small reads.
_INTERPRET_TURNS = 24
#: Extra turns beyond the budget, for the closing answer.
_CLOSING_TURNS = 2

#: Told to the agent when a budgeted tool runs out, so its last turn is a report
#: rather than more attempts it cannot make.
_EXHAUSTED_NOTICE = (
    "Your {tool} budget is used up, so no further calls are available this run. "
    "Stop editing and reply with a short account, in plain sentences, of where "
    "you got to and what was still unresolved."
)

def _timestamp() -> str:
    """Return the current UTC time in ISO 8601 form.

    :return: Timestamp, e.g. ``2026-08-18T12:01:28+00:00``.
    :rtype: str
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _file_sha256(path: Optional[str]) -> Optional[str]:
    source = Path(path) if path else None
    return hashlib.sha256(source.read_bytes()).hexdigest() if source and source.is_file() else None


class Trajectory:
    """Append-only event log for one complete investigation.

    :ivar directory: Run directory holding the log and its companion files.
    :ivar path: Path of the JSON-lines log itself.
    """

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory / "trajectory.jsonl"

    def record(self, event_type: str, **fields: Any) -> None:
        """Append one event, flushing immediately so a crashed run keeps its log.

        :param event_type: Event kind, e.g. ``"tool_call"``.
        :param fields: Event payload; must be JSON-serialisable.
        """
        event = {"ts": _timestamp(), "type": event_type, **fields}
        with self.path.open("a", encoding="utf-8") as log:
            log.write(json.dumps(event, ensure_ascii=False) + "\n")


def _loggable(tool: str, result: dict[str, Any]) -> dict[str, Any]:
    """Drop file contents from a logged result, keeping the byte count."""
    if tool == "read_file" and "text" in result:
        return {key: value for key, value in result.items() if key != "text"}
    return result


def _converse(
    messages: list[dict[str, Any]],
    model: model_client.ChatModel,
    workspace: tools.Workspace,
    trajectory: Trajectory,
    tool_schemas: list[dict[str, Any]],
    max_turns: int,
    limited_tool: Optional[str] = None,
    limit: int = 0,
    done_when: Optional[Callable[[str, dict[str, Any]], bool]] = None,
    tool_handler: Optional[Callable[[str, dict[str, Any]], dict[str, Any]]] = None,
    closing_validator: Optional[Callable[[str], Optional[str]]] = None,
    stage: Optional[str] = None,
    require_done: bool = False,
) -> tuple[str, int, list[tuple[str, dict[str, Any], dict[str, Any]]]]:
    """Drive the model until it stops calling tools, the phase is done, or turns run out.

    Tools are withdrawn once the phase is finished or its budget is spent, so the
    closing turn can only be the plain-sentence answer each phase asks for.

    :param messages: Opening conversation; extended in place.
    :param model: The chat model to drive.
    :param workspace: Filesystem scope and tool implementations.
    :param trajectory: Event log for this run.
    :param tool_schemas: Tools this phase offers.
    :param max_turns: Hard ceiling on model turns.
    :param limited_tool: Name of a tool that may only be called so many times.
    :param limit: How many times that tool may be called.
    :param done_when: Called with each tool result; returning ``True`` ends the phase.
    :param tool_handler: Optional dispatcher for stage-local record tools.
    :param closing_validator: Return an error message for an invalid closing answer.
    :param stage: Optional stage label written on assistant and tool events.
    :param require_done: Reject a text-only answer until ``done_when`` has fired.
    :return: The closing text, the turns used, and every tool call made.
    :rtype: tuple[str, int, list[tuple[str, dict, dict]]]
    """
    remaining = limit
    finished = False
    notified = False
    summary = ""
    events: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    turn = 0

    while turn < max_turns:
        turn += 1
        spent = limited_tool is not None and remaining <= 0
        if spent and not finished and not notified:
            messages.append({"role": "user", "content": _EXHAUSTED_NOTICE.format(tool=limited_tool)})
            trajectory.record("budget_exhausted", turn=turn, tool=limited_tool)
            notified = True
        reply = model.reply(messages, None if (finished or spent) else tool_schemas)
        stage_field = {"stage": stage} if stage else {}
        trajectory.record("assistant", turn=turn, text=reply.text,
                          reasoning=reply.reasoning,
                          tool_calls=[asdict(call) for call in reply.tool_calls],
                          usage=reply.usage, **stage_field)
        messages.append(reply.message)

        if not reply.tool_calls:
            if require_done and done_when is not None and not finished:
                notice = (
                    "The required structured record is still missing. Call the "
                    "record tool you were given before writing the closing answer."
                )
                messages.append({"role": "user", "content": notice})
                trajectory.record("completion_rejected", turn=turn,
                                  reason="required record missing", **stage_field)
                continue
            closing_error = closing_validator(reply.text) if closing_validator else None
            if closing_error is not None:
                messages.append({
                    "role": "user",
                    "content": f"The closing answer is invalid: {closing_error}",
                })
                trajectory.record("completion_rejected", turn=turn,
                                  reason=closing_error, **stage_field)
                continue
            summary = reply.text
            break

        for call in reply.tool_calls:
            if call.decode_error is not None:
                result: dict[str, Any] = {"error": f"could not decode arguments: {call.decode_error}"}
            elif finished:
                result = {"error": "the phase is already complete; no further tools were run"}
            elif call.name == limited_tool and remaining <= 0:
                result = {"error": f"{limited_tool} budget of {limit} call(s) is exhausted"}
            else:
                result = (tool_handler or workspace.call)(call.name, call.arguments)
                if call.name == limited_tool:
                    remaining -= 1
                if done_when is not None and done_when(call.name, result):
                    finished = True
            events.append((call.name, call.arguments, result))
            trajectory.record("tool_call", turn=turn, tool=call.name,
                              args=call.arguments, result=_loggable(call.name, result),
                              **stage_field)
            messages.append({"role": "tool", "tool_call_id": call.id,
                             "content": json.dumps(result, ensure_ascii=False)})

    return summary, turn, events


def _outcome(trajectory: Trajectory, **fields: Any) -> dict[str, Any]:
    """Record and return a phase outcome."""
    trajectory.record("outcome", **fields)
    return fields


def _report_failed_checks(path: Path) -> int | None:
    """Return the failed-check count from report frontmatter, if valid."""
    try:
        _, frontmatter, _ = path.read_text(encoding="utf-8").split("---", 2)
        failed = yaml.safe_load(frontmatter)["overall_status"]["failed"]
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError):
        return None
    return failed if isinstance(failed, int) and not isinstance(failed, bool) else None


def _write_agent_summary(
    report_path: str,
    specification: Optional[str],
    hypothesis_verdict: dict[str, Any],
    validity: dict[str, Any],
    follow_up: dict[str, Any],
    root: Path,
) -> tuple[Path, dict[str, Any]]:
    """Persist one compact, portable interpretation beside its result.

    :param report_path: Entry point of the interpreted result folder.
    :param specification: Exact experiment specification, when one exists.
    :param hypothesis_verdict: Recorded scientific verdict.
    :param validity: Recorded mechanical validity assessment.
    :param follow_up: Recorded finish-or-follow-up decision.
    :param root: Workspace root used to resolve model-visible evidence paths.
    :return: Written path and summary object.
    :rtype: tuple[Path, dict[str, Any]]
    """
    report = Path(report_path)
    report = report.resolve() if report.is_absolute() else (root / report).resolve()
    result_directory = report.parent.parent
    try:
        experiment = yaml.safe_load(specification) if specification else None
    except yaml.YAMLError:
        experiment = None
    if not isinstance(experiment, dict):
        experiment = {}

    evidence_paths = []
    for value in hypothesis_verdict["evidence_paths"]:
        source = Path(value)
        source = source.resolve() if source.is_absolute() else (root / source).resolve()
        evidence_paths.append(source.relative_to(result_directory).as_posix())

    summary = {
        "agent_summary_version": _AGENT_SUMMARY_VERSION,
        "experiment_code": result_directory.name,
        "follow_up_of": experiment.get("follow_up_of"),
        "hypothesis": experiment.get("hypothesis"),
        "verdict": {
            "status": hypothesis_verdict["status"],
            "conclusion": hypothesis_verdict["conclusion"],
            "evidence_paths": evidence_paths,
        },
        "technical_validity": {
            "failed_checks": validity["failed_checks"],
            "scope": validity["scope"],
        },
        "unresolved_question": follow_up["unresolved_question"],
    }
    target = result_directory / _AGENT_SUMMARY_NAME
    temporary = result_directory / f".{_AGENT_SUMMARY_NAME}.tmp"
    temporary.write_text(
        yaml.safe_dump(summary, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    temporary.replace(target)
    return target, summary


def _load_ancestor_summaries(
    result_directory: Path, follow_up_of: Any,
) -> list[dict[str, Any]]:
    """Load compact ancestor records by following parent experiment codes.

    :param result_directory: Directory of the result being interpreted.
    :param follow_up_of: Its parent experiment code, if any.
    :return: Valid summaries ordered from the oldest ancestor to the newest.
    :rtype: list[dict[str, Any]]
    """
    summaries: list[dict[str, Any]] = []
    seen = {result_directory.name}
    experiment_code = follow_up_of
    result_root = result_directory.parent.resolve()
    while isinstance(experiment_code, str) and experiment_code.isdigit():
        if experiment_code in seen:
            break
        seen.add(experiment_code)
        source = result_root / experiment_code / _AGENT_SUMMARY_NAME
        try:
            summary = yaml.safe_load(source.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            break
        if (
            not isinstance(summary, dict)
            or summary.get("agent_summary_version") != _AGENT_SUMMARY_VERSION
            or summary.get("experiment_code") != experiment_code
            or not isinstance(summary.get("verdict"), dict)
        ):
            break
        summaries.append(summary)
        experiment_code = summary.get("follow_up_of")
    summaries.reverse()
    return summaries


def run_design(
    task: str,
    workspace: tools.Workspace,
    model: model_client.ChatModel,
    trajectory: Trajectory,
    catalog_path: str,
    catalog_sha256: str,
    environment_path: Optional[str],
    attempts: int = _DEFAULT_ATTEMPTS,
    followups: int = _DEFAULT_FOLLOWUPS,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Turn a question into a validated experiment and hand it to the cluster.

    :param task: The question to answer, verbatim.
    :param workspace: Filesystem scope and tool implementations.
    :param model: The chat model to drive.
    :param trajectory: Event log for this run.
    :param catalog_path: Path the agent is told to read the catalog from.
    :param catalog_sha256: Digest of that catalog, recorded for provenance.
    :param environment_path: Path to the environment descriptor, or ``None``.
    :param attempts: How many validate calls the agent may make.
    :param followups: How many follow-up experiments it is told it will get.
    :param dry_run: Withhold the submission tool so nothing reaches the cluster.
    :return: ``{"validated_path", "code", "summary", "attempts_used", "turns"}``.
    :rtype: dict[str, Any]
    """
    messages = prompts.design_messages(
        task=task, catalog_path=catalog_path, environment_path=environment_path,
        inbox=workspace.inbox.name, attempts=attempts, followups=followups)
    trajectory.record("meta", phase="design", model=model.model,
                      params={"temperature": model.temperature, "max_tokens": model.max_tokens},
                      catalog_sha256=catalog_sha256,
                      environment_sha256=_file_sha256(environment_path),
                      environment_present=environment_path is not None,
                      budgets={"validate_attempts": attempts, "followups": followups})
    trajectory.record("task", text=task)

    design_tools = (
        tools.without_submit(tools.DESIGN_TOOLS) if dry_run else tools.DESIGN_TOOLS
    )
    gate = _DesignSpaceGate(workspace, environment_path)

    def handler(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "read_file":
            return gate.read_file(arguments)
        if name == "write_file" and (missing := gate.missing()):
            return {
                "error": "read the complete catalog and environment before authoring",
                "missing": missing,
            }
        return workspace.call(name, arguments)

    summary, turns, events = _converse(
        messages, model, workspace, trajectory, design_tools,
        max_turns=_TURNS_PER_ATTEMPT * attempts + _CLOSING_TURNS,
        limited_tool="validate", limit=attempts,
        done_when=lambda name, result: name == "submit" and "code" in result,
        tool_handler=handler)

    validated = [args["path"] for name, args, result in events
                 if name == "validate" and result.get("valid")]
    submissions = [result for name, _, result in events
                   if name == "submit" and "code" in result]
    return _outcome(trajectory,
                    validated_path=validated[-1] if validated else None,
                    code=submissions[-1]["code"] if submissions else None,
                    submitted_spec=submissions[-1].get("spec") if submissions else None,
                    followups_remaining=followups,
                    summary=summary,
                    attempts_used=sum(1 for name, _, _ in events if name == "validate"),
                    turns=turns)


class _DesignSpaceGate:
    """Track whether one fresh context has consulted the whole design space yet.

    Initial design and both follow-up contexts must read the catalog and the
    environment before acting on either. Holding the tracking here writes that
    rule once, so it cannot drift between design, follow-up selection, and
    follow-up authoring.

    :ivar required: Authoritative files this context has to read before acting.
    """

    def __init__(
        self, workspace: tools.Workspace, environment_path: Optional[str],
    ) -> None:
        self._workspace = workspace
        self.required = {Path(workspace.catalog_path).resolve()}
        if environment_path:
            self.required.add((workspace.root / environment_path).resolve())
        self._seen: set[Path] = set()

    def read_file(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Serve one read, remembering it only when content came back.

        :param arguments: Tool arguments as the model emitted them.
        :return: The read result, unchanged.
        :rtype: dict[str, Any]
        """
        result = self._workspace.call("read_file", arguments)
        if "text" in result:
            self._seen.add((self._workspace.root / arguments["path"]).resolve())
        return result

    def missing(self) -> list[str]:
        """Return the required files this context has not read yet.

        :return: Sorted paths, empty once the design space has been consulted.
        :rtype: list[str]
        """
        return sorted(str(path) for path in self.required - self._seen)


class _InterpretationGate:
    """Require validity-first reads and trace every cited evidence path."""

    def __init__(
        self,
        workspace: tools.Workspace,
        report_path: str,
        result_contract_path: str,
    ) -> None:
        self._workspace = workspace
        self.report = self._resolve(report_path)
        self.result_directory = self.report.parent.parent
        self.result_contract = self._resolve(result_contract_path)
        self.benchmarking = self.report.parent / "benchmarking.md"
        self.failed_checks = _report_failed_checks(self.report)
        self._read_paths: set[Path] = set()
        self._validity_read = False
        self.comparison_quality: dict[str, Any] | None = None

    def _resolve(self, path: str) -> Path:
        """Resolve one model-visible path against the workspace root."""
        source = Path(path)
        return source.resolve() if source.is_absolute() else (
            self._workspace.root / source
        ).resolve()

    def read_file(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Serve and record one successful evidence read."""
        result = self._workspace.call("read_file", arguments)
        if "text" not in result:
            return result
        source = self._resolve(arguments["path"])
        self._read_paths.add(source)
        section = str(result.get("section", "")).lstrip("# ").strip().casefold()
        if source == self.report and (not result.get("section") or section == "tests"):
            self._validity_read = True
            result["overall_status_failed"] = self.failed_checks
        return result

    def _unread(self, paths: Any) -> list[str] | None:
        """Return unread paths, or ``None`` when the path list is malformed."""
        if (
            not isinstance(paths, list) or not paths
            or any(not isinstance(path, str) or not path.strip() for path in paths)
        ):
            return None
        return sorted(
            path for path in paths if self._resolve(path) not in self._read_paths
        )

    def assess_comparison_quality(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Run and retain the deterministic comparison-quality assessment."""
        source = self._resolve(str(arguments.get("path", "")))
        if source != self.benchmarking:
            return {
                "error": "assess the benchmarking.md page beside the report index",
                "expected": str(self.benchmarking),
            }
        result = self._workspace.call("assess_comparison_quality", arguments)
        if "error" not in result:
            self.comparison_quality = result
            self._read_paths.add(source)
        return result

    def validate_record(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Validate one structured interpretation record."""
        missing_reads = []
        if self.report not in self._read_paths:
            missing_reads.append(str(self.report))
        if self.result_contract not in self._read_paths:
            missing_reads.append(str(self.result_contract))
        if not self._validity_read:
            missing_reads.append(f"{self.report} — whole file or Tests section")
        if missing_reads:
            return {"error": "read the report, validity checks, and result contract first",
                    "missing": missing_reads}
        if self.failed_checks is None:
            return {"error": "report frontmatter has no valid overall_status.failed count"}

        recorded_quality = arguments.get("comparison_quality")
        if self.benchmarking.is_file():
            if self.comparison_quality is None:
                return {
                    "error": "run assess_comparison_quality on benchmarking.md first",
                    "missing": [str(self.benchmarking)],
                }
            expected_quality = {
                "query_coverage": self.comparison_quality["query_coverage"],
                "whole_workload_throughput": self.comparison_quality[
                    "whole_workload_throughput"
                ],
                "suspect_repetitions": [
                    item["phase"]
                    for item in self.comparison_quality["suspect_repetitions"]
                ],
            }
        else:
            expected_quality = {
                "query_coverage": "not_applicable",
                "whole_workload_throughput": "not_applicable",
                "suspect_repetitions": [],
            }
        if recorded_quality != expected_quality:
            return {
                "error": "comparison_quality must match the deterministic assessment",
                "expected": expected_quality,
            }

        hypothesis_verdict = arguments.get("hypothesis_verdict")
        verdict_statuses = {"supported", "refuted", "inconclusive", "invalid"}
        if (
            not isinstance(hypothesis_verdict, dict)
            or hypothesis_verdict.get("status") not in verdict_statuses
            or not isinstance(hypothesis_verdict.get("conclusion"), str)
            or not hypothesis_verdict["conclusion"].strip()
        ):
            return {
                "error": (
                    "hypothesis_verdict needs a valid status and a non-empty conclusion"
                )
            }
        verdict_paths = hypothesis_verdict.get("evidence_paths")
        unread_verdict = self._unread(verdict_paths)
        if unread_verdict is None:
            return {"error": "hypothesis_verdict needs non-empty evidence_paths"}
        if unread_verdict:
            return {
                "error": "hypothesis_verdict cites unread evidence",
                "unread": unread_verdict,
            }
        outside_result = [
            path for path in verdict_paths
            if not self._resolve(path).is_relative_to(self.result_directory)
        ]
        if outside_result:
            return {
                "error": "hypothesis_verdict evidence must be inside this result folder",
                "outside": outside_result,
            }

        validity = arguments.get("validity")
        if not isinstance(validity, dict):
            return {"error": "validity must be an object"}
        failed_checks = validity.get("failed_checks")
        if failed_checks != self.failed_checks or isinstance(failed_checks, bool):
            return {
                "error": (
                    "validity.failed_checks must match report frontmatter: "
                    f"expected {self.failed_checks}"
                )
            }
        if not isinstance(validity.get("scope"), str):
            return {"error": "validity.scope must be text"}
        if self.failed_checks > 0 and not validity["scope"].strip():
            return {"error": "failed validity checks require a scope explanation"}
        unread_validity = self._unread(validity.get("evidence_paths"))
        if unread_validity is None:
            return {"error": "validity.evidence_paths must be a non-empty path list"}
        if unread_validity:
            return {"error": "validity cites unread evidence", "unread": unread_validity}
        if self.report not in {
            self._resolve(path) for path in validity["evidence_paths"]
        }:
            return {"error": "validity evidence must cite the report index"}

        questions = arguments.get("questions")
        if not isinstance(questions, list) or not questions:
            return {"error": "questions must be a non-empty list"}
        statuses = {"settled", "partial", "unresolved"}
        validity_states = {"supported", "limited", "invalid"}
        text_fields = {"question", "status", "conclusion", "evidence", "missing"}
        for question in questions:
            if (
                not isinstance(question, dict)
                or question.get("status") not in statuses
                or question.get("validity") not in validity_states
                or any(not isinstance(question.get(field), str) for field in text_fields)
            ):
                return {"error": "every question needs all text fields and valid states"}
            unread_evidence = self._unread(question.get("evidence_paths"))
            if unread_evidence is None:
                return {"error": "every question needs non-empty evidence_paths"}
            if unread_evidence:
                return {"error": "question cites unread evidence", "unread": unread_evidence}
            if question["status"] == "settled" and question["missing"].strip():
                return {"error": "a settled question cannot list missing evidence; "
                        "use partial or unresolved"}
            if question["status"] == "settled" and question["validity"] != "supported":
                return {"error": "a settled question requires supported evidence"}
            if question["status"] != "settled" and not question["missing"].strip():
                return {"error": "a partial or unresolved question must name missing evidence"}

        follow_up = arguments.get("follow_up")
        if not isinstance(follow_up, dict):
            return {"error": "follow_up must be an object"}
        action = follow_up.get("action")
        if action not in {"finish", "followup"}:
            return {"error": "follow_up.action must be finish or followup"}
        if not isinstance(follow_up.get("rationale"), str) or not follow_up["rationale"]:
            return {"error": "follow_up needs a rationale"}
        target_queries = follow_up.get("target_queries")
        if (
            not isinstance(target_queries, list)
            or any(
                isinstance(query, bool) or not isinstance(query, int)
                for query in target_queries
            )
        ):
            return {"error": "follow_up.target_queries must be a list of query numbers"}
        if not isinstance(follow_up.get("full_workload_required"), bool):
            return {"error": "follow_up.full_workload_required must be true or false"}
        if not isinstance(follow_up.get("cost_rationale"), str):
            return {"error": "follow_up.cost_rationale must be text"}
        if action == "followup" and (
            not follow_up.get("unresolved_question")
            or not follow_up.get("experiment_goal")
            or not follow_up.get("cost_rationale")
        ):
            return {
                "error": (
                    "a followup needs an unresolved question, experiment goal, "
                    "and cost rationale"
                )
            }
        if action == "followup" and target_queries and follow_up["full_workload_required"]:
            return {
                "error": (
                    "a focused target_queries list and full_workload_required=true "
                    "are mutually exclusive"
                )
            }
        if action == "finish" and (
            follow_up.get("unresolved_question")
            or follow_up.get("experiment_goal")
            or target_queries
            or follow_up["full_workload_required"]
        ):
            return {
                "error": (
                    "finish must leave unresolved_question, experiment_goal, and "
                    "target_queries empty, with full_workload_required=false"
                )
            }

        return {"recorded": True, "questions": len(questions)}


def _interpret_evidence(
    messages: list[dict[str, Any]],
    workspace: tools.Workspace,
    model: model_client.ChatModel,
    trajectory: Trajectory,
    report_path: str,
    result_contract_path: str,
) -> tuple[
    str, dict[str, Any], list[dict[str, Any]], dict[str, Any],
    dict[str, Any], dict[str, Any], list[Any], int,
]:
    """Read the finished result folder and record how far it answers the question.

    :param messages: Opening conversation for this context.
    :param workspace: Filesystem scope and tool implementations.
    :param model: The chat model to drive.
    :param trajectory: Event log for this investigation.
    :param report_path: Exact report entry point for this experiment.
    :param result_contract_path: Exact result contract governing the report.
    :return: Report, scientific verdict, question assessments, validity
        assessment, comparison quality, follow-up plan, events, and turns used.
    :rtype: tuple[str, dict[str, Any], list[dict[str, Any]], dict[str, Any],
        dict[str, Any], dict[str, Any], list, int]
    """
    hypothesis_verdict: dict[str, Any] = {}
    question_assessments: list[dict[str, Any]] = []
    validity_assessment: dict[str, Any] = {}
    comparison_quality: dict[str, Any] = {}
    follow_up: dict[str, Any] = {}
    workspace.restrict_to_result(report_path, result_contract_path)
    gate = _InterpretationGate(workspace, report_path, result_contract_path)

    def handler(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "read_file":
            return gate.read_file(arguments)
        if name == "assess_comparison_quality":
            return gate.assess_comparison_quality(arguments)
        if name != "record_interpretation":
            return workspace.call(name, arguments)
        result = gate.validate_record(arguments)
        if result.get("recorded"):
            hypothesis_verdict.update(arguments["hypothesis_verdict"])
            question_assessments[:] = arguments["questions"]
            validity_assessment.update(arguments["validity"])
            comparison_quality.update(arguments["comparison_quality"])
            follow_up.update(arguments["follow_up"])
        return result

    trajectory.record("stage", name="evidence_interpretation", context_reset=True)
    interpretation, turns, events = _converse(
        messages, model, workspace, trajectory, tools.INTERPRET_TOOLS,
        max_turns=_INTERPRET_TURNS + _CLOSING_TURNS,
        done_when=lambda name, result: name == "record_interpretation"
        and result.get("recorded") is True,
        tool_handler=handler, stage="evidence_interpretation",
        require_done=True)
    if gate.comparison_quality:
        comparison_quality["details"] = gate.comparison_quality
    return (
        interpretation, hypothesis_verdict, question_assessments, validity_assessment,
        comparison_quality, follow_up, events, turns,
    )


def _author_followup(
    task: str,
    specification: Optional[str],
    interpretation: str,
    decision: dict[str, Any],
    ancestor_summaries: list[dict[str, Any]],
    experiment_code: str,
    workspace: tools.Workspace,
    model: model_client.ChatModel,
    trajectory: Trajectory,
    catalog_path: str,
    environment_path: Optional[str],
    attempts: int,
    dry_run: bool,
) -> tuple[str, list[Any], int]:
    """Write and submit the chosen follow-up in another fresh mutation context.

    :param task: The original question, verbatim.
    :param specification: The experiment that produced the preceding evidence.
    :param interpretation: The closing interpretation of that evidence.
    :param decision: The recorded follow-up decision being acted on.
    :param ancestor_summaries: Compact records from earlier lineage members.
    :param experiment_code: Parent result code required by ``follow_up_of``.
    :param workspace: Filesystem scope and tool implementations.
    :param model: The chat model to drive.
    :param trajectory: Event log for this investigation.
    :param catalog_path: Path the agent is told to read the catalog from.
    :param environment_path: Path to the environment descriptor, or ``None``.
    :param attempts: How many validate calls the agent may make.
    :param dry_run: Withhold the submission tool so nothing reaches the cluster.
    :return: Closing account, events, and turns used.
    :rtype: tuple[str, list, int]
    """
    workspace.restore_design_reads()
    gate = _DesignSpaceGate(workspace, environment_path)

    try:
        parent_experiment = yaml.safe_load(specification) if specification else None
    except yaml.YAMLError:
        parent_experiment = None

    def methodology_error(message: str, path: str) -> dict[str, Any]:
        """Reject a follow-up before shared validation can approve it."""
        workspace.invalidate_validation(path)
        return {
            "valid": False,
            "errors": [{"stage": "methodology", "message": message}],
            "environment_checked": False,
            "estimate": {"runs": None, "duration_min": None},
        }

    def handler(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "read_file":
            return gate.read_file(arguments)
        if name == "write_file" and (missing := gate.missing()):
            return {"error": "read the complete catalog and environment before authoring",
                    "missing": missing}
        if name == "validate":
            draft = workspace.call("read_file", {"path": arguments.get("path", "")})
            if "text" not in draft:
                return draft
            try:
                experiment = yaml.safe_load(draft["text"])
            except yaml.YAMLError:
                experiment = None
            if not isinstance(experiment, dict):
                return methodology_error("the follow-up must be a YAML object", arguments["path"])
            if experiment.get("follow_up_of") != experiment_code:
                return methodology_error(
                    f"follow_up_of must equal the parent experiment code {experiment_code!r}",
                    arguments["path"],
                )
            if isinstance(parent_experiment, dict):
                ignored = {"title", "hypothesis", "discriminates", "follow_up_of"}
                parent_execution = {
                    key: value for key, value in parent_experiment.items() if key not in ignored
                }
                followup_execution = {
                    key: value for key, value in experiment.items() if key not in ignored
                }
                if followup_execution == parent_execution:
                    return methodology_error(
                        "the follow-up repeats its parent's execution settings; "
                        "change at least one controlled treatment",
                        arguments["path"],
                    )
            if decision.get("target_queries"):
                try:
                    active_queries = experiment["workload"]["params"]["active_queries"]
                except (KeyError, TypeError):
                    active_queries = None
            else:
                active_queries = None
            if decision.get("target_queries"):
                expected = sorted(set(decision["target_queries"]))
                actual = (
                    sorted(set(active_queries)) if isinstance(active_queries, list) else None
                )
                if actual != expected:
                    return methodology_error(
                        "the approved cost-aware follow-up requires "
                        f"workload.params.active_queries={expected}, got {active_queries!r}",
                        arguments["path"],
                    )
        return workspace.call(name, arguments)

    trajectory.record("stage", name="followup_authoring", context_reset=True)
    messages = prompts.followup_author_messages(
        task=task, specification=specification, interpretation=interpretation,
        decision=decision, ancestor_summaries=ancestor_summaries,
        experiment_code=experiment_code, catalog_path=catalog_path,
        environment_path=environment_path, inbox=workspace.inbox.name,
        attempts=attempts, dry_run=dry_run)
    author_tools = tools.FOLLOWUP_AUTHOR_TOOLS
    if dry_run:
        author_tools = tools.without_submit(author_tools)
    summary, turns, events = _converse(
        messages, model, workspace, trajectory, author_tools,
        max_turns=_TURNS_PER_ATTEMPT * attempts + _CLOSING_TURNS,
        limited_tool="validate", limit=attempts,
        done_when=(
            (lambda name, result: name == "validate" and result.get("valid") is True)
            if dry_run else
            (lambda name, result: name == "submit" and "code" in result)
        ),
        tool_handler=handler, stage="followup_authoring")
    return summary, events, turns


def run_interpret(
    task: str,
    report_path: str,
    specification: Optional[str],
    workspace: tools.Workspace,
    model: model_client.ChatModel,
    trajectory: Trajectory,
    result_contract_path: str,
    followups: int = _DEFAULT_FOLLOWUPS,
    catalog_path: str = _DEFAULT_CATALOG,
    environment_path: Optional[str] = _DEFAULT_ENVIRONMENT,
    attempts: int = _DEFAULT_ATTEMPTS,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Read a finished result folder and say what it means.

    :param task: The original question, verbatim.
    :param report_path: Entry point of the finished result folder.
    :param specification: The experiment that ran, or ``None`` if unavailable.
    :param workspace: Filesystem scope and tool implementations.
    :param model: The chat model to drive.
    :param trajectory: Event log for this run.
    :param result_contract_path: Path to ``contract_result.yml``.
    :param followups: Follow-up experiments still available.
    :return: Interpretation summary, evidence reads, and any follow-up submission.
    :rtype: dict[str, Any]
    """
    messages = prompts.interpret_messages(
        task=task, report_path=report_path, result_contract_path=result_contract_path,
        specification=specification)
    trajectory.record("meta", phase="interpret", model=model.model,
                      params={"temperature": model.temperature, "max_tokens": model.max_tokens},
                      report=report_path,
                      catalog_sha256=_file_sha256(catalog_path),
                      environment_sha256=_file_sha256(environment_path),
                      result_contract_sha256=_file_sha256(result_contract_path),
                      budgets={"followups": followups})
    trajectory.record("task", text=task)

    (
        interpretation,
        hypothesis_verdict,
        question_assessments,
        validity_assessment,
        comparison_quality,
        decision,
        all_events,
        total_turns,
    ) = _interpret_evidence(
        messages, workspace, model, trajectory, report_path, result_contract_path
    )
    all_events = list(all_events)
    author_summary = ""
    report = Path(report_path)
    report = (
        report.resolve()
        if report.is_absolute() else (workspace.root / report).resolve()
    )
    result_directory = report.parent.parent
    experiment_code = result_directory.name
    agent_summary_path, agent_summary = _write_agent_summary(
        report_path=report_path, specification=specification,
        hypothesis_verdict=hypothesis_verdict, validity=validity_assessment,
        follow_up=decision, root=workspace.root,
    )
    trajectory.record("artifact", phase="interpret",
                      agent_summary=str(agent_summary_path))
    ancestor_summaries = _load_ancestor_summaries(
        result_directory, agent_summary.get("follow_up_of")
    )

    if decision.get("action") == "followup" and followups > 0:
        author_summary, author_events, author_turns = _author_followup(
            task=task, specification=specification, interpretation=interpretation,
            decision=decision, ancestor_summaries=ancestor_summaries,
            experiment_code=experiment_code,
            workspace=workspace, model=model,
            trajectory=trajectory, catalog_path=catalog_path,
            environment_path=environment_path, attempts=attempts, dry_run=dry_run)
        all_events.extend(author_events)
        total_turns += author_turns

    summary_parts = [interpretation] if interpretation else []
    if decision.get("action") == "followup" and followups > 0:
        summary_parts.append(author_summary or (
            "A follow-up was selected but was not submitted: " + decision.get("rationale", "")
        ))
    summary = "\n\n".join(part for part in summary_parts if part)

    reads = [result for name, _, result in all_events if name == "read_file" and "bytes" in result]
    validated = [args["path"] for name, args, result in all_events
                 if name == "validate" and result.get("valid")]
    submissions = [result for name, _, result in all_events if name == "submit" and "code" in result]
    phase_complete = bool(interpretation) and bool(decision) and (
        decision.get("action") != "followup" or followups <= 0 or bool(submissions)
        or (dry_run and bool(validated))
    )
    return _outcome(trajectory, summary=summary, turns=total_turns,
                    validated_path=validated[-1] if validated else None,
                    code=submissions[-1]["code"] if submissions else None,
                    submitted_spec=submissions[-1].get("spec") if submissions else None,
                    followups_remaining=max(0, followups - len(submissions)),
                    question_assessments=question_assessments,
                    hypothesis_verdict=hypothesis_verdict,
                    validity_assessment=validity_assessment,
                    comparison_quality=comparison_quality,
                    followup_decision=decision or None,
                    agent_summary_path=str(agent_summary_path),
                    ancestor_summaries_loaded=len(ancestor_summaries),
                    phase_complete=phase_complete,
                    files_read=[result["path"] for result in reads],
                    bytes_read=sum(result["bytes"] for result in reads),
                    characters_returned=sum(
                        result.get("returned_characters", 0) for result in reads
                    ))


def _carry_forward(
    run_directory: Path, root: Path,
) -> tuple[str, Optional[str], Optional[str], Optional[int]]:
    """Rebuild what the next phase needs from an investigation's log.

    Deterministic on purpose: the task verbatim, the specification that ran and
    the experiment code are kept, and the rejected drafts that preceded them are
    dropped. They stay in the log for anyone analysing how many attempts a run
    took; they simply do not belong in the context used to read results.

    :param run_directory: Directory of the investigation being continued.
    :param root: Repository root, for resolving the specification path.
    :return: Task, current specification, experiment code, and remaining
        follow-up budget.
    """
    task, spec_path, code, followups = "", None, None, None
    for line in (run_directory / "trajectory.jsonl").read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event["type"] == "task":
            task = event["text"]
        elif event["type"] == "meta":
            followups = event.get("budgets", {}).get("followups", followups)
            if event.get("phase") == "interpret" and event.get("report"):
                code = Path(event["report"]).parent.parent.name
        elif event["type"] == "outcome":
            spec_path = event.get("submitted_spec") or event.get("validated_path") or spec_path
            code = event.get("code") or code
            followups = event.get("followups_remaining", followups)
    specification = None
    archived = run_directory / "submitted-experiment.yml"
    if not archived.is_file():
        phase_archives = sorted(
            (run_directory / "phases").glob("*/submitted-experiment.yml")
        )
        if phase_archives:
            archived = phase_archives[-1]
    source = archived if archived.is_file() else (root / spec_path if spec_path else None)
    if source and source.is_file():
        specification = source.read_text(encoding="utf-8")
    return task, specification, code, followups


def _build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser.

    :return: Configured parser.
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Design an experiment and submit it, or interpret a finished one.")
    parser.add_argument("-p", "--phase", choices=("design", "interpret"), default="design")
    parser.add_argument("-t", "--task", help="question to answer; required for design")
    parser.add_argument(
        "--run", help="investigation directory to continue (interpret phase)"
    )
    parser.add_argument(
        "--report", help="exact report/index.md to interpret without local status state"
    )
    parser.add_argument("-m", "--model", default=os.environ.get("AGENT_MODEL"),
                        help="model identifier the server serves (default: $AGENT_MODEL)")
    parser.add_argument("-u", "--base-url", default=os.environ.get("AGENT_BASE_URL", _DEFAULT_BASE_URL))
    parser.add_argument("-k", "--api-key", default=os.environ.get("AGENT_API_KEY", "EMPTY"))
    parser.add_argument("-r", "--root", default=os.getcwd())
    parser.add_argument("-i", "--inbox", default=_DEFAULT_INBOX)
    parser.add_argument("-c", "--catalog", default=_DEFAULT_CATALOG)
    parser.add_argument("-e", "--environment", default=_DEFAULT_ENVIRONMENT,
                        help="pass an empty string only for a dry run")
    parser.add_argument("-R", "--results", default=os.environ.get("AGENT_RESULTS"),
                        help="bexhoma's result folder; defaults to the resultfolder "
                             "declared in cluster.config")
    parser.add_argument("-d", "--trajectories", default=_DEFAULT_TRAJECTORIES)
    parser.add_argument("--status", default="status")
    parser.add_argument("-a", "--attempts", type=int, default=_DEFAULT_ATTEMPTS)
    parser.add_argument("-f", "--followups", type=int, default=_DEFAULT_FOLLOWUPS)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=_DEFAULT_MAX_TOKENS,
                        help="ceiling on tokens generated per turn, thinking included")
    parser.add_argument("--dry-run", action="store_true",
                        help="design and validate only; do not submit to the cluster")
    return parser


def _phase_number(run_directory: Path) -> int:
    """Return the next one-based phase number in an investigation."""
    log = run_directory / "trajectory.jsonl"
    if not log.is_file():
        return 1
    count = 0
    for line in log.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "meta" and event.get("phase") in {"design", "interpret"}:
            count += 1
    return count + 1


def _resolve_investigation(root: Path, value: str) -> Path:
    """Resolve ``--run`` relative to the repository for predictable replay."""
    path = Path(value)
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def _name_component(value: Any) -> str:
    """Return one filesystem-safe component for investigation metadata."""
    return re.sub(r"[^A-Za-z0-9._-]+", "-", str(value)).strip("-._")


def _label_design_investigation(
    run_directory: Path,
    trajectory: Trajectory,
    root: Path,
    status_directory: Path,
    model: str,
    outcome: dict[str, Any],
) -> Path:
    """Add the validated scale factor and model to a completed design directory."""
    specification_value = outcome.get("submitted_spec") or outcome.get("validated_path")
    if not specification_value:
        return run_directory
    specification_path = Path(str(specification_value))
    if not specification_path.is_absolute():
        specification_path = root / specification_path
    try:
        specification = yaml.safe_load(specification_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return run_directory
    if not isinstance(specification, dict):
        return run_directory
    workload = specification.get("workload")
    params = workload.get("params") if isinstance(workload, dict) else None
    scale_factor = params.get("scaling_factor") if isinstance(params, dict) else None
    scale_component = _name_component(scale_factor) if scale_factor is not None else ""
    model_component = _name_component(model)
    if not scale_component or not model_component:
        return run_directory

    labelled_directory = run_directory.with_name(
        f"{run_directory.name}-sf{scale_component}-{model_component}"
    )
    if labelled_directory.exists():
        trajectory.record(
            "investigation_label_skipped",
            reason="target directory already exists",
            target=str(labelled_directory),
        )
        return run_directory
    previous_directory = run_directory
    run_directory.rename(labelled_directory)
    code = outcome.get("code")
    status_file = status_directory / f"{code}.json" if code else None
    if status_file is not None and status_file.is_file():
        try:
            status = json.loads(status_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            status = None
        if isinstance(status, dict):
            for key in ("spec", "log"):
                value = status.get(key)
                if not isinstance(value, str):
                    continue
                try:
                    relative_path = Path(value).relative_to(previous_directory)
                except ValueError:
                    continue
                status[key] = str(labelled_directory / relative_path)
            provenance = status.get("provenance")
            if isinstance(provenance, dict):
                for key, value in provenance.items():
                    if not isinstance(value, str):
                        continue
                    try:
                        relative_path = Path(value).relative_to(previous_directory)
                    except ValueError:
                        continue
                    provenance[key] = str(labelled_directory / relative_path)
            status_file.write_text(json.dumps(status, indent=2), encoding="utf-8")
    trajectory.directory = labelled_directory
    trajectory.path = labelled_directory / "trajectory.jsonl"
    trajectory.record(
        "investigation_relocated",
        previous_name=previous_directory.name,
        current_name=labelled_directory.name,
        scaling_factor=scale_factor,
        model=model,
    )
    return labelled_directory


def _write_reports(
    run_directory: Path,
    trajectory: Trajectory,
    phase_number: int,
    phase: str,
    summary: str,
    final: bool,
) -> tuple[Path, Optional[Path]]:
    """Preserve a phase account and expose a completed interpretation as the answer."""
    reports = run_directory / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    phase_report = reports / f"{phase_number:02d}-{phase}.md"
    phase_report.write_text(summary + "\n", encoding="utf-8")
    final_report: Optional[Path] = None
    if final:
        final_report = run_directory / "answer.md"
        final_report.write_text(summary + "\n", encoding="utf-8")
    trajectory.record(
        "artifact", phase=phase, phase_number=phase_number,
        phase_report=str(phase_report),
        final_report=str(final_report) if final_report else None,
    )
    return phase_report, final_report


def _report_unreachable(
    error: model_client.ModelUnreachable, base_url: str, trajectory: Trajectory,
) -> int:
    """Report an endpoint that never answered, the way setup mistakes are reported.

    :param error: The failure raised by the model adapter.
    :param base_url: Endpoint the phase was configured to use.
    :param trajectory: Event log, so an abandoned phase is still auditable.
    :return: Process exit code.
    :rtype: int
    """
    trajectory.record("aborted", reason="model endpoint unreachable", base_url=base_url)
    print(f"error: no answer from the model endpoint at {base_url}. Check that a "
          "server is running there and that --base-url matches it, including the "
          "/v1 suffix most OpenAI-compatible servers expect; pass --base-url or "
          "set AGENT_BASE_URL.", file=sys.stderr)
    print(f"  {error}", file=sys.stderr)
    return 2


def _report_context_exhausted(
    error: model_client.ContextWindowExhausted, max_tokens: int, trajectory: Trajectory,
) -> int:
    """Report a conversation that outgrew the server's context window.

    :param error: The failure raised by the model adapter.
    :param max_tokens: Per-turn ceiling the phase was configured with.
    :param trajectory: Event log, so an abandoned phase is still auditable.
    :return: Process exit code.
    :rtype: int
    """
    trajectory.record("aborted", reason="context window exhausted", max_tokens=max_tokens)
    print("error: the conversation no longer leaves room for an answer within the "
          f"model server's context window. Lower --max-tokens (currently {max_tokens}) "
          "so each turn reserves less, or rerun the phase so it starts from a fresh "
          "context.", file=sys.stderr)
    print(f"  {error}", file=sys.stderr)
    return 2


def main() -> int:
    """Run one phase from the command line.

    :return: Process exit code; zero when the phase produced what it should.
    :rtype: int
    """
    # Fills AGENT_MODEL/AGENT_BASE_URL/AGENT_API_KEY from the repository's .env
    # when they are not already exported, so the parser defaults below see them.
    # A real environment variable wins over the file, and a flag over both.
    load_dotenv()
    args = _build_parser().parse_args()
    if not args.model:
        print("error: no model given; pass --model or set AGENT_MODEL", file=sys.stderr)
        return 2

    root = Path(args.root).resolve()
    explicit_report = (
        _resolve_investigation(root, args.report) if args.report else None
    )
    if explicit_report is not None and (
        explicit_report.name != "index.md" or explicit_report.parent.name != "report"
    ):
        print("error: --report must name a report/index.md entry point", file=sys.stderr)
        return 2
    results = Path(args.results).resolve() if args.results else tools.default_result_root(root)
    if results is None and args.phase == "interpret" and explicit_report is not None:
        results = explicit_report.parent.parent.parent
    if results is None:
        print("error: no result folder. Bexhoma reads one from cluster.config "
              "(cp k8s-cluster.config cluster.config), or pass --results / set "
              "AGENT_RESULTS", file=sys.stderr)
        return 2
    trajectories = root / args.trajectories
    source: Optional[Path] = None
    if args.phase == "design":
        run_directory = trajectories / datetime.now().strftime("%Y%m%dT%H%M%S%f")
    else:
        source = _resolve_investigation(root, args.run) if args.run else None
        if source is not None and not (source / "trajectory.jsonl").is_file():
            print(f"error: investigation has no trajectory: {source}", file=sys.stderr)
            return 2
        if source is None and not args.report:
            print("error: interpretation requires --run or --report", file=sys.stderr)
            return 2
        run_directory = source or (
            trajectories / datetime.now().strftime("%Y%m%dT%H%M%S%f")
        )

    phase_number = _phase_number(run_directory)
    phase_directory = run_directory / "phases" / f"{phase_number:02d}-{args.phase}"
    phase_directory.mkdir(parents=True, exist_ok=True)
    trajectory = Trajectory(run_directory)
    model = model_client.ChatModel(model=args.model, base_url=args.base_url,
                                   api_key=args.api_key, temperature=args.temperature,
                                   max_tokens=args.max_tokens)
    workspace = tools.Workspace(
        root=str(root), inbox=args.inbox, catalog_path=args.catalog,
        environment_path=args.environment or None, results_root=str(results),
        status_dir=args.status, run_directory=phase_directory)

    if args.phase == "design":
        if not args.task:
            print("error: --task is required for the design phase", file=sys.stderr)
            return 2
        catalog = root / args.catalog
        if not catalog.is_file():
            print(f"error: catalog not found at {catalog}", file=sys.stderr)
            return 2
        (run_directory / "task.txt").write_text(args.task + "\n", encoding="utf-8")
        try:
            outcome = run_design(
                task=args.task, workspace=workspace, model=model, trajectory=trajectory,
                catalog_path=args.catalog,
                catalog_sha256=hashlib.sha256(catalog.read_bytes()).hexdigest(),
                environment_path=(
                    args.environment if (root / args.environment).is_file() else None
                ),
                attempts=args.attempts, followups=args.followups, dry_run=args.dry_run)
        except model_client.ModelUnreachable as error:
            return _report_unreachable(error, args.base_url, trajectory)
        except model_client.ContextWindowExhausted as error:
            return _report_context_exhausted(error, args.max_tokens, trajectory)
    else:
        if source is not None:
            task, specification, code, carried_followups = _carry_forward(source, root)
        else:
            task, specification, code, carried_followups = args.task or "", None, None, None
        report = explicit_report if explicit_report is not None else (
            results / str(code) / "report" / "index.md"
        )
        if not report.is_file():
            print(f"error: finished report not found: {report}", file=sys.stderr)
            return 2
        result_directory = report.parent.parent
        code = result_directory.name
        archived_specification = result_directory / "experiment.yml"
        if archived_specification.is_file():
            specification = archived_specification.read_text(encoding="utf-8")
            if not task:
                try:
                    experiment = yaml.safe_load(specification)
                except yaml.YAMLError:
                    experiment = None
                if isinstance(experiment, dict):
                    task = str(
                        experiment.get("hypothesis")
                        or experiment.get("title")
                        or "Interpret this experiment."
                    )
        if not task:
            task = "Interpret this experiment according to its result contract."
        task_file = run_directory / "task.txt"
        if not task_file.is_file():
            task_file.write_text(task + "\n", encoding="utf-8")
        result_contract = result_directory / "contract_result.yml"
        try:
            outcome = run_interpret(
                task=task, report_path=str(report), specification=specification,
                workspace=workspace, model=model, trajectory=trajectory,
                result_contract_path=(
                    str(result_contract) if result_contract.is_file()
                    else _DEFAULT_RESULT_CONTRACT
                ),
                followups=min(args.followups, carried_followups)
                if carried_followups is not None else args.followups,
                catalog_path=args.catalog,
                environment_path=(
                    args.environment if (root / args.environment).is_file() else None
                ),
                attempts=args.attempts, dry_run=args.dry_run)
        except model_client.ModelUnreachable as error:
            return _report_unreachable(error, args.base_url, trajectory)
        except model_client.ContextWindowExhausted as error:
            return _report_context_exhausted(error, args.max_tokens, trajectory)

    if not outcome.get("summary"):
        print("error: the model produced no closing answer; it most likely spent the "
              "whole per-turn token budget thinking. Raise --max-tokens and retry.",
              file=sys.stderr)
    complete = outcome.get("phase_complete")
    if complete is None:
        complete = bool(outcome.get("summary")) and (
            args.phase == "interpret" or args.dry_run or bool(outcome.get("code"))
        )
    final = bool(complete) and not outcome.get("code")
    if args.phase == "design" and complete:
        previous_directory = run_directory
        run_directory = _label_design_investigation(
            run_directory, trajectory, root, workspace.status_dir, args.model, outcome
        )
        if run_directory != previous_directory:
            phase_directory = run_directory / phase_directory.relative_to(
                previous_directory
            )
            workspace.run_directory = phase_directory
    phase_report, _ = _write_reports(
        run_directory, trajectory, phase_number, args.phase,
        outcome["summary"] or "", final,
    )

    print(f"investigation: {run_directory}")
    print(f"trajectory: {trajectory.path}")
    print(f"phase report: {phase_report}")
    for key in ("validated_path", "code", "files_read", "bytes_read", "characters_returned"):
        if outcome.get(key):
            print(f"  {key}: {outcome[key]}")
    return 0 if complete else 1


if __name__ == "__main__":
    sys.exit(main())
