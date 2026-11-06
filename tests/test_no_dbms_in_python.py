"""
Guard: no DBMS-specific details in Python code (ratchet).

Design goal: nothing in a Python file is specific to a DBMS; all DBMS
adjustments live in ``cluster.config``'s ``dockers:`` section, in the
``experiments/`` scripts, or in ``k8s/`` templates. This test scans the Python
code for the names of the DBMS that ``k8s-cluster.config`` declares (plus the
names of their client tools) in

* string literals that are not docstrings,
* identifiers (names, attributes, arguments, keyword arguments, def/class names).

Docstrings, ``#`` comments and the ``help=``/``description=``/``epilog=`` texts of the command line
(its documentation) are exempt: they may name a DBMS as an example.

The existing violations are recorded per file in
``tests/dbms_guard_baseline.json``. The test fails when a file gets *more*
occurrences of a name than recorded (a new violation) and also when it gets
*fewer* (shrink the baseline, so the gain is kept). Regenerate with::

    BEXHOMA_UPDATE_SNAPSHOTS=1 python -m pytest tests/test_no_dbms_in_python.py

The goal is an empty baseline. Not scanned: ``tests/``, ``dev/``, ``docs/``,
``build/``, ``TPCTC23/``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import collections
import json
import os
import re
import unittest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dbms_guard_baseline.json')
_UPDATE = os.environ.get('BEXHOMA_UPDATE_SNAPSHOTS') == '1'

#: ``dockers:`` keys that are not a DBMS.
_NOT_A_DBMS = {'Dummy', 'Hardware'}
#: Client tools and spellings of a DBMS that the ``dockers:`` keys do not show.
_EXTRA_NAMES = {'postgres', 'psql', 'mysql', 'mysqld', 'mariadb', 'redis-cli', 'mclient', 'duckdb',
                'ysqlsh', 'cockroach', 'clickhouse-client', 'cqlsh'}
#: Names that are not DBMS-specific code in a given file: bexhoma's own message queue is
#: a Redis pod (``bexhoma-messagequeue``), driven with its client; it is infrastructure,
#: not a system under test, so it is no adjustment to a DBMS.
_INFRASTRUCTURE = {'bexhoma/clusters.py': {'redis-cli'}}
#: Directories (relative to the repository) whose Python files are scanned.
_SCAN_ROOTS = ('bexhoma',)


def dbms_names() -> list:
    """Names of the DBMS declared in ``k8s-cluster.config`` plus :data:`_EXTRA_NAMES`."""
    with open(os.path.join(_REPO, 'k8s-cluster.config'), encoding='utf-8') as file:
        config = ast.literal_eval(file.read())
    names = {name for name in config['dockers'] if name not in _NOT_A_DBMS}
    return sorted(names | _EXTRA_NAMES)


def _pattern(names: list) -> re.Pattern:
    """A name matches as written or in lower case, not inside a longer lower-case word.

    So ``Redis`` does not match ``Redistribute`` while ``MariaDBCS`` still matches ``MariaDB``.
    """
    forms = {form for name in names for form in (name, name.lower())}
    alternatives = '|'.join(re.escape(form) for form in sorted(forms, key=len, reverse=True))
    return re.compile(r'(?<![A-Za-z])(' + alternatives + r')(?![a-z])')


def python_files() -> list:
    """Repository-relative paths of the scanned Python files (root scripts and the package)."""
    files = [name for name in os.listdir(_REPO) if name.endswith('.py')]
    for root in _SCAN_ROOTS:
        for folder, _, names in os.walk(os.path.join(_REPO, root)):
            files += [os.path.relpath(os.path.join(folder, n), _REPO) for n in names if n.endswith('.py')]
    return sorted(f.replace('\\', '/') for f in files)


def _docstring_nodes(tree: ast.AST) -> set:
    """Ids of the ``Constant`` nodes that are module, class or function docstrings."""
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                ids.add(id(body[0].value))
    return ids


#: Keyword arguments whose string is documentation (of the command line), not code.
_DOCUMENTATION_KEYWORDS = ("help", "description", "epilog")


def _documentation_nodes(tree: ast.AST) -> set:
    """Ids of the ``Constant`` nodes that are the value of a ``help=``/``description=``/``epilog=`` keyword."""
    return {id(node.value) for node in ast.walk(tree)
            if isinstance(node, ast.keyword) and node.arg in _DOCUMENTATION_KEYWORDS
            and isinstance(node.value, ast.Constant)}


def code_texts(source: str) -> list:
    """Texts of a file's string literals and identifiers, without docstrings and command line help texts."""
    tree = ast.parse(source)
    docstrings = _docstring_nodes(tree) | _documentation_nodes(tree)
    texts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings:
            texts.append(node.value)
        elif isinstance(node, ast.Name):
            texts.append(node.id)
        elif isinstance(node, ast.Attribute):
            texts.append(node.attr)
        elif isinstance(node, ast.arg):
            texts.append(node.arg)
        elif isinstance(node, ast.keyword) and node.arg:
            texts.append(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            texts.append(node.name)
    return texts


def scan() -> dict:
    """``{file: {name: occurrences}}`` of DBMS names in code, files without any left out."""
    pattern = _pattern(dbms_names())
    lowercase = {name.lower(): name for name in dbms_names()}
    result = {}
    for relative in python_files():
        with open(os.path.join(_REPO, relative), encoding='utf-8') as file:
            texts = code_texts(file.read())
        counts = collections.Counter()
        for text in texts:
            for match in pattern.findall(text):
                name = lowercase.get(match.lower(), match)
                if name not in _INFRASTRUCTURE.get(relative, ()):
                    counts[name] += 1
        if counts:
            result[relative] = dict(sorted(counts.items()))
    return result


class NoDbmsInPythonTest(unittest.TestCase):
    """DBMS names in code may only decrease against the recorded baseline."""

    def test_baseline_is_not_exceeded_or_stale(self) -> None:
        actual = scan()
        if _UPDATE:
            with open(_BASELINE, 'w', encoding='utf-8', newline='\n') as file:
                json.dump(actual, file, indent=1, sort_keys=True)
                file.write('\n')
            return
        with open(_BASELINE, encoding='utf-8') as file:
            baseline = json.load(file)
        worse, better = [], []
        for relative in sorted(set(actual) | set(baseline)):
            now, before = actual.get(relative, {}), baseline.get(relative, {})
            for name in sorted(set(now) | set(before)):
                if now.get(name, 0) > before.get(name, 0):
                    worse.append(f'{relative}: {name} {before.get(name, 0)} -> {now[name]}')
                elif now.get(name, 0) < before.get(name, 0):
                    better.append(f'{relative}: {name} {before[name]} -> {now.get(name, 0)}')
        self.assertFalse(worse, 'new DBMS-specific code (move it to cluster.config dockers:):\n' + '\n'.join(worse))
        self.assertFalse(better, 'fewer DBMS names than the baseline, regenerate it '
                                 '(BEXHOMA_UPDATE_SNAPSHOTS=1) to keep the gain:\n' + '\n'.join(better))

    def test_docstrings_and_comments_are_exempt(self) -> None:
        source = '"""PostgreSQL docs."""\n\ndef f():\n    """MySQL docs."""\n    # MariaDB comment\n    return 1\n'
        self.assertEqual(code_texts(source), ['f'])

    def test_command_line_help_is_exempt(self) -> None:
        source = "parser.add_argument('-x', help='only for PostgreSQL', choices=['A'])\nparser = ArgumentParser(description='MySQL tool')\n"
        self.assertNotIn('only for PostgreSQL', code_texts(source))
        self.assertNotIn('MySQL tool', code_texts(source))
        self.assertIn('A', code_texts(source))

    def test_code_is_found(self) -> None:
        source = 'x = "PostgreSQL"\nclass PgDuckDB:\n    pass\nconfig.docker == "TiDB"\n'
        pattern = _pattern(['PostgreSQL', 'PgDuckDB', 'TiDB'])
        found = [m for text in code_texts(source) for m in pattern.findall(text)]
        self.assertEqual(sorted(found), ['PgDuckDB', 'PostgreSQL', 'TiDB'])

    def test_longer_words_do_not_match(self) -> None:
        self.assertEqual(_pattern(['Redis']).findall('Redistribute redis_key Redis'), ['redis', 'Redis'])


if __name__ == '__main__':
    unittest.main()
