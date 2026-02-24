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
    Duration: 1241s 
    Code: 1770916869
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
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-64-8-65536-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96794
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:899847
        datadisk:291814
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1351593
        datadisk:291607
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:466892
        datadisk:291609
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 3
        node:cl-worker22
    eval_parameters
        code:1770916869
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                   15744.474954                63680.0             1000000                              8276.0

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1               1       64   65536          1           0                       11570.86               864240.0           4999832                            6867.0             5000168                            134527.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component worker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1     1401.18    19.31          3.98                 7.89

### Loading phase: component loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1        6.03        0           0.1                 0.11

### Execution phase: component worker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1     19911.9    26.51         10.72                26.83

### Execution phase: component benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      590.23     0.74          0.13                 0.13

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
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
    Duration: 4097s 
    Code: 1770918190
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
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
CockroachDB-64-8-65536-1-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96794
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:896582
        datadisk:291248
        volume_size:50G
        volume_used:1.9G
        cpu_list:0-223
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:464627
        datadisk:291189
        volume_size:50G
        volume_used:1.9G
        cpu_list:0-127
    worker 2
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1349336
        datadisk:291129
        volume_size:50G
        volume_used:1.8G
        cpu_list:0-255
    eval_parameters
        code:1770918190
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3
CockroachDB-64-8-65536-2-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96794
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1349336
        datadisk:291048
        volume_size:50G
        volume_used:1.7G
        cpu_list:0-255
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:464628
        datadisk:291049
        volume_size:50G
        volume_used:1.7G
        cpu_list:0-127
    worker 2
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:896583
        datadisk:291052
        volume_size:50G
        volume_used:1.7G
        cpu_list:0-223
    worker 3
        node:cl-worker22
    eval_parameters
        code:1770918190
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                     736.037075              1361805.0             1000000                            510559.0

### Execution
                            experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-2-1               2       64   65536          1           0                         638.85              1565324.0            499948                          187775.0              500052                           4444159.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1], [1]]

### Monitoring

### Loading phase: component worker
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1    21699.49     2.03          10.3                23.39

### Loading phase: component loader
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1      158.04     0.27          0.11                 0.11

### Execution phase: component worker
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1      813.03     2.36          6.09                11.81
CockroachDB-64-8-65536-2-1     3127.46     2.52          6.60                12.33

### Execution phase: component benchmarker
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1       50.59     0.28          0.13                 0.13
CockroachDB-64-8-65536-2-1      112.39     0.08          0.13                 0.13

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST failed: Workflow not as planned
TEST passed: Execution Phase: contains no FAILED column
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
    Duration: 1585s 
    Code: 1770922331
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
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-64-8-65536-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96794
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:907492
        datadisk:301035
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081853952000
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:430500
        datadisk:300823
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1361095
        datadisk:301113
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
        code:1770922331
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                   22590.094584               443241.0            10000000                              5205.5

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1               1       64   65536          1           0                       12541.26               797368.0           5000662                            6147.0             4999338                            136447.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component worker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1     12861.7    34.12          21.3                55.54

### Loading phase: component loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      748.18     2.13          0.11                 0.11

### Execution phase: component worker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1    18441.31    26.95         26.69                 65.4

### Execution phase: component benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      593.62     0.88          0.13                 0.13

### Application Metrics

#### Loading phase: component worker
                          Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-64-8-65536-1                                   71343.93                  68740810.71                                    0.0                                      0.0                              0.0

