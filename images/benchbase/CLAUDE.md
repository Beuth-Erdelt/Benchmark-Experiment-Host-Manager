# images/benchbase — development notes

## Overview

The `images/benchbase/` directory contains Docker images for running Benchbase
experiments within the Bexhoma framework.

## Directory layout

```
images/benchbase/
├── Dockerfile_benchmarker   — benchmarker image definition
├── Dockerfile_generator     — generator image definition
├── benchmarker.sh           — entrypoint: runs the Benchbase execute phase
├── generator.sh             — entrypoint: runs the Benchbase load phase
├── config/                  — XML config templates, one subdirectory per profile
│   ├── postgres/
│   ├── mysql/
│   ├── mariadb/
│   ├── cockroachdb/
│   ├── noisepage/
│   ├── spanner/
│   ├── sqlite/
│   ├── sqlserver/
│   └── phoenix/
└── README.md                — environment variable reference for both images
```

**Important:** unlike `images/hammerdb/` and `images/ycsb/`, the benchbase folder
uses a **flat structure** — both Dockerfiles and both shell scripts live at the
folder root.  There are no `benchmarker/` or `generator/` subdirectories.
The README covers both images in a single file with two sections.

---

## Execution flow

### Benchmarker pod (`benchmarker.sh`)

1. Capture script start time.
2. Optionally sleep until `BEXHOMA_TIME_START` (synchronised start across pods).
3. Pop the pod's child index from the Redis queue
   `bexhoma-benchmarker-<CONNECTION>-<EXPERIMENT>`.
4. Multi-tenant handling:
   - `BEXHOMA_TENANT_BY=schema` → set `BEXHOMA_SCHEMA=tenant_<N>`, temporarily
     force `BEXHOMA_NUM_PODS=1` for the per-job sync.
   - `BEXHOMA_TENANT_BY=database` → set `BEXHOMA_DATABASE=tenant_<N>`,
     temporarily force `BEXHOMA_NUM_PODS=1`.
   - Otherwise → no change.
5. Increment and poll the Redis counter
   `bexhoma-benchmarker-podcount-<CONNECTION>-<EXPERIMENT>` until all
   `BEXHOMA_NUM_PODS` pods are ready (synchronisation is **unconditional**).
6. If `BEXHOMA_TENANT_BY=container`: also sync on the experiment-level counter
   `bexhoma-benchmarker-podcount-<EXPERIMENT>` (waits for `BEXHOMA_NUM_PODS_TOTAL`).
7. Select the XML config file:
   `/tmp/config/<BENCHBASE_PROFILE>/sample_<BENCHBASE_BENCH>_config.xml`.
8. If `BEXHOMA_DBMS=PGBouncer`: strip `&amp;currentSchema=BEXHOMA_SCHEMA` from
   the URL in the XML file before substitution.
9. If `BENCHBASE_BENCH=ycsb`: derive `BENCHBASE_YCSB_WEIGHTS` from
   `BENCHBASE_YCSB_WORKLOAD` (standard workload a–f mixes).
10. Substitute all placeholder tokens into the XML config via `sed`.
11. If `BENCHBASE_KEY_AND_THINK=true`: uncomment `<preExecutionWait>` and
    `<postExecutionWait>` blocks in the XML config.
12. Run `./entrypoint.sh run --bench $BENCHBASE_BENCH -c $FILENAME
    --create=false --load=false --execute=true
    [--interval-monitor $BENCHBASE_STATUS_INTERVAL]`.
13. Print `/benchbase/results/*.summary.json` wrapped in `####BEXHOMA####` markers.
14. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END` to stdout for the
    evaluator.

### Generator pod (`generator.sh`)

Same as the benchmarker except:

- Queue key uses `bexhoma-loading-` prefix:
  `bexhoma-loading-<CONNECTION>-<EXPERIMENT>`.
- There is **no unconditional per-job sync barrier** — only the
  `BEXHOMA_TENANT_BY=container` experiment-level barrier applies.
- `BENCHBASE_KEY_AND_THINK` logic is absent (no think-time activation).
- Runs with `--create=$BENCHBASE_CREATE_SCHEMA --load=true --execute=false`.
- `chbenchmark` sets the bench string to `tpcc,chbenchmark` for the Benchbase
  invocation (both sub-benchmarks must be named).

---

## Key design decisions

| Decision | Reason |
|---|---|
| Flat directory structure | The benchbase folder predates the hammerdb/ycsb subdirectory convention; restructuring was not done to avoid breaking build scripts |
| Benchmarker always synchronises | All parallel pods must start at the same time to measure concurrent throughput correctly |
| Generator has no per-job sync | Data loading is typically single-pod; multi-pod loads are coordinated by the caller, not the container |
| `BENCHBASE_KEY_AND_THINK` toggles XML comments | Benchbase uses commented-out XML blocks for think time; `sed` uncomments them rather than injecting new XML |
| `BENCHBASE_CREATE_SCHEMA` only in generator | Schema creation is a one-time setup step done during loading, never during benchmarking |
| `BEXHOMA_URL`, `BEXHOMA_JAR`, `BEXHOMA_DRIVER` declared but unused | Legacy declarations kept for compatibility; the entrypoint scripts use `BEXHOMA_HOST`/`PORT`/`USER`/`PASSWORD` directly via XML substitution |
| Multi-tenancy via `BEXHOMA_TENANT_BY` | Supports three isolation modes: `schema` (one schema per pod), `database` (one database per pod), `container` (one benchmarker job per tenant, global sync required) |

---

## Supported benchmarks

| `BENCHBASE_BENCH` | Config file selected | Notes |
|---|---|---|
| `tpcc` | `sample_tpcc_config.xml` | |
| `twitter` | `sample_twitter_config.xml` | |
| `chbenchmark` | `sample_chbenchmark_config.xml` | Bench string becomes `tpcc,chbenchmark` at runtime |
| `ycsb` | `sample_ycsb_config.xml` | Weights derived from `BENCHBASE_YCSB_WORKLOAD` |

---

## YCSB workload weight mapping

`BENCHBASE_YCSB_WORKLOAD` overrides `BENCHBASE_YCSB_WEIGHTS` with these standard mixes
(read, insert, scan, update, delete, readmodifywrite):

| Workload | Weights |
|---|---|
| `a` | `50,0,0,50,0,0` |
| `b` | `95,0,0,5,0,0` |
| `c` | `100,0,0,0,0,0` |
| `d` | `95,5,0,0,0,0` |
| `e` | `0,5,95,0,0,0` |
| `f` | `50,0,0,0,0,50` |

---

## XML config template placeholders

All templates under `config/` use these uppercase tokens substituted by `sed` at
container startup:

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

---

## Style conventions

- **Dockerfiles**: `ENV` declarations use `KEY=value` form; grouped by concern
  under section headers.  Both Dockerfiles share the same ENV layout; the only
  differences are `BENCHBASE_KEY_AND_THINK` (benchmarker only) vs
  `BENCHBASE_CREATE_SCHEMA` (generator only).
- **Shell scripts**: Section banners use `#### Title ####`.  No commented-out
  dead code.
- **README**: Single file covering both images; split into two `##` sections with
  identical ENV group structure.
