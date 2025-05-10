# Benchmark: YCSB

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

YCSB does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients.
It is not self-evident and sure, that scale-out and scale-up yield the same performance results [3].

> The goal of the YCSB project is to develop a framework and common set of workloads for evaluating the performance of different “key-value” and “cloud” serving stores. [...]
The workloads in the core package are a variation of the same basic application type. In this application, there is a table of records, each with F fields. Each record is identif ied by a primary key, which is a string like “user234123”. Each field is named field0, field1 and so on. The values of each field are a random string of ASCII characters of length L.
Each operation against the data store is randomly chosen to be one of:
> * Insert: Insert a new record.
> * Update: Update a record by replacing the value of one f ield. 
> * Read: Read a record, either one randomly chosen field or all fields.
> * Scan: Scan records in order, starting at a randomly chosen record key. The number of records to scan is randomly chosen. [1,2]

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Perform Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 1,8 \
  -nlt 64 \
  -nlf 1,4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 2 \
  -ne 1 \
  -nc 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_loading.log &
```

This
* loops over `n` in [1,8] and `t` in [1,4]
  * starts a clean instance of PostgreSQL (`-dbms`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=1, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [2]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 1.000.000 operations
      * workload A = 50% read / 50% write (`--workload`)
      * target throughput is `s` * 16384
      * threads = 64/`m` (`-nbt`)
    * with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+-----------------------+--------------+--------------+------------+-------------+
| 1726160982            | sut          |   loaded [s] | use case   | loading     |
+=======================+==============+==============+============+=============+
| PostgreSQL-64-1-16384 | (1. Running) |            1 | ycsb       | (1 Running) |
+-----------------------+--------------+--------------+------------+-------------+
```

The code `1726160982` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1726160982` (removes everything that is related to experiment `1726160982`).

## Evaluate Results

At the end of a benchmark you will see a summary like

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1247s 
    Code: 1728322000
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are [1, 4]. Factors for benchmarking are [2].
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 and 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-1-16384-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251422884
    datadisk:2451992
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-1-65536-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251194716
    datadisk:2223824
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251421216
    datadisk:2450324
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250962808
    datadisk:2008132
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-1-16384               1       64   16384          1                   16259.898213                61501.0             1000000                             1098.00
PostgreSQL-64-8-16384               1       64   16384          8                   16317.140308                61299.0             1000000                              885.25
PostgreSQL-64-1-65536               1       64   65536          1                   63617.278453                15719.0             1000000                             4751.00
PostgreSQL-64-8-65536               1       64   65536          8                   64516.680497                15519.0             1000000                             3490.00

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-1-16384-1               1       64   32768          1                       32318.53                30942.0            500686                             544.0              499314                               838.0
PostgreSQL-64-1-65536-1               1       64   32768          1                       32357.22                30905.0            499820                             430.0              500180                               628.0
PostgreSQL-64-8-16384-1               1       64   32768          1                       32302.87                30957.0            500117                             448.0              499883                               637.0
PostgreSQL-64-8-65536-1               1       64   32768          1                       32304.96                30955.0            500283                             476.0              499717                               743.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[1]]
DBMS PostgreSQL-64-8-16384 - Pods [[1]]
DBMS PostgreSQL-64-1-65536 - Pods [[1]]
DBMS PostgreSQL-64-1-16384 - Pods [[1]]

#### Planned
DBMS PostgreSQL-64-1-16384 - Pods [[1]]
DBMS PostgreSQL-64-1-65536 - Pods [[1]]
DBMS PostgreSQL-64-8-16384 - Pods [[1]]
DBMS PostgreSQL-64-8-65536 - Pods [[1]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
```

We can see that the overall throughput is very close to the target and that scaled-out drivers (8 pods with 8 threads each) have similar results as a monolithic driver (1 pod with 64 thread).
The runtime is between 8 seconds and 1 minute.

To see the summary again you can simply call `bexperiments summary -e 1708411664` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server in the cluster by `bexperiments dashboard`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

