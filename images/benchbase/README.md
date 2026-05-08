# Benchbase Images

The images are based on [benchbase.azurecr.io/benchbase](https://github.com/cmu-db/benchbase).

This folder contains two Dockerfiles for Benchbase experiments within Bexhoma:

* `Dockerfile_benchmarker` — runs the Benchbase execute phase against an already-loaded DBMS.
* `Dockerfile_generator` — runs the Benchbase load phase to populate a DBMS.

Both images bundle the XML config templates from `config/` and substitute environment
variable values into the selected template at container startup via `sed`.

Supported benchmarks: `tpcc`, `twitter`, `chbenchmark`, `ycsb`.

Supported profiles (config subdirectory / DBMS): `postgres`, `mysql`, `mariadb`,
`cockroachdb`, `noisepage`, `spanner`, `sqlite`, `sqlserver`, `phoenix`.

---

## Benchmarker (`Dockerfile_benchmarker`)

Runs `./entrypoint.sh run … --create=false --load=false --execute=true`.

### Environment variables

#### Scaling and parallelism

* `SF`: Scale factor — number of TPC-C warehouses or equivalent dataset size unit.
* `BEXHOMA_NUM_PODS`: Number of parallel benchmarker pods.
* `BEXHOMA_CHILD`: Index of the current pod (1-based). Overwritten at runtime by the Redis queue entry.
* `BEXHOMA_RNGSEED`: Random seed. Currently ignored.

#### Target DBMS connection

The following variables are substituted into the selected XML config template via `sed`.

* `BEXHOMA_HOST`: Hostname of the target DBMS.
* `BEXHOMA_PORT`: Port of the target DBMS.
* `BEXHOMA_USER`: Database user.
* `BEXHOMA_PASSWORD`: Database password.
* `BEXHOMA_DATABASE`: Database name.
* `BEXHOMA_SCHEMA`: Schema name. Set automatically in multi-tenant (`schema`) mode; otherwise substituted as-is.
* `BEXHOMA_URL`: JDBC connection URL. Not used directly by the entrypoint script.
* `BEXHOMA_JAR`: JDBC driver jar file name. Not used directly by the entrypoint script.
* `BEXHOMA_DRIVER`: JDBC driver class name. Not used directly by the entrypoint script.

#### Bexhoma experiment identity

* `BEXHOMA_DBMS`: DBMS label. When set to `PGBouncer`, the schema query parameter is stripped from the XML config URL before substitution.
* `BEXHOMA_CONFIGURATION`: Configuration name. Echoed to the log.
* `BEXHOMA_CONNECTION`: Bexhoma connection name. Used to address the Redis message queue (`bexhoma-benchmarker-<CONNECTION>-<EXPERIMENT>`).
* `BEXHOMA_EXPERIMENT`: Bexhoma experiment identifier. Used to address the Redis message queue.
* `BEXHOMA_EXPERIMENT_RUN`: Number of the current repetition of the complete experiment.
* `BEXHOMA_CLIENT`: Client index. Echoed to the log.

#### Multi-tenancy

* `BEXHOMA_TENANT_BY`: Tenant isolation strategy — `schema` (derives `BEXHOMA_SCHEMA` from `BEXHOMA_CHILD`), `database` (derives `BEXHOMA_DATABASE` from `BEXHOMA_CHILD`), `container` (enables cross-container sync barrier), or empty for no tenancy.
* `BEXHOMA_TENANT_NUM`: Total number of tenants. Echoed to the log.
* `BEXHOMA_NUM_PODS_TOTAL`: Total pods across all containers in a `container` tenancy run. Used for the experiment-level sync barrier on `bexhoma-benchmarker-podcount-<EXPERIMENT>`.

#### Pod synchronisation

Pods always synchronise before starting: each pod increments the Redis counter
`bexhoma-benchmarker-podcount-<CONNECTION>-<EXPERIMENT>` and waits until all
`BEXHOMA_NUM_PODS` pods are ready. An additional experiment-level barrier on
`bexhoma-benchmarker-podcount-<EXPERIMENT>` is used when `BEXHOMA_TENANT_BY=container`.

* `BEXHOMA_TIME_START`: Optional RFC-3339 timestamp. When non-zero, the pod sleeps until this time before starting.
* `BEXHOMA_TIME_NOW`: Informational timestamp of the planned start, echoed to the log.

#### Benchbase workload parameters

* `BENCHBASE_BENCH`: Benchmark name — `tpcc`, `twitter`, `chbenchmark`, or `ycsb`.
* `BENCHBASE_PROFILE`: DBMS profile name. Selects the XML config subdirectory (e.g. `postgres`, `mysql`).
* `BENCHBASE_TARGET`: Target throughput in requests per second. Substituted into the XML config.
* `BENCHBASE_TIME`: Benchmark duration in seconds. Substituted into the XML config.
* `BENCHBASE_TERMINALS`: Number of simulated client terminals (threads). Substituted into the XML config.
* `BENCHBASE_BATCHSIZE`: Batch size for grouped query submission. Substituted into the XML config.
* `BENCHBASE_ISOLATION`: Transaction isolation level (e.g. `TRANSACTION_SERIALIZABLE`, `TRANSACTION_READ_COMMITTED`). Substituted into the XML config.
* `BENCHBASE_STATUS_INTERVAL`: When set to a positive integer, passes `--interval-monitor <N>` to Benchbase, logging a status line every N milliseconds. Empty disables interval monitoring.
* `BENCHBASE_NEWCONNPERTXN`: When `true`, a new JDBC connection is opened for every transaction. Substituted into the XML config.
* `BENCHBASE_KEY_AND_THINK`: When `true`, uncomments the pre- and post-execution wait blocks in the XML config (TPC-C key-and-think time).
* `BENCHBASE_YCSB_WORKLOAD`: YCSB workload preset — `a`, `b`, `c`, `d`, `e`, or `f`. Automatically sets `BENCHBASE_YCSB_WEIGHTS` to the standard operation mix for that workload.
* `BENCHBASE_YCSB_WEIGHTS`: Comma-separated operation-type weights for YCSB (read, insert, scan, update, delete, readmodifywrite). Overridden by `BENCHBASE_YCSB_WORKLOAD` when set. Substituted into the XML config.

---

## Generator (`Dockerfile_generator`)

Runs `./entrypoint.sh run … --create=<BENCHBASE_CREATE_SCHEMA> --load=true --execute=false`.

### Environment variables

#### Scaling and parallelism

* `SF`: Scale factor — number of TPC-C warehouses or equivalent dataset size unit.
* `BEXHOMA_NUM_PODS`: Number of parallel generator pods.
* `BEXHOMA_CHILD`: Index of the current pod (1-based). Overwritten at runtime by the Redis queue entry.
* `BEXHOMA_RNGSEED`: Random seed. Currently ignored.

#### Target DBMS connection

The following variables are substituted into the selected XML config template via `sed`.

* `BEXHOMA_HOST`: Hostname of the target DBMS.
* `BEXHOMA_PORT`: Port of the target DBMS.
* `BEXHOMA_USER`: Database user.
* `BEXHOMA_PASSWORD`: Database password.
* `BEXHOMA_DATABASE`: Database name.
* `BEXHOMA_SCHEMA`: Schema name. Set automatically in multi-tenant (`schema`) mode; otherwise substituted as-is.
* `BEXHOMA_URL`: JDBC connection URL. Not used directly by the entrypoint script.
* `BEXHOMA_JAR`: JDBC driver jar file name. Not used directly by the entrypoint script.
* `BEXHOMA_DRIVER`: JDBC driver class name. Not used directly by the entrypoint script.

#### Bexhoma experiment identity

* `BEXHOMA_DBMS`: DBMS label. When set to `PGBouncer`, the schema query parameter is stripped from the XML config URL before substitution.
* `BEXHOMA_CONFIGURATION`: Configuration name. Echoed to the log.
* `BEXHOMA_CONNECTION`: Bexhoma connection name. Used to address the Redis message queue (`bexhoma-loading-<CONNECTION>-<EXPERIMENT>`).
* `BEXHOMA_EXPERIMENT`: Bexhoma experiment identifier. Used to address the Redis message queue.
* `BEXHOMA_EXPERIMENT_RUN`: Number of the current repetition of the complete experiment.
* `BEXHOMA_CLIENT`: Client index. Echoed to the log.

#### Multi-tenancy

* `BEXHOMA_TENANT_BY`: Tenant isolation strategy — `schema` (derives `BEXHOMA_SCHEMA` from `BEXHOMA_CHILD`), `database` (derives `BEXHOMA_DATABASE` from `BEXHOMA_CHILD`), `container` (enables cross-container sync barrier), or empty for no tenancy.
* `BEXHOMA_TENANT_NUM`: Total number of tenants. Echoed to the log.
* `BEXHOMA_NUM_PODS_TOTAL`: Total pods across all containers in a `container` tenancy run. Used for the experiment-level sync barrier on `bexhoma-benchmarker-podcount-<EXPERIMENT>`.

#### Pod synchronisation

An experiment-level sync barrier on `bexhoma-benchmarker-podcount-<EXPERIMENT>` is applied when `BEXHOMA_TENANT_BY=container`.

* `BEXHOMA_TIME_START`: Declared for compatibility; not used by the generator entrypoint script.
* `BEXHOMA_TIME_NOW`: Declared for compatibility; not used by the generator entrypoint script.

#### Benchbase workload parameters

* `BENCHBASE_BENCH`: Benchmark name — `tpcc`, `twitter`, `chbenchmark`, or `ycsb`.
* `BENCHBASE_PROFILE`: DBMS profile name. Selects the XML config subdirectory (e.g. `postgres`, `mysql`).
* `BENCHBASE_TARGET`: Target throughput. Substituted into the XML config (not meaningful for the load phase).
* `BENCHBASE_TIME`: Benchmark duration in seconds. Substituted into the XML config (not meaningful for the load phase).
* `BENCHBASE_TERMINALS`: Number of simulated client terminals. Substituted into the XML config.
* `BENCHBASE_BATCHSIZE`: Batch size for grouped query submission. Substituted into the XML config.
* `BENCHBASE_ISOLATION`: Transaction isolation level. Substituted into the XML config.
* `BENCHBASE_STATUS_INTERVAL`: When set to a positive integer, passes `--interval-monitor <N>` to Benchbase. Empty disables interval monitoring.
* `BENCHBASE_NEWCONNPERTXN`: When `true`, a new JDBC connection is opened for every transaction. Substituted into the XML config.
* `BENCHBASE_CREATE_SCHEMA`: When `true`, Benchbase creates the schema (`--create=true`) before loading data. Set to `false` when the schema is created outside these containers.
* `BENCHBASE_YCSB_WORKLOAD`: YCSB workload preset — `a`, `b`, `c`, `d`, `e`, or `f`. Automatically sets `BENCHBASE_YCSB_WEIGHTS` to the standard operation mix for that workload.
* `BENCHBASE_YCSB_WEIGHTS`: Comma-separated operation-type weights for YCSB (read, insert, scan, update, delete, readmodifywrite). Overridden by `BENCHBASE_YCSB_WORKLOAD` when set. Substituted into the XML config.

---

## XML config template placeholders

All XML templates under `config/` use the following uppercase tokens, which are
replaced by `sed` at container startup:

| Placeholder | Replaced with |
|---|---|
| `BEXHOMA_HOST` | Target DBMS hostname |
| `BEXHOMA_PORT` | Target DBMS port |
| `BEXHOMA_USER` | Database user |
| `BEXHOMA_PASSWORD` | Database password |
| `BEXHOMA_DATABASE` | Database name |
| `BEXHOMA_SCHEMA` | Schema name |
| `BEXHOMA_SF` | Scale factor (`SF`) |
| `BENCHBASE_TIME` | Benchmark duration in seconds |
| `BENCHBASE_TARGET` | Target throughput |
| `BENCHBASE_TERMINALS` | Number of client terminals |
| `BENCHBASE_BATCHSIZE` | Batch size |
| `BENCHBASE_ISOLATION` | Transaction isolation level |
| `BENCHBASE_NEWCONNPERTXN` | New connection per transaction flag |
| `BENCHBASE_YCSB_WEIGHTS` | YCSB operation-type weights |
