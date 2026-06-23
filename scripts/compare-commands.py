#!/usr/bin/env python3
"""
Compare bexhoma commands across bash scripts, PowerShell scripts, and doc files.

For each log file name that appears in more than one source, the parsed flags
are compared and any disagreements are reported as a table.

Run from the repo root:
    python scripts/compare-commands.py
"""

import re
from pathlib import Path

SCRIPTS_DIR = Path("scripts")
DOCS_DIR = Path("docs")

_RE_PS_COMMENT = re.compile(r'<#.*?#>')
_RE_BASH_LOG = re.compile(r'&>\s*\$LOG_DIR/(\S+\.log)')
_RE_PS_LOG = re.compile(r'Out-File\s+"?\$LOG_DIR[\\\/](\S+\.log)')


# ── Flag parsing ───────────────────────────────────────────────────────────────

def _strip_one_quote_pair(s: str) -> str:
    """Remove exactly one surrounding double-quote pair from *s*, if present."""
    if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s


def parse_flags(tokens: list[str], normalize: bool = False) -> dict[str, str | bool]:
    """
    Parse a flat token list into {flag: value_or_True}.

    :param normalize: when True, strip one outer double-quote pair from each value
                      so that ``"1,1"`` and ``1,1`` compare as equal.
    """
    flags: dict[str, str | bool] = {}
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.startswith('-'):
            if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                v = tokens[i + 1]
                flags[tok] = _strip_one_quote_pair(v) if normalize else v
                i += 2
            else:
                flags[tok] = True
                i += 1
        else:
            i += 1
    return flags


def _tokenize_bash_line(line: str) -> list[str]:
    """Strip bash continuation, redirect, and return tokens from one command line."""
    line = line.rstrip().rstrip('\\').strip()
    if '&>' in line:
        line = line[:line.index('&>')].strip()
    return line.split()


def _tokenize_ps_line(line: str) -> list[str]:
    """Strip PS continuation, Out-File redirect, and inline comments."""
    line = _RE_PS_COMMENT.sub('', line).rstrip().rstrip('`').strip()
    if '2>&1' in line:
        line = line[:line.index('2>&1')].strip()
    return line.split()


# ── Command extraction ─────────────────────────────────────────────────────────

def _collect_bash_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """Collect a multi-line bash bexhoma command starting at *start*."""
    block = [lines[start].rstrip()]
    i = start
    while block[-1].rstrip().endswith('\\') and i + 1 < len(lines):
        i += 1
        block.append(lines[i].rstrip())
    return block, i


def _collect_ps_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """Collect a multi-line PowerShell bexhoma command starting at *start*."""
    block = [lines[start].rstrip()]
    i = start
    while block[-1].rstrip().endswith('`') and i + 1 < len(lines):
        i += 1
        block.append(lines[i].rstrip())
    return block, i


def _parse_bash_block(block: list[str]) -> tuple[str | None, dict, str | None]:
    """Return (logfile, flags, action) from a collected bash command block."""
    logfile = None
    subcommand = None
    action = None
    tokens: list[str] = []

    for line in block:
        lm = _RE_BASH_LOG.search(line)
        if lm:
            logfile = lm.group(1)

        cleaned = _tokenize_bash_line(line)
        if not cleaned:
            continue
        bm = re.match(r'bexhoma\s+(\w+)', ' '.join(cleaned))
        if bm:
            subcommand = bm.group(1)
            continue
        if cleaned == ['run'] or (len(cleaned) == 1 and cleaned[0] == 'run'):
            action = 'run'
            continue
        # 'run' may appear at start of the redirect line (already stripped)
        if cleaned and cleaned[0] == 'run':
            action = 'run'
            cleaned = cleaned[1:]
        tokens.extend(cleaned)

    flags = parse_flags(tokens, normalize=True)
    if subcommand:
        flags['__subcommand__'] = subcommand
    if action:
        flags['__action__'] = action
    return logfile, flags, action


def _parse_ps_block(block: list[str]) -> tuple[str | None, dict, str | None]:
    """Return (logfile, flags, action) from a collected PowerShell command block."""
    logfile = None
    subcommand = None
    action = None
    tokens: list[str] = []

    for line in block:
        lm = _RE_PS_LOG.search(line)
        if lm:
            logfile = lm.group(1)

        cleaned = _tokenize_ps_line(line)
        if not cleaned:
            continue
        bm = re.match(r'bexhoma\s+(\w+)', ' '.join(cleaned))
        if bm:
            subcommand = bm.group(1)
            continue
        if cleaned and cleaned[0] == 'run':
            action = 'run'
            cleaned = cleaned[1:]
        tokens.extend(cleaned)

    flags = parse_flags(tokens, normalize=True)
    if subcommand:
        flags['__subcommand__'] = subcommand
    if action:
        flags['__action__'] = action
    return logfile, flags, action


def extract_from_sh(path: Path) -> dict[str, dict]:
    """Return {logfile: flags} for every bexhoma call in a .sh file."""
    lines = path.read_text(encoding='utf-8').splitlines()
    result: dict[str, dict] = {}
    i = 0
    while i < len(lines):
        if re.match(r'^\s*bexhoma\s+\w+', lines[i]):
            block, i = _collect_bash_block(lines, i)
            logfile, flags, _ = _parse_bash_block(block)
            if logfile:
                result[logfile] = flags
        i += 1
    return result