You can connect to an evaluation server locally by `bexperiments jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

### Time Series of Metrics

See an [example notebook](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/dev/Evaluation-YCSB-Timeseries-1739274625-Heatmaps-Compare.ipynb) about how to analyze results in detail.

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

There are per DBMS
* `initschema`-files, that are invoked before loading of data
* `checkschema`-files, that are invoked after loading of data

You can find the output of the files in the result folder.



### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/ycsb

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python ycsb.py -h`

```bash
usage: ycsb.py [-h] [-aws] [-dbms {PostgreSQL,MySQL}] [-db] [-cx CONTEXT] [-e EXPERIMENT] [-m] [-mc] [-ms MAX_SUT] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nl NUM_LOADING] [-nlp NUM_LOADING_PODS] [-wl {a,b,c,e,f}] [-sf SCALING_FACTOR] [-sfo SCALING_FACTOR_OPERATIONS] [-su SCALING_USERS]
               [-sbs SCALING_BATCHSIZE] [-ltf LIST_TARGET_FACTORS] [-tb TARGET_BASE] [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING]
               [-rnb REQUEST_NODE_BENCHMARKING] [-tr]
               {run,start,load,summary}

Perform YCSB benchmarks in a Kubernetes cluster. Number of rows and operations is SF*1,000,000. This installs a clean copy for each target and split of the driver. Optionally monitoring is activated.

positional arguments:
  {run,start,load,summary}
                        import YCSB data or run YCSB queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms {PostgreSQL,MySQL}, --dbms {PostgreSQL,MySQL}
                        DBMS to load the data
  -db, --debug          dump debug informations
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
  -e EXPERIMENT, --experiment EXPERIMENT
                        sets experiment code for continuing started experiment
  -m, --monitoring      activates monitoring for sut
  -mc, --monitoring-cluster
                        activates monitoring for all nodes of cluster
  -ms MAX_SUT, --max-sut MAX_SUT
                        maximum number of parallel DBMS configurations, default is no limit
  -nc NUM_CONFIG, --num-config NUM_CONFIG
                        number of runs per configuration
  -ne NUM_QUERY_EXECUTORS, --num-query-executors NUM_QUERY_EXECUTORS
                        comma separated list of number of parallel clients
  -nl NUM_LOADING, --num-loading NUM_LOADING
                        number of parallel loaders per configuration
  -nlp NUM_LOADING_PODS, --num-loading-pods NUM_LOADING_PODS
                        total number of loaders per configuration
  -wl {a,b,c,e,f}, --workload {a,b,c,e,f}
                        YCSB default workload
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF) = number of rows in millions
  -sfo SCALING_FACTOR_OPERATIONS, --scaling-factor-operations SCALING_FACTOR_OPERATIONS
                        scaling factor = number of operations in millions (=SF if not set)
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
                        request ram for sut, default 16Gi
  -rc REQUEST_CPU, --request-cpu REQUEST_CPU
                        request cpus for sut, default 4
  -rct REQUEST_CPU_TYPE, --request-cpu-type REQUEST_CPU_TYPE
                        request node for sut to have node label cpu=
  -rg REQUEST_GPU, --request-gpu REQUEST_GPU
                        request number of gpus for sut
  -rgt REQUEST_GPU_TYPE, --request-gpu-type REQUEST_GPU_TYPE
                        request node for sut to have node label gpu=
  -rst {None,,local-hdd,shared}, --request-storage-type {None,,local-hdd,shared}
                        request persistent storage of certain type
  -rss REQUEST_STORAGE_SIZE, --request-storage-size REQUEST_STORAGE_SIZE
                        request persistent storage of certain size
  -rnn REQUEST_NODE_NAME, --request-node-name REQUEST_NODE_NAME
                        request a specific node for sut
  -rnl REQUEST_NODE_LOADING, --request-node-loading REQUEST_NODE_LOADING
                        request a specific node for loading pods
  -rnb REQUEST_NODE_BENCHMARKING, --request-node-benchmarking REQUEST_NODE_BENCHMARKING
                        request a specific node for benchmarking pods
  -tr, --test-result    test if result fulfills some basic requirements
```

