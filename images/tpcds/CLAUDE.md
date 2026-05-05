# images/tpcds — development notes

## Overview
Same two-phase pipeline as images/tpch but for the TPC-DS benchmark. Key differences from TPC-H: larger schema (24 tables), `.dat` file format, `dsdgen` binary, `customer.dat` requires ISO-8859-1 → UTF-8 conversion, and the generator does not support multi-tenancy.

## Directory layout
```
images/tpcds/
├── generator/
│   ├── Dockerfile         — generator image
│   ├── generator.sh       — generates .dat files via dsdgen
│   ├── dsdgen             — pre-compiled TPC-DS generator binary (not in git)
│   ├── tpcds.idx          — dsdgen distribution index file
│   └── README.md
├── loader_postgresql/
│   ├── Dockerfile         — PostgreSQL loader image
│   ├── loader.sh          — loads .dat via psql \COPY
│   └── README.md
├── loader_mysql/
│   ├── Dockerfile         — MySQL loader image
│   ├── loader.sh          — loads .dat via mysql LOAD DATA LOCAL INFILE
│   └── README.md
├── loader_mariadb/
│   ├── Dockerfile         — MariaDB loader image
│   ├── loader.sh          — loads .dat via mysql LOAD DATA LOCAL INFILE
│   └── README.md
└── loader_monetdb/
    ├── Dockerfile         — MonetDB loader image
    ├── loader.sh          — loads .dat via mclient COPY FROM STDIN
    └── README.md
```

## Generator execution flow (`generator.sh`)
1. Pop child index from Redis queue `bexhoma-loading-<CONNECTION>-<EXPERIMENT>`.
2. Write child index to `/tmp/tpcds/BEXHOMA_CHILD` (loaders read this file).
3. If BEXHOMA_SYNCH_GENERATE=1: sync on `bexhoma-generator-podcount-<CONNECTION>-<EXPERIMENT>`.
4. Determine destination: `/data/tpcds/SF<SF>[/<N>/<child>]` or `/tmp/tpcds/SF<SF>[/<N>/<child>]`. Exit early if folder exists and STORE_RAW_DATA_RECREATE=0.
5. Run `dsdgen -dir <dst> -scale <SF>` (single pod) or `dsdgen -dir <dst> -scale <SF> -parallel <N> -child <i>` (multi-pod).
6. If TRANSFORM_RAW_DATA=1: convert `customer.dat` from ISO-8859-1 to UTF-8 via `iconv`, then strip trailing `|` from all `.dat` files via `sed 's/.$//' -i`.
7. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

No multi-tenant logic in the TPC-DS generator (unlike TPC-H generator).

## Loader execution flow (common)
1. Read `BEXHOMA_CHILD` from `/tmp/tpcds/BEXHOMA_CHILD`.
2. Determine `destination_raw` path.
3. If BEXHOMA_SYNCH_LOAD=1: sync on `bexhoma-loader-podcount-<CONNECTION>-<EXPERIMENT>`.
4. Loop over `.dat` files; strip pod suffix from filename to get table name in multi-pod mode.
5. If TPCDS_TABLE is set: only load that table.
6. Execute DBMS-specific command; retry on transient errors (MonetDB).
7. Emit timing.

No multi-tenant support in any TPC-DS loader.

## Key differences from images/tpch
| Aspect | TPC-H | TPC-DS |
|---|---|---|
| Generator binary | `dbgen` | `dsdgen` |
| Auxiliary file | `dists.dss` | `tpcds.idx` |
| Output format | `.tbl` files | `.dat` files |
| Customer charset | ASCII | ISO-8859-1 → UTF-8 via iconv |
| Nation/region dedup | Only pod 1 loads them | No equivalent; all tables loaded by each pod |
| Multi-tenant in generator | Yes (schema/database/container) | No |
| Multi-tenant in loaders | PostgreSQL only | None |
| MySQL/MariaDB DATABASE override | BEXHOMA_VOLUME (both) | MySQL: no override; MariaDB: BEXHOMA_VOLUME |
| Local data path | `/tmp/tpch/` | `/tmp/tpcds/` |

## Per-DBMS loader differences
| DBMS | Tool | Notes |
|---|---|---|
| PostgreSQL | `psql \COPY` | No multi-tenancy; no schema search_path; table name from filename `basename.dat` or `basename_<child>_<N>.dat` |
| MySQL | `mysql LOAD DATA LOCAL INFILE` | No BEXHOMA_VOLUME override; per-table column mapping with NULLIF |
| MariaDB | `mysql LOAD DATA LOCAL INFILE` | BEXHOMA_DATABASE=$BEXHOMA_VOLUME (same override as tpch); per-table NULLIF mappings |
| MonetDB | `mclient COPY N RECORDS INTO ... FROM STDIN` | Writes `.monetdb` credentials; retries on thread errors |

## Style conventions
Same as images/tpch: `ENV KEY=value`, grouped ENV with headers, one README per subfolder.