def extract_from_ps(path: Path) -> dict[str, dict]:
    """Return {logfile: flags} for every bexhoma call in a .ps1 file."""
    lines = path.read_text(encoding='utf-8').splitlines()
    result: dict[str, dict] = {}
    i = 0
    while i < len(lines):
        if re.match(r'^\s*bexhoma\s+\w+', lines[i]):
            block, i = _collect_ps_block(lines, i)
            logfile, flags, _ = _parse_ps_block(block)
            if logfile:
                result[logfile] = flags
        i += 1
    return result


def extract_from_doc(path: Path) -> dict[str, dict]:
    """Return {logfile: flags} from bash blocks inside a .md file."""
    text = path.read_text(encoding='utf-8')
    result: dict[str, dict] = {}
    for block_text in re.findall(r'```bash\n(.*?)\n```', text, re.DOTALL):
        lines = block_text.splitlines()
        i = 0
        while i < len(lines):
            if re.match(r'^\s*bexhoma\s+\w+', lines[i]):
                block, i = _collect_bash_block(lines, i)
                logfile, flags, _ = _parse_bash_block(block)
                if logfile:
                    result[logfile] = flags
            i += 1
    return result


# ── Aggregation ────────────────────────────────────────────────────────────────

def load_all(scripts_dir: Path, docs_dir: Path) -> dict[str, dict[str, dict]]:
    """
    Return {logfile: {source_label: flags}} for all three source types.

    Source labels: 'sh', 'ps', 'doc'.
    """
    combined: dict[str, dict[str, dict]] = {}

    def _add(logfile: str, label: str, flags: dict) -> None:
        combined.setdefault(logfile, {})[label] = flags

    for sh in sorted(scripts_dir.glob('test-docs-*.sh')):
        for logfile, flags in extract_from_sh(sh).items():
            _add(logfile, 'sh', flags)

    for ps in sorted(scripts_dir.glob('test-docs-*.ps1')):
        for logfile, flags in extract_from_ps(ps).items():
            _add(logfile, 'ps', flags)

    for md in sorted(docs_dir.glob('*.md')):
        for logfile, flags in extract_from_doc(md).items():
            _add(logfile, 'doc', flags)

    return combined


# ── Comparison and reporting ───────────────────────────────────────────────────

SOURCES = ('sh', 'ps', 'doc')
MISSING = '—'
NOT_IN_SOURCE = '(not in source)'


def compare(by_source: dict[str, dict]) -> list[tuple[str, str, str, str]]:
    """
    Return a list of (flag, sh_val, ps_val, doc_val) for every flag
    where at least two present sources disagree.
    """
    all_flags: set[str] = set()
    for flags in by_source.values():
        all_flags.update(flags.keys())

    diffs = []
    for flag in sorted(all_flags):
        values = {}
        for src in SOURCES:
            if src not in by_source:
                values[src] = NOT_IN_SOURCE
            elif flag in by_source[src]:
                v = by_source[src][flag]
                values[src] = 'True' if v is True else str(v)
            else:
                values[src] = MISSING

        # Only report if present sources disagree with each other
        present_vals = {v for src, v in values.items() if v != NOT_IN_SOURCE}
        if len(present_vals) > 1:
            diffs.append((flag, values['sh'], values['ps'], values['doc']))
    return diffs


def _col_widths(rows: list[tuple], headers: list[str]) -> list[int]:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    return widths


def _print_table(rows: list[tuple], headers: list[str]) -> None:
    widths = _col_widths(rows, headers)
    sep = '  '
    print(sep.join(h.ljust(w) for h, w in zip(headers, widths)))
    print(sep.join('-' * w for w in widths))
    for row in rows:
        print(sep.join(str(cell).ljust(w) for cell, w in zip(row, widths)))


def report(combined: dict[str, dict[str, dict]]) -> None:
    """Print per-logfile difference tables, then a summary."""
    HEADERS = ['Flag', 'SH', 'PS', 'Doc']
    total_diffs = 0
    diff_files: list[str] = []

    for logfile in sorted(combined.keys()):
        by_source = combined[logfile]
        diffs = compare(by_source)
        if not diffs:
            continue
        total_diffs += len(diffs)
        diff_files.append(logfile)
        present = sorted(by_source.keys())
        print(f'\n{logfile}  [sources: {", ".join(present)}]')
        _print_table(diffs, HEADERS)

    only_one_source = [lf for lf, s in combined.items() if len(s) == 1]

    print(f'\n\nSummary')
    print('-' * 50)
    print(f'  Log files compared:    {len(combined)}')
    print(f'  Log files with diffs:  {len(diff_files)}')
    print(f'  Total flag differences:{total_diffs}')
    if only_one_source:
        print(f'\nLog files found in only one source  ({len(only_one_source)})')
        print('-' * 50)
        for lf in sorted(only_one_source):
            src = next(iter(combined[lf]))
            print(f'  {lf}  [{src}]')


if __name__ == '__main__':
    combined = load_all(SCRIPTS_DIR, DOCS_DIR)
    report(combined)