## Perform Execution Benchmark

The default behaviour of bexhoma is that several different settings of the loading component are compared.
We might only want to benchmark the workloads of YCSB in different configurations and have a fixed loading phase.

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_benchmarking.log &
```
This loads a YCSB data set with 8 pods (`-lnp`) of 64 threads in total.
Each of the drivers has 64 threads and a target of twice or three times (`-ltf`) the base, that is 16384.

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 587s 
    Code: 1728323200
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are [4]. Factors for benchmarking are [2, 3].
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251421196
    datadisk:2450136
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251867724
    datadisk:2896664
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:252041700
    datadisk:3070640
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:252196440
    datadisk:3225380
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8                   64503.674093                15526.0             1000000                             3232.75

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   32768          1                       32301.83                30958.0            499471                            458.00              500529                              668.00
PostgreSQL-64-8-65536-2               1       64   32768          8                       32504.47                30781.0            500367                            425.62              499633                              550.50
PostgreSQL-64-8-65536-3               1       64   49152          1                       48160.28                20764.0            500544                            568.00              499456                              852.00
PostgreSQL-64-8-65536-4               1       64   49152          8                       48577.89                20600.0            499918                            456.38              500082                              641.12

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[8, 8, 1, 1]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[1, 8, 1, 8]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
```

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_monitoring.log &
```

If monitoring is activated, the summary also contains a section like

```bash
## Show Summary

### Workload
    YCSB SF=1
    Type: ycsb
    Duration: 591s 
    Code: 1728064423
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are [4]. Factors for benchmarking are [2, 3].
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS ['PostgreSQL'].
Import is handled by 8 processes (pods).
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Loading is tested with [64] threads, split into [8] pods.
Benchmarking is tested with [64] threads, split into [1, 8] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251395812
    datadisk:2450228
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251841380
    datadisk:2895796
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:252015852
    datadisk:3070268
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:252170524
    datadisk:3224940
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8                   64499.496345                15517.0             1000000                              3416.5

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   32768          1                       32311.22                30949.0            499709                            477.00              500291                              774.00
PostgreSQL-64-8-65536-2               1       64   32768          8                       32507.91                30774.0            499866                            414.25              500134                              543.88
PostgreSQL-64-8-65536-3               1       64   49152          1                       48118.56                20782.0            499867                            543.00              500133                              893.00
PostgreSQL-64-8-65536-4               1       64   49152          8                       48585.56                20604.0            500205                            453.38              499795                              622.38

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[8, 1, 8, 1]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[1, 8, 1, 8]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1       31.69        0          2.72                 2.81
PostgreSQL-64-8-65536-2       31.69        0          2.72                 2.81
PostgreSQL-64-8-65536-3       31.69        0          2.72                 2.81
PostgreSQL-64-8-65536-4       31.69        0          2.72                 2.81

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1        0.01        0           0.0                  0.0
PostgreSQL-64-8-65536-2        0.01        0           0.0                  0.0
PostgreSQL-64-8-65536-3        0.01        0           0.0                  0.0
PostgreSQL-64-8-65536-4        0.01        0           0.0                  0.0

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      184.63     0.00          3.85                 4.35
PostgreSQL-64-8-65536-2      122.81     0.00          4.02                 4.65
PostgreSQL-64-8-65536-3      173.42     3.06          3.70                 4.35
PostgreSQL-64-8-65536-4        0.24     0.00          3.70                 4.35

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1        0.00      0.0          0.00                 0.00
PostgreSQL-64-8-65536-2        6.22      0.0          0.12                 0.12
PostgreSQL-64-8-65536-3        0.00      0.0          0.12                 0.12
PostgreSQL-64-8-65536-4        0.00      0.0          0.12                 0.12

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]

