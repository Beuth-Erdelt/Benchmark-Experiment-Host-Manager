"""Make the suite independent of the directory pytest is started from.

Many tests open files such as ``contracts/contract_catalog.yml`` relative to
the repository root, so every test runs with that as the working directory.
"""
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _run_from_repo_root(monkeypatch):
    monkeypatch.chdir(_REPO_ROOT)
