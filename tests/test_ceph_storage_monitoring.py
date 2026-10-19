"""
Tests for the Ceph storage placeholders of monitoring queries.

Covers ``bexhoma.ceph_storage`` (pure helpers), the cluster lookups
(StorageClass -> pool, PVC -> RBD image, Prometheus support), the per-
configuration resolution for every kind of storage (ephemeral, ``ramdisk``,
default class, RBD, CephFS, non-Ceph, unreadable, no Ceph metrics), switching
metrics off when a placeholder stays empty, the metrics in
``k8s-cluster.config``, collector and report handling of a metric that is
off for one configuration only (storage-class sweep ``nvme`` + ``ramdisk``),
``environment.yml``, and the ``observe.metrics`` check in ``spec``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import ast
import logging
import os
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import pandas as pd
from kubernetes.client.rest import ApiException

from bexhoma import ceph_storage, clusters, environment, report_writer
from bexhoma import spec as catalog_spec
from bexhoma.collectors.base import CollectorBase, metric_is_active
from bexhoma.configurations.base import SutConfiguration
from bexhoma.configurations.metrics import switch_off_unresolved, uses_storage_placeholders, apply_metric_override

_REPO = Path(__file__).resolve().parent.parent
_RBD = "rook-ceph.rbd.csi.ceph.com"
_CEPHFS = "rook-ceph.cephfs.csi.ceph.com"


def _template_metrics() -> dict:
    config = ast.literal_eval((_REPO / "k8s-cluster.config").read_text(encoding="utf-8"))
    return config["credentials"]["k8s"]["monitor"]


class PureHelpersTest(unittest.TestCase):
    """Provisioner -> pool, placeholder detection, image names, the record."""

    def test_ceph_pool_of(self) -> None:
        self.assertEqual(ceph_storage.ceph_pool_of(_RBD, {"pool": "nvme"}), ("nvme", "rbd"))
        self.assertEqual(ceph_storage.ceph_pool_of(_CEPHFS, {"pool": "home-data0", "fsName": "home"}),
                         ("home-data0", "cephfs"))
        for provisioner, parameters in (("ceph.rook.io/block", {"pool": "x"}),
                                        ("kubernetes.io/no-provisioner", {}),
                                        (_RBD, {}), ("", None)):
            with self.subTest(provisioner):
                self.assertEqual(ceph_storage.ceph_pool_of(provisioner, parameters), ("", ""))

    def test_placeholders_ignore_promql_label_blocks(self) -> None:
        query = 'max(ceph_pool_wr_bytes{{pool_id!=""}}) * on() max(m{{name="{pool}", i=~"{rbd_images}"}}) {host}'
        self.assertEqual(ceph_storage.query_placeholders(query), {"pool", "rbd_images", "host"})
        self.assertEqual(ceph_storage.unresolved_placeholders(query, {"pool": "nvme", "rbd_images": ""}),
                         ["rbd_images"])
        self.assertEqual(ceph_storage.metric_needs(query), ceph_storage.NEEDS_CEPH_VOLUME)
        self.assertEqual(ceph_storage.metric_needs('m{{name="{pool}"}}'), ceph_storage.NEEDS_CEPH_POOL)
        self.assertIsNone(ceph_storage.metric_needs('m{{instance="{host}"}}'))

    def test_image_pattern_drops_unsafe_and_duplicate_names(self) -> None:
        self.assertEqual(ceph_storage.rbd_images_pattern(["csi-vol-a", 'x"|.*', "csi-vol-a", "csi-vol-b"]),
                         "csi-vol-a|csi-vol-b")
        self.assertEqual(ceph_storage.rbd_images_pattern([]), "")

    def test_record_only_exposes_what_is_collected(self) -> None:
        record = ceph_storage.storage_monitoring_record(
            "nvme", _RBD, "nvme", "rbd", "csi-vol-a", pool_metrics=True, volume_metrics=False)
        self.assertEqual(record["placeholders"], {"storage_class": "nvme", "pool": "nvme", "rbd_images": ""})
        record = ceph_storage.storage_monitoring_record(
            "nvme", _RBD, "nvme", "rbd", "csi-vol-a", pool_metrics=None, volume_metrics=None)
        self.assertEqual(record["placeholders"]["pool"], "")


def _cluster() -> clusters.Kubernetes:
    cluster = object.__new__(clusters.Kubernetes)
    cluster.logger = logging.getLogger("test")
    cluster.namespace = "perdelt"
    cluster.v1core = mock.MagicMock()
    cluster.v1storage = mock.MagicMock()
    cluster._storage_class_info = {}
    cluster._ceph_metrics_support = {}
    return cluster


def _storage_class(provisioner, parameters):
    return types.SimpleNamespace(provisioner=provisioner, parameters=parameters)


class ClusterLookupTest(unittest.TestCase):
    """Never raises; every failure is an empty answer."""

    def test_storage_class_info(self) -> None:
        cluster = _cluster()
        cluster.v1storage.read_storage_class.return_value = _storage_class(_RBD, {"pool": "nvme"})
        self.assertEqual(cluster.get_storage_class_info("nvme"), {"provisioner": _RBD, "pool": "nvme", "kind": "rbd"})
        cluster.get_storage_class_info("nvme")
        cluster.v1storage.read_storage_class.assert_called_once()  # cached
        cluster.v1storage.read_storage_class.return_value = _storage_class("ceph.rook.io/block", {"blockPool": "x"})
        self.assertEqual(cluster.get_storage_class_info("ceph"), {"provisioner": "ceph.rook.io/block", "pool": "", "kind": ""})

    def test_storage_class_errors_give_empty(self) -> None:
        for status in (403, 404, 500):
            with self.subTest(status):
                cluster = _cluster()
                cluster.v1storage.read_storage_class.side_effect = ApiException(status=status)
                self.assertEqual(cluster.get_storage_class_info("nvme"), {})
                cluster.v1storage.read_storage_class.side_effect = RuntimeError("down")
                self.assertEqual(cluster.get_storage_class_info("other"), {})
        self.assertEqual(_cluster().get_storage_class_info(""), {})

    def _pvc(self, cluster, volume_name, csi):
        cluster.v1core.read_namespaced_persistent_volume_claim.return_value = types.SimpleNamespace(
            spec=types.SimpleNamespace(volume_name=volume_name))
        cluster.v1core.read_persistent_volume.return_value = types.SimpleNamespace(
            spec=types.SimpleNamespace(csi=csi))

    def test_pvc_rbd_image(self) -> None:
        cases = (
            ("pv-1", types.SimpleNamespace(volume_attributes={"imageName": "csi-vol-80f4"}), "csi-vol-80f4"),
            (None, None, None),  # unbound
            ("pv-1", None, None),  # not CSI
            ("pv-1", types.SimpleNamespace(volume_attributes={"subvolumeName": "x"}), None),  # CephFS
            ("pv-1", types.SimpleNamespace(volume_attributes={"imageName": 'a"|b'}), None),  # unsafe
        )
        for volume_name, csi, expected in cases:
            with self.subTest(volume_name=volume_name, csi=csi):
                cluster = _cluster()
                self._pvc(cluster, volume_name, csi)
                self.assertEqual(cluster.get_pvc_rbd_image("pvc"), expected)
        cluster = _cluster()
        cluster.v1core.read_namespaced_persistent_volume_claim.side_effect = ApiException(status=404)
        self.assertIsNone(cluster.get_pvc_rbd_image("pvc"))

    def test_ceph_metrics_support(self) -> None:
        cluster = _cluster()
        cluster.get_dashboard_pod_name = lambda: "dashboard"
        answers = [[{"metric": {"name": "nvme"}}], [{"metric": {"pool": "nvme"}}]]
        with mock.patch.object(environment, "_prometheus_url", return_value="http://p/api/v1/"), \
                mock.patch.object(environment, "_query_prometheus", side_effect=answers) as query:
            self.assertEqual(cluster.get_ceph_metrics_support("nvme"), {"pool_metrics": True, "volume_metrics": True})
            cluster.get_ceph_metrics_support("nvme")
            self.assertEqual(query.call_count, 2)  # cached

    def test_ceph_metrics_support_unknown(self) -> None:
        cluster = _cluster()
        cluster.get_dashboard_pod_name = lambda: ""
        with mock.patch.object(environment, "_prometheus_url", return_value="http://p/api/v1/"):
            self.assertIsNone(cluster.get_ceph_metrics_support("nvme"))
        cluster = _cluster()
        cluster.get_dashboard_pod_name = lambda: "dashboard"
        with mock.patch.object(environment, "_prometheus_url", return_value="http://p/api/v1/"), \
                mock.patch.object(environment, "_query_prometheus", side_effect=RuntimeError("boom")):
            self.assertIsNone(cluster.get_ceph_metrics_support("nvme"))


class _FakeCluster:
    """Answers the four lookups a configuration makes, and records them."""

    def __init__(self, pvc_class="nvme", info=None, images=None, support=None):
        self.pvc_class = pvc_class
        self.info = {"provisioner": _RBD, "pool": "nvme", "kind": "rbd"} if info is None else info
        self.images = images if images is not None else {"pvc-1": "csi-vol-a"}
        self.support = {"pool_metrics": True, "volume_metrics": True} if support is None else support
        self.calls = []

    def get_pvc_storage_class(self, name):
        self.calls.append("pvc_class")
        return self.pvc_class

    def get_storage_class_info(self, name):
        self.calls.append("info")
        return self.info

    def get_pvc_rbd_image(self, name):
        self.calls.append("image")
        return self.images.get(name)

    def get_ceph_metrics_support(self, pool):
        self.calls.append("support")
        return self.support


def _configuration(storage_class, cluster, pvcs=("pvc-1",)) -> SutConfiguration:
    cfg = object.__new__(SutConfiguration)
    cfg.storage = {"storageClassName": storage_class} if storage_class is not False else {}
    cfg.storage_monitoring = None
    cfg.experiment = types.SimpleNamespace(cluster=cluster)
    cfg.deployment_infos = {"deployment": {"sut": {"pvc": list(pvcs)}}, "statefulset": {}}
    cfg.configuration = "PostgreSQL-1"
    cfg.code = "1791727283"
    return cfg


class ResolutionTest(unittest.TestCase):
    """The plan's behaviour table, row by row."""

    def _resolve(self, storage_class, cluster, pvcs=("pvc-1",)):
        cfg = _configuration(storage_class, cluster, pvcs)
        return cfg, cfg.resolve_storage_monitoring()

    def test_ephemeral_and_ramdisk_make_no_call(self) -> None:
        for storage_class, reason in ((None, "ephemeral"), ("ramdisk", "ramdisk")):
            with self.subTest(storage_class):
                cluster = _FakeCluster()
                cfg, record = self._resolve(storage_class, cluster, pvcs=())
                self.assertEqual(cluster.calls, [])
                self.assertIn(reason, record["reason"])
                self.assertEqual(cfg.storage_placeholder_values(), {"storage_class": "", "pool": "", "rbd_images": ""})

    def test_rbd_class(self) -> None:
        cfg, record = self._resolve("nvme", _FakeCluster())
        self.assertEqual(cfg.storage_placeholder_values(),
                         {"storage_class": "nvme", "pool": "nvme", "rbd_images": "csi-vol-a"})
        self.assertTrue(record["pool_metrics"] and record["volume_metrics"])
        self.assertEqual(record["reason"], "")

    def test_default_class_resolved_from_pvc(self) -> None:
        cfg, record = self._resolve("", _FakeCluster(pvc_class="cephcsi",
                                                     info={"provisioner": _RBD, "pool": "k8svol", "kind": "rbd"}))
        self.assertEqual(record["storage_class"], "cephcsi")
        self.assertEqual(cfg.storage_placeholder_values()["pool"], "k8svol")

    def test_cephfs_has_pool_but_no_volume_metrics(self) -> None:
        cluster = _FakeCluster(pvc_class="shared", info={"provisioner": _CEPHFS, "pool": "home-data0", "kind": "cephfs"},
                               support={"pool_metrics": True, "volume_metrics": False})
        cfg, record = self._resolve("shared", cluster)
        self.assertNotIn("image", cluster.calls)
        self.assertEqual(cfg.storage_placeholder_values(),
                         {"storage_class": "shared", "pool": "home-data0", "rbd_images": ""})
        self.assertIn("cephfs", record["reason"])

    def test_non_ceph_and_unreadable_classes(self) -> None:
        for info, reason in (({"provisioner": "kubernetes.io/no-provisioner", "pool": "", "kind": ""}, "not a Ceph"),
                             ({}, "could not be read")):
            with self.subTest(reason):
                cluster = _FakeCluster(pvc_class="local-hdd", info=info)
                cfg, record = self._resolve("local-hdd", cluster)
                self.assertNotIn("support", cluster.calls)
                self.assertEqual(cfg.storage_placeholder_values()["pool"], "")
                self.assertIn(reason, record["reason"])

    def test_no_ceph_metrics_or_unknown(self) -> None:
        for support, reason in (({"pool_metrics": False, "volume_metrics": False}, "no Ceph metrics"),
                                (None, "could not be asked")):
            with self.subTest(reason):
                cluster = _FakeCluster()
                cluster.support = support
                cfg, record = self._resolve("nvme", cluster)
                self.assertEqual(cfg.storage_placeholder_values()["pool"], "")
                self.assertEqual(cfg.storage_placeholder_values()["rbd_images"], "")
                self.assertIn(reason, record["reason"])

    def test_unbound_pvc_keeps_pool_metrics(self) -> None:
        cfg, record = self._resolve("nvme", _FakeCluster(images={}))
        self.assertEqual(cfg.storage_placeholder_values(), {"storage_class": "nvme", "pool": "nvme", "rbd_images": ""})
        self.assertIn("no RBD image", record["reason"])

    def test_worker_pvcs_give_an_alternation(self) -> None:
        cluster = _FakeCluster(images={"pvc-1": "csi-vol-a", "pvc-2": "csi-vol-b"})
        cfg = _configuration("nvme", cluster, pvcs=())
        cfg.deployment_infos = {"deployment": {}, "statefulset": {"worker": {"pvc": ["pvc-1", "pvc-2"]}}}
        cfg.resolve_storage_monitoring()
        self.assertEqual(cfg.storage_placeholder_values()["rbd_images"], "csi-vol-a|csi-vol-b")

    def test_resolved_once(self) -> None:
        cluster = _FakeCluster()
        cfg, _ = self._resolve("nvme", cluster)
        calls = list(cluster.calls)
        cfg.resolve_storage_monitoring()
        self.assertEqual(cluster.calls, calls)

    def test_queries_get_the_values(self) -> None:
        cfg, _ = self._resolve("nvme", _FakeCluster())
        query = cfg.set_metric_of_config_default(
            'm{{pool="{pool}", image=~"{rbd_images}", host="{host}"}}', host="n1", gpuid="", schema="", database="")
        self.assertEqual(query, 'm{pool="nvme", image=~"csi-vol-a", host="n1"}')


