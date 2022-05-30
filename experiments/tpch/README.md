# Command Line Tool for TPC-H

The folder contains DDL scripts and a query file for some DBMS.

The tool `tpch` helps perform some tasks related to TPC-H benchmark.
It installs MonetDB and PostgreSQL, loads the data, profiles loading or runs the reading queries.
It also starts an evaluation dashboard.

Recommended settings: `tpch run -sf 1 -t 30 -dt`

For more detail about options.

## Tutorials

### Install Data

### Start a DBMS

### Start a DBMS and Load Data

### Start a DBMS and Load Data and Connect

## Options

```
usage: tpch.py [-h] [-db] [-c CONNECTION] [-cx CONTEXT] [-e EXPERIMENT] [-d] [-m] [-ms MAX_SUT] [-dt]
               [-md MONITORING_DELAY] [-nr NUM_RUN] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-sf SCALING_FACTOR]
               [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU]
               [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE]
               [-rnn REQUEST_NODE_NAME]
               {profiling,run,start,load}

Perform TPC-H inspired benchmarks in a Kubernetes cluster. This either profiles the imported data in several DBMS and
compares some statistics, or runs the TPC-H queries. Optionally monitoring is actived. User can choose to detach the
componenten of the benchmarking system, so that as much as possible is run inside a Kubernetes (K8s) cluster. User can
also choose some parameters like number of runs per query and configuration and request some resources.

positional arguments:
  {profiling,run,start,load}
                        profile the import of TPC-H data, or run the TPC-H queries, or start DBMS and load data, or
                        just start the DBMS

optional arguments:
  -h, --help            show this help message and exit
  -db, --debug          dump debug informations
  -c CONNECTION, --connection CONNECTION
                        name of DBMS
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
  -e EXPERIMENT, --experiment EXPERIMENT
                        sets experiment code for continuing started experiment
  -d, --detached        puts most of the experiment workflow inside the cluster
  -m, --monitoring      activates monitoring
  -ms MAX_SUT, --max-sut MAX_SUT
                        maximum number of parallel DBMS configurations, default is no limit
  -dt, --datatransfer   activates datatransfer
  -md MONITORING_DELAY, --monitoring-delay MONITORING_DELAY
                        time to wait [s] before execution of the runs of a query
  -nr NUM_RUN, --num-run NUM_RUN
                        number of runs per query
  -nc NUM_CONFIG, --num-config NUM_CONFIG
                        number of runs per configuration
  -ne NUM_QUERY_EXECUTORS, --num-query-executors NUM_QUERY_EXECUTORS
                        comma separated list of number of parallel clients
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF)
  -t TIMEOUT, --timeout TIMEOUT
                        timeout for a run of a query
  -rr REQUEST_RAM, --request-ram REQUEST_RAM
                        request ram
  -rc REQUEST_CPU, --request-cpu REQUEST_CPU
                        request cpus
  -rct REQUEST_CPU_TYPE, --request-cpu-type REQUEST_CPU_TYPE
                        request node having node label cpu=
  -rg REQUEST_GPU, --request-gpu REQUEST_GPU
                        request number of gpus
  -rgt REQUEST_GPU_TYPE, --request-gpu-type REQUEST_GPU_TYPE
                        request node having node label gpu=
  -rst {None,,local-hdd,shared}, --request-storage-type {None,,local-hdd,shared}
                        request persistent storage of certain type
  -rss REQUEST_STORAGE_SIZE, --request-storage-size REQUEST_STORAGE_SIZE
                        request persistent storage of certain size
  -rnn REQUEST_NODE_NAME, --request-node-name REQUEST_NODE_NAME
                        request a specific node
```
