"""
Unit tests for :mod:`bexhoma.failure_timeline`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import unittest
from datetime import datetime

import pandas as pd

from bexhoma import failure_timeline, sut_restarts
from bexhoma.failure_timeline import FailureEvent


def _connections() -> pd.DataFrame:
    """Two phases of one run: one pod, then four pods."""
    rows = [("p-1-1", "2026-10-10 10:00:00", "2026-10-10 10:01:00")] + [
        ("p-1-2", "2026-10-10 10:05:00", "2026-10-10 10:06:00")
    ] * 4
    return pd.DataFrame(rows, columns=["phase", "benchmark_begin", "benchmark_end"])


class PhaseWindowsTest(unittest.TestCase):
    """Windows come from the connection table unless the benchmark knows better."""

    def test_windows_and_pods_from_connections(self) -> None:
        windows = failure_timeline.phase_windows(_connections())
        self.assertEqual(windows["p-1-2"].pods, 4)
        self.assertEqual(windows["p-1-2"].begin, datetime(2026, 10, 10, 10, 5))

    def test_override_replaces_times_keeps_pods(self) -> None:
        override = {"p-1-2": (datetime(2026, 10, 10, 11, 0), datetime(2026, 10, 10, 11, 1))}
        windows = failure_timeline.phase_windows(_connections(), override)
        self.assertEqual((windows["p-1-2"].begin.hour, windows["p-1-2"].pods), (11, 4))


class PlaceEventsTest(unittest.TestCase):
    """Events get a phase or a time, and come out in the order they began."""

    def test_phase_event_takes_window_and_sorts(self) -> None:
        windows = failure_timeline.phase_windows(_connections())
        events = failure_timeline.place_events([
            FailureEvent("late", phase="p-1-2"),
            FailureEvent("early", phase="p-1-1"),
        ], windows)
        self.assertEqual([e.text for e in events], ["early", "late"])
        self.assertEqual(events[0].end, datetime(2026, 10, 10, 10, 1))

    def test_point_event_inside_and_after_a_phase(self) -> None:
        windows = failure_timeline.phase_windows(_connections())
        inside, after = failure_timeline.place_events([
            FailureEvent("crash", begin=datetime(2026, 10, 10, 10, 5, 30)),
            FailureEvent("crash2", begin=datetime(2026, 10, 10, 10, 6, 5)),
        ], windows)
        self.assertEqual(inside.phase, "p-1-2")
        self.assertEqual((after.phase, after.after), ("", "p-1-2"))

    def test_untimed_event_comes_last(self) -> None:
        events = failure_timeline.place_events([
            FailureEvent("unknown"), FailureEvent("known", begin=datetime(2026, 1, 1)),
        ], {})
        self.assertEqual([e.text for e in events], ["known", "unknown"])


class RestartEventsTest(unittest.TestCase):
    """A restart becomes a point event at its termination time, in local time."""

    def test_finished_time_is_parsed(self) -> None:
        detail = sut_restarts.RestartDetail(
            pod="sut", restarts=1, container="dbms", reason="Error", exit_code="1",
            finished="Sat, 10 Oct 2026 11:59:53 +0200", data_volume=False,
        )
        event = failure_timeline.restart_events([detail])[0]
        expected = datetime.fromisoformat("2026-10-10T11:59:53+02:00").astimezone().replace(tzinfo=None)
        self.assertEqual(event.begin, expected)
        self.assertIn("dbms: Error (exit 1)", event.text)


class TimelineLinesTest(unittest.TestCase):
    """The block lists failures in order and never claims a cause."""

    def test_no_events(self) -> None:
        self.assertIn("No failures were recorded.", failure_timeline.build_timeline_lines([], pd.DataFrame()))

    def test_numbered_in_order_with_phase_and_pods(self) -> None:
        lines = failure_timeline.build_timeline_lines([
            FailureEvent("restart", begin=datetime(2026, 10, 10, 10, 6, 1), see="connections.md"),
            FailureEvent("queries failed: Q18 in 1 of 4 pods", phase="p-1-2"),
        ], _connections())
        numbered = [line for line in lines if line[:2] in ("1.", "2.")]
        self.assertIn("phase p-1-2 (4 pods): queries failed", numbered[0])
        self.assertIn("1 s after phase p-1-2 (4 pods) ended: restart — see connections.md", numbered[1])
        self.assertIn("not a diagnosis", "\n".join(lines))

    def test_long_timeline_is_cut(self) -> None:
        events = [FailureEvent(f"e{i}", begin=datetime(2026, 1, 1, 0, i)) for i in range(15)]
        lines = failure_timeline.build_timeline_lines(events, pd.DataFrame())
        self.assertIn("3 later failures are not listed here.", "\n".join(lines))


if __name__ == "__main__":
    unittest.main()
