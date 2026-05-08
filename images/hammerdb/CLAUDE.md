# images/hammerdb — development notes

## Overview

The `images/hammerdb/` directory contains Docker images for running TPC-C
experiments within the Bexhoma framework using HammerDB.

## Directory layout

```
images/hammerdb/
├── benchmarker/
│   ├── Dockerfile         — benchmarker image definition
│   ├── benchmarker.sh     — entrypoint: runs the timed TPC-C driver
│   └── README.md          — environment variable reference
└── generator/
    ├── Dockerfile         — generator image definition
    ├── generator.sh       — entrypoint: runs HammerDB buildschema
    └── README.md          — environment variable reference
```

There is no `create_Dockerfile.py` here; both Dockerfiles are the canonical
source (not generated from a template).

---

## Execution flow

### Benchmarker pod (`benchmarker.sh`)

1. Capture script start time.
2. Optionally sleep until `BEXHOMA_TIME_START` (synchronised start across pods).
3. Pop the pod's child index from the Redis queue
   `bexhoma-benchmarker-<CONNECTION>-<EXPERIMENT>`.
4. Increment and poll the Redis counter
   `bexhoma-benchmarker-podcount-<CONNECTION>-<EXPERIMENT>` until all
   `BEXHOMA_NUM_PODS` pods are ready (synchronisation is unconditional).
5. Generate a `benchmark.tcl` script tailored to `HAMMERDB_TYPE`
   (postgresql / mysql / mariadb / citus).
6. Run `hammerdbcli auto benchmark.tcl`.
7. Copy `/tmp/hammerdb.log` into the result folder as
   `hammerdb.<CONNECTION>.<CLIENT>.<UUID>.log`.
8. Print `/tmp/hdbxtprofile.log` (per-transaction latency profile, when
   `HAMMERDB_TIMEPROFILE=true`).
9. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END` to stdout for the
   evaluator.

### Generator pod (`generator.sh`)

1. Capture script start time.
2. Generate a `load.tcl` script tailored to `HAMMERDB_TYPE`.
3. Run `hammerdbcli auto load.tcl` (calls HammerDB `buildschema`).
4. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END` to stdout.

The generator does **not** use Redis — it starts immediately and loads
the full warehouse set without pod coordination.

---

## Key design decisions

| Decision | Reason |
|---|---|
| Benchmarker always synchronises | All parallel pods must start at the same time to measure concurrent throughput correctly; there is no `BEXHOMA_SYNCH_LOAD` skip flag |
| Generator has no Redis dependency | The TPC-C load is single-pod only; no key-space partitioning is needed |
| `runtimer` proc only in mysql/mariadb/citus | PostgreSQL's HammerDB driver does not require the explicit timer proc |
| `HAMMERDB_TIMEPROFILE=true` by default | The evaluator reads `/tmp/hdbxtprofile.log` to extract per-transaction latency statistics |

---

## Supported backends

| `HAMMERDB_TYPE` | HammerDB database key | Notes |
|---|---|---|
| `postgresql` | `pg` | Standard PostgreSQL TPC-C |
| `mysql` | `mysql` | Requires `mysql_ssl_options` workaround (see comments) |
| `mariadb` | `maria` | Same schema as MySQL |
| `citus` | `pg` | PostgreSQL + `pg_cituscompat true`, `pg_storedprocs false` |

---

## Style conventions

- **Dockerfiles**: `ENV` declarations use `KEY=value` form; grouped by concern
  under section headers.
- **Shell scripts**: Section banners use `#### Title ####`.  No commented-out
  dead code; no debug write-only commands (`ls`, etc.).
- **READMEs**: One entry per ENV, grouped by concern, with clear descriptions of
  units and defaults.
