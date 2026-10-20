"""
Unit tests for the HammerDB transaction counter time series in :class:`bexhoma.evaluators.tpcc.TpccEvaluator`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import os
import tempfile
import unittest

from bexhoma.evaluators.tpcc import TpccEvaluator

# Two VU tests in one pod log, as printed by benchmarker.sh after the run
_LOG = """Vuser 1:TEST RESULT : System achieved 96312 NOPM from 220914 PostgreSQL TPM
/tmp/hdbtcount_6AD6ABEE20F103E233033353.log
Hammerdb Transaction Counter Log @ Mon Oct 19 23:46:54 UTC 2026

0 PostgreSQL tpm @ Mon Oct 19 23:46:54 UTC 2026
200000 PostgreSQL tpm @ Mon Oct 19 23:47:04 UTC 2026
220000 PostgreSQL tpm @ Mon Oct 19 23:47:14 UTC 2026
/tmp/hdbtcount_6AD6ACEC301E03E273335363.log
Hammerdb Transaction Counter Log @ Mon Oct 19 23:48:00 UTC 2026

0 PostgreSQL tpm @ Mon Oct 19 23:48:00 UTC 2026
240000 PostgreSQL tpm @ Mon Oct 19 23:48:10 UTC 2026
"""


def _evaluator(path: str) -> TpccEvaluator:
    evaluator = object.__new__(TpccEvaluator)
    evaluator.path = path
    return evaluator


class ParseCounterLogTest(unittest.TestCase):
    """Counter lines become (second, tpm); the leading 0 of each counter log is skipped."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def _write(self, pod: str, text: str) -> str:
        filename = os.path.join(self.tmp.name, f"bexhoma-benchmarker-postgresql-1-123-1-1-1-{pod}.dbmsbenchmarker.log")
        with open(filename, "w") as f:
            f.write(text)
        return filename

    def test_parse(self) -> None:
        filename = self._write("aaaaa", _LOG)
        results = _evaluator(self.tmp.name).parse_hammerdb_log_file(filename)
        self.assertEqual(results, [
            {"second": 0, "tpm": 200000},
            {"second": 10, "tpm": 220000},
            {"second": 70, "tpm": 240000},  # 66 s, rounded to the 10 s refresh rate
        ])

    def test_drift_is_rounded(self) -> None:
        filename = self._write("aaaaa", "1 X tpm @ Mon Oct 19 10:00:00 UTC 2026\n2 X tpm @ Mon Oct 19 10:00:11 UTC 2026\n3 X tpm @ Mon Oct 19 10:00:21 UTC 2026\n")
        seconds = [r["second"] for r in _evaluator(self.tmp.name).parse_hammerdb_log_file(filename)]
        self.assertEqual(seconds, [0, 10, 20])

    def test_single_digit_day(self) -> None:
        filename = self._write("aaaaa", "5 MySQL tpm @ Mon Oct  5 23:48:10 UTC 2026\n")
        self.assertEqual(_evaluator(self.tmp.name).parse_hammerdb_log_file(filename), [{"second": 0, "tpm": 5}])

    def test_no_counter(self) -> None:
        filename = self._write("aaaaa", "Vuser 1:TEST RESULT : System achieved 1 NOPM from 2 PostgreSQL TPM\n")
        self.assertEqual(_evaluator(self.tmp.name).parse_hammerdb_log_file(filename), [])

    def test_aggregate_is_mean_over_pods(self) -> None:
        # the counter measures the whole database, so parallel pods are averaged, not summed
        self._write("aaaaa", "1 X tpm @ Mon Oct 19 10:00:00 UTC 2026\n2 X tpm @ Mon Oct 19 10:00:10 UTC 2026\n")
        self._write("bbbbb", "3 X tpm @ Mon Oct 19 10:00:01 UTC 2026\n4 X tpm @ Mon Oct 19 10:00:11 UTC 2026\n")
        evaluator = _evaluator(self.tmp.name)
        df = evaluator.benchmark_logs_to_timeseries_df(["aaaaa.dbmsbenchmarker", "bbbbb.dbmsbenchmarker"])
        self.assertEqual(df["tpm"].tolist(), [2.0, 3.0])
        self.assertEqual(df.index.tolist(), [0, 10])
        single = evaluator.benchmark_logs_to_timeseries_df(["aaaaa.dbmsbenchmarker", "bbbbb.dbmsbenchmarker"], aggregate=False)
        self.assertEqual(len(single), 2)

    def test_aggregate_without_counter_lines(self) -> None:
        self._write("aaaaa", "nothing here\n")
        self.assertTrue(_evaluator(self.tmp.name).benchmark_logs_to_timeseries_df(["aaaaa.dbmsbenchmarker"]).empty)


if __name__ == "__main__":
    unittest.main()
