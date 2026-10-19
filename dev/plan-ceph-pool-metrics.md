# Plan: Ceph storage placeholders for monitoring

Status: **implemented** (2026-10-11, branch `feature/storage-class-sweep`),
M1–M5, released in v0.11.3. First cluster run 2026-10-15/16 (1792091105,
1792099970, 1792116019, 1792123892): CSVs filled and plausible; the summary
report has no Ceph table yet. Queries below were run against the
reference cluster's Prometheus on 2026-10-11.

Where it landed: `bexhoma/ceph_storage.py` (pure helpers shared by all
parts), `clusters.py` (`get_storage_class_info`, `get_pvc_rbd_image`,
`get_ceph_metrics_support`), `SutConfiguration.resolve_storage_monitoring`
and `storage_placeholder_values`, `configurations/metrics.py`
(`switch_off_unresolved`, `uses_storage_placeholders`), the 13 metrics in
`k8s-cluster.config` (copy them into a local `cluster.config`),
`CollectorBase.SHARED_METRICS`, the report's Ceph Storage section and `n/a`
rows, `environment.yml` (`ceph` per storage class, `needs` per metric),
`spec._validate_metrics`, `tests/test_ceph_storage_monitoring.py`.

Deviations from the sketch: no extra `_format_metric` helper (the four
`format` calls pass `storage_placeholder_values()`); storage placeholders are
resolved only when some query uses them, so a cluster config without Ceph
metrics makes no extra calls. Catalog 1.11.0 and result contract 1.10.0 are
unreleased, so their additions were folded in; `environment.yml` moved
1.4.0 -> 1.5.0 so files with the new fields can be told apart. The handbook
got no example (optional in M5). The lag (open decision below) is
documented, not corrected.

## Goal

A run on Ceph-backed storage records, per phase and per configuration:

- **pool:** what the Ceph pool behind the configuration's storage class
  read and wrote, all clients included;
- **volume:** what the configuration's own volume(s) did, as Ceph saw it,
  including Ceph-side write/read latency;
- **others:** what every other volume in that pool did in the same window.

On any storage that does not support this (ephemeral, `ramdisk`, non-Ceph
classes, a cluster without Ceph metrics), the metrics are switched off for
that configuration and nothing fails and nothing is reported as missing.

Motivation: on 2026-10-11 a parallel HammerDB run in the same namespace
wrote ~500 MB/s to the `nvme` pool during a fio comparison. Single WAL
commits dropped ~40% and p99 fdatasync rose from 0.7 ms to 3.5–5 ms.
Nothing in a Bexhoma result would have shown the load or its source.

## Facts this plan relies on

**Bexhoma**

- Metric templates: `credentials.k8s.monitor.metrics` in `k8s-cluster.config`
  (tracked template; the local `cluster.config` is gitignored and updated by
  hand).
- Placeholders are filled by `str.format` in four calls in
  `SutConfiguration.set_metric_of_config_default` / `set_metric_of_config`
  (`configurations/base.py:851-903`). Keys today: `host`, `gpuid`,
  `configuration`, `experiment`, `schema`, `database`. `format` ignores
  unused keyword arguments but raises `KeyError` for a placeholder it is not
  given, so **all four calls must pass the new keys**.
- The calls are driven from `MetricsCollector.get_connection_config`
  (`configurations/metrics.py:161-259`). It runs after the SUT is deployed
  (it reads the SUT pods), so the PVCs exist and are bound by then.
- Storage values (`configurations/base.py:1056-1118`, `clusters.py:402`):
  - `storageClassName is None`: no PVC (ephemeral, `use_ephemeral_storage`).
  - `'ramdisk'`: no PVC, a Bexhoma special, not a Kubernetes StorageClass.
  - `''`: a PVC on the cluster's default class.
  - Any other value: a PVC on that class.
- `get_list_of_pvc()` lists the PVCs of a configuration, including worker
  StatefulSets. `Kubernetes.get_pvc_storage_class(name)`
  (`clusters.py:949`) returns a PVC's class.
- Collected values: `counter` → `max - min` per phase window; gauge → mean;
  `ratio` → max (`collectors/base.py:442`, `report_writer.py:588`). Across
  configurations, counters are summed except `NODE_LEVEL_COUNTERS`
  (`collectors/base.py:257`), which take `max`.
- `active: False` makes dbmsbenchmarker's `fetchMetric` skip a metric
  silently (`DBMS-Benchmarker/dbmsbenchmarker/monitor.py:261-264`). An
  active metric with no data is zero-filled and logged as "Metrics missing"
  (`bexhoma/missing_metrics.py`).
