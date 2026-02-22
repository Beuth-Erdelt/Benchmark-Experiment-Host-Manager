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

```bash
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

doc_ycsb_redis_1.log
```markdown
﻿## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 535s 
    Code: 1768489319
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker21.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Redis-64-8-196608-1 uses docker image redis:7.4.2
    RAM:608117153792
    CPU:AMD EPYC 7542 32-Core Processor
    Cores:64
    host:6.8.0-90-generic
    node:cl-worker21
    disk:133663
    datadisk:1095
    cpu_list:0-63
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1768489319

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   17103.422938                58720.0             1000000                              5656.0

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1               1      128   65536          1           0                       34157.56               292761.0           4996598                            7015.0             5003402                              7027.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1        55.7        0           0.1                  0.1

### Execution phase: component benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      434.48     1.86          0.12                 0.13

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
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
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_2.log &
```

yields something like

doc_ycsb_redis_2.log
```markdown
﻿## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 338s 
    Code: 1768489920
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker21.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Redis-64-8-196608-1 uses docker image redis:7.4.2
    RAM:608117153792
    CPU:AMD EPYC 7542 32-Core Processor
    Cores:64
    host:6.8.0-90-generic
    node:cl-worker21
    disk:132569
    datadisk:1
    cpu_list:0-63
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540579340288
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker22
        disk:193246
        datadisk:95
        cpu_list:0-127
    worker 1
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:132896
        datadisk:108
        cpu_list:0-95
    worker 2
        RAM:540590825472
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker25
        disk:154935
        datadisk:94
        cpu_list:0-95
    worker 3
        node:cl-worker24
    eval_parameters
        code:1768489920
        BEXHOMA_WORKERS:3

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   18102.824041                 6905.0              125000                              94.625

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)  [READ-FAILED].Operations  [READ-FAILED].99thPercentileLatency(us)
Redis-64-8-196608-1               1      128   65536          1           0                       64106.26               155991.0           4197044                            4211.0             4995899                              4247.0                    807057                                   4391.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component worker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1        3.23        0          0.11                 0.12

### Loading phase: component loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1           0        0           0.0                  0.0

### Execution phase: component worker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      280.55     2.57           0.6                 0.61

### Execution phase: component benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1       537.9      4.6          0.29                 0.29

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST failed: Execution Phase: contains FAILED column
```

## Replication

We can set the number of replicas with the parameter `-nwr`.
Note that Redis requires a worker per replicated shard, so `-nw 3` and `-nwr 1` creates 6 worker nodes, 3 for sharding and another 3 for the (single) replicas.

```bash
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

doc_ycsb_redis_3.log
```markdown
﻿## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 414s 
    Code: 1769094442
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Redis-64-8-196608-1 uses docker image redis:7.4.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:94800
    datadisk:1
    cpu_list:0-63
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:384581
        datadisk:717
        cpu_list:0-127
    worker 1
        RAM:540492902400
        CPU:Intel(R) Xeon(R) Gold 6430
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker38
        disk:250672
        datadisk:795
        cpu_list:0-127
    worker 2
        RAM:1081853980672
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:397176
        datadisk:716
        cpu_list:0-127
    worker 3
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:145224
        datadisk:710
        cpu_list:0-95
    worker 4
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:638453
        datadisk:721
        cpu_list:0-223
    worker 5
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:200821
        datadisk:797
        cpu_list:0-95
    worker 6
        node:cl-worker22
    eval_parameters
        code:1769094442
        BEXHOMA_REPLICAS:1
        BEXHOMA_WORKERS:3

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   36836.051418                27372.0             1000000                             3403.75

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1               1      128   65536          1           0                       60827.99               164398.0           5007774                            1383.0             4992226                              1352.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component worker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1       96.15     3.15          2.65                 2.69

### Loading phase: component loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1           0        0           0.0                  0.0

### Execution phase: component worker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      425.05     3.29          3.78                 3.79

### Execution phase: component benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      693.18     4.81           0.3                  0.3

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
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

```bash
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-redis-ycsb-1           | redis           | ycsb-1       | True         |                50 | Redis           | shared               | 50Gi      | Bound    | 50G    | 0      |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

doc_ycsb_redis_4.log
```markdown
﻿## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1242s 
    Code: 1769092236
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Redis-64-8-196608-1-1 uses docker image redis:7.4.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:94799
    datadisk:1095
    volume_size:50G
    volume_used:1.1G
    cpu_list:0-63
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1769092236
Redis-64-8-196608-2-1 uses docker image redis:7.4.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:94800
    datadisk:1095
    volume_size:50G
    volume_used:1.1G
    cpu_list:0-63
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1769092236

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   11028.635421                90904.0             1000000                              9029.0

### Execution
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1-1               1      128   65536          1           0                       23618.66               423394.0           4999900                           10335.0             5000100                             10335.0
Redis-64-8-196608-2-1               2      128   65536          1           0                       24868.69               402112.0           5000937                            9775.0             4999063                              9767.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1], [1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1], [1]]

### Monitoring

### Loading phase: component loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      111.56     1.44           0.1                  0.1

### Execution phase: component benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      480.61     1.31          0.13                 0.13
Redis-64-8-196608-2-1      480.61     1.30          0.13                 0.13

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```

