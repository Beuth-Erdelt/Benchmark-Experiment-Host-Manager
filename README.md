[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/graphs/commit-activity)
[![GitHub release](https://img.shields.io/github/release/Beuth-Erdelt/Benchmark-Experiment-Host-Manager.svg)](https://GitHub.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/releases/)
[![PyPI version](https://badge.fury.io/py/bexhoma.svg)](https://badge.fury.io/py/bexhoma)
[![.github/workflows/draft-pdf.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/actions/workflows/draft-pdf.yml/badge.svg)](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/actions/workflows/draft-pdf.yml)

# Benchmark Experiment Host Manager (Bexhoma)
This Python tools helps **managing benchmark experiments of Database Management Systems (DBMS) in a Kubernetes-based High-Performance-Computing (HPC) cluster environment**.
It enables users to configure hardware / software setups for easily repeating tests over varying configurations.

It serves as the **orchestrator** [2] for distributed parallel benchmarking experiments in a Kubernetes Cloud.
This has been tested at Amazon Web Services, Google Cloud, Microsoft Azure, IBM Cloud, Oracle Cloud, and at Minikube installations,
running with Citus Data (Hyperscale), Clickhouse, CockroachDB, Exasol, IBM DB2, MariaDB, MariaDB Columnstore, MemSQL (SingleStore), MonetDB, MySQL, OmniSci (HEAVY.AI), Oracle DB, PostgreSQL, SQL Server, SAP HANA, TimescaleDB, and Vertica.
.

<p align="center">
    <img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/experiment-with-orchestrator.png" width="800">
</p>

The basic workflow is [1,2]: start a virtual machine, install monitoring software and a database management system, import data, run benchmarks (external tool) and shut down everything with a single command.
A more advanced workflow is: Plan a sequence of such experiments, run plan as a batch and join results for comparison.

See the [homepage](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager) and the [documentation](https://bexhoma.readthedocs.io/en/latest/).

If you encounter any issues, please report them to our [Github issue tracker](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues).

## Installation

1. Download the repository: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager
1. Install the package `pip install bexhoma`
1. Make sure you have a working `kubectl` installed  
  (Also make sure to have access to a running Kubernetes cluster - for example [Minikube](https://minikube.sigs.k8s.io/docs/start/))
1. Adjust [configuration](https://bexhoma.readthedocs.io/en/latest/Config.html)
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

For full power, use this tool as an orchestrator as in [2]. It also starts a monitoring container using [Prometheus](https://prometheus.io/) and a metrics collector container using [cAdvisor](https://github.com/google/cadvisor). It also uses the Python package [dbmsbenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker), [3], as query executor and evaluator as in [1,2].
See the [images](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/) folder for more details.

## Contributing, Bug Reports

If you have any question or found a bug, please report them to our [Github issue tracker](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues).
In any bug report, please let us know:

* Which operating system and hardware (32 bit or 64 bit) you are using
* Python version
* Bexhoma version (or git commit/date)
* Traceback that occurs (the full error message)

We are always looking for people interested in helping with code development, documentation writing, technical administration, and whatever else comes up.
If you wish to contribute, please first read the [contribution section](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/docs/CONTRIBUTING.md) or visit the [documentation](https://bexhoma.readthedocs.io/en/latest/CONTRIBUTING.html).

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