#### Execution phase: component worker
                          Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-64-8-65536-1                                   17213.11                  31282799.76                                    0.0                                      0.0                              0.0

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
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
    Duration: 1117s 
    Code: 1770923951
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96794
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:898268
        datadisk:291861
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:466964
        datadisk:291679
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:415112
        datadisk:291982
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1770923951
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96794
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:898463
        datadisk:292053
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:467124
        datadisk:291839
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:415110
        datadisk:291979
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1770923951
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    312.983331                 311.596665         0.0                                                     103278.0                                              51107.0
CockroachDB-1-1-1024-2-2               1          8    8192       2      1  300.0           0                    127.093312                 126.606646         0.0                                                     132056.0                                              62933.0
CockroachDB-1-1-1024-2-1               1          8    8192       2      2  300.0           0                    121.826654                 121.349987         0.0                                                     132987.0                                              65652.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         16   16384          1  300.0           0                        312.98                     311.60         0.0                                                     103278.0                                              51107.0
CockroachDB-1-1-1024-2               1         16   16384          2  300.0           0                        248.92                     247.96         0.0                                                     132987.0                                              64292.5

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1      168.0        1.0   1.0         342.857143
CockroachDB-1-1-1024-2      168.0        1.0   2.0         342.857143

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
    Duration: 4088s 
    Code: 1771227370
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97600
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1330763
        datadisk:299649
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 1
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:439291
        datadisk:299619
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:485534
        datadisk:299829
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1771227370
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97600
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1332248
        datadisk:300317
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 1
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:432595
        datadisk:300488
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:485967
        datadisk:300263
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1771227370
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-3 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97600
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1333257
        datadisk:301299
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 1
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:423112
        datadisk:301290
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:486926
        datadisk:301222
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1771227370
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-4 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97600
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1334179
        datadisk:302205
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 1
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:423392
        datadisk:302158
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:487816
        datadisk:302112
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1771227370
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1       1280   16384       1      1  600.0           0                    930.599991                 928.549991         0.0                                                    3314278.0                                            1372964.0
CockroachDB-1-1-1024-2-2               1        640    8192       2      1  600.0           0                    465.838266                 464.688266         0.0                                                    3338702.0                                            1370831.0
CockroachDB-1-1-1024-2-1               1        640    8192       2      2  600.0           0                    466.716657                 465.586657         0.0                                                    3334870.0                                            1368036.0
CockroachDB-1-1-1024-3-4               1        320    4096       3      1  600.0           0                    236.209963                 235.576630         0.0                                                    3501171.0                                            1351733.0
CockroachDB-1-1-1024-3-3               1        320    4096       3      2  600.0           0                    235.336576                 234.774910         0.0                                                    3501189.0                                            1357736.0
CockroachDB-1-1-1024-3-2               1        320    4096       3      3  600.0           0                    235.439949                 234.751616         0.0                                                    3502426.0                                            1355818.0
CockroachDB-1-1-1024-3-1               1        320    4096       3      4  600.0           0                    236.858301                 236.173301         0.0                                                    3500582.0                                            1348045.0
CockroachDB-1-1-1024-4-5               1        160    2048       4      1  600.0           0                    118.561660                 118.258326         0.0                                                    4282803.0                                            1346427.0
CockroachDB-1-1-1024-4-6               1        160    2048       4      2  600.0           0                    117.584932                 117.224932         0.0                                                    4308728.0                                            1357602.0
CockroachDB-1-1-1024-4-7               1        160    2048       4      3  600.0           0                    118.701591                 118.388258         0.0                                                    4284414.0                                            1346816.0
CockroachDB-1-1-1024-4-3               1        160    2048       4      4  600.0           0                    117.984983                 117.678316         0.0                                                    4287852.0                                            1353829.0
CockroachDB-1-1-1024-4-1               1        160    2048       4      5  600.0           0                    118.494918                 118.184919         0.0                                                    4289311.0                                            1346956.0
CockroachDB-1-1-1024-4-4               1        160    2048       4      6  600.0           0                    119.016580                 118.689914         0.0                                                    4279062.0                                            1341623.0
CockroachDB-1-1-1024-4-8               1        160    2048       4      7  600.0           0                    118.134942                 117.866609         0.0                                                    4304506.0                                            1351025.0
CockroachDB-1-1-1024-4-2               1        160    2048       4      8  600.0           0                    118.548267                 118.228267         0.0                                                    4299124.0                                            1346370.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1       1280   16384          1  600.0           0                        930.60                     928.55         0.0                                                    3314278.0                                            1372964.0
CockroachDB-1-1-1024-2               1       1280   16384          2  600.0           0                        932.55                     930.27         0.0                                                    3338702.0                                            1369433.5
CockroachDB-1-1-1024-3               1       1280   16384          4  600.0           0                        943.84                     941.28         0.0                                                    3502426.0                                            1353333.0
CockroachDB-1-1-1024-4               1       1280   16384          8  600.0           0                        947.03                     944.52         0.0                                                    4308728.0                                            1348831.0

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[2, 4, 1, 8]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1     1142.0        1.0   1.0         403.502627
CockroachDB-1-1-1024-2     1142.0        1.0   2.0         403.502627
CockroachDB-1-1-1024-3     1142.0        1.0   4.0         403.502627
CockroachDB-1-1-1024-4     1142.0        1.0   8.0         403.502627

