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
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cockroachdb_1.log
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

docs_ycsb_cockroachdb_1.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1689s 
* Code: 1782919894
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
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 5Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:620603
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:623660
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:639216
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1081742745600
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:809150
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782919894
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1782919894-6f7d45648d-r76vt: 0
* bexhoma-worker-cockroachdb-ycsb-1-0: 0
* bexhoma-worker-cockroachdb-ycsb-1-1: 0
* bexhoma-worker-cockroachdb-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1984.66 |                62983.00 |            125000.00 |                              9455.00 | 1.00 |               57.16 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1996.84 |                62599.00 |            125000.00 |                              9695.00 | 1.00 |               57.51 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1970.43 |                63438.00 |            125000.00 |                              9343.00 | 1.00 |               56.75 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1963.53 |                63661.00 |            125000.00 |                              9751.00 | 1.00 |               56.55 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1987.34 |                62898.00 |            125000.00 |                              9487.00 | 1.00 |               57.24 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1971.05 |                63418.00 |            125000.00 |                              9303.00 | 1.00 |               56.77 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1966.74 |                63557.00 |            125000.00 |                              9599.00 | 1.00 |               56.64 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1977.69 |                63205.00 |            125000.00 |                              9407.00 | 1.00 |               56.96 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               56.55 |                        15818.28 |                63661.00 |           1000000.00 |                              9505.00 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [READ-FAILED].Operations |   [READ-FAILED].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|---------------------------:|------------------------------------------:|-----------------------------:|--------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        15438.01 |               647752.00 |            3100807 |                            8935.00 |              3097826 |                            143231.00 |                    1901296 |                                   1942.00 |                      1900071 |                                     1903.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [READ-FAILED].Operations |   [READ-FAILED].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|---------------------------:|------------------------------------------:|-----------------------------:|--------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        15438.01 |               647752.00 |            3100807 |                            8935.00 |              3097826 |                            143231.00 |                    1901296 |                                   1942.00 |                      1900071 |                                     1903.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |      1932.64 |     30.78 |           7.67 |                 11.60 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |        99.25 |      2.29 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     16405.93 |     33.52 |          10.09 |                 21.16 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       633.94 |      1.60 |           0.13 |                  0.13 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
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
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cockroachdb_2.log
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

