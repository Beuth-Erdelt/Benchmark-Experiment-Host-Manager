# Concept: DBMS

To include a DBMS in a Kubernetes-based experiment you need:

- a Docker image
- a JDBC driver (for SQL-based DBMS used with DBMSBenchmarker)
- a Kubernetes deployment manifest (YAML template)
- a configuration entry in `cluster.config` (the `dockers` section)
- DDL scripts for schema creation, data loading, and index building

This document covers all DBMS currently supported by bexhoma.

**Relational / SQL**
- [PostgreSQL](#postgresql)
- [PostgreSQL + PGBouncer](#pgbouncer)
- [MySQL](#mysql)
- [MariaDB](#mariadb)
- [MonetDB](#monetdb)
- [Citus](#citus)
- [ClickHouse](#clickhouse)
- [ClickHouseCluster](#clickhousecluster)
- [CedarDB](#cedardb)

**Distributed SQL / Cloud-Native**
- [YugabyteDB](#yugabytedb)
- [CockroachDB](#cockroachdb)
- [TiDB](#tidb)

**Key-Value Stores (YCSB)**
- [Dragonfly](#dragonfly)
- [DragonflyCluster](#dragonflycluster)
- [Redis (Cluster)](#redis)

**External / Cloud Database Services**
- [DatabaseService](#databaseservice)

**Raw Hardware Benchmarks (no DBMS)**
- [Hardware](#hardware)

---

## Configuration Reference

Every entry in the `dockers` section of `cluster.config` may contain the following fields:

| Field | Required | Description |
|---|---|---|
| `loadData` | yes | Shell command run inside the SUT container to execute an init script. Placeholders: `{scriptname}`, `{database}`, `{schema}`, `{service_name}`, `{namespace}` |
| `delay_prepare` | no | Seconds to wait after the container starts before bexhoma considers it ready (useful for engines that restart during init, e.g., MySQL InnoDB setup) |
| `template` | yes | Base connection template passed to DBMSBenchmarker — includes `version`, `alias`, `docker_alias`, `dialect`, and `JDBC` sub-section |
| `template.JDBC.driver` | yes¹ | Fully qualified Java class name of the JDBC driver |
| `template.JDBC.auth` | yes¹ | `[username, password]` pair |
| `template.JDBC.url` | yes¹ | JDBC URL template. Placeholders: `{serverip}`, `{database}`, `{schema}`, `{dbname}`, `{timeout_ms}`, `{namespace}` |
| `template.JDBC.jar` | yes¹ | JDBC jar filename(s) expected in `jarfolder` |
| `template.JDBC.database` | no | Default database name (substituted into `{database}` in `loadData` and the JDBC URL; overridden per tenant in multi-tenant mode) |
| `template.JDBC.schema` | no | Default schema name (substituted into `{schema}`; overridden per tenant) |
| `template.init_SQL` | no | SQL statement executed after connection is established (e.g., `SET optimizer_switch = ...`) |
| `logfile` | no | Path inside the container to a log file that bexhoma downloads after each experiment |
| `datadir` | no | Path inside the container to the DBMS data directory; bexhoma measures its size after loading |
| `attachWorker` | no | Command run on the coordinator to register a new worker node (used for distributed DBMS like Citus, CockroachDB) |
| `worker_port` | no | Internal port of the worker/coordinator headless service, appended to every host of the worker lists (used for TiDB, and for Citus' `BEXHOMA_URL_LIST`: a multi-host JDBC URL needs the port on every host) |
| `store_args` | no | Whether to capture and display the container startup arguments in the experiment summary (default: `True`) |
| `priceperhourdollar` | no | Reserved for cost modelling (currently unused) |
| `monitor` | no | Application-level monitoring configuration; see [Monitoring](Monitoring.md) |

¹ Only required for SQL DBMS queried via DBMSBenchmarker. Entries whose SUT is
never queried through DBMSBenchmarker — [Dragonfly](#dragonfly),
[DragonflyCluster](#dragonflycluster), [Redis](#redis), [Hardware](#hardware) —
omit `template.JDBC` entirely; `template` itself is still required (at minimum
`version`, `alias`, `docker_alias`), and `template.auth` (a `[username,
password]` pair) becomes required instead — `configurations/manifest.py`
falls back to `template['auth']` for `BEXHOMA_USER`/`BEXHOMA_PASSWORD`
injection whenever `template.JDBC` is absent.

### JDBC URL Placeholders

| Placeholder | Substituted with |
|---|---|
| `{serverip}` | Cluster-internal DNS name of the SUT service |
| `{database}` | Database name (from `template.JDBC.database`, overridden by tenant settings) |
| `{schema}` | Schema name (from `template.JDBC.schema`, overridden by tenant settings) |
| `{dbname}` | Alias for `{database}` (legacy; prefer `{database}`) |
| `{timeout_ms}` | Query timeout in milliseconds |
| `{namespace}` | Kubernetes namespace from the cluster config |

### Host Information Collected Automatically

After the SUT starts, bexhoma collects the following from inside the container and attaches it to the connection record:

- Total RAM (from `/proc/meminfo`)
- CPU model and core count (from `/proc/cpuinfo`)
- Kernel version (`uname -r`)
- Disk space used on `/` and in the data directory (`du` on `datadir`)
- GPU count and model (via `nvidia-smi`, if present)
- Kubernetes node name (from the pod spec)

This information appears in the **Connections** section of every experiment summary.

### Deployment Manifests

Every DBMS needs a Kubernetes manifest template at `k8s/deploymenttemplate-<Key>.yml`.
The key must match the `dockers` key in `cluster.config` exactly.
See [Deployment Template Conventions](#deployment-template-conventions) for the full authoring rules.

Resource requests, limits, and node selectors can be overridden at runtime via CLI parameters (`-rnn`, `-rnl`, `-rnb`) or programmatically via `experiment.set_resources(...)`.
See [Deployments](Deployments.md) for details.

---

## Deployment Template Conventions

This section describes the rules that every `k8s/deploymenttemplate-<Key>.yml` file must follow.
`start_sut()` in `configurations/lifecycle.py` reads these files and applies the conventions at runtime to generate the actual Kubernetes resource names and inject environment variables.
The full reference (including job templates and non-SUT manifests) is in [`k8s/README.md`](../k8s/README.md).

### File naming

The template filename is derived automatically from the `dockers` key:

```
k8s/deploymenttemplate-{Key}.yml
```

The `Key` must exactly match the key in the `dockers` section of `cluster.config` and the value passed as `docker=` to `configurations.default(...)`.
Casing matters: `PostgreSQL` → `deploymenttemplate-PostgreSQL.yml`.

### Document structure

A SUT deployment template is a **multi-document YAML** file (documents separated by `---`).
`start_sut()` processes all documents in the file.
Each document must be one of the following Kubernetes kinds:

| Kind | Required? | Notes |
|---|---|---|
| `PersistentVolumeClaim` | Optional | Omit when `use_storage=False`; removed automatically when `use_ramdisk=True` |
| `Service` | Optional | Used for the SUT port and, optionally, for worker headless services |
| `Deployment` | At least one required | The main DBMS container |
| `StatefulSet` | Optional | One per distributed worker role (e.g. TiKV, PD) |

Recommended order within the file: PVC first, then Service(s), then Deployment/StatefulSet(s).

### Mandatory labels

Every document in the template must carry these labels on `metadata.labels` (and on `spec.template.metadata.labels` for pod-creating resources):

| Label | Placeholder value | Runtime value |
|---|---|---|
| `app` | `bexhoma` | Always `bexhoma` |
| `component` | role-specific (see below) | **Never overwritten** — used as routing key by `start_sut()` |
| `configuration` | `default` | DBMS configuration name (e.g. `PostgreSQL`) |
| `experiment` | `default` | Unique experiment code (timestamp-based string) |

Use exactly these placeholder values in the template file; `start_sut()` replaces all of them at runtime except `component`.

### The `component` label

The `component` label value on each document tells `start_sut()` what kind of resource it is and how to name and wire it.
Do not change the `component` value at runtime — it is an identity, not a parameter.

| `component` value | Applied to | What `start_sut()` does |
|---|---|---|
| `sut` | Deployment, Service, PVC | Names all resources using `generate_component_name(component='sut', ...)`; the resulting name becomes the SUT service hostname |
| `storage` | PVC | Names the PVC using `generate_component_name(component='storage', ...)`; labels it with load status |
| `worker` | StatefulSet, Service | Names the StatefulSet using `get_worker_name(component='worker')`; injects `BEXHOMA_WORKER_*` env vars into all containers |
| `store` | StatefulSet, Service | Same as `worker` but injects `BEXHOMA_STORE_*` env vars |
| `pd` | StatefulSet, Service | Same pattern; injects `BEXHOMA_PD_*` env vars (used by TiDB) |
| `pool` | Deployment, Service | Connection pool sidecar (e.g. PGBouncer); named using `generate_component_name(component='pool', ...)` |

For every StatefulSet with `component: X`, `start_sut()` automatically injects these env vars into all containers:

| Env var | Content |
|---|---|
| `BEXHOMA_{X}_NAME` | StatefulSet name |
| `BEXHOMA_{X}_SERVICE` | Headless service name |
| `BEXHOMA_{X}_LIST` | Comma-separated DNS addresses of all pods (`{name}-{i}.{service}`) |
| `BEXHOMA_{X}_LIST_SPACE` | Same, space-separated |

(`X` is the uppercased component value, e.g. `worker` → `BEXHOMA_WORKER_NAME`.)

### Runtime name generation

All resource `name:` fields in the template are placeholders; `start_sut()` always overwrites them.
The generated names follow this formula (from `generate_component_name()` in `configurations/base.py`):

```
{app}-{component}-{configuration}-{experiment}
```

All lowercase.  For workers the formula draws from the storage label rather than the experiment code.
Worker PVCs from `volumeClaimTemplates` follow the fixed prefix `bxw-{worker_name}-{i}`.

Example SUT name: `bexhoma-sut-postgresql-1717000000`

### Reserved container names

The `name:` of every container inside a pod spec is read by `start_sut()` and the evaluator pipeline.
These names must be used exactly:

| Container name | Pod type | Role |
|---|---|---|
| `dbms` | SUT Deployment / StatefulSet | Primary DBMS process. `start_sut()` reads its `args` for the summary and manages its volume mounts. |
| `monitor-application` | SUT Deployment | Application metrics exporter (e.g. postgres-exporter). Removed when app monitoring is disabled. |
| `cadvisor` | SUT / worker (sidecar) | Node metrics. Removed when cluster-level monitoring already exists. |
| `dcgm-exporter` | SUT / worker (sidecar) | GPU metrics. Removed when cluster-level monitoring already exists. |
| `pool` | Connection-pool Deployment | PGBouncer or equivalent. |

For **job templates** (loading and benchmarking) the reserved names are `datagenerator` (initContainer), `sensor` (loader), and `dbmsbenchmarker` (benchmarker).
See [`k8s/README.md`](../k8s/README.md) for details.

### Reserved volume names

The following volume names in pod specs are matched by name in `start_sut()`:

| Volume name | Purpose | Removed when |
|---|---|---|
| `benchmark-storage-volume` | Mounts the per-experiment DBMS storage PVC | `use_storage=False` |
| `benchmark-data-volume` | Mounts the shared read-only dataset PVC (`bexhoma-data`) | `use_distributed_datasource=False` |
| `bxw` | Worker-node storage in StatefulSet `volumeClaimTemplates` | `use_storage=False` |
| `dshm` | Shared-memory `emptyDir` | Never removed |

### Service port names

`start_sut()` strips Service ports by name when monitoring is disabled.
Always name the DBMS connection port `port-dbms` so it is never stripped.

| Port name | Always kept |
|---|---|
| `port-dbms` | Yes |
| `port-bus` | Yes (cluster bus for distributed DBMSs) |
| `port-web` | Yes |
| `port-monitoring` | Stripped when monitoring inactive |
| `port-monitoring-application` | Stripped when app monitoring inactive |

### Server options via `--set`

`--set KIND[NAME](@CONFIG).container[C].PARAM=VALUE` changes one setting of a container in a Deployment or StatefulSet of the template.
How `PARAM` is written depends on the template:

| Style | Written as | Templates | Chosen by |
|---|---|---|---|
| `pg` | `["-c", "PARAM=VALUE"]` | PostgreSQL, PgDuckDB, Citus, PGBouncer backends | `-c` pairs in the args (default) |
| `flag` | `"--PARAM=VALUE"` | MySQL, MariaDB | annotation `bexhoma/arg-style: flag` on the workload, or `--x=y` elements in the args |
| env | env entry `PARAM=VALUE` | all | `PARAM` = `env.NAME`, e.g. Dragonfly `env.DFLY_maxmemory` |

An existing setting is replaced in place, a new one is appended.
In the `flag` style, `-` and `_` in names are equal (`innodb_buffer_pool_size` replaces `--innodb-buffer-pool-size=8G`).
Valueless flags (`--skip-log-bin`) cannot be set this way.
Flags inside `bash -c` command strings (CockroachDB, TiDB) and Helm values (YugabyteDB) are not reachable by `--set`.

Examples:
```bash
--set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=10G
--set statefulset[bexhoma-worker].container[dbms].env.DFLY_snapshot_cron="*/5 * * * *"
```

### Cluster SUTs: placement, sizing and scripts

**Placement.** `-rnn` pins the SUT pod (Deployment). `-rnw` pins the workers, i.e. every StatefulSet of the SUT (e.g. TiDB's PD and TiKV, CockroachDB's nodes), to a set of nodes joined by `+`, and spreads each StatefulSet evenly over them (`maxSkew: 1`).
`sut` stands for the `-rnn` node.
Commas sweep, one configuration per entry, paired by position with `-rc/-lc/-rr/-lr/-rst`:

```bash
-rnn cl-worker37 -rnw sut+cl-worker38+cl-worker39            # SUT pod and workers on three nodes
-rnw cl-worker37+cl-worker38,cl-worker39+cl-worker40        # two configurations
```

**Sizing.** `-rc/-rr/-lc/-lr` and `-rss` apply to the SUT pod and to the *data components* of a configuration.
By default all StatefulSets are data components.
A configuration can name them (`config.set_data_components(['tikv'])`); the other StatefulSets (TiDB's PD) then keep the resources and volume size of the template.
The storage class (`-rst`) applies to all volumes.
Per-component values win in both cases, e.g. `config.set_resources(requests_pd={'cpu': '500m'}, limits_pd={...}, storage_pd='20Gi')`.

**Placeholder SUT pods.** Where the SUT pod holds no data (entry point, client or helper pod: CockroachDB, Redis cluster, Dragonfly cluster, YugabyteDB, DatabaseService), the configuration sets `config.set_sut_role('placeholder')`.
That pod keeps the (small) resources of its template; `-rnn` still applies.
The summary reports what the whole SUT requests (`resources_total`: SUT pod plus all StatefulSets, times replicas).

**Scripts on workers.** Init, check and reset scripts run in the first SUT pod.
With `config.set_script_target('workers')` (Redis cluster, Dragonfly cluster), shell scripts (`.sh`, e.g. `save-snapshot.sh`) run in every worker pod instead; SQL scripts still run once through `loadData`.

**Post-load checks.** The last post-load script always runs, also for TPC-H and TPC-DS without `-xii/-xic/-xis` (key `Checks`): `checkschema-<benchmark>.sql` restores settings relaxed for the import (PostgreSQL `synchronous_commit`; MySQL settings saved in `bexhoma.saved_settings` before the load), writes a checkpoint (PostgreSQL, Citus) and reports row counts, sizes, the WAL/redo written by the load and the non-default configuration.

### Reset scripts (`-ar`)

With `-ar`, a reset runs before each benchmarking round (also before the first round after loading), for YCSB, Benchbase, HammerDB, TPC-H and TPC-DS.
It is off by default.
Every reset does the same steps in the same order, so rounds and systems start from comparable states:

1. **Statistics**: `VACUUM` / `ANALYZE` or the equivalent.
2. **Persist**: write dirty data to disk (`CHECKPOINT`, flush, `SAVE`), so that no checkpoint or flush left over from loading or the previous round falls into the measured round. It comes after step 1, because `VACUUM` dirties pages again.
3. **Counters**: zero the cumulative activity counters, so application metrics start at 0.

The reset does not make caches cold: a checkpoint writes dirty pages but keeps them in memory.
A step without an equivalent is a comment line `step N (...): n/a - <reason>` in the script; no other operation stands in for it.

| DBMS | 1 Statistics | 2 Persist | 3 Counters |
|---|---|---|---|
| PostgreSQL, PGBouncer, PgDuckDB | `VACUUM VERBOSE ANALYZE` (whole database) | `CHECKPOINT` | `pg_stat_reset()`, `pg_stat_reset_shared()` for `bgwriter`, `checkpointer`, `io`, `wal` |
| Citus | `VACUUM VERBOSE ANALYZE` on the distributed tables (passed on to the shards) | `CHECKPOINT` on the coordinator and with `run_command_on_workers` on every worker | as PostgreSQL, on the coordinator and every worker |
| MySQL, MariaDB | `ANALYZE TABLE` (`reset-<benchmark>.sql`) | `reset-flush.sh`: `innodb_max_dirty_pages_pct = 0`, wait until no dirty pages are left (at most 600 s), restore the old value | `FLUSH STATUS` (in `reset-flush.sh`) |
| CedarDB | `VACUUM VERBOSE ANALYZE` | n/a (no `CHECKPOINT`) | n/a (no `pg_stat_reset()`) |
| MonetDB | `ANALYZE` | n/a (the write-ahead log is applied in the background; no call to force it) | n/a |
| ClickHouse | n/a (no optimizer statistics unless declared per column) | `reset-flush.sh`: `sync` (an `INSERT` writes its parts without fsync) | n/a (`system.events` cannot be reset) |
| ClickHouseCluster | n/a | `SYSTEM FLUSH DISTRIBUTED` on every Distributed table and `SYSTEM SYNC REPLICA ON CLUSTER` on every replicated table (`reset-<benchmark>.sql`, coordinator), then `reset-flush.sh` (`sync`) in every worker | n/a |
| YugabyteDB | `ANALYZE VERBOSE` (cluster-wide) | n/a (no `CHECKPOINT` in YSQL, no `yb-admin` in the helper pod) | `reset-counters.sh`: `pg_stat_reset()` on every tserver (`yb-tserver-N.yb-tservers`), not once through the service, which picks one tserver per connection |
| CockroachDB | `ANALYZE` (cluster-wide) | n/a (Pebble flushes on its own) | `crdb_internal.reset_sql_stats()` (cluster-wide) |
| TiDB | `ANALYZE TABLE` (cluster-wide) | n/a (no flush in SQL) | `FLUSH STATUS` on the TiDB server the connection reaches |
| Dragonfly | n/a | `SAVE` on every data pod | `CONFIG RESETSTAT` |
| Redis | n/a | `SAVE` (standalone: SUT pod; cluster: every worker) | `CONFIG RESETSTAT` |

DatabaseService has no reset.
Benchbase `twitter`, `ycsb` and `chbenchmark` have a reset for PostgreSQL, PGBouncer and CedarDB only (the other DBMS have no scripts for them).
With `-ar` on a configuration without a reset, the experiment prints a warning at the start; a listed script missing in the experiment folder is skipped with a message.

Scripts are in the experiment folder of the DBMS (`experiments/<benchmark>/<DBMS>/`, Benchbase `experiments/benchbase/<benchmark>/<DBMS>/`), named `reset-<benchmark>.sql`, plus `reset-flush.sh` (MySQL, MariaDB, ClickHouse), `reset-counters.sh` (YugabyteDB) or `save-snapshot.sh` (Dragonfly, Redis).
SQL files run through `loadData` (once per tenant for database tenancy; once for schema tenancy, as the PostgreSQL scripts cover the whole database), shell files in the SUT pod or, with script target `workers`, in every worker pod.
With a TPC-H refresh stream (`-xrs`), the reset runs once per round, before both streams start.
Each reset is logged per round (`bexhoma-reset_<run>_<client>_<entry>-...log`), and its duration is reported as `reset_seconds`.
A script counts as failed when it exits non-zero, writes an error line (`ERROR`, `FATAL`) to stderr, or (redis-cli) an `ERR` reply to stdout; no output means success.
The summary's Reset table lists the failed scripts per job (`reset_failed`), and the test `Reset scripts ran without errors` fails when there are any; the agent report links the reset logs in `files.md`.
`scripts/test-docs-reset.sh` (`.ps1`) checks every reset on a cluster: one run per DBMS and benchmark with two rounds, and its header lists what to look for in the logs; see [Test: Reset Scripts](Test-Reset.md) for the commands and the logs of the last run.

Runs with `-ar` from before this contract (October 2026) are not directly comparable to newer ones for PostgreSQL (checkpoint now after `VACUUM`), Citus (checkpoints on the workers) and MySQL/MariaDB (dirty-page flush): these move I/O out of round 1.

### Load durability (`-xld`)

`-xld durable|relaxed|unsafe` (default `relaxed`) sets the durability during the load only; the benchmark runs with the configured state (template and `--set`).
Templates set no durability options.
Details and the placeholders `durability.sql` / `restoredurability.sql`: [Prepare Testbeds](Prepare-Testbeds.md).
Commands and logs of the test runs: [Test: Load Durability](Test-Durability.md).

| DBMS | durable | relaxed | unsafe |
|---|---|---|---|
| PostgreSQL, PgDuckDB, PGBouncer | `synchronous_commit`, `fsync`, `full_page_writes` on | `synchronous_commit=off` | also `fsync`, `full_page_writes` off; restore with `CHECKPOINT` + `sync` |
| Citus (coordinator + workers) | as PostgreSQL | `synchronous_commit=off` | - (= relaxed) |
| MySQL | flush 1 | flush 2 (TPC-C/YCSB 0), key checks off | also redo log off, doublewrite `DETECT_ONLY` |
| MariaDB (`.sh`, root) | flush 1, doublewrite on | flush 2 | also doublewrite off |
| others | - | - | - |

For a new DBMS: put `durability-<level>.sql`/`.sh` and `restoredurability-<level>.sql`/`.sh` next to its init scripts; the restore must return to the startup values, not to the defaults (MySQL/MariaDB save them in `bexhoma.saved_settings`).
PostgreSQL: a parameter set on the command line (`-c`, also from `--set`) cannot be changed by `ALTER SYSTEM`, so `-xld` has no effect on it.

### DDL parameters (`-xddl`)

`-xddl KEY=VALUE` fills a `{key}` placeholder in the init scripts of every DBMS of the run whose script folder declares the key in `ddl-parameters.config`; the other DBMS ignore it.
A comma list sweeps (`-xddl fillfactor=100,80`, one configuration per value), and `-xddl` can be repeated.
The default of a key reproduces the script without the parameter.
`Requires` means: the key may only leave its default if the other key has one of the listed values; this is checked before anything starts.
A sweep cannot be combined with persistent storage (`-rst`): a volume keeps the values it was loaded with (labels `ddl_<key>`), and a differing request fails the test `Data parameters as requested`.
In `experiment.yml` the catalog's keys are selected by `systems[].ddl`; there a sweep is also refused together with a resource sweep.
Keys that apply after loading need their step: `-xii` (indexes), `-xis` (statistics).

Each DBMS section below lists its keys.

### Minimal SUT template skeleton

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  labels: {app: bexhoma, component: sut, configuration: default, experiment: default}
  name: bexhoma-storage
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 50Gi
  storageClassName: shared
---
apiVersion: v1
kind: Service
metadata:
  labels: {app: bexhoma, component: sut, configuration: default, experiment: default}
  name: bexhoma-service
spec:
  ports:
  - {port: 9091, protocol: TCP, name: port-dbms, targetPort: 5432}
  selector: {app: bexhoma, component: sut, configuration: default, experiment: default}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels: {app: bexhoma, component: sut, configuration: default, experiment: default}
  name: bexhoma-deployment
spec:
  replicas: 1
  selector:
    matchLabels: {app: bexhoma, component: sut, configuration: default, experiment: default}
  template:
    metadata:
      labels: {app: bexhoma, component: sut, configuration: default, experiment: default}
    spec:
      containers:
      - name: dbms
        image: mydbms:latest
        ports:
        - {containerPort: 5432}
        volumeMounts:
        - {mountPath: /var/lib/mydbms/data, name: benchmark-storage-volume}
      volumes:
      - name: benchmark-storage-volume
        persistentVolumeClaim: {claimName: bexhoma-storage}
```

Copy [`k8s/deploymenttemplate-Dummy.yml`](../k8s/deploymenttemplate-Dummy.yml) as a starting point for a new DBMS.

---

## PostgreSQL

PostgreSQL is the primary test target for analytical benchmarks (TPC-H, TPC-DS) and transactional benchmarks (Benchbase TPC-C, YCSB).

**Deployment template:** [`k8s/deploymenttemplate-PostgreSQL.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-PostgreSQL.yml)

The default deployment uses a minimal, near-standard PostgreSQL configuration.
The only active startup argument is `max_connections=640`; all other parameters use PostgreSQL defaults.
The template includes an extensive set of **commented-out** tuning knobs (memory, parallelism, WAL, autovacuum, planner cost constants) as a reference — uncomment or override individual parameters at experiment time using `--set`.

**Configuration** (from `cluster.config`):

```python
'PostgreSQL': {
    'loadData': 'psql -U postgres -d {database} < {scriptname}',
    'delay_prepare': 0,
    'template': {
        'version': 'v11.4',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
        'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/{database}?reWriteBatchedInserts=true&currentSchema={schema}',
            'jar': 'postgresql-42.5.0.jar',
            'database': 'postgres',
            'schema': 'public',
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
    'monitor': {
        'sut': {
            'metrics': 'postgresql',
            'blackbox': True,
            'blackbox_target': 'postgres@localhost:5432/{database}?sslmode=disable',
        },
    },
},
```

The `database` and `schema` fields support multi-tenant mode: bexhoma substitutes the tenant-specific database or schema name when running schema-per-tenant or database-per-tenant experiments.

**DDL scripts:**
- [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/PostgreSQL)
- [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/PostgreSQL)
- [TPC-C](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcc/PostgreSQL)
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/PostgreSQL)

**DDL parameters** (`-xddl`, see [DDL parameters](#ddl-parameters-xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `index_method` | TPC-H | `btree`, `hash`, `brin` | `btree` | access method of the foreign key indexes (-xii) except the multicolumn index on lineitem, which stays a B-tree: hash indexes answer equality only, brin indexes are tiny but need physically ordered keys |
| `btree_dedup` | TPC-H | `on`, `off` | `on` | deduplication of B-tree index entries (-xii; PostgreSQL default on): shrinks non-unique foreign key indexes. Requires `index_method` = `btree` |
| `statistics_target` | TPC-H | integer | `100` | default_statistics_target of the database (-xis; PostgreSQL default 100): rows sampled and histogram size per column; plan quality vs. ANALYZE time |
| `extended_statistics` | TPC-H | `off`, `on` | `off` | multi-column statistics (-xis) on correlated columns of lineitem and part: the planner otherwise multiplies their selectivities |
| `fillfactor` | YCSB | integer | `100` | fillfactor of usertable (PostgreSQL default 100, allowed 10-100): free space per page lets updates stay on the page (HOT updates, see n_tup_hot_upd in pg_stat_user_tables) |
| `autovacuum_scale` | YCSB | `0.2`, `0.1`, `0.05`, `0.01` | `0.2` | autovacuum_vacuum_scale_factor of usertable (PostgreSQL default 0.2): share of dead rows that starts an autovacuum; lower values vacuum earlier in update-heavy runs (see autovacuum_count in pg_stat_user_tables) |

PgDuckDB uses the TPC-H keys (it runs these scripts), PGBouncer the YCSB keys.

---

## PGBouncer

`PGBouncer` is the configuration key for a PostgreSQL deployment fronted by a **PgBouncer connection pool**.
The SUT component runs PostgreSQL; the pool component runs PgBouncer.
Benchmarker pods connect to PgBouncer, which multiplexes connections to PostgreSQL.

This configuration is used to benchmark the overhead and benefit of connection pooling compared to direct PostgreSQL access.
See [Example: PGBouncer](Example-PGBouncer.md) for a worked example.

**Deployment template:** [`k8s/deploymenttemplate-PGBouncer.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-PGBouncer.yml)

**Configuration** (from `cluster.config`):

```python
'PGBouncer': {
    'loadData': 'psql -U postgres -d {database} < {scriptname}',
    'delay_prepare': 0,
    'template': {
        'version': 'v11.4',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
        'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/{database}?reWriteBatchedInserts=true',
            'jar': 'postgresql-42.5.0.jar',
            'database': 'postgres',
            'schema': 'public',
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery for both the sut (postgres_exporter) and pool (pgbouncer_exporter) components
},
```

The `monitor` section uses Kubernetes pod discovery to scrape both the PostgreSQL exporter (port 9187 on the SUT pods) and the PgBouncer exporter (port 9127 on the pool pods).

PGBouncer uses the same DDL scripts as PostgreSQL — see the PostgreSQL section above.

---

## MySQL

MySQL is supported for TPC-H and YCSB experiments.
The default image runs MySQL 9.7 (LTS).
MySQL 9 has no `mysql_native_password`; `root@'%'` uses `caching_sha2_password`, whose first login needs TLS or the server's RSA key.
bexhoma therefore creates a TLS Secret per SUT (see `'tls'` in the configuration) and mounts it into MySQL and the HammerDB jobs.

**Deployment template:** [`k8s/deploymenttemplate-MySQL.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MySQL.yml)

The template sets the server options as `--key=value` arguments (e.g. `--innodb-buffer-pool-size=8G`); change them per run with `--set ...container[dbms].innodb_buffer_pool_size=32G`.
The buffer pool of 8G fits the default pod size (`-rr 16Gi`; the namespace sets the memory limit equal to the request when `-lr` is not given). bexhoma does not adapt it to `-rr`/`-lr`: give larger pods a larger pool with `--set`. Until 2026-10-22 the template had 96G, which was OOM-killed in a 16Gi pod as soon as the data filled it (TPC-H SF 10).
The template sets no durability options: MySQL runs crash-safe by default (`innodb_flush_log_at_trx_commit=1`, doublewrite on); relax the benchmark per run with `--set ...container[dbms].innodb_flush_log_at_trx_commit=2`.
Load durability (`-xld`): see [Load durability](#load-durability--xld). Doublewrite cannot be switched between on and off at runtime in MySQL, so with `--set ...innodb_doublewrite=OFF` it stays off during an `-xld durable` load.
The `initconstraints` scripts (TPC-H, TPC-DS) add the foreign keys with `SET SESSION foreign_key_checks = 0`, as for MariaDB: with checks on, MySQL validates every row and its memory grew past 16 GB while adding lineitem->orders at TPC-H SF 1 (OOM-killed, 2026-10-21).
See the [MySQL 9.7 documentation](https://dev.mysql.com/doc/refman/9.7/en/) for parameter explanations.

**Configuration** (from `cluster.config`):

```python
'MySQL': {
    'loadData': 'mysql --local-infile {database} < {scriptname}',
    'delay_prepare': 120,
    'template': {
        'version': 'CE 8.0.36',
        'alias': 'General-C',
        'docker_alias': 'GP-C',
        'dialect': 'MySQL',
        'JDBC': {
            'driver': "com.mysql.cj.jdbc.Driver",
            'auth': ["root", "root"],
            'url': 'jdbc:mysql://{serverip}:9091/{dbname}?rewriteBatchedStatements=true',
            'jar': ['mysql-connector-j-8.0.31.jar', 'slf4j-simple-1.7.21.jar'],
            'database': 'mysql',  # placeholder — must be overwritten per experiment
        }
    },
    'logfile': '/var/log/mysqld.log',
    'datadir': '/var/lib/mysql/',
    'priceperhourdollar': 0.0,
    'monitor': {
        'sut': {
            'metrics': 'mysql',
            'blackbox': False,
        },
    },
},
```

`delay_prepare: 120` makes bexhoma wait 2 minutes before querying the DBMS.
This accounts for InnoDB's buffer pool initialisation, which can cause a brief restart.

**DDL scripts:**
- [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MySQL)
- [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/MySQL)
- [TPC-C](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcc/MySQL)
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/MySQL)

**DDL parameters** (`-xddl`, see [DDL parameters](#ddl-parameters-xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `histograms` | TPC-H | `off`, `on` | `off` | column histograms (ANALYZE TABLE ... UPDATE HISTOGRAM, 100 buckets) on all columns except primary keys and comments, in initstatistics (-xis): selectivity of filters on columns without an index; off: plain ANALYZE TABLE (index statistics only) |
| `stats_sample_pages` | TPC-H | `default`, `100`, `1000` | `default` | pages sampled per index by ANALYZE TABLE on each table (default: innodb_stats_persistent_sample_pages, 20): plan quality vs. ANALYZE time |
| `row_format` | YCSB | `DYNAMIC`, `COMPRESSED` | `DYNAMIC` | InnoDB row format of usertable (MySQL default DYNAMIC): COMPRESSED stores pages zlib-compressed (KEY_BLOCK_SIZE 8): less I/O, more CPU, the buffer pool may hold both copies of a page |
| `collation` | YCSB | `utf8mb4_0900_ai_ci`, `utf8mb4_bin`, `latin1` | `utf8mb4_0900_ai_ci` | character set and collation of usertable: cost of comparing the VARCHAR(255) key (binary vs. linguistic) and bytes per character |

---

## MariaDB

MariaDB is supported for TPC-H, Benchbase TPC-C, HammerDB TPC-C, and YCSB experiments.
It uses a dedicated `bexhoma` database user rather than `root`.

**Deployment template:** [`k8s/deploymenttemplate-MariaDB.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MariaDB.yml)

The default deployment sets the I/O threads, `innodb-log-buffer-size=1G`, temporary table sizes and `innodb-buffer-pool-size=8G`.
As for MySQL, the 8G pool fits the default pod size (`-rr 16Gi`); give larger pods a larger pool with `--set ...container[dbms].innodb_buffer_pool_size=32G`.

**Configuration** (from `cluster.config`):

```python
'MariaDB': {
    'loadData': 'mariadb --user=bexhoma --password=password < {scriptname}',
    'template': {
        'version': 'v10.4.6',
        'alias': 'General-A',
        'docker_alias': 'GP-A',
        'dialect': 'MySQL',
        'JDBC': {
            'driver': "org.mariadb.jdbc.Driver",
            'auth': ["bexhoma", "password"],
            'url': 'jdbc:mariadb://{serverip}:9091/{dbname}?rewriteBatchedStatements=true',
            'jar': 'mariadb-java-client-3.1.0.jar',
            'database': 'mariadb',  # placeholder — must be overwritten per experiment
        },
        'init_SQL': "SET optimizer_switch = 'mrr=on,mrr_cost_based=off'",
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/mysql/',
    'priceperhourdollar': 0.0,
},
```

The `init_SQL` statement is executed after each connection is established and enables multi-range read optimisation.

**DDL scripts:**
- [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MariaDB)
- [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/MariaDB)
- [TPC-C](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcc/MariaDB)
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/MariaDB)

**DDL parameters** (`-xddl`, see [DDL parameters](#ddl-parameters-xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `histograms` | TPC-H, TPC-DS, SSB | `off`, `on` | `off` | engine-independent statistics with histograms (ANALYZE TABLE ... PERSISTENT FOR ALL, JSON_HB, a full scan per table) in initstatistics (-xis); off: plain ANALYZE TABLE, which collects none (use_stat_tables = PREFERABLY_FOR_QUERIES, MariaDB 12.3) |
| `engine` | TPC-H | `InnoDB`, `Aria`, `MyISAM` | `InnoDB` | storage engine of all tables (ColumnStore needs an image with the plugin, not listed) |
| `row_format` | YCSB | `default`, `DYNAMIC`, `COMPRESSED` | `default` | InnoDB row format of usertable (default: innodb_default_row_format, DYNAMIC): COMPRESSED stores pages zlib-compressed: less I/O, more CPU |
| `collation` | YCSB | `default`, `utf8mb4_bin`, `latin1` | `default` | character set and collation of usertable (default: the database default): cost of comparing the VARCHAR(255) key (binary vs. linguistic) and bytes per character |

---

## MonetDB

MonetDB is a column-store DBMS well-suited for TPC-H analytical workloads.

**Deployment template:** [`k8s/deploymenttemplate-MonetDB.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MonetDB.yml)

**Configuration** (from `cluster.config`):

```python
'MonetDB': {
    'loadData': "cd /home/monetdb;printf 'user=monetdb\npassword=monetdb\n' > .monetdb;mclient demo < {scriptname}",
    'template': {
        'version': '11.37.11',
        'alias': 'Columnwise',
        'docker_alias': 'Columnwise',
        'JDBC': {
            'auth': ['monetdb', 'monetdb'],
            'driver': 'org.monetdb.jdbc.MonetDriver',
            'jar': 'monetdb-jdbc-12.2.jre8.jar',
            'url': 'jdbc:monetdb://{serverip}:9091/demo?so_timeout={timeout_ms}',
            'database': 'demo',
        }
    },
    'logfile': '/var/monetdb5/dbfarm/merovingian.log',
    'datadir': '/var/monetdb5/',
    'priceperhourdollar': 0.0,
},
```

The `loadData` command first writes a `.monetdb` credentials file into the container home directory before piping the script to `mclient`.

**DDL scripts:**
- [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MonetDB)
- [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/MonetDB)

---

## Citus

Citus is a distributed extension for PostgreSQL that shards tables across worker nodes.
The coordinator node is deployed as the SUT; worker nodes are deployed as a StatefulSet.
After each worker pod starts, bexhoma runs the `attachWorker` command on the coordinator to register it.

**Deployment template:** [`k8s/deploymenttemplate-Citus.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Citus.yml)

The template uses the Debian image `citusdata/citus:14.2.0` (PostgreSQL 18), not `-alpine`: `14.2.0-alpine` fails about 5 % of TPC-C New Order transactions with `could not append to file: Not supported`.
Coordinator and workers set `PGDATA=/var/lib/postgresql/data/pgdata`; PostgreSQL 18 images otherwise use `/var/lib/postgresql/18/docker` and refuse a volume mounted at `/var/lib/postgresql/data`.

**Configuration** (from `cluster.config`):

```python
'Citus': {
    'loadData': 'psql -U postgres < {scriptname}',
    'attachWorker': "psql -U postgres --command=\"SELECT * from master_add_node('{worker}.{service_sut}', 5432);\"",
    'template': {
        'version': '10.0.2',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
        'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", "postgres"],
            'url': 'jdbc:postgresql://{serverip}:9091/postgres?loadBalanceHosts=true',
            'jar': 'postgresql-42.5.0.jar',
            'database': 'postgres',
            'schema': 'public',
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
},
```

**DDL scripts:**
- [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/Citus)
- [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/Citus)
- [TPC-C](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcc/Citus)
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Citus)

TPC-H and SSB distribute the fact tables (`orders`/`lineitem`, `lineorder`) by the order key; the dimensions are reference tables, a full copy on every worker.
SSB can distribute the dimensions by their own key instead (`-xdim distributed`, scripts in `Citus/distributed`); then a join with `lineorder` is a repartition join.
TPC-H refuses `-xdim distributed` for Citus: with distributed dimensions Citus could not plan 12 of the 22 queries (joins that are not co-located, subqueries, a cartesian product; check 2026-10-30).

See [Example: Citus](Example-Citus.md) for a worked example.

**DDL parameters** (`-xddl`, see [DDL parameters](#ddl-parameters-xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `num_worker_shards` | TPC-H, SSB, YCSB, BenchBase TPC-C | integer | `32` | citus.shard_count of the tables distributed by warehouse (Citus default 32) |
| `tpcc_item` | BenchBase TPC-C | `reference`, `distributed` | `reference` | placement of the read-only item table: a copy on every worker, or spread by i_id, so that New-Order reads items remotely |
| `columnar_compression` | TPC-H | `default`, `none`, `lz4`, `zstd`, `pglz` | `default` | compression of the columnar orders and lineitem (-xcol only; default: columnar.compression of the server, zstd): bytes read vs. CPU per scan |
| `num_worker_replicas` | YCSB | integer | `1` | citus.shard_replication_factor of usertable (Citus default 1) |
| `fillfactor` | YCSB | integer | `100` | fillfactor of usertable and its shards (PostgreSQL default 100, allowed 10-100): free space per page lets updates stay on the page (HOT updates) |

`columnar_compression` applies only with `-xcol`.

---

## ClickHouse

ClickHouse is a column-store DBMS for analytical workloads (TPC-H, TPC-DS).

**Deployment template:** [`k8s/deploymenttemplate-ClickHouse.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-ClickHouse.yml)

The template uses the official image `clickhouse/clickhouse-server:26.8.34.13` (LTS).
Clients use the HTTP interface (JDBC, service port 9091 → 8123); loaders and init scripts use the native protocol (`clickhouse-client`, port 9000, service port `port-sut-native`).
`CLICKHOUSE_SKIP_USER_SETUP=1` keeps user `default` without password and with network access; without it the image restricts `default` to localhost.
Instead of `privileged`, the container gets the capabilities `SYS_NICE`, `IPC_LOCK` and `NET_ADMIN` (thread priorities, mlock, per-query OS metrics).

At start, the container writes two files:
- `config.d/bexhoma.xml`: ClickHouse's own Prometheus endpoint on port 9363 (application metrics, `-ma`).
- `users.d/bexhoma.xml`: settings of profile `default` for SQL-standard results, which the queries of TPC-H and TPC-DS rely on.

| Setting | Value | Without it |
|---|---|---|
| `join_use_nulls` | 1 | an outer join fills unmatched columns with 0 or `''` instead of NULL (wrong counts in TPC-H Q13) |
| `union_default_mode` | `DISTINCT` | a plain `UNION` is a syntax error |
| `cast_keep_nullable` | 1 | `CAST` of a NULL fails |
| `allow_lossy_numeric_supertype` | 1 | `CASE`/`COALESCE` over Decimal and Float has no common type |

`prefer_column_name_to_alias` is not set: it would also apply to `ORDER BY`, where standard SQL resolves the alias of the select list first.

**Schema** ([TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/ClickHouse), [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/ClickHouse)):
tables are MergeTree in database `default`; the sorting key is the primary key of the benchmark, which also is ClickHouse's sparse primary index.
There are no secondary indexes, constraints or statistics, so `-xii`, `-xic` and `-xis` have no scripts.
CHAR/VARCHAR are `String` (`FixedString` pads with `\0`, not blanks).
TPC-DS columns without `NOT NULL` are `Nullable` (empty fields load as NULL), dates are `Date32` (TPC-DS dates start in 1900).
The loaders (`bexhoma/loader_tpch_clickhouse`, `bexhoma/loader_tpcds_clickhouse`) send each flat file with `INSERT INTO <table> FORMAT CSV` (delimiter `|`, double quotes are data).

**Queries:** the variants for ClickHouse have the key `Clickhouse` in the query files (selected by `dialect` and by the connection name).
They are needed where ClickHouse differs from standard SQL (identifier case, the name of a selected `t.col` is `t.col`, `ORDER BY` after a parenthesized `UNION`, an alias visible in its own select list) and for correlated subqueries, which ClickHouseCluster cannot run.
Every variant returns the same result as the original query on ClickHouse.

**Configuration** (from `cluster.config`):

```python
'ClickHouse': {
    'loadData': 'clickhouse-client --multiquery < {scriptname}',
    'template': {
        'version': '26.8',
        'alias': 'Columnwise-B',
        'docker_alias': 'Columnwise-B',
        'dialect': 'Clickhouse',
        'JDBC': {
            'auth': ['default', ''],
            'driver': 'com.clickhouse.jdbc.Driver',
            'jar': 'clickhouse-jdbc-0.11.0-all-dependencies.jar',
            'url': 'jdbc:clickhouse://{serverip}:9091/default',
            'database': 'default',
            'explain': ['EXPLAIN {query}'],
        }
    },
    'logfile': '/var/log/clickhouse-server/clickhouse-server.log',
    'datadir': '/var/lib/clickhouse/',
    'priceperhourdollar': 0.0,
    'monitor': {'sut': {'metrics': 'clickhouse', 'discovery': True, ...}},
},
```

```bash
bexhoma tpch -dbms ClickHouse -sf 1 -nlp 8 -tr run
```

See [Example: ClickHouse](Example-ClickHouse.md) for a worked example.

**DDL parameters** (`-xddl`, see [DDL parameters](#ddl-parameters-xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `order_orders` | TPC-H | `key`, `date` | `key` | sort key (= primary index) of orders: by key, or by date first so date ranges (Q3-Q5, Q7-Q10, Q12) skip granules |
| `order_lineitem` | TPC-H | `key`, `date` | `key` | sort key (= primary index) of lineitem: by key, or by ship date first so date ranges (Q1, Q6, Q7, Q14, Q15, Q20) skip granules |
| `partition_orders` | TPC-H | `none`, `year`, `month` | `none` | partitions of orders by order date: queries with a date range skip whole partitions; more partitions mean more parts per insert block |
| `partition_lineitem` | TPC-H | `none`, `year`, `month` | `none` | partitions of lineitem by ship date: queries with a ship date range (Q1, Q6, Q14, Q15, Q20) skip whole partitions; more partitions mean more parts per insert block |
| `index_granularity` | TPC-H | integer | `8192` | rows per granule (= entry of the sparse primary index) of orders and lineitem (ClickHouse default 8192): smaller granules skip more precisely, the index grows |
| `wide_parts` | TPC-H | `default`, `wide`, `compact` | `default` | part format of orders and lineitem by min_bytes_for_wide_part: default (10 MiB: small parts compact, one file; larger parts wide, a file per column), wide (every part), compact (every part up to 1 TiB); parallel loaders write many small parts |
| `low_cardinality` | TPC-H | `off`, `on` | `off` | dictionary encoding of the string columns with few distinct values (flags, modes, priorities, segments, brands, types, containers, nation and region names): faster filters and GROUP BY |
| `codec` | TPC-H | `default`, `zstd1`, `zstd3` | `default` | compression of all columns of orders and lineitem (default: the server setting, LZ4): bytes read vs. CPU per scan |

---

## ClickHouseCluster

A ClickHouse cluster of one coordinator (the SUT) and `-nw` shards (worker StatefulSet, one replica per shard), for TPC-H and TPC-DS.

**Deployment template:** [`k8s/deploymenttemplate-ClickHouseCluster.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-ClickHouseCluster.yml)

Image, ports, capabilities and settings as [ClickHouse](#clickhouse); in addition:
- At start, every pod writes the cluster `bexhoma` (`remote_servers`, one shard per worker, from `BEXHOMA_WORKER_LIST_SPACE`).
- The coordinator is not a shard. It is the entry point of clients and loaders and runs a single-node ClickHouse Keeper (port 9181, service port `port-sut-keeper`), which `ON CLUSTER` statements need; the workers reach it through the SUT service.
- The coordinator sets `distributed_product_mode = global`: a Distributed table inside a join or `IN` is read once and sent to all shards, which is correct whatever the sharding keys are.
- A worker is ready when it has a session with the Keeper (readiness probe on `system.zookeeper`); bexhoma runs the init scripts only after all workers are ready. Workers start before the Keeper and retry every 5 s, so with `/ping` as probe the first `ON CLUSTER` statement would time out.
- Workers set the macros `{shard}` (pod ordinal) and `{replica}` (pod name) for later `ReplicatedMergeTree` setups.

**Schema** ([TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/ClickHouseCluster), [TPC-DS](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds/ClickHouseCluster)):
a distributed table is a MergeTree table `<name>_local` on every shard (`ON CLUSTER bexhoma`, columns and sorting key as ClickHouse) and a Distributed table `<name>` on the coordinator and on every shard (the parts of a distributed query that name a table resolve it there); rows are spread by the first column of the sorting key.
A replicated table is a `ReplicatedMergeTree` on every shard and on the coordinator, all replicas of one table; Keeper copies the parts the loader writes on the coordinator to the shards.
TPC-DS: every table is distributed.
TPC-H: `orders` and `lineitem` are distributed; `part`, `partsupp`, `supplier` and `customer` are replicated (`-xdim replicated`, default, so joins with `orders`/`lineitem` run on each shard against its local copy) or distributed (`-xdim distributed`, scripts in `ClickHouseCluster/distributed`, volume `tpch-distributed-<SF>`); `nation` and `region` are replicated in both.
The loader writes into the tables on the coordinator; a Distributed table uses `distributed_foreground_insert=1`, so the load time includes sending the rows to the shards.
The check script waits for the replicas, fails if a node holds other rows of a replicated table than the coordinator, and reports rows, parts and sizes per table and node.

The configuration equals ClickHouse plus `'attachWorker': ''` (the shards are in `remote_servers`, nothing to register) and the monitor component `worker`, which scrapes coordinator and shards (the metrics are totals of the cluster).
In `tpch.py` and `tpcds.py` the configuration sets `set_script_target('workers')`, so the reset's `reset-flush.sh` runs in every worker.

```bash
bexhoma tpch -dbms ClickHouseCluster -nw 3 -sf 1 -nlp 8 -tr run
```

See [Example: ClickHouse](Example-ClickHouse.md#clickhouse-as-a-cluster) for a worked example.

**DDL parameters** (`-xddl`, see [DDL parameters](#ddl-parameters-xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `order_orders` | TPC-H | `key`, `date` | `key` | sort key (= primary index) of orders: by key, or by date first so date ranges (Q3-Q5, Q7-Q10, Q12) skip granules |
| `order_lineitem` | TPC-H | `key`, `date` | `key` | sort key (= primary index) of lineitem: by key, or by ship date first so date ranges (Q1, Q6, Q7, Q14, Q15, Q20) skip granules |
| `partition_orders` | TPC-H | `none`, `year`, `month` | `none` | partitions of orders by order date: queries with a date range skip whole partitions; more partitions mean more parts per insert block |
| `partition_lineitem` | TPC-H | `none`, `year`, `month` | `none` | partitions of lineitem by ship date: queries with a ship date range (Q1, Q6, Q14, Q15, Q20) skip whole partitions; more partitions mean more parts per insert block |
| `index_granularity` | TPC-H | integer | `8192` | rows per granule (= entry of the sparse primary index) of orders and lineitem (ClickHouse default 8192): smaller granules skip more precisely, the index grows |
| `wide_parts` | TPC-H | `default`, `wide`, `compact` | `default` | part format of orders and lineitem by min_bytes_for_wide_part: default (10 MiB: small parts compact, one file; larger parts wide, a file per column), wide (every part), compact (every part up to 1 TiB); parallel loaders write many small parts |
| `low_cardinality` | TPC-H | `off`, `on` | `off` | dictionary encoding of the string columns with few distinct values (flags, modes, priorities, segments, brands, types, containers, nation and region names): faster filters and GROUP BY |
| `codec` | TPC-H | `default`, `zstd1`, `zstd3` | `default` | compression of all columns of orders and lineitem (default: the server setting, LZ4): bytes read vs. CPU per scan |

The dimension placement of TPC-H is `-xdim`, see above.

---

## CedarDB

CedarDB is an HTAP DBMS with a PostgreSQL wire protocol, the commercial successor of TUM's Umbra (TPC-H, SSB, YCSB, Benchbase).

**Deployment template:** [`k8s/deploymenttemplate-CedarDB.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-CedarDB.yml)

The template pins the Community Edition image `cedardb/cedardb:v2026-10-22`.
It differs from a PostgreSQL template in these points:

| Point | Handling | Without it |
|---|---|---|
| Password | `CEDAR_PASSWORD` has at least 20 characters, as the JDBC `auth` of `cluster.config`; letters and digits only, it goes through `sed` in the YCSB and Benchbase images | the image refuses a weak password and the server stops |
| Authentication | no trust authentication: `client_env` of `cluster.config` gives every job `PGPASSWORD` | the `psql` of the loader images cannot connect |
| Address | the entrypoint binds to `::`; the container command changes it to `0.0.0.0` before the start | no IPv6 in the pods, the server stops; `-address` as an argument is refused as given twice |
| `psql` | the image has none; the initContainer `include-client` copies it from `postgres:18.6` to `/pgclient` for `loadData` | init scripts cannot run |

Memory and threads follow the limits of the container: `buffersize` and `workmemsize` default to 45% of the memory limit each.
CedarDB warns that the `memlock` limit is too low for its `io_uring` buffers (performance may degrade); this limit cannot be changed from a pod.

**Community Edition:** free, at most 64 GiB of data; above that the database is read-only.
TPC-H is about 1.3 GiB per scale factor including indexes, so SF30 fits and SF100 does not (there is no SF100 script).
The [terms](https://cedardb.com/legal/agreements/community_tcs.pdf) allow no passing on of the software, so bexhoma does not build a derived image.

**Schema** ([TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/CedarDB), [SSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ssb/CedarDB), [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/CedarDB)):
the statements of PostgreSQL, in schema `public`.
The loaders are those of PostgreSQL; `\COPY` accepts the trailing `|` of the TPC-H files.
TPC-H uses dialect `CedarDB`: Q8, Q10 and Q15 have a variant with `date '...'`, as CedarDB has no function `date(text)`; the other queries are the main text.

CedarDB does not share code with PostgreSQL. What the scripts cannot use:

| Not available | Consequence |
|---|---|
| `CHECKPOINT` | no persist step in `checkschema` and the reset |
| settable `synchronous_commit`, `fsync` | `-xld` has no effect, there are no durability scripts |
| `pg_stat_reset()` | no counters step in the reset |
| `query_to_xml`, `pg_stat_wal`, `pg_stat_bgwriter` | `checkschema` lists the tables itself |

Isolation: every transaction runs as repeatable read. `READ COMMITTED` is accepted but stays repeatable read, `SERIALIZABLE` is refused, so Benchbase runs on repeatable read here.
With concurrent writes to the same rows, transactions fail with `conflict with concurrent transaction` instead of waiting.
YCSB does not retry them: workload A lost about 0.4% of its updates at 16 threads (`[UPDATE-FAILED]`), so the test `Execution Phase: contains FAILED column` fails.

Benchbase `twitter` loads, but its benchmark stops when it connects: the PostgreSQL profile of the image fixes `TRANSACTION_SERIALIZABLE` for it and ignores `BENCHBASE_ISOLATION`.

CH-benCHmark runs, but `num_errors` is not 0 and no bexhoma test reports it; the SQL comes from Benchbase:
- Q22 always fails: `GROUP BY substring(c_state from 1 for 1)` and `ORDER BY substring(c_state,1,1)` are not the same expression for CedarDB.
- Q15 fails when terminals overlap: all create the same view (`Catalog object was concurrently created`).

CedarDB has no Prometheus endpoint in bexhoma (`-ma`).

```bash
bexhoma tpch -dbms CedarDB -sf 1 -nlp 8 -xii -xic -xis -tr run
```

See [Example: Other DBMS](Example-Other-DBMS.md#cedardb) for the workloads and the test script.

## YugabyteDB

YugabyteDB is a distributed, PostgreSQL-compatible DBMS.
It consists of master and tablet-server (TServer) components, both deployed as StatefulSets.
The JDBC connection targets the TServer service.

**Configuration** (from `cluster.config`):

```python
'YugabyteDB': {
    'loadData': 'psql -U yugabyte --host yb-tserver-service.{namespace}.svc.cluster.local --port 5433 < {scriptname}',
    'template': {
        'version': 'v2.17.1',
        'alias': 'Cloud-Native-1',
        'docker_alias': 'CN1',
        'JDBC': {
            'driver': "com.yugabyte.Driver",
            'auth': ["yugabyte", ""],
            'url': 'jdbc:yugabytedb://yb-tserver-service.{namespace}.svc.cluster.local:5433/yugabyte?load-balance=true',
            'jar': 'jdbc-yugabytedb-42.3.5-yb-2.jar',
            'database': 'yugabyte',
            'schema': 'public',
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery for yb-master (port 7000) and yb-tserver (port 9000) pods
},
```

The monitoring section configures Kubernetes pod discovery for both the master component (port 7000) and the TServer component (port 9000), scraping YugabyteDB's native Prometheus endpoint at `/prometheus-metrics`.

YugabyteDB itself is installed by Helm (chart `2025.2.7`, see `Install-YugabyteDB` / `install_yugabytedb` in `scripts/test-docs-yugabytedb.*`, with parameters for persistence, storage class, volumes per tserver and nodes); the bexhoma SUT pod is a placeholder helper.
With persistent storage the chart adds a liveness probe (a disk check); its timeout is the chart's root key `livenessProbe.timeoutSeconds` (per-component keys are ignored).
The storage metrics include the tserver volumes (`config.set_pvc_selector('app=yb-tserver')`); `volume_used`/`volume_size` still come from the helper pod.

**DDL scripts:**
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/YugabyteDB)

See [Example: YugabyteDB](Example-YugaByteDB.md) for a worked example.

**DDL parameters** (`-xddl`, see [DDL parameters](#ddl-parameters-xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `pk_sharding` | YCSB | `hash`, `asc` | `hash` | sharding of the primary key: hash spreads load evenly and suits point reads, asc keeps key order for range scans (workload e) but concentrates ordered inserts |
| `num_tablets` | YCSB | `auto`, `4`, `8`, `16`, `32`, `64`, `128` | `auto` | tablets of usertable from the start (auto: ysql_num_shards_per_tserver and automatic splitting); only with pk_sharding=hash (asc needs SPLIT AT VALUES). Requires `pk_sharding` = `hash` |

---

## CockroachDB

CockroachDB is a distributed, PostgreSQL wire-compatible DBMS.
Worker nodes form the CockroachDB cluster; bexhoma registers each worker via the `attachWorker` command.
The PostgreSQL JDBC driver is used for connectivity.

**Configuration** (from `cluster.config`):

```python
'CockroachDB': {
    'loadData': 'cockroach sql --host {service_name} --port 9091 --insecure --file {scriptname}',
    'delay_prepare': 120,
    'attachWorker': "",  # CockroachDB auto-discovers cluster members
    'template': {
        'version': 'v24.2.4',
        'alias': 'Cloud-Native-2',
        'docker_alias': 'CN2',
        'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["root", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/defaultdb?reWriteBatchedInserts=true&sslmode=disable',
            'jar': 'postgresql-42.5.0.jar',
            'database': 'defaultdb',
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/cockroach/cockroach-data',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery for worker pods at /_status/vars on port 8080
},
```

The monitoring section scrapes CockroachDB's built-in Prometheus endpoint (`/_status/vars`, port 8080) from all worker pods.

**DDL scripts:**
- [TPC-C](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcc/CockroachDB)
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/CockroachDB)

See [Example: CockroachDB](Example-CockroachDB.md) for a worked example.

**DDL parameters** (`-xddl`, see [DDL parameters](#ddl-parameters-xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `num_worker_replicas` | YCSB | integer | `3` | zone num_replicas of usertable (CockroachDB default 3) |
| `pk_hash` | YCSB | `hash`, `none` | `hash` | hash-sharded primary key: spreads sequential inserts (-xio ordered) over ranges, costs range scans (workload e) |
| `bucket_count` | YCSB | `default`, `4`, `8`, `16`, `32`, `64` | `default` | buckets of the hash-sharded primary key (default: cluster setting sql.defaults.default_hash_sharded_index_bucket_count, 16 in v24.2): write spread vs. scan fan-out. Requires `pk_hash` = `hash` |
| `range_max_bytes` | YCSB | `default`, `64MiB`, `128MiB`, `256MiB` | `default` | zone range_max_bytes of usertable (default 512 MiB, range_min_bytes 128 MiB; a smaller value sets range_min_bytes to a quarter): more, smaller ranges spread leaseholders at small data sizes |
| `column_families` | YCSB | `one`, `per_field` | `one` | column families of usertable: one family per row, or one per field, so updating one field writes one KV pair instead of the whole row (workloads a, b, f); costs reads of whole rows |
| `pre_split` | YCSB | `none`, `9`, `90` | `none` | ranges of usertable before the load, split at the first digits of the YCSB keys (hashed insert order): avoids splitting and rebalancing during the load; a hash-sharded key has its buckets instead. Requires `pk_hash` = `none` |

---

## TiDB

TiDB is a distributed, MySQL-compatible DBMS.
It consists of three components: the TiDB SQL layer (SUT), TiKV storage nodes (worker), and the Placement Driver (PD) coordinator.
All three are deployed and monitored separately.

**Configuration** (from `cluster.config`):

```python
'TiDB': {
    'loadData': 'mysql -P 4000 -h 127.0.0.1 -D {database} --local-infile < {scriptname}',
    'delay_prepare': 60,
    'template': {
        'version': 'CE 8.0.22',
        'alias': 'General-C',
        'docker_alias': 'GP-C',
        'dialect': 'MySQL',
        'JDBC': {
            'driver': "com.mysql.cj.jdbc.Driver",
            'auth': ["root", "root"],
            'url': 'jdbc:mysql://{serverip}:9091/{dbname}?rewriteBatchedStatements=true',
            'jar': ['mysql-connector-j-8.0.31.jar', 'slf4j-simple-1.7.21.jar'],
            'database': 'test',
        }
    },
    'logfile': '/var/log/mysqld.log',
    'datadir': '/var/lib/mysql/',
    'priceperhourdollar': 0.0,
    'worker_port': 2379,
    'store_args': False,
    'monitor': { ... },  # Prometheus discovery for tidb (port 9500), pd (port 2379), and tikv (port 20180) pods
},
```

`store_args: False` suppresses capturing TiDB's verbose startup arguments in the summary.
Only TiKV is a data component (`config.set_data_components(['tikv'])`): `-rc/-rr/-lc/-lr` and `-rss` size TiKV and the SQL pod, while PD keeps the template's resources (0.25-1 CPU, 0.5-2 GiB) and volume size (10Gi).
`worker_port: 2379` is the PD headless service port used internally for cluster coordination.
The monitoring section scrapes all three components via Kubernetes pod discovery.

**DDL scripts:**
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/TiDB)

See [Example: TiDB](Example-TiDB.md) for a worked example.

**DDL parameters** (`-xddl`, see [DDL parameters](#ddl-parameters-xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `num_worker_replicas` | YCSB, BenchBase TPC-C | integer | `3` | PD max-replicas (TiDB default 3) |
| `clustered` | YCSB | `default`, `clustered`, `nonclustered` | `default` | clustered index of usertable (default: tidb_enable_clustered_index of the server); clustered saves a lookup, nonclustered stores rows by a hidden _tidb_rowid |
| `split_regions` | YCSB | `none`, `4`, `8`, `16`, `32`, `64`, `128` | `none` | regions of usertable on all TiKV nodes before the load, over the YCSB key range user0..user9; needs a clustered key (nonclustered rows are stored by the integer _tidb_rowid, which SHARD_ROW_ID_BITS spreads instead). PRE_SPLIT_REGIONS needs SHARD_ROW_ID_BITS or AUTO_RANDOM, not a VARCHAR key. Requires `clustered` = `default` or `clustered` |
| `shard_row_id_bits` | YCSB | `none`, `2`, `4`, `6` | `none` | shard bits of the hidden _tidb_rowid of a nonclustered usertable (2^n ranges): spreads the insert hot spot of increasing row ids; too many cost RPCs in scans. Requires `clustered` = `nonclustered` |
| `pre_split_regions` | YCSB | `none`, `1`, `2`, `3`, `4` | `none` | 2^n regions of the sharded row ids when the table is created, instead of splitting during the load; needs shard_row_id_bits at least n. Requires `shard_row_id_bits` = `4` or `6` |

---

## Dragonfly

Dragonfly is a Redis-compatible, high-performance in-memory data store.
It is used as the SUT for YCSB key-value workloads as a single-instance deployment.

**Configuration** (from `cluster.config`):

```python
'Dragonfly': {
    'loadData': 'redis-cli < {scriptname}',
    'delay_prepare': 0,
    'attachWorker': '',
    'template': {
        'version': 'xxx',
        'alias': 'Key-Value-1',
        'docker_alias': 'KV1',
        'auth': ["root", ""],
    },
    'logfile': '/var/log/redis/redis-server.log',
    'datadir': '/data',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery for sut pods on port 6379 at /metrics
},
```

No JDBC driver is needed — YCSB communicates via the Redis wire protocol.
The monitoring section scrapes Dragonfly's native Prometheus endpoint at `/metrics` on port 6379.

Dragonfly settings are environment variables `DFLY_<flag>` in the templates (e.g. `DFLY_maxmemory`), not command-line flags, because a flag on the command line would win over the variable.
Change them per run with `--set`, e.g. `--set deployment[bexhoma-deployment-dragonfly].container[dbms].env.DFLY_snapshot_cron="*/5 * * * *"` (for the cluster workers: `statefulset[bexhoma-worker]`).
With `-ar`, `save-snapshot.sh` (`SAVE`) runs before each benchmarking round. In a Dragonfly or Redis cluster it runs on every worker, with replicas (DragonflyReplica) too: `SAVE` is not replicated, so each replica writes its own snapshot.
The data pods save under the fixed name `dump` (`DFLY_dbfilename`), so each `SAVE` overwrites the previous snapshot and a restart loads it.

**DDL scripts:**
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Dragonfly)

See [Example: Dragonfly](Example-Dragonfly.md) for a worked example.

---

## DragonflyCluster

`DragonflyCluster` is the configuration key for Dragonfly deployed as a **cluster** (multiple worker nodes).
The loader and benchmarker connect via the cluster's headless service name.

**Configuration** (from `cluster.config`):

```python
'DragonflyCluster': {
    'loadData': 'redis-cli --host bexhoma-service.{namespace}.svc.cluster.local < {scriptname}',
    'delay_prepare': 0,
    'attachWorker': '',
    'template': {
        'version': 'xxx',
        'alias': 'Key-Value-1',
        'docker_alias': 'KV1',
        'auth': ["root", ""],
    },
    'logfile': '/var/log/redis/redis-server.log',
    'datadir': '/data',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery for worker pods on port 6379 at /metrics
},
```

The key difference from single-node Dragonfly is that `loadData` targets the cluster service DNS name rather than `localhost`.
DragonflyCluster uses the same YCSB DDL scripts as single-node [Dragonfly](#dragonfly).

---

## Redis

`Redis` is the configuration key for a Redis cluster deployment (multiple shards as workers).
It is used as the SUT for YCSB key-value workloads in a distributed setting.

**Configuration** (from `cluster.config`):

```python
'Redis': {
    'loadData': 'redis-cli --host bexhoma-service.{namespace}.svc.cluster.local < {scriptname}',
    'delay_prepare': 0,
    'attachWorker': '',
    'template': {
        'version': 'xxx',
        'alias': 'Key-Value-1',
        'docker_alias': 'KV1',
        'auth': ["root", ""],
    },
    'logfile': '/var/log/redis/redis-server.log',
    'datadir': '/data',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery for worker pods on port 9121 (redis_exporter)
},
```

Monitoring uses a `redis_exporter` sidecar scraping each worker pod on port 9121.

Redis does not have dedicated DDL scripts; YCSB manages table/key-space creation directly via the Redis wire protocol.

See [Example: Redis](Example-Redis.md) for a worked example.

---

## DatabaseService

`DatabaseService` is a generic configuration for **external database services** — cloud-managed databases or any PostgreSQL-compatible endpoint that is not itself deployed inside the Kubernetes cluster.
The JDBC connection and `loadData` command reference the service by its in-cluster DNS name via `{namespace}`.

**Configuration** (from `cluster.config`):

```python
'DatabaseService': {
    'loadData': 'psql -U postgres --host bexhoma-service.{namespace}.svc.cluster.local --port 9091 < {scriptname}',
    'template': {
        'version': 'v11.4',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
        'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", ""],
            'url': 'jdbc:postgresql://bexhoma-service.{namespace}.svc.cluster.local:9091/postgres?reWriteBatchedInserts=true',
            'jar': 'postgresql-42.5.0.jar',
            'database': 'postgres',
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
},
```

**DDL scripts:**
- [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/DatabaseService)
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/DatabaseService)

See [Example: Cloud Database](Example-CloudDatabase.md) for a worked example.

---

## Hardware

`Hardware` is not a DBMS — it benchmarks raw disk I/O (fio), CPU/memory
(sysbench), or network latency/throughput (sockperf) on a dedicated SUT
container, bypassing any database engine entirely. The fio/sysbench
benchmarker connects to the SUT over SSH; sockperf connects directly to one
of a fixed pool of persistent `sockperf server` instances running on the SUT
(see below). There is no `loadData` command and no DDL scripts. Run it with
`python hardware.py run -dbms Hardware -xht fio ...` (see `hardware.py -h`
for the full set of fio/sysbench/sockperf-specific flags).

**Deployment template:** [`k8s/deploymenttemplate-Hardware.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Hardware.yml)
— mounts a PVC at `/database` on the SUT; the benchmarker's
`HARDWARE_TEST_DIR` targets a subdirectory of this mount so fio measures the
PVC-backed storage instead of the SUT container's ephemeral filesystem. The
same manifest also declares a static pool of `SOCKPERF_NUM_SERVERS` (default
16) container/Service ports starting at `SOCKPERF_BASE_PORT` (default 20000),
each running one UDP and one TCP `sockperf server` (started by
`images/hardware/sut/entrypoint.sh`); a benchmarker pod picks its dedicated
server via `BEXHOMA_CHILD` (see `images/hardware/benchmarker/run_sockperf.sh`),
so several benchmarker pods can each reach a separate server instead of
contending on one socket.

**Configuration** (from `cluster.config`):

```python
'Hardware': {
    'loadData': '',
    'delay_prepare': 0,
    'template': {
        'version': 'v1.0',
        'alias': 'Hardware',
        'docker_alias': 'HW',
        'auth': ['bench', ''],
    },
    'logfile': '',
    'datadir': '/database',
    'priceperhourdollar': 0.0,
},
```

`template.auth` is required for every non-JDBC `dockers` entry — it's used to
populate `BEXHOMA_USER`/`BEXHOMA_PASSWORD` env vars injected into every job
pod (`configurations/manifest.py`). Hardware's benchmarker scripts don't
actually use these two vars (SSH auth goes through `BEXHOMA_SUT_USER`/
`BEXHOMA_SUT_KEY` instead), but the manifest builder still requires the key
to be present.

No `template.JDBC` block (see footnote¹ above) — results are parsed from the
benchmarker pod's own log output, not queried through DBMSBenchmarker.

**DDL scripts:** none — Hardware has no loading phase; `experiment_dict_template["loader"]`
is always empty and `cluster.config['volumes']['hardware']['initscripts']['Schema']`
is an empty placeholder required only so `configurations.default(...)` can resolve
its (unused) init-script lookup.

---

## Add a New DBMS

To add a DBMS called `NewDBMS`:

1. **Add a configuration entry** in the `dockers` section of `cluster.config` following the reference above.

2. **Create a deployment manifest** at `k8s/deploymenttemplate-NewDBMS.yml`.  
   Copy `k8s/deploymenttemplate-Dummy.yml` as a starting point and adjust the image, port, and resource defaults.

3. **Add DDL scripts** in a subfolder of `experiments/`, e.g., `experiments/tpch/NewDBMS/` for TPC-H.

4. **Register the DBMS in the experiment script** (e.g., `example.py`):

   ```python
   if args.dbms == "NewDBMS":
       name_format = 'NewDBMS-{cluster}'
       config = configurations.default(
           experiment=experiment,
           docker='NewDBMS',
           configuration=name_format.format(cluster=cluster_name),
           alias='DBMS A1'
       )
   ```

   The `docker='NewDBMS'` parameter must match the `dockers` key and the YAML filename.

5. **Add the choice** to the CLI argument parser:

   ```python
   parser.add_argument('-dbms', help='DBMS to run the experiment on', choices=['NewDBMS'])
   ```

If you need a JDBC driver that is not yet included, please raise an issue at https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues.
