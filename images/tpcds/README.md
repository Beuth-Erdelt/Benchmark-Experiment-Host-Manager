# TPC-DS images

Same two-phase pipeline as `images/tpch/`: a generator pod creates flat files on
disk, then one or more loader pods read those files and insert them into a target
DBMS. Key differences from TPC-H: larger schema (24 tables), `.dat` file format,
`dsdgen` binary, `customer.dat` requires ISO-8859-1 → UTF-8 conversion, and the
generator does not support multi-tenancy.

## Directory layout

```
images/tpcds/
├── generator/
│   ├── Dockerfile         — generator image
│   ├── generator.sh       — generates .dat files via dsdgen
│   ├── dsdgen             — pre-compiled TPC-DS generator binary (not in git)
│   ├── tpcds.idx          — dsdgen distribution index file
│   └── README.md          — environment variable reference + execution flow
├── loader_postgresql/
│   ├── Dockerfile         — PostgreSQL loader image
│   ├── loader.sh          — loads .dat via psql \COPY
│   └── README.md          — environment variable reference + execution flow
├── loader_mysql/
│   ├── Dockerfile         — MySQL loader image
│   ├── loader.sh          — loads .dat via mysql LOAD DATA LOCAL INFILE
│   └── README.md          — environment variable reference + execution flow
├── loader_mariadb/
│   ├── Dockerfile         — MariaDB loader image
│   ├── loader.sh          — loads .dat via mysql LOAD DATA LOCAL INFILE
│   └── README.md          — environment variable reference + execution flow
├── loader_monetdb/
│   ├── Dockerfile         — MonetDB loader image
│   ├── loader.sh          — loads .dat via mclient COPY FROM STDIN
│   └── README.md          — environment variable reference + execution flow
└── README.md              — this file
```

Environment variables for each image are documented in that image's own README.
This file covers the shared pipeline design and decisions that apply across all
of them.

No multi-tenant support exists anywhere in the TPC-DS generator or loaders
(unlike TPC-H, where the generator and the PostgreSQL loader both support it).

---

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

Same as `images/tpch/`: `ENV KEY=value`, grouped ENV with headers, one README per
subfolder, each including that image's own execution flow.
