"""
Failed loader pods and failed ingestion units, judged from a result folder.

Nothing here talks to the cluster or the DBMS: the checks read only what
bexhoma stored while the experiment ran, so they work on a downloaded result
folder too and never touch the loaded data.

Three sources:

* ``<app>-loading-<configuration>-<code>-<job>-<suffix>.describe.log`` -
  ``kubectl describe pod`` of every finished loader pod: the pod phase and
  each container's terminated state (reason, exit code).
* ``<app>-loading-<configuration>-<code>-<job>.describe.job.log`` -
  ``kubectl describe job``: ``Pods Statuses: ... / <n> Failed`` counts failed
  pods even when the pod object itself is gone.
* ``<app>-loading-<configuration>-<code>-<job>-<suffix>.<container>.log`` -
  the container logs, with one line per ingested unit (table, file chunk,
  warehouse set) written by the loader images::

      BEXHOMA_INGEST:<unit>:<expected>:<reported>:<ok|failed>

  ``expected`` and ``reported`` are empty when the loader cannot know them.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

__all__ = ['IngestUnit', 'LoaderCheck', 'check_loader_pods', 'parse_ingest_markers',
           'parse_pod_description', 'parse_job_failed_pods']

#: One ingested unit, as printed by a loader container.
_INGEST_MARKER = re.compile(r'^BEXHOMA_INGEST:([^:\r\n]*):([^:\r\n]*):([^:\r\n]*):(ok|failed)\s*$', re.M)
_JOB_FAILED = re.compile(r'^Pods Statuses:.*/\s*(\d+)\s+Failed', re.M)
_POD_STATUS = re.compile(r'^Status:\s+(\S+)', re.M)


@dataclass
class IngestUnit:
    """One ``BEXHOMA_INGEST`` line of a loader container log."""

    pod: str
    container: str
    unit: str
    expected: str
    reported: str
    ok: bool


@dataclass
class LoaderCheck:
    """Loader pods and ingestion units of one configuration.

    :ivar pods: Names of the loader pods with a stored description.
    :ivar failures: Human-readable failures (failed pods, failed jobs, failed units).
    :ivar units: Every ``BEXHOMA_INGEST`` line found in the container logs.
    """

    pods: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    units: list[IngestUnit] = field(default_factory=list)


def parse_ingest_markers(text: str, pod: str = '', container: str = '') -> list[IngestUnit]:
    """Return the ``BEXHOMA_INGEST`` lines of a container log.

    :param text: Content of the log.
    :param pod: Pod name, kept on each unit.
    :param container: Container name, kept on each unit.
    :return: One :class:`IngestUnit` per marker line, in log order.
    :rtype: list[IngestUnit]
    """
    return [IngestUnit(pod, container, unit, expected, reported, status == 'ok')
            for unit, expected, reported, status in _INGEST_MARKER.findall(text or '')]


def parse_pod_description(text: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Return the phase of a pod and its containers that ended with an error.

    Reads a ``kubectl describe pod`` output: the top-level ``Status:`` and, for
    every container (init containers included), the ``State: Terminated``
    block with its ``Reason`` and ``Exit Code``. ``Last State`` blocks are
    ignored (loader pods never restart: ``restartPolicy: Never``).

    :param text: Content of the description.
    :return: ``(phase, [(container, reason, exit_code), ...])`` with only the
        containers whose exit code is not 0.
    :rtype: tuple[str, list[tuple[str, str, str]]]
    """
    match = _POD_STATUS.search(text or '')
    phase = match.group(1) if match else ''
    failed = []
    container, in_state, reason = '', False, ''
    for line in (text or '').splitlines():
        header = re.match(r'^  (\S[^:]*):\s*$', line)
        if header:
            container, in_state, reason = header.group(1), False, ''
            continue
        stripped = line.strip()
        if re.match(r'^State:\s+Terminated', stripped) and line.startswith('    State:'):
            in_state, reason = True, ''
        elif re.match(r'^(State|Last State|Ready):', stripped):
            in_state = False
        elif in_state and stripped.startswith('Reason:'):
            reason = stripped.split(':', 1)[1].strip()
        elif in_state and stripped.startswith('Exit Code:'):
            code = stripped.split(':', 1)[1].strip()
            if code != '0':
                failed.append((container, reason, code))
            in_state = False
    return phase, failed


def parse_job_failed_pods(text: str) -> int:
    """Return the number of failed pods of a ``kubectl describe job`` output (0 if not given).

    :param text: Content of the description.
    :rtype: int
    """
    match = _JOB_FAILED.search(text or '')
    return int(match.group(1)) if match else 0


def check_loader_pods(folder: str, appname: str, code: str, configurations: list) -> dict[str, LoaderCheck]:
    """Collect failed loader pods, failed loading jobs and failed ingestion units per configuration.

    :param folder: Result folder of the experiment.
    :param appname: App label (file name prefix, e.g. ``bexhoma``).
    :param code: Experiment code.
    :param configurations: Configuration names of the experiment.
    :return: One :class:`LoaderCheck` per configuration that has stored loader
        pods or jobs; configurations without any are left out.
    :rtype: dict[str, LoaderCheck]
    """
    if not folder or not os.path.isdir(folder):
        return {}
    original = {str(c).lower(): c for c in configurations}
    # longest name first: 'postgresql-1-0' before 'postgresql-1'
    names = sorted(original, key=len, reverse=True)
    prefix = '{}-loading-'.format(appname.lower())
    infix = '-{}-'.format(str(code).lower())
    checks: dict[str, LoaderCheck] = {}
    jobs_failed: dict[str, tuple[str, int]] = {}
    pods_failed_per_job: dict[str, int] = {}
    for filename in sorted(os.listdir(folder)):
        if not filename.startswith(prefix) or not filename.endswith('.log'):
            continue
        rest = filename[len(prefix):]
        configuration = next((n for n in names if rest.startswith(n + infix)), None)
        if configuration is None:
            continue
        check = checks.setdefault(original[configuration], LoaderCheck())
        path = os.path.join(folder, filename)
        with open(path, encoding='utf-8', errors='replace') as file:
            text = file.read()
        if filename.endswith('.describe.job.log'):
            job = filename[:-len('.describe.job.log')]
            failed = parse_job_failed_pods(text)
            if failed:
                jobs_failed[job] = (original[configuration], failed)
        elif filename.endswith('.describe.log'):
            pod = filename[:-len('.describe.log')]
            check.pods.append(pod)
            phase, containers = parse_pod_description(text)
            if phase == 'Failed' or containers:
                job = pod.rsplit('-', 1)[0]
                pods_failed_per_job[job] = pods_failed_per_job.get(job, 0) + 1
                details = ', '.join('{} exit {}{}'.format(c, e, ' ({})'.format(r) if r else '')
                                    for c, r, e in containers)
                check.failures.append('pod {} {}{}'.format(
                    pod, phase or 'failed', ': ' + details if details else ''))
        else:
            pod, _, container = filename[:-len('.log')].rpartition('.')
            for unit in parse_ingest_markers(text, pod=pod, container=container):
                check.units.append(unit)
                if not unit.ok:
                    check.failures.append('pod {} unit {} failed (expected {}, reported {})'.format(
                        pod, unit.unit, unit.expected or '?', unit.reported or '?'))
    # failed pods whose description is gone (e.g. replaced by a retry of the job)
    for job, (configuration, failed) in sorted(jobs_failed.items()):
        missing = failed - pods_failed_per_job.get(job, 0)
        if missing > 0:
            checks[configuration].failures.append('job {}: {} failed pod{} without stored description'.format(
                job, missing, '' if missing == 1 else 's'))
    return checks
