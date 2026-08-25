# TPC-H images

Two-phase pipeline: a generator pod creates flat files on disk, then one or more
loader pods read those files and insert them into a target DBMS.

## Directory layout

```
images/tpch/
├── generator/
│   ├── Dockerfile         — generator image
│   ├── generator.sh       — generates .tbl files via dbgen
│   ├── dbgen              — pre-compiled TPC-H generator binary (not in git)
│   ├── dists.dss          — dbgen distribution file
│   └── README.md          — environment variable reference + execution flow
├── loader_postgresql/
│   ├── Dockerfile         — PostgreSQL loader image
│   ├── loader.sh          — loads .tbl via psql \COPY
│   └── README.md          — environment variable reference + execution flow
├── loader_mysql/
│   ├── Dockerfile         — MySQL loader image
│   ├── loader.sh          — loads .tbl via mysql LOAD DATA LOCAL INFILE
│   ├── loader-parallel.sh — alternative using mysqlsh util.import_table (inactive)
│   └── README.md          — environment variable reference + execution flow
├── loader_mariadb/
│   ├── Dockerfile         — MariaDB loader image
│   ├── loader.sh          — loads .tbl via mysql LOAD DATA LOCAL INFILE
│   └── README.md          — environment variable reference + execution flow
├── loader_monetdb/
│   ├── Dockerfile         — MonetDB loader image
│   ├── loader.sh          — loads .tbl via mclient COPY FROM STDIN
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
- **READMEs**: One entry per ENV, grouped by concern, one file per generator/loader
  subfolder, each including that image's own execution flow.
