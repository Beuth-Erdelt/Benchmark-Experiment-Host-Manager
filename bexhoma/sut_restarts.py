"""
SUT container restart analysis for a finished experiment's result folder.

Two sources are combined:

* ``bexhoma-sut-{configuration}-{code}-{experiment_run}-restarts.json`` — per-pod
  restart counts, one snapshot per experiment_run. The SUT pod is restarted
  in place rather than recreated across repeat runs, so its ``restartCount``
  is cumulative across snapshots; aggregate by max per pod, never by sum.
* ``bexhoma-sut-*.describe.log`` — ``kubectl describe pod`` captures, which
  carry each container's ``Last State`` (termination reason, exit code,
  finish time) and the volumes it mounts.

The second source answers what the counts alone cannot: *why* a container
restarted (e.g. ``OOMKilled``), and whether its on-disk state survived. A
container whose data directory is not on a mounted volume keeps it in its
own writable layer, which a restart discards — the DBMS then re-initializes
an empty database and every later query fails for that reason alone.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

#: Mount paths that never hold a DBMS's own on-disk state: shared memory,
#: and the raw-data staging volume the loaders read from.
_NON_STATE_MOUNT_PATHS = ("/dev/shm", "/data")

#: Volume types that project configuration into a container, never state.
_NON_STATE_VOLUME_TYPES = ("ConfigMap", "Secret", "Projected", "DownwardAPI")

#: Environment variables that name a DBMS's data directory, when present.
_DATA_DIR_ENV_VARS = ("PGDATA",)

_CONTAINER_SECTIONS = ("Containers:", "Init Containers:")
_TOP_LEVEL_KEY = re.compile(r"^(\S[^:]*):\s*(.*)$")
_INDENTED_NAME = re.compile(r"^  (\S[^:]*):\s*$")
_FIELD = re.compile(r"^\s+([A-Za-z][\w .-]*?):\s*(.*)$")
_MOUNT = re.compile(r"^\s+(/\S*) from (\S+) \(")
_COUNTS_LINE = re.compile(r"^\d+(\s+\d+)*$")


def clean_restart_counts(output: str | None) -> str:
    """
    Extract the per-container restart counts from raw kubectl output.

    ``cluster.kubectl()`` merges stderr into stdout, so client-side warnings
    (klog lines such as ``E0928 10:11:12.123 1234 memcache.go:265] ...``)
    can surround the jsonpath result. Only a line made up entirely of
    integers is the result; the last such line wins.

    :param output: Raw kubectl output, possibly ``None`` on failure.
    :return: Space-separated restart counts, or ``""`` if none were found.
    :rtype: str
    """
    counts = ""
    for line in (output or "").splitlines():
        line = line.strip().strip('"')
        if _COUNTS_LINE.match(line):
            counts = line
    return counts


@dataclass
class ContainerState:
    """Restart-relevant state of one container, parsed from a describe log."""

    name: str
    restart_count: int = 0
    last_state: str = ""
    reason: str = ""
    exit_code: str = ""
    finished: str = ""
    env: dict[str, str] = field(default_factory=dict)
    mounts: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class PodDescription:
    """The parts of one ``kubectl describe pod`` capture this module needs."""

    name: str
    containers: dict[str, ContainerState] = field(default_factory=dict)
    volume_types: dict[str, str] = field(default_factory=dict)


@dataclass
class RestartDetail:
    """
    One restarted SUT container, or one restarted pod whose describe log
    could not explain the restart.

    ``data_volume`` is ``True`` when the container's data directory sits on a
    mounted volume (so it survived the restart), ``False`` when it does not
    (the restart discarded it), and ``None`` when no describe log was found.
    """

    pod: str
    restarts: int
    container: str = ""
    reason: str = "unknown"
    exit_code: str = ""
    finished: str = ""
    data_volume: bool | None = None
    describe_file: str = ""
    previous_log: str = ""


def _previous_log_name(result_dir: Path, describe_file: str, container: str) -> str:
    """
    Return the stored ``--previous`` log of a container, if one was captured.

    It shares the describe log's per-run pod label, so it is found by name:
    ``<label>.describe.log`` pairs with ``<label>.<container>.previous.log``.

    :param result_dir: The experiment's result folder.
    :param describe_file: Filename of the describe log the detail came from.
    :param container: The restarted container.
    :return: The previous log's filename, or ``""`` if none was stored.
    :rtype: str
    """
    name = describe_file.removesuffix(".describe.log") + f".{container}.previous.log"
    return name if (result_dir / name).is_file() else ""


def read_restart_counts(result_dir: Path) -> tuple[dict[str, int], dict[str, str]]:
    """
    Aggregate every ``bexhoma-sut-*-restarts.json`` snapshot by max per pod.

    :param result_dir: The experiment's result folder.
    :return: Tuple of (pod name to total restart count, pod name to the raw
             per-container restart-count string of the snapshot chosen).
    :rtype: tuple[dict[str, int], dict[str, str]]
    """
    per_pod_total: dict[str, int] = {}
    per_pod_raw: dict[str, str] = {}
    for restarts_file in sorted(result_dir.glob("bexhoma-sut-*-restarts.json")):
        with open(restarts_file) as handle:
            pod_restarts: dict[str, str] = json.load(handle)
        for pod, counts in pod_restarts.items():
            # Snapshots written before clean_restart_counts() existed may
            # still carry kubectl warning lines.
            counts = clean_restart_counts(counts)
            pod_total = sum(int(x) for x in counts.split())
            if pod not in per_pod_total or pod_total > per_pod_total[pod]:
                per_pod_total[pod] = pod_total
                per_pod_raw[pod] = counts
    return per_pod_total, per_pod_raw


def parse_describe_log(text: str) -> PodDescription:
    """
    Parse the pod name, per-container restart state and volume types out of
    ``kubectl describe pod`` output.

    :param text: Full describe-log text.
    :return: The parsed pod description; missing sections stay empty.
    :rtype: PodDescription
    """
    pod = PodDescription(name="")
    section = ""
    container: ContainerState | None = None
    subsection = ""
    volume = ""
    for line in text.splitlines():
        top_level = _TOP_LEVEL_KEY.match(line)
        if top_level:
            section = line.strip() if line.strip() in _CONTAINER_SECTIONS else top_level.group(1)
            if section == "Name" and not pod.name:
                pod.name = top_level.group(2).strip()
            container, subsection, volume = None, "", ""
            continue
        indented_name = _INDENTED_NAME.match(line)
        if section in _CONTAINER_SECTIONS:
            if indented_name:
                container = ContainerState(name=indented_name.group(1))
                pod.containers[container.name] = container
                subsection = ""
                continue
            if container is None:
                continue
            indent = len(line) - len(line.lstrip())
            mount = _MOUNT.match(line)
            if subsection == "Mounts" and mount:
                container.mounts.append((mount.group(1), mount.group(2)))
                continue
            field_match = _FIELD.match(line)
            if not field_match:
                continue
            key, value = field_match.group(1), field_match.group(2).strip()
            if indent == 4:
                subsection = key
                if key == "Restart Count":
                    container.restart_count = int(value) if value.isdigit() else 0
                elif key == "Last State":
                    container.last_state = value
                elif key == "Mounts" and value == "<none>":
                    subsection = ""
            elif indent == 6 and subsection == "Last State":
                if key == "Reason":
                    container.reason = value
                elif key == "Exit Code":
                    container.exit_code = value
                elif key == "Finished":
                    container.finished = value
            elif indent == 6 and subsection == "Environment":
                container.env[key] = value
        elif section == "Volumes":
            if indented_name:
                volume = indented_name.group(1)
                continue
            field_match = _FIELD.match(line)
            if volume and field_match and field_match.group(1) == "Type":
                pod.volume_types[volume] = field_match.group(2).split()[0] if field_match.group(2) else ""
    return pod


def has_data_volume(container: ContainerState, volume_types: dict[str, str]) -> bool:
    """
    Decide whether a container's on-disk state sits on a mounted volume.

    When the container names its data directory (``PGDATA``), a mount at or
    above that path is required. Otherwise any mount that is neither shared
    memory, the raw-data staging volume, nor a config/secret projection
    counts.

    :param container: Parsed container state.
    :param volume_types: Volume name to its Kubernetes volume type.
    :return: Whether a restart of this container keeps its on-disk state.
    :rtype: bool
    """
    state_mounts = [
        path for path, volume in container.mounts
        if path not in _NON_STATE_MOUNT_PATHS
        and volume_types.get(volume, "") not in _NON_STATE_VOLUME_TYPES
    ]
    data_dirs = [container.env[name] for name in _DATA_DIR_ENV_VARS if container.env.get(name)]
    if data_dirs:
        return any(
            data_dir == path or data_dir.startswith(path.rstrip("/") + "/")
            for data_dir in data_dirs for path in state_mounts
        )
    return bool(state_mounts)


def collect_restart_details(result_dir: Path) -> list[RestartDetail]:
    """
    Explain every SUT restart counted in ``bexhoma-sut-*-restarts.json``.

    For each pod with a non-zero count, the describe log of that pod with the
    highest restart count (the latest capture) supplies one detail per
    restarted container. A pod with no matching describe log yields a single
    detail with ``reason="unknown"`` and ``data_volume=None``.

    :param result_dir: The experiment's result folder.
    :return: Restart details, ordered by pod name then container name.
    :rtype: list[RestartDetail]
    """
    per_pod_total, _ = read_restart_counts(result_dir)
    restarted = {pod: total for pod, total in per_pod_total.items() if total > 0}
    if not restarted:
        return []
    descriptions: dict[str, tuple[PodDescription, str]] = {}
    for describe_file in sorted(result_dir.glob("bexhoma-sut-*.describe.log")):
        description = parse_describe_log(describe_file.read_text(encoding="utf-8", errors="replace"))
        if description.name not in restarted:
            continue
        restarts = sum(c.restart_count for c in description.containers.values())
        previous = descriptions.get(description.name)
        if previous is None or restarts >= sum(c.restart_count for c in previous[0].containers.values()):
            descriptions[description.name] = (description, describe_file.name)
    details: list[RestartDetail] = []
    for pod in sorted(restarted):
        if pod not in descriptions:
            details.append(RestartDetail(pod=pod, restarts=restarted[pod]))
            continue
        description, describe_file = descriptions[pod]
        containers = [c for c in description.containers.values() if c.restart_count > 0]
        if not containers:
            details.append(RestartDetail(pod=pod, restarts=restarted[pod], describe_file=describe_file))
            continue
        for container in sorted(containers, key=lambda c: c.name):
            details.append(RestartDetail(
                pod=pod,
                restarts=container.restart_count,
                container=container.name,
                reason=container.reason or "unknown",
                exit_code=container.exit_code,
                finished=container.finished,
                data_volume=has_data_volume(container, description.volume_types),
                describe_file=describe_file,
                previous_log=_previous_log_name(result_dir, describe_file, container.name),
            ))
    return details


def summarize_reasons(details: list[RestartDetail]) -> dict[str, int]:
    """
    Count restarts per termination reason.

    :param details: Output of :func:`collect_restart_details`.
    :return: Reason to number of restarts, most frequent first.
    :rtype: dict[str, int]
    """
    counts: dict[str, int] = {}
    for detail in details:
        counts[detail.reason] = counts.get(detail.reason, 0) + detail.restarts
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def format_detail(detail: RestartDetail) -> str:
    """
    Render one restart detail as a single human-readable line.

    :param detail: One restart detail.
    :return: e.g. ``"dbms: OOMKilled (exit 137) at <time>; no data volume -- data lost"``.
    :rtype: str
    """
    what = detail.container or "container unknown"
    text = f"{what}: {detail.reason}"
    if detail.exit_code:
        text += f" (exit {detail.exit_code})"
    if detail.finished:
        text += f" at {detail.finished}"
    if detail.data_volume is True:
        text += "; data on a mounted volume"
    elif detail.data_volume is False:
        text += "; no data volume, on-disk state was lost"
    else:
        text += "; no describe log, data volume unknown"
    return text
