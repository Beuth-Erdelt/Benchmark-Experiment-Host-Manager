#!/usr/bin/env python3
"""
Summarise the recorded demo runs (logs_tests/*.log referenced from docs/*.md).

Every log counts once, classified by its test results:
  failed     a test failed, or the evaluation crashed (Python traceback in the log)
  warn       no test failed, but at least one test warns (needs judgement)
  unchecked  the log has no test results at all
  passed     everything else

Writes
  logs_tests/SUMMARY.md             one table of all runs, failed ones first
  logs_tests/demo-runs-badge.json   shields.io endpoint badge ("x passed, y failed, z warn")

The demos need a Kubernetes cluster and take hours, so nothing is run here: the
numbers describe the last recorded runs. Experiment codes are Unix timestamps,
which gives the date of a run.

Run from the repo root:
    python scripts/demo-runs.py            # write the two files
    python scripts/demo-runs.py --check    # exit 1 if they are not up to date (CI)
"""

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SUMMARY = Path("logs_tests/SUMMARY.md")
BADGE = Path("logs_tests/demo-runs-badge.json")
ORDER = ("failed", "warn", "unchecked", "passed")


def load_scanner():
    """Import scan-docs.py (the file name has a hyphen, so no plain import)."""
    spec = importlib.util.spec_from_file_location("scan_docs", Path(__file__).with_name("scan-docs.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def classify(rec: dict) -> str:
    tests = rec["tests"]
    if rec.get("crashed") or any(t.startswith("TEST failed") for t in tests):
        return "failed"
    if any(t.startswith("TEST warning") for t in tests):
        return "warn"
    if not tests:
        return "unchecked"
    return "passed"


def run_date(code: str | None) -> str:
    """Experiment codes are Unix timestamps."""
    try:
        return datetime.fromtimestamp(int(code), timezone.utc).strftime("%Y-%m-%d")
    except (TypeError, ValueError, OverflowError, OSError):
        return "—"


def collect(scanner) -> list[dict]:
    """One record per log file, in a stable order."""
    records = []
    for md_file in sorted(scanner.DOCS_DIR.glob("*.md")):
        records.extend(scanner.scan_doc(md_file))
    unique: dict[str, dict] = {}
    for rec in records:
        # a log referenced from several pages is the same run
        if rec["logfile"] not in unique or (rec["source"] != "doc" and unique[rec["logfile"]]["source"] == "doc"):
            unique[rec["logfile"]] = rec
    runs = []
    for name, rec in sorted(unique.items()):
        status = classify(rec)
        details = [t.split(": ", 1)[1] if ": " in t else t
                   for t in rec["tests"] if t.startswith(("TEST failed", "TEST warning"))]
        if rec.get("crashed"):
            details.append("evaluation crashed (Python traceback in the log)")
        runs.append({
            "log": name, "doc": rec["doc"], "status": status, "details": details,
            "date": run_date(rec["code"]), "version": rec["version"] or "—",
            "duration": rec["duration"] or "—", "missing": not rec["log_exists"],
        })
    runs.sort(key=lambda r: (ORDER.index(r["status"]), r["log"]))
    return runs


def counts(runs: list[dict]) -> dict:
    return {s: sum(1 for r in runs if r["status"] == s) for s in ORDER}


def badge_json(c: dict) -> str:
    # runs without test results (e.g. the testbed start logs) are listed in SUMMARY.md, not in the badge
    message = f"{c['passed']} passed, {c['failed']} failed, {c['warn']} warn"
    color = "red" if c["failed"] else ("yellow" if c["warn"] else "brightgreen")
    return json.dumps({"schemaVersion": 1, "label": "demo runs", "message": message, "color": color}, indent=2) + "\n"


def summary_md(runs: list[dict]) -> str:
    c = counts(runs)
    lines = [
        "# Demo runs",
        "",
        "Last recorded runs of the examples in `docs/`, one row per log in `logs_tests/`.",
        "Nothing is run to create this page: it is read from the committed logs by `scripts/demo-runs.py`,",
        "so it shows what the runs looked like when they were recorded, not whether the current code still passes.",
        "",
        f"**{c['passed']} passed, {c['failed']} failed, {c['warn']} warn, {c['unchecked']} unchecked** ({len(runs)} runs)",
        "",
        "| Status | Log | Page | Date | Version | Duration | Failed tests / warnings |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in runs:
        what = "<br>".join(r["details"]) if r["details"] else ""
        name = r["log"] + (" (missing)" if r["missing"] else "")
        lines.append(f"| {r['status']} | {name} | {r['doc']} | {r['date']} | {r['version'].rstrip('.')} | {r['duration']} | {what} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    scanner = load_scanner()
    runs = collect(scanner)
    if not runs:
        print("no log references found, run from the repo root", file=sys.stderr)
        return 2
    new = {SUMMARY: summary_md(runs), BADGE: badge_json(counts(runs))}
    if "--check" in sys.argv:
        stale = [str(p) for p, text in new.items()
                 if not p.exists() or p.read_text(encoding="utf-8").replace("\r\n", "\n") != text]
        if stale:
            print("not up to date: " + ", ".join(stale) + "\nrun: python scripts/demo-runs.py", file=sys.stderr)
            return 1
        print("demo run summary is up to date: " + json.loads(new[BADGE])["message"])
        return 0
    for path, text in new.items():
        path.write_text(text, encoding="utf-8", newline="\n")
    print(json.loads(new[BADGE])["message"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
