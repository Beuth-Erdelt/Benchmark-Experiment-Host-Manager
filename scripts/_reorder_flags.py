#!/usr/bin/env python3
"""
Reorder flags in bexhoma test-script calls to match the canonical ordering
defined in scripts/CLAUDE.md.  Handles both .sh and .ps1 formats.

Run from the repo root:
    python scripts/_reorder_flags.py
"""

import re
import sys
from pathlib import Path

# ── Canonical flag ordering ────────────────────────────────────────────────────

FLAG_ORDER = [
    # A: Target
    '-dbms', '-sf',
    # B: Benchmark identity
    '-xbt', '-xwl',
    # C: Benchmark timing
    '-xqr', '-xrt', '-xsd',
    # D: Throughput targets
    '-xtb', '-xnbf', '-xnlf',
    # E: Sweep dimensions
    '-nc', '-ne',
    # F: Loading parallelism
    '-nlp', '-nlt',
    # G: Benchmarking parallelism
    '-nbp', '-nbt',
    # H: SUT topology
    '-xnsr', '-nw', '-nwr', '-nws',
    # I: Connection pooling
    '-xnpp', '-xnpi', '-xnpo',
    # J: Post-load init (logical order)
    '-xii', '-xic', '-xis', '-xcol',
    # K: Query/load modifiers
    '-xlit', '-xnls', '-xrcp', '-xshq',
    # L: Extra features
    '-xbatch', '-xconn', '-xdt', '-xio', '-xkey', '-xlat', '-xli', '-xmet', '-xop', '-xsbs',
    # M: Monitoring
    '-m', '-ma', '-mc',
    # N: Experiment control
    '-ms', '-sl', '-ss', '-t', '-tr',
    # O: SUT resources
    '-lc', '-lr', '-rc', '-rr',
    '-rct', '-rg', '-rgt',
    '-rsr', '-rss', '-rst',
    # P: Multi-tenancy
    '-mtb', '-mtn', '-mtv',
    # Q: Node pinning
    '-rnn', '-rnl', '-rnb',
]

FLAG_RANK = {f: i for i, f in enumerate(FLAG_ORDER)}

# Flags that are grouped on one line in .sh output (in this order)
INIT_FLAGS = ['-xii', '-xic', '-xis', '-xcol']
NODE_FLAGS = ['-rnn', '-rnl', '-rnb']

MODES = frozenset({'run', 'load', 'start', 'profiling', 'empty', 'summary'})

# Long-form aliases to normalise to short form
LONG_TO_SHORT = {
    '--dbms':           '-dbms',
    '--workload':       '-xwl',
    '--xworkload':      '-xwl',
    '--benchmark':      '-xbt',
}


# ── Shared helpers ─────────────────────────────────────────────────────────────

def nrm(flag: str) -> str:
    """Normalise a flag to its canonical short form."""
    return LONG_TO_SHORT.get(flag, flag)


def rank(flag: str) -> int:
    return FLAG_RANK.get(nrm(flag), len(FLAG_ORDER))


def is_flag(tok: str) -> bool:
    """True for -flag and --flag tokens (not negative numbers)."""
    return bool(re.match(r'^--?[a-zA-Z]', tok))


def parse_flag_pairs(tokens: list[str]) -> list[tuple[str, str | None]]:
    """Convert a flat token list into [(flag, value_or_None), ...], stopping at mode."""
    pairs: list[tuple[str, str | None]] = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in MODES:
            break
        if t.startswith('&>') or t.startswith('>>') or t == '2>&1':
            i += 1
            continue
        if is_flag(t):
            f = nrm(t)
            nxt = tokens[i + 1] if i + 1 < len(tokens) else None
            if nxt and not is_flag(nxt) and nxt not in MODES and not nxt.startswith('&>'):
                pairs.append((f, nxt))
                i += 2
            else:
                pairs.append((f, None))
                i += 1
        else:
            i += 1
    return pairs


def reorder_and_dedup(pairs: list[tuple[str, str | None]]) -> list[tuple[str, str | None]]:
    seen: set[str] = set()
    result = []
    for flag, value in sorted(pairs, key=lambda p: rank(p[0])):
        if flag not in seen:
            seen.add(flag)
            result.append((flag, value))
    return result


def fmt_comment_sh(flag: str, value: str | None, description: str, col: int = 32) -> str:
    prefix = f'# {flag}' + (f' {value}' if value is not None else '')
    if description:
        prefix = prefix.ljust(col) if len(prefix) < col else prefix + ' '
        prefix += description
    return prefix


