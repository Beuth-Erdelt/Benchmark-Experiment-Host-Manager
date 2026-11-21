"""
The collector validators (scripts/validate_collector_*.py) on the results in
tests/validations/, without cluster or result folder.

The codes come from the collector logs in logs_tests/: every code has a zip,
and every zip belongs to a code. Then each validator runs with ``--zips``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import os
import subprocess
import sys

import pytest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS = os.path.join(_REPO, "scripts")
sys.path.insert(0, _SCRIPTS)
from validate_collector_common import (  # noqa: E402
    LOGS, VALIDATIONS_DIR, code_from_log)

#: Lines of a validator's output shown when it fails.
_TAIL = 60


def _codes():
    """Code of every collector log, by log name."""
    return {log: code_from_log(log)
            for logs in LOGS.values() for log in logs}


def test_every_log_names_a_code():
    missing = [log for log, code in _codes().items() if code is None]
    assert not missing, f"no experiment code in logs_tests/{missing}"


def test_every_code_has_a_zip():
    missing = [f"{log}: {code}" for log, code in _codes().items()
               if code and not os.path.isfile(
                   os.path.join(VALIDATIONS_DIR, f"{code}.zip"))]
    assert not missing, (
        f"no zip in tests/validations/ for {missing} - run the validators "
        "locally without --zips to create them, and commit the zips")


def test_every_zip_belongs_to_a_log():
    codes = set(_codes().values())
    orphans = sorted(name for name in os.listdir(VALIDATIONS_DIR)
                     if name.endswith(".zip") and name[:-4] not in codes)
    assert not orphans, (
        f"zips in tests/validations/ without collector log: {orphans} "
        "- left over from an earlier test-docs-collector run, delete them")


@pytest.mark.parametrize("name", sorted(LOGS))
def test_validator(name):
    script = os.path.join(_SCRIPTS, f"validate_collector_{name}.py")
    # a script starts with scripts/ on sys.path; without the repository first,
    # it would import an installed bexhoma instead of the code under test
    python_path = os.pathsep.join(
        filter(None, [_REPO, os.environ.get("PYTHONPATH")]))
    result = subprocess.run(
        [sys.executable, script, "--zips"], capture_output=True,
        text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8",
             "PYTHONPATH": python_path})
    output = (result.stdout + result.stderr).splitlines()
    assert result.returncode == 0, "\n".join(output[-_TAIL:])
