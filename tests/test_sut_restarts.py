"""
Unit tests for :mod:`bexhoma.sut_restarts` and the restart detail it feeds
into :mod:`bexhoma.report_writer`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from bexhoma import report_writer, sut_restarts

_POD = "bexhoma-sut-postgresql-1-123-6b87f4bbb5-l9sr2"

# Trimmed from a real capture of an OOMKilled PostgreSQL SUT without a PVC.
_DESCRIBE_TEMPLATE = """Name:                 {pod}
Namespace:            test
Status:               Running
Containers:
  dbms:
    Container ID:  containerd://45c9
    Image:         postgres:18.3
    Args:
      -c
      work_mem=1024MB
    State:          Running
      Started:      Sat, 26 Sep 2026 23:08:25 +0000
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    137
      Started:      Sat, 26 Sep 2026 22:54:22 +0000
      Finished:     Sat, 26 Sep 2026 23:08:22 +0000
    Ready:          True
    Restart Count:  1
    Readiness:  exec [/bin/sh -c if pg_isready -h localhost; then
  exit 0;
fi
] delay=15s timeout=1s period=60s #success=3 #failure=3
    Environment:
      POSTGRES_HOST_AUTH_METHOD:  trust
      PGDATA:                     /var/lib/postgresql/data/pgdata
    Mounts:
      /dev/shm from dshm (rw)
{extra_mount}  monitor-application:
    Container ID:  containerd://1124
    State:          Running
      Started:      Sat, 26 Sep 2026 22:54:23 +0000
    Ready:          True
    Restart Count:  0
    Mounts:                       <none>
Conditions:
  Type                        Status
  Ready                       True
Volumes:
  dshm:
    Type:        EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:      Memory
{extra_volume}QoS Class:       Guaranteed
"""


def _describe(pod: str = _POD, with_pvc: bool = False) -> str:
    extra_mount = "      /var/lib/postgresql/data from benchmark-storage-volume (rw)\n" if with_pvc else ""
    extra_volume = (
        "  benchmark-storage-volume:\n"
        "    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)\n"
        "    ClaimName:  bexhoma-storage\n"
    ) if with_pvc else ""
    return _DESCRIBE_TEMPLATE.format(pod=pod, extra_mount=extra_mount, extra_volume=extra_volume)


def _write_result(result_dir: Path, restarts: str, describe_text: str | None) -> None:
    (result_dir / "bexhoma-sut-postgresql-1-1784910886-1-restarts.json").write_text(json.dumps({_POD: restarts}))
    if describe_text is not None:
        (result_dir / f"bexhoma-sut-postgresql-1-123-1-{_POD[-16:]}.describe.log").write_text(describe_text)


class ParseDescribeLogTest(unittest.TestCase):
    """The parser must pick up the Last State block, env and mounts per container."""

    def test_oomkilled_container(self) -> None:
        description = sut_restarts.parse_describe_log(_describe())
        self.assertEqual(description.name, _POD)
        dbms = description.containers["dbms"]
        self.assertEqual(dbms.restart_count, 1)
        self.assertEqual(dbms.reason, "OOMKilled")
        self.assertEqual(dbms.exit_code, "137")
        self.assertEqual(dbms.finished, "Sat, 26 Sep 2026 23:08:22 +0000")
        self.assertEqual(dbms.env["PGDATA"], "/var/lib/postgresql/data/pgdata")
        self.assertEqual(dbms.mounts, [("/dev/shm", "dshm")])
        self.assertEqual(description.containers["monitor-application"].mounts, [])
        self.assertEqual(description.volume_types, {"dshm": "EmptyDir"})

    def test_data_volume_requires_mount_above_pgdata(self) -> None:
        without_pvc = sut_restarts.parse_describe_log(_describe())
        with_pvc = sut_restarts.parse_describe_log(_describe(with_pvc=True))
        self.assertFalse(sut_restarts.has_data_volume(without_pvc.containers["dbms"], without_pvc.volume_types))
        self.assertTrue(sut_restarts.has_data_volume(with_pvc.containers["dbms"], with_pvc.volume_types))


class RestartCountsTest(unittest.TestCase):
    """kubectl merges stderr into stdout, so warning lines surround the counts."""

    _KLOG = "E0928 10:11:12.123456   1234 memcache.go:265] couldn't get current server API group list\n"

    def test_clean_drops_kubectl_warnings(self) -> None:
        self.assertEqual(sut_restarts.clean_restart_counts(self._KLOG + "1 0"), "1 0")
        self.assertEqual(sut_restarts.clean_restart_counts(self._KLOG), "")
        self.assertEqual(sut_restarts.clean_restart_counts(None), "")

    def test_read_tolerates_polluted_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            _write_result(result_dir, self._KLOG + "1 0", None)
            self.assertEqual(sut_restarts.read_restart_counts(result_dir), ({_POD: 1}, {_POD: "1 0"}))


class CollectRestartDetailsTest(unittest.TestCase):
    """Restart counts come from restarts.json; reasons from the describe log."""

    def test_no_restarts_yields_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            _write_result(result_dir, "0 0", _describe())
            self.assertEqual(sut_restarts.collect_restart_details(result_dir), [])

    def test_oomkill_without_pvc_loses_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            _write_result(result_dir, "1 0", _describe())
            details = sut_restarts.collect_restart_details(result_dir)
        self.assertEqual(len(details), 1)
        self.assertEqual((details[0].container, details[0].reason, details[0].data_volume), ("dbms", "OOMKilled", False))
        self.assertEqual(sut_restarts.summarize_reasons(details), {"OOMKilled": 1})

    def test_oomkill_with_pvc_keeps_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            _write_result(result_dir, "1 0", _describe(with_pvc=True))
            details = sut_restarts.collect_restart_details(result_dir)
        self.assertTrue(details[0].data_volume)

    def test_missing_describe_log_is_unknown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            _write_result(result_dir, "2 0", None)
            details = sut_restarts.collect_restart_details(result_dir)
        self.assertEqual((details[0].reason, details[0].data_volume, details[0].restarts), ("unknown", None, 2))


class ReportRestartDetailTest(unittest.TestCase):
    """The report must surface the reason and the lost data, not just a count."""

    def test_health_summary_names_reason_and_lost_data(self) -> None:
        details = [sut_restarts.RestartDetail(pod=_POD, restarts=1, container="dbms", reason="OOMKilled", data_volume=False)]
        lines = report_writer._build_health_summary_lines(1, {}, details)
        restart_line = next(line for line in lines if "SUT container restarts" in line)
        self.assertIn("OOMKilled: 1", restart_line)
        self.assertIn("1 without a data volume", restart_line)

    def test_health_summary_without_details_keeps_old_line(self) -> None:
        lines = report_writer._build_health_summary_lines(0, {})
        self.assertIn("- SUT container restarts: none", lines)

    def test_connections_md_lists_reason_under_pod(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            report_dir = result_dir / "report"
            report_dir.mkdir()
            _write_result(result_dir, "1 0", _describe())
            details = sut_restarts.collect_restart_details(result_dir)
            lines = report_writer._build_connections_md_lines(
                pd.DataFrame(), result_dir, report_dir, {_POD: "1 0"}, details,
            )
        pod_index = lines.index(f"* {_POD}: 1 0")
        self.assertIn("dbms: OOMKilled (exit 137)", lines[pod_index + 1])
        self.assertIn("on-disk state was lost", lines[pod_index + 1])
        self.assertIn("](../bexhoma-sut-", lines[pod_index + 1])


if __name__ == "__main__":
    unittest.main()
