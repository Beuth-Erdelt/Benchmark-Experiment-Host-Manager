#!/usr/bin/env python3
"""
Sync test-docs-cases.sh to match test-docs-cases.ps1.

The PowerShell file is the canonical source for this cases script.  This
script reads the PS commands and regenerates the bash equivalent, preserving
SH-specific format conventions (header comment block, backslash continuation,
post-load-init flag grouping, node-pin flag grouping).

Run from the repo root:
    python scripts/_sync_cases_sh.py
"""

import re
from pathlib import Path

SCRIPTS_DIR = Path("scripts")
PS_FILE = SCRIPTS_DIR / "test-docs-cases.ps1"
SH_FILE = SCRIPTS_DIR / "test-docs-cases.sh"

POST_LOAD_INIT_FLAGS = frozenset({'-xii', '-xic', '-xis', '-xcol'})
NODE_PIN_FLAGS = frozenset({'-rnn', '-rnl', '-rnb'})
COMMENT_COL = 32

_RE_PS_COMMENT = re.compile(r'<#\s*(.*?)\s*#>')
_RE_PS_REDIRECT = re.compile(r'Out-File\s+"?\$LOG_DIR[\\\/](\S+?)(?:"\s+|\s+)-Encoding')
_RE_WRITE_HOST = re.compile(
    r'Write-Host\s+"(\$\(Get-Date -Format \'yyyy-MM-dd HH:mm:ss\'\).*?)"'
)
_RE_SLEEP = re.compile(r'Start-Sleep -Seconds\s+(\d+)')

SH_PREAMBLE = """\
#!/bin/bash
# Extended test runs covering additional DBMS and parameter combinations.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh
"""


def _strip_one_quote_pair(s: str) -> str:
    """Remove exactly one surrounding double-quote pair from *s*, if present."""
    if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s


def _parse_ps_block(
    lines: list[str], start: int
) -> tuple[str, list[tuple[str, str | None, str]], str | None, int]:
    """
    Parse a PS bexhoma block starting at *start*.

    :return: (subcommand, flags_list, logfile, end_index) where
             flags_list contains (flag, value_or_None, description) tuples
             in the order they appear in the PS block.
    """
    block = [lines[start]]
    i = start
    while block[-1].rstrip().endswith('`') and i + 1 < len(lines):
        i += 1
        block.append(lines[i])

    m = re.match(r'\s*bexhoma\s+(\w+)', block[0])
    subcommand = m.group(1) if m else ''

    flags_list: list[tuple[str, str | None, str]] = []
    logfile: str | None = None

    for line in block[1:]:
        desc_m = _RE_PS_COMMENT.search(line)
        desc = desc_m.group(1) if desc_m else ''

        out_m = _RE_PS_REDIRECT.search(line)
        if out_m:
            logfile = out_m.group(1)
            continue

        clean = _RE_PS_COMMENT.sub('', line).rstrip().rstrip('`').strip()
        if '2>&1' in clean or not clean or clean == 'run':
            continue

        tokens = clean.split()
        if not tokens or not tokens[0].startswith('-'):
            continue

        flag = tokens[0]
        value: str | None = None
        if len(tokens) > 1:
            value = _strip_one_quote_pair(tokens[1])

        flags_list.append((flag, value, desc))

    return subcommand, flags_list, logfile, i


def _make_sh_comment_lines(flags_list: list[tuple[str, str | None, str]]) -> list[str]:
    """Return one header comment line per flag."""
    lines: list[str] = []
    for flag, value, desc in flags_list:
        prefix = f'# {flag}' if value is None else f'# {flag} {value}'
        padding = max(1, COMMENT_COL - len(prefix))
        lines.append(f'{prefix}{" " * padding}{desc}')
    return lines


def _make_sh_command_lines(
    subcommand: str,
    flags_list: list[tuple[str, str | None, str]],
    logfile: str,
) -> list[str]:
    """Return SH bexhoma command lines with backslash continuation."""
    lines: list[str] = [f'bexhoma {subcommand} \\']

    idx = 0
    n = len(flags_list)
    while idx < n:
        flag, value, _ = flags_list[idx]

        if flag in POST_LOAD_INIT_FLAGS:
            # Group consecutive post-load-init flags onto one line.
            parts: list[str] = []
            while idx < n and flags_list[idx][0] in POST_LOAD_INIT_FLAGS:
                f, v, _ = flags_list[idx]
                parts.append(f if v is None else f'{f} {v}')
                idx += 1
            lines.append(f'  {" ".join(parts)} \\')
            continue

        if flag in NODE_PIN_FLAGS:
            # Group consecutive node-pinning flags onto one line.
            parts = []
            while idx < n and flags_list[idx][0] in NODE_PIN_FLAGS:
                f, v, _ = flags_list[idx]
                parts.append(f if v is None else f'{f} {v}')
                idx += 1
            lines.append(f'  {" ".join(parts)} \\')
            continue

        lines.append(f'  {flag} \\' if value is None else f'  {flag} {value} \\')
        idx += 1

    lines.append(f'  run &>$LOG_DIR/{logfile}')
    return lines


def _convert_write_host(line: str) -> str:
    """Convert a Write-Host status line to echo."""
    m = _RE_WRITE_HOST.match(line.strip())
    if m:
        inner = m.group(1).replace(
            "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
            "$(date '+%Y-%m-%d %H:%M:%S')",
        )
        return f'echo "{inner}"'
    return line.strip()


def _find_ps_preamble_end(lines: list[str]) -> int:
    """Return the index of the first line after the PS preamble (testfunctions dot-source)."""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('. .\\scripts\\testfunctions') or \
                stripped.startswith('. ./scripts/testfunctions'):
            return i + 1
    return 0


def ps_to_sh(ps_path: Path) -> str:
    """
    Read *ps_path* and return the equivalent bash script content.

    :param ps_path: path to the PS test-docs-cases.ps1 file
    :return: complete SH script as a string
    """
    lines = ps_path.read_text(encoding='utf-8').splitlines()
    output: list[str] = [SH_PREAMBLE.rstrip('\n')]

    i = _find_ps_preamble_end(lines)

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            output.append('')
            i += 1
            continue

        if re.match(r'^\s*bexhoma\s+\w+', stripped):
            subcmd, flags, logfile, end = _parse_ps_block(lines, i)
            if logfile and flags:
                output.extend(_make_sh_comment_lines(flags))
                output.extend(_make_sh_command_lines(subcmd, flags, logfile))
            i = end + 1
            continue

        if stripped.startswith('Write-Host'):
            output.append(_convert_write_host(stripped))
            i += 1
            continue

        m_sleep = _RE_SLEEP.match(stripped)
        if m_sleep:
            output.append(f'sleep {m_sleep.group(1)}')
            i += 1
            continue

        if stripped == 'Invoke-CleanLogs':
            output.append('clean_logs')
            i += 1
            continue

        # Comment lines, kubectl lines, variable assignments, and anything else.
        output.append(stripped)
        i += 1

    return '\n'.join(output) + '\n'


if __name__ == '__main__':
    content = ps_to_sh(PS_FILE)
    SH_FILE.write_text(content, encoding='utf-8')
    print(f'Generated {SH_FILE}')
    line_count = content.count('\n')
    cmd_count = content.count('run &>$LOG_DIR/')
    print(f'  {line_count} lines, {cmd_count} bexhoma commands')
