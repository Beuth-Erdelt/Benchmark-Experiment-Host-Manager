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
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
bexhoma ycsb \
  -dbms CockroachDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 3 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_cockroachdb_1.log
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
      * 10.000.000 operations (`-xop`)
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

## Evaluate Results

At the end of a benchmark you will see a summary like

doc_ycsb_cockroachdb_1.log
```markdown
﻿## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1848s 
* Code: 1782144628
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.9.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219926
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1339852
    * datadisk:705700
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 1
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:841133
    * datadisk:705512
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:645883
    * datadisk:705509
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 3
    * node:cl-worker24
  * eval_parameters
    * code:1782144628
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2625.06 |                47618.00 |            125000.00 |                              7099.00 | 1.00 |               75.60 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2614.63 |                47808.00 |            125000.00 |                              6895.00 | 1.00 |               75.30 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2617.75 |                47751.00 |            125000.00 |                              7155.00 | 1.00 |               75.39 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2616.21 |                47779.00 |            125000.00 |                              7107.00 | 1.00 |               75.35 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2600.92 |                48060.00 |            125000.00 |                              7151.00 | 1.00 |               74.91 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2627.32 |                47577.00 |            125000.00 |                              7247.00 | 1.00 |               75.67 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2608.79 |                47915.00 |            125000.00 |                              6731.00 | 1.00 |               75.13 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2642.99 |                47295.00 |            125000.00 |                              6523.00 | 1.00 |               76.12 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               74.91 |                        20953.65 |                48060.00 |           1000000.00 |                              6988.50 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         6805.87 |              1469319.00 |            4998355 |                            9255.00 |              5001645 |                            424703.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                         6805.87 |              1469319.00 |            4998355 |                            9255.00 |              5001645 |                            424703.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |      1174.00 |     26.76 |           4.49 |                  8.15 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |        86.02 |      2.05 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     24941.61 |     23.23 |           9.58 |                 23.28 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       765.76 |      0.80 |           0.13 |                  0.13 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
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
bexhoma ycsb \
  -dbms CockroachDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 3 \
  -xop 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_cockroachdb_2.log
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
﻿## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 3100s 
* Code: 1782146495
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.9.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219926
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1337485
    * datadisk:705151
    * volume_size:50G
    * volume_used:1.9G
    * cpu_list:0-255
  * worker 1
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:838172
    * datadisk:704969
    * volume_size:50G
    * volume_used:1.7G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:643622
    * datadisk:705029
    * volume_size:50G
    * volume_used:1.7G
    * cpu_list:0-127
  * eval_parameters
    * code:1782146495
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-2-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219926
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1337491
    * datadisk:705243
    * volume_size:50G
    * volume_used:2.0G
    * cpu_list:0-255
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:643621
    * datadisk:705242
    * volume_size:50G
    * volume_used:2.0G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:836553
    * datadisk:705245
    * volume_size:50G
    * volume_used:2.0G
    * cpu_list:0-223
  * worker 3
    * node:cl-worker24
  * eval_parameters
    * code:1782146495
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.83 |               786985.00 |            125000.00 |                            199423.00 | 1.00 |                4.57 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.66 |               787852.00 |            125000.00 |                            198015.00 | 1.00 |                4.57 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.92 |               786557.00 |            125000.00 |                            199551.00 | 1.00 |                4.58 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.93 |               786502.00 |            125000.00 |                            199167.00 | 1.00 |                4.58 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.91 |               786585.00 |            125000.00 |                            199295.00 | 1.00 |                4.58 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.81 |               787120.00 |            125000.00 |                            197631.00 | 1.00 |                4.57 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.64 |               787964.00 |            125000.00 |                            199295.00 | 1.00 |                4.57 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          158.85 |               786914.00 |            125000.00 |                            198527.00 | 1.00 |                4.57 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |                4.57 |                         1270.55 |               787964.00 |           1000000.00 |                            198863.00 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-2-1-1-1 | CockroachDB-1-2-1 | CockroachDB-1-2-1-1 | CockroachDB-1   |                2 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         1269.24 |               787875.00 |             499716 |                           94335.00 |               500284 |                           1576959.00 |
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         1319.68 |               757760.00 |             499571 |                           77887.00 |               500429 |                           1323007.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                         1319.68 |               757760.00 |             499571 |                           77887.00 |               500429 |                           1323007.00 |
| CockroachDB-1-2-1 | CockroachDB-1-2-1 |                2 |        64 |    65536 |               1 |           1 |            0 |                         1269.24 |               787875.00 |             499716 |                           94335.00 |               500284 |                           1576959.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     26330.71 |      2.92 |          10.06 |                 23.12 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       142.20 |      0.75 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |      3075.07 |      5.85 |           6.88 |                 13.17 |
| CockroachDB-1-2-1-1 |      3674.46 |      5.52 |           6.46 |                 12.35 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |        96.00 |      0.38 |           0.13 |                  0.14 |
| CockroachDB-1-2-1-1 |        95.74 |      0.16 |           0.13 |                  0.13 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```