- `environment.py` finds a query's series only as `name{...}`
  (`_SERIES_SELECTOR`), so every series in a query needs a label block.

**Prometheus / Ceph** (`prometheus.monitor`, mgr module)

- Pool counters: `ceph_pool_{wr,rd}` (ops) and `ceph_pool_{wr,rd}_bytes`, by
  `pool_id`. Pool names: `ceph_pool_metadata{pool_id, name}`. Every series
  appears twice, so deduplicate with `max by (pool_id)`.
- Per-image counters: `ceph_rbd_{write,read}_{ops,bytes}` and
  `ceph_rbd_{write,read}_latency_{sum,count}` (nanoseconds), by
  `pool`, `image`. These are also duplicated, so use `max by (image)`.
  Enabled for `k8svol` (773 images) and `nvme`, not for the CephFS data
  pool `home-data0`.
- Pool minus the sum of all images comes out slightly negative (−5 MB/s at
  one point), so the two families do not reconcile. "Others" is therefore
  computed from per-image counters only.
- A new image appears in the metrics after a short delay, with its counter
  already including the writes made before (seen: first sample 16.0 GiB).
  Without a fallback, `max - min` over the window would drop those writes.
- The counters lag the real I/O by about 1–2 minutes (scrape plus mgr
  stats period).

**Kubernetes**

- StorageClass → pool: `parameters.pool` for the Ceph CSI provisioners
  `rook-ceph.rbd.csi.ceph.com` (`cephcsi` → `k8svol`, `nvme` → `nvme`) and
  `rook-ceph.cephfs.csi.ceph.com` (`shared` → `home-data0`). Legacy Rook
  FlexVolume classes (`ceph`, `cephxfs`, provisioner `ceph.rook.io/block`)
  and `local-*` classes are not supported.
- PVC → image: PVC `spec.volumeName` → PV
  `spec.csi.volumeAttributes.imageName` (`csi-vol-<uuid>`, RBD only).
- User `perdelt` can read StorageClasses, PVCs and PVs.

## Decisions

1. **Three placeholders, resolved per configuration after deployment:**
   `{storage_class}` (the class the PVC actually uses, so `''` resolves to
   the default class), `{pool}` (the Ceph pool), and `{rbd_images}` (a
   regex alternation of the configuration's RBD image names, for example
   `csi-vol-a|csi-vol-b` for distributed workers).
2. **Unresolved means off, never failing.** A metric whose query contains a
   placeholder that resolved empty is set `active: False` for that
   configuration. Resolution never raises; every failure becomes an empty
   value plus a reason.
3. **The reason is recorded.** Every connection gets
   `storage_monitoring: {storage_class, provisioner, pool, rbd_images,
   pool_metrics, volume_metrics, reason}` in `connections.config`, so a
   result shows why Ceph metrics are absent.
4. **Prometheus is checked before enabling.** One query per experiment and
   pool through the dashboard pod (reuse `environment._query_prometheus`):
   does `ceph_pool_metadata{name=pool}` exist, and does
   `ceph_rbd_write_bytes{pool=pool}` exist? Absent or unchecked means the
   pool or volume metrics are off. This keeps clusters without Ceph metrics
   from logging "Metrics missing".
5. **Volume counters fall back to 0** (`or on() (0 * <pool series>)`) only
   after decision 4 confirmed that per-image stats exist for the pool. This
   covers the delay before a new image appears. The writes made before it
   appears are not lost, because the first sample already contains them.
6. **Others come from rates, not counters.** The set of other images
   changes while a phase runs (created, deleted), and a `max - min` over a
   sum of changing counters is wrong. Others are gauges in MiB/s and ops/s:
   the phase mean via the gauge reduction.
7. **Pool counters and others are shared values:** across configurations
   they take `max` (rename `NODE_LEVEL_COUNTERS` to `SHARED_COUNTERS`, keep
   an alias, add the keys). Volume counters sum normally.
8. **Overrides cannot re-enable an unresolved metric.**
   `monitoring_metric_overrides` is applied first, the placeholder check
   last.
9. **No new required metrics.** Nothing joins
   `environment.REQUIRED_HARDWARE_METRICS`.
10. **Descriptive, under `observe`, never a validity check.** The cluster
    and its Ceph pools are used by others all the time, so load from other
    volumes is the normal operating condition, not a fault. The metrics are
    collected like every other hardware metric (when hardware monitoring is
    on, listed in `observe.metrics` when the hypothesis relies on them).
    No check fails on them and the Health Summary does not mention them.
    They matter for an interpretation when the load from others differs
    between the configurations or phases being compared, because then it
    is a confounder (handbook M6.4/M6.5).
