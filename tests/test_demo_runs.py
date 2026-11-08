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


if __name__ == "__main__":
    unittest.main()