class SwitchOffTest(unittest.TestCase):
    """A metric whose storage placeholder is empty is off, even when an experiment asks for it."""

    def test_switch_off_after_override(self) -> None:
        definition = {"active": False, "query": 'm{{pool="{pool}"}}', "title": "Pool"}
        metric = switch_off_unresolved(
            apply_metric_override("ceph_pool_write", definition, {"ceph_pool_write": True}),
            {"storage_class": "", "pool": "", "rbd_images": ""})
        self.assertFalse(metric["active"])
        self.assertIn("pool", metric["inactive_reason"])

    def test_resolved_or_unrelated_metrics_stay(self) -> None:
        values = {"storage_class": "nvme", "pool": "nvme", "rbd_images": ""}
        self.assertTrue(switch_off_unresolved({"active": True, "query": 'm{{pool="{pool}"}}'}, values)["active"])
        self.assertTrue(switch_off_unresolved({"active": True, "query": 'm{{instance="{host}"}}'},
                                              {"storage_class": "", "pool": "", "rbd_images": ""})["active"])
        self.assertFalse(switch_off_unresolved({"active": True, "query": 'm{{image=~"{rbd_images}"}}'}, values)["active"])

    def test_uses_storage_placeholders(self) -> None:
        self.assertTrue(uses_storage_placeholders(_template_metrics()))
        self.assertFalse(uses_storage_placeholders({"metrics": {"cpu": {"query": 'm{{instance="{host}"}}'}},
                                                    "pd": {"metrics": {"x": {"query": "y"}}}}))


