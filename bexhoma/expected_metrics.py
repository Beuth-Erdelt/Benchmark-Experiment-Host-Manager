"""
List of the monitoring metrics an experiment fetched, checked against its result folder.

A fetch that fails before it queries Prometheus (dashboard pod gone, broken
stream, an exception in ``metrics.py``) leaves no ``Metrics missing for`` line,
so :mod:`bexhoma.missing_metrics` cannot see it. Instead, every fetch writes
down which metric files it is going to produce, and the summary checks that
each one is in the result folder.

* While the run is going, :func:`record` appends rows to
  ``bexhoma-metrics-expected.csv`` (one row per connection, component type and
  metric, see :data:`FIELDS`). The rows follow the rules of DBMSBenchmarker's
  ``monitor.metrics.fetchMetric()``, which writes no file for an inactive
  metric, for an application metric of another component, or for an
  application metric outside the loading and benchmarking phases of the SUT
  (:func:`expected_metric_names`). The number of rows is kept in the workload
  (:data:`WORKLOAD_KEY` in ``queries.config``), so a folder that lost the list
  fails instead of being skipped as an older result.
* The list is written only to the local result folder. It reaches the dashboard
  pod with the final upload of the whole folder, after the last download, so a
  copy in the pod can never overwrite a newer local one.
* :func:`check` reads only the result folder. A row is present when its
  per-connection file ``query_{component_type}_metric_{metric}_{connection}.csv``
  exists, or, after ``-rp`` merged those into
  ``query_{component_type}_metric_{metric}.csv`` and deleted them, when that
  aggregate has a column for the connection. Values are never judged: a metric
  that is 0 or NaN over the whole window can be correct (e.g. the number of
  vacuums when none ran). A file and a column correspond one to one, so the
  check gives the same answer before and after the cleanup.
* A fetch that was never queued has no row. The phase times in
  ``connections.config`` are a second source the fetch code does not write: a
  connection that loaded needs rows for ``loading`` and ``loader``, one that was
  benchmarked rows for ``benchmarking`` and ``benchmarker``, when other
  connections of the same configuration have rows of that type.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import csv
import os
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

from .monitoring_math import JOB_QUERY_SETS, read_connections

__all__ = [
    "FILENAME", "WORKLOAD_KEY", "FIELDS", "STATUS_MISSING", "STATUS_NOT_FETCHED",
    "LOADING_COMPONENTS", "BENCHMARKING_COMPONENTS",
    "expected_metric_names", "query_set", "metric_filename", "aggregate_filename",
    "record", "read", "check", "write_check", "describe", "CheckResult", "Miss",
]

#: The list in the result folder.
FILENAME = "bexhoma-metrics-expected.csv"
#: Workload key (``queries.config``) holding the number of rows of the list.
WORKLOAD_KEY = "monitoring_expected_metrics"
#: Columns of the list.
FIELDS = ("connection", "configuration", "component_type", "metrics_type", "metric",
          "time_start", "time_end", "source")
#: Status of a row whose file and aggregate column are both absent.
STATUS_MISSING = "missing"
#: Status of a (connection, component type) whose phase ran but that has no row at all.
STATUS_NOT_FETCHED = "not fetched"
#: Component types fetched for the loading phase of a connection that loaded.
LOADING_COMPONENTS = ("loading", "loader")
#: Component types fetched for the benchmarking phase of a connection with a benchmarker job.
BENCHMARKING_COMPONENTS = ("benchmarking", "benchmarker")

_LOCK = threading.Lock()
_KEY = ("connection", "component_type", "metric")


def query_set(monitoring: dict, metrics_type: str, component_type: str) -> str:
    """Metric set a fetch uses, as ``MetricsCollector.fetch`` and ``metrics.py`` choose it.

    A job component (loader, data generator, benchmarker) uses its own query set
    when the connection has one (:data:`JOB_QUERY_SETS`); a set the connection
    does not have falls back to ``metrics`` (as ``metrics.py`` does).

    :param monitoring: ``connectiondata['monitoring']``.
    :param metrics_type: ``metrics_type`` of the fetch.
    :param component_type: Monitoring component type of the fetch.
    :return: Key of the metric set in ``monitoring``.
    """
    if metrics_type == 'metrics' and JOB_QUERY_SETS.get(component_type) in monitoring:
        metrics_type = JOB_QUERY_SETS[component_type]
    if metrics_type and metrics_type in monitoring:
        return metrics_type
    return 'metrics'


def expected_metric_names(connectiondata: dict, metrics_type: str, component: str,
                          component_type: str) -> list[str]:
    """Metrics one ``metrics.py`` run writes a file for.

    Mirrors ``monitor.metrics.fetchMetric()`` of DBMSBenchmarker: nothing for an
    inactive connection or one without a Prometheus URL; no file for a metric with
    ``active`` false, for a metric bound to another ``component``, and for an
    application metric outside a loading or benchmarking component type when an
    application endpoint exists.

    :param connectiondata: The connection's config dict.
    :param metrics_type: ``metrics_type`` of the fetch.
    :param component: ``component`` of the fetch (``-com``).
    :param component_type: Monitoring component type of the fetch (``-ct``).
    :return: Metric keys, in the order of the metric set.
    """
    monitoring = connectiondata.get('monitoring') or {}
    if not connectiondata.get('active', True) or not monitoring.get('prometheus_url'):
        return []
    url_app = monitoring.get('prometheus_url_application', '')
    names = []
    for name, metric in (monitoring.get(query_set(monitoring, metrics_type, component_type)) or {}).items():
        if not isinstance(metric, dict) or not metric.get('active', True):
            continue
        if component and 'component' in metric and metric['component'] != component:
            continue
        if (metric.get('type') == 'application' and url_app
                and 'loading' not in component_type and 'benchmarking' not in component_type):
            continue
        names.append(name)
    return names


def metric_filename(component_type: str, metric: str, connection: str) -> str:
    """Per-connection metric file of a fetch (``metrics.py``)."""
    return f"query_{component_type}_metric_{metric}_{connection}.csv"


def aggregate_filename(component_type: str, metric: str) -> str:
    """Aggregate of a metric over all connections (``metrics.evaluation.py``, ``-rp``)."""
    return f"query_{component_type}_metric_{metric}.csv"


def read(result_dir) -> Optional[list[dict]]:
    """Rows of the list in a result folder.

    :param result_dir: The experiment's result folder.
    :return: The rows, or None when the folder has no list.
    """
    path = Path(result_dir) / FILENAME
    try:
        with open(path, newline='', encoding='utf-8') as f:
            return [dict(row) for row in csv.DictReader(f)]
    except FileNotFoundError:
        return None


def record(result_dir, rows: Iterable[dict]) -> int:
    """Add rows to the list (atomic rewrite; a row replaces an earlier one with the same key).

    Fetches of one batch are queued from several threads, so this holds a lock.

    :param result_dir: The experiment's result folder.
    :param rows: Dicts with the keys of :data:`FIELDS`.
    :return: Number of rows in the list afterwards.
    """
    rows = list(rows)
    path = Path(result_dir) / FILENAME
    with _LOCK:
        existing = read(result_dir) or []
        by_key = {tuple(row.get(k, '') for k in _KEY): row for row in existing}
        for row in rows:
            by_key[tuple(str(row.get(k, '')) for k in _KEY)] = {k: row.get(k, '') for k in FIELDS}
        if rows or not path.exists():
            os.makedirs(result_dir, exist_ok=True)
            tmp = path.with_name(path.name + '.tmp')
            with open(tmp, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(by_key.values())
            os.replace(tmp, path)
        return len(by_key)


@dataclass(frozen=True)
class Miss:
    """One expected metric (or, for ``not fetched``, one component) that is not in the folder."""

    connection: str
    component_type: str
    metric: str
    status: str


@dataclass
class CheckResult:
    """Outcome of :func:`check`.

    ``skipped`` names why no test applies (older result, monitoring off);
    ``list_missing`` is set when ``queries.config`` records a list the folder lacks.
    """

    rows: list = field(default_factory=list)
    misses: list = field(default_factory=list)
    skipped: str = ""
    list_missing: bool = False

    @property
    def passed(self) -> bool:
        """True when nothing is missing and the list is there."""
        return not self.misses and not self.list_missing


def _aggregate_columns(folder: Path, filename: str, cache: dict) -> set:
    """Column names of an aggregate metric file (its header line), cached per file."""
    if filename not in cache:
        try:
            with open(folder / filename, encoding='utf-8') as f:
                header = f.readline().strip()
            cache[filename] = {name.strip().strip('"') for name in header.split(',') if name.strip()}
        except OSError:
            cache[filename] = set()
    return cache[filename]


def _loading_ran(connection: dict) -> bool:
    """Whether this connection's repetition loaded (and so fetched loading metrics)."""
    if connection.get('loading_inherited') or connection.get('loading_deactivated'):
        return False
    try:
        return float(connection.get('time_loading') or 0) > 0
    except (TypeError, ValueError):
        return False


