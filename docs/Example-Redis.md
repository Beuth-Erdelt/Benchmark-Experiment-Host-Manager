# Example: Benchmark Redis

This differs from the default behaviour of bexhoma, since we benchmark **a distributed NoSQL DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Redis is a Key / Value store [1].
There is a single-host and a cluster version.
In the cluster version, there are several pods deployed for the worker nodes using a stateful set.
Each shard and each replication needs it's own pod.
Redis cluster does not require a coordinator.
Bexhoma still deploys a main pod (called master) as a substitute for a single point of contact and to annotate status of experiments.
Bexhoma also deploys a service for communication external to Redis (from within the cluster) and a headless service for communication between the pods of the Redis cluster.
See [dummy manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Redis.yml) for a single-host version that is suitable for bexhoma and see [dummy manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-RedisCluster.yml) for a multi-host version that is suitable for bexhoma.

This can be managed by bexhoma.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Redis: https://redis.io/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9


## Perform YCSB Benchmark - Ingestion of Data Included

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
  -sfo 10 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_1.log &
```

This
* loops over `n` in [8] and `t` in [12]
  * starts a clean instance of Redis (`-dbms`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=1, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [4]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 10.000.000 operations (i.e., SF=10, `-sfo`)
      * workload A = 50% read / 50% write (`--workload`)
      * target throughput is `s` * 16384
      * threads = 64/`m` (`-nbt`)
    * with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* monitors (`-m`) all components (`-mc`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+-------------------+--------------+------------+------------------------+
| 1741876409        | sut          | use case   | loading                |
+===================+==============+============+========================+
| Redis-64-8-196608 | (1. Running) | ycsb       | (7 Running)(1 Pending) |
+-------------------+--------------+------------+------------------------+
```

The code `1730133803` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1730133803` (removes everything that is related to experiment `1730133803`).

### Evaluate Results

At the end of a benchmark you will see a summary like

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 810s 
    Code: 1742570653
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Redis-64-8-196608-1 uses docker image redis:7.4.2
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:151739584
    datadisk:1095
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1742570653

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   12375.152296                80983.0             1000000                              7928.5

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1               1      128   65536          1           0                       25682.38               389372.0           4997043                            9463.0             5002957                              9479.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1]]

### Ingestion - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      108.41     0.84          1.74                 1.74

### Ingestion - Loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1       84.27        0           0.5                  0.5

### Execution - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      529.76     1.54          2.81                 2.82

### Execution - Benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1       959.2     2.71          0.59                 0.59

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

To see the summary again you can simply call `bexperiments summary -e 1742224433` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexperiments jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888




## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components.
In the following example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the Redis cluster.


## Distributed DBMS

If you want to deploy Redis as a cluster, you can adjust the number of workers `-nw` when calling the script:
```
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_2.log &
```

yields something like

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 633s 
    Code: 1742571522
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Redis-64-8-196608-1 uses docker image redis:7.4.2
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:150618888
    datadisk:1
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:117486192
        datadisk:718
    worker 1
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:22144724
        datadisk:799
    worker 2
        RAM:540595896320
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker24
        disk:145920520
        datadisk:720
    worker 3
        node:cl-worker12
    eval_parameters
        code:1742571522
        BEXHOMA_WORKERS:3

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   25843.775975                38834.0             1000000                              4961.0

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1               1      128   65536          1           0                       63192.35               158247.0           5001503                            1877.0             4998497                              1873.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1]]

### Ingestion - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      103.89     0.18          1.77                 1.77

### Ingestion - Loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1       85.86        0          0.52                 0.52

### Execution - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      379.45     0.84          1.79                  1.8

### Execution - Benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      554.78        0          0.83                 0.83

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

## Replication

We can set the number of replicas with the parameter `-nwr`.
Note that Redis requires a worker per replicated shard, so `-nw 3` and `-nwr 1` creates 6 worker nodes, 3 for sharding and another 3 for the (single) replicas.

```
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_3.log &
```

yields something like

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 681s
    Code: 1742466306
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Redis-64-8-196608-1 uses docker image redis:7.4.2
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:150613216
    datadisk:1
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:117360996
        datadisk:719
    worker 1
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:22144976
        datadisk:805
    worker 2
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:48292744
        datadisk:719
    worker 3
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:87168020
        datadisk:721
    worker 4
        RAM:540595896320
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker24
        disk:145833304
        datadisk:721
    worker 5
        RAM:1081751007232
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker29
        disk:186216468
        datadisk:802
    worker 6
    eval_parameters
        code:1742466306
        BEXHOMA_REPLICAS:1
        BEXHOMA_WORKERS:3

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   23561.704906                42697.0             1000000                              5286.5

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1               1      128   65536          1           0                       57476.88               173983.0           4998731                            1789.0             5001269                              1793.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1]]

### Ingestion - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1        0.88     0.01          0.01                 0.01

### Ingestion - Loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1        0.05        0           0.0                  0.0

### Execution - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1        1.47     0.01          0.01                 0.01

### Execution - Benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      655.54     5.36          0.82                 0.82

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_4.log &
```

