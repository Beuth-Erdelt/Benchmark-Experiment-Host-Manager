#!/usr/bin/env python3
"""
Scan docs/ for log-file references and report experiment metadata.

For each log file referenced inside a docs/*.md markdown block, look up the
corresponding log / summary file in logs_tests/ and display:
  - experiment code
  - duration
  - bexhoma version
  - TEST-failed and TEST-warning lines

Run from the repo root:
    python scripts/scan-docs.py
"""

import re
import sys
from pathlib import Path

DOCS_DIR = Path("docs")
LOGS_DIR = Path("logs_tests")

# Captures the log filename from a <details><summary>Show <a ...>NAME.log</a></summary>
# line, followed by an optional ```markdown block.
# The embedded block content is available as group "embedded" when present.
LOG_REF_PATTERN = re.compile(
    r'<summary>[^\n]*?<a [^>\n]*>(?P<logfile>[\w\-.\/]+\.log)</a>[^\n]*</summary>[ \t]*\n'
    r'(?:\s*```markdown\n(?P<embedded>.*?)\n```)?',
    re.DOTALL,
)

# Both "* Code: 123" (summary/log format) and "    Code: 123" (doc embedded format).
_RE_CODE = re.compile(r'(?:^\s*\*\s+|^\s{2,})Code:\s+(\d+)', re.MULTILINE)
_RE_DURATION = re.compile(r'(?:^\s*\*\s+|^\s{2,})Duration:\s+([\d]+s)', re.MULTILINE)
_RE_VERSION = re.compile(r'bexhoma version (\d+(?:\.\d+)*)')
# Newer logs prefix the line with "* ", older summaries do not.
_RE_TEST = re.compile(r'^(?:\*\s+)?(TEST (?:passed|failed|warning):[^\n]+)', re.MULTILINE)


def extract_metadata(text: str) -> dict:
    """Extract code, duration, version, and test results from log or summary text."""
    code_match = _RE_CODE.search(text)
    duration_match = _RE_DURATION.search(text)
    version_match = _RE_VERSION.search(text)
    tests = _RE_TEST.findall(text)
    return {
        "code": code_match.group(1) if code_match else None,
        "duration": duration_match.group(1) if duration_match else None,
        "version": version_match.group(1) if version_match else None,
        "tests": tests,
    }


def load_source(logfile_name: str) -> tuple[str | None, str]:
    """
    Return (text, source_label) preferring _summary.md over the full .log file.
    Returns (None, '') when neither file exists.
    """
    base = Path(logfile_name).stem
    summary_path = LOGS_DIR / f"{base}_summary.md"
    log_path = LOGS_DIR / logfile_name

    if summary_path.exists():
        return summary_path.read_text(encoding="utf-8"), "summary"
    if log_path.exists():
        return log_path.read_text(encoding="utf-8"), "log"
    return None, ""


def scan_doc(md_path: Path) -> list[dict]:
    """Return a list of reference records found in *md_path*."""
    text = md_path.read_text(encoding="utf-8")
    records = []
    for match in LOG_REF_PATTERN.finditer(text):
        logfile_name = match.group("logfile")
        embedded = match.group("embedded")
        content, source = load_source(logfile_name)
        if content is None and embedded:
            content, source = embedded, "doc"
        if content is not None:
            meta = extract_metadata(content)
        else:
            meta = {"code": None, "duration": None, "version": None, "tests": []}
        log_path = LOGS_DIR / logfile_name
        crashed = log_path.exists() and "Traceback (most recent call last)" in log_path.read_text(encoding="utf-8", errors="replace")
        records.append({
            "crashed": crashed,
            "doc": md_path.name,
            "logfile": logfile_name,
            "source": source,
            "log_exists": (LOGS_DIR / logfile_name).exists(),
            "summary_exists": (LOGS_DIR / f"{Path(logfile_name).stem}_summary.md").exists(),
            **meta,
        })
    return records


def _status_flags(rec: dict) -> str:
    """Return a compact two-char status: L=log present, S=summary present."""
    log = "L" if rec["log_exists"] else "-"
    summ = "S" if rec["summary_exists"] else "-"
    return f"{log}{summ}"