11. **Design-time validation must not let a listed metric vanish.** A
    Ceph metric in `observe.metrics` is refused when none of the experiment's
    storage classes supports it, because decision 2 would otherwise switch it
    off silently and break the catalog's promise that every listed metric is
    collected.
12. **`active` is per connection; metadata is the union.** In a sweep such as
    `nvme` + `ramdisk`, the Ceph metrics are active for one configuration and
    off for the other. A metric counts as collected for the experiment when
    *any* connection has it active. Today both the collector
    (`collectors/base.py:366-374`, first connection by name wins per key) and
    the report (`report_writer.py:492-514`, first connection with metrics)
    read `active` from one connection. If the `ramdisk` configuration sorts
    first, the `nvme` data would be fetched but never reported. Both must
    switch to "active in any connection".
13. **Not applicable is shown as such, never as 0 and never dropped.** A
    configuration whose metric is off has no CSV column; in report tables its
    cell is `n/a` with the reason from `storage_monitoring`, not `nan`, `0` or
    a missing row.

### Behaviour by storage

| Storage | `{storage_class}` | `{pool}` | `{rbd_images}` | Pool metrics | Volume + others metrics |
|---|---|---|---|---|---|
| `None` (ephemeral) | empty | empty | empty | off | off |
| `'ramdisk'` | empty | empty | empty | off | off |
| `''` (default class, e.g. `cephcsi`) | resolved from PVC | resolved | resolved | on | on |
| `cephcsi`, `nvme` (RBD CSI) | class | pool | images | on | on |
| `shared` (CephFS CSI) | `shared` | `home-data0` | empty | on | off |
| non-Ceph or legacy class | class | empty | empty | off | off |
| PVC missing or unbound | from config | from class | empty | on if pool resolved | off |
| StorageClass unreadable (403, deleted) | class | empty | empty | off | off |
| No Ceph series in Prometheus | resolved | resolved | resolved | off (decision 4) | off |
| Monitoring disabled | not resolved (no API calls) | | | | |

For `None` and `'ramdisk'` no Kubernetes call is made at all.

### Example: a sweep over `nvme` and `ramdisk`

| Stage | `nvme` configuration | `ramdisk` configuration |
|---|---|---|
| Validation (`spec.py`) | Ceph metrics in `observe.metrics` are accepted because one cell supports them | reported as not applicable for this cell |
| Resolution | class, pool `nvme`, its image | all empty, reason `ramdisk: no Ceph volume`, no API call |
| `connections.config` | Ceph metrics `active: True` | Ceph metrics `active: False`, `storage_monitoring.reason` set |
| Fetch (DBMS-Benchmarker) | `query_{component}_metric_ceph_*_{connection}.csv` written | metric skipped, no CSV, no "Metrics missing" |
| Combined CSV | one column | no column |
| Collector / report metadata | metric collected (decision 12) | |
| `monitoring.md` | values | `n/a (ramdisk: no Ceph volume)` (decision 13) |
| Shared-counter aggregation | `max` ignores the missing cell | |

Reading rule for the catalog and result contract: in such a sweep, the load
from other volumes on the Ceph pool is part of what distinguishes the
treatments (shared network storage versus private memory), not a confounder
between them. It is a confounder between phases or repetitions of the same
Ceph cell, and between two cells on Ceph pools. The cAdvisor
`total_fs_write` of a `ramdisk` cell is 0 by construction (tmpfs is no block
device); that is an existing limitation, unchanged here.

## Proposed metrics for `cluster.config`

All are `type: 'cluster'`. Each series in a query has a label block, so
`environment.yml` can check its availability. Brackets are doubled for
`str.format`.