## Application Metrics

Collecting application metrics for CockroachDB is supported.
It can be activated by `-m -mc -ma`.
See [example configuration](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config) for some example definitions.

```bash
bexhoma ycsb \
  -dbms CockroachDB \
  -sf 10 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 3 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_cockroachdb_3.log
```


The result looks something like

doc_ycsb_cockroachdb_3.log
```markdown
﻿## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 2163s 
* Code: 1782149616
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.9.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219926
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:848181
    * datadisk:714933
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:655116
    * datadisk:714724
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1348242
    * datadisk:714783
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782149616
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1626.34 |               768596.00 |           1250000.00 |                             40319.00 | 10.00 |               46.84 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1625.87 |               768820.00 |           1250000.00 |                             40319.00 | 10.00 |               46.83 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1624.98 |               769240.00 |           1250000.00 |                             40287.00 | 10.00 |               46.80 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1624.29 |               769569.00 |           1250000.00 |                             40447.00 | 10.00 |               46.78 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1626.54 |               768502.00 |           1250000.00 |                             40351.00 | 10.00 |               46.84 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1629.44 |               767137.00 |           1250000.00 |                             40383.00 | 10.00 |               46.93 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1627.87 |               767874.00 |           1250000.00 |                             40127.00 | 10.00 |               46.88 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1629.74 |               766993.00 |           1250000.00 |                             40223.00 | 10.00 |               46.94 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |               46.78 |                        13015.07 |               769569.00 |          10000000.00 |                             40307.00 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         9631.24 |              1038288.00 |            5000488 |                            9023.00 |              4999512 |                            194815.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                         9631.24 |              1038288.00 |            5000488 |                            9023.00 |              4999512 |                            194815.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     18085.56 |     31.71 |          18.88 |                 52.23 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       819.31 |      1.99 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     22819.10 |     29.86 |          25.97 |                 64.39 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       697.70 |      0.97 |           0.13 |                  0.14 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
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
bexhoma benchbase \
  -dbms CockroachDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -nw 3 \
  -nwr 3 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_1.log
```

### Evaluate Results

doc_benchbase_cockroachdb_1.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1186s 
* Code: 1782151798
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.18.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219927
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:838989
    * datadisk:705754
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:312783
    * datadisk:705551
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-55
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1338923
    * datadisk:705546
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782151798
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219927
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:839257
    * datadisk:706027
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:313045
    * datadisk:705812
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-55
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1339188
    * datadisk:705810
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782151798
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| CockroachDB-1-1 |                1 |   16 |      349.00 |           2.00 |            0.00 |        155.00 |          192.00 |              1 |           1 |             | None           |             0 | False         |              165.04 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         432.05 |                      430.22 |         0.00 |                                                      91614.00 |                                              37023.00 |
| CockroachDB-1-1-2-1-1 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         167.17 |                      166.47 |         0.00 |                                                     119261.00 |                                              47843.00 |
| CockroachDB-1-1-2-1-2 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         167.79 |                      167.06 |         0.00 |                                                     116025.00 |                                              47668.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         432.05 |                      430.22 |         0.00 |                                                      91614.00 |                                              37023.00 |
| CockroachDB-1-1-2 | CockroachDB-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         334.96 |                      333.53 |         0.00 |                                                     119261.00 |                                              47755.50 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

