"""scripts/demo-runs.py: classification of recorded runs and the badge."""
import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "demo-runs.py"
spec = importlib.util.spec_from_file_location("demo_runs", SCRIPT)
demo_runs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo_runs)


class ClassifyTest(unittest.TestCase):
    def test_status_of_a_run(self):
        self.assertEqual(demo_runs.classify({"tests": ["TEST passed: a"], "crashed": False}), "passed")
        self.assertEqual(demo_runs.classify({"tests": ["TEST passed: a", "TEST failed: b"]}), "failed")
        self.assertEqual(demo_runs.classify({"tests": ["TEST passed: a", "TEST warning: b"]}), "warn")
        self.assertEqual(demo_runs.classify({"tests": ["TEST warning: a", "TEST failed: b"]}), "failed")
        self.assertEqual(demo_runs.classify({"tests": []}), "unchecked")

    def test_a_crashed_evaluation_fails_even_without_test_lines(self):
        self.assertEqual(demo_runs.classify({"tests": [], "crashed": True}), "failed")

    def test_run_date_from_experiment_code(self):
        self.assertEqual(demo_runs.run_date("1794055327"), "2026-11-07")
        self.assertEqual(demo_runs.run_date(None), "—")

    def test_badge(self):
        badge = json.loads(demo_runs.badge_json({"passed": 5, "failed": 1, "warn": 2, "unchecked": 3}))
        self.assertEqual(badge["message"], "5 passed, 1 failed, 2 warn")
        self.assertEqual(badge["color"], "red")
        green = json.loads(demo_runs.badge_json({"passed": 5, "failed": 0, "warn": 0, "unchecked": 3}))
        self.assertEqual(green["color"], "brightgreen")


class ScanDocTest(unittest.TestCase):
    def test_plain_log_links_are_runs_too(self):
        """Test-Reset.md and Test-Durability.md link their logs outside <summary> blocks."""
        import tempfile
        scanner = demo_runs.load_scanner()
        page = ('<details>\n<summary>Show <a href="x">docs_a.log</a></summary>\n\n</details>\n\n'
                'Result: <a href="y">docs_b.log</a>\n\nResult: <a href="y">docs_b.log</a>\n'
                'Again: <a href="x">docs_a.log</a>\n')
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "Test-Page.md"
            path.write_text(page, encoding="utf-8")
            records = scanner.scan_doc(path)
        self.assertEqual([rec["logfile"] for rec in records], ["docs_a.log", "docs_b.log"])


class ReleaseGateTest(unittest.TestCase):
    PASSED = "bexhoma version 0.13.0\nTEST passed: a\n"

    def test_reference_logs_come_from_the_reference_script(self):
        import os
        cwd = os.getcwd()
        os.chdir(SCRIPT.parent.parent)
        try:
            logs = demo_runs.reference_logs()
        finally:
            os.chdir(cwd)
        self.assertEqual(len(logs), 10)
        self.assertIn("docs_tpch_postgresql_monitoring", logs)

    def test_a_passed_log_of_the_version(self):
        self.assertEqual(demo_runs.gate_problems(self.PASSED, "0.13.0"), [])

    def test_problems_of_a_log(self):
        self.assertEqual(demo_runs.gate_problems("bexhoma version 0.13.0\n", "0.13.0"), ["no passed test"])
        self.assertEqual(demo_runs.gate_problems(self.PASSED + "TEST failed: b\n", "0.13.0"), ["failed test"])
        self.assertEqual(demo_runs.gate_problems(self.PASSED + "Traceback (most recent call last):\n", "0.13.0"),
                         ["traceback"])

    def test_the_version_must_match_exactly(self):
        self.assertEqual(demo_runs.gate_problems(self.PASSED, "0.12.0"), ["not bexhoma 0.12.0"])
        self.assertEqual(demo_runs.gate_problems(self.PASSED, "0.13"), ["not bexhoma 0.13"])
        self.assertEqual(demo_runs.gate_problems(self.PASSED.replace("0.13.0", "0.13.01"), "0.13.0"),
                         ["not bexhoma 0.13.0"])


class PerformanceTableTest(unittest.TestCase):
    SUMMARY = (
        "## Show Summary\n\n### Benchmarking\n\n#### Per Connection\n\n"
        "| connection | phase | NOPM |\n|:--|:--|--:|\n| c-1 | p-1 | 5 |\n\n"
        "#### Per Phase\n\n"
        "| DBMS | phase | NOPM | hardware_fio_read_iops |\n|:--|:--|--:|--:|\n"
        "| p-1 | p-1 | 58048.00 | 0 |\n| p-2 | p-2 | 100.00 | 0 |\n\n"
        "### Monitoring\n\n| DBMS | phase | NOPM |\n|:--|:--|--:|\n| x | x | 1 |\n")

    def test_rows_of_the_per_phase_table(self):
        phases = demo_runs.benchmarking_phases(self.SUMMARY)
        self.assertEqual([p["phase"] for p in phases], ["p-1", "p-2"])
        self.assertEqual(phases[0]["NOPM"], "58048.00")

    def test_no_benchmarking_section(self):
        self.assertEqual(demo_runs.benchmarking_phases("## Show Summary\n\n### Loading\n"), [])

    def test_key_metrics_skip_zero_and_missing(self):
        self.assertEqual(demo_runs.key_metrics({"NOPM": "58048.00", "hardware_fio_read_iops": "0"}),
                         "NOPM 58048.00")
        self.assertEqual(demo_runs.key_metrics({}), "—")


if __name__ == "__main__":
    unittest.main()