```python
# --- Ceph pool behind the storage class: all clients (shared counters) ---
'ceph_pool_write': {
    'type': 'cluster', 'active': True, 'metric': 'counter',
    'query': 'max(max by (pool_id) (ceph_pool_wr_bytes{{pool_id!=""}}) * on(pool_id) group_left(name) max by (pool_id, name) (ceph_pool_metadata{{name="{pool}"}}))/1024/1024',
    'title': 'Ceph Pool Write, All Clients [MiB]'
},
'ceph_pool_write_ops': {
    'type': 'cluster', 'active': True, 'metric': 'counter',
    'query': 'max(max by (pool_id) (ceph_pool_wr{{pool_id!=""}}) * on(pool_id) group_left(name) max by (pool_id, name) (ceph_pool_metadata{{name="{pool}"}}))',
    'title': 'Ceph Pool Write Operations, All Clients [ops]'
},
'ceph_pool_read': {
    'type': 'cluster', 'active': True, 'metric': 'counter',
    'query': 'max(max by (pool_id) (ceph_pool_rd_bytes{{pool_id!=""}}) * on(pool_id) group_left(name) max by (pool_id, name) (ceph_pool_metadata{{name="{pool}"}}))/1024/1024',
    'title': 'Ceph Pool Read, All Clients [MiB]'
},
'ceph_pool_read_ops': {
    'type': 'cluster', 'active': True, 'metric': 'counter',
    'query': 'max(max by (pool_id) (ceph_pool_rd{{pool_id!=""}}) * on(pool_id) group_left(name) max by (pool_id, name) (ceph_pool_metadata{{name="{pool}"}}))',
    'title': 'Ceph Pool Read Operations, All Clients [ops]'
},
# --- This configuration's own RBD volume(s) (summed across configurations) ---
'ceph_volume_write': {
    'type': 'cluster', 'active': True, 'metric': 'counter',
    'query': '(sum(max by (image) (ceph_rbd_write_bytes{{pool="{pool}", image=~"{rbd_images}"}})) or on() (0 * max(ceph_pool_metadata{{name="{pool}"}})))/1024/1024',
    'title': 'Ceph Volume Write, This SUT [MiB]'
},
'ceph_volume_write_ops': {
    'type': 'cluster', 'active': True, 'metric': 'counter',
    'query': 'sum(max by (image) (ceph_rbd_write_ops{{pool="{pool}", image=~"{rbd_images}"}})) or on() (0 * max(ceph_pool_metadata{{name="{pool}"}}))',
    'title': 'Ceph Volume Write Operations, This SUT [ops]'
},
'ceph_volume_read': {
    'type': 'cluster', 'active': True, 'metric': 'counter',
    'query': '(sum(max by (image) (ceph_rbd_read_bytes{{pool="{pool}", image=~"{rbd_images}"}})) or on() (0 * max(ceph_pool_metadata{{name="{pool}"}})))/1024/1024',
    'title': 'Ceph Volume Read, This SUT [MiB]'
},
'ceph_volume_read_ops': {
    'type': 'cluster', 'active': True, 'metric': 'counter',
    'query': 'sum(max by (image) (ceph_rbd_read_ops{{pool="{pool}", image=~"{rbd_images}"}})) or on() (0 * max(ceph_pool_metadata{{name="{pool}"}}))',
    'title': 'Ceph Volume Read Operations, This SUT [ops]'
},
'ceph_volume_write_latency': {
    'type': 'cluster', 'active': True, 'metric': 'gauge',
    # NaN while the volume is idle (0/0); the phase mean skips NaN
    'query': 'sum(max by (image) (rate(ceph_rbd_write_latency_sum{{pool="{pool}", image=~"{rbd_images}"}}[2m]))) / sum(max by (image) (rate(ceph_rbd_write_latency_count{{pool="{pool}", image=~"{rbd_images}"}}[2m]))) / 1e6',
    'title': 'Ceph Volume Write Latency, This SUT [ms]'
},
'ceph_volume_read_latency': {
    'type': 'cluster', 'active': True, 'metric': 'gauge',
    'query': 'sum(max by (image) (rate(ceph_rbd_read_latency_sum{{pool="{pool}", image=~"{rbd_images}"}}[2m]))) / sum(max by (image) (rate(ceph_rbd_read_latency_count{{pool="{pool}", image=~"{rbd_images}"}}[2m]))) / 1e6',
    'title': 'Ceph Volume Read Latency, This SUT [ms]'
},
# --- Every other volume in the same pool (shared gauges) ---
'ceph_others_write_rate': {
    'type': 'cluster', 'active': True, 'metric': 'gauge',
    'query': '(sum(max by (image) (rate(ceph_rbd_write_bytes{{pool="{pool}", image!~"{rbd_images}"}}[2m]))) or on() (0 * max(ceph_pool_metadata{{name="{pool}"}})))/1024/1024',
    'title': 'Ceph Pool Write Rate, Other Volumes [MiB/s]'
},
'ceph_others_write_ops_rate': {
    'type': 'cluster', 'active': True, 'metric': 'gauge',
    'query': 'sum(max by (image) (rate(ceph_rbd_write_ops{{pool="{pool}", image!~"{rbd_images}"}}[2m]))) or on() (0 * max(ceph_pool_metadata{{name="{pool}"}}))',
    'title': 'Ceph Pool Write Operations Rate, Other Volumes [ops/s]'
},
'ceph_others_read_ops_rate': {
    'type': 'cluster', 'active': True, 'metric': 'gauge',
    'query': 'sum(max by (image) (rate(ceph_rbd_read_ops{{pool="{pool}", image!~"{rbd_images}"}}[2m]))) or on() (0 * max(ceph_pool_metadata{{name="{pool}"}}))',
    'title': 'Ceph Pool Read Operations Rate, Other Volumes [ops/s]'
},
```

