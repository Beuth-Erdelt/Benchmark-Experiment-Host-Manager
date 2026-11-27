#!/usr/bin/env python3
"""
Sync bexhoma commands in PowerShell test scripts to match the bash scripts.

For each bexhoma call in a test-docs-*.ps1 file, if it differs from the
canonical bash version (ignoring PS-specific quoting), replace the PS command
block with a regenerated PS-formatted version of the bash command.

A call is compared as (subcommand, positional arguments, flags in order, mode):
- every value of a flag is kept (``-dbms PostgreSQL PgDuckDB``);
- a repeated flag (``--set a --set b``) is kept every time, in its order;
- positional arguments stay (``bexhoma experiment <yaml>``), and a one-line
  bash call becomes a one-line PS call;
- the mode (``run``, ``load``, ``start``, ...) is taken from the bash call.

Preserved PS conventions:
  - Backtick (`) line continuation
  - Inline <# description #> comments aligned to column 32
  - Double-quoted values for arguments containing commas

Run from the repo root:
    python scripts/_sync_ps.py            # rewrite the .ps1 files
    python scripts/_sync_ps.py --check    # only list the files it would change (exit 1 if any)
"""

import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path("scripts")

_RE_PS_COMMENT = re.compile(r'<#.*?#>')
_RE_BASH_REDIRECT = re.compile(r'&>\s*\$LOG_DIR/(\S+\.log)')
_RE_PS_REDIRECT = re.compile(r'Out-File\s+"?\$LOG_DIR[\\\/](\S+\.log)')

COMMENT_COL = 32

MODES = frozenset({'run', 'load', 'start', 'profiling', 'empty', 'summary'})


def _strip_one_quote_pair(s: str) -> str:
    """Remove exactly one surrounding double-quote pair, if present."""
    if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s


def _is_flag(tok: str) -> bool:
    """True for -flag and --flag tokens (not negative numbers)."""
    return bool(re.match(r'^--?[a-zA-Z]', tok))


# ── Call model ─────────────────────────────────────────────────────────────────

def parse_call(tokens: list[str]) -> dict:
    """
    Split the tokens of one call (redirect already removed) into its parts.

    :param tokens: e.g. ``['bexhoma', 'tpch', '-dbms', 'A', 'B', '--set', 'x', 'run']``
    :return: ``{'command': 'bexhoma tpch', 'positional': [...], 'flags': [(flag, [values])...], 'mode': str|None}``;
        values without their outer double quotes.
    """
    command = ' '.join(tokens[:2])
    positional: list[str] = []
    flags: list[tuple[str, list[str]]] = []
    mode = None
    for tok in tokens[2:]:
        if _is_flag(tok):
            flags.append((tok, []))
        elif tok in MODES:
            # the mode word; no flag value in these scripts equals a mode
            mode = tok
        elif flags:
            flags[-1][1].append(_strip_one_quote_pair(tok))
        else:
            positional.append(_strip_one_quote_pair(tok))
    return {'command': command, 'positional': positional, 'flags': flags, 'mode': mode}


def _comparable(call: dict) -> tuple:
    return (call['command'], tuple(call['positional']),
            tuple((flag, tuple(values)) for flag, values in call['flags']), call['mode'])


# ── SH command loading ─────────────────────────────────────────────────────────

def _parse_sh_header_comment(line: str) -> tuple[str | None, str | None, str]:
    """
    Return (flag, value, description) from one SH header comment line.

    Handles both normal lines (flag+value < 30 chars, description at col 32)
    and overlong lines (1-space gap after the flag/value).
    """
    if not line.startswith('# -'):
        return None, None, ''
    content = line[2:]  # strip '# '
    tokens = content.split()
    if not tokens or not tokens[0].startswith('-'):
        return None, None, ''
    flag = tokens[0]
    value = None
    prefix_end = len(tokens[0])
    if len(tokens) > 1 and not tokens[1].startswith('-'):
        value = tokens[1]
        prefix_end += 1 + len(tokens[1])
    if prefix_end < 30:
        desc = content[30:].strip()
    else:
        desc = content[prefix_end:].strip()
    # a comment is not a format string: '%%' is a literal percent written twice
    return flag, value, desc.replace('%%', '%')


def _collect_bash_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """Collect a backslash-continued bash command block."""
    block = [lines[start].rstrip()]
    i = start
    while block[-1].endswith('\\') and i + 1 < len(lines):
        i += 1
        block.append(lines[i].rstrip())
    return block, i


def _sh_tokens(block: list[str]) -> list[str]:
    text = ' '.join(line.rstrip().rstrip('\\').strip() for line in block)
    if '&>' in text:
        text = text[:text.index('&>')]
    return text.split()


