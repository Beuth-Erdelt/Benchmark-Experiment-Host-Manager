# images/ycsb — development notes

## Overview

The `images/ycsb/` directory contains Docker images for running YCSB (Yahoo Cloud
Serving Benchmark) experiments within the Bexhoma framework.

## Directory layout

```
images/ycsb/
├── benchmarker/
│   ├── Dockerfile         — benchmarker image definition
│   ├── benchmarker.sh     — entrypoint: runs 'ycsb run'
│   ├── workloads/         — YCSB workload template files (a–f)
│   └── README.md          — environment variable reference
└── generator/
    ├── Dockerfile         — generator image definition
    ├── generator.sh       — entrypoint: runs 'ycsb load'
    ├── workloads/         — YCSB workload template files (a–f)
    └── README.md          — environment variable reference
```

There is no `create_Dockerfile.py` here, so both Dockerfiles are the canonical
source (not generated from a template).

---

## Execution flow

### Benchmarker pod (`benchmarker.sh`)

1. Capture script start time.
2. Optionally sleep until `BEXHOMA_TIME_START` (synchronized start across pods).
3. Pop the pod's child index from the Redis queue
   `bexhoma-benchmarker-<CONNECTION>-<EXPERIMENT>`.
4. Compute row-range parameters; override to full key range
   (`ROW_START=0`, `ROW_PART=YCSB_ROWS`) so every benchmarking pod covers the
   complete dataset.
5. Increment and poll the Redis counter
   `bexhoma-benchmarker-podcount-<CONNECTION>-<EXPERIMENT>` until all
   `BEXHOMA_NUM_PODS` pods are ready.
6. Write `db.properties` (JDBC or Redis branch, optionally with batch settings).
7. Copy workload template → `/tmp/workload`; substitute placeholder tokens via
   `sed`.
8. Run `ycsb run` (redis / redis-cluster / jdbc branch, with or without `-s`).
9. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END` to stdout for the
   evaluator.

### Generator pod (`generator.sh`)

Same as benchmarker except:

- Queue key is `bexhoma-loading-<CONNECTION>-<EXPERIMENT>`.
- Counter key is `bexhoma-loader-podcount-<CONNECTION>-<EXPERIMENT>`.
- Row partitioning is **per-pod** (`ROW_PART = YCSB_ROWS / BEXHOMA_NUM_PODS`,
  `ROW_START = ROW_PART × (BEXHOMA_CHILD − 1)`) so each pod loads a distinct
  slice of keys without overlap.
- Runs `ycsb load` instead of `ycsb run`.

---

## Key design decisions

| Decision | Reason |
|---|---|
| Benchmarker uses full key range | All parallel pods must see the same dataset; partitioning the read workload would skew results |
| Generator partitions the key space | Parallel loading requires each pod to insert a non-overlapping row range |
| `ROWS_TO_INSERT = OPERATIONS_TOTAL` in the generator | During load, 100 % of operations are INSERTs; the 5 % figure only applies to the benchmark's insert proportion in workloads D/E |
| jemalloc built from source | Better memory allocation performance for Java workloads on Alpine |
| redis-cli built from source | Alpine packages may lag behind; a known-good stable build is embedded |

---

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

---

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

---

## Style conventions

- **Dockerfiles**: `ENV` declarations use `KEY=value` form; grouped by concern
  under section headers.  Each JDBC driver download is a single `RUN` layer.
- **Shell scripts**: Section banners use `#### Title ####`.  No commented-out
  dead code; no debug write-only files.
- **READMEs**: One entry per ENV, grouped by concern, with clear descriptions of
  units and defaults.