### Monitoring

### Loading phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    13019.73    16.62         27.52                55.99
CockroachDB-1-1-1024-2    13019.73    16.62         27.52                55.99
CockroachDB-1-1-1024-3    13019.73    16.62         27.52                55.99
CockroachDB-1-1-1024-4    13019.73    16.62         27.52                55.99

### Loading phase: component loader
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    10579.49    17.02          0.29                 0.29
CockroachDB-1-1-1024-2    10579.49    17.02          0.29                 0.29
CockroachDB-1-1-1024-3    10579.49    17.02          0.29                 0.29
CockroachDB-1-1-1024-4    10579.49    17.02          0.29                 0.29

### Execution phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    23518.48    42.46         33.96                62.46
CockroachDB-1-1-1024-2    23772.09    42.21         34.53                65.76
CockroachDB-1-1-1024-3    23408.61    44.17         33.06                67.32
CockroachDB-1-1-1024-4    24196.24    43.86         34.18                71.73

### Execution phase: component benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1      754.82     1.38          4.20                 4.20
CockroachDB-1-1-1024-2      754.82     2.63          4.20                 4.20
CockroachDB-1-1-1024-3      795.47     2.98          2.36                 2.36
CockroachDB-1-1-1024-4      779.53     2.92          1.57                 1.57

### Application Metrics

#### Loading phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                    2627.87                  34410037.94                            10843992.69                                     0.37                              0.0
CockroachDB-1-1-1024-2                                    2627.87                  34410037.94                            10843992.69                                     0.37                              0.0
CockroachDB-1-1-1024-3                                    2627.87                  34410037.94                            10843992.69                                     0.37                              0.0
CockroachDB-1-1-1024-4                                    2627.87                  34410037.94                            10843992.69                                     0.37                              0.0

#### Execution phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                   31925.56                  10300069.08                             6353525.47                                      0.0                              0.0
CockroachDB-1-1-1024-2                                    9538.86                   4668670.61                                   0.00                                      0.0                              0.0
CockroachDB-1-1-1024-3                                   11638.14                   6839420.00                                   0.00                                      0.0                              0.0
CockroachDB-1-1-1024-4                                   10255.16                   6158455.68                                   0.00                                      0.0                              0.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
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
    Duration: 4088s 
    Code: 1771227370
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97600
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1330763
        datadisk:299649
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 1
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:439291
        datadisk:299619
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:485534
        datadisk:299829
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1771227370
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97600
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1332248
        datadisk:300317
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 1
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:432595
        datadisk:300488
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:485967
        datadisk:300263
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1771227370
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-3 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97600
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1333257
        datadisk:301299
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 1
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:423112
        datadisk:301290
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:486926
        datadisk:301222
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1771227370
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-4 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97600
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1334179
        datadisk:302205
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 1
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:423392
        datadisk:302158
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:487816
        datadisk:302112
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    eval_parameters
                code:1771227370
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1       1280   16384       1      1  600.0           0                    930.599991                 928.549991         0.0                                                    3314278.0                                            1372964.0
CockroachDB-1-1-1024-2-2               1        640    8192       2      1  600.0           0                    465.838266                 464.688266         0.0                                                    3338702.0                                            1370831.0
CockroachDB-1-1-1024-2-1               1        640    8192       2      2  600.0           0                    466.716657                 465.586657         0.0                                                    3334870.0                                            1368036.0
CockroachDB-1-1-1024-3-4               1        320    4096       3      1  600.0           0                    236.209963                 235.576630         0.0                                                    3501171.0                                            1351733.0
CockroachDB-1-1-1024-3-3               1        320    4096       3      2  600.0           0                    235.336576                 234.774910         0.0                                                    3501189.0                                            1357736.0
CockroachDB-1-1-1024-3-2               1        320    4096       3      3  600.0           0                    235.439949                 234.751616         0.0                                                    3502426.0                                            1355818.0
CockroachDB-1-1-1024-3-1               1        320    4096       3      4  600.0           0                    236.858301                 236.173301         0.0                                                    3500582.0                                            1348045.0
CockroachDB-1-1-1024-4-5               1        160    2048       4      1  600.0           0                    118.561660                 118.258326         0.0                                                    4282803.0                                            1346427.0
CockroachDB-1-1-1024-4-6               1        160    2048       4      2  600.0           0                    117.584932                 117.224932         0.0                                                    4308728.0                                            1357602.0
CockroachDB-1-1-1024-4-7               1        160    2048       4      3  600.0           0                    118.701591                 118.388258         0.0                                                    4284414.0                                            1346816.0
CockroachDB-1-1-1024-4-3               1        160    2048       4      4  600.0           0                    117.984983                 117.678316         0.0                                                    4287852.0                                            1353829.0
CockroachDB-1-1-1024-4-1               1        160    2048       4      5  600.0           0                    118.494918                 118.184919         0.0                                                    4289311.0                                            1346956.0
CockroachDB-1-1-1024-4-4               1        160    2048       4      6  600.0           0                    119.016580                 118.689914         0.0                                                    4279062.0                                            1341623.0
CockroachDB-1-1-1024-4-8               1        160    2048       4      7  600.0           0                    118.134942                 117.866609         0.0                                                    4304506.0                                            1351025.0
CockroachDB-1-1-1024-4-2               1        160    2048       4      8  600.0           0                    118.548267                 118.228267         0.0                                                    4299124.0                                            1346370.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1       1280   16384          1  600.0           0                        930.60                     928.55         0.0                                                    3314278.0                                            1372964.0
CockroachDB-1-1-1024-2               1       1280   16384          2  600.0           0                        932.55                     930.27         0.0                                                    3338702.0                                            1369433.5
CockroachDB-1-1-1024-3               1       1280   16384          4  600.0           0                        943.84                     941.28         0.0                                                    3502426.0                                            1353333.0
CockroachDB-1-1-1024-4               1       1280   16384          8  600.0           0                        947.03                     944.52         0.0                                                    4308728.0                                            1348831.0

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[2, 4, 1, 8]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1     1142.0        1.0   1.0         403.502627
CockroachDB-1-1-1024-2     1142.0        1.0   2.0         403.502627
CockroachDB-1-1-1024-3     1142.0        1.0   4.0         403.502627
CockroachDB-1-1-1024-4     1142.0        1.0   8.0         403.502627

