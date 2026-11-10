"""
Status of a test in the summary (``* TEST <status>: <label>``) and the report.

A test result is a ``(passed, label)`` pair. ``passed`` is ``True`` (passed),
``False`` (failed), ``None`` (skipped: the test does not apply, e.g. the data
was pre-existing) or :data:`WARNING` (the result needs judgement: it is not
shown to be wrong, but not shown to be right either, e.g. a metric that is
missing because the component did no disk I/O). A warning does not count as
a failure.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
__all__ = ["WARNING", "status_of", "count_statuses"]

#: ``passed`` value of a test whose result needs judgement.
WARNING = "warning"


def status_of(passed) -> str:
    """The status word of a test result: ``passed``, ``failed``, ``skipped`` or ``warning``.

    :param passed: ``True``, ``False``, ``None`` or :data:`WARNING`.
    :return: The word printed after ``TEST``.
    :rtype: str
    """
    if passed is None:
        return "skipped"
    if passed == WARNING:
        return "warning"
    return "passed" if passed is True else "failed"


def count_statuses(test_results: list) -> dict:
    """The number of tests per status.

    :param test_results: ``(passed, label)`` pairs.
    :return: ``{'passed': n, 'failed': n, 'skipped': n, 'warning': n}``.
    :rtype: dict
    """
    counts = {"passed": 0, "failed": 0, "skipped": 0, "warning": 0}
    for passed, _ in test_results:
        counts[status_of(passed)] += 1
    return counts
