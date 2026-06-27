#!/usr/bin/env python3
"""
Sync bexhoma commands in PowerShell test scripts to match the bash scripts.

For each bexhoma call in a test-docs-*.ps1 file, if its flags differ from the
canonical bash version (ignoring PS-specific quoting), replace the PS command
block with a regenerated PS-formatted version of the bash command.

Preserved PS conventions:
  - Backtick (`) line continuation
  - Inline <# description #> comments aligned to column 32
  - Double-quoted values for arguments containing commas

Run from the repo root:
    python scripts/_sync_ps.py
"""

import re
from pathlib import Path

SCRIPTS_DIR = Path("scripts")

_RE_PS_COMMENT = re.compile(r'<#.*?#>')
_RE_BASH_REDIRECT = re.compile(r'&>\s*\$LOG_DIR/(\S+\.log)')
_RE_PS_REDIRECT = re.compile(r'Out-File\s+"?\$LOG_DIR[\\\/](\S+\.log)')

COMMENT_COL = 32


def _strip_one_quote_pair(s: str) -> str:
    """Remove exactly one surrounding double-quote pair, if present."""
    if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s


# ── SH command loading ─────────────────────────────────────────────────────────

def _parse_sh_header_comment(line: str) -> tuple[str | None, str]:
    """
    Return (flag, description) from one SH header comment line.

    Handles both normal lines (flag+value < 30 chars, description at col 32)
    and overlong lines (1-space gap after the flag/value).
    """
    if not line.startswith('# -'):
        return None, ''
    content = line[2:]  # strip '# '
    tokens = content.split()
    if not tokens or not tokens[0].startswith('-'):
        return None, ''
    flag = tokens[0]
    prefix_end = len(tokens[0])
    if len(tokens) > 1 and not tokens[1].startswith('-'):
        prefix_end += 1 + len(tokens[1])
    if prefix_end < 30:
        desc = content[30:].strip()
    else:
        desc = content[prefix_end:].strip()
    return flag, desc


def _collect_bash_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """Collect a backslash-continued bash command block."""
    block = [lines[start].rstrip()]
    i = start
    while block[-1].endswith('\\') and i + 1 < len(lines):
        i += 1
        block.append(lines[i].rstrip())
    return block, i


def extract_sh_commands(sh_path: Path) -> dict[str, dict]:
    """
    Return {logfile: {'lines': [...], 'comments': {flag: desc}}} for each
    bexhoma call in *sh_path*.

    :param sh_path: path to a test-docs-*.sh file
    :return: mapping from log filename to command info
    """
    lines = sh_path.read_text(encoding='utf-8').splitlines()
    result: dict[str, dict] = {}
    i = 0
    while i < len(lines):
        if re.match(r'^\s*bexhoma\s+\w+', lines[i]):
            block, end = _collect_bash_block(lines, i)
            logfile = None
            for bl in block:
                m = _RE_BASH_REDIRECT.search(bl)
                if m:
                    logfile = m.group(1)
            if logfile:
                comments: dict[str, str] = {}
                k = i - 1
                while k >= 0 and lines[k].startswith('# '):
                    flag, desc = _parse_sh_header_comment(lines[k])
                    if flag:
                        comments[flag] = desc
                    k -= 1
                result[logfile] = {'lines': block, 'comments': comments}
            i = end
        i += 1
    return result


def load_all_sh(scripts_dir: Path) -> dict[str, dict]:
    """Aggregate commands from all test-docs-*.sh files."""
    cmds: dict[str, dict] = {}
    for sh in sorted(scripts_dir.glob('test-docs-*.sh')):
        cmds.update(extract_sh_commands(sh))
    return cmds


# ── Flag parsing ───────────────────────────────────────────────────────────────

def _parse_flags(tokens: list[str]) -> dict[str, str | bool]:
    """Parse a flat token list into {flag: value_or_True}."""
    flags: dict[str, str | bool] = {}
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.startswith('-'):
            if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                flags[tok] = tokens[i + 1]
                i += 2
            else:
                flags[tok] = True
                i += 1
        else:
            i += 1
    return flags


def _flags_from_sh(sh_info: dict) -> dict[str, str | bool]:
    """Parse a SH command block into normalised {flag: value} (outer quotes stripped)."""
    flags: dict[str, str | bool] = {}
    for line in sh_info['lines']:
        clean = line.rstrip().rstrip('\\').strip()
        if '&>' in clean:
            clean = clean[:clean.index('&>')].strip()
        if not clean or clean.startswith('#') or clean == 'run':
            continue
        m = re.match(r'bexhoma\s+(\w+)', clean)
        if m:
            flags['__subcommand__'] = m.group(1)
            continue
        tokens = clean.split()
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok.startswith('-'):
                if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                    flags[tok] = _strip_one_quote_pair(tokens[i + 1])  # normalise: strip shell quotes
                    i += 2
                else:
                    flags[tok] = True
                    i += 1
            else:
                i += 1
    return flags


