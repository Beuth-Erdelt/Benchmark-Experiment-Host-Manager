"""
Failure timeline for a finished experiment's report.

Lists the failures of one experiment in the order they began, each placed in
the benchmark phase that was running at the time. Two kinds of source feed it:

* generic ones every benchmark type has — SUT container restarts, from
  :mod:`bexhoma.sut_restarts`, placed by their termination time;
* benchmark-specific ones, which a benchmark hands over as
  :class:`FailureEvent` objects (e.g. DBMSBenchmarker: queries that failed in
  some pods of a phase). An event that names only its phase is given that
  phase's time window.

The timeline orders evidence; it does not diagnose. A failure may cause later
ones, or be unrelated to them, and how failures show up differs between
benchmark tools — so nothing here decides which failure caused which.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from email.utils import parsedate_to_datetime

import pandas as pd

from bexhoma import sut_restarts

#: Entries shown before the rest is only counted.
_MAX_EVENTS = 12


@dataclass
class FailureEvent:
    """
    One failure, as a line of the timeline.

    :param text: What failed, without any claim about why.
    :param phase: Phase identifier the failure belongs to, or ``""``.
    :param begin: When it began (naive local time, like the evaluators'
        ``benchmark_begin``); ``None`` takes the phase's begin.
    :param end: When it ended, for a failure spanning a phase; ``None`` for
        a point in time, or to take the phase's end when ``begin`` is ``None``.
    :param see: Markdown pointer to the evidence.
    :param after: For a point in time outside every phase window, the phase
        that ended most recently before it; set by :func:`place_events`.
    """

    text: str
    phase: str = ""
    begin: datetime | None = None
    end: datetime | None = None
    see: str = ""
    after: str = ""


@dataclass
class PhaseWindow:
    """Time window and pod count of one benchmark phase."""

    begin: datetime | None
    end: datetime | None
    pods: int


def phase_windows(
    df_connections: pd.DataFrame, overrides: dict[str, tuple[datetime, datetime]] | None = None,
) -> dict[str, PhaseWindow]:
    """
    Collect each phase's time window and pod count.

    :param df_connections: Output of ``evaluator.get_connections_of_experiment()``;
        uses its ``phase``, ``benchmark_begin`` and ``benchmark_end`` columns.
    :param overrides: Phase to ``(begin, end)`` from the benchmark tool's own
        timing, preferred over the connection table's columns where given.
    :return: Phase identifier to its window; a phase without timing data
        keeps ``None`` bounds.
    :rtype: dict[str, PhaseWindow]
    """
    windows: dict[str, PhaseWindow] = {}
    if not df_connections.empty and 'phase' in df_connections.columns:
        for phase, group in df_connections.groupby('phase'):
            begin = pd.to_datetime(group['benchmark_begin'], errors='coerce') if 'benchmark_begin' in group else None
            end = pd.to_datetime(group['benchmark_end'], errors='coerce') if 'benchmark_end' in group else None
            windows[str(phase)] = PhaseWindow(
                begin=None if begin is None or begin.isna().all() else begin.min().to_pydatetime(),
                end=None if end is None or end.isna().all() else end.max().to_pydatetime(),
                pods=len(group),
            )
    for phase, (begin, end) in (overrides or {}).items():
        pods = windows[phase].pods if phase in windows else 0
        windows[phase] = PhaseWindow(begin=begin, end=end, pods=pods)
    return windows


def _local_time(text: str) -> datetime | None:
    """
    Parse a ``kubectl describe`` timestamp into naive local time.

    :param text: e.g. ``"Sat, 10 Oct 2026 11:59:53 +0200"``.
    :return: The same instant in this machine's local time, without tzinfo,
        so it compares with the evaluators' ``benchmark_begin``; ``None``
        when unparseable.
    :rtype: datetime | None
    """
    try:
        parsed = parsedate_to_datetime(text)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone().replace(tzinfo=None)
    return parsed


def restart_events(details: list[sut_restarts.RestartDetail]) -> list[FailureEvent]:
    """
    Turn SUT restart details into failure events at their termination time.

    :param details: Output of :func:`sut_restarts.collect_restart_details`.
    :return: One event per restarted container.
    :rtype: list[FailureEvent]
    """
    return [
        FailureEvent(
            text=f"SUT container restarted ({detail.pod}: {sut_restarts.format_detail(detail)})",
            begin=_local_time(detail.finished) if detail.finished else None,
            see="[connections.md](connections.md)'s SUT Container Restarts",
        )
        for detail in details
    ]


def place_events(events: list[FailureEvent], windows: dict[str, PhaseWindow]) -> list[FailureEvent]:
    """
    Give phase-only events their phase's window, put point-in-time events in
    the phase running at that time, and sort by begin.

    :param events: Events from all sources.
    :param windows: Output of :func:`phase_windows`.
    :return: The events, earliest first; events without any time come last.
    :rtype: list[FailureEvent]
    """
    placed: list[FailureEvent] = []
    timed = {phase: window for phase, window in windows.items() if window.begin is not None and window.end is not None}
    for event in events:
        if event.begin is None and event.phase in windows:
            window = windows[event.phase]
            event = replace(event, begin=window.begin, end=window.end)
        elif event.begin is not None and not event.phase:
            running = [phase for phase, window in timed.items() if window.begin <= event.begin <= window.end]
            ended = [phase for phase, window in timed.items() if window.end < event.begin]
            if running:
                event = replace(event, phase=", ".join(sorted(running)))
            elif ended:
                event = replace(event, after=max(ended, key=lambda phase: timed[phase].end))
        placed.append(event)
    return sorted(placed, key=lambda e: (e.begin is None, e.begin or datetime.min, e.phase))


def _format_event(event: FailureEvent, windows: dict[str, PhaseWindow]) -> str:
    """Render one event as the body of a numbered timeline line."""
    if event.begin is None:
        when = "time unknown"
    elif event.end is not None and event.end != event.begin:
        when = f"{event.begin:%Y-%m-%d %H:%M:%S} – {event.end:%H:%M:%S}"
    else:
        when = f"{event.begin:%Y-%m-%d %H:%M:%S}"
    if event.phase:
        pods = [windows[phase].pods for phase in event.phase.split(", ") if phase in windows]
        where = f"phase {event.phase}" + (f" ({pods[0]} pods)" if len(pods) == 1 else "")
    elif event.after and event.begin is not None:
        window = windows[event.after]
        seconds = int((event.begin - window.end).total_seconds())
        where = f"no benchmark phase running; {seconds} s after phase {event.after} ({window.pods} pods) ended"
    else:
        where = "no benchmark phase running"
    line = f"{when}, {where}: {event.text}"
    if event.see:
        line += f" — see {event.see}"
    return line


def build_timeline_lines(
    events: list[FailureEvent], df_connections: pd.DataFrame,
    window_overrides: dict[str, tuple[datetime, datetime]] | None = None,
) -> list[str]:
    """
    Build ``index.md``'s ``### Failure Timeline`` block.

    :param events: Failure events from every source, in any order.
    :param df_connections: Output of ``evaluator.get_connections_of_experiment()``,
        for the phase windows; may be empty.
    :param window_overrides: Phase windows from the benchmark tool's own
        timing, see :func:`phase_windows`.
    :return: Markdown lines; says "none" when there are no events.
    :rtype: list[str]
    """
    lines = ["### Failure Timeline", ""]
    if not events:
        lines.append("No failures were recorded.")
        return lines
    windows = phase_windows(df_connections, window_overrides)
    placed = place_events(events, windows)
    lines.append(
        "Failures in the order they began, each placed in the benchmark phase that was running. "
        "A failure spanning a phase is shown with that phase's time window. The order is evidence, "
        "not a diagnosis: a failure may cause later ones or be unrelated to them, and this report "
        "does not decide which. Read the first entry first."
    )
    lines.append("")
    for number, event in enumerate(placed[:_MAX_EVENTS], start=1):
        lines.append(f"{number}. {_format_event(event, windows)}")
    if len(placed) > _MAX_EVENTS:
        lines.append(f"\n{len(placed) - _MAX_EVENTS} later failures are not listed here.")
    return lines