class TemplateMetricsTest(unittest.TestCase):
    """The Ceph metrics in k8s-cluster.config, and that every other query formats as before."""

    _BASE = {"host": "n1", "gpuid": "", "configuration": "pg", "experiment": "1", "schema": "s", "database": "d",
             "pods": "(.*)pg-1(.*)", "namespace": "ns"}

    def test_existing_queries_are_unchanged(self) -> None:
        values = {"storage_class": "nvme", "pool": "nvme", "rbd_images": "csi-vol-a"}
        for key, metric in _template_metrics()["metrics"].items():
            if ceph_storage.metric_needs(metric["query"]):
                continue
            with self.subTest(key):
                self.assertEqual(metric["query"].format(**self._BASE, **values), metric["query"].format(**self._BASE))

    def test_ceph_metrics(self) -> None:
        metrics = {key: metric for key, metric in _template_metrics()["metrics"].items() if key.startswith("ceph_")}
        self.assertEqual(len(metrics), 13)
        values = {"storage_class": "nvme", "pool": "nvme", "rbd_images": "csi-vol-a"}
        for key, metric in metrics.items():
            with self.subTest(key):
                self.assertTrue(metric["active"])
                expected = ceph_storage.NEEDS_CEPH_POOL if key.startswith("ceph_pool") else ceph_storage.NEEDS_CEPH_VOLUME
                self.assertEqual(ceph_storage.metric_needs(metric["query"]), expected)
                formatted = metric["query"].format(**self._BASE, **values)
                self.assertNotIn("{{", formatted)
                self.assertIn('"nvme"', formatted)
                self.assertTrue(environment._metric_series_names(metric["query"]))
        self.assertIn('image!~"csi-vol-a"', metrics["ceph_others_write_rate"]["query"].format(**self._BASE, **values))