def _flags_from_ps_block(block: list[str]) -> dict[str, str | bool]:
    """
    Parse a PS command block into normalised {flag: value}.

    PS-specific quoting is stripped for comparison: ``"1,1"`` → ``1,1``.
    """
    flags: dict[str, str | bool] = {}
    for line in block:
        clean = _RE_PS_COMMENT.sub('', line).rstrip().rstrip('`').strip()
        if '2>&1' in clean or 'Out-File' in clean or clean == 'run':
            continue
        m = re.match(r'bexhoma\s+(\w+)', clean)
        if m:
            flags['__subcommand__'] = m.group(1)
            continue
        tokens = clean.split()
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok.startswith('-'):
                if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                    flags[tok] = _strip_one_quote_pair(tokens[i + 1])  # normalise: drop PS quotes
                    i += 2
                else:
                    flags[tok] = True
                    i += 1
            else:
                i += 1
    return flags


# ── PS command reconstruction ──────────────────────────────────────────────────

def _ps_value(raw: str) -> str:
    """Wrap *raw* in double quotes when it contains a comma (required by PS)."""
    if ',' in raw:
        return f'"{raw}"'
    return raw


def _ps_flag_line(flag: str, value: str | None, desc: str) -> str:
    """Return one PS flag line with inline comment and backtick continuation."""
    prefix = f'  {flag}' if value is None else f'  {flag} {_ps_value(value)}'
    if desc:
        padding = max(1, COMMENT_COL - len(prefix))
        return f'{prefix}{" " * padding}<# {desc} #> `'
    return f'{prefix} `'


def sh_to_ps_block(sh_info: dict, logfile: str) -> list[str]:
    """
    Reconstruct a full PS command block from SH command lines and header comments.

    :param sh_info: dict with keys 'lines' (SH command lines) and 'comments' ({flag: desc})
    :param logfile: log file name used in the Out-File redirect
    :return: list of PS-formatted lines (no trailing newlines)
    """
    sh_lines = sh_info['lines']
    comments = sh_info['comments']

    bm = re.match(r'\s*(bexhoma\s+\w+)', sh_lines[0])
    subcommand = bm.group(1).strip() if bm else 'bexhoma'
    ps: list[str] = [f'{subcommand} `']

    for sh_line in sh_lines[1:]:
        clean = sh_line.rstrip().rstrip('\\').strip()
        if '&>' in clean:
            clean = clean[:clean.index('&>')].strip()
        if not clean or clean.startswith('#') or clean == 'run':
            continue
        tokens = clean.split()
        idx = 0
        while idx < len(tokens):
            tok = tokens[idx]
            if tok.startswith('-'):
                if idx + 1 < len(tokens) and not tokens[idx + 1].startswith('-'):
                    raw = _strip_one_quote_pair(tokens[idx + 1])  # normalise shell quotes before PS re-quoting
                    ps.append(_ps_flag_line(tok, raw, comments.get(tok, '')))
                    idx += 2
                else:
                    ps.append(_ps_flag_line(tok, None, comments.get(tok, '')))
                    idx += 1
            else:
                idx += 1

    ps.append(f'  run 2>&1 | Out-File "$LOG_DIR\\{logfile}" -Encoding utf8')
    return ps


# ── PS file patching ───────────────────────────────────────────────────────────

def _collect_ps_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    Collect a PS bexhoma command block (backtick-continued lines plus the
    trailing ``run 2>&1 | Out-File …`` line which has no backtick).
    """
    block = [lines[start].rstrip()]
    i = start
    while block[-1].rstrip().endswith('`') and i + 1 < len(lines):
        i += 1
        block.append(lines[i].rstrip())
    return block, i


def patch_ps_file(ps_path: Path, sh_commands: dict[str, dict]) -> bool:
    """
    Patch *ps_path* in-place so every bexhoma command matches the SH version.

    :param ps_path: path to the .ps1 file to update
    :param sh_commands: output of :func:`load_all_sh`
    :return: True if the file was modified
    """
    lines = ps_path.read_text(encoding='utf-8').splitlines(keepends=False)
    out: list[str] = []
    changed = False
    i = 0
    while i < len(lines):
        if re.match(r'^\s*bexhoma\s+\w+', lines[i]):
            block, end = _collect_ps_block(lines, i)
            logfile = None
            for bl in block:
                m = _RE_PS_REDIRECT.search(bl)
                if m:
                    logfile = m.group(1)
            if logfile and logfile in sh_commands:
                sh_flags = _flags_from_sh(sh_commands[logfile])
                ps_flags = _flags_from_ps_block(block)
                if sh_flags != ps_flags:
                    out.extend(sh_to_ps_block(sh_commands[logfile], logfile))
                    i = end + 1
                    changed = True
                    continue
        out.append(lines[i])
        i += 1
    if changed:
        ps_path.write_text('\n'.join(out) + '\n', encoding='utf-8', newline='\n')
    return changed


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    sh_commands = load_all_sh(SCRIPTS_DIR)
    print(f'Loaded {len(sh_commands)} commands from test-docs-*.sh scripts.\n')

    total_changed = 0
    for ps_file in sorted(SCRIPTS_DIR.glob('test-docs-*.ps1')):
        if patch_ps_file(ps_file, sh_commands):
            print(f'  updated  {ps_file.name}')
            total_changed += 1
        else:
            print(f'  no change {ps_file.name}')

    print(f'\n{total_changed} file(s) updated.')
