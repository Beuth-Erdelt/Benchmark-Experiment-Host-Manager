# Example: YCSB

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

References:
1. https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload

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
    -nbp 1,8 \
    -nbt 64 \
    -nbf 2,3 \
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
      * threads = 64/`n`
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=1)
      * imports it into the DBMS
  * loops over `m` in [1,8] and `s` in [2,3]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 1.000.000 operations
      * workload A = 50% read / 50% write (`--workload`)
      * target throughput is `s` * 16384
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
Benchmarking is tested with [64] threads, split into [1, 8] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-64-1-16384-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:309947380
    datadisk:39372
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-1-16384-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:309947380
    datadisk:39372
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-1-16384-3 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:309947380
    datadisk:39372
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-1-16384-4 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:309947380
    datadisk:39372
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-1-65536-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:312231624
    datadisk:2323612
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-1-65536-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:312809324
    datadisk:2901312
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-1-65536-3 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:312999124
    datadisk:3091112
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-1-65536-4 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:313136836
    datadisk:3228824
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:312358576
    datadisk:2450056
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:312804344
    datadisk:2895824
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-3 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:312979088
    datadisk:3070568
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-4 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:313133696
    datadisk:3225176
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:312293100
    datadisk:2384236
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:312805416
    datadisk:2896092
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-3 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:312979960
    datadisk:3070620
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-65536-4 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:313134648
    datadisk:3225308
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-1-16384               1       64   16384          1                       0.000000                10233.0                   0                                0.00
PostgreSQL-64-8-16384               1       64   16384          8                   16339.268600                61205.0             1000000                              634.25
PostgreSQL-64-1-65536               1       64   65536          1                   64160.143719                15586.0             1000000                             4099.00
PostgreSQL-64-8-65536               1       64   65536          8                   64817.216610                15431.0             1000000                             3308.50

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-1-16384-1               1       64   32768          1                       32454.89                30812.0                 0                              0.00                   0                                0.00
PostgreSQL-64-1-65536-1               1       64   32768          1                       32404.41                30860.0            500789                            375.00              499211                              572.00
PostgreSQL-64-8-16384-1               1       64   32768          1                       32425.42                30840.0            500473                            384.00              499527                              566.00
PostgreSQL-64-8-65536-1               1       64   32768          1                       32410.71                30854.0            499892                            398.00              500108                              585.00
PostgreSQL-64-1-16384-2               1       64   32768          8                       32588.42                30695.0                 0                              0.00                   0                                0.00
PostgreSQL-64-1-65536-2               1       64   32768          8                       32585.10                30707.0            500025                            367.38              499975                              509.88
PostgreSQL-64-8-16384-2               1       64   32768          8                       32586.03                30696.0            500376                            371.75              499624                              515.75
PostgreSQL-64-8-65536-2               1       64   32768          8                       32591.07                30690.0            501194                            392.50              498806                              524.12
PostgreSQL-64-1-16384-3               1       64   49152          1                       48306.85                20701.0                 0                              0.00                   0                                0.00
PostgreSQL-64-1-65536-3               1       64   49152          1                       48358.24                20679.0            500744                            507.00              499256                              799.00
PostgreSQL-64-8-16384-3               1       64   49152          1                       48285.85                20710.0            500172                            444.00              499828                              745.00
PostgreSQL-64-8-65536-3               1       64   49152          1                       48376.95                20671.0            500631                            455.00              499369                              680.00
PostgreSQL-64-1-16384-4               1       64   49152          8                       48738.89                20537.0                 0                              0.00                   0                                0.00
PostgreSQL-64-1-65536-4               1       64   49152          8                       48736.51                20530.0            500011                            379.38              499989                              540.25
PostgreSQL-64-8-16384-4               1       64   49152          8                       48734.14                20536.0            500680                            402.50              499320                              595.00
PostgreSQL-64-8-65536-4               1       64   49152          8                       48738.59                20525.0            500381                            381.25              499619                              548.75
TEST failed: [OVERALL].Throughput(ops/sec) contains 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```

We can see that the overall throughput is close to the target and that scaled-out drivers (8 pods with 8 threads each) have similar results as a monolithic driver (1 pod with 64 thread).
The runtime is between 8 seconds and 1 minute.

To see the summary of experiment `1726160982` you can simply call `python ycsb.py -e 1726160982 summary`.

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
### Ingestion
                          SUT - CPU of Ingestion (via counter) [CPUs]  SUT - Max RAM of Ingestion [Gb]
PostgreSQL-64-1-16384-1                                        211.08                             3.56
PostgreSQL-64-1-32768-1                                        208.34                             3.51
PostgreSQL-64-1-49152-1                                         43.55                             2.78
PostgreSQL-64-1-65536-1                                         95.57                             3.16
PostgreSQL-64-1-81920-1                                        224.71                             3.50
PostgreSQL-64-1-98304-1                                        208.72                             3.50
PostgreSQL-64-1-114688-1                                        39.80                             2.74
PostgreSQL-64-1-131072-1                                       142.15                             3.47
PostgreSQL-64-8-16384-1                                        192.93                             3.51
PostgreSQL-64-8-32768-1                                        185.90                             3.50
PostgreSQL-64-8-49152-1                                        191.40                             3.81
PostgreSQL-64-8-65536-1                                        189.31                             3.77
PostgreSQL-64-8-81920-1                                        141.00                             3.46
PostgreSQL-64-8-98304-1                                        117.22                             3.28
PostgreSQL-64-8-114688-1                                       209.95                             3.50
PostgreSQL-64-8-131072-1                                       208.55                             3.50

### Execution
                          SUT - CPU of Execution (via counter) [CPUs]  SUT - Max RAM of Execution [Gb]
PostgreSQL-64-1-16384-1                                        158.03                             4.02
PostgreSQL-64-1-32768-1                                        171.52                             4.02
PostgreSQL-64-1-49152-1                                        131.15                             3.98
PostgreSQL-64-1-65536-1                                        185.56                             3.68
PostgreSQL-64-1-81920-1                                          0.00                             3.50
PostgreSQL-64-1-98304-1                                          0.00                             3.50
PostgreSQL-64-1-114688-1                                         0.00                             3.50
PostgreSQL-64-1-131072-1                                         0.00                             3.50
PostgreSQL-64-8-16384-1                                        122.51                             3.98
PostgreSQL-64-8-32768-1                                        110.22                             3.97
PostgreSQL-64-8-49152-1                                        163.70                             4.00
PostgreSQL-64-8-65536-1                                          0.00                             3.50
PostgreSQL-64-8-81920-1                                        169.54                             4.00
PostgreSQL-64-8-98304-1                                         66.88                             3.92
PostgreSQL-64-8-114688-1                                       190.45                             3.69
PostgreSQL-64-8-131072-1                                       146.15                             4.02
```

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.

