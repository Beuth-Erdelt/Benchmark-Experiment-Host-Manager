"""
Ceph storage facts shared by monitoring, ``environment.yml`` and spec validation.

Monitoring queries in ``cluster.config`` may use three storage placeholders,
filled per SUT configuration once its volumes exist:

* ``{storage_class}`` -- the StorageClass the configuration's PVC uses;
* ``{pool}`` -- the Ceph pool behind it (``parameters.pool`` of a Ceph CSI
  StorageClass);
* ``{rbd_images}`` -- the RBD images behind the configuration's PVCs, as a
  PromQL regex alternation (``csi-vol-a|csi-vol-b``).

A placeholder that cannot be filled (ephemeral or ``ramdisk`` storage, a
non-Ceph class, CephFS for ``{rbd_images}``, a cluster without Ceph metrics)
stays empty, and every metric whose query uses it is switched off for that
configuration instead of being fetched with an empty label value.

Everything here is a pure function, so it can be tested without a cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import re
import string
from typing import Any, Optional

__all__ = [
    "STORAGE_PLACEHOLDERS", "NEEDS_CEPH_POOL", "NEEDS_CEPH_VOLUME",
    "ceph_pool_of", "query_placeholders", "unresolved_placeholders", "metric_needs",
    "is_valid_image_name", "rbd_images_pattern", "promql_pool_check", "promql_volume_check",
    "storage_monitoring_record",
]

#: Placeholders filled from a configuration's storage, in addition to the
#: ``host``/``gpuid``/``configuration``/``experiment``/``schema``/``database``
#: keys every metric query may use.
STORAGE_PLACEHOLDERS = ("storage_class", "pool", "rbd_images")

#: ``needs`` of a metric whose query uses ``{pool}`` but not ``{rbd_images}``.
NEEDS_CEPH_POOL = "ceph_pool"
#: ``needs`` of a metric whose query uses ``{rbd_images}``.
NEEDS_CEPH_VOLUME = "ceph_volume"

#: Ceph CSI provisioner suffixes and the kind of volume they create. Rook
#: names the driver ``<operator namespace>.rbd.csi.ceph.com``, so only the
#: suffix is fixed. Legacy FlexVolume classes (``ceph.rook.io/block``) are
#: deliberately not listed.
_CEPH_CSI_KINDS = (
    (".rbd.csi.ceph.com", "rbd"),
    (".cephfs.csi.ceph.com", "cephfs"),
)

#: RBD image names as Ceph CSI creates them (``csi-vol-<uuid>``). Anything
#: else is refused, so a name can go into a PromQL regex unescaped.
_IMAGE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")


def ceph_pool_of(provisioner: str, parameters: Optional[dict[str, Any]]) -> tuple[str, str]:
    """Return the Ceph pool and volume kind of a StorageClass.

    :param provisioner: The StorageClass's ``provisioner``.
    :param parameters: The StorageClass's ``parameters``.
    :return: ``(pool, kind)`` with kind ``"rbd"`` or ``"cephfs"``; ``("", "")``
        for any other provisioner or when no pool is set.
    :rtype: tuple[str, str]
    """
    for suffix, kind in _CEPH_CSI_KINDS:
        if (provisioner or "").endswith(suffix):
            pool = str((parameters or {}).get("pool") or "")
            return (pool, kind) if pool else ("", "")
    return "", ""


def query_placeholders(query: str) -> set[str]:
    """Return the placeholder names a ``str.format`` query template uses.

    Doubled braces (``{{...}}``, PromQL label blocks) are literals and not
    placeholders.

    :param query: A metric's ``query`` template.
    :return: Placeholder names, e.g. ``{"host", "pool"}``.
    :rtype: set[str]
    """
    try:
        return {field_name for _, field_name, _, _ in string.Formatter().parse(query)
                if field_name}
    except ValueError:
        return set()


def unresolved_placeholders(query: str, values: dict[str, str]) -> list[str]:
    """Return the storage placeholders a query uses but ``values`` leaves empty.

    :param query: A metric's ``query`` template.
    :param values: Filled storage placeholders (``storage_class``, ``pool``,
        ``rbd_images``).
    :return: Names of the unresolved storage placeholders, sorted.
    :rtype: list[str]
    """
    used = query_placeholders(query)
    return sorted(name for name in STORAGE_PLACEHOLDERS if name in used and not values.get(name))


def metric_needs(query: str) -> Optional[str]:
    """Return what kind of storage a metric query needs to be collected.

    :param query: A metric's ``query`` template.
    :return: :data:`NEEDS_CEPH_VOLUME` when it uses ``{rbd_images}``,
        :data:`NEEDS_CEPH_POOL` when it uses ``{pool}`` only, else ``None``.
    :rtype: Optional[str]
    """
    used = query_placeholders(query)
    if "rbd_images" in used:
        return NEEDS_CEPH_VOLUME
    if "pool" in used:
        return NEEDS_CEPH_POOL
    return None


def is_valid_image_name(name: Any) -> bool:
    """Whether ``name`` is safe to put into a PromQL regex unescaped.

    :param name: Candidate RBD image name.
    :rtype: bool
    """
    return isinstance(name, str) and bool(_IMAGE_NAME.match(name))


def rbd_images_pattern(images: list[str]) -> str:
    """Join RBD image names into the ``{rbd_images}`` regex alternation.

    :param images: Image names; invalid and duplicate ones are dropped.
    :return: ``"a|b"``, or ``""`` when no valid image is left.
    :rtype: str
    """
    return "|".join(dict.fromkeys(image for image in images if is_valid_image_name(image)))


def promql_pool_check(pools: list[str]) -> str:
    """PromQL listing which of ``pools`` the Ceph exporter reports.

    :param pools: Ceph pool names.
    :return: A query whose result has one series per reported pool, label ``name``.
    :rtype: str
    """
    pattern = "|".join(re.escape(pool) for pool in pools)
    return f'count by (name) (ceph_pool_metadata{{name=~"{pattern}"}})'


def promql_volume_check(pools: list[str]) -> str:
    """PromQL listing which of ``pools`` have per-image (RBD) statistics.

    :param pools: Ceph pool names.
    :return: A query whose result has one series per pool with RBD stats, label ``pool``.
    :rtype: str
    """
    pattern = "|".join(re.escape(pool) for pool in pools)
    return f'count by (pool) (ceph_rbd_write_bytes{{pool=~"{pattern}"}})'


def storage_monitoring_record(
    storage_class: str = "",
    provisioner: str = "",
    pool: str = "",
    kind: str = "",
    rbd_images: str = "",
    pool_metrics: Optional[bool] = False,
    volume_metrics: Optional[bool] = False,
    reason: str = "",
) -> dict[str, Any]:
    """Build the ``storage_monitoring`` record a connection carries.

    :param storage_class: StorageClass of the configuration's PVC.
    :param provisioner: Its provisioner.
    :param pool: Ceph pool behind it.
    :param kind: ``"rbd"``, ``"cephfs"`` or ``""``.
    :param rbd_images: ``{rbd_images}`` alternation.
    :param pool_metrics: Whether pool-level metrics are collected.
    :param volume_metrics: Whether per-volume metrics are collected.
    :param reason: Why (some) Ceph metrics are off; empty when both are on.
    :return: The record, with the three placeholder values under ``placeholders``.
    :rtype: dict[str, Any]
    """
    return {
        "storage_class": storage_class,
        "provisioner": provisioner,
        "pool": pool,
        "kind": kind,
        "rbd_images": rbd_images,
        "pool_metrics": pool_metrics,
        "volume_metrics": volume_metrics,
        "reason": reason,
        "placeholders": {
            "storage_class": storage_class,
            "pool": pool if pool_metrics else "",
            "rbd_images": rbd_images if (pool_metrics and volume_metrics) else "",
        },
    }
