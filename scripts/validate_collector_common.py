"""
Shared setup and checks of the collector validators (validate_collector_*.py).

The experiment codes come from the collector logs in logs_tests/, the
results from the zips in tests/validations/ (one per code).

Locally (default), the results are read from the result folder of
cluster.config: a result without zip is archived, a zip without result
folder is extracted there.

With ``--zips`` (CI), neither cluster.config nor the result folder is used:
the zips are extracted into a temporary folder, and a code without zip
fails.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import argparse
import ast
import os
import re
import sys
import tempfile
import traceback
import zipfile

import pandas as pd

__all__ = [
    "LOG_DIR",
    "LOGS",
    "VALIDATIONS_DIR",
    "Validation",
    "code_from_log",
]

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(REPO, "logs_tests")
VALIDATIONS_DIR = os.path.join(REPO, "tests", "validations")
CLUSTER_CONFIG = os.path.join(REPO, "cluster.config")
#: Line of a bexhoma log naming the code of its experiment.
_CODE_IN_LOG = re.compile(r"Experiment\s+: has code (\d+)")
_LINE = "=" * 60

#: Collector logs of test-docs-collector per validator; their experiments
#: are the input of validate_collector_<name>.py.
LOGS = {
    "benchbase": [
        "docs_benchbase_postgresql_collector_1.log",
        "docs_benchbase_postgresql_collector_2.log",
        "docs_benchbase_postgresql_collector_3.log",
    ],
    "benchbase_mt": [
        "docs_benchbase_postgresql_collector_tenants_schema.log",
        "docs_benchbase_postgresql_collector_tenants_database.log",
        "docs_benchbase_postgresql_collector_tenants_container.log",
    ],
    "hammerdb": [
        "docs_hammerdb_postgresql_collector_1.log",
        "docs_hammerdb_postgresql_collector_2.log",
        "docs_hammerdb_postgresql_collector_3.log",
    ],
    # one experiment per tool: each tool has its own log parser and columns
    "hardware": [
        "docs_hardware_fio_collector.log",
        "docs_hardware_sysbench_collector.log",
        "docs_hardware_sockperf_collector.log",
        "docs_hardware_netperf_collector.log",
    ],
    "ssb": [
        "docs_ssb_postgresql_collector_1.log",
        "docs_ssb_postgresql_collector_2.log",
        "docs_ssb_postgresql_collector_3.log",
    ],
    "tpcds": [
        "docs_tpcds_postgresql_collector_1.log",
        "docs_tpcds_postgresql_collector_2.log",
        "docs_tpcds_postgresql_collector_3.log",
    ],
    "tpch": [
        "docs_tpch_postgresql_collector_1.log",
        "docs_tpch_postgresql_collector_2.log",
        "docs_tpch_postgresql_collector_3.log",
    ],
    "tpch_mt": [
        "docs_tpch_postgresql_collector_tenants_schema.log",
        "docs_tpch_postgresql_collector_tenants_database.log",
        "docs_tpch_postgresql_collector_tenants_container.log",
    ],
    "ycsb": [
        "docs_ycsb_postgresql_collector_1.log",
        "docs_ycsb_postgresql_collector_2.log",
        "docs_ycsb_postgresql_collector_3.log",
    ],
}


def code_from_log(filename: str) -> str | None:
    """Return the experiment code named in a log of logs_tests/, or None."""
    try:
        with open(os.path.join(LOG_DIR, filename), encoding="utf-8",
                  errors="replace") as f:
            for line in f:
                match = _CODE_IN_LOG.search(line)
                if match:
                    return match.group(1)
    except FileNotFoundError:
        pass
    return None


def _zip_path(code: str) -> str:
    """Path of the zip holding the result of an experiment."""
    return os.path.join(VALIDATIONS_DIR, f"{code}.zip")


def _archive(path: str, code: str) -> None:
    """Zip the result folder <path>/<code>, paths relative to <path>."""
    print(f"Archiving result {code} -> tests/validations/{code}.zip")
    with zipfile.ZipFile(_zip_path(code), "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(os.path.join(path, code)):
            for file in files:
                file_path = os.path.join(root, file)
                zf.write(file_path, os.path.relpath(file_path, path))


def _extract(path: str, code: str) -> None:
    """Extract the zip of an experiment into <path>."""
    print(f"Extracting tests/validations/{code}.zip -> {code}")
    with zipfile.ZipFile(_zip_path(code), "r") as zf:
        zf.extractall(path)


class Validation:
    """
    Setup, checks and bottom line of one collector validator.

    :param name: Key in :data:`LOGS`, the part after validate_collector_.
    :type name: str
    """

    def __init__(self, name: str):
        parser = argparse.ArgumentParser(
            description=f"Validate the collector output of {name}.")
        parser.add_argument(
            "--zips", action="store_true",
            help="read the results from tests/validations/ only, "
                 "without cluster.config and result folder (CI)")
        parser.add_argument(
            "--preview", action="store_true",
            help="show head() of every DataFrame")
        args = parser.parse_args()
        self.preview = args.preview
        self.from_zips = args.zips
        self.failures = []
        self._temporary = None
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_colwidth", None)
        pd.options.display.max_columns = None
        pd.options.display.float_format = "{:.2f}".format
        self.codes = [code for code in map(code_from_log, LOGS[name])
                      if code is not None]
        if not self.codes:
            self._abort("no experiment codes found in logs_tests/ "
                        "- run test-docs-collector first.")
        if self.from_zips:
            self.path = self._extract_zips()
        else:
            self.path = self._sync_result_folder()

    def _abort(self, message: str) -> None:
        """Print an error and stop with exit code 1."""
        print(f"ERROR: {message}", file=sys.stderr)
        sys.exit(1)

    def _extract_zips(self) -> str:
        """Extract the zips of all codes into a temporary folder."""
        missing = [code for code in self.codes
                   if not os.path.isfile(_zip_path(code))]
        if missing:
            self._abort(f"no zip in tests/validations/ for {missing} - "
                        "rerun locally without --zips to create it.")
        self._temporary = tempfile.TemporaryDirectory(
            prefix="bexhoma-validation-", ignore_cleanup_errors=True)
        for code in self.codes:
            _extract(self._temporary.name, code)
        return self._temporary.name

    def _sync_result_folder(self) -> str:
        """Archive results without zip, extract zips without result."""
        with open(CLUSTER_CONFIG, encoding="utf-8") as f:
            path = ast.literal_eval(f.read())["benchmarker"]["resultfolder"]
        os.makedirs(VALIDATIONS_DIR, exist_ok=True)
        for code in self.codes:
            has_folder = os.path.isdir(os.path.join(path, code))
            has_zip = os.path.isfile(_zip_path(code))
            if has_folder and not has_zip:
                _archive(path, code)
            elif has_zip and not has_folder:
                _extract(path, code)
        return path

    @staticmethod
    def sep(title: str) -> None:
        """Print a section title."""
        print(f"\n{_LINE}\n{title}\n{_LINE}")

    def check_df(self, df, label: str,
                 required_cols: list[str] | None = None) -> bool:
        """
        Check that a DataFrame is not empty and has the required columns.

        :param df: DataFrame returned by the collector.
        :type df: pandas.DataFrame
        :param label: Name of the check in the output.
        :type label: str
        :param required_cols: Columns that must be present.
        :type required_cols: list[str]
        :return: True if all checks passed.
        :rtype: bool
        """
        if df is None or len(df) == 0:
            print(f"  FAIL  {label}: DataFrame is empty")
            self.failures.append(f"{label}: empty")
            return False
        print(f"  OK    {label}: shape={df.shape}")
        missing = [c for c in required_cols or [] if c not in df.columns]
        if missing:
            print(f"  FAIL  {label}: missing columns {missing}")
            self.failures.append(f"{label}: missing columns {missing}")
            return False
        if self.preview:
            print(df.head())
        return True

    def create_collector(self, collector_class, title: str):
        """
        Create the collector of the codes; stop if that fails.

        :param collector_class: Collector class of the benchmark.
        :type collector_class: type
        :param title: Name of the collector in the output.
        :type title: str
        :return: The collector.
        """
        self.sep(f"Setup: {title}")
        try:
            collector = collector_class(self.path, self.codes)
        except Exception:
            traceback.print_exc()
            print(f"\n{_LINE}\nRESULT: FAIL "
                  f"(collector could not be created)\n{_LINE}")
            sys.exit(1)
        print("  OK    collector created")
        return collector

    def finish(self) -> None:
        """Print the bottom line and exit, 1 if a check failed."""
        print(f"\n{_LINE}")
        if self.failures:
            print(f"RESULT: FAIL  ({len(self.failures)} issue(s))")
            for failure in self.failures:
                print(f"  - {failure}")
        else:
            print("RESULT: ALL CHECKS PASSED")
        print(_LINE)
        if self._temporary is not None:
            self._temporary.cleanup()
        sys.exit(1 if self.failures else 0)