def _connection(name, active, reason=""):
    connection = {"name": name, "monitoring": {"metrics": {
        "ceph_volume_write": {"title": "Ceph Volume Write, This SUT [MiB]", "active": active,
                              "type": "cluster", "metric": "counter"},
        "total_cpu_util": {"title": "CPU", "active": True, "type": "cluster", "metric": "gauge"},
    }}}
    if reason:
        connection["storage_monitoring"] = {"reason": reason}
    return connection


class MixedSweepTest(unittest.TestCase):
    """nvme + ramdisk: the metric is active in one connection only, in either name order."""

    def _connections(self, ramdisk_first):
        nvme = _connection("PostgreSQL-nvme", True)
        ramdisk = _connection("PostgreSQL-ramdisk", False, "ramdisk: no Ceph volume")
        return [ramdisk, nvme] if ramdisk_first else [nvme, ramdisk]

    def test_report_definitions_merge_active(self) -> None:
        for ramdisk_first in (True, False):
            with self.subTest(ramdisk_first=ramdisk_first):
                definitions = report_writer._get_metric_definitions(self._connections(ramdisk_first))
                self.assertTrue(report_writer._metric_is_active(definitions["ceph_volume_write"]))

    def test_collector_metadata_merges_active(self) -> None:
        for ramdisk_first in (True, False):
            with self.subTest(ramdisk_first=ramdisk_first), tempfile.TemporaryDirectory() as folder:
                os.makedirs(os.path.join(folder, "1"))
                Path(folder, "1", "connections.config").write_text(repr(self._connections(ramdisk_first)), encoding="utf-8")
                collector = object.__new__(CollectorBase)
                collector.path = folder
                df_metrics = collector.get_metrics(types.SimpleNamespace(code="1"))
                self.assertTrue(metric_is_active(df_metrics.loc["ceph_volume_write"].to_dict()))

    def test_not_applicable_rows(self) -> None:
        connections = self._connections(True)
        inactive = report_writer._inactive_connections(connections, "ceph_volume_write")
        self.assertEqual(inactive, {"PostgreSQL-ramdisk": "ramdisk: no Ceph volume"})
        df = pd.DataFrame({"Ceph Volume Write, This SUT [MiB]": [123.0]}, index=["PostgreSQL-nvme"])
        df = report_writer._add_not_applicable(df, inactive)
        self.assertEqual(df.loc["PostgreSQL-ramdisk"].iloc[0], "n/a (ramdisk: no Ceph volume)")
        self.assertEqual(df.loc["PostgreSQL-nvme"].iloc[0], 123.0)

    def test_ceph_storage_section(self) -> None:
        connections = self._connections(True)
        definitions = report_writer._get_metric_definitions(connections)
        series = pd.DataFrame({"PostgreSQL-nvme": [100.0, 160.0]})
        evaluator = types.SimpleNamespace(get_monitoring_metric=lambda metric, component: series.copy())
        section = report_writer._build_ceph_storage_section(
            evaluator, connections, definitions, {"benchmarking": "Benchmarking phase: SUT deployment"})
        table = section.children[0].dataframe
        self.assertEqual(table.loc["PostgreSQL-nvme", "Ceph Volume Write, This SUT [MiB]"], 60.0)
        self.assertEqual(table.loc["PostgreSQL-ramdisk", "Ceph Volume Write, This SUT [MiB]"],
                         "n/a (ramdisk: no Ceph volume)")

    def test_ceph_storage_section_only_for_sut_components(self) -> None:
        connections = self._connections(True)
        definitions = report_writer._get_metric_definitions(connections)
        series = pd.DataFrame({"PostgreSQL-nvme": [100.0, 160.0]})
        evaluator = types.SimpleNamespace(get_monitoring_metric=lambda metric, component: series.copy())
        section = report_writer._build_ceph_storage_section(evaluator, connections, definitions, {
            "loading": "Loading phase: SUT deployment",
            "datagenerator": "Loading phase: component data generator",
            "loader": "Loading phase: component loader",
            "workerloading": "Loading phase: component worker",
            "benchmarker": "Benchmarking phase: component benchmarker",
        })
        self.assertEqual([child.heading for child in section.children],
                         ["Loading phase: SUT deployment", "Loading phase: component worker"])

    def test_no_section_without_ceph_metrics(self) -> None:
        connections = [_connection("a", False, "ephemeral storage: no Ceph volume")]
        definitions = report_writer._get_metric_definitions(connections)
        evaluator = types.SimpleNamespace(get_monitoring_metric=lambda metric, component: pd.DataFrame())
        self.assertIsNone(report_writer._build_ceph_storage_section(evaluator, connections, definitions, {"b": "B"}))


