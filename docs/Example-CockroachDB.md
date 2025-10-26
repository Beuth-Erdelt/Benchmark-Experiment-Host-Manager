# Example: Benchmark CockroachDB

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

CockroachDB offers several installation methods [1].
We here rely on *CockroachDB insecure test cluster in a single Kubernetes cluster* [2].
The benefit of this approach is we can use a [manifest](https://github.com/cockroachdb/cockroach/blob/master/cloud/kubernetes/cockroachdb-statefulset.yaml) for a stateful set provided by CockroachDB.
See [dummy manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-CockroachDB.yml) for a version that is suitable for bexhoma.
CockroachDB cluster does not require a coordinator.
Bexhoma still deploys a main pod (called master) as a substitute for a single point of contact and to annotate status of experiments.
Bexhoma also deploys a service for communication external to CockroachDB (from within the cluster) and a headless service for communication between the pods of the CockroachDB cluster.

This can be managed by bexhoma.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Install CockroachDB:  https://www.cockroachlabs.com/docs/v24.2/install-cockroachdb-linux.html
1. Deploy CockroachDB in a Single Kubernetes Cluster (Insecure): https://www.cockroachlabs.com/docs/v24.2/deploy-cockroachdb-with-kubernetes-insecure
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. Benchbase Repository: https://github.com/cmu-db/benchbase/wiki/TPC-C
1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
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
  -nw 3 \
  -nwr 3 \
  --workload a \
  -dbms CockroachDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_1.log &
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of CockroachDB (`-dbms`) with 3 workers (`-nw`) and replication factor 3 (`-nwr`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=10, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [4]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 10.000.000 operations (`-sfo`)
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
+----------------------+--------------+--------------+----------------+-------------------------------+-------------+
| 1734624013           | sut          |   loaded [s] | use case       | worker                        | loading     |
+======================+==============+==============+================+===============================+=============+
| CockroachDB-1-1-1024 | (1. Running) |            2 | benchbase_tpcc | (Running) (Running) (Running) | (1 Running) |
+----------------------+--------------+--------------+----------------+-------------------------------+-------------+
```

The code `1730133803` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1730133803` (removes everything that is related to experiment `1730133803`).

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_ycsb_cockroachdb_1.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1654s 
    Code: 1761499187
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.13.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-64-8-65536-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419630632
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:687468360
        datadisk:291819
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1398730724
        datadisk:291763
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081742749696
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1295311960
        datadisk:291609
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
        code:1761499187
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                   18922.668893                53082.0             1000000                              6504.0

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1               1       64   65536          1           0                       11767.02               849833.0           5000649                            6431.0             4999351                            188799.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1     1444.92    22.43          7.04                11.05

### Ingestion - Loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1       53.08        0           0.1                 0.11

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1    20622.69     27.4          9.87                22.82

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      662.24     0.83          0.14                 0.14

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```

To see the summary again you can simply call `bexperiments summary -e 1730133803` with the experiment code.

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
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the CockroachDB cluster.


## Use Persistent Storage


The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 1 \
  -nw 3 \
  -nwr 3 \
  --workload a \
  -dbms CockroachDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi -rsr \
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_2.log &
```
The following status shows we have one volume of type `shared`.
Every Citus experiment will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of CockroachDB mounts the volume and generates the data.
All other instances just use the database without generating and loading data.
Bexhoma uses two types of volumes.
The first volume is attached to the (dummy) coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.
Here, we remove existing storage via `-rsr` to start with a clean copy.


```bash
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-cockroachdb-ycsb-1     | cockroachdb     | ycsb-1       | True         |              1589 | CockroachDB     | shared               | 50Gi      | Bound    | 50G    | 0      |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+

+-----------------------------------------+------------------------+--------------+-------------+----------------------+-----------+----------+--------+--------+
| Volumes of Workers                      | configuration          |   experiment | dbms        | storage_class_name   | storage   | status   | size   | used   |
+=========================================+========================+==============+=============+======================+===========+==========+========+========+
| bxw-bexhoma-worker-cockroachdb-ycsb-1-0 | CockroachDB-64-8-65536 |   1742540515 | CockroachDB | shared               | 50Gi      | Bound    | 50G    | 4.8G   |
+-----------------------------------------+------------------------+--------------+-------------+----------------------+-----------+----------+--------+--------+
| bxw-bexhoma-worker-cockroachdb-ycsb-1-1 | CockroachDB-64-8-65536 |   1742540515 | CockroachDB | shared               | 50Gi      | Bound    | 50G    | 4.7G   |
+-----------------------------------------+------------------------+--------------+-------------+----------------------+-----------+----------+--------+--------+
| bxw-bexhoma-worker-cockroachdb-ycsb-1-2 | CockroachDB-64-8-65536 |   1742540515 | CockroachDB | shared               | 50Gi      | Bound    | 50G    | 4.8G   |
+-----------------------------------------+------------------------+--------------+-------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

doc_ycsb_cockroachdb_2.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 6239s 
    Code: 1761500892
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.13.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
CockroachDB-64-8-65536-1-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419630648
    volume_size:50G
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:683951892
        datadisk:291251
        volume_size:50G
        volume_used:1.9G
        cpu_list:0-223
    worker 1
        RAM:1077382864896
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1300616500
        datadisk:291130
        volume_size:50G
        volume_used:1.8G
        cpu_list:0-255
    worker 2
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1396255824
        datadisk:291191
        volume_size:50G
        volume_used:1.9G
        cpu_list:0-255
    eval_parameters
        code:1761500892
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3
CockroachDB-64-8-65536-2-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419630812
    volume_size:50G
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:683123672
        datadisk:291383
        volume_size:50G
        volume_used:2.0G
        cpu_list:0-223
    worker 1
        RAM:1081742749696
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1293991496
        datadisk:291388
        volume_size:50G
        volume_used:2.0G
        cpu_list:0-127
    worker 2
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1396255468
        datadisk:291391
        volume_size:50G
        volume_used:2.0G
        cpu_list:0-255
    worker 3
    eval_parameters
        code:1761500892
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                     707.336765              1414642.0             1000000                            515647.0

### Execution
                            experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1-1               1       64   65536          1           0                         614.47              1627421.0            499980                          132095.0              500020                           4067327.0
CockroachDB-64-8-65536-2-1               2       64   65536          1           0                         578.41              1728882.0            499828                          175615.0              500172                           4476927.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1], [1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1], [1]]

### Ingestion - SUT
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1     1808.31      1.6          5.38                10.53

### Ingestion - Loader
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1      144.12     0.45          0.11                 0.11

### Execution - SUT
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1     2806.63     2.56          6.76                13.31
CockroachDB-64-8-65536-2-1     2974.89     2.27          6.73                12.03

### Execution - Benchmarker
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1       96.55     0.09          0.13                 0.13
CockroachDB-64-8-65536-2-1       94.77     0.07          0.13                 0.13

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```



## Application Metrics

Collecting application metrics for CockroachDB is supported.
It can be activated by `-m -mc -ma`.
See [example configuration](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config) for some example definitions.

```bash
#### YCSB PVC (Example-CockroachDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  -sfo 10 \
  -nw 3 \
  -nwr 3 \
  --workload a \
  -dbms CockroachDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_3.log &
```


The result looks something like

doc_ycsb_cockroachdb_3.log
```markdown
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 2124s 
    Code: 1761508062
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 10000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.13.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-64-8-65536-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419630984
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:695109224
        datadisk:301018
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1408015004
        datadisk:300803
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081742749696
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1306532096
        datadisk:300803
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
        code:1761508062
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                   16651.995671               603056.0            10000000                             11528.0

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1               1       64   65536          1           0                       14580.62               685842.0           5003330                            5367.0             4996670                            121855.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1    17320.53    32.31         21.78                63.43

### Ingestion - Loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      800.19     1.68          0.11                 0.11

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1    19701.58    31.52         24.59                67.46

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      624.12     1.03          0.13                 0.13

### Application Metrics
                          Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-64-8-65536-1                                    7579.66                   7579802.36                                    0.0                                      0.0                              0.0

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```


## YCSB Example Explained

### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'CockroachDB': {
    'loadData': 'cockroach sql --host {service_name} --port 9091 --insecure --file {scriptname}',
    'delay_prepare': 120,
    'template': {
        'version': 'v24.2.4',
        'alias': 'Cloud-Native-2',
        'docker_alias': 'CN2',
         'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["root", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/defaultdb?reWriteBatchedInserts=true',
            'jar': 'postgresql-42.5.0.jar'
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/cockroach/cockroach-data',
    'priceperhourdollar': 0.0,
},
```

where
* `loadData`: This command is used to create the schema
* `JDBC`: These infos are used to configure YCSB


CockroachDB uses the PostgreSQL JDBC driver.



### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/CockroachDB









## Benchbase's TPC-C

### Simple Run

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
CockroachDB has 3 workers.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_1.log &
```

### Evaluate Results

doc_benchbase_cockroachdb_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1738s 
    Code: 1761513559
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.13.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419631332
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:686363260
        datadisk:291855
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1398625636
        datadisk:291643
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081742749696
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1296981624
        datadisk:291642
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1761513559
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419631332
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:686684676
        datadisk:292167
        cpu_list:0-223
    worker 1
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1398949972
        datadisk:291958
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081742749696
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1296474056
        datadisk:291954
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1761513559
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    536.796649                 534.346649         0.0                                                      78757.0                                              29798.0
CockroachDB-1-1-1024-2-1               1          8    8192       2      1  300.0           0                    217.356608                 216.339941         0.0                                                      92102.0                                              36794.0
CockroachDB-1-1-1024-2-2               1          8    8192       2      2  300.0           0                    226.129926                 225.143259         0.0                                                      92370.0                                              35366.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         16   16384          1  300.0           0                        536.80                     534.35         0.0                                                      78757.0                                              29798.0
CockroachDB-1-1-1024-2               1         16   16384          2  300.0           0                        443.49                     441.48         0.0                                                      92370.0                                              36080.0

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1      222.0        1.0   1.0         259.459459
CockroachDB-1-1-1024-2      222.0        1.0   2.0         259.459459

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### Benchbase More Complex

TPC-C is performed at 128 warehouses.
The 1280 threads of the client are split into a cascading sequence of 1,2,4 and 8 pods.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 10 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2,4,8 \
  -nbt 1280 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_2.log &
```

### Evaluate Results

doc_benchbase_cockroachdb_2.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
    Type: benchbase
    Duration: 5365s 
    Code: 1761543081
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
    Experiment uses bexhoma version 0.8.13.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419632744
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:694759624
        datadisk:299185
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1077382864896
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1308736380
        datadisk:299001
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1406011580
        datadisk:299044
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1761543081
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419632744
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:696440736
        datadisk:300836
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1077382864896
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1310408924
        datadisk:300628
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1407690380
        datadisk:300678
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1761543081
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-3 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419632744
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:697838784
        datadisk:302205
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1077382864896
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1311811332
        datadisk:301992
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1409114872
        datadisk:302063
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1761543081
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-4 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419632920
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:699105424
        datadisk:303435
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1077382864896
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1313020660
        datadisk:303170
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1410344916
        datadisk:303259
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1761543081
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1       1280   16384       1      1  600.0           0                   1432.703255                1428.411588         0.0                                                    1775140.0                                             892418.0
CockroachDB-1-1-1024-2-2               1        640    8192       2      1  600.0           0                    717.863309                 715.451643         0.0                                                    1913956.0                                             890480.0
CockroachDB-1-1-1024-2-1               1        640    8192       2      2  600.0           0                    713.881646                 711.469979         0.0                                                    1914985.0                                             895883.0
CockroachDB-1-1-1024-3-2               1        320    4096       3      1  600.0           0                    337.819954                 336.813288         0.0                                                    2283853.0                                             946931.0
CockroachDB-1-1-1024-3-3               1        320    4096       3      2  600.0           0                    334.403200                 333.319868         0.0                                                    2288041.0                                             955740.0
CockroachDB-1-1-1024-3-4               1        320    4096       3      3  600.0           0                    338.944984                 337.886650         0.0                                                    2282524.0                                             942731.0
CockroachDB-1-1-1024-3-1               1        320    4096       3      4  600.0           0                    335.593298                 334.449965         0.0                                                    2286207.0                                             952483.0
CockroachDB-1-1-1024-4-2               1        160    2048       4      1  600.0           0                    160.829923                 160.239923         0.0                                                    2925607.0                                             993405.0
CockroachDB-1-1-1024-4-8               1        160    2048       4      2  600.0           0                    161.834998                 161.278331         0.0                                                    2923214.0                                             987243.0
CockroachDB-1-1-1024-4-4               1        160    2048       4      3  600.0           0                    162.909983                 162.359983         0.0                                                    2905980.0                                             980673.0
CockroachDB-1-1-1024-4-1               1        160    2048       4      4  600.0           0                    165.728323                 165.174990         0.0                                                    2900518.0                                             965157.0
CockroachDB-1-1-1024-4-6               1        160    2048       4      5  600.0           0                    160.074875                 159.493209         0.0                                                    2922925.0                                             998353.0
CockroachDB-1-1-1024-4-7               1        160    2048       4      6  600.0           0                    164.719952                 164.193286         0.0                                                    2900662.0                                             971004.0
CockroachDB-1-1-1024-4-5               1        160    2048       4      7  600.0           0                    162.396576                 161.819910         0.0                                                    2923841.0                                             983669.0
CockroachDB-1-1-1024-4-3               1        160    2048       4      8  600.0           0                    161.879924                 161.324924         0.0                                                    2927074.0                                             986864.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1       1280   16384          1  600.0           0                       1432.70                    1428.41         0.0                                                    1775140.0                                            892418.00
CockroachDB-1-1-1024-2               1       1280   16384          2  600.0           0                       1431.74                    1426.92         0.0                                                    1914985.0                                            893181.50
CockroachDB-1-1-1024-3               1       1280   16384          4  600.0           0                       1346.76                    1342.47         0.0                                                    2288041.0                                            949471.25
CockroachDB-1-1-1024-4               1       1280   16384          8  600.0           0                       1300.37                    1295.88         0.0                                                    2927074.0                                            983296.00

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 4, 8]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1     1158.0        1.0   1.0         397.927461
CockroachDB-1-1-1024-2     1158.0        1.0   2.0         397.927461
CockroachDB-1-1-1024-3     1158.0        1.0   4.0         397.927461
CockroachDB-1-1-1024-4     1158.0        1.0   8.0         397.927461

### Ingestion - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    30544.16     40.3         18.85                44.19
CockroachDB-1-1-1024-2    30544.16     40.3         18.85                44.19
CockroachDB-1-1-1024-3    30544.16     40.3         18.85                44.19
CockroachDB-1-1-1024-4    30544.16     40.3         18.85                44.19

### Ingestion - Loader
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    15057.12     34.7          0.29                 0.29
CockroachDB-1-1-1024-2    15057.12     34.7          0.29                 0.29
CockroachDB-1-1-1024-3    15057.12     34.7          0.29                 0.29
CockroachDB-1-1-1024-4    15057.12     34.7          0.29                 0.29

### Execution - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    26472.49    46.03         35.41                65.95
CockroachDB-1-1-1024-2    27113.06    46.67         35.46                69.83
CockroachDB-1-1-1024-3    26200.08    45.78         35.81                72.38
CockroachDB-1-1-1024-4    26028.11    45.83         34.33                74.03

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1     1037.52     1.89          4.19                 4.19
CockroachDB-1-1-1024-2     1159.99     2.33          2.45                 2.45
CockroachDB-1-1-1024-3     1217.95     2.17          1.46                 1.46
CockroachDB-1-1-1024-4     1383.85     4.24          1.20                 1.20

### Application Metrics
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                    9907.34                   9169393.48                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-2                                   10686.37                   9739568.18                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-3                                   10537.88                   8174572.83                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-4                                   10868.00                   8544721.11                                    0.0                                      0.0                              0.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


### Benchbase With PVC

TPC-C is performed at 128 warehouses.
The 1280 threads of the client are split into a cascading sequence of 1,2,4 and 8 pods.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 10 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2,4,8 \
  -nbt 1280 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc -ma \
  -rst shared -rss 100Gi -rsr \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_3.log &
```

### Evaluate Results

doc_benchbase_cockroachdb_2.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
    Type: benchbase
    Duration: 5365s 
    Code: 1761543081
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
    Experiment uses bexhoma version 0.8.13.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419632744
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:694759624
        datadisk:299185
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1077382864896
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1308736380
        datadisk:299001
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1406011580
        datadisk:299044
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1761543081
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419632744
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:696440736
        datadisk:300836
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1077382864896
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1310408924
        datadisk:300628
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1407690380
        datadisk:300678
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1761543081
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-3 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419632744
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:697838784
        datadisk:302205
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1077382864896
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1311811332
        datadisk:301992
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1409114872
        datadisk:302063
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1761543081
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-4 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:419632920
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:2164173279232
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:699105424
        datadisk:303435
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1077382864896
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1313020660
        datadisk:303170
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081965486080
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1410344916
        datadisk:303259
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1761543081
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1       1280   16384       1      1  600.0           0                   1432.703255                1428.411588         0.0                                                    1775140.0                                             892418.0
CockroachDB-1-1-1024-2-2               1        640    8192       2      1  600.0           0                    717.863309                 715.451643         0.0                                                    1913956.0                                             890480.0
CockroachDB-1-1-1024-2-1               1        640    8192       2      2  600.0           0                    713.881646                 711.469979         0.0                                                    1914985.0                                             895883.0
CockroachDB-1-1-1024-3-2               1        320    4096       3      1  600.0           0                    337.819954                 336.813288         0.0                                                    2283853.0                                             946931.0
CockroachDB-1-1-1024-3-3               1        320    4096       3      2  600.0           0                    334.403200                 333.319868         0.0                                                    2288041.0                                             955740.0
CockroachDB-1-1-1024-3-4               1        320    4096       3      3  600.0           0                    338.944984                 337.886650         0.0                                                    2282524.0                                             942731.0
CockroachDB-1-1-1024-3-1               1        320    4096       3      4  600.0           0                    335.593298                 334.449965         0.0                                                    2286207.0                                             952483.0
CockroachDB-1-1-1024-4-2               1        160    2048       4      1  600.0           0                    160.829923                 160.239923         0.0                                                    2925607.0                                             993405.0
CockroachDB-1-1-1024-4-8               1        160    2048       4      2  600.0           0                    161.834998                 161.278331         0.0                                                    2923214.0                                             987243.0
CockroachDB-1-1-1024-4-4               1        160    2048       4      3  600.0           0                    162.909983                 162.359983         0.0                                                    2905980.0                                             980673.0
CockroachDB-1-1-1024-4-1               1        160    2048       4      4  600.0           0                    165.728323                 165.174990         0.0                                                    2900518.0                                             965157.0
CockroachDB-1-1-1024-4-6               1        160    2048       4      5  600.0           0                    160.074875                 159.493209         0.0                                                    2922925.0                                             998353.0
CockroachDB-1-1-1024-4-7               1        160    2048       4      6  600.0           0                    164.719952                 164.193286         0.0                                                    2900662.0                                             971004.0
CockroachDB-1-1-1024-4-5               1        160    2048       4      7  600.0           0                    162.396576                 161.819910         0.0                                                    2923841.0                                             983669.0
CockroachDB-1-1-1024-4-3               1        160    2048       4      8  600.0           0                    161.879924                 161.324924         0.0                                                    2927074.0                                             986864.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1       1280   16384          1  600.0           0                       1432.70                    1428.41         0.0                                                    1775140.0                                            892418.00
CockroachDB-1-1-1024-2               1       1280   16384          2  600.0           0                       1431.74                    1426.92         0.0                                                    1914985.0                                            893181.50
CockroachDB-1-1-1024-3               1       1280   16384          4  600.0           0                       1346.76                    1342.47         0.0                                                    2288041.0                                            949471.25
CockroachDB-1-1-1024-4               1       1280   16384          8  600.0           0                       1300.37                    1295.88         0.0                                                    2927074.0                                            983296.00

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 4, 8]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1     1158.0        1.0   1.0         397.927461
CockroachDB-1-1-1024-2     1158.0        1.0   2.0         397.927461
CockroachDB-1-1-1024-3     1158.0        1.0   4.0         397.927461
CockroachDB-1-1-1024-4     1158.0        1.0   8.0         397.927461

### Ingestion - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    30544.16     40.3         18.85                44.19
CockroachDB-1-1-1024-2    30544.16     40.3         18.85                44.19
CockroachDB-1-1-1024-3    30544.16     40.3         18.85                44.19
CockroachDB-1-1-1024-4    30544.16     40.3         18.85                44.19

### Ingestion - Loader
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    15057.12     34.7          0.29                 0.29
CockroachDB-1-1-1024-2    15057.12     34.7          0.29                 0.29
CockroachDB-1-1-1024-3    15057.12     34.7          0.29                 0.29
CockroachDB-1-1-1024-4    15057.12     34.7          0.29                 0.29

### Execution - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    26472.49    46.03         35.41                65.95
CockroachDB-1-1-1024-2    27113.06    46.67         35.46                69.83
CockroachDB-1-1-1024-3    26200.08    45.78         35.81                72.38
CockroachDB-1-1-1024-4    26028.11    45.83         34.33                74.03

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1     1037.52     1.89          4.19                 4.19
CockroachDB-1-1-1024-2     1159.99     2.33          2.45                 2.45
CockroachDB-1-1-1024-3     1217.95     2.17          1.46                 1.46
CockroachDB-1-1-1024-4     1383.85     4.24          1.20                 1.20

### Application Metrics
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                    9907.34                   9169393.48                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-2                                   10686.37                   9739568.18                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-3                                   10537.88                   8174572.83                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-4                                   10868.00                   8544721.11                                    0.0                                      0.0                              0.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```




### Benchbase Example Explained

The setup is the same as for YCSB (see above).