def extract_sh_commands(sh_path: Path) -> dict[str, dict]:
    """
    Return {logfile: {'lines': [...], 'comments': {...}}} for each bexhoma call in *sh_path*.

    ``comments`` maps ``(flag, value)`` and ``(flag, None)`` to the description of the
    header comment, so repeated flags keep their own descriptions.

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
                comments: dict[tuple[str, str | None], str] = {}
                k = i - 1
                while k >= 0 and lines[k].startswith('# '):
                    flag, value, desc = _parse_sh_header_comment(lines[k])
                    if flag:
                        comments[(flag, value)] = desc
                        comments[(flag, None)] = desc   # scanning upwards: the first comment of a flag wins
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


def call_from_sh(sh_info: dict) -> dict:
    """The call of a SH command block."""
    return parse_call(_sh_tokens(sh_info['lines']))


def call_from_ps_block(block: list[str]) -> dict:
    """
    The call of a PS command block. PS-specific quoting is stripped: ``"1,1"`` → ``1,1``.
    """
    text = ' '.join(_RE_PS_COMMENT.sub('', line).rstrip().rstrip('`').strip() for line in block)
    if '2>&1' in text:
        text = text[:text.index('2>&1')]
    return parse_call(text.split())


# ── PS command reconstruction ──────────────────────────────────────────────────

def _ps_value(raw: str) -> str:
    """Wrap *raw* in double quotes when it contains a comma (required by PS)."""
    if ',' in raw:
        return f'"{raw}"'
    return raw


def _ps_flag_line(flag: str, values: list[str], desc: str) -> str:
    """Return one PS flag line with inline comment and backtick continuation."""
    prefix = '  ' + ' '.join([flag] + [_ps_value(value) for value in values])
    if desc:
        padding = max(1, COMMENT_COL - len(prefix))
        return f'{prefix}{" " * padding}<# {desc} #> `'
    return f'{prefix} `'


def sh_to_ps_block(sh_info: dict, logfile: str) -> list[str]:
    """
    Reconstruct a full PS command block from SH command lines and header comments.

    :param sh_info: dict with keys 'lines' (SH command lines) and 'comments' (see :func:`extract_sh_commands`)
    :param logfile: log file name used in the Out-File redirect
    :return: list of PS-formatted lines (no trailing newlines)
    """
    call = call_from_sh(sh_info)
    comments = sh_info['comments']
    redirect = f'2>&1 | Out-File "$LOG_DIR\\{logfile}" -Encoding utf8'
    head = ' '.join([call['command']] + [_ps_value(value) for value in call['positional']])
    tail = ' '.join(part for part in (call['mode'], redirect) if part)
    if len(sh_info['lines']) == 1:
        flags = ' '.join(' '.join([flag] + [_ps_value(value) for value in values]) for flag, values in call['flags'])
        return [' '.join(part for part in (head, flags, tail) if part)]
    ps: list[str] = [f'{head} `']
    for flag, values in call['flags']:
        desc = comments.get((flag, values[0] if len(values) == 1 else None), comments.get((flag, None), ''))
        ps.append(_ps_flag_line(flag, values, desc))
    ps.append(f'  {tail}')
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


def patch_ps_file(ps_path: Path, sh_commands: dict[str, dict], write: bool = True) -> bool:
    """
    Patch *ps_path* in-place so every bexhoma command matches the SH version.

    :param ps_path: path to the .ps1 file to update
    :param sh_commands: output of :func:`load_all_sh`
    :param write: False only reports whether the file would change
    :return: True if the file was (or would be) modified
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
                if _comparable(call_from_sh(sh_commands[logfile])) != _comparable(call_from_ps_block(block)):
                    out.extend(sh_to_ps_block(sh_commands[logfile], logfile))
                    i = end + 1
                    changed = True
                    continue
        out.append(lines[i])
        i += 1
    if changed and write:
        ps_path.write_text('\n'.join(out) + '\n', encoding='utf-8', newline='\n')
    return changed


# ── Entry point ────────────────────────────────────────────────────────────────

def main(argv: list[str]) -> int:
    check = '--check' in argv
    sh_commands = load_all_sh(SCRIPTS_DIR)
    print(f'Loaded {len(sh_commands)} commands from test-docs-*.sh scripts.\n')
    total_changed = 0
    for ps_file in sorted(SCRIPTS_DIR.glob('test-docs-*.ps1')):
        if patch_ps_file(ps_file, sh_commands, write=not check):
            print(f'  {"would update" if check else "updated"}  {ps_file.name}')
            total_changed += 1
        elif not check:
            print(f'  no change {ps_file.name}')
    print(f'\n{total_changed} file(s) {"would be " if check else ""}updated.')
    return 1 if check and total_changed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
