# Benchmarker for DBMSBenchmarker

The image is based on [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker).

This folder contains the Dockerfile template for a benchmarker that runs a DBMSBenchmarker
query workload against an already-loaded DBMS.

## Directory layout

```
images/benchmarker_dbmsbenchmarker/
├── Dockerfile_template    — image template; {version} replaced by create_Dockerfiles.py
├── create_Dockerfiles.py  — generates the versioned Dockerfile from Dockerfile_template
├── benchmarker.sh         — entrypoint: runs the timed DBMSBenchmarker workload
├── connections.config     — default DBMS connection config (used in TESTRUN mode)
├── queries.config         — default query config (used in TESTRUN mode)
└── README.md              — this file
```

`Dockerfile_template` is the canonical source. Do not edit generated `Dockerfile` files directly.
It contains the placeholder `{version}` which `create_Dockerfiles.py` replaces with the target
DBMSBenchmarker Git tag (e.g. `v0.14.6`). Both the pip install step and the `git clone` step use
the same tag to ensure consistency.

---

## Execution flow (`benchmarker.sh`)

1. Capture script start time.
2. Optionally sleep until `BEXHOMA_TIME_START` (synchronized start across pods).
3. Create `/results/$BEXHOMA_EXPERIMENT/` if it does not exist.
4. Pop the pod's child index from the Redis queue
   `bexhoma-benchmarker-<CONNECTION>-<EXPERIMENT>`.
5. **Multi-tenant adjustment**: if `BEXHOMA_TENANT_BY` is `schema` or `database`,
   divide `BEXHOMA_NUM_PODS` by `BEXHOMA_TENANT_NUM` and compute the per-tenant
   child index; override `BEXHOMA_SCHEMA` or `BEXHOMA_DATABASE` accordingly.
   Original values are saved so pod-count synchronisation uses the full count.
6. Increment and poll the Redis counter
   `bexhoma-benchmarker-podcount-<CONNECTION>-<EXPERIMENT>` until all
   `BEXHOMA_NUM_PODS` pods (full count) are ready.
7. If `BEXHOMA_TENANT_BY=container`, additionally wait on the cross-tenant counter
   `bexhoma-benchmarker-podcount-<EXPERIMENT>` until `BEXHOMA_NUM_PODS_TOTAL` pods
   are ready.
8. Restore per-tenant `BEXHOMA_CHILD` and `BEXHOMA_NUM_PODS`.
9. Convert `DBMSBENCHMARKER_SHUFFLE_QUERIES`, `DBMSBENCHMARKER_RECREATE_PARAMETER`,
   and `DBMSBENCHMARKER_VERBOSE_EXPLAIN` from Python boolean strings (`True`/`False`)
   to integers (`1`/`0`).
10. Run `python benchmark.py run` with the full flag set. Verbose mode adds
    `-d -vq -vr -vp -vs`. `-ve` is added independently of verbose mode, in both
    branches, whenever `DBMSBENCHMARKER_VERBOSE_EXPLAIN=1`.
11. Extract the precise benchmark duration from DBMSBenchmarker's log line
    `DBMSBenchmarker duration...: N [s]` and compute `bexhoma_end_epoch_computed`.
12. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END` to stdout.

### Multi-tenant modes

| `BEXHOMA_TENANT_BY` | Effect on `BEXHOMA_NUM_PODS` | Effect on `BEXHOMA_CHILD` | Override |
|---|---|---|---|
| `schema` | Divided by `BEXHOMA_TENANT_NUM` | `BEXHOMA_CHILD % BEXHOMA_TENANT_NUM + 1` | `BEXHOMA_SCHEMA=tenant_<N>` |
| `database` | Divided by `BEXHOMA_TENANT_NUM` | `BEXHOMA_CHILD % BEXHOMA_TENANT_NUM + 1` | `BEXHOMA_DATABASE=tenant_<N>` |
| `container` | Unchanged | Unchanged | Separate pod-count barrier on `BEXHOMA_NUM_PODS_TOTAL` |
| *(empty)* | Unchanged | Unchanged | None |

Pod-count synchronisation always uses the full `BEXHOMA_NUM_PODS` (restored before
the wait loop).

---

## Key design decisions

| Decision | Reason |
|---|---|
| `DBMSBENCHMARKER_CODE` has no Docker ENV default | The value is used in a `RUN mkdir` build step; giving it an ENV default would cause Docker to create a mis-named directory at image build time |
| Timing uses wall-clock epoch, then refined | DBMSBenchmarker reports its internal duration; the script computes `END = START + duration` for higher precision than a post-run `date` call |
| Python boolean conversion before flag expansion | DBMSBenchmarker's environment variables use Python `True`/`False` strings; shell needs integers for arithmetic tests |
| Disabled `-sl` and `-st` flags | Timing is handled by the shell (`BEXHOMA_TIME_START` sleep); passing them again to DBMSBenchmarker would double-count the wait |
| Verbose and non-verbose paths are two explicit branches | Makes the non-verbose case self-contained and easy to read; no conditional flag assembly needed |

---

## DBMSBenchmarker CLI flags

| Flag | Argument | Meaning |
|---|---|---|
| `-f` / `-r` | `DBMSBENCHMARKER_CODE` | Config and result base folder |
| `-cs -sf` | `DBMSBENCHMARKER_CONNECTION` | Create sub-folder per DBMS connection |
| `-ms` | `DBMSBENCHMARKER_CLIENT` | Maximum number of connection sub-folders |
| `-c` | `DBMSBENCHMARKER_CONNECTION` | DBMS connection name to benchmark |
| `-ca` | `DBMSBENCHMARKER_ALIAS` | Alias for the DBMS connection |
| `-cf` | `<CONNECTION>.config` | Per-connection config file |
| `-rcp` | `0` or `1` | Recreate query parameters per stream |
| `-sid` | `BEXHOMA_CHILD` | Stream ID for parallel execution |
| `-ssh` | `0` or `1` | Shuffle query order by stream ID |
| `-mps` | *(flag)* | Monitor per stream, not per query |
| `-fixdb` | `BEXHOMA_DATABASE` | Override the database name |
| `-fixs` | `BEXHOMA_SCHEMA` | Override the schema name |
| `-d -vq -vr -vp -vs` | *(flags)* | Verbose output (verbose mode only) |
| `-db` | *(flag)* | Debug mode (dev mode only) |
| `-ve` | *(flag)* | Run and print configured EXPLAIN statements after each query (independent of verbose/dev mode, see `DBMSBENCHMARKER_VERBOSE_EXPLAIN`) |

---

## Environment variables

### Scaling and parallelism

* `SF`: Scaling factor. Passed to the benchmark configuration to control the dataset size.
* `BEXHOMA_NUM_PODS`: Number of parallel pods in the Kubernetes job. Used for pod-count synchronisation.
* `BEXHOMA_CHILD`: Index of the current pod (1-based). Overwritten at runtime by the Redis queue entry.
* `BEXHOMA_RNGSEED`: Random seed. Currently passed as context but not consumed by DBMSBenchmarker directly.

### Target DBMS connection

* `BEXHOMA_URL`: JDBC connection URL (e.g. `jdbc:mysql://localhost:3306/ycsb`). Written into the per-connection config file.
* `BEXHOMA_HOST`: Hostname of the target DBMS.
* `BEXHOMA_PORT`: Port of the target DBMS.
* `BEXHOMA_JAR`: JDBC driver jar file name (must exist in `jars/` inside the image — see Dockerfile for bundled drivers).
* `BEXHOMA_DRIVER`: JDBC driver class name (e.g. `com.mysql.cj.jdbc.Driver`).
* `BEXHOMA_USER`: Database username.
* `BEXHOMA_PASSWORD`: Database password.
* `BEXHOMA_DATABASE`: Database (catalog) name. Passed to DBMSBenchmarker via `-fixdb`. In `database` tenancy mode this is overridden to `tenant_<N>`.
* `BEXHOMA_SCHEMA`: Schema name. Passed to DBMSBenchmarker via `-fixs`. In `schema` tenancy mode this is overridden to `tenant_<N>`.

### Bexhoma experiment identity

* `BEXHOMA_DBMS`: DBMS type identifier (e.g. `postgresql`). Informational only.
* `BEXHOMA_CONFIGURATION`: Bexhoma configuration name. Informational only.
* `BEXHOMA_CONNECTION`: Bexhoma connection name. Used to address the Redis message queue and counter keys.
* `BEXHOMA_EXPERIMENT`: Bexhoma experiment identifier. Used to address the Redis message queue and counter keys, and to name the result sub-folder.
* `BEXHOMA_EXPERIMENT_RUN`: Number of the current repetition of the complete experiment.
* `BEXHOMA_CLIENT`: Client index (1-based) within the current run. Used as the upper bound on result sub-folders (`-ms`).

