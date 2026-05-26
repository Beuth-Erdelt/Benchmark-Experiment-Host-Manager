# TPC-H Experiments

This folder contains DDL scripts for loading and preparing the [TPC-H](https://www.tpc.org/tpch/) benchmark dataset across 20 database systems. Each subfolder corresponds to one DBMS and follows the same file naming convention.

## Benchmark Overview

TPC-H is a decision-support benchmark consisting of 8 tables and 22 analytical queries. The data generator (`dbgen`) produces pipe-delimited `.tbl` files. Supported scale factors are:

| Scale Factor | Approximate size |
|---|---|
| SF1 | 1 GB |
| SF10 | 10 GB |
| SF30 | 30 GB |
| SF100 | 100 GB |

Data files reside at `/data/tpch/<SF>/` (e.g. `/data/tpch/SF10/lineitem.tbl`).

### Table dependency order

```
region → nation → part      → partsupp ─┐
                → supplier  → partsupp  → orders → lineitem
                                        → customer
```

FK dependency order (referenced before dependent):
`region → nation → part / supplier → partsupp / customer → orders → lineitem`

---

## File Naming Convention

| File | Purpose |
|---|---|
| `initschema-tpch.sql` | Create the 8 TPC-H tables |
| `initschemadummy-tpch.sql` | Same but each table has a trailing `dummy CHAR(1)` column that absorbs the trailing `\|` delimiter dbgen appends to every row |
| `initschema-tpch-schema.sql` | Schema variant using the `{BEXHOMA_SCHEMA}` placeholder instead of a hard-coded schema name |
| `initconstraints-tpch.sql` | Add primary key and foreign key constraints |
| `initindexes-tpch.sql` | Create secondary indexes on FK columns |
| `initstatistics-tpch.sql` | Collect planner statistics; verify row counts |
| `initdata-tpch-SF1.sql` | Load data at scale factor 1 |
| `initdata-tpch-SF10.sql` | Load data at scale factor 10 |
| `initdata-tpch-SF30.sql` | Load data at scale factor 30 |
| `initdata-tpch-SF100.sql` | Load data at scale factor 100 |

Files whose names contain `filled` are generated variants with Bexhoma placeholders already substituted; they are not edited directly.

---

## Supported DBMS

| Folder | Schema / DB | Data load | Constraints | Notes |
|---|---|---|---|---|
| `PostgreSQL` | `public` or `{BEXHOMA_SCHEMA}` | `COPY … FROM … DELIMITER '\|' NULL ''` | PK + FK (combined ALTER TABLE) | `synchronous_commit` disabled during load; `-schema` variants available |
| `MySQL` | `tpch` | `LOAD DATA INFILE … FIELDS TERMINATED BY '\|'` | PK + FK (combined ALTER TABLE) | `SET GLOBAL local_infile = 1`; zero-date mode disabled |
| `MariaDB` | `tpch` | `LOAD DATA INFILE … FIELDS TERMINATED BY '\|'` | PK + FK (combined ALTER TABLE) | Same as MySQL |
| `MariaDBCS` | `tpch` | `cpimport` bulk loader | None (columnar engine) | `engine=columnstore` on every table |
| `Clickhouse` | `tpch` | `cat … \| clickhouse-client --format_csv_delimiter="\|"` | None | `ENGINE = MergeTree() ORDER BY …`; `Int32` / `Float64` types |
| `CockroachDB` | varies | `COPY` / `INSERT` | PK + FK | PostgreSQL-compatible SQL |
| `YugabyteDB` | varies | `COPY` | PK + FK | PostgreSQL-compatible SQL |
| `DB2` | varies | SQL | PK + FK | IBM DB2 dialect |
| `MonetDB` | varies | `COPY … INTO … FROM … USING DELIMITERS '\|'` | PK (FK optional) | `initschemadummy` variant used for loading |
| `CedarDB` | `public` | `COPY … FROM … DELIMITER '\|' NULL ''` | PK + FK | `initschemadummy` variant used for loading |
| `DatabaseService` | `public` | `COPY … FROM … DELIMITER '\|' NULL ''` | PK + FK | `initschemadummy` variant used for loading |
| `Exasol` | `public` | `IMPORT INTO … FROM LOCAL CSV FILE …` | PK (optimizer hint) + FK | PKs placed in `initindexes`; columnar zone maps replace secondary indexes |
| `Kinetica` | (default) | SQL `INSERT` | PK | `CREATE REPLICATED TABLE` for dimensions; `SHARD KEY` for fact tables; replicated-only variant available |
| `MemSQL` | `tpch` | `LOAD DATA INFILE … FIELDS TERMINATED BY '\|'` | PK (CLUSTERED COLUMNSTORE) | FK not supported; `ADD INDEX USING HASH` for lookups |
| `SingleStore` | `tpch` | `LOAD DATA INFILE … FIELDS TERMINATED BY '\|'` | PK | FK not supported; `ADD INDEX USING HASH` for lookups |
| `OracleDB` | `tpch` | `INSERT … SELECT * FROM ext_<table>` (external tables) | PK + FK + CHECK | Dual-table design: external tables for loading, internal tables for storage |
| `SAPHANA` | `TPCH` | `IMPORT FROM CSV FILE …` | PK (inline) | `CREATE COLUMN TABLE`; uppercase quoted identifiers; no secondary indexes |
| `SQLServer` | `dbo` | `BULK INSERT … WITH (FIRSTROW=1, FIELDTERMINATOR='\|', LASTROW=N, TABLOCK)` | PK (clustered, inline) | T-SQL; GO batch separators; `RECOVERY BULK_LOGGED` during load |
| `Citus` | `public` | `COPY public.<table> FROM … DELIMITER '\|' NULL ''` | PK + FK | Extends PostgreSQL; dimension tables as reference tables; `orders`/`lineitem` distributed; columnar variant available; `{shard_count}` template variant |
| `OmniSci` | (default) | `COPY <table> FROM … WITH (delimiter='\|', header='false', quoted='false')` | None | GPU-accelerated analytics; multiple schema variants (TEXT ENCODING DICT keys, BIGINT/DECIMAL, INTEGER/DOUBLE, 1/2/4/8 fixed shards) |

---

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