Checked live (pool `nvme`, image of the running HammerDB volume): pool
write 1,145,089 MiB, volume write 431,396 MiB, an unknown image gives 0
(fallback), others 0 MiB/s, write latency 3.57 ms, an unknown pool gives no
data, and `home-data0` has no per-image series.

Not proposed: a CephFS "others" metric (no per-subvolume stats) and OSD-level
metrics. Both are open points below.

## Implementation sketch

### M1 — resolution (`clusters.py`)

- `get_storage_class_info(name) -> dict`: reads the StorageClass and returns
  `{provisioner, pool}`. `pool` is set only for provisioners ending in
  `.rbd.csi.ceph.com` or `.cephfs.csi.ceph.com`. Results are cached per
  class. 404/403/other errors return `{}` with a warning; this never raises
  and never retries in a loop (unlike `get_pvc_storage_class`).
- `get_pvc_rbd_image(pvc_name) -> str | None`: PVC → PV →
  `spec.csi.volumeAttributes.imageName`. Returns `None` when the PVC is
  unbound, the PV is not CSI, or there is no `imageName`. Accepts only
  `^[A-Za-z0-9._-]+$`, so the name can go into a PromQL regex without
  escaping.
- Tests with a mocked API: RBD, CephFS, legacy provisioner, `local-hdd`,
  404, 403, unbound PVC, PV without CSI.

### M2 — placeholders (`configurations/`)

- `SutConfiguration.resolve_storage_monitoring() -> dict`, cached on the
  configuration:
  - `None` or `'ramdisk'` → all empty, `reason` set, no API call;
  - else the class from the first PVC of `get_list_of_pvc()` via
    `get_pvc_storage_class` (falls back to `storageClassName`), then
    `get_storage_class_info`, then `get_pvc_rbd_image` for every PVC;
    images are joined with `|`;
  - decision 4: the Prometheus check, cached per experiment and pool, sets
    `pool_metrics` and `volume_metrics`;
  - `{rbd_images}` stays empty unless `volume_metrics`, and `{pool}` stays
    empty unless `pool_metrics`, so decision 2 does the switching.
- `_format_metric(metric, **keys)`: one helper used by the four `format`
  calls, which adds `storage_class`, `pool` and `rbd_images` from the cached
  dict.
- `metrics.py` (`get_connection_config`, all three loops: default metrics,
  `metrics_{statefulset}`, application metrics): after
  `apply_metric_override`, set `active = False` when the query contains a
  placeholder whose value is empty (`_unresolved_placeholders(query, values)`
  via `string.Formatter().parse`). Write `c['storage_monitoring']`.
- Only inside `if cfg.experiment.monitoring_active and 'monitor' in
  config_K8s`, so runs without monitoring make no extra calls.
- Tests: the table above row by row (formatted query or `active False`
  plus reason); the existing queries format exactly as before (golden test
  over `k8s-cluster.config`); an override to `True` stays `False` when
  unresolved; a StatefulSet with two PVCs gives `a|b`.

### M3 — metrics, aggregation, docs

- Add the metrics above to `k8s-cluster.config`. Note in the changelog that
  the local `cluster.config` needs them copied.
- `collectors/base.py`: `SHARED_COUNTERS` (alias `NODE_LEVEL_COUNTERS`) adds
  the `ceph_pool_*` and `ceph_others_*` keys. Despite the name, the gauges
  also need `max` across configurations; adjust
  `across_configurations` so that shared keys of any kind take `max`.
- `environment.py`: no code change. Check that `environment.yml` lists the
  new metrics as available on the reference cluster.
- `docs/Monitoring.md`: the placeholders, the behaviour table, the lag, and
  how to read volume vs. others.
- Tests: series names are found for each new query; shared reduction.

### M4 — report (descriptive only)