class SharedMetricsTest(unittest.TestCase):
    """Pool and other-volume metrics are shared across configurations; the old name still works."""

    def test_shared_keys(self) -> None:
        self.assertIs(CollectorBase.NODE_LEVEL_COUNTERS, CollectorBase.SHARED_METRICS)
        for key in ("io_wait_total", "ceph_pool_write", "ceph_others_write_rate"):
            self.assertIn(key, CollectorBase.SHARED_METRICS)
        self.assertNotIn("ceph_volume_write", CollectorBase.SHARED_METRICS)

    def test_others_gauge_takes_max_across_configurations(self) -> None:
        title = "Ceph Pool Write Rate, Other Volumes [MiB/s]"
        collector = object.__new__(CollectorBase)
        collector.with_monitoring = True
        collector.df_metrics = pd.DataFrame({"ceph_others_write_rate": {
            "title": title, "active": True, "type": "cluster", "metric": "gauge"}}).T
        per_job = pd.DataFrame({title: [40.0, 50.0]}, index=["1-pg-0-1-1-1", "1-pg-1-1-1-1"])
        meta = per_job.copy()
        meta["configuration"] = ["pg-0", "pg-1"]
        for column, value in (("code", "1"), ("experiment_run", 1), ("client", 1),
                              ("type_tenants", "container"), ("num_tenants", 2)):
            meta[column] = value
        collector.get_monitoring_aggregated_per_job = lambda type: per_job
        collector.add_metadata = lambda df: meta
        row = collector.get_monitoring_aggregated_per_phase_multitenant("benchmarking").iloc[0]
        self.assertEqual(row[title], 50.0)


