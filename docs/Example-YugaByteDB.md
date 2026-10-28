# Example: Benchmark YugabyteDB

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that is not managed by bexhoma, but exists in the Kubernetes cluster in the same namespace**.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Important implications of this:
* Bexhoma does neither start nor stop the DBMS.
* There can only be one DBMS in the cluster at the same time.
* Bexhoma does not know what resides inside of the database.
* Bexhoma still can monitor all components of the experiment, including the DBMS itself.

In order to be fully functional, bexhoma installs an instance of PostgreSQL, that does nothing (a container with psql would be enough).
Bexhoma writes infos about the status of the experiment to this "SUT" pod to mimick it has access to the DBMS.
Moreover the container is used to install a schema to YugabyteDB via psql.

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the YugabyteDB cluster.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. YugabyteDB YCSB: https://docs.yugabyte.com/preview/benchmark/ycsb-jdbc/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. Benchbase Repository: https://github.com/cmu-db/benchbase/wiki/TPC-C
1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Install YugabyteDB

Get the helm chart and follow the instructions: https://docs.yugabyte.com/stable/deploy/kubernetes/single-zone/oss/helm-chart/

This will deploy master and tserver worker.
The master pods manage table metadata and keep track of which nodes store which data.
They handle automatic sharding and tablet distribution and manage Raft-based leader election for tablets (shards).
The number of master pods is 3 or 5 typically.
The tserver worker store the actual data (tablets) and execute SQL queries via the YSQL or YCQL API.
The number of tserver depends on the size of the data and the cluster.

```bash
helm install bexhoma yugabytedb/yugabyte \
--version 2025.2.1 \
--set \
gflags.tserver.ysql_enable_packed_row=true,\
resource.master.limits.cpu=2,\
resource.master.limits.memory=8Gi,\
resource.master.requests.cpu=2,\
resource.master.requests.memory=8Gi,\
resource.tserver.limits.cpu=8,\
resource.tserver.limits.memory=8Gi,\
resource.tserver.requests.cpu=8,\
resource.tserver.requests.memory=8Gi,\
storage.master.size=100Gi,\
storage.tserver.size=100Gi,\
storage.ephemeral=true,\
tserver.tolerations[0].effect=NoSchedule,\
tserver.tolerations[0].key=nvidia.com/gpu,\
tserver.ysql_max_connections=1280,\
replicas.master=3,\
replicas.tserver=3,\
enableLoadBalancer=True
```

Optionally pin master and tserver pods to nodes with a values file (`-f nodes.yaml`) holding a node affinity for `master` and `tserver` (`kubernetes.io/hostname In [...]`).
The test script does this with `Install-YugabyteDB -Nodes $BEXHOMA_NODES_WORKER`: without persistent storage the data sits on the nodes' local disks, so the nodes decide the results.


Test the installation
```bash
helm status bexhoma
```


After the experiment: Remove the installation
```bash
helm delete bexhoma
kubectl delete pvc -l app=yb-tserver
kubectl delete pvc -l app=yb-master
```

Optionally: Connect to the installation
* to DBMS: `kubectl port-forward service/yb-tserver-service 5433:5433`
* to GUI: `kubectl port-forward service/yb-master-ui 8080:7000`


