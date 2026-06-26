#!/usr/bin/env python3
"""
Sync bexhoma example commands in docs/ from the corresponding test-docs-*.sh scripts.

For each bexhoma call in a test-docs-*.sh file, the script records the canonical
command (already reordered by _reorder_flags.py).  It then scans every *.md file
under docs/ for bash code blocks that contain a matching log-file redirect and
replaces the old command with the canonical one.

Run from the repo root:
    python scripts/_sync_docs.py
"""

import re
import sys
from pathlib import Path


# ── Extract commands from test scripts ────────────────────────────────────────

def extract_commands(sh_path: Path) -> dict[str, list[str]]:
    """Return {log_filename: [command_lines]} for every bexhoma call in *sh_path*."""
    lines = sh_path.read_text(encoding='utf-8').splitlines()
    result: dict[str, list[str]] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^\s*bexhoma\s+\w+', line):
            cmd: list[str] = [line.rstrip()]
            while cmd[-1].rstrip().endswith('\\') and i + 1 < len(lines):
                i += 1
                cmd.append(lines[i].rstrip())
            # Find log filename in the last line
            m = re.search(r'&>\s*\$LOG_DIR/(\S+\.log)', cmd[-1])
            if m:
                log_file = m.group(1)
                result[log_file] = cmd
        i += 1
    return result


def load_all_commands(scripts_dir: Path) -> dict[str, list[str]]:
    """Aggregate commands from all test-docs-*.sh files."""
    all_cmds: dict[str, list[str]] = {}
    for sh in sorted(scripts_dir.glob('test-docs-*.sh')):
        all_cmds.update(extract_commands(sh))
    return all_cmds


# ── Patch doc files ────────────────────────────────────────────────────────────

def find_bexhoma_block(lines: list[str], start: int) -> tuple[int, int] | None:
    """
    Starting at *start*, find the extent of a bexhoma command block.
    Returns (block_start, block_end) indices (inclusive) or None.
    """
    if not re.match(r'^\s*bexhoma\s+\w+', lines[start]):
        return None
    end = start
    while lines[end].rstrip().endswith('\\') and end + 1 < len(lines):
        end += 1
    return start, end


def build_doc_command(cmd_lines: list[str]) -> list[str]:
    """
    Convert a test-script command (with comment lines stripped) to doc format.

    Test scripts add a comment block above the command; docs only have the
    command itself.  Comment lines (# …) are stripped; the command lines are
    kept as-is.
    """
    return [l for l in cmd_lines if not l.startswith('#')]


def patch_doc_file(doc_path: Path, commands: dict[str, list[str]]) -> bool:
    """Patch *doc_path* in-place; return True if the file was changed."""
    text = doc_path.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=False)

    in_bash_block = False
    changed = False
    i = 0
    out: list[str] = []

    while i < len(lines):
        raw = lines[i]

        # Track bash code fences
        if raw.strip() == '```bash':
            in_bash_block = True
            out.append(raw)
            i += 1
            continue
        if raw.strip() == '```' and in_bash_block:
            in_bash_block = False
            out.append(raw)
            i += 1
            continue

        if in_bash_block and re.match(r'^\s*bexhoma\s+\w+', raw):
            span = find_bexhoma_block(lines, i)
            if span:
                s, e = span
                block = lines[s:e + 1]
                # Find log file in the last line of the block
                m = re.search(r'&>\s*\$LOG_DIR/(\S+\.log)', block[-1])
                if m and m.group(1) in commands:
                    new_cmd = build_doc_command(commands[m.group(1)])
                    if block != new_cmd:
                        out.extend(new_cmd)
                        i = e + 1
                        changed = True
                        continue
        out.append(raw)
        i += 1

    if changed:
        doc_path.write_text('\n'.join(out) + '\n', encoding='utf-8', newline='\n')
    return changed


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    repo = Path(__file__).resolve().parent.parent
    scripts_dir = repo / 'scripts'
    docs_dir = repo / 'docs'

    commands = load_all_commands(scripts_dir)
    print(f'Loaded {len(commands)} commands from test-docs-*.sh scripts.\n')

    changed = 0
    for md in sorted(docs_dir.glob('*.md')):
        if patch_doc_file(md, commands):
            print(f'  updated  {md.name}')
            changed += 1
        else:
            print(f'  no change {md.name}')

    print(f'\n{changed} file(s) updated.')
