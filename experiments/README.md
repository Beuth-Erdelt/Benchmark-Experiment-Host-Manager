# Benchmark Experiment Host Manager — Schema and Query Files

This directory contains workload and schema files for benchmarking experiments. Each subfolder corresponds to one benchmark and holds per-DBMS DDL scripts, data-loading scripts, and query configuration files.

## Directory Overview

| Folder | Benchmark | Type | Workload driver |
|---|---|---|---|
| [`tpch/`](tpch/) | [TPC-H](https://www.tpc.org/tpch/) | Analytical — 8 tables, 22 queries | dbmsbenchmarker |
| [`tpcds/`](tpcds/) | [TPC-DS](https://www.tpc.org/tpcds/) | Analytical — 25 tables, 99 queries | dbmsbenchmarker |
| [`tpcc/`](tpcc/) | TPC-C (HammerDB TPROC-C) | Transactional — 9 tables | HammerDB |
| [`ycsb/`](ycsb/) | [YCSB](https://github.com/brianfrankcooper/YCSB) | Key-value — 1 table | YCSB-JDBC |
| [`benchbase/`](benchbase/) | [Benchbase](https://github.com/cmu-db/benchbase) — TPC-C, chBenchmark, YCSB, Twitter | Mixed | Benchbase |
| [`example/`](example/) | Custom SQL workload template | — | dbmsbenchmarker |

## Orchestration of Benchmarking Experiments

<p align="center">
    <img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/v0.5.6/docs/experiment-with-orchestrator.png" width="800">
</p>

For full power, use this tool as an orchestrator as in [2]. It also starts a monitoring container using [Prometheus](https://prometheus.io/) and a metrics collector container using [cAdvisor](https://github.com/google/cadvisor). For analytical use cases, the Python package [dbmsbenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker), [3], is used as query executor and evaluator as in [1,2].
For transactional use cases, HammerDB's TPC-C, Benchbase's TPC-C and YCSB are used as drivers for generating and loading data and for running the workload as in [4].

---

## References

If you use Bexhoma in work contributing to a scientific publication, we kindly ask that you cite our application note [2] or [1]:

[1] [A Framework for Supporting Repetition and Evaluation in the Process of Cloud-Based DBMS Performance Benchmarking](https://doi.org/10.1007/978-3-030-84924-5_6)
> Erdelt P.K. (2021)
> A Framework for Supporting Repetition and Evaluation in the Process of Cloud-Based DBMS Performance Benchmarking.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2020.
> Lecture Notes in Computer Science, vol 12752. Springer, Cham.
> https://doi.org/10.1007/978-3-030-84924-5_6

[2] [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
> Erdelt P.K. (2022)
> Orchestrating DBMS Benchmarking in the Cloud with Kubernetes.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2021.
> Lecture Notes in Computer Science, vol 13169. Springer, Cham.
> https://doi.org/10.1007/978-3-030-94437-7_6

[3] [DBMS-Benchmarker: Benchmark and Evaluate DBMS in Python](https://doi.org/10.21105/joss.04628)
> Erdelt P.K., Jestel J. (2022).
> DBMS-Benchmarker: Benchmark and Evaluate DBMS in Python.
> Journal of Open Source Software, 7(79), 4628
> https://doi.org/10.21105/joss.04628

[4] [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](http://dx.doi.org/10.13140/RG.2.2.29866.18880)
> Erdelt P.K. (2023)
> http://dx.doi.org/10.13140/RG.2.2.29866.18880

---

## SQL and shell file conventions

These rules apply to all SQL (`.sql`) and shell (`.sh`) files under
`experiments/`. They extend and specialise the root-level conventions in
`docs/CONTRIBUTING.md`.
**Do not change the logic or execution result of any file.**

### File scope

- **Ignore** every file whose name contains `filled` (e.g. `filled_initschema-tpch.sql`).
- **Ignore** `connections.config` and every `queries*.config` file.
- Process all other `.sql` and `.sh` files.

### Directory layout

```
experiments/<benchmark>/          e.g. tpch/, tpcds/
    <DBMS>/                       e.g. PostgreSQL/, MySQL/, Clickhouse/
        initschema-tpch.sql       create tables (public / default schema)
        initschema-tpch-schema.sql  create tables in a named schema
        initschemadummy-tpch.sql  create tables with trailing dummy column
        initconstraints-tpch.sql  add primary and foreign key constraints
        initindexes-tpch.sql      create indexes on FK columns
        initdata-tpch-SF1.sql     load data at scale factor 1
        initdata-tpch-SF10.sql    load data at scale factor 10
        initdata-tpch-SF30.sql    load data at scale factor 30
        initdata-tpch-SF100.sql   load data at scale factor 100
        initstatistics-tpch.sql   collect statistics, verify counts
```

`-schema` variants use the `{BEXHOMA_SCHEMA}` placeholder instead of a
hard-coded schema name; it is substituted at runtime by the Bexhoma framework.

### Required file header (all .sql and .sh files)

Every file must start with this exact block, adapted to its path and purpose:

```sql
-- Benchmark-Experiment-Host-Manager | experiments/<benchmark>/<DBMS>
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: <one or two sentences describing what this file does and when
--           it is executed relative to the other init files>
```

For shell scripts use `#` instead of `--`.

### SQL formatting

**Keywords**
- Uppercase all SQL reserved words: `CREATE`, `TABLE`, `ALTER`, `ADD`,
  `PRIMARY KEY`, `FOREIGN KEY`, `REFERENCES`, `NOT NULL`, `INTEGER`,
  `DECIMAL`, `CHAR`, `VARCHAR`, `DATE`, `COPY`, `ANALYZE`, `SELECT`,
  `COUNT`, `FROM`, `INDEX`, `ON`, `NULL`, `AS`, etc.
- Keep identifier names exactly as they are (lowercase with underscores).

**CREATE TABLE**
- One column per line, 4-space indent.
- Align column names to the width of the longest name in the table + 2 spaces.
- Align type declarations to a fixed width after the name column.
- Closing `)` on its own line followed by `;`.

```sql
CREATE TABLE public.orders (
    o_orderkey      INTEGER       NOT NULL,
    o_custkey       INTEGER       NOT NULL,
    o_orderstatus   CHAR(1)       NOT NULL,
    o_totalprice    DECIMAL(15,2) NOT NULL,
    o_orderdate     DATE          NOT NULL,
    o_orderpriority CHAR(15)      NOT NULL,
    o_clerk         CHAR(15)      NOT NULL,
    o_shippriority  INTEGER       NOT NULL,
    o_comment       VARCHAR(79)   NOT NULL
);
```

**ALTER TABLE — constraints** (PostgreSQL, CockroachDB, YugabyteDB, DB2, MySQL/MariaDB)
- Combine all actions for a table into **one** `ALTER TABLE` statement so the
  table is locked only once.
- Order statements by FK dependency: referenced tables first, dependent tables last.
- Indent each action by 4 spaces.

```sql
ALTER TABLE public.lineitem
    ADD PRIMARY KEY (l_orderkey, l_linenumber),
    ADD FOREIGN KEY (l_orderkey)           REFERENCES public.orders(o_orderkey),
    ADD FOREIGN KEY (l_partkey)            REFERENCES public.part(p_partkey),
    ADD FOREIGN KEY (l_suppkey)            REFERENCES public.supplier(s_suppkey),
    ADD FOREIGN KEY (l_partkey, l_suppkey) REFERENCES public.partsupp(ps_partkey, ps_suppkey);
```

**CREATE INDEX**
- Cannot be combined; one statement per index — this is a SQL language limit.
- Align table names across the index group for scannability.

### Cleaning rules (apply to every file)

| Remove | Reason |
|---|---|
| `-- sccsid: @(#)dss.ddl …` lines | Old SCCS source-control artefact |
| `-- tpcd benchmark version 8.0` | Outdated reference, no documentation value |
| Commented-out SQL code blocks | Dead code; see `docs/CONTRIBUTING.md`'s code-style rules |
| Trailing whitespace on any line | Cosmetic |
| Blank lines beyond one consecutive blank line | Cosmetic |

When removing a commented-out block that was an intentional exclusion
(e.g. a FK that is deliberately not applied), replace it with a single
`-- <table>-><table> FK not applied: <reason>` comment.

### Benchmark-specific findings

#### TPC-H (`experiments/tpch/`)

**TPC-H table set** (8 tables, in FK dependency order):
`region -> nation -> part / supplier -> partsupp / customer -> orders -> lineitem`

**supplier -> nation FK**: part of the TPC-H DDL standard but not required
by any query in the TPC-H workload; intentionally not applied in all DBMS
variants. Document with: `-- supplier->nation FK not applied: not required by the TPC-H query workload`

**dummy column** (`initschemadummy-*`): each table gets a trailing `dummy CHAR(1)`
column that absorbs the trailing `|` delimiter dbgen appends to every row in
`.tbl` files. Always explain this in the file header.

**Omitted lineitem indexes**: individual indexes on `lineitem(l_partkey)` and
`lineitem(l_suppkey)` are intentionally skipped.
- `l_partkey` is redundant — it is the leading column of the compound index
  `(l_partkey, l_suppkey)` which already covers prefix lookups.
- `l_suppkey` alone is not selective enough to benefit the TPC-H query workload.
Document with a comment at the top of every `initindexes` file.

**synchronous_commit pattern (PostgreSQL only)**:
- `initschema-tpch.sql` disables synchronous commit at the end (`ALTER SYSTEM SET synchronous_commit = off; SELECT pg_reload_conf();`) to accelerate bulk loading.
- `initstatistics-tpch.sql` re-enables it at the end after `ANALYZE`.
- The commented-out `fsync = off` alternative has been removed (dead code).

**Scale factor data path**: `/data/tpch/<SF>/` where `<SF>` is `SF1`, `SF10`,
`SF30`, or `SF100`. All `.tbl` files are pipe-delimited with a trailing `|`.

**{BEXHOMA_SCHEMA} variants**: `-schema` files create a named schema
(`CREATE SCHEMA {BEXHOMA_SCHEMA}`) and qualify every table reference with it.
They do **not** include the `ALTER SYSTEM synchronous_commit` lines.

### DBMS dialect notes (to be extended as each folder is cleaned)

| DBMS | Schema/DB | Data load method | Constraint support | Notes |
|---|---|---|---|---|
| PostgreSQL | `public` (default) or `{BEXHOMA_SCHEMA}` | `COPY … FROM … DELIMITER '|' NULL ''` | Full PK + FK; combined `ALTER TABLE` | synchronous_commit pattern; -schema variants |
| MySQL / MariaDB | `tpch` database | `LOAD DATA INFILE … FIELDS TERMINATED BY '|'` | Full PK + FK; combined `ALTER TABLE` | `SET GLOBAL local_infile = 1`; zero-date mode |
| MariaDBCS | `tpch` database | `cpimport` bulk loader | None (columnar engine) | `engine=columnstore` on every table |
| Clickhouse | `tpch` database | `cat … \| clickhouse-client --format_csv_delimiter="\|"` | None | `ENGINE = MergeTree() ORDER BY …`; uses `Int32` not `INTEGER` |
| CockroachDB | varies | SQL `INSERT` / COPY | PK + FK | Similar to PostgreSQL syntax |
| YugabyteDB | varies | SQL | PK + FK | PostgreSQL-compatible |
| DB2 | varies | SQL | PK + FK | Keyword `NOT NULL` same; type names may differ |
| MonetDB | varies | SQL COPY | PK; FK optional | `initschemadummy` needed |
| CedarDB | varies | SQL | PK + FK | `initschemadummy` needed |
| DatabaseService | varies | SQL | PK + FK | `initschemadummy` needed |
| OmniSci / HeavyAI | `tpch` | SQL | None (analytical) | Multiple shard variants |
| Exasol | varies | SQL | PK + FK | |
| Kinetica | varies | SQL | PK; replicated variant | |
| MemSQL / SingleStore | varies | SQL | PK + FK | |
| OracleDB | varies | SQL | PK + FK | |
| SAPHANA | varies | SQL | PK only | No `initindexes` file |
| SQLServer | varies | SQL | PK + FK | T-SQL dialect |
| Citus | `public` | SQL | PK + FK; columnar variant | Extends PostgreSQL |

### Progress tracker

| Folder | Status |
|---|---|
| `tpch/PostgreSQL` | Done |
| `tpch/MySQL` | Done |
| `tpch/MariaDB` | Done |
| `tpch/MariaDBCS` | Done |
| `tpch/Clickhouse` | Done |
| `tpch/CockroachDB` | Done |
| `tpch/YugabyteDB` | Done |
| `tpch/DB2` | Done |
| `tpch/MonetDB` | Done |
| `tpch/CedarDB` | Done |
| `tpch/DatabaseService` | Done |
| `tpch/OmniSci` | Done |
| `tpch/Exasol` | Done |
| `tpch/Kinetica` | Done |
| `tpch/MemSQL` | Done |
| `tpch/SingleStore` | Done |
| `tpch/OracleDB` | Done |
| `tpch/SAPHANA` | Done |
| `tpch/SQLServer` | Done |
| `tpch/Citus` | Done |
| `tpcds/MariaDB` | Done |
| `tpcds/MySQL` | Done |
| `tpcds/Clickhouse` | Done |
| `tpcds/DB2` | Done |
| `tpcds/Exasol` | Done |
| `tpcds/MariaDBCS` | Done |
| `tpcds/MemSQL` | Done |
| `tpcds/MonetDB` | Done |
| `tpcds/OmniSci` | Done |
| `tpcds/OmniSciCPU` | Done |
| `tpcds/SAPHANA` | Done |
| `tpcds/SQLServer` | Done |
| `tpcds/Citus` | Done |
| `tpcc/MariaDB` | Done |
| `tpcc/PostgreSQL` | Done |
| `tpcc/CockroachDB` | Done |
| `tpcc/MySQL` | Done |
| `tpcc/SingleStore` | Done |
| `tpcc/Citus` | Done |
| `ycsb/CedarDB` | Done |
| `ycsb/Citus` | Done |
| `ycsb/CockroachDB` | Done |
| `ycsb/DatabaseService` | Done |
| `ycsb/Dragonfly` | Done |
| `ycsb/Kinetica` | Done |
| `ycsb/MariaDB` | Done |
| `ycsb/MonetDB` | Done |
| `ycsb/MySQL` | Done |
| `ycsb/PostgreSQL` | Done |
| `ycsb/SingleStore` | Done |
| `ycsb/TiDB` | Done |
| `ycsb/YugabyteDB` | Done |
| `benchbase/chbenchmark/PostgreSQL` | Done |
| `benchbase/tpcc/Citus` | Done |
| `benchbase/tpcc/CockroachDB` | Done |
| `benchbase/tpcc/MariaDB` | Done |
| `benchbase/tpcc/MySQL` | Done |
| `benchbase/tpcc/PostgreSQL` | Done |
| `benchbase/tpcc/TiDB` | Done |
| `benchbase/tpcc/YugabyteDB` | Done |
| `benchbase/twitter/PostgreSQL` | Done |
| `benchbase/ycsb/PostgreSQL` | Done |