The following status shows we have one volume of type `shared`.
Every single-host Redis experiment running YCSB of SF=1 will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of Redis mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-redis-ycsb-1           | redis           | ycsb-1       | True         |                50 | Redis           | shared               | 50Gi      | Bound    | 50G    | 0      |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like


```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1383s 
    Code: 1742467147
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Redis-64-8-196608-1-1 uses docker image redis:7.4.2
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:150613376
    datadisk:1816
    volume_size:50G
    volume_used:1.8G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1742467147
Redis-64-8-196608-2-1 uses docker image redis:7.4.2
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:150613376
    datadisk:1095
    volume_size:50G
    volume_used:1.1G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1742467147

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                    12654.64816                79208.0             1000000                              7689.0

### Execution
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1-1               1      128   65536          1           0                       26486.56               377550.0           5000075                            9183.0             4999925                              9191.0
Redis-64-8-196608-2-1               2      128   65536          1           0                       27073.86               369360.0           5001542                            9015.0             4998458                              9015.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1], [1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1], [1]]

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      105.44     1.09          1.74                 1.74

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      120.01        0           0.5                  0.5

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      482.22     1.40          2.72                 2.73
Redis-64-8-196608-2-1      680.22     1.57          2.74                 2.74

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      829.47     2.71          0.59                 0.59
Redis-64-8-196608-2-1      829.47     2.84          0.59                 0.59

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

### Redis as a Cluster

Similarly we can make a Redis cluster to store the database in persistent storage.

```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_5.log &
```

Redis expects fully qualified domain name (FQDN) for each pod.
At the same time, the length of hostnames is limited.
Therefore bexhoma will shorten the name of the pods and pvcs in this case.
The first volume is attached to the (dummy) coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.


```
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-redis-ycsb-1           | redis           | ycsb-1       | True         |                48 | Redis           | shared               | 50Gi      | Bound    | 0      | 0      |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
+-------------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| Volumes of Workers                  | configuration     |   experiment | dbms   | storage_class_name   | storage   | status   | size   | used   |
+=====================================+===================+==============+========+======================+===========+==========+========+========+
| bexhoma-workers-bx-w-redis-ycsb-1-0 | Redis-64-8-196608 |   1742468798 | Redis  | shared               | 50Gi      | Bound    | 50G    | 708M   |
+-------------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bexhoma-workers-bx-w-redis-ycsb-1-1 | Redis-64-8-196608 |   1742468798 | Redis  | shared               | 50Gi      | Bound    | 50G    | 800M   |
+-------------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bexhoma-workers-bx-w-redis-ycsb-1-2 | Redis-64-8-196608 |   1742468798 | Redis  | shared               | 50Gi      | Bound    | 50G    | 708M   |
+-------------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1069s
    Code: 1742572213
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Redis-64-8-196608-1-1 uses docker image redis:7.4.2
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:150618888
    datadisk:1
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:21327596
        datadisk:714
        volume_size:50G
        volume_used:712M
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:116752124
        datadisk:791
        volume_size:50G
        volume_used:788M
    worker 2
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:47560664
        datadisk:713
        volume_size:50G
        volume_used:712M
    worker 3
        node:cl-worker12
    eval_parameters
        code:1742572213
        BEXHOMA_WORKERS:3
Redis-64-8-196608-2-1 uses docker image redis:7.4.2
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:150618888
    datadisk:1
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:116752276
        datadisk:972
        volume_size:50G
        volume_used:968M
    worker 1
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:21327620
        datadisk:771
        volume_size:50G
        volume_used:768M
    worker 2
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:47560672
        datadisk:992
        volume_size:50G
        volume_used:988M
    worker 3
        node:cl-worker12
    eval_parameters
        code:1742572213
        BEXHOMA_WORKERS:3

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   24054.585271                41890.0             1000000                              5011.0

### Execution
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1-1               1      128   65536          1           0                       63162.02               158323.0           5002350                            3127.0             4997650                              3121.0
Redis-64-8-196608-2-1               2      128   65536          1           0                       63223.91               158168.0           5001169                            4319.0             4998831                              4311.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1], [1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1], [1]]

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      473.71     0.39          2.35                 2.36

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      129.07        0          0.58                 0.58

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      317.19     1.51          2.30                 2.33
Redis-64-8-196608-2-1      369.86     0.89          2.17                 3.31

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      884.45     0.00          0.83                 0.84
Redis-64-8-196608-2-1      819.22     6.98          0.83                 0.84

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```
'Redis': {
    'loadData': 'redis-cli < {scriptname}',
    'delay_prepare': 0,
    'attachWorker': '',
    'template': {
        'version': 'xxx',
        'alias': 'Key-Value-1',
        'docker_alias': 'KV1',
        'auth': ["root", ""],
    },
    'logfile': '/var/log/redis/redis-server.log',
    'datadir': '/data',
    'priceperhourdollar': 0.0,
},
```

Notice how this does not have a JDBC section (as Redis does not support this).