TEST passed: Workflow as planned
```

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.

In this example, metrics are very instable. Metrics are fetched every 30 seconds.
This is too coarse for such a quick example.

## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_storage.log &
```
The following status shows we have one volume of type `shared`.
Every PostgreSQL experiment running YCSB of SF=1 will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of PostgreSQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                  | configuration   | experiment    | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+==========================================+=================+===============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-postgresql-ycsb-1        | postgresql      | ycsb-1        | True         |                16 | PostgreSQL | shared               | 100Gi     | Bound    | 100G   | 3.7G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-ycsb-10       | postgresql      | ycsb-10       | True         |               217 | PostgreSQL | shared               | 100Gi     | Bound    | 100G   | 33G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like


```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1295s 
    Code: 1742312868
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [2, 3].
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-64-8-65536-1-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:145339028
    datadisk:2393
    volume_size:30G
    volume_used:2.4G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1742312868
PostgreSQL-64-8-65536-1-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:145339028
    datadisk:2829
    volume_size:30G
    volume_used:2.4G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1742312868
PostgreSQL-64-8-65536-1-3 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:145339028
    datadisk:2999
    volume_size:30G
    volume_used:2.4G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1742312868
PostgreSQL-64-8-65536-1-4 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:145339028
    datadisk:3150
    volume_size:30G
    volume_used:2.4G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1742312868
PostgreSQL-64-8-65536-2-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:145339020
    datadisk:3271
    volume_size:30G
    volume_used:3.2G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1742312868
PostgreSQL-64-8-65536-2-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:145339020
    datadisk:3286
    volume_size:30G
    volume_used:3.2G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
        code:1742312868
PostgreSQL-64-8-65536-2-3 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:145339020
    datadisk:3288
    volume_size:30G
    volume_used:3.2G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
        code:1742312868
PostgreSQL-64-8-65536-2-4 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:145339020
    datadisk:3290
    volume_size:30G
    volume_used:3.2G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
        code:1742312868

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8           0                   64525.508843                15514.0             1000000                             3430.75

### Execution
                           experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1-1               1       64   32768          1           0                       32375.03                30888.0            499915                             462.0              500085                               684.0
PostgreSQL-64-8-65536-1-2               1       64   32768          8           0                       32515.84                30780.0            500370                             466.0              499630                               576.0
PostgreSQL-64-8-65536-1-3               1       64   49152          1           0                       48044.59                20814.0            500330                             561.0              499670                               858.0
PostgreSQL-64-8-65536-1-4               1       64   49152          8           0                       48582.31                20596.0            498940                             560.0              501060                               699.0
PostgreSQL-64-8-65536-2-1               2       64   32768          1           0                       32351.99                30910.0            500515                             953.0              499485                              1547.0
PostgreSQL-64-8-65536-2-2               2       64   32768          8           0                       32507.38                30785.0            500111                             426.0              499889                               545.0
PostgreSQL-64-8-65536-2-3               2       64   49152          1           0                       47980.04                20842.0            499921                             552.0              500079                               875.0
PostgreSQL-64-8-65536-2-4               2       64   49152          8           0                       48570.82                20608.0            500135                             553.0              499865                               670.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[8, 8, 1, 1], [8, 1, 8, 1]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[1, 8, 1, 8], [1, 8, 1, 8]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
```

Note the added section about `volume_size` and `volume_used` in the connections section.


## All Workloads

### Workload A

Workload A is 50% READ and 50% UPDATE.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_a.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 1000s 
    Code: 1746620772
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 10000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.5.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:254618920
    datadisk:23601
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1746620772
PostgreSQL-64-8-65536-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:258958780
    datadisk:27839
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1746620772

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8           0                   37091.016615               271019.0            10000000                              5949.5

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   65536          1           0                       65359.05               153001.0           4999188                             671.0             5000812                              1432.0
PostgreSQL-64-8-65536-2               1       64   65536          8           0                       65430.41               152846.0           4999421                             447.0             5000579                               999.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[8, 1]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[1, 8]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      1774.7      6.2         14.28                18.29
PostgreSQL-64-8-65536-2      1774.7      6.2         14.28                18.29

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      1123.2      1.8          4.62                 4.64
PostgreSQL-64-8-65536-2      1123.2      1.8          4.62                 4.64

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1332.65    11.55         17.20                22.58
PostgreSQL-64-8-65536-2     1359.55    10.46         17.69                23.51

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      880.36     6.38          0.60                 0.61
PostgreSQL-64-8-65536-2      508.45     1.84          5.15                 5.18

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



