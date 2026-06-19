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

---

## Configuration Reference

Every entry in the `dockers` section of `cluster.config` may contain the following fields:

| Field | Required | Description |
|---|---|---|
| `loadData` | yes | Shell command run inside the SUT container to execute an init script. Placeholders: `{scriptname}`, `{database}`, `{schema}`, `{service_name}`, `{namespace}` |
| `delay_prepare` | no | Seconds to wait after the container starts before bexhoma considers it ready (useful for engines that restart during init, e.g., MySQL InnoDB setup) |
| `template` | yes | Base connection template passed to DBMSBenchmarker — includes `version`, `alias`, `docker_alias`, `dialect`, and `JDBC` sub-section |
| `template.JDBC.driver` | yes | Fully qualified Java class name of the JDBC driver |
| `template.JDBC.auth` | yes | `[username, password]` pair |
| `template.JDBC.url` | yes | JDBC URL template. Placeholders: `{serverip}`, `{database}`, `{schema}`, `{dbname}`, `{timeout_ms}`, `{namespace}` |
| `template.JDBC.jar` | yes | JDBC jar filename(s) expected in `jarfolder` |
| `template.JDBC.database` | no | Default database name (substituted into `{database}` in `loadData` and the JDBC URL; overridden per tenant in multi-tenant mode) |
| `template.JDBC.schema` | no | Default schema name (substituted into `{schema}`; overridden per tenant) |
| `template.init_SQL` | no | SQL statement executed after connection is established (e.g., `SET optimizer_switch = ...`) |
| `logfile` | no | Path inside the container to a log file that bexhoma downloads after each experiment |
| `datadir` | no | Path inside the container to the DBMS data directory; bexhoma measures its size after loading |
| `attachWorker` | no | Command run on the coordinator to register a new worker node (used for distributed DBMS like Citus, CockroachDB) |
| `worker_port` | no | Internal port of the worker/coordinator headless service (used for TiDB) |
| `store_args` | no | Whether to capture and display the container startup arguments in the experiment summary (default: `True`) |
| `priceperhourdollar` | no | Reserved for cost modelling (currently unused) |
| `monitor` | no | Application-level monitoring configuration; see [Monitoring](Monitoring.md) |

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
The default image runs MySQL 8.4.

**Deployment template:** [`k8s/deploymenttemplate-MySQL.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MySQL.yml)

The default deployment tuning includes `innodb-buffer-pool-size=32G`, `innodb-write-io-threads=64`, `innodb-read-io-threads=64`, `innodb-redo-log-capacity=8G`, `innodb-flush-log-at-trx-commit=0`, and `innodb-parallel-read-threads=64`.
See the [MySQL 8.4 documentation](https://dev.mysql.com/doc/refman/8.4/en/mysql-nutshell.html) for parameter explanations.

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

---

## MariaDB

MariaDB is supported for TPC-H, Benchbase TPC-C, HammerDB TPC-C, and YCSB experiments.
It uses a dedicated `bexhoma` database user rather than `root`.

**Deployment template:** [`k8s/deploymenttemplate-MariaDB.yml`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MariaDB.yml)

The default deployment sets `innodb_log_buffer_size`, `innodb-write-io-threads=16`, and `innodb-log-file-size`.

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

See [Example: Citus](Example-Citus.md) for a worked example.

---

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

**DDL scripts:**
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/YugabyteDB)

See [Example: YugabyteDB](Example-YugaByteDB.md) for a worked example.

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
`worker_port: 2379` is the PD headless service port used internally for cluster coordination.
The monitoring section scrapes all three components via Kubernetes pod discovery.

**DDL scripts:**
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/TiDB)

See [Example: TiDB](Example-TiDB.md) for a worked example.

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
