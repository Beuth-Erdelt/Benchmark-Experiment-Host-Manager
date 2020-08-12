# Benchmark Experiment Host Manager
This Python tools helps **managing benchmark experiments of Database Management Systems (DBMS) in a High-Performance-Computing (HPC) cluster environment**.
It enables users to configure hardware / software setups for easily repeating tests over varying configurations.
The basic workflow is: start a virtual machine, install monitoring software and a database management system, import data, run benchmarks (external tool) and shut down everything with a single command.
A more advanced workflow is: Plan a sequence of such experiments, run plan as a batch and join results for comparison.
This tool supports AWS and kubernetes (k8s) based clusters.

This documentation
* illustrates the [concepts](docs/Concept.md)
* provides [basic examples](docs/Examples.md)
  * [Example: TPC-H Benchmark for 3 DBMS on 1 Virtual Machine](docs/Examples.md#example-tpc-h-benchmark-for-3-dbms-on-1-virtual-machine)
  * [Example: TPC-H Benchmark for 1 DBMS on 3 Virtual Machines](docs/Examples.md#example-tpc-h-benchmark-for-1-dbms-on-3-virtual-machines)
* defines [how to configure an experiment setup](docs/Config.md)
* goes into more detail about the [API](docs/API.md), that is the commands for
  * [Run an Experiment](docs/API.md#run-experiment)
  * [Prepare an Experiment](docs/API.md#prepare-experiment)
  * [Start an Experiment](docs/API.md#start-experiment)
  * [Run Benchmarks](docs/API.md#run-benchmarks)
  * [Stop an Experiment](docs/API.md#stop-experiment)
  * [Clean an Experiment](docs/API.md#clean-experiment)
* shows [alternative workflows](docs/API.md#alternative-workflows)
  * [Parking DBMS at AWS](docs/API.md#parking-dbms-at-aws)
  * [Rerun a List of Experiments](docs/API.md#rerun-a-list-of-experiments)

