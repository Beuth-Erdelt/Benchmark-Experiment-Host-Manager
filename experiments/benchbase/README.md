# Benchbase Experiments

This folder contains DDL scripts for use with the [Benchbase](https://github.com/cmu-db/benchbase) benchmarking framework. Benchbase is a Java-based tool that manages data generation, schema creation, data loading, and workload execution entirely; the SQL files here handle server configuration and post-load verification.

## Benchmark Overview

Benchbase supports multiple workloads. This folder is organised by workload and then by DBMS:

```
benchbase/
    tpcc/         TPC-C — transactional order-processing (9 tables)
    chbenchmark/  CH-benCHmark — OLAP queries over TPC-C data
    ycsb/         YCSB — key-value workload (usertable)
    twitter/      Twitter benchmark — social-network read/write workload
```

Each workload subfolder contains one subdirectory per supported DBMS.

---

## File Naming Convention

| File | Purpose |
|---|---|
| `initschema-benchbase.sql` | Server configuration (user accounts, engine settings) and/or `CREATE DATABASE`; schema creation is handled by Benchbase at runtime |
| `initschema-benchbase-schema.sql` | Named-schema variant using the `{BEXHOMA_SCHEMA}` placeholder (PostgreSQL TPC-C only) |
| `initschema-benchbase-postgresql.sql` | Full benchbase-generated PostgreSQL DDL with FK constraints; reference schema for the Citus variant (Citus TPC-C only) |
| `checkschema-benchbase.sql` | Post-load verification: `VACUUM ANALYZE` / `ANALYZE TABLE`, row counts, cluster topology, InnoDB configuration |
| `checkschema-benchbase-schema.sql` | Named-schema variant of the checkschema file (PostgreSQL TPC-C only) |

Files whose names contain `filled` are generated variants with Bexhoma placeholders already substituted; they are not edited directly.

---

## Supported DBMS by Workload

### TPC-C (`tpcc/`)

TPC-C simulates a wholesale supplier order-processing system with 9 tables (warehouse, district, customer, history, new_order, orders, order_line, item, stock). Benchbase creates all tables automatically; the SQL files configure the server and verify the result.

| Folder | Notes |
|---|---|
| `PostgreSQL` | `checkschema` runs `VACUUM ANALYZE`, reports pg_settings; `-schema` variant with `{BEXHOMA_SCHEMA}` |
| `MariaDB` | Server configuration placeholder; Benchbase creates tables |
| `MySQL` | User account setup, `local_infile`, zero-date mode, `CREATE DATABASE benchbase` |
| `CockroachDB` | `checkschema` reports range distribution and gossip node status |
| `TiDB` | Sets `max-replicas` via `SET CONFIG pd`; creates `benchbase` database |
| `YugabyteDB` | Full DDL with YugabyteDB HASH/ASC primary key syntax; FK constraints omitted; 300 s wait for tablet splitting |
| `Citus` | Full DDL with Citus shard distribution commands; FK constraints omitted; PostgreSQL reference DDL in separate file |

### chBenchmark (`chbenchmark/`)

CH-benCHmark runs analytical queries over TPC-C data, combining OLTP and OLAP in one schema. Benchbase creates the schema.

| Folder | Notes |
|---|---|
| `PostgreSQL` | `checkschema` reports table and index sizes |

### YCSB (`ycsb/`)

| Folder | Notes |
|---|---|
| `PostgreSQL` | `checkschema` reports table and index sizes |

### Twitter (`twitter/`)

| Folder | Notes |
|---|---|
| `PostgreSQL` | `checkschema` reports table and index sizes |

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