### Pod synchronisation

* `BEXHOMA_TIME_START`: Optional RFC-3339 timestamp. When non-zero, the pod sleeps until this time before proceeding.
* `BEXHOMA_TIME_NOW`: Informational timestamp of the planned start, echoed to the log.

### Multi-tenant parameters

* `BEXHOMA_TENANT_BY`: Tenancy mode. One of `schema`, `database`, or `container`. Empty means no multi-tenant mode. Controls how `BEXHOMA_CHILD` and `BEXHOMA_NUM_PODS` are adjusted before the benchmark run.
* `BEXHOMA_TENANT_NUM`: Number of tenants. Used to partition `BEXHOMA_NUM_PODS` and compute the per-tenant child index. Default: `1`.
* `BEXHOMA_NUM_PODS_TOTAL`: Total number of pods across all tenants. Used for the cross-tenant pod-count barrier when `BEXHOMA_TENANT_BY=container`. Default: `4`.

### DBMSBenchmarker parameters

* `DBMSBENCHMARKER_CODE`: Experiment code used as the result folder name (`/results/<CODE>`). No Docker default — must be set at runtime.
* `DBMSBENCHMARKER_CONNECTION`: DBMSBenchmarker connection name. Passed via `-c` and used to locate the per-connection config file (`<CONNECTION>.config`). Should match `BEXHOMA_CONNECTION`.
* `DBMSBENCHMARKER_ALIAS`: Alias for the DBMS connection. Passed via `-ca`.
* `DBMSBENCHMARKER_CLIENT`: Maximum number of per-connection result sub-folders. Passed via `-ms`. Should match `BEXHOMA_CLIENT`.
* `DBMSBENCHMARKER_SLEEP`: Sleep seconds before benchmarking. Kept for reference; timing is handled by the shell via `BEXHOMA_TIME_START` instead.
* `DBMSBENCHMARKER_RECREATE_PARAMETER`: When `True`, force recreation of query parameters for each stream (`-rcp 1`). Default: `False` (all streams share the same parameters).
* `DBMSBENCHMARKER_VERBOSE`: When non-zero, enable verbose output flags (`-d -vq -vr -vp -vs`). Default: `0`.
* `DBMSBENCHMARKER_DEV`: When non-zero, check out the `dev` branch of the cloned repository and pass `-db` to DBMSBenchmarker. Default: `0`.
* `DBMSBENCHMARKER_SHUFFLE_QUERIES`: When `True`, randomise query order per stream (`-ssh 1`). Default: `False`.
* `DBMSBENCHMARKER_VERBOSE_EXPLAIN`: When `True`, pass `-ve` so DBMSBenchmarker runs and prints any `explain` statements configured in the DBMS connection's JDBC config right after each benchmark query. Default: `False`.
* `DBMSBENCHMARKER_TESTRUN`: When non-zero, run a quick self-test (TPC-DS against MonetDB at localhost) and exit immediately. Default: `0`.

## Bundled JDBC drivers

| Driver | Version | Jar |
|---|---|---|
| PostgreSQL | 42.5.0 | `postgresql-42.5.0.jar` |
| MySQL | 8.0.31 | `mysql-connector-j-8.0.31.jar` |
| MariaDB | 3.1.0 | `mariadb-java-client-3.1.0.jar` |
| MonetDB | 12.1 (jre8) | `monetdb-jdbc-12.1.jre8.jar` |
| MonetDB | 12.2 (jre8) | `monetdb-jdbc-12.2.jre8.jar` |
| SingleStore | 1.1.4 | `singlestore-jdbc-client-1.1.4.jar` |
| YugabyteDB | 42.3.5-yb-2 | `jdbc-yugabytedb-42.3.5-yb-2.jar` |

See [DBMSBenchmarker docs](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) for details
on the query workload configuration.

---

## Style conventions

- **Dockerfile_template**: `ENV` declarations use `KEY=value` form; grouped by concern
  under section headers. The `{version}` placeholder appears only in the two
  DBMSBenchmarker install/clone steps.
- **Shell scripts**: Section banners use `#### Title ####`. No commented-out dead
  code; no debug write-only commands.
- **This README**: One entry per ENV, grouped by concern, with clear descriptions of
  units and defaults.
