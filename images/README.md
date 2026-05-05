# Benchmark Experiment Host Manager — Docker Images

This folder contains Docker images for all components of the Bexhoma benchmarking
experiments: data generators, workload drivers, loaders, evaluators, and monitoring.

## Orchestration of Benchmarking Experiments

<p align="center">
    <img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/v0.5.6/docs/experiment-with-orchestrator.png" width="800">
</p>

For full power, use this tool as an orchestrator as in [2]. It also starts a monitoring
container using [Prometheus](https://prometheus.io/) and a metrics collector container
using [cAdvisor](https://github.com/google/cadvisor). For analytical use cases, the
Python package [dbmsbenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker), [3],
is used as query executor and evaluator as in [1,2]. For transactional use cases,
HammerDB's TPC-C, Benchbase's TPC-C and YCSB are used as drivers for generating and
loading data and for running the workload as in [4].

---

## Subfolders

### Analytical query workloads

| Folder | Role | Description |
|---|---|---|
| [`benchmarker_dbmsbenchmarker/`](benchmarker_dbmsbenchmarker/) | Benchmarker | Runs [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) query workloads against a target DBMS over JDBC. Supports parallel streams, multi-tenant modes (schema / database / container), and synchronized start across pods. |
| [`evaluator_dbmsbenchmarker/`](evaluator_dbmsbenchmarker/) | Evaluator | Serves the DBMSBenchmarker results dashboard (port 8050) and a Jupyter Notebook server (port 8888) for post-experiment analysis. |

Both images are built from a `Dockerfile_template`; the `{version}` placeholder is
replaced by `create_Dockerfiles.py` with the target DBMSBenchmarker Git tag.

**Supported DBMS (JDBC drivers bundled):** PostgreSQL, MySQL, MariaDB, MonetDB,
SingleStore, YugabyteDB.

---

### TPC-C / YCSB transactional workloads

| Folder | Role | Description |
|---|---|---|
| [`benchbase/`](benchbase/) | Generator + Benchmarker | Runs [Benchbase](https://github.com/cmu-db/benchbase) TPC-C or YCSB workloads. Two separate Dockerfiles: `Dockerfile_generator` (schema creation and data loading) and `Dockerfile_benchmarker` (timed workload execution). |
| [`hammerdb/benchmarker/`](hammerdb/benchmarker/) | Benchmarker | Runs [HammerDB](https://www.hammerdb.com/) TPC-C timed driver. Generates a `benchmark.tcl` script at runtime based on `HAMMERDB_TYPE` and runs it via `hammerdbcli`. |
| [`hammerdb/generator/`](hammerdb/generator/) | Generator | Runs HammerDB `buildschema` to create and populate the TPC-C schema. |
| [`ycsb/benchmarker/`](ycsb/benchmarker/) | Benchmarker | Runs [YCSB](https://github.com/brianfrankcooper/YCSB) workloads (a–f) against an already-loaded dataset. |
| [`ycsb/generator/`](ycsb/generator/) | Generator | Runs `ycsb load` to populate the target DBMS with a YCSB dataset. Each pod loads a distinct key-range partition. |

**HammerDB supported backends:** PostgreSQL, MySQL, MariaDB, Citus.

**YCSB supported backends:** JDBC (PostgreSQL, MySQL, MariaDB, MonetDB, SingleStore,
YugabyteDB), Redis, Redis Cluster.

---

### TPC-DS / TPC-H data generation and loading

Both benchmarks follow a two-phase approach: a generator pod writes flat files to a
shared persistent volume, then one or more loader pods import those files into the DBMS.

#### TPC-DS

| Folder | Role | Description |
|---|---|---|
| [`tpcds/generator/`](tpcds/generator/) | Generator | Runs the TPC-DS `dsdgen` tool to produce flat files. Supports parallel generation across pods and optional persistent storage. |
| [`tpcds/loader_postgresql/`](tpcds/loader_postgresql/) | Loader | Loads TPC-DS flat files into PostgreSQL via `psql \COPY`. |
| [`tpcds/loader_mysql/`](tpcds/loader_mysql/) | Loader | Loads TPC-DS flat files into MySQL. |
| [`tpcds/loader_mariadb/`](tpcds/loader_mariadb/) | Loader | Loads TPC-DS flat files into MariaDB. |
| [`tpcds/loader_monetdb/`](tpcds/loader_monetdb/) | Loader | Loads TPC-DS flat files into MonetDB. |

The `dsdgen` binary and `tpcds.idx` index file must be present in
`tpcds/generator/` before building the image (not included due to TPC licensing).

#### TPC-H

| Folder | Role | Description |
|---|---|---|
| [`tpch/generator/`](tpch/generator/) | Generator | Runs the TPC-H `dbgen` tool to produce flat files. Supports parallel generation across pods and optional persistent storage. |
| [`tpch/loader_postgresql/`](tpch/loader_postgresql/) | Loader | Loads TPC-H flat files into PostgreSQL via `psql \COPY`. |
| [`tpch/loader_mysql/`](tpch/loader_mysql/) | Loader | Loads TPC-H flat files into MySQL. |
| [`tpch/loader_mariadb/`](tpch/loader_mariadb/) | Loader | Loads TPC-H flat files into MariaDB. |
| [`tpch/loader_monetdb/`](tpch/loader_monetdb/) | Loader | Loads TPC-H flat files into MonetDB. |

The `dbgen` binary and `dists.dss` file must be present in `tpch/generator/`
before building the image (not included due to TPC licensing).

---

### Infrastructure

| Folder | Role | Description |
|---|---|---|
| [`monitoring/`](monitoring/) | Monitoring | Runs a [Prometheus](https://prometheus.io/) instance. The scrape configuration is supplied at runtime via the `BEXHOMA_WORKERS` environment variable. |

---

## References

If you use Bexhoma in work contributing to a scientific publication, we kindly ask that
you cite our application note [2] or [1]:

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

[4] [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
> Erdelt, P.K. (2024).
> A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools.
> In: Nambiar, R., Poess, M. (eds) Performance Evaluation and Benchmarking. TPCTC 2023.
> Lecture Notes in Computer Science, vol 14247. Springer, Cham.
> https://doi.org/10.1007/978-3-031-68031-1_9
