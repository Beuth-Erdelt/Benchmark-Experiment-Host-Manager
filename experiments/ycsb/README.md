# YCSB Experiments

This folder contains DDL scripts for initialising the YCSB schema across 13 database systems. YCSB-JDBC (or the native YCSB driver) handles all data generation and loading; the SQL files here handle server configuration, schema creation, and post-load verification.

## Benchmark Overview

The [Yahoo Cloud Serving Benchmark (YCSB)](https://github.com/brianfrankcooper/YCSB) is a key-value workload benchmark that operates on a single table:

```sql
CREATE TABLE usertable (
    YCSB_KEY  VARCHAR(255)  PRIMARY KEY,
    FIELD0    TEXT,
    FIELD1    TEXT,
    ...
    FIELD9    TEXT
);
```

Six standard workloads (A–F) mix reads, updates, inserts, and scans at different ratios to model different application access patterns.

---

## File Naming Convention

| File | Purpose |
|---|---|
| `initschema-ycsb.sql` | Create `usertable`; configure distribution for distributed DBMSs |
| `checkschema-ycsb.sql` | Post-load verification: row count, tablet distribution, cluster status |
| `save-snapshot.sh` | Trigger a persistence snapshot (Dragonfly only) |

Files whose names contain `filled` are generated variants with Bexhoma placeholders already substituted; they are not edited directly.

---

## Supported DBMS

| Folder | Engine / DB | Distribution | Notes |
|---|---|---|---|
| `PostgreSQL` | `public` schema | Single node | Standard `COPY` for loading; `VACUUM ANALYZE` in checkschema |
| `CedarDB` | `public` schema | Single node | PostgreSQL-compatible; `CREATE TABLE … PRIMARY KEY` |
| `DatabaseService` | Managed PostgreSQL | Single node | `CREATE TABLE IF NOT EXISTS`; inline primary key |
| `MariaDB` | `ycsb` database | Single node | Backtick identifiers; InnoDB engine |
| `MySQL` | `ycsb` database | Single node | InnoDB; innodb buffer pool and redo log tuning |
| `MonetDB` | Default schema | Single node | SQL COPY for loading |
| `Kinetica` | Default schema | Single node | `DROP TABLE IF EXISTS` before create |
| `SingleStore` | `ycsb` database | Distributed | `CREATE ROWSTORE TABLE`; `USE ycsb` |
| `CockroachDB` | `public` schema | Distributed | `PRIMARY KEY USING HASH`; `CONFIGURE ZONE USING num_replicas` |
| `Citus` | `public` schema | Distributed | `create_distributed_table('usertable', 'ycsb_key')`; `{num_worker_shards}` placeholder |
| `TiDB` | MySQL-compatible | Distributed | `SET CONFIG pd max-replicas`; hash sharding for distribution |
| `YugabyteDB` | yugabyte database | Distributed | `ALTER DATABASE SET temp_file_limit=-1`; tablet distribution verified via `yb_table_properties` |
| `Dragonfly` | Key-value store | — | Redis-compatible; `save-snapshot.sh` triggers persistence; no SQL schema |

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
