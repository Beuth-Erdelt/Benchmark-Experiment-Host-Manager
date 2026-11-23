"""The documentation is consistent with itself and with the code (offline, no Sphinx needed).

S3 of dev/plan-software-quality.md:

1. every ``docs/*.md`` page can be reached from the toctree of ``docs/index.rst``,
   directly or through links from reachable pages (an orphan page is found by no reader);
2. every relative link in ``docs/*.md`` and ``README.md`` points to an existing file, and
   every ``#anchor`` to a Markdown page points to an existing heading (MyST
   ``myst_heading_anchors``, GitHub-style slugs) or an explicit anchor;
3. every function or method the docs name in code style, ``name()`` or ``obj.name(args)``,
   is defined in the repository's Python code, unless it is a SQL, PromQL or library
   function (``FOREIGN``). Stale method names after a rename fail here.

Code blocks are skipped for links and anchors; inline code is skipped for links only.
"""
import ast
import builtins
import re
import unittest
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
PAGES = sorted(DOCS.glob('*.md')) + [ROOT / 'README.md']

#: Pages that need not be reachable: docs/README.md is GitHub's landing page of the folder.
UNREACHABLE_ALLOWED = {'README.md'}

#: Functions the docs name that are not defined in this repository: SQL and PromQL
#: functions, DBMS procedures, library calls, and notation. Compared case-insensitively.
FOREIGN = {
    # SQL and DBMS functions or types
    'avg', 'cast', 'coalesce', 'concat', 'count', 'date', 'decimal', 'grouping', 'lag', 'lead',
    'number', 'varchar', 'varchar2', 'pg_stat_reset', 'pg_stat_reset_shared', 'reset_sql_stats',
    'master_add_node',
    # PromQL
    'rate', 'irate',
    # library calls and methods of built-in types
    'safe_dump', 'get', 'default',
    # big-O notation
    'o',
}

_FENCE = re.compile(r'^\s*(```|~~~)')
_LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
_HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
_CALL = re.compile(r'`([\w.]*?)(\w+)\([^`]*\)`')
_SCHEME = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')


def _lines_outside_code_blocks(path: Path):
    """Yield (line number, line) of a Markdown file, leaving out fenced code blocks."""
    fenced = False
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
        if _FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            yield number, line


def _slug(title: str) -> str:
    """GitHub-style heading slug, as MyST builds it with ``myst_heading_anchors``."""
    title = re.sub(r'<[^>]+>', '', title)
    title = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', title)
    title = title.replace('`', '').strip().lower()
    title = re.sub(r'[^\w\- ]', '', title)
    return title.replace(' ', '-')


_anchor_cache: dict = {}


def _anchors(path: Path) -> set:
    """Heading slugs (with -1, -2 ... for repeats) and explicit anchors of a Markdown file."""
    if path not in _anchor_cache:
        found, seen = set(), {}
        for _, line in _lines_outside_code_blocks(path):
            heading = _HEADING.match(line)
            if heading:
                slug = _slug(heading.group(2))
                count = seen.get(slug, 0)
                found.add(slug if count == 0 else f'{slug}-{count}')
                seen[slug] = count + 1
            found.update(re.findall(r'<a\s+(?:name|id)="([^"]+)"', line))
            label = re.match(r'^\(([\w\-]+)\)=\s*$', line)
            if label:
                found.add(label.group(1))
        _anchor_cache[path] = found
    return _anchor_cache[path]


def _local_links(page: Path):
    """Yield (line number, target) of every relative link of a page, outside code."""
    for number, line in _lines_outside_code_blocks(page):
        for target in _LINK.findall(re.sub(r'`[^`]*`', '', line)):
            if _SCHEME.match(target) or target.startswith('//'):
                continue
            yield number, target


def _defined_names() -> set:
    """Names of every function and class in the repository's Python code."""
    names = set()
    sources = [*ROOT.glob('*.py')]
    for folder in ('bexhoma', 'agent', 'scripts', 'images'):
        sources.extend((ROOT / folder).rglob('*.py'))
    for path in sources:
        try:
            tree = ast.parse(path.read_text(encoding='utf-8', errors='replace'))
        except SyntaxError:
            continue
        names.update(node.name for node in ast.walk(tree)
                     if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)))
    return names


class DocsConsistencyTest(unittest.TestCase):

    def test_every_page_is_reachable_from_the_toctree(self) -> None:
        index = (DOCS / 'index.rst').read_text(encoding='utf-8')
        roots = {DOCS / name for name in re.findall(r'^\s+\./([\w\-]+\.md)\s*$', index, re.M)}
        reached, queue = set(roots), deque(roots)
        while queue:
            page = queue.popleft()
            for _, target in _local_links(page):
                file_part = target.partition('#')[0]
                linked = (page.parent / file_part).resolve() if file_part else None
                if linked and linked.suffix == '.md' and linked.parent == DOCS and linked not in reached:
                    reached.add(linked)
                    queue.append(linked)
        orphans = sorted(page.name for page in DOCS.glob('*.md')
                         if page.resolve() not in {p.resolve() for p in reached}
                         and page.name not in UNREACHABLE_ALLOWED)
        self.assertEqual(orphans, [], "pages no reader can reach: add them to docs/index.rst or link them")

    def test_relative_links_and_anchors_resolve(self) -> None:
        broken = []
        for page in PAGES:
            for number, target in _local_links(page):
                file_part, _, anchor = target.partition('#')
                destination = (page.parent / file_part).resolve() if file_part else page
                where = f'{page.relative_to(ROOT).as_posix()}:{number}'
                if not destination.exists():
                    broken.append(f'{where}: no file {target}')
                elif anchor and destination.suffix == '.md' and anchor not in _anchors(destination):
                    broken.append(f'{where}: no heading or anchor {target}')
        self.assertEqual(broken, [])

    def test_named_functions_exist_in_the_code(self) -> None:
        defined = _defined_names()
        known = defined | set(dir(builtins)) | {name.lower() for name in FOREIGN}
        missing = []
        for page in PAGES:
            for number, line in enumerate(page.read_text(encoding='utf-8').splitlines(), start=1):
                for _, name in _CALL.findall(line):
                    if name not in known and name.lower() not in FOREIGN:
                        missing.append(f'{page.relative_to(ROOT).as_posix()}:{number}: {name}()')
        self.assertEqual(missing, [], "renamed or removed? Otherwise add a foreign name to FOREIGN")

    def test_the_checks_see_what_they_check(self) -> None:
        """Guards against a check that silently matches nothing."""
        self.assertEqual(_slug('Example: `bexhoma tpch` (SF 1)'), 'example-bexhoma-tpch-sf-1')
        self.assertGreater(sum(1 for page in PAGES for _ in _local_links(page)), 300)
        calls = sum(len(_CALL.findall(line)) for page in PAGES
                    for line in page.read_text(encoding='utf-8').splitlines())
        self.assertGreater(calls, 300)


if __name__ == '__main__':
    unittest.main()
