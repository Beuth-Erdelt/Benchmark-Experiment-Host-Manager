# images/tpch_refresh — development notes

## Overview

Two-container pipeline for the TPC-H refresh stream benchmarker: a generator
initContainer creates update files on the PVC, then the loader main container reads
them and applies RF1/RF2 to the target DBMS.  This mirrors the `images/tpch/`
structure exactly.

## Directory layout

```
images/tpch_refresh/
├── generator/
│   ├── Dockerfile         — generator image (debian:stable-slim + redis-cli + dbgen)
│   ├── generator.sh       — generates update files via dbgen -U N
│   └── README.md
├── loader_postgresql/
│   ├── Dockerfile         — PostgreSQL loader image (alpine + psql + redis-cli)
│   ├── loader.sh          — applies RF1 via \COPY, RF2 via temp table + bulk DELETE
│   └── README.md
└── loader_mysql/
    ├── Dockerfile         — MySQL loader image (debian:stable-slim + mysql-client + redis-cli)
    ├── loader.sh          — applies RF1 via LOAD DATA LOCAL INFILE, RF2 via temp table + DELETE
    └── README.md
```

## Generator execution flow (`generator.sh`)

1. Compute `LAST_SET = TPCH_REFRESH_STREAM_OFFSET + TPCH_REFRESH_STREAMS`.
2. Determine `destination_raw`: `/data/tpch-refresh/SF<SF>/` if `STORE_RAW_DATA=1`,
   else `/tmp/tpch-refresh/SF<SF>/`.
3. **Fast exit** if `delete.$LAST_SET` already exists — emits timing and exits 0.
4. Copy `dbgen` and `dists.dss` into `destination_raw`, run
   `./dbgen -s SF -U LAST_SET`, then remove the executables.
   Existing sets (lower K) are overwritten with identical deterministic content —
   harmless because `dbgen` output is fully determined by SF and set number.
5. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

## Loader execution flow (common to all DBMS variants)

1. Compute `FIRST_SET = OFFSET+1`, `LAST_SET = OFFSET+STREAMS`.
2. Determine `destination_raw` (same logic as generator).
3. Sync: decrement **job counter** `bexhoma-benchmarker-podcount-job-<CONNECTION>-<EXPERIMENT>`,
   poll until ≤ 0.
4. Sync: decrement **round counter**
   `bexhoma-benchmarker-podcount-round-<EXPERIMENT_RUN>-<CLIENT>-<EXPERIMENT>`,
   poll until ≤ 0.  This ensures the refresh stream starts at the same moment as
   the parallel query stream (benchmark_run=1).
5. For K in FIRST_SET..LAST_SET:
   - **RF1** — insert `orders.tbl.uK` then `lineitem.tbl.uK` into the DBMS.
   - **RF2** — load `delete.K` (one orderkey per line) into a temporary table,
     bulk-DELETE matching rows from `lineitem` and `orders`, drop the temp table.
6. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

## Key design decisions

| Decision | Reason |
|---|---|
| Generator runs as initContainer of the benchmarker job | Data generation is coupled to the benchmark run; PVC caching (fast-exit) makes subsequent runs cheap |
| `destination_raw` has no child sub-path | `dbgen -U N` is not parallelisable across pods; one pod generates all N sets |
| Overwrite existing lower sets without guard | `dbgen` is deterministic: same SF + same set number → identical bytes; overwriting is harmless |
| Fast-exit check on `delete.$LAST_SET` | The last file is the most likely to be missing when LAST_SET grows; checking it is sufficient |
| Loader uses benchmarker Redis counters | The loader runs as `benchmark_run=2`, not as a loader pod; it must synchronise with the round counter to start in parallel with the query stream |
| MySQL uses `BEXHOMA_VOLUME` as database name | Matches the existing MySQL loader convention in `images/tpch/loader_mysql/` |

## Build note

`dbgen` and `dists.dss` must be copied from `images/tpch/generator/` into
`images/tpch_refresh/generator/` before building the generator image.

## Repeated runs / state

After applying sets OFFSET+1..OFFSET+STREAMS, the database has changed.
Running again with the same OFFSET will cause RF1 primary-key violations.
Advance `TPCH_REFRESH_STREAM_OFFSET` by `TPCH_REFRESH_STREAMS` between runs,
or reload the database before repeating.

## Per-DBMS loader differences

| DBMS | Tool | RF1 | RF2 |
|---|---|---|---|
| PostgreSQL | `psql \COPY` | `\COPY orders/lineitem FROM file` | temp table + `DELETE ... IN (SELECT ...)` via heredoc |
| MySQL | `mysql LOAD DATA LOCAL INFILE` | column-mapped LOAD DATA per table | temp table + `DELETE l FROM lineitem l WHERE ...` |