def _v1storageclass(name, provisioner, parameters):
    return types.SimpleNamespace(metadata=types.SimpleNamespace(name=name), provisioner=provisioner,
                                 parameters=parameters, reclaim_policy="Delete", volume_binding_mode="Immediate")


class EnvironmentTest(unittest.TestCase):
    """environment.yml records Ceph support per class and what each metric needs."""

    def _classes(self):
        return [
            environment.StorageClassInfo.from_v1storageclass(_v1storageclass("nvme", _RBD, {"pool": "nvme"}), {"nvme": "nvme"}),
            environment.StorageClassInfo.from_v1storageclass(
                _v1storageclass("shared", _CEPHFS, {"pool": "home-data0"}), {"shared": "shared"}),
            environment.StorageClassInfo.from_v1storageclass(
                _v1storageclass("local-hdd", "kubernetes.io/no-provisioner", {}), {}),
        ]

    def test_ceph_field(self) -> None:
        nvme, shared, local = self._classes()
        self.assertEqual(nvme.ceph, {"pool": "nvme", "kind": "rbd"})
        self.assertEqual(shared.ceph, {"pool": "home-data0", "kind": "cephfs"})
        self.assertIsNone(local.ceph)

    def test_support_checked(self) -> None:
        classes = self._classes()
        cluster = types.SimpleNamespace(get_dashboard_pod_name=lambda: "dashboard")
        answers = [[{"metric": {"name": "nvme"}}, {"metric": {"name": "home-data0"}}], [{"metric": {"pool": "nvme"}}]]
        with mock.patch.object(environment, "_prometheus_url", return_value="http://p/api/v1/"), \
                mock.patch.object(environment, "_query_prometheus", side_effect=answers):
            self.assertTrue(environment.apply_ceph_metrics_support(cluster, classes))
        nvme, shared, local = classes
        self.assertEqual((nvme.ceph["pool_metrics"], nvme.ceph["volume_metrics"]), (True, True))
        self.assertEqual((shared.ceph["pool_metrics"], shared.ceph["volume_metrics"]), (True, False))
        self.assertIsNone(local.ceph)

    def test_support_unchecked_leaves_flags_out(self) -> None:
        classes = self._classes()
        cluster = types.SimpleNamespace(get_dashboard_pod_name=lambda: "")
        with mock.patch.object(environment, "_prometheus_url", return_value="http://p/api/v1/"):
            self.assertFalse(environment.apply_ceph_metrics_support(cluster, classes))
        self.assertNotIn("pool_metrics", classes[0].ceph)
        self.assertIsNone(environment.apply_ceph_metrics_support(cluster, [classes[2]]))

    def test_metrics_carry_needs(self) -> None:
        cluster = types.SimpleNamespace(config={"credentials": {"k8s": {"monitor": _template_metrics()}}})
        with mock.patch.object(environment, "_available_series", return_value=None):
            hardware = environment.collect_monitoring_metrics(cluster)["hardware"]
        self.assertEqual(hardware["ceph_pool_write"]["needs"], "ceph_pool")
        self.assertEqual(hardware["ceph_volume_write"]["needs"], "ceph_volume")
        self.assertEqual(hardware["ceph_others_write_rate"]["needs"], "ceph_volume")
        self.assertNotIn("needs", hardware["total_cpu_util"])