Optionally: Use [YugabyteDB connection manager](https://docs.yugabyte.com/preview/explore/going-beyond-sql/connection-mgr-ysql/) by adding
```bash
gflags.tserver.enable_ysql_conn_mgr=true,\
gflags.tserver.allowed_preview_flags_csv=enable_ysql_conn_mgr,\
```

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
  -dbms YugabyteDB \
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
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_yugabytedb_1.log
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of a dummy container as a placeholder for YugabyteDB (`-dbms`)
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
+-----------------------+--------------+--------------+------------+---------------+
| 1730133803            | sut          |   loaded [s] | use case   | benchmarker   |
+=======================+==============+==============+============+===============+
| YugabyteDB-64-8-65536 | (1. Running) |           41 | ycsb       | (1. Running)  |
+-----------------------+--------------+--------------+------------+---------------+
```

The code `1730133803` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1730133803` (removes everything that is related to experiment `1730133803`).

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_1_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb_1.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 977s 
* Code: 1793220712
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:471704
  * datadisk:39
  * volume_size:1.8T
  * volume_used:461G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:565818
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:471901
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:514850
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:471704
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:514850
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:565818
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793220712

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793220712-7868bddc49-cpbd4: 0
* yb-tserver-0: 0
* yb-tserver-1: 0
* yb-tserver-2: 0
* yb-master-0: 0
* yb-master-1: 0
* yb-master-2: 0

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| yugabytedb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2483.81 |                50326.00 |            125000.00 |                             24639.00 | 1.00 |               71.53 |
| yugabytedb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2498.20 |                50036.00 |            125000.00 |                             24879.00 | 1.00 |               71.95 |
| yugabytedb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2484.45 |                50313.00 |            125000.00 |                             25103.00 | 1.00 |               71.55 |
| yugabytedb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2436.22 |                51309.00 |            125000.00 |                             24559.00 | 1.00 |               70.16 |
| yugabytedb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2470.11 |                50605.00 |            125000.00 |                             24527.00 | 1.00 |               71.14 |
| yugabytedb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2456.09 |                50894.00 |            125000.00 |                             24815.00 | 1.00 |               70.74 |
| yugabytedb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2515.70 |                49688.00 |            125000.00 |                             24495.00 | 1.00 |               72.45 |
| yugabytedb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2465.34 |                50703.00 |            125000.00 |                             25103.00 | 1.00 |               71.00 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               70.16 |                        19809.91 |                51309.00 |           1000000.00 |                             24765.00 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 | YugabyteDB-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        21596.36 |               463041.00 |            5000970 |                           36863.00 |              4999030 |                             43711.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        21596.36 |               463041.00 |            5000970 |                           36863.00 |              4999030 |                             43711.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1637.60 |     35.04 |           6.41 |                 12.76 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |         9.06 |      0.07 |           0.21 |                  0.24 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       113.48 |      2.12 |           0.11 |                  0.11 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     17606.45 |     40.85 |          10.68 |                 22.07 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        21.62 |      0.09 |           0.22 |                  0.25 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       663.77 |      1.62 |           0.55 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-master contains no 0 or NaN in CPU [CPUs]
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


## Perform YCSB Benchmark - Execution only

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
bexhoma ycsb \
  -dbms YugabyteDB \
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
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -sl \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_yugabytedb_2.log
```

This skips loading (`-sl`), as data is already present in the database.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_2_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb_2.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 753s 
* Code: 1793221755
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is skipped.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:366065
  * datadisk:39
  * volume_size:1.8T
  * volume_used:358G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:566872
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:366066
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:515962
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:366068
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:515962
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:566873
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1793221755

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793221755-5cb5b4c9b9-w8dwl: 0
* yb-tserver-0: 0
* yb-tserver-1: 0
* yb-tserver-2: 0
* yb-master-0: 0
* yb-master-1: 0
* yb-master-2: 0

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 | YugabyteDB-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        21636.03 |               462192.00 |            4997743 |                           39167.00 |              5002257 |                             44927.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        21636.03 |               462192.00 |            4997743 |                           39167.00 |              5002257 |                             44927.00 |

### Monitoring

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     17507.64 |     41.35 |          12.78 |                 23.73 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        22.50 |      0.12 |           0.23 |                  0.26 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       631.54 |      1.72 |           0.54 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the YugabyteDB cluster.

The `-mc` option is mandatory here: The sidecar container approach is not working (since bexhoma does not manage the deployment), so either you have Prometheus / Node exporter already installed in your cluster or a daemonset is needed.
For further explanation see the monitoring section of this documentation.


## Use Persistent Storage

### Bexhoma Status Volume

Persistent Storage is not managed by bexhoma, but by YugabyteDB.
We can add the request for a PVC to the experiment setup.
Make sure to reset the database before this test as it should not contain data from previous test runs.
```bash
bexhoma ycsb \
  -dbms YugabyteDB \
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
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_yugabytedb_3.log
```
This will add a PVC to the Dummy DBMS.
Nothing will be stored there, but it maintains status information about previous loading processes.

```bash
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                 | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+=========================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-yugabytedb-ycsb-1       | yugabytedb      | ycsb-1       | True         |               300 | YugabyteDB | shared               | 1Gi       | Bound    | 1.0G   | 36M    |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

The above means there has been a YCSB loading process (managed by bexhoma) of size SF=1, that has been completed.
All following calls of such an experiment will skip loading, since the PVC tells it has been finished.
This thus helps to spare the `-sl` parameter.

However bexhoma cannot verify such information.
If YugabyteDB is restarted or data is delete somehow, this PVC information will be outdated and wrong.

This approach helps bexhoma to persist status information, but it does not persist data inside YugabyteDB.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_3_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb_3.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1008s 
* Code: 1793222758
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:364932
  * datadisk:39
  * volume_size:49G
  * volume_used:39M
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:565880
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:364932
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:514983
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:565880
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:364933
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:514983
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793222758

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793222758-66f7f88688-6mlbz: 0
* yb-tserver-0: 0
* yb-tserver-1: 0
* yb-tserver-2: 0
* yb-master-0: 0
* yb-master-1: 0
* yb-master-2: 0

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| yugabytedb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2523.67 |                49531.00 |            125000.00 |                             11695.00 | 1.00 |               72.68 |
| yugabytedb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2473.09 |                50544.00 |            125000.00 |                             11943.00 | 1.00 |               71.23 |
| yugabytedb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2508.48 |                49831.00 |            125000.00 |                             12087.00 | 1.00 |               72.24 |
| yugabytedb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2535.45 |                49301.00 |            125000.00 |                             11495.00 | 1.00 |               73.02 |
| yugabytedb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2484.79 |                50306.00 |            125000.00 |                             11591.00 | 1.00 |               71.56 |
| yugabytedb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2495.06 |                50099.00 |            125000.00 |                             11975.00 | 1.00 |               71.86 |
| yugabytedb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2529.60 |                49415.00 |            125000.00 |                             11687.00 | 1.00 |               72.85 |
| yugabytedb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2483.21 |                50338.00 |            125000.00 |                             11575.00 | 1.00 |               71.52 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               71.23 |                        20033.35 |                50544.00 |           1000000.00 |                             11756.00 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 | YugabyteDB-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        19213.48 |               520468.00 |            4998575 |                           44767.00 |              5001425 |                             52831.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        19213.48 |               520468.00 |            4998575 |                           44767.00 |              5001425 |                             52831.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1602.66 |     30.16 |           5.98 |                 13.56 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |         6.34 |      0.06 |           0.22 |                  0.25 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        63.21 |      1.38 |           0.11 |                  0.11 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     18221.45 |     38.08 |          10.49 |                 21.99 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        21.22 |      0.12 |           0.24 |                  0.27 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       666.94 |      1.50 |           0.54 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

### Persist YugabyteDB

If you want YugabyteDB to have real persistent storage, remove the line `storage.ephemeral=true,\` from the installation.


## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'YugabyteDB': {
    'loadData': 'psql -U yugabyte --host yb-tserver-service.{namespace}.svc.cluster.local --port 5433 < {scriptname}',
    'template': {
        'version': '2.17.1',
        'alias': 'Cloud-Native-1',
        'docker_alias': 'CN1',
         'JDBC': {
            'driver': "com.yugabyte.Driver",
            'auth': ["yugabyte", ""],
            'url': 'jdbc:yugabytedb://yb-tserver-service.{namespace}.svc.cluster.local:5433/yugabyte?load-balance=true',
            'jar': 'jdbc-yugabytedb-42.3.5-yb-2.jar'
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
},
```

where
* `loadData`: This command is used to create the schema
* `JDBC`: These infos are used to configure YCSB


### Preparation of YCSB

In the Docker files for YCSB
* https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ycsb/generator/Dockerfile
* https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ycsb/benchmarker/Dockerfile

there is a section about including the needed JDBC driver:
```bash
######### Specific version of YugabyteDB JDBC #########
RUN wget https://github.com/yugabyte/pgjdbc/releases/download/v42.3.5-yb-2/jdbc-yugabytedb-42.3.5-yb-2.jar
RUN cp jdbc-yugabytedb-42.3.5-yb-2.jar jars/jdbc-yugabytedb-42.3.5-yb-2.jar
```


### Dummy SUT

Bexhoma deploys a pod to carry status informations.
Here it is an instance of PostgreSQL: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-YugabyteDB.yml


### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/YugabyteDB


### Workflow of YCSB

In `ycsb.py` there is a section about YugabyteDB.

Watch for
* `config.sut_service_name`: Fixed name for the service of the SUT (="yb-tserver-service")
* `config.sut_container_name`: Fixed name for the container of the SUT (="")
* `config.get_worker_pods()`: Method to find the pods of worker nodes (['yb-tserver-0', 'yb-tserver-1', 'yb-tserver-2']). This allows getting host infos like CPU, RAM, node name, ...
* `config.create_monitoring()`: Method to create names for monitored components (for SUT = "yb-tserver-"). This avoids the SUT dummy contributing to the monitoring.
* `config.get_worker_endpoints()`: This is neccessary, when we have sidecar containers attached to workers of a distributed dbms. Monitoring needs to find these containers.
* `config.set_metric_of_config()`: Method to create promql queries from templates (pod like "yb-tserver", no container name, for our SUT)









## Benchbase's TPC-C

TPC-C is performed at 16 warehouses. The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.

```bash
bexhoma benchbase \
  -dbms YugabyteDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_yugabytedb_1.log
```

yields

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_yugabytedb_1_summary.md" target="_blank" rel="noopener">docs_benchbase_yugabytedb_1.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1508s 
* Code: 1793224024
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:365487
  * datadisk:39
  * volume_size:1.8T
  * volume_used:357G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:566387
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:515401
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:365496
    * cpu_list:0-223
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:566387
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:365496
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:515401
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793224024
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:366439
  * datadisk:39
  * volume_size:1.8T
  * volume_used:358G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:574911
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:516425
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:366439
    * cpu_list:0-223
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:577645
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:366439
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:516425
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793224024

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793224024-775cbd68ff-jrdt7: 0
* yb-tserver-0: 0
* yb-tserver-1: 0
* yb-tserver-2: 0
* yb-master-0: 0
* yb-master-1: 0
* yb-master-2: 0

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| YugabyteDB-1-1 |                1 |   16 |      465.00 |         305.00 |            0.00 |        158.00 |            2.00 |              1 |           1 |             | None           |             0 | False         |              123.87 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         349.66 |                      348.13 |         0.00 |                                                     117844.00 |                                              45730.00 |
| yugabytedb-1-1-2-1-1 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         130.52 |                      129.92 |         0.00 |                                                     170552.00 |                                              61260.00 |
| yugabytedb-1-1-2-1-2 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         127.09 |                      126.54 |         0.00 |                                                     174289.00 |                                              62902.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         349.66 |                      348.13 |         0.00 |                                                     117844.00 |                                              45730.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         257.61 |                      256.46 |         0.00 |                                                     174289.00 |                                              62081.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      2907.94 |     27.77 |           8.36 |                 16.46 |
| yugabytedb-1-1-2-1 |      2907.94 |     27.77 |           8.36 |                 16.46 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        19.83 |      0.08 |           0.23 |                  0.25 |
| yugabytedb-1-1-2-1 |        19.83 |      0.08 |           0.23 |                  0.25 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1105.52 |     12.82 |           0.26 |                  0.26 |
| yugabytedb-1-1-2-1 |      1105.52 |     12.82 |           0.26 |                  0.26 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     10394.97 |     39.23 |          10.74 |                 20.22 |
| yugabytedb-1-1-2-1 |      9896.87 |     37.19 |          11.31 |                 21.78 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        11.86 |      0.09 |           0.24 |                  0.27 |
| yugabytedb-1-1-2-1 |        16.69 |      0.09 |           0.25 |                  0.28 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       288.16 |      1.34 |           0.32 |                  0.32 |
| yugabytedb-1-1-2-1 |       273.10 |      1.05 |           0.27 |                  0.27 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

### Benchbase Example Explained

The setup is the same as for YCSB (see above).

However the connection string this time is not read from `cluster.config`, but instead constructed from parameters that are set explicitly in the workflow file `benchbase.py`:

```bash
BENCHBASE_PROFILE = 'postgres',
BEXHOMA_DATABASE = 'yugabyte',
BEXHOMA_USER = "yugabyte",
BEXHOMA_PASSWORD = "",
BEXHOMA_PORT = 5433,
```

### More Complex Example 

We now run Benchbase's TPC-C variant with more data, for a longer period of time and with a varying number of pods for execution.
Make sure to reset the database before this test as it should not contain data from previous test runs.


```bash
bexhoma benchbase \
  -dbms YugabyteDB \
  -sf 128 \
  -xsd 20 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -xkey \
  -xli 30 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_yugabytedb_2.log
```

yields

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_yugabytedb_2_summary.md" target="_blank" rel="noopener">docs_benchbase_yugabytedb_2.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 8154s 
* Code: 1793225792
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking has keying and thinking times activated. Benchmarking runs for 20 minutes.
  * Status is logged every 30ms.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1280] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:378586
  * datadisk:39
  * volume_size:1.8T
  * volume_used:370G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:607142
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:378458
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:528508
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:378270
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:528315
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:606890
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793225792
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:372781
  * datadisk:39
  * volume_size:1.8T
  * volume_used:365G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:601459
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:372781
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:522693
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:372782
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:522697
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:601459
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793225792
* yugabytedb-1-1-3-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:373026
  * datadisk:39
  * volume_size:1.8T
  * volume_used:365G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:497563
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:373026
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:522866
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:373026
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:522866
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:497563
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793225792
* yugabytedb-1-1-4-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:427066
  * datadisk:39
  * volume_size:1.8T
  * volume_used:418G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:500459
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:426869
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:523102
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:426869
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:523102
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:500459
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793225792

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793225792-76d8b7867f-6k2kq: 0
* yb-tserver-0: 0
* yb-tserver-1: 0
* yb-tserver-2: 0
* yb-master-0: 0
* yb-master-1: 0
* yb-master-2: 0

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 4: benchbase (10 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 4: benchbase (10 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| YugabyteDB-1-1 |                1 |  128 |     2374.00 |         304.00 |            0.00 |       2067.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              194.10 | False               |

### Benchmarking

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1  | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 1200.00 |            0 |                          58.13 |                       57.88 |        94.94 |                                                     185516.00 |                                            1062245.00 |
| yugabytedb-1-1-2-1-1  | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 1200.00 |            0 |                          29.83 |                       29.70 |        48.72 |                                                     137472.00 |                                             560839.00 |
| yugabytedb-1-1-2-1-2  | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 1200.00 |            0 |                          29.72 |                       29.60 |        48.55 |                                                     135969.00 |                                             609022.00 |
| yugabytedb-1-1-3-1-1  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |         256 |     3276 |        3 |               1 |       1 |          -1 | 1200.00 |            0 |                          11.39 |                       11.33 |        18.59 |                                                    1884007.00 |                                            1395181.00 |
| yugabytedb-1-1-3-1-2  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |         256 |     3276 |        3 |               1 |       2 |          -1 | 1200.00 |            1 |                          11.57 |                       11.52 |        18.89 |                                                    1527155.00 |                                            1288270.00 |
| yugabytedb-1-1-3-1-3  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |         256 |     3276 |        3 |               1 |       3 |          -1 | 1200.00 |            0 |                          11.53 |                       11.47 |        18.82 |                                                    1605499.00 |                                            1391541.00 |
| yugabytedb-1-1-3-1-4  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |         256 |     3276 |        3 |               1 |       4 |          -1 | 1200.00 |            0 |                          11.48 |                       11.43 |        18.74 |                                                    1619872.00 |                                            1358638.00 |
| yugabytedb-1-1-3-1-5  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |         256 |     3276 |        3 |               1 |       5 |          -1 | 1200.00 |            1 |                          11.41 |                       11.35 |        18.62 |                                                    1585992.00 |                                            1381496.00 |
| yugabytedb-1-1-4-1-1  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       1 |          -1 | 1200.00 |            0 |                           5.83 |                        5.80 |         9.52 |                                                     143473.00 |                                            1156846.00 |
| yugabytedb-1-1-4-1-2  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       2 |          -1 | 1200.00 |            0 |                           5.78 |                        5.75 |         9.43 |                                                     145184.00 |                                            1140761.00 |
| yugabytedb-1-1-4-1-3  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       3 |          -1 | 1200.00 |            0 |                           5.88 |                        5.84 |         9.57 |                                                     145975.00 |                                            1112021.00 |
| yugabytedb-1-1-4-1-4  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       4 |          -1 | 1200.00 |            0 |                           5.83 |                        5.81 |         9.53 |                                                     146387.00 |                                            1201594.00 |
| yugabytedb-1-1-4-1-5  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       5 |          -1 | 1200.00 |            0 |                           5.80 |                        5.78 |         9.48 |                                                     146063.00 |                                            1126176.00 |
| yugabytedb-1-1-4-1-6  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       6 |          -1 | 1200.00 |            0 |                           5.78 |                        5.76 |         9.45 |                                                     144188.00 |                                            1148348.00 |
| yugabytedb-1-1-4-1-7  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       7 |          -1 | 1200.00 |            0 |                           5.85 |                        5.82 |         9.55 |                                                     144463.00 |                                            1088968.00 |
| yugabytedb-1-1-4-1-8  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       8 |          -1 | 1200.00 |            0 |                           5.87 |                        5.84 |         9.58 |                                                     146056.00 |                                            1147027.00 |
| yugabytedb-1-1-4-1-9  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       9 |          -1 | 1200.00 |            0 |                           5.84 |                        5.82 |         9.54 |                                                     145644.00 |                                            1086011.00 |
| yugabytedb-1-1-4-1-10 | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |      10 |          -1 | 1200.00 |            0 |                           5.73 |                        5.71 |         9.36 |                                                     151583.00 |                                            1053560.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 1200.00 |            0 |                          58.13 |                       57.88 |        94.94 |                                                     185516.00 |                                            1062245.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 1200.00 |            0 |                          59.55 |                       59.30 |        97.27 |                                                     137472.00 |                                             584930.50 |
| yugabytedb-1-1-3 | yugabytedb-1-1-3 |                1 |        1280 |    16380 |               1 |           5 |          -1 | 1200.00 |            2 |                          57.38 |                       57.10 |        93.67 |                                                    1884007.00 |                                            1363025.20 |
| yugabytedb-1-1-4 | yugabytedb-1-1-4 |                1 |        1280 |    16380 |               1 |          10 |          -1 | 1200.00 |            0 |                          58.20 |                       57.93 |        95.02 |                                                     151583.00 |                                            1126131.20 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     26653.00 |     40.09 |          21.26 |                 48.02 |
| yugabytedb-1-1-2-1 |     26653.00 |     40.09 |          21.26 |                 48.02 |
| yugabytedb-1-1-3-1 |     26653.00 |     40.09 |          21.26 |                 48.02 |
| yugabytedb-1-1-4-1 |     26653.00 |     40.09 |          21.26 |                 48.02 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       110.72 |      0.14 |           0.25 |                  0.27 |
| yugabytedb-1-1-2-1 |       110.72 |      0.14 |           0.25 |                  0.27 |
| yugabytedb-1-1-3-1 |       110.72 |      0.14 |           0.25 |                  0.27 |
| yugabytedb-1-1-4-1 |       110.72 |      0.14 |           0.25 |                  0.27 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |    190409.81 |    122.95 |           0.39 |                  0.39 |
| yugabytedb-1-1-2-1 |    190409.81 |    122.95 |           0.39 |                  0.39 |
| yugabytedb-1-1-3-1 |    190409.81 |    122.95 |           0.39 |                  0.39 |
| yugabytedb-1-1-4-1 |    190409.81 |    122.95 |           0.39 |                  0.39 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     14522.96 |     19.79 |          39.18 |                 48.04 |
| yugabytedb-1-1-2-1 |     13301.04 |     20.11 |          39.93 |                 48.04 |
| yugabytedb-1-1-3-1 |     14240.26 |     22.55 |          41.05 |                 47.83 |
| yugabytedb-1-1-4-1 |     13763.11 |     22.26 |          42.28 |                 48.04 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       495.30 |      4.01 |           0.36 |                  0.39 |
| yugabytedb-1-1-2-1 |       381.72 |      3.61 |           0.36 |                  0.38 |
| yugabytedb-1-1-3-1 |       576.17 |      4.02 |           0.36 |                  0.39 |
| yugabytedb-1-1-4-1 |       502.57 |      4.01 |           0.36 |                  0.39 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       559.68 |      1.01 |           3.57 |                  3.57 |
| yugabytedb-1-1-2-1 |       632.36 |      2.65 |           2.25 |                  2.25 |
| yugabytedb-1-1-3-1 |       905.34 |      6.16 |           0.98 |                  0.98 |
| yugabytedb-1-1-4-1 |      1347.17 |     13.94 |           0.64 |                  0.64 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-3-1 (bexhoma-metrics-yugabytedb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-3-1 (bexhoma-metrics-yugabytedb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-4-1 (bexhoma-metrics-yugabytedb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-4-1 (bexhoma-metrics-yugabytedb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: efficiency contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>



