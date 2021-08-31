# Benchmark Experiment Host Manager
This Python tools helps **managing benchmark experiments of Database Management Systems (DBMS) in a Kubernetes-based High-Performance-Computing (HPC) cluster environment**.
It enables users to configure hardware / software setups for easily repeating tests over varying configurations.

It serves as the **orchestrator** [2] for distributed parallel benchmarking experiments in a Kubernetes Cloud.
This has been tested at Amazon Web Services, Google Cloud, Microsoft Azure, IBM Cloud und Oracle Cloud.

<p align="center">
    <img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/v0.5.6/docs/experiment-with-orchestrator.png" width="800">
</p>

The basic workflow is [1,2]: start a virtual machine, install monitoring software and a database management system, import data, run benchmarks (external tool) and shut down everything with a single command.
A more advanced workflow is: Plan a sequence of such experiments, run plan as a batch and join results for comparison.

## Installation

1. Download the repository: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager
1. Install the package `pip install bexhoma`
1. Make sure you have a working `kubectl` installed  
  (Also make sure to have access to a running Kubernetes cluster - for example [Minikube](https://minikube.sigs.k8s.io/docs/start/))
1. Adjust configuration [tbd in detail]
    1. Rename `k8s-cluster.config` to `cluster.config`
    1. Set name of context, namespace and name of cluster in that file
1. Install data [tbd in detail]  
  Example for TPC-H SF=1:  
    * Run `kubectl create -f k8s/job-data-tpch-1.yml`  
    * When job is done, clean up with  
    `kubectl delete job -l app=bexhoma -l component=data-source` and  
    `kubectl delete deployment -l app=bexhoma -l component=data-source`.
1. Install result folder  
  Run `kubectl create -f k8s/pvc-bexhoma-results.yml`


## Quickstart

The repository contains a [tool](experiments/tpch/) for running TPC-H (reading) queries at MonetDB and PostgreSQL.

1. Run `tpch run -sf 1 -t 30`.
1. You can watch status using `bexperiments status` while running.  
  This is equivalent to `python cluster.py status`.
1. After benchmarking has finished, run `bexperiments dashboard` to connect to a dashboard. You can open dashboard in browser at `http://localhost:8050`.  
  This is equivalent to `python cluster.py dashboard`  
  Alternatively you can open a Jupyter notebook at `http://localhost:8888`.

## More Informations

For full power, use this tool as an orchestrator as in [2]. It also starts a monitoring container using [Prometheus](https://prometheus.io/) and a metrics collector container using [cAdvisor](https://github.com/google/cadvisor). It also uses the Python package [dbmsbenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) as query executor [2] and evaluator [1].
See the [images](images/) folder for more details.

This module has been tested with Brytlyt, Citus, Clickhouse, DB2, Exasol, Kinetica, MariaDB, MariaDB Columnstore, MemSQL, Mariadb, MonetDB, MySQL, OmniSci, Oracle DB, PostgreSQL, SingleStore, SQL Server and SAP HANA.

## References

[1] [A Framework for Supporting Repetition and Evaluation in the Process of Cloud-Based DBMS Performance Benchmarking](https://doi.org/10.1007/978-3-030-84924-5_6)

> Erdelt P.K. (2021)
> A Framework for Supporting Repetition and Evaluation in the Process of Cloud-Based DBMS Performance Benchmarking.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2020.
> Lecture Notes in Computer Science, vol 12752. Springer, Cham.
> https://doi.org/10.1007/978-3-030-84924-5_6


[2] [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://www.researchgate.net/publication/353236865_Orchestrating_DBMS_Benchmarking_in_the_Cloud_with_Kubernetes)

(old, slightly outdated [docs](docs/Docs_old.md))