docs_ycsb_cockroachdb_2.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2632s 
* Code: 1782921706
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
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:641950
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:653020
    * volume_size:50G
    * volume_used:740M
    * cpu_list:0-127
  * worker 1
    * RAM:540590841856
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:189091
    * volume_size:50G
    * volume_used:808M
    * cpu_list:0-95
  * worker 2
    * RAM:1081742745600
    * node:cl-worker29
    * disk:806887
    * volume_size:50G
    * volume_used:1012M
    * cpu_list:0-127
  * eval_parameters
    * code:1782921706
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-2-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:610506
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:610563
    * volume_size:50G
    * volume_used:788M
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:653019
    * volume_size:50G
    * volume_used:792M
    * cpu_list:0-127
  * worker 2
    * RAM:1081742745600
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:807192
    * volume_size:50G
    * volume_used:768M
    * cpu_list:0-127
  * worker 3
  * eval_parameters
    * code:1782921706
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1782921706-b76d675f6-mgrbb: 0
* bexhoma-worker-cockroachdb-ycsb-1-0: 0
* bexhoma-worker-cockroachdb-ycsb-1-1: 0
* bexhoma-worker-cockroachdb-ycsb-1-2: 1

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
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           54.77 |               171291.00 |              9381.00 |                            397823.00 | 1.00 |               21.02 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           41.28 |               540333.00 |             22307.00 |                            299519.00 | 1.00 |                6.66 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           55.84 |               172054.00 |              9607.00 |                            397311.00 | 1.00 |               20.92 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           70.72 |               539436.00 |             38149.00 |                            274687.00 | 1.00 |                6.67 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           54.96 |               171495.00 |              9426.00 |                            397311.00 | 1.00 |               20.99 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           74.01 |               171865.00 |             12720.00 |                            393471.00 | 1.00 |               20.95 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           68.29 |               540656.00 |             36921.00 |                            271103.00 | 1.00 |                6.66 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           92.05 |               540842.00 |             49784.00 |                            257663.00 | 1.00 |                6.66 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |                6.66 |                          511.92 |               540842.00 |            188295.00 |                            336111.00 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [READ-FAILED].Operations |   [READ-FAILED].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|---------------------------:|------------------------------------------:|-----------------------------:|--------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |          128 |                            0.00 |                  251.00 |                  0 |                               0.00 |                    0 |                                 0.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| CockroachDB-1-2-1-1-1 | CockroachDB-1-2-1 | CockroachDB-1-2-1-1 | CockroachDB-1   |                2 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         3244.00 |               308261.00 |              72914 |                          136959.00 |                72505 |                           3612671.00 |                     426870 |                                   3537.00 |                       427711 |                                     3867.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [READ-FAILED].Operations |   [READ-FAILED].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|---------------------------:|------------------------------------------:|-----------------------------:|--------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |          128 |                            0.00 |                  251.00 |                  0 |                               0.00 |                    0 |                                 0.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| CockroachDB-1-2-1 | CockroachDB-1-2-1 |                2 |        64 |    65536 |               1 |           1 |            0 |                         3244.00 |               308261.00 |              72914 |                          136959.00 |                72505 |                           3612671.00 |                     426870 |                                   3537.00 |                       427711 |                                     3867.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       847.72 |      3.16 |           3.49 |                  6.51 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |        51.53 |      0.65 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |         0.00 |      0.38 |           2.47 |                  3.86 |
| CockroachDB-1-2-1-1 |      1833.85 |     10.51 |           3.74 |                  4.96 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| CockroachDB-1-2-1-1 |        72.71 |      0.39 |           0.13 |                  0.13 |

### Tests
* TEST failed: No SUT container restarts
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component worker contains 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST failed: Execution Phase: [OVERALL].Throughput(ops/sec) contains 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cockroachdb_3.log
```


The result looks something like

docs_ycsb_cockroachdb_3.log
```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 2683s 
* Code: 1782924411
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
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:622279
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:625127
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081742745600
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:818356
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:675745
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782924411
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1782924411-788f99949d-r84wz: 0
* bexhoma-worker-cockroachdb-ycsb-10-0: 0
* bexhoma-worker-cockroachdb-ycsb-10-1: 0
* bexhoma-worker-cockroachdb-ycsb-10-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1661.02 |               752548.00 |           1250000.00 |                             60671.00 | 10.00 |               47.84 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1662.92 |               751688.00 |           1250000.00 |                             62047.00 | 10.00 |               47.89 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1662.18 |               752026.00 |           1250000.00 |                             61759.00 | 10.00 |               47.87 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1661.37 |               752393.00 |           1250000.00 |                             62527.00 | 10.00 |               47.85 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1663.65 |               751361.00 |           1250000.00 |                             61535.00 | 10.00 |               47.91 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1660.02 |               753001.00 |           1250000.00 |                             61023.00 | 10.00 |               47.81 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1653.69 |               755887.00 |           1250000.00 |                             61759.00 | 10.00 |               47.63 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1652.01 |               756652.00 |           1250000.00 |                             61247.00 | 10.00 |               47.58 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |               47.58 |                        13276.86 |               756652.00 |          10000000.00 |                             61571.00 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         9689.47 |              1032048.00 |            5002964 |                            7467.00 |              4997036 |                            167295.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                         9689.47 |              1032048.00 |            5002964 |                            7467.00 |              4997036 |                            167295.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     24891.87 |     40.60 |          19.30 |                 47.93 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       893.66 |      1.51 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     26531.07 |     33.64 |          25.11 |                 48.00 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       747.10 |      1.19 |           0.13 |                  0.13 |

