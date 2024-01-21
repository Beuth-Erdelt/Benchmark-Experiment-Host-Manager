# Example: YCSB

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

References:
1. https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload

## Perform Benchmark

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: `python ycsb.py -ms 1 -dbms PostgreSQL -workload a -tr run`

This
* loops over `n` in [1,8] and `t` in [1,2,3,4,5,6,7,8]
  * starts a clean instance of PostgreSQL
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n`
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows
      * imports it into the DBMS
  * runs 1 stream of YCSB queries per DBMS
    * 1.000.000 operations
    * workload A = 50% read / 50% write
    * target throughput is `t` * 16384
  * with a maximum of 1 DBMS per time
* tests if results match workflow
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```
|-----------------------|--------------|--------------|----------|---------------|-----------|--------------|---------------|
| 1705792604            | sut          |   loaded [s] | worker   | maintaining   | loading   | monitoring   | benchmarker   |
|=======================|==============|==============|==========|===============|===========|==============|===============|
| PostgreSQL-64-8-98304 | (1. Running) |         2.02 |          |               |           | (Running)    |               |
|-----------------------|--------------|--------------|----------|---------------|-----------|--------------|---------------|
```


### Evaluate Results

At the end of a benchmark you will see a summary like

```
### Loading
                        threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-1-65536        64   65536          1                   59869.484524                16703.0             1000000                             17711.0
PostgreSQL-64-8-65536        64   65536          8                   63990.008246                15691.0             1000000                              6803.5
PostgreSQL-64-1-98304        64   98304          1                   55682.387661                17959.0             1000000                             18095.0
PostgreSQL-64-8-98304        64   98304          8                   74717.773542                13672.0             1000000                             17293.0
PostgreSQL-64-1-131072       64  131072          1                   66436.353973                15052.0             1000000                             17759.0
PostgreSQL-64-8-131072       64  131072          8                   73813.262541                13789.0             1000000                             17127.0
### Execution
                          threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-1-65536-1        64   65536          1                   62383.031815                16030.0            499898                           608.000              500102                            1594.000
PostgreSQL-64-8-65536-1        64   65536          8                   63924.003925                15705.0            501152                           473.875              498848                             828.000
PostgreSQL-64-1-98304-1        64   98304          1                   92764.378479                10780.0            500171                           686.000              499829                            1462.000
PostgreSQL-64-8-98304-1        64   98304          8                   94597.863875                10659.0            499159                           729.000              500841                            1402.875
PostgreSQL-64-1-131072-1       64  131072          1                  111234.705228                 8990.0            500143                          1217.000              499857                            6123.000
PostgreSQL-64-8-131072-1       64  131072          8                  119665.556799                 8648.0            500301                          1625.000              499699                            3476.500
```

Detailed evaluations can be done using
* [Jupyter Notebooks](https://beuth-erdelt.github.io/DBMS-Benchmarker/Evaluation-Demo.html)

You can connect to an evaluation server by `bexperiments dashboard`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

## Adjust Parameters

The script supports
* exact repetitions for statistical confidence
* variations to scan a large parameters space
* combine results for easy evaluation

There are various ways to change parameters.

### Manifests

The YAML manifests for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb

### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/ycsb

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python ycsb.py -h`

```
usage: ycsb.py [-h] [-aws] [-dbms {PostgreSQL,MySQL}] [-workload {a,b,c,d,e,f}] [-db] [-cx CONTEXT] [-e EXPERIMENT] [-d] [-m] [-mc] [-ms MAX_SUT] [-dt] [-md MONITORING_DELAY] [-nr NUM_RUN] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nl NUM_LOADING]
               [-nlp NUM_LOADING_PODS] [-sf SCALING_FACTOR] [-sfo SCALING_FACTOR_OPERATIONS] [-su SCALING_USERS] [-sbs SCALING_BATCHSIZE] [-ltf LIST_TARGET_FACTORS] [-tb TARGET_BASE] [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE]
               [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING] [-rnb REQUEST_NODE_BENCHMARKING] [-tr]
               {run,start,load}

Perform YCSB benchmarks in a Kubernetes cluster. Number of rows and operations is SF*100,000. Optionally monitoring is activated.

positional arguments:
  {run,start,load}      import YCSB data or run YCSB queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms {PostgreSQL,MonetDB,SingleStore,CockroachDB,MySQL,MariaDB,YugabyteDB,Kinetica}
                        DBMS to load the data
  -workload {a,b,c,d,e,f}
                        YCSB default workload
  -db, --debug          dump debug informations
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
  -e EXPERIMENT, --experiment EXPERIMENT
                        sets experiment code for continuing started experiment
  -d, --detached        puts most of the experiment workflow inside the cluster
  -m, --monitoring      activates monitoring for sut
  -mc, --monitoring-cluster
                        activates monitoring for all nodes of cluster
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
  -nl NUM_LOADING, --num-loading NUM_LOADING
                        number of parallel loaders per configuration
  -nlp NUM_LOADING_PODS, --num-loading-pods NUM_LOADING_PODS
                        total number of loaders per configuration
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF) = number of rows in millions
  -sfo SCALING_FACTOR_OPERATIONS, --scaling-factor-operations SCALING_FACTOR_OPERATIONS
                        scaling factor (SF) = number of operations in millions (=SF if not set)
  -su SCALING_USERS, --scaling-users SCALING_USERS
                        scaling factor = number of total threads
  -sbs SCALING_BATCHSIZE, --scaling-batchsize SCALING_BATCHSIZE
                        batch size
  -ltf LIST_TARGET_FACTORS, --list-target-factors LIST_TARGET_FACTORS
                        comma separated list of factors of 16384 ops as target - default range(1,9)
  -tb TARGET_BASE, --target-base TARGET_BASE
                        ops as target, base for factors - default 16384 = 2**14
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
  -rnl REQUEST_NODE_LOADING, --request-node-loading REQUEST_NODE_LOADING
                        request a specific node
  -rnb REQUEST_NODE_BENCHMARKING, --request-node-benchmarking REQUEST_NODE_BENCHMARKING
                        request a specific node
  -tr, --test-result    test if result fulfills some basic requirements

```

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).
