"""
Reduction of monitoring time series to one value per connection.

A ``counter`` metric (e.g. ``total_cpu_util_s``, the summed
``container_cpu_usage_seconds_total`` of a component's pods) is fetched as one
summed series per connection. Its total over a phase is not ``max - min``:
the sum can drop, and then ``max - min`` measures the wrong thing.

* A pod of the previous repetition or round stays in the sum for about five
  minutes after it stopped, flat at its final value, and then vanishes. With
  ``max - min``, a phase starting in that time reports that pod's lifetime
  total (e.g. 4205 CPU-s for a 52 s load that used 147).
* A container restart sets its counter back to 0.
* DBMSBenchmarker pads a series that Prometheus returned short with zeros.

:func:`counter_increase` counts only the growth, like PromQL ``increase()``.
That needs the series' first value to be the counter at the start of the
phase, which holds for the SUT (its pod lives across the phase) but not for
job pods (loader, data generator, benchmarker): they start inside the phase,
and DBMSBenchmarker re-indexes a series to start at its first sample and pads
missing samples at the end, so a job whose first scrape already shows most of
its CPU would count almost nothing. :func:`counter_total` therefore keeps
``max - min`` for those, which is still wrong while a job of the previous
round lingers in the sum (see ``dev/plan-metrics-pod-scope.md``).

A cluster template with ``pod=~"{pods}"`` gives every connection its own job
query sets (:data:`JOB_QUERY_SETS`), which select only that job's pods. Such
a series starts at 0 before the job's first scrape, so its first value is
growth too: :func:`counter_total` counts first value + growth for the
connections :func:`scoped_job_connections` finds. Results fetched with an old
template (job query sets equal to ``metrics``) keep ``max - min``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

__all__ = [
    "JOB_COMPONENTS", "JOB_QUERY_SETS", "DEFAULT_SCRAPE_INTERVAL_SECONDS", "SCRAPE_JITTER",
    "counter_increase", "counter_total", "min_measurable_window",
    "read_connections", "scoped_job_connections",
]

#: Monitoring components whose pods are jobs started inside the phase.
JOB_COMPONENTS = frozenset({'loader', 'datagenerator', 'benchmarker'})

#: Query set of a connection's ``monitoring`` that selects a job component's
#: own pods (filled from ``{pods}``, see ``configurations/metrics.py``).
JOB_QUERY_SETS = {
    'benchmarker': 'metrics_benchmarker',
    'loader': 'metrics_loading',
    'datagenerator': 'metrics_loading',
}

#: Scrape interval of the cluster Prometheus when ``cluster.config`` names none
#: (``monitor.scrape_interval``).
DEFAULT_SCRAPE_INTERVAL_SECONDS = 30

#: Factor on the scrape interval for "at least one scrape inside the window",
#: since scrapes come with some jitter (28-32 s on the cluster at 30 s).
SCRAPE_JITTER = 1.2


def min_measurable_window(component: str, scrape_interval: float, jobs_scoped: bool = False) -> float:
    """Shortest phase window, in seconds, whose CPU total can be measured.

    The fetch repeats the latest scrape in every 1 s row, so the first row of a
    pod that already runs (SUT, workers) is the scrape before the window: one
    scrape inside the window is enough. A job pod starts inside the window and
    has no scrape before it, so ``max - min`` needs two scrapes inside; once its
    query covers only its own pods and its first value counts as growth
    (``jobs_scoped``), one is enough. See ``dev/plan-metrics-pod-scope.md`` (M1b).

    :param component: The monitoring component, e.g. ``loading`` or ``benchmarker``.
    :param scrape_interval: Seconds between two scrapes of the Prometheus the metrics come from.
    :param jobs_scoped: Whether job counters count their first value (their
        query covers only their own pods).
    :return: ``2 x scrape_interval`` for a job counted by ``max - min``, else
        ``SCRAPE_JITTER x scrape_interval``.
    :rtype: float
    """
    if component in JOB_COMPONENTS and not jobs_scoped:  # scoped: see scoped_job_connections()
        return 2 * scrape_interval
    return SCRAPE_JITTER * scrape_interval


def counter_increase(df: pd.DataFrame) -> pd.Series:
    """Return the growth of each counter column: the sum of its positive steps.

    A drop (a vanishing series, a counter reset, zero padding) is not
    counted; growth before and after it is. Gaps (NaN) are bridged, so growth
    across a gap is counted when the series resumes. In the one step where a
    series vanishes, the growth of the others in that step is lost, at most
    one scrape interval.

    :param df: One column per connection, one row per sample, in time order.
    :return: One value per column, sorted by column; NaN for a column without
        any value, 0 for a column with a single value (as ``max - min``).
    :rtype: pandas.Series
    """
    steps = df.ffill().diff().clip(lower=0)
    increase = steps.sum(min_count=1)
    has_values = df.notna().any()
    increase[has_values & increase.isna()] = 0.0
    return increase.sort_index()


def counter_total(df: pd.DataFrame, component: str, scoped: Iterable[str] = ()) -> pd.Series:
    """Return each counter column's total for one monitoring component's phase.

    For a scoped job column the first value counts as growth from 0, then
    :func:`counter_increase` adds the positive steps. A drop (a finished pod
    of the job leaving the sum, zero padding) is not counted; a later rise
    counts only its step, so a pod reappearing after missed scrapes is not
    counted twice.

    :param df: One column per connection, one row per sample, in time order.
    :param component: The monitoring component (``workload['monitoring_components']``
        key), e.g. ``loading``, ``benchmarking``, ``loader``, ``benchmarker``.
    :param scoped: Columns whose series cover only the job's own pods
        (:func:`scoped_job_connections`); only used for :data:`JOB_COMPONENTS`.
    :return: :func:`counter_increase` for the SUT side; for
        :data:`JOB_COMPONENTS` first value + growth in scoped columns,
        ``max - min`` in the others; one value per column, sorted by column.
    :rtype: pandas.Series
    """
    if component not in JOB_COMPONENTS:
        return counter_increase(df)
    total = df.max().sort_index() - df.min().sort_index()
    scoped = set(scoped)
    columns = [column for column in df.columns if column in scoped]
    if columns and len(df) > 0:
        first = df[columns].bfill().iloc[0]
        total.loc[columns] = (first + counter_increase(df[columns])).loc[columns].values
    return total


def read_connections(result_dir) -> list:
    """Read a result folder's ``connections.config``.

    :param result_dir: The experiment's result folder.
    :return: The connection dicts; empty when the file is missing or unreadable.
    :rtype: list
    """
    try:
        connections = ast.literal_eval(Path(result_dir, 'connections.config').read_text(encoding='utf-8'))
    except (OSError, SyntaxError, ValueError, TypeError):
        return []
    return connections if isinstance(connections, list) else []


def scoped_job_connections(connections: list, component: str, metric: Optional[str] = None) -> set:
    """Connections whose job query set of ``component`` selects only the job's own pods.

    That is the case when the connection's query in :data:`JOB_QUERY_SETS`
    differs from the one in ``metrics``: the cluster template had ``{pods}``.
    A silent check on the stored queries, so re-evaluating old results keeps
    their rule.

    :param connections: Connection dicts (:func:`read_connections`).
    :param component: The monitoring component; only :data:`JOB_COMPONENTS` can be scoped.
    :param metric: Metric key to compare; None means any metric of the set.
    :return: Names of the scoped connections.
    :rtype: set
    """
    query_set = JOB_QUERY_SETS.get(component)
    if query_set is None:
        return set()
    scoped = set()
    for connection in connections:
        monitoring = connection.get('monitoring') or {}
        job_metrics = monitoring.get(query_set) or {}
        default_metrics = monitoring.get('metrics') or {}
        keys = job_metrics if metric is None else [metric]
        if any(key in job_metrics
               and job_metrics[key].get('query') != (default_metrics.get(key) or {}).get('query')
               for key in keys):
            scoped.add(connection.get('name'))
    return scoped
