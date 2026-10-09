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

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

__all__ = ["MissingMetric", "parse_missing_metrics", "collect_missing_metrics", "fetch_log_name"]

#: Log files that can carry the message, relative to the result folder.
_LOG_PATTERNS = ("bexhoma-metrics-*.log", "bexhoma-benchmarker-*.log")

_MARKER = re.compile(r"Metrics missing for (?P<label>.+?)(?:: \S*)?$")
_LABEL = re.compile(r"^(?P<title>.*?) \((?P<query>.*)\)(?: for connection (?P<connection>\S+))?$")


@dataclass(frozen=True)
class MissingMetric:
    """One metric query that returned no data, as logged by DBMSBenchmarker."""

    source: str
    title: str
    connection: str = ""
    query: str = ""


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
        parts = _LABEL.match(label)
        if parts:
            entry = MissingMetric(source, parts.group("title"), parts.group("connection") or "", parts.group("query"))
        else:
            entry = MissingMetric(source, label)
        found.setdefault(entry, None)
    return list(found)


def collect_missing_metrics(result_dir: Path) -> list[MissingMetric]:
    """
    Scan a result folder's metric-fetch and benchmarker logs for metrics that
    were missing.

    :param result_dir: The experiment's result folder.
    :return: Every missing metric, grouped by source file in name order.
    :rtype: list[MissingMetric]
    """
    files = sorted({path for pattern in _LOG_PATTERNS for path in Path(result_dir).glob(pattern)})
    missing: list[MissingMetric] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        missing.extend(parse_missing_metrics(text, path.name))
    return missing
