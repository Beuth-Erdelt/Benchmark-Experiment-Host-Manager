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
## Show Summary

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
## Show Summary

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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_cockroachdb_3.log
```


The result looks something like

doc_ycsb_cockroachdb_3.log
```markdown
## Show Summary

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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_1.log
```

### Evaluate Results

doc_benchbase_cockroachdb_1.log
```markdown
## Show Summary

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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_2.log
```

### Evaluate Results

doc_benchbase_cockroachdb_2.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 3874s 
* Code: 1782078658
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
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
  * disk:262619
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:318113
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-55
  * worker 1
    * RAM:540597927936
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:286128
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1346020
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782078658
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222216
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:319272
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-55
  * worker 1
    * RAM:540597927936
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:287281
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1347194
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782078658
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222216
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:320264
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-55
  * worker 1
    * RAM:540597927936
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:288268
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1348276
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782078658
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225919
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:321157
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-55
  * worker 1
    * RAM:540597927936
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:287452
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1349151
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782078658
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
| CockroachDB-1-1 |                1 |  128 |     1245.00 |           1.00 |            0.00 |        611.00 |          633.00 |              1 |           1 |             | None           |             0 | False         |              370.12 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 600.00 |            0 |                         953.54 |                      951.26 |         0.00 |                                                    3000795.00 |                                            1339422.00 |
| CockroachDB-1-1-2-1-1 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 600.00 |            0 |                         478.87 |                      477.74 |         0.00 |                                                    3251884.00 |                                            1334267.00 |
| CockroachDB-1-1-2-1-2 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 600.00 |            0 |                         476.53 |                      475.33 |         0.00 |                                                    3254242.00 |                                            1341019.00 |
| CockroachDB-1-1-3-1-1 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       1 |          -1 | 600.00 |            0 |                         230.63 |                      230.03 |         0.00 |                                                    3665721.00 |                                            1385547.00 |
| CockroachDB-1-1-3-1-2 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       2 |          -1 | 600.00 |            0 |                         231.33 |                      230.75 |         0.00 |                                                    3670476.00 |                                            1380858.00 |
| CockroachDB-1-1-3-1-3 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       3 |          -1 | 600.00 |            0 |                         230.31 |                      229.70 |         0.00 |                                                    3670632.00 |                                            1387528.00 |
| CockroachDB-1-1-3-1-4 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       4 |          -1 | 600.00 |            0 |                         230.30 |                      229.69 |         0.00 |                                                    3662109.00 |                                            1387112.00 |
| CockroachDB-1-1-4-1-1 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       1 |          -1 | 600.00 |            0 |                         108.41 |                      108.10 |         0.00 |                                                    4682197.00 |                                            1472683.00 |
| CockroachDB-1-1-4-1-2 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       2 |          -1 | 600.00 |            0 |                         109.12 |                      108.83 |         0.00 |                                                    4683410.00 |                                            1462989.00 |
| CockroachDB-1-1-4-1-3 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       3 |          -1 | 600.00 |            0 |                         107.68 |                      107.34 |         0.00 |                                                    4710264.00 |                                            1482672.00 |
| CockroachDB-1-1-4-1-4 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       4 |          -1 | 600.00 |            0 |                         107.30 |                      106.97 |         0.00 |                                                    4723466.00 |                                            1490239.00 |
| CockroachDB-1-1-4-1-5 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       5 |          -1 | 600.00 |            0 |                         107.71 |                      107.35 |         0.00 |                                                    4702505.00 |                                            1482337.00 |
| CockroachDB-1-1-4-1-6 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       6 |          -1 | 600.00 |            0 |                         109.52 |                      109.13 |         0.00 |                                                    4663940.00 |                                            1458730.00 |
| CockroachDB-1-1-4-1-7 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       7 |          -1 | 600.00 |            0 |                         107.87 |                      107.56 |         0.00 |                                                    4703306.00 |                                            1480581.00 |
| CockroachDB-1-1-4-1-8 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       8 |          -1 | 600.00 |            0 |                         109.29 |                      108.98 |         0.00 |                                                    4679845.00 |                                            1460780.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 600.00 |            0 |                         953.54 |                      951.26 |         0.00 |                                                    3000795.00 |                                            1339422.00 |
| CockroachDB-1-1-2 | CockroachDB-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 600.00 |            0 |                         955.40 |                      953.07 |         0.00 |                                                    3254242.00 |                                            1337643.00 |
| CockroachDB-1-1-3 | CockroachDB-1-1-3 |                1 |        1280 |    16384 |               1 |           4 |          -1 | 600.00 |            0 |                         922.56 |                      920.16 |         0.00 |                                                    3670632.00 |                                            1385261.25 |
| CockroachDB-1-1-4 | CockroachDB-1-1-4 |                1 |        1280 |    16384 |               1 |           8 |          -1 | 600.00 |            0 |                         866.89 |                      864.27 |         0.00 |                                                    4723466.00 |                                            1473876.38 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |      9786.97 |     22.41 |          18.33 |                 43.57 |
| CockroachDB-1-1-2-1 |      9786.97 |     22.41 |          18.33 |                 43.57 |
| CockroachDB-1-1-3-1 |      9786.97 |     22.41 |          18.33 |                 43.57 |
| CockroachDB-1-1-4-1 |      9786.97 |     22.41 |          18.33 |                 43.57 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     11964.22 |     32.14 |           0.30 |                  0.30 |
| CockroachDB-1-1-2-1 |     11964.22 |     32.14 |           0.30 |                  0.30 |
| CockroachDB-1-1-3-1 |     11964.22 |     32.14 |           0.30 |                  0.30 |
| CockroachDB-1-1-4-1 |     11964.22 |     32.14 |           0.30 |                  0.30 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     24204.62 |     44.46 |          31.72 |                 60.34 |
| CockroachDB-1-1-2-1 |     25142.41 |     43.74 |          36.32 |                 67.80 |
| CockroachDB-1-1-3-1 |     24547.46 |     44.81 |          38.53 |                 72.67 |
| CockroachDB-1-1-4-1 |     24780.91 |     44.10 |          36.65 |                 72.46 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       796.57 |      2.26 |           4.16 |                  4.16 |
| CockroachDB-1-1-2-1 |       796.57 |      4.12 |           4.16 |                  4.16 |
| CockroachDB-1-1-3-1 |       888.63 |      4.58 |           2.36 |                  2.36 |
| CockroachDB-1-1-4-1 |       855.81 |      3.21 |           1.68 |                  1.68 |

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                     7276.59 |                   65233860.04 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-2-1 |                                     7276.59 |                   65233860.04 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-3-1 |                                     7276.59 |                   65233860.04 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-4-1 |                                     7276.59 |                   65233860.04 |                                    0.00 |                                      0.00 |                              0.00 |

#### Execution phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                    26464.39 |                   17680874.87 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-2-1 |                                    14240.47 |                    8503865.09 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-3-1 |                                    16482.17 |                    9006584.53 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-4-1 |                                    19016.96 |                   10181018.74 |                                    0.00 |                                      0.00 |                              0.00 |

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
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
    Type: benchbase
    Duration: 5751s 
    Code: 1771231512
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
    Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
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
        disk:1325988
        datadisk:299115
        volume_size:100G
        volume_used:9.6G
        cpu_list:0-255
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:475050
        datadisk:299053
        volume_size:100G
        volume_used:9.5G
        cpu_list:0-127
    worker 2
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:933372
        datadisk:299050
        volume_size:100G
        volume_used:9.5G
        cpu_list:0-223
    eval_parameters
                code:1771231512
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
        disk:1325989
        datadisk:299120
        volume_size:100G
        volume_used:9.6G
        cpu_list:0-255
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:475050
        datadisk:299057
        volume_size:100G
        volume_used:9.5G
        cpu_list:0-127
    worker 2
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:933373
        datadisk:299050
        volume_size:100G
        volume_used:9.5G
        cpu_list:0-223
    eval_parameters
                code:1771231512
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
        disk:1325992
        datadisk:299592
        volume_size:100G
        volume_used:11G
        cpu_list:0-255
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:475050
        datadisk:299529
        volume_size:100G
        volume_used:9.9G
        cpu_list:0-127
    worker 2
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:933377
        datadisk:299649
        volume_size:100G
        volume_used:10G
        cpu_list:0-223
    eval_parameters
                code:1771231512
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
        disk:1326061
        datadisk:300008
        volume_size:100G
        volume_used:11G
        cpu_list:0-255
    worker 1
        RAM:1081742745600
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:475050
        datadisk:299949
        volume_size:100G
        volume_used:11G
        cpu_list:0-127
    worker 2
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:933383
        datadisk:299941
        volume_size:100G
        volume_used:11G
        cpu_list:0-223
    eval_parameters
                code:1771231512
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1          0   16384       1      1  600.0           0                      0.000000                   0.000000         0.0                                                          0.0                                                  0.0
CockroachDB-1-1-1024-2-1               1        640    8192       2      1  600.0           0                    178.791648                 178.961648         0.0                                                    9013168.0                                            3549629.0
CockroachDB-1-1-1024-2-2               1        640    8192       2      2  600.0           0                    180.449977                 180.684977         0.0                                                    8986949.0                                            3515573.0
CockroachDB-1-1-1024-3-2               1        320    4096       3      1  600.0           0                     82.661634                  82.799967         0.0                                                   11000017.0                                            3848169.0
CockroachDB-1-1-1024-3-1               1        320    4096       3      2  600.0           0                     83.284997                  83.401664         0.0                                                   11010778.0                                            3821198.0
CockroachDB-1-1-1024-3-3               1        320    4096       3      3  600.0           0                     82.379982                  82.563315         0.0                                                   11036315.0                                            3872202.0
CockroachDB-1-1-1024-3-4               1        320    4096       3      4  600.0           0                     83.546657                  83.701657         0.0                                                   10998663.0                                            3806944.0
CockroachDB-1-1-1024-4-4               1        160    2048       4      1  600.0           0                     37.314997                  37.401664         0.0                                                   14423387.0                                            4254147.0
CockroachDB-1-1-1024-4-3               1        160    2048       4      2  600.0           0                     37.616659                  37.714992         0.0                                                   14327464.0                                            4219671.0
CockroachDB-1-1-1024-4-7               1        160    2048       4      3  600.0           0                     37.791642                  37.871642         0.0                                                   14375306.0                                            4203922.0
CockroachDB-1-1-1024-4-5               1        160    2048       4      4  600.0           0                     37.656661                  37.738327         0.0                                                   14346553.0                                            4220773.0
CockroachDB-1-1-1024-4-1               1        160    2048       4      5  600.0           0                     37.764981                  37.839981         0.0                                                   14327624.0                                            4210259.0
CockroachDB-1-1-1024-4-6               1        160    2048       4      6  600.0           0                     37.328315                  37.423315         0.0                                                   14466268.0                                            4254209.0
CockroachDB-1-1-1024-4-8               1        160    2048       4      7  600.0           0                     37.494999                  37.591666         0.0                                                   14405936.0                                            4237508.0
CockroachDB-1-1-1024-4-2               1        160    2048       4      8  600.0           0                     37.598327                  37.696661         0.0                                                   14413052.0                                            4218755.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1          0   16384          1  600.0           0                          0.00                       0.00         0.0                                                          0.0                                                 0.00
CockroachDB-1-1-1024-2               1       1280   16384          2  600.0           0                        359.24                     359.65         0.0                                                    9013168.0                                           3532601.00
CockroachDB-1-1-1024-3               1       1280   16384          4  600.0           0                        331.87                     332.47         0.0                                                   11036315.0                                           3837128.25
CockroachDB-1-1-1024-4               1       1280   16384          8  600.0           0                        300.57                     301.28         0.0                                                   14466268.0                                           4227405.50

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[8, 1, 2, 4]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1     3336.0        1.0   1.0         138.129496
CockroachDB-1-1-1024-2     3336.0        1.0   2.0         138.129496
CockroachDB-1-1-1024-3     3336.0        1.0   4.0         138.129496
CockroachDB-1-1-1024-4     3336.0        1.0   8.0         138.129496

### Monitoring

### Loading phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1   112944.18    21.45         31.01                 69.3
CockroachDB-1-1-1024-2   112944.18    21.45         31.01                 69.3
CockroachDB-1-1-1024-3   112944.18    21.45         31.01                 69.3
CockroachDB-1-1-1024-4   112944.18    21.45         31.01                 69.3

### Loading phase: component loader
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1    10547.59     8.22          0.29                 0.29
CockroachDB-1-1-1024-2    10547.59     8.22          0.29                 0.29
CockroachDB-1-1-1024-3    10547.59     8.22          0.29                 0.29
CockroachDB-1-1-1024-4    10547.59     8.22          0.29                 0.29

### Execution phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1        0.00     0.47         19.80                48.31
CockroachDB-1-1-1024-2    10577.58    20.12         29.15                59.05
CockroachDB-1-1-1024-3    10282.86    18.34         29.35                59.88
CockroachDB-1-1-1024-4     9811.86    17.70         29.22                61.43

### Execution phase: component benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1        0.00     0.00          0.00                 0.00
CockroachDB-1-1-1024-2      417.54     1.16          2.22                 2.22
CockroachDB-1-1-1024-3      417.56     1.55          2.22                 2.22
CockroachDB-1-1-1024-4      430.58     1.57          1.17                 1.17

### Application Metrics

#### Loading phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                     988.77                  16446575.49                                    0.0                                     0.45                              0.0
CockroachDB-1-1-1024-2                                     988.77                  16446575.49                                    0.0                                     0.45                              0.0
CockroachDB-1-1-1024-3                                     988.77                  16446575.49                                    0.0                                     0.45                              0.0
CockroachDB-1-1-1024-4                                     988.77                  16446575.49                                    0.0                                     0.45                              0.0

#### Execution phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                       0.00                         0.00                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-2                                   17624.27                   7002074.27                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-3                                    4695.35                   2000012.73                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-4                                    4852.60                   2143701.81                                    0.0                                      0.0                              0.0

### Tests
TEST failed: Throughput (requests/second) contains 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution phase: component worker contains 0 or NaN in CPU [CPUs]
TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```




### Benchbase Example Explained

The setup is the same as for YCSB (see above).