def _benchmarking_ran(connection: dict) -> bool:
    """Whether a benchmarker job of this connection ran (it has pod timespans)."""
    timespans = (connection.get('hostsystem') or {}).get('benchmarking_timespans') or {}
    return any(timespans.values()) if isinstance(timespans, dict) else bool(timespans)


def _not_fetched(rows: list, connections: list) -> list:
    """(connection, component type) pairs whose phase ran but that have no row.

    Only the base components, and only types that other connections of the same
    configuration have rows for (a configuration without SUT monitoring fetches no
    ``benchmarking``). A connection is known by its ``name`` and, for the entries
    DBMSBenchmarker expands per pod, its job-level ``orig_name``.
    """
    present = {(row['connection'], row['component_type']) for row in rows}
    types_of_configuration: dict = {}
    for row in rows:
        types_of_configuration.setdefault(row.get('configuration', ''), set()).add(row['component_type'])
    misses = []
    seen = set()
    for connection in connections:
        name = connection.get('orig_name') or connection.get('name', '')
        names = {name, connection.get('name', '')}
        types = types_of_configuration.get(connection.get('configuration', ''), set())
        required = []
        if _loading_ran(connection):
            required += [t for t in LOADING_COMPONENTS if t in types]
        if _benchmarking_ran(connection):
            required += [t for t in BENCHMARKING_COMPONENTS if t in types]
        for component_type in required:
            if (name, component_type) in seen:
                continue
            if not any((n, component_type) in present for n in names):
                seen.add((name, component_type))
                misses.append(Miss(name, component_type, "", STATUS_NOT_FETCHED))
    return misses


