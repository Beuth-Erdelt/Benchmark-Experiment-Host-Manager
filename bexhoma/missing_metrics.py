"""
Detection of monitoring metrics that Prometheus did not return.

DBMSBenchmarker's ``monitor.metrics.getMetrics()`` does not fail when a
Prometheus query comes back empty: it logs
``ERROR:root:Metrics missing for <title> (<query>)[ for connection <c>]: <url>``
and substitutes a series of zeros, which then reads like a measured idle
component. Two processes run that code, and both leave their output in the
result folder:

* ``bexhoma-metrics-{connection}-{component_type}.log`` — output of
  ``metrics.py`` in the dashboard pod, written by
  :meth:`bexhoma.configurations.metrics.MetricsCollector.fetch`.
* ``bexhoma-benchmarker-*.log`` — the DBMSBenchmarker pod (e.g. TPC-H, run
  with ``-mps``) fetching per-stream metrics itself.

Both processes may fetch the same metric for the same connection, so a gap
is reported once. Some gaps are expected and carry the reason in
``expected``: an optional component whose data was pre-existing (the data
generator then exits before the first scrape), and a metric that
``cluster.config`` marks ``sparse`` because its series only exists while the
value is non-zero (e.g. backends waiting on locks, or CPU throttling of a
container without a CPU limit), so no data means 0.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable

__all__ = [
    "MissingMetric", "parse_missing_metrics", "collect_missing_metrics", "fetch_log_name",
    "EXPECTED_DATA_PREEXISTING", "EXPECTED_SPARSE",
]

#: Log files that can carry the message, relative to the result folder.
_LOG_PATTERNS = ("bexhoma-metrics-*.log", "bexhoma-benchmarker-*.log")

_MARKER = re.compile(r"Metrics missing for (?P<label>.+?)(?:: \S*)?$")
_CONNECTION = re.compile(r"^(?P<label>.*) for connection (?P<connection>\S+)$")
_FETCH_LOG = re.compile(r"^bexhoma-metrics-.+-(?P<component>[^-]+)\.log$")

#: ``expected`` reason for a gap in an optional component (e.g. the data generator).
EXPECTED_DATA_PREEXISTING = "data pre-existing"
#: ``expected`` reason for a gap in a metric ``cluster.config`` marks ``sparse``.
EXPECTED_SPARSE = "series exists only while non-zero"


@dataclass(frozen=True)
class MissingMetric:
    """One metric query that returned no data, as logged by DBMSBenchmarker.

    ``component`` is the monitoring component type the log reports on
    (``benchmarking`` for a DBMSBenchmarker pod log). ``expected`` names why the gap is
    harmless, or is empty when the zero-filled values hide a real gap.
    """

    source: str
    title: str
    connection: str = ""
    query: str = ""
    component: str = ""
    expected: str = ""


def _component_of(source: str) -> str:
    """Monitoring component type a log reports on.

    A dashboard-pod fetch log names it (``bexhoma-metrics-{connection}-{component}.log``);
    a DBMSBenchmarker pod fetches its per-stream metrics during benchmarking.
    Anything else (e.g. a parsed text without a file) has none.
    """
    if match := _FETCH_LOG.match(source):
        return match.group("component")
    if source.startswith("bexhoma-benchmarker-"):
        return "benchmarking"
    return ""


def _balanced(text: str) -> bool:
    """Whether every parenthesis in ``text`` closes one opened before it, and all are closed."""
    depth = 0
    for character in text:
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def _split_label(label: str) -> tuple[str, str, str] | None:
    """Split ``<title> (<query>)[ for connection <c>]`` into its parts.

    Titles may contain parentheses themselves (``Max Transaction Duration (WAL
    Wait)``), so the split is the first `` (`` that leaves both the title and
    the query with balanced parentheses.

    :return: ``(title, query, connection)``, or ``None`` when the label has no query.
    """
    connection = ""
    if match := _CONNECTION.match(label):
        label, connection = match.group("label"), match.group("connection")
    if not label.endswith(")"):
        return None
    start = label.find(" (")
    while start != -1:
        title, query = label[:start], label[start + 2:-1]
        if _balanced(title) and _balanced(query):
            return title, query, connection
        start = label.find(" (", start + 1)
    return None


def fetch_log_name(connection: str, component_type: str) -> str:
    """
    Name of the result-folder file that keeps the output of one
    ``metrics.py`` run in the dashboard pod.

    :param connection: dbmsbenchmarker connection name.
    :param component_type: Monitoring component type, e.g. ``benchmarking``.
    :return: Filename (basename only).
    :rtype: str
    """
    return f"bexhoma-metrics-{connection}-{component_type}.log"


def parse_missing_metrics(text: str, source: str = "") -> list[MissingMetric]:
    """
    Extract every ``Metrics missing for ...`` message from a log text.

    Messages from dbmsbenchmarker versions that do not use the
    ``<title> (<query>)`` label keep the whole label as title.

    :param text: Log text.
    :param source: Name of the file the text came from.
    :return: One entry per distinct message, in order of first appearance.
    :rtype: list[MissingMetric]
    """
    found: dict[MissingMetric, None] = {}
    for line in text.splitlines():
        match = _MARKER.search(line.strip())
        if not match:
            continue
        label = match.group("label")
        component = _component_of(source)
        parts = _split_label(label)
        if parts:
            title, query, connection = parts
            entry = MissingMetric(source, title, connection, query, component)
        else:
            entry = MissingMetric(source, label, component=component)
        found.setdefault(entry, None)
    return list(found)


def _sparse_titles(result_dir: Path) -> set[str]:
    """Titles of the metrics the run's ``connections.config`` marks ``sparse``.

    :param result_dir: The experiment's result folder.
    :return: Metric titles, empty when the file is missing or unreadable.
    :rtype: set[str]
    """
    try:
        connections = ast.literal_eval((Path(result_dir) / "connections.config").read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return set()
    titles = set()
    for connection in connections if isinstance(connections, list) else []:
        for key, metrics in connection.get("monitoring", {}).items():
            if key.startswith("metrics") and isinstance(metrics, dict):
                titles.update(metric.get("title") for metric in metrics.values()
                              if isinstance(metric, dict) and metric.get("sparse"))
    return titles


def collect_missing_metrics(
    result_dir: Path, optional_components: Iterable[str] = (),
) -> list[MissingMetric]:
    """
    Scan a result folder's metric-fetch and benchmarker logs for metrics that
    were missing.

    A gap logged by both processes for the same metric, connection and
    component is kept once, as the dashboard pod's fetch-log entry. Each entry's ``expected`` names
    why the gap is harmless, when it is.

    :param result_dir: The experiment's result folder.
    :param optional_components: Component types whose gaps mean the data was
        pre-existing (the experiment's ``optional_monitoring_components``).
    :return: Every missing metric, grouped by source file in name order.
    :rtype: list[MissingMetric]
    """
    files = sorted({path for pattern in _LOG_PATTERNS for path in Path(result_dir).glob(pattern)})
    optional = set(optional_components)
    sparse = _sparse_titles(result_dir)
    missing: dict[tuple[str, str, str], MissingMetric] = {}
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for entry in parse_missing_metrics(text, path.name):
            if entry.component in optional:
                entry = replace(entry, expected=EXPECTED_DATA_PREEXISTING)
            elif entry.title in sparse:
                entry = replace(entry, expected=EXPECTED_SPARSE)
            missing.setdefault((entry.title, entry.connection, entry.query, entry.component), entry)
    # A DBMSBenchmarker pod names its connection with the client appended
    # ("pgduckdb-1-1-1-1-1" for the fetch log's "pgduckdb-1-1-1-1"), so its
    # copy of a gap the dashboard pod also logged is only found by prefix.
    fetched = {(title, connection, query, component)
               for (title, connection, query, component), entry in missing.items()
               if _FETCH_LOG.match(entry.source)}
    return [
        entry for entry in missing.values()
        if _FETCH_LOG.match(entry.source) or not any(
            (entry.title, entry.connection.rsplit("-", 1)[0], entry.query, entry.component) == key
            for key in fetched)
    ]
