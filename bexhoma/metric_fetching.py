"""Batched, parallel fetching of Prometheus metrics into experiment results.

Every fetch is one ``metrics.py`` run in the dashboard pod (``kubectl exec``),
so fetches of different connections and components are independent and can
run side by side. Each task is built from its own configuration, so tenants
with different DBMS, components or metric sets need nothing special.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable

from .cluster_calls import CALL_STATS

__all__ = ['DEFAULT_MAX_PARALLEL_FETCHES', 'MetricFetchBatch', 'fetch_failed']

#: Default number of ``metrics.py`` runs at the same time. Each queries
#: Prometheus metric by metric, so a few in parallel are cheap for Prometheus
#: and the dashboard pod (limits 16 CPU, 128 Gi; one run is one Python
#: process with pandas). A run is mostly waiting (about 4.7 s of exec overhead
#: against 0.4 s of Prometheus work), so 8 at once halve a pass's fetch time.
DEFAULT_MAX_PARALLEL_FETCHES = 8


def fetch_failed(output: str) -> bool:
    """Whether a ``metrics.py`` run ended in an exception.

    dbmsbenchmarker before atomic config writes rewrites ``queries.config`` and
    ``connections.config`` of the result folder in place, so a run reading them
    while another one writes can fail. Such a run is repeated on its own.

    :param output: Combined stdout and stderr of the run.
    :return: True if the output contains a Python traceback.
    """
    return 'Traceback (most recent call last)' in (output or '')


class MetricFetchBatch:
    """Fetch tasks collected during one pass of the experiment loop, run together.

    Fetches run in parallel; actions added with :meth:`add_after` run once all
    fetches are done (e.g. copying metrics another fetch of this batch wrote).
    ``connections.config`` is uploaded once at the end, because every
    ``metrics.py`` run may overwrite it in the pod.
    """

    def __init__(self) -> None:
        self.fetches: list[tuple[Any, dict]] = []
        self.after: list[Callable[[], None]] = []
        # filled by job submissions / job ends running side by side (parallel_steps)
        self._lock = threading.Lock()

    def __len__(self) -> int:
        return len(self.fetches) + len(self.after)

    def add_fetch(self, config: Any, **kwargs: Any) -> None:
        """Queue ``config.metrics.fetch(**kwargs)``; the component is registered now, in this thread.

        :param config: Configuration whose collector fetches.
        :param kwargs: Arguments of :meth:`MetricsCollector.fetch`.
        """
        config.metrics.register(kwargs['component_type'], kwargs['title'], kwargs.get('optional', False))
        with self._lock:
            self.fetches.append((config, kwargs))

    def add_after(self, action: Callable[[], None]) -> None:
        """Queue an action to run after all fetches of this batch.

        :param action: Callable without arguments.
        """
        with self._lock:
            self.after.append(action)

    def run(self, max_workers: int = DEFAULT_MAX_PARALLEL_FETCHES) -> None:
        """Run all queued fetches (up to ``max_workers`` at once), then the queued actions.

        :param max_workers: Maximum number of fetches at the same time; 1 runs them one by one.
        """
        if not len(self):
            return
        started = time.monotonic()
        calls_started = CALL_STATS.snapshot()
        failed = []
        if self.fetches:
            workers = max(1, min(max_workers, len(self.fetches)))
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = {
                    pool.submit(config.metrics.fetch, register=False, upload=False, **kwargs): (config, kwargs)
                    for config, kwargs in self.fetches}
                for future in as_completed(futures):
                    try:
                        output = future.result()
                    except Exception as exc:   # noqa: BLE001 - reported and repeated below
                        output = f"Traceback (most recent call last)\n{exc!r}"
                    if fetch_failed(output):
                        failed.append(futures[future])
            # repeated one by one: a run fails when it read a config file another run was writing
            for config, kwargs in failed:
                print("{:30s}: repeating failed metrics fetch {}".format(kwargs['connection'], kwargs['component_type']))
                config.metrics.fetch(register=False, upload=False, **kwargs)
        for action in self.after:
            action()
        if self.fetches:
            self.fetches[0][0].upload_experiment_file('connections.config')
        if self.fetches:
            print("{:30s}: fetched {} metric sets in {:.0f}s ({} at once, {} repeated, {} follow-up actions; {})".format(
                "Experiment", len(self.fetches), time.monotonic() - started,
                max(1, min(max_workers, len(self.fetches))), len(failed), len(self.after),
                CALL_STATS.since(calls_started)))
        else:
            print("{:30s}: ran {} follow-up actions (e.g. reused loading metrics) in {:.0f}s".format(
                "Experiment", len(self.after), time.monotonic() - started))
        self.fetches = []
        self.after = []
