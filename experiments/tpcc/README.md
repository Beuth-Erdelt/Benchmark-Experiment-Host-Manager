# TPC-C Experiments (HammerDB)

This folder contains DDL scripts for initialising the TPC-C schema across 6 database systems. HammerDB implements TPC-C as **TPROC-C** and drives all data generation and loading internally; the SQL files here handle only server configuration, schema creation, and post-load verification.

## Benchmark Overview

TPC-C is an OLTP benchmark that simulates a wholesale supplier order-processing system. It operates on 9 tables:

| Table | Role |
|---|---|
| `warehouse` | Top-level entity; root of FK hierarchy |
| `district` | 10 districts per warehouse |
| `customer` | 3 000 customers per district |
| `history` | Payment history records; no PK |
| `new_order` | Open orders awaiting delivery |
| `orders` | Completed order headers (`oorder` in some DBMS) |
| `order_line` | Line items; up to 15 per order |
| `item` | 100 000 product records; lookup table |
| `stock` | Inventory levels; one row per item per warehouse |

FK dependency order (referenced before dependent):
`warehouse → district / stock → customer → history / orders → new_order / order_line; item → stock`

---

## File Naming Convention

| File | Purpose |
|---|---|
| `initschema-tpcc.sql` | Create all 9 TPC-C tables with inline primary key and (where applicable) foreign key constraints |
| `checkschema-tpcc.sql` | Post-load verification: collect statistics and report table sizes (PostgreSQL, Citus only) |
| `initschema-tpcc-functions.sql` | PL/pgSQL stored procedures for the five TPROC-C transactions (Citus only) |
| `initschema-tpcc-tmp.sql` | pg_dump-derived DDL with Citus shard distribution commands (Citus only) |

Files whose names contain `filled` are generated variants with Bexhoma placeholders already substituted; they are not edited directly.

---

## Supported DBMS

| Folder | Schema / DB | Constraints | Notes |
|---|---|---|---|
| `PostgreSQL` | `public` | Inline PK; no FK | `checkschema-tpcc.sql` runs `VACUUM ANALYZE` and reports pg_settings |
| `MariaDB` | `tpcc` | Inline PK + FK | InnoDB; `IDENTIFIED WITH mysql_native_password BY 'root'` |
| `MySQL` | `tpcc` | Inline PK + FK | InnoDB; MEMORY engine for warehouse; zero-date mode |
| `CockroachDB` | `public` | `PRIMARY KEY USING HASH`; no FK | `ALTER TABLE … CONFIGURE ZONE USING num_replicas = {num_worker_replicas}` |
| `SingleStore` | `tpcc` | `KEY … USING CLUSTERED COLUMNSTORE`; no FK | `SHARD KEY`; `CREATE REFERENCE TABLE` for item |
| `Citus` | `public` | Named `CONSTRAINT … PRIMARY KEY`; no FK | Stored procedures; Citus shard distribution; pg_dump-derived DDL variant |

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