### Redis as a Cluster

Similarly we can make a Redis cluster to store the database in persistent storage.
Here, we remove existing storage via `-rsr` to start with a clean copy.

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
  -rst shared -rss 50Gi -rsr \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_5.log &
```

Redis expects fully qualified domain name (FQDN) for each pod.
At the same time, the length of hostnames is limited.
Therefore bexhoma will shorten the name of the pods and pvcs in this case.
The first volume is attached to the (dummy) coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.


```bash
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-redis-ycsb-1           | redis           | ycsb-1       | True         |                48 | Redis           | shared               | 50Gi      | Bound    | 0      | 0      |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+

+-------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| Volumes of Workers      | configuration     |   experiment | dbms   | storage_class_name   | storage   | status   | size   | used   |
+=========================+===================+==============+========+======================+===========+==========+========+========+
| bxw-bx-w-redis-ycsb-1-0 | Redis-64-8-196608 |   1742468798 | Redis  | shared               | 50Gi      | Bound    | 50G    | 708M   |
+-------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bxw-bx-w-redis-ycsb-1-1 | Redis-64-8-196608 |   1742468798 | Redis  | shared               | 50Gi      | Bound    | 50G    | 800M   |
+-------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bxw-bx-w-redis-ycsb-1-2 | Redis-64-8-196608 |   1742468798 | Redis  | shared               | 50Gi      | Bound    | 50G    | 708M   |
+-------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

doc_ycsb_redis_5.log
```markdown
﻿## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1588s 
    Code: 1759259968
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker34.
    Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Redis-64-8-196608-1-1 uses docker image redis:7.4.2
    RAM:1081649909760
    CPU:AMD EPYC 7453 28-Core Processor
    Cores:56
    host:6.8.0-60-generic
    node:cl-worker34
    disk:316315280
    datadisk:1
    cpu_list:0-55
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-83-generic
        node:cl-worker24
        disk:142237604
        datadisk:727
        volume_size:50G
        volume_used:724M
        cpu_list:0-95
        args:['--maxclients', '10000', '--io-threads', '64']
    worker 1
        RAM:2164173299712
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:1359248500
        datadisk:825
        volume_size:50G
        volume_used:824M
        cpu_list:0-223
        args:['--maxclients', '10000', '--io-threads', '64']
    worker 2
        RAM:540579414016
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-79-generic
        node:cl-worker22
        disk:430149676
        datadisk:735
        volume_size:50G
        volume_used:732M
        cpu_list:0-127
        args:['--maxclients', '10000', '--io-threads', '64']
    eval_parameters
        code:1759259968
        BEXHOMA_WORKERS:3
Redis-64-8-196608-2-1 uses docker image redis:7.4.2
    RAM:1081649909760
    CPU:AMD EPYC 7453 28-Core Processor
    Cores:56
    host:6.8.0-60-generic
    node:cl-worker34
    disk:316317264
    datadisk:1
    cpu_list:0-55
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:540590940160
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-83-generic
        node:cl-worker23
        disk:1395842396
        datadisk:710
        volume_size:50G
        volume_used:708M
        cpu_list:0-95
        args:['--maxclients', '10000', '--io-threads', '64']
    worker 1
        RAM:2164173299712
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:1359237688
        datadisk:1004
        volume_size:50G
        volume_used:1000M
        cpu_list:0-223
        args:['--maxclients', '10000', '--io-threads', '64']
    worker 2
        RAM:540579414016
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-79-generic
        node:cl-worker22
        disk:430150084
        datadisk:935
        volume_size:50G
        volume_used:932M
        cpu_list:0-127
        args:['--maxclients', '10000', '--io-threads', '64']
    eval_parameters
        code:1759259968
        BEXHOMA_WORKERS:3

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   51265.358004                19767.0             1000000                             2816.75

### Execution
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1-1               1      128   65536          1           0                       63247.91               158108.0           5000840                            4467.0             4999160                              4443.0
Redis-64-8-196608-2-1               2      128   65536          1           0                       63128.12               158408.0           4999843                            6843.0             5000157                              6839.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1], [1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1], [1]]

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1       12.51     0.66          1.76                 1.77

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1           0        0           0.0                  0.0

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1      267.47     2.21          2.09                 2.10
Redis-64-8-196608-2-1      286.82     2.41          2.24                 2.99

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1-1     1161.67     8.57          0.29                 0.29
Redis-64-8-196608-2-1     1217.73     8.84          0.29                 0.29

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```



## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
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



