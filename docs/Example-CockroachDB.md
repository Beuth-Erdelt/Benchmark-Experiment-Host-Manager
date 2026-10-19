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
BEXHOMA_NODES_WORKER="cl-worker36+cl-worker37+cl-worker29"
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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
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

You can watch the status while benchmark is running via `bexhoma status`

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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cockroachdb_1_summary.md" target="_blank" rel="noopener">docs_ycsb_cockroachdb_1.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2259s 
* Code: 1792369960
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
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:576843
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:148621
    * datadisk:691686
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161858
    * datadisk:691561
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:621352
    * datadisk:691507
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792369960
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792369960-6db45bf9b-gtgf9: 0
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
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1286.47 |                97165.00 |            125000.00 |                             12479.00 | 1.00 |               37.05 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1284.59 |                97307.00 |            125000.00 |                             12383.00 | 1.00 |               37.00 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1281.72 |                97525.00 |            125000.00 |                             12551.00 | 1.00 |               36.91 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1286.47 |                97165.00 |            125000.00 |                             12575.00 | 1.00 |               37.05 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1285.80 |                97216.00 |            125000.00 |                             12159.00 | 1.00 |               37.03 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1286.70 |                97148.00 |            125000.00 |                             12471.00 | 1.00 |               37.06 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1288.43 |                97017.00 |            125000.00 |                             12255.00 | 1.00 |               37.11 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1284.15 |                97341.00 |            125000.00 |                             12159.00 | 1.00 |               36.98 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               36.91 |                        10284.33 |                97525.00 |           1000000.00 |                             12379.00 |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         5813.83 |              1720038.00 |            5001488 |                           12527.00 |              4998512 |                            140543.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                         5813.83 |              1720038.00 |            5001488 |                           12527.00 |              4998512 |                            140543.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      1879.60 |     20.72 |           8.11 |                 12.15 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |        90.59 |      1.73 |           0.10 |                  0.10 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     27869.39 |     25.77 |          13.18 |                 26.44 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       627.60 |      0.61 |           0.19 |                  0.19 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

To see the summary again you can simply call `bexhoma summary -e 1730133803` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888




## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the CockroachDB cluster.


## Use Persistent Storage