def fmt_flag_ps1(flag: str, value: str | None, description: str, col: int = 32) -> str:
    prefix = f'  {flag}' + (f' {value}' if value is not None else '')
    if description:
        prefix = prefix.ljust(col) if len(prefix) < col else prefix + ' '
        prefix += f'<# {description} #>'
    return prefix + ' `'


# ── .sh processing ─────────────────────────────────────────────────────────────

def parse_sh_comment(line: str) -> tuple[str, str | None, str] | None:
    """Parse '# -flag [value]   description' → (flag, value, description) or None."""
    s = line.rstrip()
    if not re.match(r'^\s*# -', s):
        return None
    content = re.sub(r'^\s*# ', '', s)
    m = re.search(r'\s{2,}', content)
    if m:
        prefix = content[:m.start()].strip()
        description = content[m.end():]
    else:
        # Value may exceed column 32 (e.g. -ne $VERY_LONG_VAR,...); split as
        # flag + value + description using the first two whitespace boundaries.
        parts3 = content.split(None, 2)
        if len(parts3) >= 3 and parts3[0].startswith('-'):
            prefix = f'{parts3[0]} {parts3[1]}'
            description = parts3[2]
        elif len(parts3) == 2 and parts3[0].startswith('-'):
            prefix = parts3[0]
            description = parts3[1]
        else:
            prefix = content.strip()
            description = ''
    parts = prefix.split(None, 1)
    if not parts or not parts[0].startswith('-'):
        return None
    return nrm(parts[0]), (parts[1] if len(parts) > 1 else None), description


def is_bexhoma_sh(line: str) -> bool:
    return bool(re.match(r'^\s*bexhoma\s+\w+\b', line))


def cmd_name_sh(first_line: str) -> str:
    m = re.match(r'^\s*(bexhoma\s+\w+)', first_line)
    return m.group(1) if m else first_line.strip().split()[0]


def build_sh_cmd(name: str, pairs: list[tuple[str, str | None]],
                 mode: str, redirect: str | None) -> list[str]:
    lines = [f'{name} \\']
    pair_dict = {f: v for f, v in pairs}
    init_present = [f for f in INIT_FLAGS if f in pair_dict]
    node_present = [f for f in NODE_FLAGS if f in pair_dict]
    emitted: set[str] = set()

    for flag, value in pairs:
        if flag in emitted:
            continue
        if flag in INIT_FLAGS:
            if not emitted.intersection(INIT_FLAGS):
                lines.append(f'  {" ".join(init_present)} \\')
                emitted.update(init_present)
        elif flag in NODE_FLAGS:
            if not emitted.intersection(NODE_FLAGS):
                parts = ' '.join(
                    f'{f} {pair_dict[f]}' for f in node_present
                    if pair_dict.get(f) is not None
                )
                lines.append(f'  {parts} \\')
                emitted.update(node_present)
        else:
            emitted.add(flag)
            val = f' {value}' if value is not None else ''
            lines.append(f'  {flag}{val} \\')

    redir = f' {redirect}' if redirect else ''
    lines.append(f'  {mode}{redir}')
    return lines


def get_redirect_sh(lines: list[str]) -> str | None:
    for line in reversed(lines):
        m = re.search(r'&>\S+', line)
        if m:
            return m.group(0)
    return None


def get_mode_sh(lines: list[str]) -> str:
    last = re.sub(r'&>\S+', '', lines[-1]).strip().rstrip('\\').strip()
    for w in reversed(last.split()):
        if w in MODES:
            return w
    return 'run'


def process_sh_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    src_lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0

    while i < len(src_lines):
        raw = src_lines[i]
        if is_bexhoma_sh(raw):
            # Collect preceding comment block from out[] by scanning backwards
            cb_start = len(out)
            while cb_start > 0 and re.match(r'^\s*# -', out[cb_start - 1].rstrip()):
                cb_start -= 1
            comment_lines = [l.rstrip('\n') for l in out[cb_start:]]
            out = out[:cb_start]

            # Collect all command lines (including continuations)
            cmd_lines = [raw.rstrip('\n')]
            while cmd_lines[-1].rstrip().endswith('\\') and i + 1 < len(src_lines):
                i += 1
                cmd_lines.append(src_lines[i].rstrip('\n'))

            # Parse
            name = cmd_name_sh(cmd_lines[0])
            redirect = get_redirect_sh(cmd_lines)
            mode = get_mode_sh(cmd_lines)

            all_tokens = ' '.join(
                l.rstrip().rstrip('\\').strip() for l in cmd_lines
            ).split()
            # Strip command-name prefix tokens
            if all_tokens and all_tokens[0] == 'bexhoma':
                all_tokens = all_tokens[2:]
            elif all_tokens and all_tokens[0] in ('nohup', 'python'):
                skip = 3 if all_tokens[0] == 'nohup' else 2
                all_tokens = all_tokens[skip:]

            pairs = parse_flag_pairs(all_tokens)
            pairs = reorder_and_dedup(pairs)

            # Build description map from comment block
            desc_map: dict[str, str] = {}
            for cl in comment_lines:
                parsed = parse_sh_comment(cl)
                if parsed:
                    desc_map[parsed[0]] = parsed[2]

            # Reconstruct
            for flag, value in pairs:
                out.append(fmt_comment_sh(flag, value, desc_map.get(flag, '')) + '\n')
            for cl in build_sh_cmd(name, pairs, mode, redirect):
                out.append(cl + '\n')
        else:
            out.append(raw)
        i += 1

    new_text = ''.join(out)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8', newline='\n')
        return True
    return False


