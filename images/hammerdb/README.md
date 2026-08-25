# HammerDB (TPC-C) images

Docker images for running TPC-C experiments within the Bexhoma framework using
HammerDB.

## Directory layout

```
images/hammerdb/
├── benchmarker/
│   ├── Dockerfile         — benchmarker image definition
│   ├── benchmarker.sh     — entrypoint: runs the timed TPC-C driver
│   └── README.md          — environment variable reference + execution flow
├── generator/
│   ├── Dockerfile         — generator image definition
│   ├── generator.sh       — entrypoint: runs HammerDB buildschema
│   └── README.md          — environment variable reference + execution flow
└── README.md              — this file
```

There is no `create_Dockerfile.py` here; both Dockerfiles are the canonical
source (not generated from a template).

Environment variables for each image are documented in that image's own README.
This file covers the shared design and decisions that apply across both.

---

## Key design decisions

| Decision | Reason |
|---|---|
| Benchmarker always synchronises | All parallel pods must start at the same time to measure concurrent throughput correctly; there is no `BEXHOMA_SYNCH_LOAD` skip flag |
| Generator has no Redis dependency | The TPC-C load is single-pod only; no key-space partitioning is needed |
| `runtimer` proc only in mysql/mariadb/citus | PostgreSQL's HammerDB driver does not require the explicit timer proc |
| `HAMMERDB_TIMEPROFILE=true` by default | The evaluator reads `/tmp/hdbxtprofile.log` to extract per-transaction latency statistics |

## Supported backends

| `HAMMERDB_TYPE` | HammerDB database key | Notes |
|---|---|---|
| `postgresql` | `pg` | Standard PostgreSQL TPC-C |
| `mysql` | `mysql` | Requires `mysql_ssl_options` workaround (see comments) |
| `mariadb` | `maria` | Same schema as MySQL |
| `citus` | `pg` | PostgreSQL + `pg_cituscompat true`, `pg_storedprocs false` |

## Style conventions

- **Dockerfiles**: `ENV` declarations use `KEY=value` form; grouped by concern
  under section headers.
- **Shell scripts**: Section banners use `#### Title ####`. No commented-out
  dead code; no debug write-only commands (`ls`, etc.).
- **READMEs**: One entry per ENV, grouped by concern, with clear descriptions of
  units and defaults; each includes that image's own execution flow.