### Tests
* TEST passed: No SUT container restarts
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_cockroachdb_1.log
```

### Evaluate Results

docs_benchbase_cockroachdb_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1722s 
* Code: 1782927166
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 16Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:624398
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:623293
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081742745600
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:809190
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:665598
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782927166
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:620885
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:622847
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081742745600
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:809401
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:665729
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782927166
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1782927166-c6f69bb4b-hfdws: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-0: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-1: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-2: 0

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
| CockroachDB-1-1 |                1 |   16 |      319.00 |           9.00 |            0.00 |        119.00 |          191.00 |              1 |           1 |             | None           |             0 | False         |              180.56 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         337.51 |                      335.94 |         0.00 |                                                     129445.00 |                                              47387.00 |
| CockroachDB-1-1-2-1-1 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         136.25 |                      135.71 |         0.00 |                                                     152753.00 |                                              58694.00 |
| CockroachDB-1-1-2-1-2 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         149.54 |                      148.88 |         0.00 |                                                     143313.00 |                                              53478.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         337.51 |                      335.94 |         0.00 |                                                     129445.00 |                                              47387.00 |
| CockroachDB-1-1-2 | CockroachDB-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         285.79 |                      284.60 |         0.00 |                                                     152753.00 |                                              56086.00 |

### Tests
* TEST passed: No SUT container restarts
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_cockroachdb_2.log
```

### Evaluate Results