def print_table(rows: list[tuple], col_widths: list[int], header: list[str]) -> None:
    """Print a fixed-width table with a header separator."""
    sep = "  "
    header_line = sep.join(h.ljust(w) for h, w in zip(header, col_widths))
    divider = sep.join("-" * w for w in col_widths)
    print(header_line)
    print(divider)
    for row in rows:
        print(sep.join(str(cell).ljust(w) for cell, w in zip(row, col_widths)))


def print_report(all_records: list[dict]) -> None:
    """Print a formatted table of all log references, then failed-test and warning details."""
    HEADERS = ["Doc", "Log file", "Code", "Duration", "Version", "OK", "FAIL", "WARN", "St"]

    table_rows: list[tuple] = []
    failures: list[dict] = []
    warnings: list[dict] = []

    for rec in all_records:
        failed = [t for t in rec["tests"] if t.startswith("TEST failed")]
        passed = [t for t in rec["tests"] if t.startswith("TEST passed")]
        warned = [t for t in rec["tests"] if t.startswith("TEST warning")]
        table_rows.append((
            rec["doc"],
            rec["logfile"],
            rec["code"] or "—",
            rec["duration"] or "—",
            rec["version"] or "—",
            str(len(passed)) if passed else "—",
            str(len(failed) + (1 if rec.get("crashed") else 0)) if (failed or rec.get("crashed")) else "",
            str(len(warned)) if warned else "",
            _status_flags(rec),
        ))
        if rec.get("crashed"):
            failed = failed + ["log contains a Python traceback (evaluation crashed)"]
        if failed:
            failures.append({"logfile": rec["logfile"], "doc": rec["doc"], "failed": failed})
        if warned:
            warnings.append({"logfile": rec["logfile"], "doc": rec["doc"], "warned": warned})

    col_widths = [
        max(len(HEADERS[i]), max(len(str(row[i])) for row in table_rows))
        for i in range(len(HEADERS))
    ]

    print_table(table_rows, col_widths, HEADERS)

    if failures:
        print(f"\n\nFailed tests")
        print("-" * 70)
        for entry in failures:
            print(f"\n  {entry['logfile']}  ({entry['doc']})")
            for msg in entry["failed"]:
                print(f"    ✗ {msg}")

    if warnings:
        print(f"\n\nTests with warnings (need judgement, not failures)")
        print("-" * 70)
        for entry in warnings:
            print(f"\n  {entry['logfile']}  ({entry['doc']})")
            for msg in entry["warned"]:
                print(f"    ! {msg}")

    missing = sorted({rec["logfile"] for rec in all_records if not rec["log_exists"]})
    if missing:
        print(f"\n\nMissing log files")
        print("-" * 70)
        for name in missing:
            print(f"  {name}")

    referenced = {rec["logfile"] for rec in all_records}
    # Pages also link logs outside <summary> blocks, e.g. "Result: <a ...>NAME.log</a>"
    for md_file in DOCS_DIR.glob("*.md"):
        referenced.update(re.findall(
            r'<a [^>\n]*>([\w\-.\/]+\.log)</a>', md_file.read_text(encoding="utf-8")))
    unreferenced = sorted(
        p.name for p in LOGS_DIR.glob("*.log") if p.name not in referenced
    )
    if unreferenced:
        print(f"\n\nLog files in {LOGS_DIR}/ not referenced in any doc  ({len(unreferenced)})")
        print("-" * 70)
        for name in unreferenced:
            print(f"  {name}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # table uses "—" and "✗"; Windows consoles default to cp1252
    if not DOCS_DIR.exists():
        print(f"ERROR: docs directory not found at {DOCS_DIR.resolve()}", file=sys.stderr)
        sys.exit(1)

    all_records: list[dict] = []
    for md_file in sorted(DOCS_DIR.glob("*.md")):
        all_records.extend(scan_doc(md_file))

    print(f"Scanned {DOCS_DIR} — found {len(all_records)} log reference(s) across docs.")
    print_report(all_records)
