# TPC-DS Experiments

This folder contains DDL scripts for loading and preparing the [TPC-DS](https://www.tpc.org/tpcds/) benchmark dataset across 14 database systems. Each subfolder corresponds to one DBMS and follows the same file naming convention.

## Benchmark Overview

TPC-DS is a decision-support benchmark consisting of 25 tables and 99 analytical queries modelling a retail catalogue and web channel business. The data generator (`dsdgen`) produces pipe-delimited `.dat` files. Supported scale factors are:

| Scale Factor | Approximate size |
|---|---|
| SF1 | 1 GB |
| SF10 | 10 GB |
| SF30 | 30 GB |
| SF100 | 100 GB |

Data files reside at `/data/tpcds/<SF>/` (e.g. `/data/tpcds/SF10/store_sales.dat`).

---

## File Naming Convention

| File | Purpose |
|---|---|
| `initschema-tpcds.sql` | Create the 25 TPC-DS tables |
| `initconstraints-tpcds.sql` | Add primary key and foreign key constraints |
| `initindexes-tpcds.sql` | Create secondary indexes on FK columns |
| `initstatistics-tpcds.sql` | Collect planner statistics; verify row counts (selected DBMS only) |
| `initdata-tpcds-SF1.sql` | Load data at scale factor 1 |
| `initdata-tpcds-SF10.sql` | Load data at scale factor 10 |
| `initdata-tpcds-SF30.sql` | Load data at scale factor 30 |
| `initdata-tpcds-SF100.sql` | Load data at scale factor 100 |

Files whose names contain `filled` are generated variants with Bexhoma placeholders already substituted; they are not edited directly.

---

## Supported DBMS

| Folder | Schema / DB | Data load | Constraints | Notes |
|---|---|---|---|---|
| `PostgreSQL` | `public` | `COPY … FROM … DELIMITER '\|' NULL ''` | PK + FK + indexes | `initstatistics-tpcds.sql` runs `ANALYZE` |
| `MariaDB` | `tpcds` | `LOAD DATA INFILE … FIELDS TERMINATED BY '\|'` | PK + FK + indexes | InnoDB |
| `MySQL` | `tpcds` | `LOAD DATA INFILE … FIELDS TERMINATED BY '\|'` | PK + FK + indexes | InnoDB; `SET GLOBAL local_infile = 1` |
| `Clickhouse` | `tpcds` | `cat … \| clickhouse-client --format_csv_delimiter="\|"` | None | `ENGINE = MergeTree() ORDER BY …`; `Int32` / `Float64` types |
| `DB2` | varies | `LOAD FROM … OF DEL` | PK + FK | IBM DB2 dialect |
| `Exasol` | `public` | `IMPORT INTO … FROM LOCAL CSV FILE …` | PK (optimizer hint) + FK | Columnar zone maps replace secondary indexes |
| `MariaDBCS` | `tpcds` | `cpimport` bulk loader | None (columnar engine) | `engine=columnstore` on every table |
| `MemSQL` | `tpcds` | `LOAD DATA INFILE … FIELDS TERMINATED BY '\|'` | PK | FK not supported; columnstore tables |
| `MonetDB` | varies | `COPY … INTO … FROM … USING DELIMITERS '\|'` | PK; FK optional | |
| `OmniSci` | `tpcds` | `COPY … FROM … WITH (delimiter='\|')` | None | GPU-accelerated analytics; multiple schema variants |
| `OmniSciCPU` | `tpcds` | `COPY … FROM … WITH (delimiter='\|')` | None | CPU-only variant of OmniSci |
| `SAPHANA` | `TPCDS` | `IMPORT FROM CSV FILE …` | PK (inline) | `CREATE COLUMN TABLE`; uppercase quoted identifiers |
| `SQLServer` | `dbo` | `BULK INSERT … WITH (FIELDTERMINATOR='\|', TABLOCK)` | PK (clustered, inline) | T-SQL; GO batch separators |
| `Citus` | `public` | `COPY public.<table> FROM … DELIMITER '\|' NULL ''` | PK + FK + indexes | Extends PostgreSQL; fact tables distributed; dimensions as reference tables |

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