### Benchbase More Complex

TPC-C is performed at 128 warehouses.
The 1280 threads of the client are split into a cascading sequence of 1,2,4 and 8 pods.

```bash
bexhoma benchbase \
  -dbms CockroachDB \
  -sf 128 \
  -xsd 10 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2,4,8 \
  -nbt 1280 \
  -nw 3 \
  -nwr 3 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_2.log
```

### Evaluate Results

doc_benchbase_cockroachdb_2.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 4530s 
* Code: 1782200972
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Experiment uses bexhoma version 0.9.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 100Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219933
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:945056
    * datadisk:713090
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:653288
    * datadisk:712889
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1346530
    * datadisk:712955
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782200972
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219933
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:945907
    * datadisk:714733
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:654951
    * datadisk:714552
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1348075
    * datadisk:714586
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782200972
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219933
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:947230
    * datadisk:716042
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:656205
    * datadisk:715803
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1349387
    * datadisk:715892
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782200972
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219933
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:947853
    * datadisk:716638
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:656830
    * datadisk:716420
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1350100
    * datadisk:716527
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782200972
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 4: benchbase (8 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 4: benchbase (8 pods)

### Loading

#### Per Run

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| CockroachDB-1-1 |                1 |  128 |     1834.00 |           2.00 |            0.00 |        895.00 |          937.00 |              1 |           1 |             | None           |             0 | False         |              251.25 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 600.00 |            0 |                        1433.76 |                     1429.40 |         0.00 |                                                    2140035.00 |                                             891948.00 |
| CockroachDB-1-1-2-1-1 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 600.00 |            0 |                         681.77 |                      679.52 |         0.00 |                                                    2255359.00 |                                             937254.00 |
| CockroachDB-1-1-2-1-2 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 600.00 |            0 |                         679.37 |                      677.29 |         0.00 |                                                    2255904.00 |                                             940441.00 |
| CockroachDB-1-1-3-1-1 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       1 |          -1 | 600.00 |          135 |                         190.19 |                      189.40 |         0.00 |                                                    1838032.00 |                                             430662.00 |
| CockroachDB-1-1-3-1-2 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       2 |          -1 | 600.00 |          130 |                         192.82 |                      192.01 |         0.00 |                                                    1817723.00 |                                             420804.00 |
| CockroachDB-1-1-3-1-3 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       3 |          -1 | 600.00 |          116 |                         191.45 |                      190.66 |         0.00 |                                                    1844212.00 |                                             428645.00 |
| CockroachDB-1-1-3-1-4 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       4 |          -1 | 600.00 |          125 |                         192.21 |                      191.50 |         0.00 |                                                    1829561.00 |                                             422160.00 |
| CockroachDB-1-1-4-1-1 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       1 |          -1 | 600.00 |            0 |                         162.08 |                      161.39 |         0.00 |                                                    2953853.00 |                                             985895.00 |
| CockroachDB-1-1-4-1-2 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       2 |          -1 | 600.00 |            0 |                         163.61 |                      162.91 |         0.00 |                                                    2969501.00 |                                             977120.00 |
| CockroachDB-1-1-4-1-3 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       3 |          -1 | 600.00 |            0 |                         161.40 |                      160.65 |         0.00 |                                                    2990804.00 |                                             990396.00 |
| CockroachDB-1-1-4-1-4 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       4 |          -1 | 600.00 |            0 |                         163.49 |                      162.72 |         0.00 |                                                    2957625.00 |                                             976775.00 |
| CockroachDB-1-1-4-1-5 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       5 |          -1 | 600.00 |            0 |                         164.38 |                      163.66 |         0.00 |                                                    2953000.00 |                                             971489.00 |
| CockroachDB-1-1-4-1-6 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       6 |          -1 | 600.00 |            0 |                         164.46 |                      163.81 |         0.00 |                                                    2928477.00 |                                             971520.00 |
| CockroachDB-1-1-4-1-7 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       7 |          -1 | 600.00 |            0 |                         161.81 |                      161.13 |         0.00 |                                                    2974160.00 |                                             988162.00 |
| CockroachDB-1-1-4-1-8 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       8 |          -1 | 600.00 |            0 |                         161.48 |                      160.75 |         0.00 |                                                    2971232.00 |                                             989138.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 600.00 |            0 |                        1433.76 |                     1429.40 |         0.00 |                                                    2140035.00 |                                             891948.00 |
| CockroachDB-1-1-2 | CockroachDB-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 600.00 |            0 |                        1361.14 |                     1356.81 |         0.00 |                                                    2255904.00 |                                             938847.50 |
| CockroachDB-1-1-3 | CockroachDB-1-1-3 |                1 |        1280 |    16384 |               1 |           4 |          -1 | 600.00 |          506 |                         766.67 |                      763.57 |         0.00 |                                                    1844212.00 |                                             425567.75 |
| CockroachDB-1-1-4 | CockroachDB-1-1-4 |                1 |        1280 |    16384 |               1 |           8 |          -1 | 600.00 |            0 |                        1302.71 |                     1297.04 |         0.00 |                                                    2990804.00 |                                             981311.88 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     22636.06 |     38.32 |          17.40 |                 42.76 |
| CockroachDB-1-1-2-1 |     22636.06 |     38.32 |          17.40 |                 42.76 |
| CockroachDB-1-1-3-1 |     22636.06 |     38.32 |          17.40 |                 42.76 |
| CockroachDB-1-1-4-1 |     22636.06 |     38.32 |          17.40 |                 42.76 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     11759.89 |     31.93 |           0.29 |                  0.29 |
| CockroachDB-1-1-2-1 |     11759.89 |     31.93 |           0.29 |                  0.29 |
| CockroachDB-1-1-3-1 |     11759.89 |     31.93 |           0.29 |                  0.29 |
| CockroachDB-1-1-4-1 |     11759.89 |     31.93 |           0.29 |                  0.29 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     24959.14 |     45.01 |          26.77 |                 56.83 |
| CockroachDB-1-1-2-1 |     25592.87 |     44.51 |          31.65 |                 65.54 |
| CockroachDB-1-1-3-1 |     21441.38 |     42.99 |          31.67 |                 67.45 |
| CockroachDB-1-1-4-1 |     25938.91 |     44.74 |          37.95 |                 76.70 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |      1068.67 |      2.18 |           4.18 |                  4.18 |
| CockroachDB-1-1-2-1 |      1038.04 |      4.01 |           4.18 |                  4.18 |
| CockroachDB-1-1-3-1 |      3067.58 |      6.66 |           2.40 |                  2.40 |
| CockroachDB-1-1-4-1 |      3352.71 |      6.79 |           1.84 |                  1.84 |

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                     8568.43 |                   73447301.51 |                                    0.00 |                                      0.41 |                              0.00 |
| CockroachDB-1-1-2-1 |                                     8568.43 |                   73447301.51 |                                    0.00 |                                      0.41 |                              0.00 |
| CockroachDB-1-1-3-1 |                                     8568.43 |                   73447301.51 |                                    0.00 |                                      0.41 |                              0.00 |
| CockroachDB-1-1-4-1 |                                     8568.43 |                   73447301.51 |                                    0.00 |                                      0.41 |                              0.00 |

#### Execution phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                    35982.12 |                   32959116.01 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-2-1 |                                    12003.49 |                    7357817.68 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-3-1 |                                    42754.44 |                   19414843.58 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-4-1 |                                    44243.44 |                   27651289.76 |                                    0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```


### Benchbase With PVC

TPC-C is performed at 128 warehouses.
The 1280 threads of the client are split into a cascading sequence of 1,2,4 and 8 pods.

```bash
bexhoma benchbase \
  -dbms CockroachDB \
  -sf 128 \
  -xsd 10 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2,4,8 \
  -nbt 1280 \
  -nw 3 \
  -nwr 3 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 100Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_3.log
```

### Evaluate Results

doc_benchbase_cockroachdb_3.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 5784s 
* Code: 1782205525
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Experiment uses bexhoma version 0.9.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219934
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1336666
    * datadisk:713027
    * volume_size:100G
    * volume_used:9.6G
    * cpu_list:0-255
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:643639
    * datadisk:712956
    * volume_size:100G
    * volume_used:9.5G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:922329
    * datadisk:712955
    * volume_size:100G
    * volume_used:9.5G
    * cpu_list:0-223
  * eval_parameters
    * code:1782205525
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219934
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1336669
    * datadisk:713851
    * volume_size:100G
    * volume_used:11G
    * cpu_list:0-255
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:643642
    * datadisk:713806
    * volume_size:100G
    * volume_used:11G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:922637
    * datadisk:713793
    * volume_size:100G
    * volume_used:11G
    * cpu_list:0-223
  * eval_parameters
    * code:1782205525
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219934
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1336670
    * datadisk:714614
    * volume_size:100G
    * volume_used:12G
    * cpu_list:0-255
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:643645
    * datadisk:714538
    * volume_size:100G
    * volume_used:11G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:922828
    * datadisk:714531
    * volume_size:100G
    * volume_used:11G
    * cpu_list:0-223
  * eval_parameters
    * code:1782205525
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219934
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1337463
    * datadisk:715302
    * volume_size:100G
    * volume_used:12G
    * cpu_list:0-255
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:643648
    * datadisk:715231
    * volume_size:100G
    * volume_used:12G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:921952
    * datadisk:715222
    * volume_size:100G
    * volume_used:12G
    * cpu_list:0-223
  * eval_parameters
    * code:1782205525
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 4: benchbase (8 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 4: benchbase (8 pods)

### Loading

#### Per Run

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| CockroachDB-1-1 |                1 |  128 |     3529.00 |           6.00 |            0.00 |       1751.00 |         1772.00 |              1 |           1 |             | None           |             0 | False         |              130.58 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 600.00 |            0 |                         666.73 |                      665.74 |         0.00 |                                                    4632521.00 |                                            1914069.00 |
| CockroachDB-1-1-2-1-1 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 600.00 |            0 |                         342.03 |                      341.52 |         0.00 |                                                    4536085.00 |                                            1866192.00 |
| CockroachDB-1-1-2-1-2 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 600.00 |            0 |                         338.33 |                      337.80 |         0.00 |                                                    4543099.00 |                                            1886457.00 |
| CockroachDB-1-1-3-1-1 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       1 |          -1 | 600.00 |            0 |                         169.99 |                      169.73 |         0.00 |                                                    5161920.00 |                                            1877359.00 |
| CockroachDB-1-1-3-1-2 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       2 |          -1 | 600.00 |            0 |                         170.64 |                      170.36 |         0.00 |                                                    5159807.00 |                                            1870075.00 |
| CockroachDB-1-1-3-1-3 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       3 |          -1 | 600.00 |            0 |                         168.97 |                      168.69 |         0.00 |                                                    5164982.00 |                                            1890018.00 |
| CockroachDB-1-1-3-1-4 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       4 |          -1 | 600.00 |            0 |                         168.46 |                      168.21 |         0.00 |                                                    5175442.00 |                                            1894616.00 |
| CockroachDB-1-1-4-1-1 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       1 |          -1 | 600.00 |            0 |                          83.61 |                       83.45 |         0.00 |                                                    6505505.00 |                                            1908009.00 |
| CockroachDB-1-1-4-1-2 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       2 |          -1 | 600.00 |            0 |                          82.71 |                       82.59 |         0.00 |                                                    6501104.00 |                                            1927706.00 |
| CockroachDB-1-1-4-1-3 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       3 |          -1 | 600.00 |            0 |                          84.16 |                       84.05 |         0.00 |                                                    6474477.00 |                                            1894857.00 |
| CockroachDB-1-1-4-1-4 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       4 |          -1 | 600.00 |            0 |                          83.18 |                       83.02 |         0.00 |                                                    6493685.00 |                                            1917389.00 |
| CockroachDB-1-1-4-1-5 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       5 |          -1 | 600.00 |            0 |                          83.32 |                       83.23 |         0.00 |                                                    6470360.00 |                                            1914556.00 |
| CockroachDB-1-1-4-1-6 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       6 |          -1 | 600.00 |            0 |                          83.56 |                       83.43 |         0.00 |                                                    6501809.00 |                                            1910285.00 |
| CockroachDB-1-1-4-1-7 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       7 |          -1 | 600.00 |            0 |                          83.61 |                       83.47 |         0.00 |                                                    6481791.00 |                                            1906817.00 |
| CockroachDB-1-1-4-1-8 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       8 |          -1 | 600.00 |            0 |                          83.91 |                       83.81 |         0.00 |                                                    6498230.00 |                                            1902392.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 600.00 |            0 |                         666.73 |                      665.74 |         0.00 |                                                    4632521.00 |                                            1914069.00 |
| CockroachDB-1-1-2 | CockroachDB-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 600.00 |            0 |                         680.37 |                      679.33 |         0.00 |                                                    4543099.00 |                                            1876324.50 |
| CockroachDB-1-1-3 | CockroachDB-1-1-3 |                1 |        1280 |    16384 |               1 |           4 |          -1 | 600.00 |            0 |                         678.05 |                      677.00 |         0.00 |                                                    5175442.00 |                                            1883017.00 |
| CockroachDB-1-1-4 | CockroachDB-1-1-4 |                1 |        1280 |    16384 |               1 |           8 |          -1 | 600.00 |            0 |                         668.07 |                      667.06 |         0.00 |                                                    6505505.00 |                                            1910251.38 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     12440.96 |      9.93 |          27.08 |                 55.68 |
| CockroachDB-1-1-2-1 |     12440.96 |      9.93 |          27.08 |                 55.68 |
| CockroachDB-1-1-3-1 |     12440.96 |      9.93 |          27.08 |                 55.68 |
| CockroachDB-1-1-4-1 |     12440.96 |      9.93 |          27.08 |                 55.68 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     12229.96 |     15.97 |           0.30 |                  0.30 |
| CockroachDB-1-1-2-1 |     12229.96 |     15.97 |           0.30 |                  0.30 |
| CockroachDB-1-1-3-1 |     12229.96 |     15.97 |           0.30 |                  0.30 |
| CockroachDB-1-1-4-1 |     12229.96 |     15.97 |           0.30 |                  0.30 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     17920.50 |     32.40 |          33.37 |                 64.08 |
| CockroachDB-1-1-2-1 |     18685.48 |     32.57 |          32.95 |                 66.05 |
| CockroachDB-1-1-3-1 |     18502.78 |     32.32 |          33.27 |                 68.17 |
| CockroachDB-1-1-4-1 |     17920.07 |     31.87 |          33.00 |                 70.11 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       586.76 |      2.38 |           4.21 |                  4.21 |
| CockroachDB-1-1-2-1 |       586.76 |      2.65 |           4.21 |                  4.21 |
| CockroachDB-1-1-3-1 |       649.00 |      2.44 |           2.33 |                  2.33 |
| CockroachDB-1-1-4-1 |       646.34 |      2.77 |           1.69 |                  1.69 |

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                     2146.89 |                   25900279.35 |                                    0.00 |                                      0.36 |                              0.00 |
| CockroachDB-1-1-2-1 |                                     2146.89 |                   25900279.35 |                                    0.00 |                                      0.36 |                              0.00 |
| CockroachDB-1-1-3-1 |                                     2146.89 |                   25900279.35 |                                    0.00 |                                      0.36 |                              0.00 |
| CockroachDB-1-1-4-1 |                                     2146.89 |                   25900279.35 |                                    0.00 |                                      0.36 |                              0.00 |

#### Execution phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                    26571.47 |                    8270363.64 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-2-1 |                                     8834.16 |                    3894581.87 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-3-1 |                                     9257.59 |                    4245113.15 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-4-1 |                                     9166.61 |                    4639797.15 |                                    0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```




### Benchbase Example Explained

The setup is the same as for YCSB (see above).



