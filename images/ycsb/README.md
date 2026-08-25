# YCSB images

Docker images for running YCSB (Yahoo Cloud Serving Benchmark) experiments
within the Bexhoma framework.

## Directory layout

```
images/ycsb/
├── benchmarker/
│   ├── Dockerfile         — benchmarker image definition
│   ├── benchmarker.sh     — entrypoint: runs 'ycsb run'
│   ├── workloads/         — YCSB workload template files (a–f)
│   └── README.md          — environment variable reference + execution flow
├── generator/
│   ├── Dockerfile         — generator image definition
│   ├── generator.sh       — entrypoint: runs 'ycsb load'
│   ├── workloads/         — YCSB workload template files (a–f)
│   └── README.md          — environment variable reference + execution flow
└── README.md              — this file
```

There is no `create_Dockerfile.py` here, so both Dockerfiles are the canonical
source (not generated from a template).

Environment variables for each image are documented in that image's own README.
This file covers the shared design and decisions that apply across both.

---

## Key design decisions

| Decision | Reason |
|---|---|
| Benchmarker uses full key range | All parallel pods must see the same dataset; partitioning the read workload would skew results |
| Generator partitions the key space | Parallel loading requires each pod to insert a non-overlapping row range |
| `ROWS_TO_INSERT = OPERATIONS_TOTAL` in the generator | During load, 100 % of operations are INSERTs; the 5 % figure only applies to the benchmark's insert proportion in workloads D/E |
| jemalloc built from source | Better memory allocation performance for Java workloads on Alpine |
| redis-cli built from source | Alpine packages may lag behind; a known-good stable build is embedded |

## Included JDBC drivers

| Driver | Version | Jar |
|---|---|---|
| PostgreSQL | 42.5.0 | `postgresql-42.5.0.jar` |
| MySQL | 8.0.31 | `mysql-connector-j-8.0.31.jar` |
| MariaDB | 3.1.0 | `mariadb-java-client-3.1.0.jar` |
| MonetDB | 3.2 (jre8) | `monetdb-jdbc-3.2.jre8.jar` |
| SingleStore | 1.1.4 | `singlestore-jdbc-client-1.1.4.jar` |
| Kinetica | 7.1.8.7 | `kinetica-jdbc-7.1.8.7-jar-with-dependencies.jar` |
| YugabyteDB | 42.3.5-yb-2 | `jdbc-yugabytedb-42.3.5-yb-2.jar` |
| YugabyteDB | 42.7.3-yb-3 | `jdbc-yugabytedb-42.7.3-yb-3.jar` (generator only) |

## Workload template placeholders

The workload files under `workloads/` contain uppercase tokens that are replaced
by `sed` at container startup:

| Placeholder | Replaced with |
|---|---|
| `YCSB_ROWS` | Total record count |
| `YCSB_OPERATIONS` | Operations per pod |
| `OPERATIONS_TOTAL` | Total operations across all pods |
| `ROW_START` | Start key for this pod's insert range |
| `ROW_PART` | Key count for this pod's insert range |
| `ROW_START_AFTER_LOADING` | Insert start offset after initial load |
| `ROW_PART_AFTER_LOADING` | Insert count after initial load |
| `ROWS_AFTER_BENCHMARK` | Total record count after benchmark inserts |
| `YCSB_THREADCOUNT` | Thread count |
| `YCSB_TARGET` | Target throughput cap |
| `YCSB_STATUS_INTERVAL` | Status reporting interval (seconds) |
| `YCSB_MEASUREMENT_TYPE` | Measurement type (`hdrhistogram` / `histogram`) |
| `YCSB_INSERTORDER` | Insert order (`hashed` / `ordered`) |

## Command-line flags built at runtime

These environment variables are not substituted into the workload file but are
used to build optional `-p` arguments passed directly to the `bin/ycsb` command:

| Variable | YCSB property | Notes |
|---|---|---|
| `YCSB_MAX_EXECUTION` | `maxexecutiontime` | Seconds; 0 (default) means no limit; flag is omitted when 0 |

## Style conventions

- **Dockerfiles**: `ENV` declarations use `KEY=value` form; grouped by concern
  under section headers. Each JDBC driver download is a single `RUN` layer.
- **Shell scripts**: Section banners use `#### Title ####`. No commented-out
  dead code; no debug write-only files.
- **READMEs**: One entry per ENV, grouped by concern, with clear descriptions of
  units and defaults; each includes that image's own execution flow.
