---
title: 'Bexhoma: Cloud-native Benchmarking of DBMS at Kubernetes'
tags:
  - Python
  - DBMS
  - Kubernetes
  - Docker
  - Cloud-native
  - Microservices
authors:
  - name: Patrick K. Erdelt
    orcid: 0000-0002-3359-2386
    corresponding: true
    affiliation: 1
affiliations:
 - name: Berliner Hochschule für Technik (BHT)
   index: 1
date: 05 November 2022
bibliography: paper.bib

---

# Summary

Bexhoma (Benchmark Experiment Host Manager) is a Python tool that helps with managing benchmark experiments of Database Management Systems (DBMS) in a Kubernetes-based High-Performance-Computing (HPC) cluster environment. It enables users to configure hardware / software setups for easily repeating tests over varying configurations.

It serves as the orchestrator [@10.1007/978-3-030-94437-7_6] for distributed parallel benchmarking experiments in a Kubernetes Cloud. This has been tested at Amazon Web Services, Google Cloud, Microsoft Azure, IBM Cloud, Oracle Cloud, and at Minikube installations, running with Clickhouse, Exasol, Citus Data (Hyperscale), IBM DB2, MariaDB, MariaDB Columnstore, MemSQL (SingleStore), MonetDB, MySQL, OmniSci (HEAVY.AI), Oracle DB, PostgreSQL, SQL Server, SAP HANA, TimescaleDB, and Vertica.

The basic workflow is [@10.1007/978-3-030-94437-7_6; @10.1007/978-3-030-84924-5_6]: start a containerized version of the DBMS, install monitoring software, import data, run benchmarks and shut down everything with a single command. A more advanced workflow is: Plan a sequence of such experiments, run plan as a batch and join results for comparison.

It is also possible to scale-out drivers for generating and loading data and for benchmarking to simulate cloud-native environments as in [@10.1007/978-3-031-68031-1_9]. Benchmarks included are YCSB, TPC-H and TPC-C (HammerDB and Benchbase version).


Used by [@Erdelt2022DBMSBenchmarker; @10.1007/978-3-030-84924-5_6; @10.1007/978-3-031-68031-1_9]
See the [homepage](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager) and the [documentation](https://bexhoma.readthedocs.io/en/latest/) for more details.

# Statement of Need

## Summary of Solution

# A Basic Example

# Acknowledgements


# References