- `monitoring.md`: a "Storage" subsection per phase and configuration with
  own volume (MiB, ops, latency), other volumes (MiB/s, ops/s) and pool
  totals. A short note says: pool and other-volume numbers include every
  client on the pool, which is normally busy; they lag 1–2 minutes; they
  matter for a comparison when they differ between the compared
  configurations or phases.
- `connections.md`: each configuration's `storage_monitoring` record
  (class, pool, images, or the reason the metrics are off), next to
  `storage_reused`.
- No Health Summary line, no validity check (decision 10).
- Decision 12: `collectors/base.py::get_metrics` and
  `report_writer.py::_get_metric_definitions` merge `active` over all
  connections (`any`), keeping title/type/metric from the first definition.
  This also fixes the same latent issue for `monitoring_metric_overrides`.
- Decision 13: where monitoring tables are rendered, a configuration with
  the metric inactive shows `n/a` plus a footnote with its
  `storage_monitoring.reason`.
- Tests: a two-configuration fixture (`nvme` active, `ramdisk` inactive) in
  both name orders: the metric is reported, the nvme value appears, the
  ramdisk cell reads `n/a`, and no missing-metric entry is produced.
- `contract_result.yml`: describe the Storage subsection and the
  `storage_monitoring` field in the monitoring/connections entries, with
  the same reading rule; `docs/AgentResultContract.md`.

### M5 — environment, validation, catalog, agent

- `environment.py`: per storage class in `environment.yml`, record
  `ceph: {pool, per_volume}` from the StorageClass and the Prometheus check
  (`cephcsi`, `nvme`: per_volume true; `shared`: false; others: absent).
  Mark each metric that uses `{pool}` or `{rbd_images}` with what it needs
  (`needs: ceph_pool` or `needs: ceph_volume`), derived from its query.
- `spec.py::_validate_metrics`: refuse a listed metric whose need no storage
  class of the experiment meets (ephemeral, `ramdisk`, non-Ceph, CephFS for
  per-volume metrics), and name the reason. In a storage-class sweep, accept
  it when at least one cell meets it; the other cells report it as not
  applicable.
- `contract_catalog.yml`, `observe.metrics.out_of_scope`: these metrics
  cover the Ceph pool or the SUT's own volume, not the container or node;
  they exist only on Ceph classes (per-volume only on RBD); "other volumes"
  are other volumes in the same pool, not other pools on the same disks;
  the pool is shared and normally busy. Minor version bump, comments entry,
  `docs/AgentCatalogContract.md`.
- Agent prompt / handbook: nothing new is needed beyond the catalog text;
  M6.4/M6.5 already say to instrument shared resources and to state what
  isolation is known. Optionally one example under M6.5 naming
  `ceph_others_*` as the way to disclose storage load from others.
- Tests: validation refuses `ceph_volume_write` for an ephemeral and a
  `shared` design and accepts it for `cephcsi`; a mixed sweep is accepted;
  `environment.yml` marks needs and per-class support.

## Risks and open points

- **Lag versus window (open decision).** Phase windows are not widened
  (`extend: 20` and `shift` never took effect; since 2026-10-18 both are
  read and default to 0, see `dev/plan-metrics-pod-scope.md` M1b decision
  6; a global `shift` would move all metrics, not only Ceph's); the Ceph counters lag 1–2 minutes. Options: a per-metric
  `shift` honoured by DBMS-Benchmarker's `fetchMetric` (change in that
  repository), or accept the lag and document it. Phases shorter than
  ~5 minutes are affected most. Measure the real lag first by comparing a
  fio run's known start with the first counter movement.
- **Component windows.** The same metric set is fetched for the DBMS,
  loader and benchmarker windows; the Ceph metrics are per configuration,
  so they appear in every component table (like `io_wait_pct` today).
  Optionally restrict them with the metric's `component` filter after
  checking which component names `fetch` passes.
- **New image never appears within a short phase.** The fallback then
  reports 0 for the own volume. Rare (the delay is about a minute), but a
  loading phase under a minute on a fresh volume could hit it.
- **CephFS (`shared`)**: pool level only. Metadata and journal writes go to
  `home-metadata` and are not counted.
- **Pool scope, not OSD scope.** Pools share OSD hosts; load on another pool
  on the same OSDs stays invisible. `ceph_osd_op_w_latency_*` by host could
  follow.
- **Identifying the others.** Per-image stats name the other images; PVs of
  finished runs disappear, so any namespace/PVC lookup has to happen at
  collection time. Out of scope here.