# ── .ps1 processing ────────────────────────────────────────────────────────────

def is_bexhoma_ps1(line: str) -> bool:
    return bool(re.match(r'^\s*bexhoma\s+\w+\s*`\s*$', line.rstrip()))


def parse_ps1_flag_line(line: str) -> tuple[str, str | None, str] | None:
    """Parse '  -flag [value]    <# description #> `' → (flag, value, desc) or None."""
    s = line.rstrip().rstrip('`').strip()
    desc_m = re.search(r'<#\s*(.*?)\s*#>', s)
    description = desc_m.group(1) if desc_m else ''
    s = re.sub(r'<#.*?#>', '', s).strip()
    parts = s.split(None, 1)
    if not parts or not is_flag(parts[0]):
        return None
    flag = nrm(parts[0])
    rest = parts[1].strip() if len(parts) > 1 else None
    # rest is a value only if it doesn't look like a flag
    value = rest if (rest and not is_flag(rest)) else None
    return flag, value, description


def process_ps1_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    src_lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0

    while i < len(src_lines):
        raw = src_lines[i]
        if is_bexhoma_ps1(raw):
            cmd_m = re.match(r'^\s*(bexhoma\s+\w+)', raw.strip())
            cmd_name = cmd_m.group(1) if cmd_m else 'bexhoma'

            # Collect call lines
            call_lines = [raw.rstrip('\n')]
            while True:
                i += 1
                if i >= len(src_lines):
                    break
                call_lines.append(src_lines[i].rstrip('\n'))
                if not src_lines[i].rstrip().endswith('`'):
                    break

            # Parse flags from flag lines (not first command line, not last mode line)
            triples: list[tuple[str, str | None, str]] = []
            mode = 'run'
            redirect = ''
            for cl in call_lines[1:]:
                s = cl.rstrip()
                if not s.rstrip('`').strip().startswith('-'):
                    # Mode/redirect line
                    s2 = s.strip()
                    m2 = re.match(r'^(\w+)\s+(.*)', s2)
                    if m2 and m2.group(1) in MODES:
                        mode = m2.group(1)
                        redirect = m2.group(2)
                    continue
                parsed = parse_ps1_flag_line(cl)
                if parsed:
                    triples.append(parsed)

            # Sort
            triples = sorted(triples, key=lambda t: rank(t[0]))
            seen: set[str] = set()
            deduped = []
            for t in triples:
                if t[0] not in seen:
                    seen.add(t[0])
                    deduped.append(t)
            triples = deduped

            # Reconstruct
            out.append(f'{cmd_name} `\n')
            for flag, value, description in triples:
                out.append(fmt_flag_ps1(flag, value, description) + '\n')
            out.append(f'  {mode} {redirect}\n' if redirect else f'  {mode}\n')
        else:
            out.append(raw)
        i += 1

    new_text = ''.join(out)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8', newline='\n')
        return True
    return False


# ── Entry point ────────────────────────────────────────────────────────────────

SKIP = {
    'testfunctions.sh', 'testfunctions.ps1',
    'run_collector_tests.sh', 'run_collector_tests.ps1',
    'run_collector_validations.sh', 'run_collector_validations.ps1',
    '_reorder_flags.py',
}

if __name__ == '__main__':
    root = Path(__file__).parent
    changed = 0

    for p in sorted(root.glob('test*.sh')):
        if p.name in SKIP:
            continue
        if process_sh_file(p):
            print(f'  updated  {p.name}')
            changed += 1
        else:
            print(f'  no change {p.name}')

    for p in sorted(root.glob('test*.ps1')):
        if p.name in SKIP:
            continue
        if process_ps1_file(p):
            print(f'  updated  {p.name}')
            changed += 1
        else:
            print(f'  no change {p.name}')

    print(f'\n{changed} file(s) updated.')
