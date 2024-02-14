# Concepts

An **experiment** is a benchmark of a DBMS in a certain **host setting** and a specific **benchmark setting**.

A **host setting** consists of
* a DBMS (as a docker image)
* a volume (containing some data)
* init scripts (for pre-loading and post-loading)

A **benchmark setting** consists of
* a number of client processes
* a number of runs per connection
* a maximum timeout
* a lot more, depending on the benchmark tool, e.g. [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker)

## Workflow

The **management** roughly means
* start a DBMS and load raw data
* run some benchmarks, fetch metrics and do reporting
* shut down environment and clean up

<p align="center">
    <img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/architecture.png" width="640">
</p>

In more detail this means
1. **Prepare Experiment**  
    1. Use Virtual Machines provided as K8s nodes - create deployment
    1. Attach Network - create service
    1. Attach Data Storage Volume - attach PVC
    1. Start Monitoring - start node exporters and Prometheus as docker containers
1. **Start Experiment**  
    1. Start DBMS Docker Container, upload and run pre-loading init scripts (e.g., create schema), load data, upload and run post-loading init scripts (e.g., create indexes)
1. **Run Benchmarks**  
1. **Report**  
    1. Pull Logs from containers
    1. Pull Metrics from Prometheus monitoring server
1. **Stop Experiment**
1. **Clean Experiment**  
    1. Delete deployment and services
