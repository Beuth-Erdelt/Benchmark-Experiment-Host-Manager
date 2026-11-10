# Concept: DBMS

To include a DBMS in a Kubernetes-based experiment you need:

- a Docker image
- a JDBC driver (for SQL-based DBMS used with DBMSBenchmarker)
- a Kubernetes deployment manifest (YAML template)
- a configuration entry in `cluster.config` (the `dockers` section)
- DDL scripts for schema creation, data loading, and index building

This document covers the concepts that all DBMS share: the configuration entry, the deployment templates, reset scripts, load durability and DDL parameters.
Each supported DBMS has a short section below; configuration, deployment, scripts and examples are on its example page.

| Group | DBMS | `-dbms` | Benchmarks | Example |
|---|---|---|---|---|
| Relational / SQL | [PostgreSQL](#postgresql) | `PostgreSQL` | TPC-H, TPC-DS, SSB, YCSB, Benchbase, HammerDB | [Example-PostgreSQL](Example-PostgreSQL.md) |
| Relational / SQL | [PostgreSQL + PGBouncer](#pgbouncer) | `PGBouncer` | YCSB, Benchbase | [Example-PGBouncer](Example-PGBouncer.md) |
| Relational / SQL | [PgDuckDB](#pgduckdb) | `PgDuckDB` | TPC-H, SSB | [Example-PgDuckDB](Example-PgDuckDB.md) |
| Relational / SQL | [MySQL](#mysql) | `MySQL` | TPC-H, TPC-DS, SSB, YCSB, Benchbase, HammerDB | [Example-MySQL](Example-MySQL.md) |
| Relational / SQL | [MariaDB](#mariadb) | `MariaDB` | TPC-H, TPC-DS, SSB, YCSB, Benchbase, HammerDB | [Example-MariaDB](Example-MariaDB.md) |
| Relational / SQL | [MariaDB ColumnStore](#mariadb-columnstore) | `MariaDBCS` | TPC-H, TPC-DS, SSB | [Example-MariaDBCS](Example-MariaDBCS.md) |
| Relational / SQL | [MonetDB](#monetdb) | `MonetDB` | TPC-H, TPC-DS, SSB | [Example-MonetDB](Example-MonetDB.md) |
| Relational / SQL | [ClickHouse](#clickhouse) | `ClickHouse`, `ClickHouseCluster` | TPC-H, TPC-DS, SSB | [Example-ClickHouse](Example-ClickHouse.md) |
| Relational / SQL | [CedarDB](#cedardb) | `CedarDB` | TPC-H, SSB, YCSB, Benchbase | [Example-Other-DBMS](Example-Other-DBMS.md#cedardb) |
| Distributed SQL | [Citus](#citus) | `Citus` | TPC-H, SSB, YCSB, Benchbase, HammerDB | [Example-Citus](Example-Citus.md) |
| Distributed SQL | [YugabyteDB](#yugabytedb) | `YugabyteDB` | YCSB, Benchbase | [Example-YugaByteDB](Example-YugaByteDB.md) |
| Distributed SQL | [CockroachDB](#cockroachdb) | `CockroachDB` | YCSB, Benchbase | [Example-CockroachDB](Example-CockroachDB.md) |
| Distributed SQL | [TiDB](#tidb) | `TiDB` | YCSB, Benchbase | [Example-TiDB](Example-TiDB.md) |
| Key-Value | [Redis](#redis) | `Redis` | YCSB | [Example-Redis](Example-Redis.md) |
| Key-Value | [Dragonfly](#dragonfly) | `Dragonfly` | YCSB | [Example-Dragonfly](Example-Dragonfly.md) |
| Key-Value | [Valkey](#valkey) | `Valkey` | YCSB | [Example-Valkey](Example-Valkey.md) |
| Key-Value | [Garnet](#garnet) | `Garnet` | YCSB | [Example-Garnet](Example-Garnet.md) |
| Wide-Column | [Cassandra](#cassandra) | `Cassandra` | YCSB | [Example-Cassandra](Example-Cassandra.md) |
| External service | [DatabaseService](#databaseservice) | `DatabaseService` | TPC-H, YCSB, Benchbase | [Example-CloudDatabase](Example-CloudDatabase.md) |
| No DBMS | [Hardware](#hardware) | `Hardware` | fio, sysbench, netperf, sockperf | [Example-Hardware](Example-Hardware.md) |

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
| `benchmarks` | yes² | The benchmarks the DBMS can run, and what each needs of it; see [Benchmarks of a DBMS](#benchmarks-of-a-dbms) |
| `storage_prefix` | yes² | Name of the storage (volume) of the DBMS, the same for every benchmark (e.g. `postgresql`, `PgDuckDB`) |
| `abbreviation` | no | Short name of the DBMS in the names of volumes and worker stateful sets (`pg`, `chc`, `df`, ...): a storage name that starts with the DBMS name gets it instead (`postgresql-schema-16` → `pg-schema-16`), since Kubernetes and some DBMS limit the length of these names |
| `tls` | no | `{'secret': True}`: a CA and server certificate Secret is created per SUT, for the server and the benchmark client (MySQL with HammerDB, see [MySQL](Example-MySQL.md)) |
| `base_system` | no | DBMS whose script folder `experiments/<benchmark>/<base_system>` this DBMS uses, if it is not its own (PgDuckDB and PGBouncer use `PostgreSQL`) |
| `workers` | no | `True` if the SUT takes `-nw` workers (shards) next to its coordinator |
| `sut_attributes` | no | How the SUT is set up (placeholder pod, no monitoring, Helm-managed stateful sets, ...); see [Benchmarks of a DBMS](#how-the-sut-is-set-up-sut_attributes) |
| `initial_cluster` | no | `{component, port, scheme, env}`: the members of this component are passed to the SUT pods as `env`, for a DBMS that bootstraps as a cluster (TiDB: the `pd` nodes) |
| `template.alias` | yes | The name of the DBMS in the reports: one per DBMS, the same for every benchmark and experiment |
| `template.dialect` | no | SQL dialect of the DBMS: the key of its query variants in the query files (`MySQL`, `Clickhouse`, `CedarDB`, ...) |
| `monitor.<component>.blackbox_database` | no | Database that the blackbox probe of the application monitoring connects to |

¹ Only required for SQL DBMS queried via DBMSBenchmarker. Entries whose SUT is
never queried through DBMSBenchmarker — [Dragonfly](#dragonfly),
[DragonflyCluster](#dragonflycluster), [Redis](#redis), [Valkey](#valkey), [Garnet](#garnet), [Cassandra](#cassandra), [Hardware](#hardware) —
omit `template.JDBC` entirely; `template` itself is still required (at minimum
`version`, `alias`, `docker_alias`), and `template.auth` (a `[username,
password]` pair) becomes required instead — `configurations/manifest.py`
falls back to `template['auth']` for `BEXHOMA_USER`/`BEXHOMA_PASSWORD`
injection whenever `template.JDBC` is absent.

² Required for a DBMS that has `benchmarks`.

### Benchmarks of a DBMS

The entry scripts (`tpch.py`, `tpcds.py`, `ssb.py`, `ycsb.py`, `benchbase.py`, `hammerdb.py`) contain nothing that is specific to a DBMS.
Everything a script needs to know about a DBMS is in its `dockers` entry, so a DBMS is added by configuration alone, see [Add a New DBMS](#add-a-new-dbms).

`benchmarks` has one key per benchmark the DBMS can run: `tpch`, `tpcds`, `ssb`, `ycsb`, `benchbase` and `tpcc` (HammerDB).
**A missing key means that the DBMS cannot run that benchmark**: the `-dbms` of a script offers exactly the DBMS that have an entry for it.
For example, MariaDB ColumnStore has no `ycsb` key:

```python
'MariaDBCS': {
    'storage_prefix': 'mariadbcs',
    'template': {'alias': 'Columnwise-C', 'dialect': 'MySQL', ...},
    'benchmarks': {
        'tpch': {'loading_template': 'jobtemplate-loading-tpch-MariaDB.yml',
                 'refresh_template': 'jobtemplate-benchmarking-tpch-refresh-MariaDB.yml',
                 'reset_scripts': ['reset-tpch.sql'],
                 'loading_parameters': {'MYSQL_LOADING_FROM': 'LOCAL'},
                 'sut_parameters': {'MARIADB_DATABASE': 'tpch'},
                 'max_loading_pods': 1},
        'ssb': {...},
    },
},
```

The keys of an entry of `benchmarks`:

| Key | Description |
|---|---|
| `default` | `True`: the DBMS runs if `-dbms` is not given. Without it the DBMS has to be named. |
| `loading_template` | Job template in `k8s/` that loads the data (TPC-H, TPC-DS, SSB). A DBMS that loads needs one: there is no default job. HammerDB, Benchbase and YCSB bring a loading job of their own. |
| `refresh_template` | Job template of the TPC-H refresh stream (`-xrs`), see [TPC-H](Example-TPC-H.md#refresh-stream). All DBMS of one run need the same job. |
| `reset_scripts` | Scripts run before each benchmarking round with `-ar`, see [Reset scripts](#reset-scripts--ar) |
| `loading_parameters`, `benchmarking_parameters` | Environment of the loading and benchmarking jobs |
| `sut_parameters` | Environment of the SUT container; a value you set yourself wins |
| `eval_parameters` | Parameters stored with the results |
| `option_parameters` | `{ENV_NAME: option}`: environment of the SUT container taken from a boolean option of the command line (`DUCKDB_FORCE_EXECUTION` from `-xdfe`) |
| `option_experiment` | Init and indexing scripts used when a boolean option is set (Citus: `-xcol` switches to columnar storage) |
| `max_loading_pods` | Number of loading pods the DBMS tolerates; more are reduced with a message (MariaDB ColumnStore: 1) |
| `max_sut_dbms` | Number of SUT of the DBMS that may run at the same time |
| `per_loading_threads` | The DBMS gets one configuration per `-nlt` value, with these loading parameters (MySQL) |
| `pooling` | For a DBMS behind a connection pooler: one configuration per combination of `-xnpp`, `-xnpi` and `-xnpo` (PGBouncer) |
| `dimensions`, `unsupported_dimensions` | `-xdim` applies to the DBMS; or it refuses a variant of it, with the reason |
| `multi_tenancy`, `tenant_parameters` | The tenancy modes the DBMS supports and the parameters it gets, see [Multi-Tenant](Example-Multi-Tenant.md) |
| `notes` | Lines for the workload info of the experiment |
| `experiment_yaml` | An `experiment.yaml` may name the DBMS for the benchmark |
| `variants` | Changes that depend on the command line, see below |

#### Values

Values of `loading_parameters`, `sut_parameters`, `reset_scripts` and the like may contain placeholders for options of the command line, e.g. `'{num_worker_replicas}'` or `'{workload}'`.
A value that is exactly one placeholder keeps its type, so numbers stay numbers.
A selector `{'$by': 'benchmark', 'tpcc': 'false', '*': 'true'}` takes the value for the option `benchmark` (`-xbt` of Benchbase), or the one of `'*'`; without a match, the value is left out.

#### Variants

A DBMS can look different depending on the options.
`variants` is a list of `{'when': <expression>, ...}`; every variant whose expression holds for the command line is applied in order, and the keys it names replace those of the entry (dicts are merged).
An expression may use options of the command line, numbers, strings, `+ - * //`, comparisons, `and`, `or` and `not`; nothing else is allowed.
A variant can also set `docker` (another entry of `dockers` to build the configuration from), `sut_template`, `storage_prefix`, `worker_count` and `sut_attributes`.

The key-value systems use this for their modes.
Dragonfly, for example, is a single node by default; with workers it is the `DragonflyCluster`, and with replicas on top it uses the replica template and its own storage:

```python
'variants': [
    {'when': 'num_worker > 0', 'docker': 'DragonflyCluster',
     'sut_attributes': {'sut_role': 'placeholder', 'monitoring_sut': False, 'script_target': 'workers'},
     'loading_parameters': {'BEXHOMA_DBMS_TYPE': 'redis-cluster'},
     'benchmarking_parameters': {'BEXHOMA_DBMS_TYPE': 'redis-cluster'}},
    {'when': 'num_worker > 0 and num_worker_replicas > 0',
     'sut_template': 'deploymenttemplate-DragonflyReplica.yml', 'storage_prefix': 'dfr',
     'loading_parameters': {'BEXHOMA_DBMS_TYPE': 'redis'},
     'benchmarking_parameters': {'BEXHOMA_DBMS_TYPE': 'redis'}},
],
```

Redis, Valkey and Garnet use `'worker_count': 'num_worker * (1 + num_worker_replicas)'` for the pods of a cluster with replicas.

#### How the SUT is set up (`sut_attributes`)

`sut_attributes` is a dict that is applied to the configuration of the DBMS.
`sut_role`, `pvc_selector`, `script_target`, `data_components` and `resources` call the setter of that name, `statefulsets` (`{name: pods}`) records stateful sets that something else manages (the Helm chart of YugabyteDB), and `monitoring_sut`, `resource_sweep`, `statefulset_name`, `sut_container_name`, `sut_has_pool`, `sut_pod_name`, `sut_service_name` and `worker_metric_strip_container` are attributes of the configuration.
Any other key is refused, so a typo does not go unnoticed.
For example, DatabaseService runs outside of Kubernetes: `{'sut_role': 'placeholder', 'monitoring_sut': False, 'resource_sweep': False}`.

#### Checking an entry

`python -m pytest tests/test_system_descriptors.py` checks the entries of `k8s-cluster.config`: known keys, correct types, expressions that are allowed, and job templates that exist in `k8s/`.
`tests/test_dbms_snapshots.py` records what each entry script builds for each DBMS.

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
The full reference (including job templates and non-SUT manifests) is in the [Kubernetes manifests README](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/README.md).

### File naming

The template filename is derived automatically from the `dockers` key:

```
k8s/deploymenttemplate-{Key}.yml
```

The `Key` must exactly match the key of the DBMS in the `dockers` section of `cluster.config` (or the `docker` a variant of its `benchmarks` entry names, e.g. `DragonflyCluster`), unless the entry sets its own `sut_template`.
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
See the [Kubernetes manifests README](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/README.md) for details.

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

#### Volumes of the SUT

`--set KIND[NAME](@CONFIG).volume[V].FIELD=VALUE` changes an `emptyDir` volume of a Deployment or StatefulSet of the SUT template:

| `FIELD` | Value | Effect |
|---|---|---|
| `sizeLimit` | a quantity, e.g. `64Gi` | maximum size of the volume |
| `medium` | `Memory` | the volume is a tmpfs in RAM |
| `medium` | empty | the volume lives on the node's disk |

Examples are the tmpdir of MySQL (`mysqltmp`, a 32Gi tmpfs in the template) and the shared memory of PostgreSQL and others (`dshm`):
```bash
--set deployment[bexhoma-deployment-mysql].volume[mysqltmp].sizeLimit=64Gi
--set deployment[bexhoma-deployment-mysql].volume[mysqltmp].medium=
```
Files in a volume of `medium: Memory` count against the memory limit of the container (`-lr`).
Bexhoma warns when `sizeLimit` is larger than that limit.
Only `emptyDir` volumes can be changed this way; the persistent volume of the SUT is sized by `-rss`.
The volumes of loading and benchmarking jobs are not reachable by `--set`.

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
| MariaDBCS | `ANALYZE TABLE` | n/a (no dirty pages to flush) | n/a (the check scripts read no ColumnStore counter) |
| CedarDB | `VACUUM VERBOSE ANALYZE` | n/a (no `CHECKPOINT`) | n/a (no `pg_stat_reset()`) |
| MonetDB | `ANALYZE` | n/a (the write-ahead log is applied in the background; no call to force it) | n/a |
| ClickHouse | n/a (no optimizer statistics unless declared per column) | `reset-flush.sh`: `sync` (an `INSERT` writes its parts without fsync) | n/a (`system.events` cannot be reset) |
| ClickHouseCluster | n/a | `SYSTEM FLUSH DISTRIBUTED` on every Distributed table and `SYSTEM SYNC REPLICA ON CLUSTER` on every replicated table (`reset-<benchmark>.sql`, coordinator), then `reset-flush.sh` (`sync`) in every worker | n/a |
| YugabyteDB | `ANALYZE VERBOSE` (cluster-wide) | n/a (no `CHECKPOINT` in YSQL, no `yb-admin` in the helper pod) | `reset-counters.sh`: `pg_stat_reset()` on every tserver (`yb-tserver-N.yb-tservers`), not once through the service, which picks one tserver per connection |
| CockroachDB | `ANALYZE` (cluster-wide) | n/a (Pebble flushes on its own) | `crdb_internal.reset_sql_stats()` (cluster-wide) |
| TiDB | `ANALYZE TABLE` (cluster-wide) | n/a (no flush in SQL) | `FLUSH STATUS` on the TiDB server the connection reaches |
| Dragonfly | n/a | `SAVE` on every data pod | `CONFIG RESETSTAT` |
| Redis | n/a | `SAVE` (standalone: SUT pod; cluster: every worker) | `CONFIG RESETSTAT` |
| Valkey | n/a | `SAVE` (standalone: SUT pod; cluster: every worker) | `CONFIG RESETSTAT` |
| Garnet | n/a | `SAVE` (checkpoint; standalone: SUT pod; cluster: every worker) | n/a (no `CONFIG RESETSTAT`) |
| Cassandra | n/a | `save-snapshot.sh`: `nodetool flush`, wait until no compactions are pending (at most 1800 s; single node: SUT pod; cluster: every worker) | n/a (the JMX metrics cannot be reset) |

DatabaseService has no reset.
Benchbase `twitter`, `ycsb` and `chbenchmark` have a reset for PostgreSQL, PGBouncer and CedarDB only (the other DBMS have no scripts for them).
With `-ar` on a configuration without a reset, the experiment prints a warning at the start; a listed script missing in the experiment folder is skipped with a message.

Scripts are in the experiment folder of the DBMS (`experiments/<benchmark>/<DBMS>/`, Benchbase `experiments/benchbase/<benchmark>/<DBMS>/`), named `reset-<benchmark>.sql`, plus `reset-flush.sh` (MySQL, MariaDB, ClickHouse), `reset-counters.sh` (YugabyteDB) or `save-snapshot.sh` (Dragonfly, Redis, Cassandra).
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

For a new DBMS: put `durability-<level>.sql`/`.sh` and `restoredurability-<level>.sql`/`.sh` next to its init scripts; the restore must return to the startup values, not to the defaults (MySQL/MariaDB save them in `bexhoma.saved_settings`). A value that can only be set server-wide, so a `--set` value wins over the script, is declared in a header line `-- server-wide: name=value ...`; bexhoma then refuses a conflicting `--set` before loading.
PostgreSQL: `--set` passes a value as `-c` on the command line, which `ALTER SYSTEM` cannot change. `synchronous_commit` is therefore also set per database (`ALTER DATABASE ... SET`, which wins over the command line, for new sessions; Citus also on every worker) and reset after the load: `-xld relaxed --set synchronous_commit=on` loads with `off` and benchmarks with `on`. `fsync` and `full_page_writes` are server-wide only: when `--set` fixes them differently from what the level needs (e.g. `-xld unsafe --set ...fsync=on`), bexhoma refuses to load and aborts the experiment with the reason (test `Loading completed without failures`); the durability scripts also check the values they set and end with an `ERROR` otherwise.

### Failed loads

Nothing reads the loaded tables to check a load. A load counts as failed if
- a loader pod fails: a loader exits with 1 when the reply of a load statement is an error or reports fewer rows than the file has (`BEXHOMA_INGEST:...:failed` in its log); test `Loader pods without errors`,
- a loading script fails (schema, durability, indexes, constraints, statistics, checks; shell scripts run with `sh -e`); test `Init scripts without errors`,
- the SUT restarts during loading, or scripts cannot be uploaded; test `Loading completed without failures`.

A failed loading job aborts the experiment (with diagnostics). A failed load never labels its volume `loaded=True`; such a volume is not reused, remove it with `-rsr`.

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

`PostgreSQL` is the configuration key for PostgreSQL, the primary test target of bexhoma for analytical (TPC-H, TPC-DS, SSB) and transactional benchmarks (Benchbase, HammerDB, YCSB).

See [Example: Benchmark PostgreSQL](Example-PostgreSQL.md) for configuration, deployment, scripts, DDL parameters, durability, reset and examples.

---

## PGBouncer

`PGBouncer` is the configuration key for a PostgreSQL deployment fronted by a PgBouncer connection pool: the SUT component runs PostgreSQL, the pool component runs PgBouncer, and benchmarker pods connect to PgBouncer.
It uses the DDL, durability and reset scripts of [PostgreSQL](#postgresql).

See [Example: Benchmark PGBouncer](Example-PGBouncer.md) for configuration, deployment and examples.

---

## PgDuckDB

`PgDuckDB` is the configuration key for PostgreSQL with the extension `pg_duckdb`, used for TPC-H and SSB; with `-xdfe` the queries run in DuckDB's engine.
It uses the DDL, durability and reset scripts of [PostgreSQL](#postgresql).

See [Example: Benchmark PgDuckDB](Example-PgDuckDB.md) for configuration, deployment and examples.

---

## MySQL

`MySQL` is the configuration key for MySQL 9.7 (LTS), used for TPC-H, TPC-DS, Benchbase, HammerDB and YCSB.
MySQL 9 needs TLS for the first login of `root`, so bexhoma creates a TLS Secret per SUT.

See [Example: Benchmark MySQL](Example-MySQL.md) for configuration, deployment, scripts, DDL parameters, durability, reset and examples.

---

## MariaDB

`MariaDB` is the configuration key for MariaDB, used for TPC-H, TPC-DS, Benchbase, HammerDB and YCSB.
It uses a dedicated `bexhoma` database user rather than `root`.

See [Example: Benchmark MariaDB](Example-MariaDB.md) for configuration, deployment, scripts, DDL parameters, durability, reset and examples.

---

## MariaDB ColumnStore

MariaDB ColumnStore (`MariaDBCS`) is the columnar storage engine of MariaDB, GPL-2.0, for TPC-H, TPC-DS and SSB on a single node.
The template runs the official image of MariaDB and installs the plugin at every start; loading always uses one loader pod.

```bash
bexhoma tpch -dbms MariaDBCS -sf 1 -xis -tr run
```

See [Example: Benchmark MariaDB ColumnStore](Example-MariaDBCS.md) for deployment, loading, schema, query variants and examples.

---

## MonetDB

`MonetDB` is the configuration key for MonetDB, a column-store DBMS for TPC-H, TPC-DS and SSB on a single node.

See [Example: Benchmark MonetDB](Example-MonetDB.md) for configuration, deployment, scripts and examples.

---

## ClickHouse

`ClickHouse` is the configuration key for ClickHouse, a column-store DBMS for analytical workloads (TPC-H, TPC-DS, SSB), as a single server.
Queries run over JDBC (HTTP interface), loaders and init scripts use `clickhouse-client`; application metrics come from ClickHouse's own Prometheus endpoint (port 9363).

See [Example: Benchmark ClickHouse](Example-ClickHouse.md) for configuration, deployment, SQL settings, schema, DDL parameters, query variants and examples.

---

## ClickHouseCluster

`ClickHouseCluster` is the configuration key for a ClickHouse cluster of one coordinator (the SUT, with a single-node ClickHouse Keeper) and `-nw` shards (worker StatefulSet, one replica per shard).

See [Example: Benchmark ClickHouse](Example-ClickHouse.md#cluster) for deployment, schema and examples.

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

---

## Citus

`Citus` is the configuration key for Citus, a PostgreSQL extension that shards tables across worker nodes.
The coordinator is deployed as the SUT, the workers as a stateful set; after each worker pod starts, bexhoma registers it at the coordinator (`attachWorker`).

See [Example: Benchmark Citus](Example-Citus.md) for configuration, deployment, scripts, DDL parameters and examples.

---

## YugabyteDB

`YugabyteDB` is the configuration key for YugabyteDB, a distributed, PostgreSQL-compatible DBMS, used as the SUT for YCSB and Benchbase.
YugabyteDB itself is installed by Helm, not by bexhoma; the bexhoma SUT pod is a placeholder helper.
Monitoring scrapes the native endpoints of the master (port 7000) and tserver (port 9000) pods.

See [Example: Benchmark YugabyteDB](Example-YugaByteDB.md) for installation, configuration, deployment, scripts, DDL parameters and examples.

---

## CockroachDB

`CockroachDB` is the configuration key for CockroachDB, a distributed, PostgreSQL wire-compatible DBMS, used as the SUT for YCSB and Benchbase.
The workers form the CockroachDB cluster, the SUT pod is a placeholder; monitoring scrapes the built-in endpoint `/_status/vars` (port 8080) of all worker pods.

See [Example: Benchmark CockroachDB](Example-CockroachDB.md) for configuration, deployment, scripts, DDL parameters and examples.

---

## TiDB

`TiDB` is the configuration key for TiDB, a distributed, MySQL-compatible DBMS, used as the SUT for YCSB and Benchbase.
It consists of the TiDB SQL layer (SUT), TiKV storage nodes (worker) and the Placement Driver (PD); all three are deployed and monitored separately.

See [Example: Benchmark TiDB](Example-TiDB.md) for configuration, deployment, scaling of the components, scripts, DDL parameters and examples.

---

## Redis

`Redis` is the configuration key for Redis, as a single host or as a cluster (`-nw`), used as the SUT for YCSB.
Monitoring uses a `redis_exporter` sidecar on port 9121.

See [Example: Benchmark Redis](Example-Redis.md) for configuration, deployment, scripts and examples.

---

## Dragonfly

`Dragonfly` is the configuration key for Dragonfly as a single host, `DragonflyCluster` for a cluster or master with replicas (`-nw`), used as the SUT for YCSB.
Monitoring scrapes the native Prometheus endpoint of Dragonfly at `/metrics` on port 6379.

See [Example: Benchmark Dragonfly](Example-Dragonfly.md) for configuration, deployment, settings, scripts and examples.

---

## DragonflyCluster

See [Dragonfly](#dragonfly).

---

## Valkey

`Valkey` is the configuration key for Valkey, as a single host or as a cluster (`-nw`), used as the SUT for YCSB.
It is the configuration of [Redis](#redis) with `valkey-cli` instead of `redis-cli`; monitoring uses the same `redis_exporter` sidecar (port 9121) and the `redis` metric set.

See [Example: Benchmark Valkey](Example-Valkey.md) for configuration, deployment, scripts and examples.

---

## Garnet

`Garnet` is the configuration key for Garnet, Microsoft Research's RESP-compatible cache store, as a single host or as a cluster (`-nw`), used as the SUT for YCSB with the Redis binding.
There is no exporter, so only cAdvisor metrics are collected.

See [Example: Benchmark Garnet](Example-Garnet.md) for configuration, deployment, scripts and examples.

---

## Cassandra

`Cassandra` is the configuration key for Apache Cassandra as a single node, `CassandraCluster` for a cluster (`-nw`), used as the SUT for YCSB with its `cassandra-cql` binding.
Monitoring uses a `cassandra_exporter` sidecar on port 8080.

See [Example: Benchmark Cassandra](Example-Cassandra.md) for configuration, deployment, scripts, DDL parameters and examples.

---

## DatabaseService

`DatabaseService` is a generic configuration for external database services — cloud-managed databases or any PostgreSQL-compatible endpoint that is not deployed inside the Kubernetes cluster.
The bexhoma SUT pod is a placeholder, and the SUT itself is not monitored.

See [Example: Benchmark a Cloud Database](Example-CloudDatabase.md) for configuration, the placeholder of a cloud service and examples.

---

## Hardware

`Hardware` is not a DBMS: it benchmarks raw disk I/O (fio), CPU/memory (sysbench) or network latency and throughput (netperf, sockperf) on a dedicated SUT container.
There is no `loadData` command and there are no DDL scripts.

See [Example: Hardware](Example-Hardware.md#technical-details) for the deployment, the configuration and examples.

---

## Add a New DBMS

To add a DBMS called `NewDBMS`:

1. **Add a configuration entry** in the `dockers` section of `cluster.config` following the reference above.

2. **Create a deployment manifest** at `k8s/deploymenttemplate-NewDBMS.yml`.  
   Copy `k8s/deploymenttemplate-Dummy.yml` as a starting point and adjust the image, port, and resource defaults.

3. **Add DDL scripts** in a subfolder of `experiments/`, e.g., `experiments/tpch/NewDBMS/` for TPC-H.

4. **Declare the benchmarks** it can run in `benchmarks` of the entry, with `storage_prefix` and `template.alias`, see [Benchmarks of a DBMS](#benchmarks-of-a-dbms).
   No entry script has to be changed: `-dbms` offers every DBMS that has an entry for the benchmark, and the configuration is built from the entry.
   The key of the entry must match the YAML filename of the deployment template (`docker='NewDBMS'`).

If you need a JDBC driver that is not yet included, please raise an issue at https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues.

5. **Add an example page** `docs/Example-NewDBMS.md` with a test script `scripts/test-docs-newdbms.sh` and `.ps1`, whose runs are in the order of the page.
   All example pages of a DBMS have the same structure:

   * a short introduction and references (as links), including the test script
   * the main use case (`Perform <Benchmark> Benchmark`): a quick run without monitoring, with subsections Status, Cleanup and Evaluate Results
   * Monitoring: a run of at least one minute of benchmarking with `-m -mc`, and Application Metrics (`-ma`) where the DBMS has an exporter
   * Persistent Storage: a run with `-rst` and `-nc 2`, so the second repetition uses the loaded volume
   * Variants, where the DBMS has them (cluster, replication, components, ...), one subsection with an example result each
   * Technical Details: configuration of bexhoma, deployment, schema and scripts, DDL parameters, load durability and reset scripts
   * one section per further use case (benchmark)

   Logs are named `docs_<benchmark>_<dbms>[_<role>].log`, e.g. `_monitoring`, `_appmetrics`, `_storage`, `_cluster`; [TestCases](TestCases.md) lists all test scripts.
   Add the page to `docs/index.rst` and a short section with a link to this document.