### Workload B

Workload B is 95% READ and 5% UPDATE.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload b \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 8 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_b.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 849s 
    Code: 1746621852
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'B'.
    Number of rows to insert is 10000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.5.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:254627344
    datadisk:23609
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1746621852

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8           0                   35929.486434               280615.0            10000000                              6012.5

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   65536          8           0                       65428.59               152848.0           9500698                             421.0              499302                               656.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[8]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[8]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1781.99     5.71         14.55                18.47

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1067.21     2.62          4.62                 4.64

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1436.04     7.73         15.84                20.27

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      673.32     2.35          4.56                 4.58

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



### Workload C

Workload C is 100% READ.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload c \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 8 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_c.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 839s 
    Code: 1746622753
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'C'.
    Number of rows to insert is 10000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.5.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:254620740
    datadisk:23603
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1746622753

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8           0                   35060.192335               287528.0            10000000                              6109.5

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   65536          8           0                        65428.7               152852.0          10000000                             437.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[8]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[8]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1755.21     5.74         14.71                18.53

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1046.93     1.66          4.62                 4.64

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1339.43     8.57         15.49                19.71

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      666.26     2.42          4.54                 4.56

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



### Workload D

Workload D is 95% READ and 5% INSERT.
This means there are more rows in the database after the benchmark than before the benchmark.
The range of key that can be read or inserted changes.
Repetition is only fully sensible after a clean creation of the database.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload d \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_d.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 804s 
    Code: 1747036729
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'D'.
    Number of rows to insert is 10000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.5.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:255174140
    datadisk:23601
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1747036729

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8           0                   34879.995039               288656.0            10000000                              6341.5

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)  [READ].Return=OK  [READ].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   65536          1           0                       65343.25               153038.0              499213                               572.0           9500787                             404.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[1]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1688.38     6.16         14.43                 18.1

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1024.95     2.67          4.62                 4.65

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1316.93     8.17         15.95                20.53

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      635.94     4.42           0.6                  0.6

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



### Workload E

Workload E is 95% SCAN and 5% INSERT.
This means there are more rows in the database after the benchmark than before the benchmark.
The range of key that can be read or inserted changes.
Repetition is only fully sensible after a clean creation of the database.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload e \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_e.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 1137s 
    Code: 1747037570
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'E'.
    Number of rows to insert is 10000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.5.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:255177920
    datadisk:23605
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1747037570

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8           0                   35973.979103               280240.0            10000000                              5956.0

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)  [SCAN].Return=OK  [SCAN].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   65536          1           0                       22449.46               445445.0              500712                              3979.0           9499288                           40351.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[1]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1821.34     5.76         13.91                18.22

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1163.93     1.62          4.62                 4.64

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     7874.79    26.16         16.12                20.91

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     2890.42     10.4          0.62                 0.62

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



### Workload F

Workload F is 50% READ and 50% READ-MODIFY-WRITE.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload f \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 8 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_f.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 783s 
    Code: 1747038770
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'F'.
    Number of rows to insert is 10000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.5.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:255178652
    datadisk:23605
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1747038770

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8           0                   35691.857812               281320.0            10000000                              6054.5

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)  [READ-MODIFY-WRITE].Operations  [READ-MODIFY-WRITE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   65536          8           0                       65426.83               152859.0          10000000                            1335.0             5000670                              1619.0                         5000670                                         2421.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[8]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[8]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1816.46     6.15         13.91                18.24

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1186.28     1.69          4.62                 4.64

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      1971.6    14.67         17.29                22.88

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      670.32     4.02          4.58                 4.61

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```