### Monitoring

### Loading phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    13019.73    16.62         27.52                55.99
CockroachDB-1-1-1024-2    13019.73    16.62         27.52                55.99
CockroachDB-1-1-1024-3    13019.73    16.62         27.52                55.99
CockroachDB-1-1-1024-4    13019.73    16.62         27.52                55.99

### Loading phase: component loader
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    10579.49    17.02          0.29                 0.29
CockroachDB-1-1-1024-2    10579.49    17.02          0.29                 0.29
CockroachDB-1-1-1024-3    10579.49    17.02          0.29                 0.29
CockroachDB-1-1-1024-4    10579.49    17.02          0.29                 0.29

### Execution phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    23518.48    42.46         33.96                62.46
CockroachDB-1-1-1024-2    23772.09    42.21         34.53                65.76
CockroachDB-1-1-1024-3    23408.61    44.17         33.06                67.32
CockroachDB-1-1-1024-4    24196.24    43.86         34.18                71.73

### Execution phase: component benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1      754.82     1.38          4.20                 4.20
CockroachDB-1-1-1024-2      754.82     2.63          4.20                 4.20
CockroachDB-1-1-1024-3      795.47     2.98          2.36                 2.36
CockroachDB-1-1-1024-4      779.53     2.92          1.57                 1.57

### Application Metrics

#### Loading phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                    2627.87                  34410037.94                            10843992.69                                     0.37                              0.0
CockroachDB-1-1-1024-2                                    2627.87                  34410037.94                            10843992.69                                     0.37                              0.0
CockroachDB-1-1-1024-3                                    2627.87                  34410037.94                            10843992.69                                     0.37                              0.0
CockroachDB-1-1-1024-4                                    2627.87                  34410037.94                            10843992.69                                     0.37                              0.0

#### Execution phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                   31925.56                  10300069.08                             6353525.47                                      0.0                              0.0
CockroachDB-1-1-1024-2                                    9538.86                   4668670.61                                   0.00                                      0.0                              0.0
CockroachDB-1-1-1024-3                                   11638.14                   6839420.00                                   0.00                                      0.0                              0.0
CockroachDB-1-1-1024-4                                   10255.16                   6158455.68                                   0.00                                      0.0                              0.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```




### Benchbase Example Explained

The setup is the same as for YCSB (see above).