def check(result_dir, expected_count=None, connections: Optional[list] = None) -> CheckResult:
    """Check every expected metric against the result folder.

    Reads only local files: the list, the metric CSVs (per connection, or the
    aggregates after ``-rp``) and ``connections.config``.

    :param result_dir: The experiment's result folder.
    :param expected_count: :data:`WORKLOAD_KEY` of the workload; None for results
        from before the list (then a folder without a list is skipped).
    :param connections: Connection dicts; read from the folder when None.
    :return: The outcome.
    """
    folder = Path(result_dir)
    rows = read(folder)
    if rows is None:
        if expected_count:
            return CheckResult(list_missing=True)
        return CheckResult(skipped="no expected-metrics list (older result)")
    if connections is None:
        connections = read_connections(folder)
    orig_names: dict = {}
    for connection in connections:
        if connection.get('orig_name'):
            orig_names.setdefault(connection.get('name', ''), set()).add(connection['orig_name'])
    cache: dict = {}
    misses = []
    for row in rows:
        connection, component_type, metric = row['connection'], row['component_type'], row['metric']
        if (folder / metric_filename(component_type, metric, connection)).is_file():
            continue
        columns = _aggregate_columns(folder, aggregate_filename(component_type, metric), cache)
        if columns & ({connection} | orig_names.get(connection, set())):
            continue
        misses.append(Miss(connection, component_type, metric, STATUS_MISSING))
    misses += _not_fetched(rows, connections)
    return CheckResult(rows=rows, misses=misses)


def write_check(path, result: CheckResult) -> None:
    """Write the status of every row (and every ``not fetched`` component) to a CSV.

    :param path: Target file, e.g. ``report/metrics-check.csv``.
    :param result: Outcome of :func:`check`.
    """
    missing = {(m.connection, m.component_type, m.metric) for m in result.misses if m.status == STATUS_MISSING}
    fieldnames = ("connection", "component_type", "metric", "source", "status")
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in result.rows:
            key = (row['connection'], row['component_type'], row['metric'])
            writer.writerow(dict(connection=key[0], component_type=key[1], metric=key[2],
                                 source=row.get('source', ''),
                                 status=STATUS_MISSING if key in missing else "present"))
        for miss in result.misses:
            if miss.status == STATUS_NOT_FETCHED:
                writer.writerow(dict(connection=miss.connection, component_type=miss.component_type,
                                     metric="", source="", status=STATUS_NOT_FETCHED))


def describe(result: CheckResult, examples: int = 5) -> list[tuple[str, str, list[str]]]:
    """Misses grouped per (connection, component type), largest first.

    A failed fetch loses all metrics of its component at once, so one line per
    fetch is easier to read than one per metric.

    :param result: Outcome of :func:`check`.
    :param examples: Number of metric names kept per group.
    :return: ``(connection, component_type, text)`` per group, text like
        ``"30 of 30 metrics missing (total_cpu_util, ...)"`` or ``"not fetched"``.
    """
    totals: dict = {}
    for row in result.rows:
        key = (row['connection'], row['component_type'])
        totals[key] = totals.get(key, 0) + 1
    groups: dict = {}
    for miss in result.misses:
        groups.setdefault((miss.connection, miss.component_type, miss.status), []).append(miss.metric)
    lines = []
    for (connection, component_type, status), metrics in sorted(groups.items(), key=lambda g: (-len(g[1]), g[0])):
        if status == STATUS_NOT_FETCHED:
            text = "not fetched (the phase ran, but no fetch was queued)"
        else:
            shown = ", ".join(sorted(metrics)[:examples]) + (", ..." if len(metrics) > examples else "")
            text = f"{len(metrics)} of {totals.get((connection, component_type), len(metrics))} metrics missing ({shown})"
        lines.append((connection, component_type, text))
    return lines
