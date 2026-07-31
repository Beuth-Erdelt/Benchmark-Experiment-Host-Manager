# TPC-H refresh stream images

Two-container pipeline for the TPC-H refresh stream benchmarker: a generator
initContainer creates update files on the PVC, then the loader main container
reads them and applies RF1/RF2 to the target DBMS. This mirrors the
`images/tpch/` structure, but the loader runs as `benchmark_run=2` alongside
the query-stream benchmarker (`benchmark_run=1`) instead of as a standalone
loader pod.

## Directory layout

```
images/tpch_refresh/
├── generator/
│   ├── Dockerfile         — generator image (debian:stable-slim + redis-cli + dbgen)
│   ├── generator.sh       — generates update files via dbgen -U N
│   └── README.md          — environment variable reference + execution flow
├── loader_postgresql/
│   ├── Dockerfile         — PostgreSQL loader image (alpine + psql + redis-cli)
│   ├── loader.sh          — applies RF1 via \COPY, RF2 via temp table + bulk DELETE
│   └── README.md          — environment variable reference + execution flow
├── loader_mysql/
│   ├── Dockerfile         — MySQL loader image (debian:stable-slim + mysql-client + redis-cli)
│   ├── loader.sh          — applies RF1 via LOAD DATA LOCAL INFILE, RF2 via temp table + DELETE
│   └── README.md          — environment variable reference + execution flow
├── loader_mariadb/
│   ├── Dockerfile         — MariaDB loader image (debian:stable-slim + mariadb-client + redis-cli)
│   ├── loader.sh          — applies RF1 via LOAD DATA LOCAL INFILE, RF2 via temp table + DELETE
│   └── README.md          — environment variable reference + execution flow
├── loader_monetdb/
│   ├── Dockerfile         — MonetDB loader image (monetdb/monetdb:Dec2025 + redis + yum)
│   ├── loader.sh          — applies RF1 via mclient COPY FROM STDIN, RF2 via piped session
│   └── README.md          — environment variable reference + execution flow
└── README.md              — this file
```

Environment variables for each image are documented in that image's own README.
This file covers the shared pipeline design and decisions that apply across all
of them.

---

## Key design decisions

| Decision | Reason |
|---|---|
| Generator runs as initContainer of the benchmarker job | Data generation is coupled to the benchmark run; PVC caching (fast-exit) makes subsequent runs cheap |
| `destination_raw` has no child sub-path | `dbgen -U N` is not parallelisable across pods; one pod generates all N sets |
| Overwrite existing lower sets without guard | `dbgen` is deterministic: same SF + same set number → identical bytes; overwriting is harmless |
| Fast-exit check on `delete.$LAST_SET` | The last file is the most likely to be missing when LAST_SET grows; checking it is sufficient |
| Loader uses benchmarker Redis counters | The loader runs as `benchmark_run=2`, not as a loader pod; it must synchronise with the round counter to start in parallel with the query stream |
| MySQL/MariaDB use `BEXHOMA_VOLUME` as database name | Matches the existing MySQL/MariaDB loader convention in `images/tpch/loader_mysql/` and `images/tpch/loader_mariadb/` |
| MonetDB RF2 uses a single piped mclient session | `mclient` reads the N data records from stdin immediately after `COPY N RECORDS INTO ... FROM STDIN`, then continues reading SQL from the same stdin stream; the temporary table therefore persists across statements |

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
| MariaDB | `mysql LOAD DATA LOCAL INFILE` | column-mapped LOAD DATA per table | temp table + `DELETE l FROM lineitem l WHERE ...` |
| MonetDB | `mclient COPY N RECORDS INTO ... FROM STDIN` | count lines, pipe file to mclient per table | all statements in one stdin pipeline; temp table persists within the session |