The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cockroachdb_2_summary.md" target="_blank" rel="noopener">docs_ycsb_cockroachdb_2.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1095s 
* Code: 1792372284
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
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:568076
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:883537
    * datadisk:691286
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-255
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619010
    * datadisk:691043
    * volume_size:49G
    * volume_used:1.8G
    * cpu_list:0-127
  * worker 2
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159529
    * datadisk:691090
    * volume_size:49G
    * volume_used:1.9G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792372284
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-2-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567699
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:144350
    * datadisk:691350
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-95
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:162097
    * datadisk:691348
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-127
  * worker 2
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:883540
    * datadisk:691349
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-255
  * worker 3
    * node:cl-worker37
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792372284
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: CockroachDB-1-2

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792372284-5c866f54fb-2nc26: 0
* bexhoma-worker-cockroachdb-nvme-ycsb-1-0: 0
* bexhoma-worker-cockroachdb-nvme-ycsb-1-1: 0
* bexhoma-worker-cockroachdb-nvme-ycsb-1-2: 0
* bexhoma-sut-cockroachdb-1-1792372284-7bfdf8444d-x7chc: 0

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
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1897.10 |                65890.00 |            125000.00 |                             11183.00 | 1.00 |               54.64 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1883.86 |                66353.00 |            125000.00 |                             11415.00 | 1.00 |               54.26 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1881.96 |                66420.00 |            125000.00 |                             11311.00 | 1.00 |               54.20 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1890.79 |                66110.00 |            125000.00 |                             11551.00 | 1.00 |               54.45 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1886.85 |                66248.00 |            125000.00 |                             11231.00 | 1.00 |               54.34 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1895.00 |                65963.00 |            125000.00 |                             11255.00 | 1.00 |               54.58 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1891.36 |                66090.00 |            125000.00 |                             11271.00 | 1.00 |               54.47 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1887.59 |                66222.00 |            125000.00 |                             11327.00 | 1.00 |               54.36 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               54.20 |                        15114.52 |                66420.00 |           1000000.00 |                             11318.00 |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        10945.83 |                91359.00 |             500260 |                            7183.00 |               499740 |                            177663.00 |
| cockroachdb-1-2-1-1-1 | cockroachdb-1-2-1 | cockroachdb-1-2-1-1 | CockroachDB-1   |                2 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         9512.30 |               105127.00 |             499882 |                            8191.00 |               500118 |                            220415.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        10945.83 |                91359.00 |             500260 |                            7183.00 |               499740 |                            177663.00 |
| cockroachdb-1-2-1 | cockroachdb-1-2-1 |                2 |        64 |    65536 |               1 |           1 |            0 |                         9512.30 |               105127.00 |             499882 |                            8191.00 |               500118 |                            220415.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      1923.74 |     35.74 |           7.36 |                 11.82 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |        73.24 |      1.32 |           0.10 |                  0.10 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      1962.64 |     27.78 |           8.65 |                 12.68 |
| cockroachdb-1-2-1-1 |      2060.46 |     24.84 |           5.62 |                 10.20 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |        58.56 |      0.72 |           0.20 |                  0.20 |
| cockroachdb-1-2-1-1 |        57.40 |      0.67 |           0.18 |                  0.18 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-2-1-1 (bexhoma-metrics-cockroachdb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-2-1-1 (bexhoma-metrics-cockroachdb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-2-1-1 (bexhoma-metrics-cockroachdb-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-2-1-1 (bexhoma-metrics-cockroachdb-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>



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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_ycsb_cockroachdb_3.log
```


The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cockroachdb_3_summary.md" target="_blank" rel="noopener">docs_ycsb_cockroachdb_3.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 4269s 
* Code: 1792373455
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
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567704
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:156832
    * datadisk:701772
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:171242
    * datadisk:700933
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:631582
    * datadisk:701756
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792373455
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792373455-57bb4fdff4-2m8n4: 0
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
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1203.89 |              1038303.00 |           1250000.00 |                             23615.00 | 10.00 |               34.67 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1209.11 |              1033814.00 |           1250000.00 |                             23663.00 | 10.00 |               34.82 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1205.14 |              1037221.00 |           1250000.00 |                             23743.00 | 10.00 |               34.71 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1201.90 |              1040024.00 |           1250000.00 |                             23679.00 | 10.00 |               34.61 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1204.92 |              1037411.00 |           1250000.00 |                             23679.00 | 10.00 |               34.70 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1203.78 |              1038396.00 |           1250000.00 |                             23775.00 | 10.00 |               34.67 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1203.63 |              1038524.00 |           1250000.00 |                             23599.00 | 10.00 |               34.66 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1203.14 |              1038950.00 |           1250000.00 |                             23567.00 | 10.00 |               34.65 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |               34.61 |                         9635.51 |              1040024.00 |          10000000.00 |                             23665.00 |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         3502.95 |              2854738.00 |            5000734 |                           23775.00 |              4999266 |                           1285119.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                         3502.95 |              2854738.00 |            5000734 |                           23775.00 |              4999266 |                           1285119.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     22282.05 |     27.10 |          25.28 |                 64.61 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       765.23 |      1.17 |           0.10 |                  0.10 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     31274.39 |     27.42 |          29.86 |                 70.86 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       718.87 |      0.78 |           0.20 |                  0.21 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_benchbase_cockroachdb_1.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_cockroachdb_1_summary.md" target="_blank" rel="noopener">docs_benchbase_cockroachdb_1.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1256s 
* Code: 1792377776
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.11.6.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567739
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:147386
    * datadisk:691778
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161811
    * datadisk:691638
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:887042
    * datadisk:691499
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792377776
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567741
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:147182
    * datadisk:691879
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161936
    * datadisk:691808
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:887214
    * datadisk:691670
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792377776
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792377776-8684988789-vc67q: 0
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

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |   16 |      242.00 |           3.00 |            0.00 |        237.00 |            2.00 |              1 |           1 |             | None           |             0 | False         |              238.02 | False               |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         254.60 |                      253.55 |         0.00 |                                                     125014.00 |                                              62828.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                          98.00 |                       97.62 |         0.00 |                                                     181082.00 |                                              81604.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                          98.85 |                       98.43 |         0.00 |                                                     180352.00 |                                              80911.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         254.60 |                      253.55 |         0.00 |                                                     125014.00 |                                              62828.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         196.85 |                      196.06 |         0.00 |                                                     181082.00 |                                              81257.50 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_benchbase_cockroachdb_2.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_cockroachdb_2_summary.md" target="_blank" rel="noopener">docs_benchbase_cockroachdb_2.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 3777s 
* Code: 1792379048
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 100Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567749
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:154649
    * datadisk:699026
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:628653
    * datadisk:698824
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:894378
    * datadisk:698823
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792379048
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567755
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:156933
    * datadisk:701304
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:630930
    * datadisk:701092
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:896657
    * datadisk:701095
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792379048
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567760
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:159002
    * datadisk:703362
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:632966
    * datadisk:703127
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:898696
    * datadisk:703134
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792379048
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567766
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:159334
    * datadisk:705268
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:634868
    * datadisk:705027
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:902084
    * datadisk:705034
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792379048
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792379048-7d98799b5f-p6fpj: 0
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

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |  128 |      771.00 |           2.00 |            0.00 |        766.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              597.67 | False               |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 600.00 |            0 |                        2066.67 |                     2059.25 |         0.00 |                                                    1594139.00 |                                             618631.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 600.00 |            0 |                        1161.79 |                     1157.53 |         0.00 |                                                    1400877.00 |                                             550274.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 600.00 |            0 |                        1162.87 |                     1158.68 |         0.00 |                                                    1400917.00 |                                             550112.00 |
| cockroachdb-1-1-3-1-1 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       1 |          -1 | 600.00 |            0 |                         627.33 |                      624.87 |         0.00 |                                                    1486997.00 |                                             509691.00 |
| cockroachdb-1-1-3-1-2 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       2 |          -1 | 600.00 |            0 |                         625.81 |                      623.41 |         0.00 |                                                    1488612.00 |                                             511140.00 |
| cockroachdb-1-1-3-1-3 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       3 |          -1 | 600.00 |            0 |                         627.12 |                      624.79 |         0.00 |                                                    1487846.00 |                                             509795.00 |
| cockroachdb-1-1-3-1-4 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       4 |          -1 | 600.00 |            0 |                         625.65 |                      623.26 |         0.00 |                                                    1489506.00 |                                             511339.00 |
| cockroachdb-1-1-4-1-1 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       1 |          -1 | 600.00 |            0 |                         289.67 |                      288.59 |         0.00 |                                                    1929436.00 |                                             552192.00 |
| cockroachdb-1-1-4-1-2 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       2 |          -1 | 600.00 |            0 |                         289.89 |                      288.78 |         0.00 |                                                    1935950.00 |                                             551314.00 |
| cockroachdb-1-1-4-1-3 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       3 |          -1 | 600.00 |            0 |                         289.75 |                      288.63 |         0.00 |                                                    1934908.00 |                                             551566.00 |
| cockroachdb-1-1-4-1-4 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       4 |          -1 | 600.00 |            0 |                         288.82 |                      287.84 |         0.00 |                                                    1937697.00 |                                             553620.00 |
| cockroachdb-1-1-4-1-5 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       5 |          -1 | 600.00 |            0 |                         288.69 |                      287.52 |         0.00 |                                                    1936936.00 |                                             553637.00 |
| cockroachdb-1-1-4-1-6 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       6 |          -1 | 600.00 |            0 |                         288.34 |                      287.28 |         0.00 |                                                    1938460.00 |                                             554573.00 |
| cockroachdb-1-1-4-1-7 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       7 |          -1 | 600.00 |            0 |                         287.99 |                      286.96 |         0.00 |                                                    1939468.00 |                                             555116.00 |
| cockroachdb-1-1-4-1-8 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       8 |          -1 | 600.00 |            0 |                         288.61 |                      287.48 |         0.00 |                                                    1937808.00 |                                             554107.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 600.00 |            0 |                        2066.67 |                     2059.25 |         0.00 |                                                    1594139.00 |                                             618631.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 600.00 |            0 |                        2324.66 |                     2316.22 |         0.00 |                                                    1400917.00 |                                             550193.00 |
| cockroachdb-1-1-3 | cockroachdb-1-1-3 |                1 |        1280 |    16384 |               1 |           4 |          -1 | 600.00 |            0 |                        2505.90 |                     2496.32 |         0.00 |                                                    1489506.00 |                                             510491.25 |
| cockroachdb-1-1-4 | cockroachdb-1-1-4 |                1 |        1280 |    16384 |               1 |           8 |          -1 | 600.00 |            0 |                        2311.78 |                     2303.10 |         0.00 |                                                    1939468.00 |                                             553265.62 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     17299.24 |     53.29 |          21.83 |                 47.05 |
| cockroachdb-1-1-2-1 |     17299.24 |     53.29 |          21.83 |                 47.05 |
| cockroachdb-1-1-3-1 |     17299.24 |     53.29 |          21.83 |                 47.05 |
| cockroachdb-1-1-4-1 |     17299.24 |     53.29 |          21.83 |                 47.05 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     12313.80 |     28.68 |           0.29 |                  0.29 |
| cockroachdb-1-1-2-1 |     12313.80 |     28.68 |           0.29 |                  0.29 |
| cockroachdb-1-1-3-1 |     12313.80 |     28.68 |           0.29 |                  0.29 |
| cockroachdb-1-1-4-1 |     12313.80 |     28.68 |           0.29 |                  0.29 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     90583.79 |    170.63 |          35.50 |                 67.51 |
| cockroachdb-1-1-2-1 |    101974.88 |    187.34 |          39.68 |                 80.30 |
| cockroachdb-1-1-3-1 |    110404.28 |    191.18 |          40.21 |                 84.75 |
| cockroachdb-1-1-4-1 |    107686.60 |    195.30 |          41.36 |                 88.43 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      1614.31 |      3.24 |           4.21 |                  4.21 |
| cockroachdb-1-1-2-1 |      1781.85 |      3.80 |           2.49 |                  2.49 |
| cockroachdb-1-1-3-1 |      1824.50 |      5.10 |           1.65 |                  1.65 |
| cockroachdb-1-1-4-1 |      1941.23 |      4.12 |           1.31 |                  1.31 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-4-1 (bexhoma-metrics-cockroachdb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-4-1 (bexhoma-metrics-cockroachdb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-4-1 (bexhoma-metrics-cockroachdb-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-4-1 (bexhoma-metrics-cockroachdb-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                     6087.36 |             57597316.69 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                     6087.36 |             57597316.69 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-3-1 |                                     6087.36 |             57597316.69 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-4-1 |                                     6087.36 |             57597316.69 |                              0.00 |                                      0.00 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                   112619.63 |             42919256.99 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                   128516.48 |             48907495.88 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-3-1 |                                   140223.13 |             53731765.00 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-4-1 |                                   137983.02 |             53464839.54 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>


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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_benchbase_cockroachdb_3.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_cockroachdb_3_summary.md" target="_blank" rel="noopener">docs_benchbase_cockroachdb_3.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 3840s 
* Code: 1792382877
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567789
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:884517
    * datadisk:699028
    * volume_size:98G
    * volume_used:9.6G
    * cpu_list:0-255
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159981
    * datadisk:698895
    * volume_size:98G
    * volume_used:9.5G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173172736
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:567789
    * datadisk:698822
    * volume_size:98G
    * volume_used:9.4G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792382877
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567804
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:884526
    * datadisk:702059
    * volume_size:98G
    * volume_used:13G
    * cpu_list:0-255
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159150
    * datadisk:701925
    * volume_size:98G
    * volume_used:13G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173172736
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:567804
    * datadisk:701844
    * volume_size:98G
    * volume_used:13G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792382877
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567810
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:884527
    * datadisk:704540
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-255
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159157
    * datadisk:704343
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173172736
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:567810
    * datadisk:704438
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792382877
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567815
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:884427
    * datadisk:706417
    * volume_size:98G
    * volume_used:17G
    * cpu_list:0-255
  * worker 1
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:158991
    * datadisk:706273
    * volume_size:98G
    * volume_used:17G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173172736
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:567816
    * datadisk:706223
    * volume_size:98G
    * volume_used:17G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792382877
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792382877-7b84586d58-gvk66: 0
* bexhoma-worker-cockroachdb-nvme-benchbase-tpcc-128-0: 0
* bexhoma-worker-cockroachdb-nvme-benchbase-tpcc-128-1: 0
* bexhoma-worker-cockroachdb-nvme-benchbase-tpcc-128-2: 0

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

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |  128 |      538.00 |           3.00 |            0.00 |        532.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              856.51 | False               |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 600.00 |            0 |                        2924.67 |                     2913.67 |         0.00 |                                                    1071576.00 |                                             437184.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 600.00 |            0 |                        1477.42 |                     1471.61 |         0.00 |                                                    1116605.00 |                                             432831.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 600.00 |            0 |                        1474.10 |                     1468.49 |         0.00 |                                                    1117711.00 |                                             433993.00 |
| cockroachdb-1-1-3-1-1 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       1 |          -1 | 600.00 |            0 |                         712.23 |                      709.48 |         0.00 |                                                    1302552.00 |                                             449039.00 |
| cockroachdb-1-1-3-1-2 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       2 |          -1 | 600.00 |            0 |                         714.88 |                      712.17 |         0.00 |                                                    1299773.00 |                                             447162.00 |
| cockroachdb-1-1-3-1-3 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       3 |          -1 | 600.00 |            0 |                         713.02 |                      710.12 |         0.00 |                                                    1303387.00 |                                             448606.00 |
| cockroachdb-1-1-3-1-4 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       4 |          -1 | 600.00 |            0 |                         713.75 |                      710.95 |         0.00 |                                                    1302419.00 |                                             448024.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 600.00 |            0 |                        2924.67 |                     2913.67 |         0.00 |                                                    1071576.00 |                                             437184.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 600.00 |            0 |                        2951.52 |                     2940.10 |         0.00 |                                                    1117711.00 |                                             433412.00 |
| cockroachdb-1-1-3 | cockroachdb-1-1-3 |                1 |        1280 |    16384 |               1 |           4 |          -1 | 600.00 |            0 |                        2853.88 |                     2842.72 |         0.00 |                                                    1303387.00 |                                             448207.75 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      9717.84 |     25.56 |          23.37 |                 48.77 |
| cockroachdb-1-1-2-1 |      9717.84 |     25.56 |          23.37 |                 48.77 |
| cockroachdb-1-1-3-1 |      9717.84 |     25.56 |          23.37 |                 48.77 |
| cockroachdb-1-1-4-1 |      9717.84 |     25.56 |          23.37 |                 48.77 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     11615.69 |     33.13 |           0.29 |                  0.29 |
| cockroachdb-1-1-2-1 |     11615.69 |     33.13 |           0.29 |                  0.29 |
| cockroachdb-1-1-3-1 |     11615.69 |     33.13 |           0.29 |                  0.29 |
| cockroachdb-1-1-4-1 |     11615.69 |     33.13 |           0.29 |                  0.29 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |    112473.06 |    197.26 |          37.62 |                 71.41 |
| cockroachdb-1-1-2-1 |    117164.65 |    202.64 |          38.57 |                 80.17 |
| cockroachdb-1-1-3-1 |    113425.25 |    195.83 |          40.73 |                 85.80 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      1909.07 |      4.21 |           4.21 |                  4.21 |
| cockroachdb-1-1-2-1 |      2166.99 |      4.75 |           2.49 |                  2.49 |
| cockroachdb-1-1-3-1 |      2167.88 |      4.18 |           1.67 |                  1.67 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                     9956.51 |             75843131.43 |                              0.00 |                                      0.25 |                              0.00 |
| cockroachdb-1-1-2-1 |                                     9956.51 |             75843131.43 |                              0.00 |                                      0.25 |                              0.00 |
| cockroachdb-1-1-3-1 |                                     9956.51 |             75843131.43 |                              0.00 |                                      0.25 |                              0.00 |
| cockroachdb-1-1-4-1 |                                     9956.51 |             75843131.43 |                              0.00 |                                      0.25 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                   150420.31 |             58843400.91 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                   154384.46 |             60092548.00 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-3-1 |                                   154307.69 |             60139069.37 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST failed: Benchmark round of CockroachDB-1 did not start within 15 minutes (8 pods still missing)
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>




### Benchbase Example Explained

The setup is the same as for YCSB (see above).