_ENVIRONMENT = {
    "nodes": [],
    "storage_classes": [
        {"name": "nvme", "usable": True, "ceph": {"pool": "nvme", "kind": "rbd", "pool_metrics": True, "volume_metrics": True}},
        {"name": "cephcsi", "usable": True, "ceph": {"pool": "k8svol", "kind": "rbd"}},  # support not checked
        {"name": "shared", "usable": True, "ceph": {"pool": "home-data0", "kind": "cephfs", "pool_metrics": True, "volume_metrics": False}},
        {"name": "silent", "usable": True, "ceph": {"pool": "p", "kind": "rbd", "pool_metrics": False, "volume_metrics": False}},
        {"name": "local", "usable": True, "ceph": None},
    ],
    "monitoring": {"hardware": {
        "ceph_volume_write": {"title": "V", "kind": "counter", "active": True, "available": True, "needs": "ceph_volume"},
        "ceph_pool_write": {"title": "P", "kind": "counter", "active": True, "available": True, "needs": "ceph_pool"},
        "total_cpu_util": {"title": "CPU", "kind": "gauge", "active": True, "available": True},
    }},
}


def _experiment(storage_class, metrics):
    return {"resources": {"storage_class": storage_class},
            "observe": {"monitoring_sut": True, "metrics": metrics}}


