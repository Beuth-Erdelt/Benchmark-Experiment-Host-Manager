# Example: YCSB

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

References:
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Perform Benchmark

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```
python ycsb.py -ms 1 -tr \
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
  run
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
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are []. Factors for benchmarking are [].
Benchmark is limited to DBMS PostgreSQL.
Import is handled by 1 and 8 processes (pods).
Loading is tested with [64] threads, split into [1, 8] pods.
Benchmarking is tested with [64] threads, split into [1] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-64-1-16384-1 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:180714156
    datadisk:2452172
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-1-65536-1 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:180467768
    datadisk:2205784
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:180712468
    datadisk:2450484
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:180466912
    datadisk:2204928
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-1-16384               1       64   16384          1                   16298.590172                61355.0             1000000                              2359.0
PostgreSQL-64-8-16384               1       64   16384          8                   16341.171089                61207.0             1000000                              2705.0
PostgreSQL-64-1-65536               1       64   65536          1                   63488.032506                15751.0             1000000                              7363.0
PostgreSQL-64-8-65536               1       64   65536          8                   64838.241976                15435.0             1000000                              6589.5

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-1-16384-1               1       64   32768          1                       32412.81                30852.0            501161                             764.0              498839                              1324.0
PostgreSQL-64-1-65536-1               1       64   32768          1                       32449.62                30817.0            500076                             910.0              499924                              1517.0
PostgreSQL-64-8-16384-1               1       64   32768          1                       32448.57                30818.0            500877                             800.0              499123                              1329.0
PostgreSQL-64-8-65536-1               1       64   32768          1                       32431.73                30834.0            500143                             712.0              499857                              1258.0
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
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

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

If monitoring is activated, the summary also contains a section like

```bash
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are []. Factors for benchmarking are [].
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS PostgreSQL.
Import is handled by 8 processes (pods).
Loading is tested with [64] threads, split into [8] pods.
Benchmarking is tested with [64] threads, split into [1, 8] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:180847076
    datadisk:2335584
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-2 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:181414628
    datadisk:2899644
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-3 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:181604868
    datadisk:3089884
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-4 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:181742996
    datadisk:3228012
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8                   64791.255996                15516.0             1000000                              6983.0

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   32768          1                       32439.10                30827.0            500169                            751.00              499831                             1386.00
PostgreSQL-64-8-65536-2               1       64   32768          8                       32595.72                30696.0            500396                            745.88              499604                             1028.25
PostgreSQL-64-8-65536-3               1       64   49152          1                       48353.56                20681.0            499847                           1069.00              500153                             1574.00
PostgreSQL-64-8-65536-4               1       64   49152          8                       48757.01                20519.0            500631                            896.25              499369                             1487.38

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      273.11        0          3.75                 4.13
PostgreSQL-64-8-65536-2      273.11        0          3.75                 4.13
PostgreSQL-64-8-65536-3      273.11        0          3.75                 4.13
PostgreSQL-64-8-65536-4      273.11        0          3.75                 4.13

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1        0.27        0          0.01                 0.01
PostgreSQL-64-8-65536-2        0.27        0          0.01                 0.01
PostgreSQL-64-8-65536-3        0.27        0          0.01                 0.01
PostgreSQL-64-8-65536-4        0.27        0          0.01                 0.01

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      254.95     5.44          3.98                 4.50
PostgreSQL-64-8-65536-2      311.48     5.55          4.03                 4.61
PostgreSQL-64-8-65536-3        0.00     0.00          3.70                 4.28
PostgreSQL-64-8-65536-4      304.27     5.17          3.71                 4.30

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1        0.00      0.0          0.00                 0.00
PostgreSQL-64-8-65536-2        3.92      0.0          0.11                 0.12
PostgreSQL-64-8-65536-3       41.76      0.0          0.66                 0.67
PostgreSQL-64-8-65536-4        5.10      0.0          0.82                 0.83
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.

In this example, metrics are very instable. Metrics are fetched every 30 seconds.
This is too coarse for such a quick example.

## Perform Execution Benchmark

The default behaviour of bexhoma is that several different settings of the loading component are compared.
We might only want to benchmark the workloads of YCSB in different configurations and have a fixed loading phase.

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```
python ycsb.py -ms 1 -tr \
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
  run
```
This loads a YCSB data set with 8 pods (`-lnp`) of 64 threads in total.
Each of the drivers has 64 threads and a target of twice or three times (`-ltf`) the base, that is 16384.

```
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are []. Factors for benchmarking are [].
Benchmark is limited to DBMS PostgreSQL.
Import is handled by 8 processes (pods).
Loading is tested with [64] threads, split into [8] pods.
Benchmarking is tested with [64] threads, split into [1, 8] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:180352492
    datadisk:2089996
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-2 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:181161960
    datadisk:2898988
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-3 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:181351820
    datadisk:3089324
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-4 uses docker image postgres:16.1
    RAM:541008601088
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker4
    disk:181490020
    datadisk:3227524
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8                   64841.400426                15435.0             1000000                              6098.5

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   32768          1                       32434.89                30831.0            499060                            805.00              500940                             1263.00
PostgreSQL-64-8-65536-2               1       64   32768          8                       32597.05                30691.0            500736                            709.75              499264                             1106.12
PostgreSQL-64-8-65536-3               1       64   49152          1                       48388.66                20666.0            499989                            937.00              500011                             1562.00
PostgreSQL-64-8-65536-4               1       64   49152          8                       48762.06                20517.0            500258                            800.25              499742                             1340.00
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```

## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```
python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 2 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 50Gi \
  run
```
The following status shows we have one volume of type `shared`.
Every experiment running YCSB of SF=1, if it's MySQL or PostgreSQL, will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of MySQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                            | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+====================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-postgresql-ycsb-1  | postgresql      | ycsb-1       | True         |                64 | PostgreSQL | shared               | 50Gi      | Bound    | 50G    | 2.1G   |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```