docs_benchbase_cockroachdb_2.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 4967s 
* Code: 1782928925
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 100Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:636581
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:636581
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081742745600
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:818834
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:661553
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782928925
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:652501
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:657612
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081742745600
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:821872
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:653235
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782928925
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:649431
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:648468
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081742745600
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:824098
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:655518
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782928925
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:658746
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:658255
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081742745600
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:825928
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:657359
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782928925
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1782928925-79cf9c4cb4-w7psg: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-128-0: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-128-1: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-128-2: 0

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
| CockroachDB-1-1 |                1 |  128 |     1349.00 |          12.00 |            0.00 |        635.00 |          702.00 |              1 |           1 |             | None           |             0 | False         |              341.59 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 600.00 |            0 |                        2873.51 |                     2862.58 |         0.00 |                                                    1068240.00 |                                             445088.00 |
| CockroachDB-1-1-2-1-1 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 600.00 |            0 |                        1387.15 |                     1381.88 |         0.00 |                                                    1242179.00 |                                             461204.00 |
| CockroachDB-1-1-2-1-2 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 600.00 |            0 |                        1390.76 |                     1385.42 |         0.00 |                                                    1240907.00 |                                             459889.00 |
| CockroachDB-1-1-3-1-1 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       1 |          -1 | 600.00 |            0 |                         656.73 |                      654.14 |         0.00 |                                                    1400411.00 |                                             487002.00 |
| CockroachDB-1-1-3-1-2 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       2 |          -1 | 600.00 |            0 |                         669.80 |                      667.27 |         0.00 |                                                    1394708.00 |                                             477399.00 |
| CockroachDB-1-1-3-1-3 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       3 |          -1 | 600.00 |            0 |                         659.40 |                      656.72 |         0.00 |                                                    1401091.00 |                                             485088.00 |
| CockroachDB-1-1-3-1-4 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       4 |          -1 | 600.00 |            0 |                         656.18 |                      653.65 |         0.00 |                                                    1400920.00 |                                             487444.00 |
| CockroachDB-1-1-4-1-1 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       1 |          -1 | 600.00 |            0 |                         319.46 |                      318.19 |         0.00 |                                                    1658931.00 |                                             500597.00 |
| CockroachDB-1-1-4-1-2 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       2 |          -1 | 600.00 |            0 |                         325.36 |                      324.11 |         0.00 |                                                    1644458.00 |                                             491259.00 |
| CockroachDB-1-1-4-1-3 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       3 |          -1 | 600.00 |            0 |                         321.34 |                      320.10 |         0.00 |                                                    1650516.00 |                                             497830.00 |
| CockroachDB-1-1-4-1-4 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       4 |          -1 | 600.00 |            0 |                         320.59 |                      319.33 |         0.00 |                                                    1651699.00 |                                             498774.00 |
| CockroachDB-1-1-4-1-5 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       5 |          -1 | 600.00 |            0 |                         321.14 |                      319.90 |         0.00 |                                                    1654020.00 |                                             497858.00 |
| CockroachDB-1-1-4-1-6 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       6 |          -1 | 600.00 |            0 |                         322.87 |                      321.58 |         0.00 |                                                    1650622.00 |                                             495084.00 |
| CockroachDB-1-1-4-1-7 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       7 |          -1 | 600.00 |            0 |                         321.10 |                      319.86 |         0.00 |                                                    1646350.00 |                                             498132.00 |
| CockroachDB-1-1-4-1-8 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       8 |          -1 | 600.00 |            0 |                         319.16 |                      317.96 |         0.00 |                                                    1651879.00 |                                             501020.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 600.00 |            0 |                        2873.51 |                     2862.58 |         0.00 |                                                    1068240.00 |                                             445088.00 |
| CockroachDB-1-1-2 | CockroachDB-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 600.00 |            0 |                        2777.91 |                     2767.31 |         0.00 |                                                    1242179.00 |                                             460546.50 |
| CockroachDB-1-1-3 | CockroachDB-1-1-3 |                1 |        1280 |    16384 |               1 |           4 |          -1 | 600.00 |            0 |                        2642.11 |                     2631.78 |         0.00 |                                                    1401091.00 |                                             484233.25 |
| CockroachDB-1-1-4 | CockroachDB-1-1-4 |                1 |        1280 |    16384 |               1 |           8 |          -1 | 600.00 |            0 |                        2571.03 |                     2561.03 |         0.00 |                                                    1658931.00 |                                             497569.25 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     16076.33 |     47.99 |          20.65 |                 45.69 |
| CockroachDB-1-1-2-1 |     16076.33 |     47.99 |          20.65 |                 45.69 |
| CockroachDB-1-1-3-1 |     16076.33 |     47.99 |          20.65 |                 45.69 |
| CockroachDB-1-1-4-1 |     16076.33 |     47.99 |          20.65 |                 45.69 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     11048.47 |     31.13 |           0.29 |                  0.29 |
| CockroachDB-1-1-2-1 |     11048.47 |     31.13 |           0.29 |                  0.29 |
| CockroachDB-1-1-3-1 |     11048.47 |     31.13 |           0.29 |                  0.29 |
| CockroachDB-1-1-4-1 |     11048.47 |     31.13 |           0.29 |                  0.29 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |    107776.85 |    191.20 |          37.39 |                 47.88 |
| CockroachDB-1-1-2-1 |    107842.25 |    192.49 |          37.69 |                 47.92 |
| CockroachDB-1-1-3-1 |    103883.40 |    191.10 |          39.70 |                 47.96 |
| CockroachDB-1-1-4-1 |    105623.90 |    192.26 |          39.43 |                 47.95 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |      2380.70 |      4.60 |           4.21 |                  4.21 |
| CockroachDB-1-1-2-1 |      2639.73 |      5.08 |           2.49 |                  2.49 |
| CockroachDB-1-1-3-1 |      2636.69 |      5.45 |           1.83 |                  1.83 |
| CockroachDB-1-1-4-1 |      2837.11 |      6.49 |           1.46 |                  1.46 |

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                     8810.39 |                   68401957.71 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-2-1 |                                     8810.39 |                   68401957.71 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-3-1 |                                     8810.39 |                   68401957.71 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-4-1 |                                     8810.39 |                   68401957.71 |                                    0.00 |                                      0.00 |                              0.00 |

#### Execution phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                   148322.31 |                   59081770.36 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-2-1 |                                   145043.90 |                   57050043.30 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-3-1 |                                   139910.80 |                   55392410.34 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-4-1 |                                   145960.09 |                   58439749.60 |                                    0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: No SUT container restarts
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
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 100Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_cockroachdb_3.log
```

### Evaluate Results

docs_benchbase_cockroachdb_3.log
```markdown
## Show Summary

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



