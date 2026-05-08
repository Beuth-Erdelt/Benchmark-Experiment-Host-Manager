# images/tpch — development notes

## Overview
Two-phase pipeline: a generator pod creates flat files on disk, then one or more loader pods read those files and insert them into a target DBMS.

## Directory layout
```
images/tpch/
├── generator/
│   ├── Dockerfile         — generator image
│   ├── generator.sh       — generates .tbl files via dbgen
│   ├── dbgen              — pre-compiled TPC-H generator binary (not in git)
│   ├── dists.dss          — dbgen distribution file
│   └── README.md
├── loader_postgresql/
│   ├── Dockerfile         — PostgreSQL loader image
│   ├── loader.sh          — loads .tbl via psql \COPY
│   └── README.md
├── loader_mysql/
│   ├── Dockerfile         — MySQL loader image
│   ├── loader.sh          — loads .tbl via mysql LOAD DATA LOCAL INFILE
│   ├── loader-parallel.sh — alternative using mysqlsh util.import_table (inactive)
│   └── README.md
├── loader_mariadb/
│   ├── Dockerfile         — MariaDB loader image
│   ├── loader.sh          — loads .tbl via mysql LOAD DATA LOCAL INFILE
│   └── README.md
└── loader_monetdb/
    ├── Dockerfile         — MonetDB loader image
    ├── loader.sh          — loads .tbl via mclient COPY FROM STDIN
    └── README.md
```

## Generator execution flow (`generator.sh`)
1. Pop child index from Redis queue `bexhoma-loading-<CONNECTION>-<EXPERIMENT>`.
2. Write child index to `/tmp/tpch/BEXHOMA_CHILD` (loaders read this file).
3. Multi-tenant handling: `schema` or `database` mode remaps BEXHOMA_CHILD and scales BEXHOMA_NUM_PODS per tenant; `container` mode logs but does not remap.
4. Determine `destination_raw`: `/data/tpch/SF<SF>[/<N>/<child>]` if STORE_RAW_DATA=1, else `/tmp/tpch/SF<SF>[/<N>/<child>]`. Exit early if folder exists and STORE_RAW_DATA_RECREATE=0.
5. If BEXHOMA_SYNCH_GENERATE=1: sync on `bexhoma-generator-podcount-<CONNECTION>-<EXPERIMENT>`.
6. Run `dbgen -s <SF>` (single pod) or `dbgen -s <SF> -S <child> -C <num_pods>` (multi-pod).
7. If TRANSFORM_RAW_DATA=1: strip trailing `|` from every `.tbl` file via `sed 's/.$//' -i`.
8. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

## Loader execution flow (common to all DBMS variants)
1. Read `BEXHOMA_CHILD` from `/tmp/tpch/BEXHOMA_CHILD`.
2. Determine `destination_raw` path (same logic as generator).
3. Multi-tenant handling (PostgreSQL loader only; mysql/mariadb/monetdb loaders do not have this).
4. If BEXHOMA_SYNCH_LOAD=1: sync on `bexhoma-loader-podcount-<CONNECTION>-<EXPERIMENT>`.
   PostgreSQL loader additionally syncs on `bexhoma-loader-podcount-<EXPERIMENT>` when BEXHOMA_TENANT_BY=container.
5. Loop over `.tbl` files; skip `nation` and `region` for pods > 1 in non-tenant mode.
6. If TPCH_TABLE is set: only load that table.
7. Execute DBMS-specific COPY/LOAD command per table; retry on known transient errors.
8. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

## Key design decisions
| Decision | Reason |
|---|---|
| Generator writes `/tmp/tpch/BEXHOMA_CHILD` | Loaders run in the same pod after the generator; this file is how the loader knows its partition index without querying Redis again |
| `nation` and `region` only loaded by pod 1 | These are reference tables (small, non-partitioned); loading them from multiple pods would cause duplicate key errors |
| `TRANSFORM_RAW_DATA` strips trailing `|` in generator | dbgen appends a trailing delimiter; stripping it at generation time avoids needing it in every loader variant |
| MySQL/MariaDB loaders override BEXHOMA_DATABASE with BEXHOMA_VOLUME | MySQL needs the database name from a separate Bexhoma volume variable that differs from the generic BEXHOMA_DATABASE |
| PostgreSQL loader has full multi-tenant support | TPC-H is used in schema/database isolation experiments; MySQL/MariaDB/MonetDB loaders do not have this |
| `loader-parallel.sh` in loader_mysql is inactive | It uses `mysqlsh util.import_table` which collects all partitions from all pods into one loader (pod 1 only); the active `loader.sh` uses `mysql LOAD DATA` per pod independently |

## Per-DBMS loader differences
| DBMS | Tool | Special handling |
|---|---|---|
| PostgreSQL | `psql \COPY` | Multi-tenancy; `PGOPTIONS --search_path` for schema isolation |
| MySQL | `mysql LOAD DATA LOCAL INFILE` | BEXHOMA_DATABASE=$BEXHOMA_VOLUME; per-table column mapping with NULLIF |
| MariaDB | `mysql LOAD DATA LOCAL INFILE` | BEXHOMA_DATABASE=$BEXHOMA_VOLUME; same column mapping |
| MonetDB | `mclient COPY N RECORDS INTO ... FROM STDIN` | Writes `.monetdb` credentials file; retries on worker thread errors |

## Style conventions
- **Dockerfiles**: `ENV KEY=value` form, grouped by concern with section headers.
- **Shell scripts**: Section banners use `#### Title ####`.
- **READMEs**: One entry per ENV, grouped by concern, one file per loader subfolder.