class SpecValidationTest(unittest.TestCase):
    """A Ceph metric needs at least one storage cell that can serve it."""

    def test_accepted(self) -> None:
        for storage_class, metrics in (
            ("nvme", ["ceph_volume_write", "ceph_pool_write"]),
            ("cephcsi", ["ceph_volume_write"]),  # not checked counts as possible
            ("shared", ["ceph_pool_write"]),
            (["nvme", None], ["ceph_volume_write"]),  # mixed sweep
            (None, ["total_cpu_util"]),
        ):
            with self.subTest(storage_class=storage_class, metrics=metrics):
                catalog_spec.validate_environment(_ENVIRONMENT, _experiment(storage_class, metrics))

    def test_refused(self) -> None:
        for storage_class, metric, reason in (
            (None, "ceph_volume_write", "ephemeral"),
            (None, "ceph_pool_write", "ephemeral"),
            ("shared", "ceph_volume_write", "no per-volume statistics"),
            ("local", "ceph_pool_write", "not a Ceph storage class"),
            ("silent", "ceph_pool_write", "no Ceph metrics"),
            (["shared", None], "ceph_volume_write", "ephemeral"),
        ):
            with self.subTest(storage_class=storage_class, metric=metric), \
                    self.assertRaisesRegex(catalog_spec.SpecError, reason):
                catalog_spec.validate_environment(_ENVIRONMENT, _experiment(storage_class, [metric]))


if __name__ == "__main__":
    unittest.main()