In this example, metrics are very instable. Metrics are fetched every 30 seconds.
This is too coarse for such a quick example.

## Perform Execution Benchmark

The default behaviour of bexhoma is that several different settings of the loading component are compared.
We might only want to benchmark the workloads of YCSB in different configurations and have a fixed loading phase.

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: `python ycsb.py -ms 1 -m --workload a -tr -nlp 1 -dbms PostgreSQL -ne 1,2 -nc 2 -ltf 2 run`

This loads a YCSB data set with 1 pod (`-lnp`) of 64 threads.
There are two executions (`-ne`) run against the database, the first with 1 driver and the second with two drivers.
Each of the drivers has 64 threads and a target of twice (`-ltf`) the base, that is 16384 per default.
The experiment is run twice (`-nc`).


```
## Show Summary

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-1-32768               1       64   32768          1                   32337.343164                30924.0             1000000                              2913.0
PostgreSQL-64-1-32768               2       64   32768          1                   32355.129906                30907.0             1000000                              2705.0

### Execution
                           experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-1-32768-1-1               1       64   32768          1                       32369.79                30893.0            499162                             888.0              500838                              1467.0
PostgreSQL-64-1-32768-1-2               1      128   65536          2                       55616.72                36454.0            999790                            1446.0             1000210                             11679.0
PostgreSQL-64-1-32768-2-1               2       64   32768          1                       32371.89                30891.0            499548                             542.0              500452                               829.0
PostgreSQL-64-1-32768-2-2               2      128   65536          2                       64706.09                30926.0            999404                            1392.0             1000596                              3480.0
```

## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example: `python ycsb.py -ms 1 -m -dbms MySQL --workload a -tr -nc 2 -rst local-hdd -rss 50Gi run`

The following status shows we have two volumes of type `local-hdd`. Every experiment running YCSB of SF=1, if it's MySQL or PostgreSQL, will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of MySQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                            | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+====================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-postgresql-ycsb-1  | postgresql      | ycsb-1       | True         |                64 | PostgreSQL | shared               | 50Gi      | Bound    | 50G    | 2.1G   |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
+------------------+--------------+--------------+--------------------------+

+------------------+--------------+--------------+--------------+---------------+
| 1706957093       | sut          |   loaded [s] | monitoring   | benchmarker   |
+==================+==============+==============+==============+===============+
| MySQL-64-1-16384 | (2. Running) |      2398.11 | (Running)    | (1. Running)  |
+------------------+--------------+--------------+--------------+---------------+
```




