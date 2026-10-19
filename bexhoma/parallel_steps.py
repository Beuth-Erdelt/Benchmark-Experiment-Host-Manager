"""Steps of one experiment loop pass that run side by side (fewer-kubectl-calls M6).

Submitting a benchmarker job (``BenchmarkRunner.run_pod()``) and ending one
(``end_benchmarking()``) take several seconds each, mostly waiting for the
cluster. With many tenants the steps of one pass ran one after another; here
they run in threads, one step per configuration.

What the steps share is protected:

- the result files every connection reads and rewrites (``connections.config``,
  ``protocol.json``, ``experiments.config``): one lock, see
  :meth:`ExperimentBase.result_files_lock`;
- their upload to the dashboard pod: :class:`OrderedUpload`, so a copy read
  before another step's write never lands after that step's copy.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Iterable, Optional

__all__ = ['DEFAULT_MAX_PARALLEL_STEPS', 'run_steps', 'OrderedUpload']

#: Default number of configurations whose job submissions (or job ends) of one
#: loop pass run at the same time; 1 runs them one by one, in order.
DEFAULT_MAX_PARALLEL_STEPS = 8


def run_steps(steps: list[Callable[[], Any]], max_workers: int = DEFAULT_MAX_PARALLEL_STEPS) -> list:
    """Run steps side by side and wait for all of them.

    With ``max_workers`` 1 or a single step they run in the calling thread,
    in order, as before. Otherwise every step runs to its end even if
    another one fails; the first exception (in list order) is raised after
    all steps are done.

    :param steps: Callables without arguments.
    :param max_workers: Maximum number of steps at the same time.
    :return: The results, in the order of ``steps``.
    """
    if max_workers <= 1 or len(steps) <= 1:
        return [step() for step in steps]
    with ThreadPoolExecutor(max_workers=min(max_workers, len(steps))) as pool:
        futures = [pool.submit(step) for step in steps]
    results = []
    for future in futures:
        results.append(future.result())
    return results


class OrderedUpload:
    """Uploads of shared result files from several threads, newest content last.

    A step writes its files (under the result files lock) and then calls
    :meth:`upload`, which returns once an upload *started after that write*
    has finished. Only one upload runs at a time; requests arriving meanwhile
    are merged into the next one. So the pod never gets an older version of a
    file after a newer one, and N steps arriving together need about two
    uploads instead of N.

    :param upload_files: Uploads a list of file names (raises on failure).
    """

    def __init__(self, upload_files: Callable[[list], Any]) -> None:
        self._upload_files = upload_files
        self._condition = threading.Condition()
        self._pending: list = []
        self._requested = 0        # number of the last request
        self._done = 0             # requests up to this number are uploaded (or failed)
        self._uploading = False
        self._errors: list[tuple[int, int, BaseException]] = []    # (first, last request, error)

    def upload(self, filenames: Iterable[str]) -> None:
        """Upload ``filenames`` (merged with the requests of other threads).

        :param filenames: Names relative to the experiment result folder.
        :raises Exception: The error of the upload that carried this request.
        """
        with self._condition:
            self._requested += 1
            ticket = self._requested
            self._pending.extend(filenames)
            while self._done < ticket:
                if self._uploading:
                    self._condition.wait()
                    continue
                self._uploading = True
                first, last = self._done + 1, self._requested
                batch = list(dict.fromkeys(self._pending))
                self._pending = []
                self._condition.release()
                error: Optional[BaseException] = None
                try:
                    self._upload_files(batch)
                except BaseException as exc:     # noqa: BLE001 - handed to every request of the batch
                    error = exc
                finally:
                    self._condition.acquire()
                    if error is not None:
                        self._errors.append((first, last, error))
                    self._done = last
                    self._uploading = False
                    self._condition.notify_all()
            for first, last, error in self._errors:
                if first <= ticket <= last:
                    raise error
