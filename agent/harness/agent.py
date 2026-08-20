"""The agent loop: design an experiment, submit it, then interpret what came back.

One reusable tool-calling loop drives bounded contexts with different prompts,
tools, and stopping rules. Each invocation is one phase of an investigation.
Every phase appends to the investigation's single trajectory; separate phase
reports preserve local detail and the final interpretation becomes the required
aggregated human-facing report. Durable state is rebuilt from the event log
rather than from model memory.

    python -m agent.harness.agent --task "..."          # design and submit
    python -m agent.harness.agent --phase interpret     # read the newest result

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
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from agent.harness import model_client, prompts, tools

__all__ = ["Trajectory", "run_design", "run_interpret"]

_DEFAULT_INBOX = "inbox"
_DEFAULT_CATALOG = os.path.join("contracts", "contract_catalog.yml")
_DEFAULT_RESULT_CONTRACT = os.path.join("contracts", "contract_result.yml")
_DEFAULT_ENVIRONMENT = os.path.join("dev", "catalog", "environment.yml")
_DEFAULT_TRAJECTORIES = os.path.join("agent", "trajectories")
_DEFAULT_RESULTS = "/home/ll/benchmarks"
_DEFAULT_BASE_URL = "http://localhost:8000/v1"

#: Validate calls allowed per run: one first attempt plus two repairs.
_DEFAULT_ATTEMPTS = 3
#: Follow-up experiments the agent is told it will be offered.
_DEFAULT_FOLLOWUPS = 1
#: Tokens a single turn may generate, thinking included. A reasoning model
#: reading a large report needs room to think and still write its answer.
_DEFAULT_MAX_TOKENS = 16384

#: A follow-up starts with a fresh conversation. Preserve the previous result's
#: conclusion and specification, but keep that handoff predictably small.
_HANDOFF_SUMMARY_CHARACTER_LIMIT = 6_000
_HANDOFF_SPECIFICATION_CHARACTER_LIMIT = 8_000

#: Turns allowed per validation attempt. Four cover read, read, write, validate;
#: the slack absorbs a model that narrates or rewrites before validating.
_TURNS_PER_ATTEMPT = 6
#: Turns allowed for reading a result folder, which is many small reads.
_INTERPRET_TURNS = 24
#: A fresh follow-up gate needs only two authoritative reads and one decision.
_FOLLOWUP_DECISION_TURNS = 8
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

    summary, turns, events = _converse(
        messages, model, workspace, trajectory, tools.DESIGN_TOOLS,
        max_turns=_TURNS_PER_ATTEMPT * attempts + _CLOSING_TURNS,
        limited_tool="validate", limit=attempts,
        done_when=lambda name, result: name == "submit" and "code" in result)

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
    previous_experiment: Optional[dict[str, Any]] = None,
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
    :param previous_experiment: Bounded result/specification handoff from the
        preceding experiment in a follow-up chain.
    :return: Interpretation summary, evidence reads, and any follow-up submission.
    :rtype: dict[str, Any]
    """
    messages = prompts.interpret_messages(
        task=task, report_path=report_path, result_contract_path=result_contract_path,
        specification=specification, previous_experiment=previous_experiment)
    trajectory.record("meta", phase="interpret", model=model.model,
                      params={"temperature": model.temperature, "max_tokens": model.max_tokens},
                      report=report_path,
                      catalog_sha256=_file_sha256(catalog_path),
                      environment_sha256=_file_sha256(environment_path),
                      result_contract_sha256=_file_sha256(result_contract_path),
                      previous_report=(previous_experiment or {}).get("report"),
                      budgets={"followups": followups})
    trajectory.record("task", text=task)

    question_assessments: list[dict[str, Any]] = []

    def interpret_handler(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name != "record_interpretation":
            return workspace.call(name, arguments)
        questions = arguments.get("questions")
        if not isinstance(questions, list) or not questions:
            return {"error": "questions must be a non-empty list"}
        statuses = {"settled", "partial", "unresolved"}
        fields = {"question", "status", "conclusion", "evidence", "missing"}
        if any(not isinstance(item, dict) or item.get("status") not in statuses
               or any(not isinstance(item.get(field), str) for field in fields)
               for item in questions):
            return {"error": "every question needs all text fields and a valid status"}
        if any(item["status"] == "settled" and item["missing"].strip()
               for item in questions):
            return {"error": "a settled question cannot list missing evidence; "
                    "use partial or unresolved"}
        question_assessments[:] = questions
        return {"recorded": True, "questions": len(questions)}

    trajectory.record("stage", name="evidence_interpretation", context_reset=True)
    interpretation, interpret_turns, interpret_events = _converse(
        messages, model, workspace, trajectory, tools.INTERPRET_TOOLS,
        max_turns=_INTERPRET_TURNS + _CLOSING_TURNS,
        done_when=lambda name, result: name == "record_interpretation"
        and result.get("recorded") is True,
        tool_handler=interpret_handler, stage="evidence_interpretation",
        require_done=True)

    all_events = list(interpret_events)
    total_turns = interpret_turns
    decision: dict[str, str] = {}
    author_summary = ""

    if followups > 0 and interpretation:
        workspace.reset_read_context()
        required = {Path(workspace.catalog_path).resolve()}
        if environment_path:
            required.add((workspace.root / environment_path).resolve())
        decision_reads: set[Path] = set()

        def decision_handler(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
            if name == "read_file":
                result = workspace.call(name, arguments)
                if "text" in result:
                    decision_reads.add((workspace.root / arguments["path"]).resolve())
                return result
            if name != "record_followup_decision":
                return workspace.call(name, arguments)
            missing = sorted(str(path) for path in required - decision_reads)
            if missing:
                return {"error": "read the complete design space before deciding",
                        "missing": missing}
            action = arguments.get("action")
            if action not in {"finish", "followup"}:
                return {"error": "action must be finish or followup"}
            if not isinstance(arguments.get("rationale"), str) or not arguments["rationale"]:
                return {"error": "the decision needs a rationale"}
            if action == "followup" and (
                not arguments.get("unresolved_question") or not arguments.get("experiment_goal")
            ):
                return {"error": "a followup needs an unresolved question and experiment goal"}
            if action == "finish" and (
                arguments.get("unresolved_question") or arguments.get("experiment_goal")
            ):
                return {"error": "finish must leave unresolved_question and experiment_goal empty"}
            decision.clear()
            decision.update({key: str(arguments.get(key, "")) for key in (
                "action", "rationale", "unresolved_question", "experiment_goal",
            )})
            return {"recorded": True, "action": action}

        trajectory.record("stage", name="followup_decision", context_reset=True)
        decision_messages = prompts.followup_decision_messages(
            task=task, specification=specification, interpretation=interpretation,
            question_assessments=question_assessments, catalog_path=catalog_path,
            environment_path=environment_path)
        _, decision_turns, decision_events = _converse(
            decision_messages, model, workspace, trajectory, tools.FOLLOWUP_DECISION_TOOLS,
            max_turns=_FOLLOWUP_DECISION_TURNS + _CLOSING_TURNS,
            done_when=lambda name, result: name == "record_followup_decision"
            and result.get("recorded") is True,
            tool_handler=decision_handler, stage="followup_decision",
            require_done=True)
        all_events.extend(decision_events)
        total_turns += decision_turns

    if decision.get("action") == "followup":
        workspace.reset_read_context()
        required = {Path(workspace.catalog_path).resolve()}
        if environment_path:
            required.add((workspace.root / environment_path).resolve())
        author_reads: set[Path] = set()

        def author_handler(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
            if name == "read_file":
                result = workspace.call(name, arguments)
                if "text" in result:
                    author_reads.add((workspace.root / arguments["path"]).resolve())
                return result
            if name == "write_file" and required - author_reads:
                return {"error": "read the complete catalog and environment before authoring",
                        "missing": sorted(str(path) for path in required - author_reads)}
            return workspace.call(name, arguments)

        trajectory.record("stage", name="followup_authoring", context_reset=True)
        author_messages = prompts.followup_author_messages(
            task=task, specification=specification, interpretation=interpretation,
            decision=decision, catalog_path=catalog_path,
            environment_path=environment_path, inbox=workspace.inbox.name,
            attempts=attempts, dry_run=dry_run)
        author_tools = tools.FOLLOWUP_AUTHOR_TOOLS
        if dry_run:
            author_tools = [schema for schema in author_tools
                            if schema["function"]["name"] != "submit"]
        author_summary, author_turns, author_events = _converse(
            author_messages, model, workspace, trajectory, author_tools,
            max_turns=_TURNS_PER_ATTEMPT * attempts + _CLOSING_TURNS,
            limited_tool="validate", limit=attempts,
            done_when=(
                (lambda name, result: name == "validate" and result.get("valid") is True)
                if dry_run else
                (lambda name, result: name == "submit" and "code" in result)
            ),
            tool_handler=author_handler, stage="followup_authoring")
        all_events.extend(author_events)
        total_turns += author_turns

    summary_parts = [interpretation] if interpretation else []
    if decision.get("action") == "finish" and decision.get("rationale"):
        summary_parts.append("Follow-up decision: " + decision["rationale"])
    elif decision.get("action") == "followup":
        summary_parts.append(author_summary or (
            "A follow-up was selected but was not submitted: " + decision.get("rationale", "")
        ))
    summary = "\n\n".join(part for part in summary_parts if part)

    reads = [result for name, _, result in all_events if name == "read_file" and "bytes" in result]
    validated = [args["path"] for name, args, result in all_events
                 if name == "validate" and result.get("valid")]
    submissions = [result for name, _, result in all_events if name == "submit" and "code" in result]
    phase_complete = bool(interpretation) and (
        followups <= 0 or bool(decision)
    ) and (
        decision.get("action") != "followup" or bool(submissions)
        or (dry_run and bool(validated))
    )
    return _outcome(trajectory, summary=summary, turns=total_turns,
                    validated_path=validated[-1] if validated else None,
                    code=submissions[-1]["code"] if submissions else None,
                    submitted_spec=submissions[-1].get("spec") if submissions else None,
                    followups_remaining=followups - len(submissions),
                    question_assessments=question_assessments,
                    followup_decision=decision or None,
                    phase_complete=phase_complete,
                    files_read=[result["path"] for result in reads],
                    bytes_read=sum(result["bytes"] for result in reads),
                    characters_returned=sum(
                        result.get("returned_characters", 0) for result in reads
                    ))


def _carry_forward(
    run_directory: Path, root: Path,
) -> tuple[str, Optional[str], Optional[str], Optional[int], Optional[dict[str, Any]]]:
    """Rebuild what the next phase needs from an investigation's log.

    Deterministic on purpose: the task verbatim, the specification that ran and
    the experiment code are kept, and the rejected drafts that preceded them are
    dropped. They stay in the log for anyone analysing how many attempts a run
    took; they simply do not belong in the context used to read results.

    :param run_directory: Directory of the investigation being continued.
    :param root: Repository root, for resolving the specification path.
    :return: Task, specification, experiment code, remaining follow-up budget,
        and a bounded previous-experiment handoff when continuing a follow-up.
    """
    task, spec_path, code, followups = "", None, None, None
    phase, previous_report, previous_summary, previous_followup_decision = (
        None, None, None, None
    )
    for line in (run_directory / "trajectory.jsonl").read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event["type"] == "task":
            task = event["text"]
        elif event["type"] == "meta":
            phase = event.get("phase", phase)
            followups = event.get("budgets", {}).get("followups", followups)
            if event.get("phase") == "interpret" and event.get("report"):
                previous_report = event["report"]
                code = Path(previous_report).parent.parent.name
        elif event["type"] == "outcome":
            spec_path = event.get("submitted_spec") or event.get("validated_path") or spec_path
            code = event.get("code") or code
            followups = event.get("followups_remaining", followups)
            if phase == "interpret" and event.get("summary"):
                previous_summary = event["summary"]
                previous_followup_decision = event.get("followup_decision")
    specification = None
    archived = run_directory / "submitted-experiment.yml"
    source = archived if archived.is_file() else (root / spec_path if spec_path else None)
    if source and source.is_file():
        specification = source.read_text(encoding="utf-8")

    previous_experiment = None
    if previous_report:
        previous_experiment = {"report": previous_report}
        previous_spec = Path(previous_report).parent.parent / "experiment.yml"
        if previous_spec.is_file():
            previous_experiment["specification"] = previous_spec.read_text(
                encoding="utf-8"
            )[:_HANDOFF_SPECIFICATION_CHARACTER_LIMIT]
        if previous_summary:
            previous_experiment["summary"] = previous_summary[
                :_HANDOFF_SUMMARY_CHARACTER_LIMIT
            ]
        if previous_followup_decision:
            previous_experiment["followup_decision"] = previous_followup_decision
    return task, specification, code, followups, previous_experiment


def _build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser.

    :return: Configured parser.
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Design an experiment and submit it, or interpret a finished one.")
    parser.add_argument("-p", "--phase", choices=("design", "interpret"), default="design")
    parser.add_argument("-t", "--task", help="the question to answer (design phase)")
    parser.add_argument(
        "--run", help="investigation directory to continue (interpret phase)"
    )
    parser.add_argument("-m", "--model", default=os.environ.get("AGENT_MODEL"),
                        help="model identifier the server serves (default: $AGENT_MODEL)")
    parser.add_argument("-u", "--base-url", default=os.environ.get("AGENT_BASE_URL", _DEFAULT_BASE_URL))
    parser.add_argument("-k", "--api-key", default=os.environ.get("AGENT_API_KEY", "EMPTY"))
    parser.add_argument("-r", "--root", default=os.getcwd())
    parser.add_argument("-i", "--inbox", default=_DEFAULT_INBOX)
    parser.add_argument("-c", "--catalog", default=_DEFAULT_CATALOG)
    parser.add_argument("-e", "--environment", default=_DEFAULT_ENVIRONMENT,
                        help="pass an empty string to run without one")
    parser.add_argument("-R", "--results", default=os.environ.get("AGENT_RESULTS", _DEFAULT_RESULTS),
                        help="bexhoma's result folder")
    parser.add_argument("-d", "--trajectories", default=_DEFAULT_TRAJECTORIES)
    parser.add_argument("-a", "--attempts", type=int, default=_DEFAULT_ATTEMPTS)
    parser.add_argument("-f", "--followups", type=int, default=_DEFAULT_FOLLOWUPS)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=_DEFAULT_MAX_TOKENS,
                        help="ceiling on tokens generated per turn, thinking included")
    parser.add_argument("--dry-run", action="store_true",
                        help="design and validate only; do not submit to the cluster")
    return parser


def _latest_run(trajectories: Path) -> Optional[Path]:
    """Return the most recent investigation directory, if any."""
    runs = sorted((d for d in trajectories.glob("*") if (d / "trajectory.jsonl").is_file()))
    return runs[-1] if runs else None


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


def _write_reports(
    run_directory: Path,
    trajectory: Trajectory,
    phase_number: int,
    phase: str,
    summary: str,
    final: bool,
) -> tuple[Path, Optional[Path]]:
    """Preserve a phase account and, only at completion, the aggregate report."""
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


def main() -> int:
    """Run one phase from the command line.

    :return: Process exit code; zero when the phase produced what it should.
    :rtype: int
    """
    args = _build_parser().parse_args()
    if not args.model:
        print("error: no model given; pass --model or set AGENT_MODEL", file=sys.stderr)
        return 2

    root = Path(args.root).resolve()
    trajectories = root / args.trajectories
    source: Optional[Path] = None
    if args.phase == "design":
        run_directory = trajectories / datetime.now().strftime("%Y%m%dT%H%M%S%f")
    else:
        source = (
            _resolve_investigation(root, args.run)
            if args.run else _latest_run(trajectories)
        )
        if source is None or not (source / "trajectory.jsonl").is_file():
            print("error: no earlier investigation to interpret; pass --run", file=sys.stderr)
            return 2
        run_directory = source

    phase_number = _phase_number(run_directory)
    phase_directory = run_directory / "phases" / f"{phase_number:02d}-{args.phase}"
    phase_directory.mkdir(parents=True, exist_ok=True)
    trajectory = Trajectory(run_directory)
    model = model_client.ChatModel(model=args.model, base_url=args.base_url,
                                   api_key=args.api_key, temperature=args.temperature,
                                   max_tokens=args.max_tokens)
    workspace = tools.Workspace(
        root=str(root), inbox=args.inbox, catalog_path=args.catalog,
        environment_path=args.environment or None, results_root=args.results,
        run_directory=phase_directory)

    if args.phase == "design":
        if not args.task:
            print("error: --task is required for the design phase", file=sys.stderr)
            return 2
        catalog = root / args.catalog
        if not catalog.is_file():
            print(f"error: catalog not found at {catalog}", file=sys.stderr)
            return 2
        (run_directory / "task.txt").write_text(args.task + "\n", encoding="utf-8")
        if args.dry_run:
            tools.DESIGN_TOOLS[:] = [s for s in tools.DESIGN_TOOLS
                                     if s["function"]["name"] != "submit"]
        outcome = run_design(
            task=args.task, workspace=workspace, model=model, trajectory=trajectory,
            catalog_path=args.catalog,
            catalog_sha256=hashlib.sha256(catalog.read_bytes()).hexdigest(),
            environment_path=args.environment if (root / args.environment).is_file() else None,
            attempts=args.attempts, followups=args.followups)
    else:
        assert source is not None
        task, specification, code, carried_followups, previous_experiment = _carry_forward(
            source, root
        )
        task_file = run_directory / "task.txt"
        if not task_file.is_file():
            task_file.write_text(task + "\n", encoding="utf-8")
        listing = workspace.list_results()["experiments"]
        finished = [e for e in listing if e["state"] == "finished" and (not code or e["code"] == code)]
        if not finished:
            print(f"error: no finished result for code {code or '(any)'}; "
                  f"{len(listing)} experiment(s) known", file=sys.stderr)
            return 2
        result_contract = Path(finished[0]["report"]).parent.parent / "contract_result.yml"
        outcome = run_interpret(
            task=task, report_path=finished[0]["report"], specification=specification,
            workspace=workspace, model=model, trajectory=trajectory,
            result_contract_path=(
                str(result_contract) if result_contract.is_file() else _DEFAULT_RESULT_CONTRACT
            ),
            followups=min(args.followups, carried_followups)
            if carried_followups is not None else args.followups,
            catalog_path=args.catalog,
            environment_path=args.environment if (root / args.environment).is_file() else None,
            attempts=args.attempts, previous_experiment=previous_experiment,
            dry_run=args.dry_run)

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
