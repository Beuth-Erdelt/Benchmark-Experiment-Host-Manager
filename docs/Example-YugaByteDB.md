# Example: Benchmark YugabyteDB

This example shows how to benchmark YugabyteDB with YCSB and Benchbase's TPC-C.
This differs from the default behaviour of bexhoma, since the SUT is **a distributed DBMS, that is not managed by bexhoma, but exists in the Kubernetes cluster in the same namespace**.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[YugabyteDB](https://www.yugabyte.com/) is a distributed, PostgreSQL-compatible DBMS.
It consists of master and tablet-server (tserver) components, both deployed as stateful sets by its own Helm chart.
Important implications of this:
* Bexhoma does neither start nor stop the DBMS.
* There can only be one DBMS in the cluster at the same time.
* Bexhoma does not know what resides inside of the database.
* Bexhoma still can monitor all components of the experiment, including the DBMS itself.

Bexhoma deploys a placeholder pod as the "SUT", which carries the status of the experiment and installs the schema to YugabyteDB via `psql`.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [YugabyteDB](https://www.yugabyte.com/)
1. [YugabyteDB YCSB](https://docs.yugabyte.com/preview/benchmark/ycsb-jdbc/)
1. [YugabyteDB Helm chart](https://docs.yugabyte.com/stable/deploy/kubernetes/single-zone/oss/helm-chart/)
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. [Benchbase Repository](https://github.com/cmu-db/benchbase/wiki/TPC-C)
1. [OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases](http://www.vldb.org/pvldb/vol7/p277-difallah.pdf)
1. Test script of this page: [test-docs-yugabytedb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-yugabytedb.sh), [test-docs-yugabytedb.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-yugabytedb.ps1)


## Perform YCSB Benchmark

### Prerequisites: Install YugabyteDB

Get the Helm chart and follow the [instructions](https://docs.yugabyte.com/stable/deploy/kubernetes/single-zone/oss/helm-chart/).

This will deploy master and tserver pods.
The master pods manage table metadata and keep track of which nodes store which data.
They handle automatic sharding and tablet distribution and manage Raft-based leader election for tablets (shards).
The number of master pods is 3 or 5 typically.
The tserver pods store the actual data (tablets) and execute SQL queries via the YSQL or YCQL API.
The number of tservers depends on the size of the data and the cluster.

The test script installs YugabyteDB before each experiment and removes it afterwards (`install_yugabytedb` / `remove_yugabytedb`, `Install-YugabyteDB` / `Remove-YugabyteDB`), with these values:

```bash
helm install bexhoma yugabytedb/yugabyte \
--version 2025.2.7 \
--set \
gflags.tserver.ysql_enable_packed_row=true,\
gflags.tserver.ysql_max_connections=1280,\
resource.master.limits.cpu=2,\
resource.master.limits.memory=16Gi,\
resource.master.requests.cpu=2,\
resource.master.requests.memory=16Gi,\
resource.tserver.limits.cpu=8,\
resource.tserver.limits.memory=16Gi,\
resource.tserver.requests.cpu=8,\
resource.tserver.requests.memory=16Gi,\
storage.master.size=100Gi,\
storage.master.storageClass=shared,\
storage.tserver.size=100Gi,\
storage.tserver.storageClass=shared,\
storage.tserver.count=2,\
storage.ephemeral=true,\
livenessProbe.timeoutSeconds=10,\
preflight.skipUlimit=true,\
enableLoadBalancer=true
```

The script pins master and tserver pods to the nodes `$BEXHOMA_NODES_WORKER` with a values file (`-f nodes.yaml`) holding a node affinity for `master` and `tserver` (`kubernetes.io/hostname In [...]`): without persistent storage the data sits on the nodes' local disks, so the nodes decide the results.

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

### Run the Benchmark

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

The experiment is run with the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

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
  -xop 1 \
  -ms $BEXHOMA_MS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_yugabytedb.log
```

This
* starts a placeholder pod for YugabyteDB (`-dbms`)
* creates the YCSB schema in YugabyteDB
* starts 8 loader pods (`-nlp`)
  * threads = 64/8 per pod (`-nlt`)
  * target throughput is 4 * 16384 (`-xnlf`, `-xtb`)
  * generates YCSB data = 1.000.000 rows (i.e., SF=1, `-sf`)
  * imports it into the DBMS
* runs 1 stream of YCSB queries (`-nbp`)
  * 1.000.000 operations (`-xop`)
  * workload A = 50% read / 50% update (`-xwl`)
  * target throughput is 4 * 16384 (`-xnbf`, `-xtb`)
  * threads = 64 (`-nbt`)
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
You can find the number also in the output of the benchmark script.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1730133803` (removes everything that is related to experiment `1730133803`).

### Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 366s 
* Code: 1794849409
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
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
  * disk:1326651
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:661788
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406858
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1326690
    * cpu_list:0-223
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:661981
    * cpu_list:0-127
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406858
    * cpu_list:0-127
  * yb-master 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1326690
    * cpu_list:0-223
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794849409

### Ingestion
* YugabyteDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794849409-c9b5dc795-plw68: 0
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

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| yugabytedb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2284.11 |                54726.00 |            125000.00 |                             16431.00 | 1.00 |               65.78 |
| yugabytedb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2310.96 |                54090.00 |            125000.00 |                             16623.00 | 1.00 |               66.56 |
| yugabytedb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2298.94 |                54373.00 |            125000.00 |                             16559.00 | 1.00 |               66.21 |
| yugabytedb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2323.07 |                53808.00 |            125000.00 |                             16447.00 | 1.00 |               66.90 |
| yugabytedb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2309.60 |                54122.00 |            125000.00 |                             16463.00 | 1.00 |               66.52 |
| yugabytedb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2288.41 |                54623.00 |            125000.00 |                             16543.00 | 1.00 |               65.91 |
| yugabytedb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2319.80 |                53884.00 |            125000.00 |                             16447.00 | 1.00 |               66.81 |
| yugabytedb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2303.81 |                54258.00 |            125000.00 |                             16543.00 | 1.00 |               66.35 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |               65.78 |                        18438.70 |                54726.00 |           1000000.00 |                             16507.00 |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        21067.71 |                47466.00 |             499968 |                           26783.00 |               500032 |                             39647.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        21067.71 |                47466.00 |             499968 |                           26783.00 |               500032 |                             39647.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

To see the summary again you can simply call `bexhoma summary -e 1730133803` with the experiment code.

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example the [Jupyter notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/notebooks/), in particular [Collector-YCSB.ipynb](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/notebooks/Collector-YCSB.ipynb).

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Monitoring

[Monitoring](Monitoring.md) can be activated for DBMS only (`-m`) or for all components (`-mc`).
Metrics are sampled every few seconds, so the benchmarking phase should take at least a minute.
This run uses 10.000.000 operations (`-xop`).

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 tservers of the YugabyteDB cluster.

The `-mc` option is mandatory here: the sidecar container approach does not work (since bexhoma does not manage the deployment), so either you have Prometheus / Node exporter already installed in your cluster or a daemonset is needed.
See [Monitoring](Monitoring.md) for further explanation.

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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_yugabytedb_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 814s 
* Code: 1794849968
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
  * Experiment uses bexhoma version 0.11.18.
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
  * disk:1394587
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.4T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662005
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1394578
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406838
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662149
    * cpu_list:0-127
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406838
    * cpu_list:0-127
  * yb-master 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1394372
    * cpu_list:0-223
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794849968

### Ingestion
* YugabyteDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794849968-6db864f947-7hzmj: 0
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

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| yugabytedb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2462.33 |                50765.00 |            125000.00 |                             16311.00 | 1.00 |               70.92 |
| yugabytedb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2498.50 |                50030.00 |            125000.00 |                             16343.00 | 1.00 |               71.96 |
| yugabytedb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2500.95 |                49981.00 |            125000.00 |                             16271.00 | 1.00 |               72.03 |
| yugabytedb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2498.45 |                50031.00 |            125000.00 |                             16295.00 | 1.00 |               71.96 |
| yugabytedb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2500.40 |                49992.00 |            125000.00 |                             16103.00 | 1.00 |               72.01 |
| yugabytedb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2477.46 |                50455.00 |            125000.00 |                             16359.00 | 1.00 |               71.35 |
| yugabytedb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2463.15 |                50748.00 |            125000.00 |                             16351.00 | 1.00 |               70.94 |
| yugabytedb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2457.00 |                50875.00 |            125000.00 |                             16295.00 | 1.00 |               70.76 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |               70.76 |                        19858.24 |                50875.00 |           1000000.00 |                             16291.00 |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        20063.76 |               498411.00 |            5000447 |                           46655.00 |              4999553 |                             53503.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        20063.76 |               498411.00 |            5000447 |                           46655.00 |              4999553 |                             53503.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1827.40 |     34.91 |           6.12 |                 13.42 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |         7.02 |      0.09 |           0.24 |                  0.27 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        69.72 |      1.97 |           0.11 |                  0.11 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     17277.47 |     37.84 |          11.40 |                 22.72 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        19.79 |      0.13 |           0.25 |                  0.28 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       657.91 |      1.86 |           0.55 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

### Application Metrics

Collecting application metrics for YugabyteDB is supported.
It can be activated by `-m -mc -ma`.
Prometheus discovers the master pods (port 7000) and the tserver pods (port 9000) and scrapes the native endpoint `/prometheus-metrics` of YugabyteDB, with the metric sets `yb-master` and `yb-tserver`.
See [Metrics](Example-Metrics.md) for application metrics of all DBMS.

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
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  run &>$LOG_DIR/docs_ycsb_yugabytedb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1239s 
* Code: 1794910206
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
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:554787
  * datadisk:39
  * volume_size:879G
  * volume_used:542G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:554790
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1058112
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1405842
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:555226
    * cpu_list:0-127
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1405842
    * cpu_list:0-127
  * yb-master 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1058112
    * cpu_list:0-223
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794910206

### Ingestion
* YugabyteDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794910206-bcbfb6f4f-pqw7f: 0
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

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| yugabytedb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1975.85 |                63264.00 |            125000.00 |                             15031.00 | 1.00 |               56.90 |
| yugabytedb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1966.92 |                63551.00 |            125000.00 |                             15407.00 | 1.00 |               56.65 |
| yugabytedb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1991.24 |                62775.00 |            125000.00 |                             15039.00 | 1.00 |               57.35 |
| yugabytedb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1978.13 |                63191.00 |            125000.00 |                             15415.00 | 1.00 |               56.97 |
| yugabytedb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1992.95 |                62721.00 |            125000.00 |                             15127.00 | 1.00 |               57.40 |
| yugabytedb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2003.04 |                62405.00 |            125000.00 |                             15439.00 | 1.00 |               57.69 |
| yugabytedb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1962.91 |                63681.00 |            125000.00 |                             15087.00 | 1.00 |               56.53 |
| yugabytedb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1852.37 |                67481.00 |            125000.00 |                             15903.00 | 1.00 |               53.35 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |               53.35 |                        15723.42 |                67481.00 |           1000000.00 |                             15306.00 |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        12101.37 |               826353.00 |            5001234 |                           52799.00 |              4998766 |                             61887.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        12101.37 |               826353.00 |            5001234 |                           52799.00 |              4998766 |                             61887.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1854.49 |     32.87 |           6.06 |                 13.32 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |         7.10 |      0.07 |           0.24 |                  0.26 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        72.33 |      1.28 |           0.20 |                  0.21 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     24091.74 |     34.30 |          10.40 |                 21.51 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        39.57 |      0.16 |           0.31 |                  0.34 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1155.28 |      1.96 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                    3751.65 |                                        0.26 |                                         3.48 |                     59.00 |                      612.00 |

#### Loading phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               0.18 |                                         0.59 |                                0.00 |                       500.93 |                               0.17 |

#### Benchmarking phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                   13960.01 |                                        0.70 |                                         4.01 |                     63.00 |                      616.00 |

#### Benchmarking phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               0.18 |                                         0.08 |                                0.00 |                       501.00 |                               0.17 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## Persistent Storage

Persistent storage is not managed by bexhoma, but by YugabyteDB.
If you want YugabyteDB to have real persistent storage, install it with `storage.ephemeral=false` (`install_yugabytedb yes <storage class>`).

### Execution Only

As YugabyteDB lives outside of bexhoma, its data survives an experiment as long as the installation is kept.
The test script runs this right after the monitoring example, on the same installation:

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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_yugabytedb_execution.log
```

This skips loading (`-sl`), as data is already present in the database.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_execution_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb_execution.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 655s 
* Code: 1794850816
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
  * Experiment uses bexhoma version 0.11.18.
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
  * disk:1326253
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:663866
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1326253
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1408843
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:664083
    * cpu_list:0-127
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1408843
    * cpu_list:0-127
  * yb-master 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1326253
    * cpu_list:0-223
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1794850816

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794850816-87cb75dc9-zhh89: 0
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

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        20390.98 |               490413.00 |            4999287 |                           46719.00 |              5000713 |                             54175.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        20390.98 |               490413.00 |            4999287 |                           46719.00 |              5000713 |                             54175.00 |

### Monitoring

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     17309.71 |     40.03 |          13.27 |                 25.35 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        19.14 |      0.13 |           0.26 |                  0.29 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       602.96 |      1.51 |           0.54 |                  0.54 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Loading completed without failures
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

### Bexhoma Status Volume

The experiment setup can request a PVC.
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
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_yugabytedb_storage.log
```

This will add a PVC to the placeholder pod.
Nothing will be stored there, but it maintains status information about previous loading processes.

```bash
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                 | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+=========================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-yugabytedb-ycsb-1       | yugabytedb      | ycsb-1       | True         |               300 | YugabyteDB | shared               | 1Gi       | Bound    | 1.0G   | 36M    |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

The status shows a completed YCSB loading process (managed by bexhoma) of size SF=1.
Later experiments of this kind skip loading, since the PVC marks the loading as finished.
This thus helps to spare the `-sl` parameter.

However bexhoma cannot verify such information.
If YugabyteDB is restarted or data is deleted somehow, this PVC information will be outdated and wrong.
This approach helps bexhoma to persist status information, but it does not persist data inside YugabyteDB.

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 842s 
* Code: 1794852739
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
  * Experiment uses bexhoma version 0.11.18.
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
  * disk:1276542
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
    * disk:662267
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406081
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1276658
    * cpu_list:0-223
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662267
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1276768
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406081
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794852739

### Ingestion
* YugabyteDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794852739-69cc6ddf5-6kvkz: 0
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

| connection           |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| yugabytedb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2540.50 |                49203.00 |            125000.00 |                             13735.00 | 1.00 |               73.17 |
| yugabytedb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2579.98 |                48450.00 |            125000.00 |                             13503.00 | 1.00 |               74.30 |
| yugabytedb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2620.65 |                47698.00 |            125000.00 |                             13399.00 | 1.00 |               75.47 |
| yugabytedb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2624.84 |                47622.00 |            125000.00 |                             13375.00 | 1.00 |               75.60 |
| yugabytedb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2619.56 |                47718.00 |            125000.00 |                             13391.00 | 1.00 |               75.44 |
| yugabytedb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2585.48 |                48347.00 |            125000.00 |                             13527.00 | 1.00 |               74.46 |
| yugabytedb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2621.75 |                47678.00 |            125000.00 |                             13463.00 | 1.00 |               75.51 |
| yugabytedb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2598.00 |                48114.00 |            125000.00 |                             13543.00 | 1.00 |               74.82 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |               73.17 |                        20790.75 |                49203.00 |           1000000.00 |                             13492.00 |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        19606.77 |               510028.00 |            4998440 |                           44031.00 |              5001560 |                             50847.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        19606.77 |               510028.00 |            4998440 |                           44031.00 |              5001560 |                             50847.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1574.94 |     31.67 |           6.22 |                 13.65 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |         5.16 |      0.08 |           0.22 |                  0.24 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        55.47 |      2.43 |           0.11 |                  0.11 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     17801.14 |     37.88 |          11.03 |                 22.37 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        20.01 |      0.12 |           0.23 |                  0.25 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       611.52 |      1.50 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## Technical Details

### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'YugabyteDB': {
    'abbreviation': 'yb',
    'loadData': 'psql -U yugabyte --host yb-tserver-service.{namespace}.svc.cluster.local --port 5433 < {scriptname}',
    'template': {
        'version': 'v2.17.1',
        'alias': 'Cloud-Native-1',
        'docker_alias': 'CN1',
        'JDBC': {
            'driver': "com.yugabyte.Driver",
            'auth': ["yugabyte", ""],
            'url': 'jdbc:yugabytedb://yb-tserver-service.{namespace}.svc.cluster.local:5433/yugabyte?load-balance=true',
            'jar': 'jdbc-yugabytedb-42.3.5-yb-2.jar',
            'database': 'yugabyte',
            'schema': 'public',
            'explain': ['EXPLAIN (VERBOSE, FORMAT JSON) {query}'],
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery for yb-master (port 7000) and yb-tserver (port 9000) pods
},
```

where
* `abbreviation`: short name in the names of volumes
* `loadData`: command to create the schema, via `psql` of the placeholder pod against the tserver service
* `JDBC`: used to configure YCSB; the connection targets the tserver service
* `monitor`: Prometheus discovery of the master and tserver pods, scraping the native endpoint `/prometheus-metrics`

Benchbase does not read the connection from `cluster.config`, but from parameters that are set explicitly in `benchbase.py`:

```bash
BENCHBASE_PROFILE = 'postgres',
BEXHOMA_DATABASE = 'yugabyte',
BEXHOMA_USER = "yugabyte",
BEXHOMA_PASSWORD = "",
BEXHOMA_PORT = 5433,
```

### Deployment

* YugabyteDB itself is installed by Helm, see [Prerequisites](#prerequisites-install-yugabytedb).
  With persistent storage the chart adds a liveness probe (a disk check); its timeout is the chart's root key `livenessProbe.timeoutSeconds` (per-component keys are ignored).
* The placeholder pod is an instance of PostgreSQL, that does nothing but carry status information and run `psql`: [deploymenttemplate-YugabyteDB.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-YugabyteDB.yml).
* The storage metrics include the tserver volumes (`config.set_pvc_selector('app=yb-tserver')`); `volume_used`/`volume_size` still come from the placeholder pod.
* In `ycsb.py` there is a section about YugabyteDB. Watch for
  * `config.sut_service_name`: fixed name for the service of the SUT (`yb-tserver-service`)
  * `config.sut_container_name`: fixed name for the container of the SUT (empty)
  * `config.get_worker_pods()`: finds the pods of the worker nodes (`yb-tserver-0`, `yb-tserver-1`, `yb-tserver-2`), for host infos like CPU, RAM, node name
  * `config.create_monitoring()`: creates names for monitored components (for the SUT `yb-tserver-`), so the placeholder does not contribute to the monitoring
  * `config.get_worker_endpoints()`: finds the sidecar containers of the workers of a distributed DBMS for monitoring
  * `config.set_metric_of_config()`: creates PromQL queries from templates (pod like `yb-tserver`, no container name)
* The YCSB images include the YugabyteDB JDBC driver ([generator](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ycsb/generator/Dockerfile), [benchmarker](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ycsb/benchmarker/Dockerfile)):

```bash
######### Specific version of YugabyteDB JDBC #########
RUN wget https://github.com/yugabyte/pgjdbc/releases/download/v42.3.5-yb-2/jdbc-yugabytedb-42.3.5-yb-2.jar
RUN cp jdbc-yugabytedb-42.3.5-yb-2.jar jars/jdbc-yugabytedb-42.3.5-yb-2.jar
```

### Schema and Scripts

If data should be loaded, bexhoma at first creates a schema according to [experiments/ycsb/YugabyteDB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/YugabyteDB).

DDL parameters (`-xddl`, see [DDL parameters](DBMS.md#ddl-parameters--xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `pk_sharding` | YCSB | `hash`, `asc` | `hash` | sharding of the primary key: hash spreads load evenly and suits point reads, asc keeps key order for range scans (workload e) but concentrates ordered inserts |
| `num_tablets` | YCSB | `auto`, `4`, `8`, `16`, `32`, `64`, `128` | `auto` | tablets of usertable from the start (auto: ysql_num_shards_per_tserver and automatic splitting); only with pk_sharding=hash (asc needs SPLIT AT VALUES). Requires `pk_sharding` = `hash` |
| `colocated` | BenchBase TPC-C | `off`, `small` | `off` | small: database benchbase created WITH colocation = true, so warehouse, district and item share one tablet (fewer RPCs for small tables; district gets a range key instead of a hash key); stock, customer, history, oorder, new_order and order_line keep their own tablets. off: a tablet set per table |

### Load Durability

`-xld` has no effect on YugabyteDB: there are no durability scripts for it.

### Reset Scripts

With `-ar`, the reset scripts run before each benchmarking round:

1. Statistics: `ANALYZE VERBOSE` (cluster-wide)
2. Persist: n/a (no `CHECKPOINT` in YSQL, no `yb-admin` in the placeholder pod)
3. Counters: `reset-counters.sh`: `pg_stat_reset()` on every tserver (`yb-tserver-N.yb-tservers`), not once through the service, which picks one tserver per connection

See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract and [Test: Reset Scripts](Test-Reset.md) for the test runs, with results for [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_yugabytedb_summary.md), [Benchbase](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_yugabytedb_summary.md).


## Benchbase's TPC-C

### Simple Example

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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_yugabytedb.log
```

yields

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_yugabytedb_summary.md" target="_blank" rel="noopener">docs_benchbase_yugabytedb.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1322s 
* Code: 1794853811
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
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
  * disk:1276537
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:661027
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1276618
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406628
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:661018
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1276621
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406432
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794853811
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1278724
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:661934
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1278727
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1407373
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:661936
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1278788
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1407373
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794853811

### Ingestion
* YugabyteDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794853811-6955bcbbf9-x5x4l: 0
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

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| YugabyteDB-1-1 |                1 |   16 |      445.00 |         305.00 |            0.00 |        138.00 |            2.00 |              1 |         1 |             | None           |             0 | False         |              129.44 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         319.79 |                      318.62 |         0.00 |                                                     127120.00 |                                              50013.00 |
| yugabytedb-1-1-2-1-1 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                         150.57 |                      149.83 |         0.00 |                                                     132826.00 |                                              53103.00 |
| yugabytedb-1-1-2-1-2 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        0 |                         146.76 |                      146.11 |         0.00 |                                                     132883.00 |                                              54484.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         319.79 |                      318.62 |         0.00 |                                                     127120.00 |                                              50013.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        0 |                         297.32 |                      295.94 |         0.00 |                                                     132883.00 |                                              53793.50 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      2847.97 |     26.94 |           8.53 |                 16.28 |
| yugabytedb-1-1-2-1 |      2847.97 |     26.94 |           8.53 |                 16.28 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        26.08 |      0.12 |           0.30 |                  0.33 |
| yugabytedb-1-1-2-1 |        26.08 |      0.12 |           0.30 |                  0.33 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       727.07 |     12.16 |           0.26 |                  0.26 |
| yugabytedb-1-1-2-1 |       727.07 |     12.16 |           0.26 |                  0.26 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     10231.11 |     38.02 |          10.60 |                 19.92 |
| yugabytedb-1-1-2-1 |      9767.29 |     35.25 |          11.27 |                 22.33 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        17.27 |      0.18 |           0.31 |                  0.34 |
| yugabytedb-1-1-2-1 |        20.42 |      0.18 |           0.32 |                  0.34 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       143.68 |      1.00 |           0.31 |                  0.31 |
| yugabytedb-1-1-2-1 |       272.25 |      1.20 |           0.27 |                  0.27 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
           : storage bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-1 exists
TiDB-1                        : storage bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-2 exists
TiDB-1                        : storage bxw-bx-pd-ti-nvme-benchbase-tpcc-16-0 exists
TiDB-1                        : storage bxw-bx-pd-ti-nvme-benchbase-tpcc-16-1 exists
TiDB-1                        : storage bxw-bx-pd-ti-nvme-benchbase-tpcc-16-2 exists
Loop pass                     : took 2.5s (1 kubectl calls 1.3s, 17 API requests 0.7s)
- waiting 30s -               : done
TiDB-1                        : waits for health check to succeed
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 23 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : worker pods found: ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : found 3 / 3 running workers (component pd)
TiDB-1                        : worker pods found: ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : found 3 / 3 running workers (component tikv)
TiDB-1                        : will start benchmarking but not before 2026-11-14 16:20:11 (that is in 60 secs)
Loop pass                     : took 2.6s (0 kubectl calls 0.0s, 37 API requests 1.7s)
- waiting 30s -               : done
TiDB-1                        : will start benchmarking but not before 2026-11-14 16:20:11
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 16 API requests 0.7s)
- waiting 30s -               : done
Experiment                    : Reset experiment counter. This is first run of client number 1.
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-2-1-TiDB-1-1794671794 initialized to 1.
TiDB-1                        : benchmarks done 1 of 2. This will be client 1
tidb-1-2-1-1                  : start benchmarking (benchmark_run=1)
TiDB-1                        : worker pods found: ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : worker pods found: ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-5t8qc
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-7fclf
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-pxpmr
tidb-1-2-1-1                  : needs monitoring (common metrics) for deployment sut
tidb-1-2-1-1                  : needs monitoring (custom metrics) for stateful set pd
tidb-1-2-1-1                  : needs monitoring (custom metrics) for stateful set tikv
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : benchmarking results in folder D:\data\benchmarks/1794671794
TiDB-1                        : submitted benchmarker job in 51.6s (6 kubectl calls 6.5s, 169 API requests 41.0s)
Loop pass                     : took 54.4s (6 kubectl calls 6.5s, 192 API requests 42.5s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 23 API requests 0.8s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.9s (0 kubectl calls 0.0s, 21 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.2s (0 kubectl calls 0.0s, 21 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 21 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 21 API requests 0.9s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 21 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 21 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.9s (0 kubectl calls 0.0s, 21 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 2.6s (0 kubectl calls 0.0s, 21 API requests 1.1s)
- waiting 30s -               : done
tidb-1-2-1-1                  : wrote benchmarking_timespans to D:/data/benchmarks/1794671794/tidb-1-2-1-1.config
tidb-1-2-1-1                  : showing benchmarker times
tidb-1-2-1-1                  : benchmarker timespan job from 1794673266 to 1794673587
tidb-1-2-1-1                  : benchmarker timespan pods from 1794673269 to 1794673571
tidb-1-2-1-1                  : benchmarker timespan (start to end single container [s]) = 302
tidb-1-2-1-1                  : benchmarker times (start/end per pod and container) = [(1794673269, 1794673571)]
tidb-1-2-1-1                  : found and updated times {'benchmarker': [(1794673269, 1794673571)]}
tidb-1-2-1-1                  : needs monitoring (common metrics) for deployment sut
tidb-1-2-1-1                  : collecting execution metrics of SUT at connection tidb-1-2-1-1
tidb-1-2-1-1                  : needs monitoring (custom metrics) for stateful set pd
tidb-1-2-1-1                  : collecting execution metrics of pd at connection tidb-1-2-1-1
tidb-1-2-1-1                  : needs monitoring (custom metrics) for stateful set tikv
tidb-1-2-1-1                  : collecting execution metrics of tikv at connection tidb-1-2-1-1
tidb-1-2-1-1                  : collecting metrics of benchmarker at connection tidb-1-2-1-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-2
tidb-1-2-1-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)tidb-1-1794671794(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)tidb-1-1794671794(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-1-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)bx-pd-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)bx-pd-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-1-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)bx-tikv-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)bx-tikv-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-1-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-tidb-1-1794671794-2-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-tidb-1-1794671794-2-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-1-1                  : WARNING metric missing for benchmarking: CPU Throttling Rate [s/s]
tidb-1-2-1-1                  : WARNING metric missing for benchmarking: CPU Throttled Time [s]
tidb-1-2-1-1                  : WARNING metric missing for benchmarker: CPU Throttling Rate [s/s]
tidb-1-2-1-1                  : WARNING metric missing for benchmarker: CPU Throttled Time [s]
tidb-1-2-1-1                  : WARNING metric missing for tikvbenchmarking: CPU Throttling Rate [s/s]
tidb-1-2-1-1                  : WARNING metric missing for tikvbenchmarking: CPU Throttled Time [s]
Experiment                    : fetched 4 metric sets in 6s (4 at once, 0 repeated, 0 follow-up actions; 6 kubectl calls 16.7s, 0 API requests 0.0s)
Loop pass                     : took 18.1s (14 kubectl calls 25.3s, 32 API requests 2.8s)
Experiment                    : Reset experiment counter. This is first run of client number 2.
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-2-2-TiDB-1-1794671794 initialized to 2.
TiDB-1                        : benchmarks done 1 of 2. This will be client 2
tidb-1-2-2-1                  : start benchmarking (benchmark_run=1)
TiDB-1                        : worker pods found: ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : worker pods found: ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-5t8qc
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-7fclf
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-pxpmr
tidb-1-2-2-1                  : needs monitoring (common metrics) for deployment sut
tidb-1-2-2-1                  : needs monitoring (custom metrics) for stateful set pd
tidb-1-2-2-1                  : needs monitoring (custom metrics) for stateful set tikv
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : benchmarking results in folder D:\data\benchmarks/1794671794
TiDB-1                        : submitted benchmarker job in 12.9s (3 kubectl calls 3.5s, 66 API requests 8.4s)
Loop pass                     : took 14.6s (3 kubectl calls 3.5s, 90 API requests 9.6s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.3s (0 kubectl calls 0.0s, 24 API requests 1.2s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 22 API requests 1.2s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.2s (0 kubectl calls 0.0s, 22 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 22 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.2s (0 kubectl calls 0.0s, 22 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 22 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 9.8s (0 kubectl calls 0.0s, 22 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 22 API requests 1.2s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.2s (0 kubectl calls 0.0s, 22 API requests 1.2s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 22 API requests 0.9s)
- waiting 30s -               : done
tidb-1-2-2-1                  : wrote benchmarking_timespans to D:/data/benchmarks/1794671794/tidb-1-2-2-1.config
tidb-1-2-2-1                  : showing benchmarker times
tidb-1-2-2-1                  : benchmarker timespan job from 1794673615 to 1794673980
tidb-1-2-2-1                  : benchmarker timespan pods from 1794673632 to 1794673934
tidb-1-2-2-1                  : benchmarker timespan (start to end single container [s]) = 302
tidb-1-2-2-1                  : benchmarker times (start/end per pod and container) = [(1794673632, 1794673934), (1794673632, 1794673934)]
tidb-1-2-2-1                  : found and updated times {'benchmarker': [(1794673632, 1794673934), (1794673632, 1794673934)]}
tidb-1-2-2-1                  : needs monitoring (common metrics) for deployment sut
tidb-1-2-2-1                  : collecting execution metrics of SUT at connection tidb-1-2-2-1
tidb-1-2-2-1                  : needs monitoring (custom metrics) for stateful set pd
tidb-1-2-2-1                  : collecting execution metrics of pd at connection tidb-1-2-2-1
tidb-1-2-2-1                  : needs monitoring (custom metrics) for stateful set tikv
tidb-1-2-2-1                  : collecting execution metrics of tikv at connection tidb-1-2-2-1
tidb-1-2-2-1                  : collecting metrics of benchmarker at connection tidb-1-2-2-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-2
tidb-1-2-2-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)tidb-1-1794671794(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)tidb-1-1794671794(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-2-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)bx-pd-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)bx-pd-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-2-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)bx-tikv-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)bx-tikv-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-2-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-tidb-1-1794671794-2-2-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-tidb-1-1794671794-2-2-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-2-1                  : WARNING metric missing for benchmarker: CPU Throttling Rate [s/s]
tidb-1-2-2-1                  : WARNING metric missing for benchmarker: CPU Throttled Time [s]
tidb-1-2-2-1                  : WARNING metric missing for tikvbenchmarking: CPU Throttling Rate [s/s]
tidb-1-2-2-1                  : WARNING metric missing for tikvbenchmarking: CPU Throttled Time [s]
tidb-1-2-2-1                  : WARNING metric missing for benchmarking: CPU Throttling Rate [s/s]
tidb-1-2-2-1                  : WARNING metric missing for benchmarking: CPU Throttled Time [s]
Experiment                    : fetched 4 metric sets in 7s (4 at once, 0 repeated, 0 follow-up actions; 6 kubectl calls 19.8s, 0 API requests 0.0s)
Loop pass                     : took 20.7s (16 kubectl calls 30.7s, 36 API requests 2.9s)
TiDB-1                        : can be stopped
TiDB-1                        : had 0 restarts at worker bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-5t8qc
TiDB-1                        : had 0 restarts at worker bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-7fclf
TiDB-1                        : had 0 restarts at worker bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-pxpmr
TiDB-1                        : worker pods found: ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : had 0 restarts at worker bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : had 0 restarts at worker bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : had 0 restarts at worker bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : worker pods found: ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : had 0 restarts at worker bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : had 0 restarts at worker bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : had 0 restarts at worker bx-tikv-ti-nvme-benchbase-tpcc-16-2
Loop pass                     : took 25.0s (19 kubectl calls 21.0s, 59 API requests 2.5s)
Experiment                    : ends at 2026-11-14 17:33:40.835045 (310562.1913098) - 2224.48s total
Experiment                    : transforming metrics for loading
Experiment                    : transforming metrics for loading completed
Experiment                    : transforming metrics for benchmarking
Experiment                    : transforming metrics for benchmarking completed
Experiment                    : transforming metrics for loader
Experiment                    : transforming metrics for loader completed
Experiment                    : transforming metrics for benchmarker
Experiment                    : transforming metrics for benchmarker completed
Experiment                    : transforming metrics for loading
Experiment                    : transforming metrics for loading completed
Experiment                    : transforming metrics for pdloading
Experiment                    : transforming metrics for pdloading completed
Experiment                    : transforming metrics for tikvloading
Experiment                    : transforming metrics for tikvloading completed
Experiment                    : transforming metrics for loader
Experiment                    : transforming metrics for loader completed
Experiment                    : transforming metrics for benchmarking
Experiment                    : transforming metrics for benchmarking completed
Experiment                    : transforming metrics for pdbenchmarking
Experiment                    : transforming metrics for pdbenchmarking completed
Experiment                    : transforming metrics for tikvbenchmarking
Experiment                    : transforming metrics for tikvbenchmarking completed
Experiment                    : transforming metrics for benchmarker
Experiment                    : transforming metrics for benchmarker completed
Experiment                    : downloading partial results
Experiment                    : uploading full results
Experiment                    : uploading workload file
Result workflow complete

## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2225s 
* Code: 1794671794
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 1 processes (pods).
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* tidb-1-1-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:613794
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:613794
    * cpu_list:0-127
  * sut 1
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:282051
    * cpu_list:0-255
  * sut 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384403
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:613794
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146787
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-223
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384403
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:613794
    * datadisk:7591
    * volume_size:49G
    * volume_used:7.5G
    * cpu_list:0-127
  * tikv 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146788
    * datadisk:5380
    * volume_size:49G
    * volume_used:5.3G
    * cpu_list:0-223
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384403
    * datadisk:7576
    * volume_size:49G
    * volume_used:7.4G
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794671794
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-1-2-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:613793
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:613793
    * cpu_list:0-127
  * sut 1
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:282054
    * cpu_list:0-255
  * sut 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384319
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:613793
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146790
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-223
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384319
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:613793
    * datadisk:5121
    * volume_size:49G
    * volume_used:5.1G
    * cpu_list:0-127
  * tikv 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146790
    * datadisk:7004
    * volume_size:49G
    * volume_used:6.9G
    * cpu_list:0-223
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384319
    * datadisk:5025
    * volume_size:49G
    * volume_used:5.0G
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794671794
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-2-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:770370
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:770366
    * cpu_list:0-255
  * sut 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * cpu_list:0-127
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146789
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-223
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * datadisk:4608
    * volume_size:49G
    * volume_used:4.5G
    * cpu_list:0-127
  * tikv 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146789
    * datadisk:4631
    * volume_size:49G
    * volume_used:4.6G
    * cpu_list:0-223
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * datadisk:4647
    * volume_size:49G
    * volume_used:4.6G
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794671794
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
    * ddl_num_worker_replicas:3
* tidb-1-2-2-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:787183
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:787183
    * cpu_list:0-255
  * sut 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * cpu_list:0-127
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146790
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-223
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * datadisk:7042
    * volume_size:49G
    * volume_used:6.9G
    * cpu_list:0-127
  * tikv 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146790
    * datadisk:7038
    * volume_size:49G
    * volume_used:6.9G
    * cpu_list:0-223
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * datadisk:7056
    * volume_size:49G
    * volume_used:6.9G
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794671794
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
    * ddl_num_worker_replicas:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: TiDB-1-2

### Data Parameters of Reused Volumes
* TiDB-1: DDL values of the volume: num_worker_replicas=3
* TiDB-1: loading values of the volume: script=Schema, indexing=Checks

### Ingestion
* TiDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-tidb-1-1794671794-57cb8499bb-b4d9s: 0
* bexhoma-sut-tidb-1-1794671794-57cb8499bb-g2bk6: 0
* bexhoma-sut-tidb-1-1794671794-57cb8499bb-kvwfc: 0
* bx-pd-ti-nvme-benchbase-tpcc-16-0: 0
* bx-pd-ti-nvme-benchbase-tpcc-16-1: 0
* bx-pd-ti-nvme-benchbase-tpcc-16-2: 0
* bx-tikv-ti-nvme-benchbase-tpcc-16-0: 0
* bx-tikv-ti-nvme-benchbase-tpcc-16-1: 0
* bx-tikv-ti-nvme-benchbase-tpcc-16-2: 0
* bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-5t8qc: 0
* bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-7fclf: 0
* bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-pxpmr: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS TiDB-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 2 Client 2: benchbase (2 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS TiDB-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 2 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| TiDB-1-1 |                1 |   16 |      178.00 |           4.00 |            0.00 |        171.00 |            3.00 |              1 |         1 |             | None           |             0 | False         |              323.60 | False               |
| TiDB-1-2 |                2 |   16 |      178.00 |           4.00 |            0.00 |        171.00 |            3.00 |              1 |         1 |             | None           |             0 | False         |              323.60 | True                |

### Benchmarking

#### Per Connection

| connection     | phase      | job          |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:-----------|:-------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         261.16 |                      260.01 |         0.00 |                                                     142258.00 |                                              61251.00 |
| tidb-1-1-2-1-1 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                          85.64 |                       84.82 |         0.00 |                                                     261190.00 |                                              92643.00 |
| tidb-1-1-2-1-2 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        0 |                          85.32 |                       84.48 |         0.00 |                                                     265375.00 |                                              93375.00 |
| tidb-1-2-1-1-1 | tidb-1-2-1 | tidb-1-2-1-1 |                2 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         388.18 |                      386.37 |         0.00 |                                                      90154.00 |                                              41209.00 |
| tidb-1-2-2-1-1 | tidb-1-2-2 | tidb-1-2-2-1 |                2 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                         142.10 |                      140.59 |         0.00 |                                                     129096.00 |                                              56263.00 |
| tidb-1-2-2-1-2 | tidb-1-2-2 | tidb-1-2-2-1 |                2 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        0 |                         154.61 |                      152.86 |         0.00 |                                                     121664.00 |                                              51716.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------|:-----------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         261.16 |                      260.01 |         0.00 |                                                     142258.00 |                                              61251.00 |
| tidb-1-1-2 | tidb-1-1-2 |                1 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        0 |                         170.96 |                      169.31 |         0.00 |                                                     265375.00 |                                              93009.00 |
| tidb-1-2-1 | tidb-1-2-1 |                2 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         388.18 |                      386.37 |         0.00 |                                                      90154.00 |                                              41209.00 |
| tidb-1-2-2 | tidb-1-2-2 |                2 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        0 |                         296.71 |                      293.46 |         0.00 |                                                     129096.00 |                                              53989.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      1190.33 |      8.95 |           3.35 |                  3.93 |
| tidb-1-1-2-1 |      1190.33 |      8.95 |           3.35 |                  3.93 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        84.65 |      0.52 |           0.21 |                  0.21 |
| tidb-1-1-2-1 |        84.65 |      0.52 |           0.21 |                  0.21 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      2696.38 |     20.81 |          13.34 |                 29.84 |
| tidb-1-1-2-1 |      2696.38 |     20.81 |          13.34 |                 29.84 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       114.52 |      1.34 |           0.56 |                  0.56 |
| tidb-1-1-2-1 |       114.52 |      1.34 |           0.56 |                  0.56 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      2800.82 |     10.08 |           3.35 |                  3.93 |
| tidb-1-1-2-1 |      1947.22 |      9.28 |           2.15 |                  2.73 |
| tidb-1-2-1-1 |      3035.57 |     10.96 |           1.87 |                  2.45 |
| tidb-1-2-2-1 |      2621.77 |      8.97 |           2.49 |                  3.07 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       301.46 |      1.04 |           0.22 |                  0.22 |
| tidb-1-1-2-1 |       248.62 |      1.05 |           0.22 |                  0.22 |
| tidb-1-2-1-1 |       164.32 |      0.65 |           0.26 |                  0.26 |
| tidb-1-2-2-1 |       176.05 |      0.69 |           0.27 |                  0.27 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      3781.57 |     16.05 |          14.75 |                 31.95 |
| tidb-1-1-2-1 |      2708.51 |     13.63 |          16.13 |                 32.26 |
| tidb-1-2-1-1 |      4528.13 |     17.29 |          11.46 |                 26.18 |
| tidb-1-2-2-1 |      3807.01 |     15.66 |          13.45 |                 32.14 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       145.34 |      0.55 |           0.32 |                  0.32 |
| tidb-1-1-2-1 |       117.71 |      0.46 |           0.29 |                  0.29 |
| tidb-1-2-1-1 |       182.46 |      0.86 |           0.32 |                  0.32 |
| tidb-1-2-2-1 |       412.57 |      1.54 |           0.30 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

### More Complex Example

This runs Benchbase's TPC-C variant with more data, for a longer period of time, with keying and thinking time (`-xkey`) and with a varying number of pods for execution.
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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_yugabytedb_keytime.log
```

yields

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_yugabytedb_keytime_summary.md" target="_blank" rel="noopener">docs_benchbase_yugabytedb_keytime.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 7445s 
* Code: 1794900771
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking has keying and thinking times activated. Benchmarking runs for 20 minutes.
  * Status is logged every 30ms.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
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
  * disk:1071465
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:567105
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1071449
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1420998
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:566965
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1071255
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1420772
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794900771
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1063874
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:561395
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1063874
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1413590
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:561395
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1063874
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1413590
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794900771
* yugabytedb-1-1-3-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1064121
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:557975
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1064121
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1413723
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:558862
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1064134
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1413723
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794900771
* yugabytedb-1-1-4-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1064275
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:559799
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1064275
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1413911
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:559842
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1064472
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1413911
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794900771

### Ingestion
* YugabyteDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794900771-fd98c9bfc-m49nq: 0
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

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| YugabyteDB-1-1 |                1 |  128 |     1769.00 |         306.00 |            0.00 |       1461.00 |            2.00 |              1 |         1 |             | None           |             0 | False         |              260.49 | False               |

### Benchmarking

#### Per Connection

| connection            | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |    time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|--------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1  | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |      1280 |    16384 |          -1 | 1200.00 |        0 |                          59.07 |                       58.82 |        96.48 |                                                     144279.00 |                                             900870.00 |
| yugabytedb-1-1-2-1-1  | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       1 |       640 |     8192 |          -1 | 1200.00 |        0 |                          29.43 |                       29.28 |        48.04 |                                                     170672.00 |                                             847551.00 |
| yugabytedb-1-1-2-1-2  | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       2 |       640 |     8192 |          -1 | 1200.00 |        0 |                          29.47 |                       29.34 |        48.12 |                                                     169574.00 |                                             896946.00 |
| yugabytedb-1-1-3-1-1  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |        3 |               1 |       1 |       256 |     3276 |          -1 | 1200.00 |        0 |                          11.77 |                       11.72 |        19.22 |                                                     181147.00 |                                             878574.00 |
| yugabytedb-1-1-3-1-2  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |        3 |               1 |       2 |       256 |     3276 |          -1 | 1200.00 |        0 |                          11.77 |                       11.73 |        19.23 |                                                     181085.00 |                                             842905.00 |
| yugabytedb-1-1-3-1-3  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |        3 |               1 |       3 |       256 |     3276 |          -1 | 1200.00 |        0 |                          11.73 |                       11.68 |        19.16 |                                                     178924.00 |                                             871481.00 |
| yugabytedb-1-1-3-1-4  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |        3 |               1 |       4 |       256 |     3276 |          -1 | 1200.00 |        0 |                          11.68 |                       11.63 |        19.08 |                                                     183082.00 |                                             836640.00 |
| yugabytedb-1-1-3-1-5  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |        3 |               1 |       5 |       256 |     3276 |          -1 | 1200.00 |        0 |                          11.83 |                       11.79 |        19.34 |                                                     181022.00 |                                             869028.00 |
| yugabytedb-1-1-4-1-1  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       1 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.86 |                        5.82 |         9.55 |                                                     191075.00 |                                             821183.00 |
| yugabytedb-1-1-4-1-2  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       2 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.89 |                        5.86 |         9.61 |                                                     187589.00 |                                             819572.00 |
| yugabytedb-1-1-4-1-3  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       3 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.98 |                        5.95 |         9.76 |                                                     193780.00 |                                             763706.00 |
| yugabytedb-1-1-4-1-4  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       4 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.74 |                        5.72 |         9.38 |                                                     187998.00 |                                             889616.00 |
| yugabytedb-1-1-4-1-5  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       5 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.84 |                        5.82 |         9.54 |                                                     188987.00 |                                             813357.00 |
| yugabytedb-1-1-4-1-6  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       6 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.88 |                        5.86 |         9.61 |                                                     194099.00 |                                             833858.00 |
| yugabytedb-1-1-4-1-7  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       7 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.96 |                        5.94 |         9.74 |                                                     200999.00 |                                             772878.00 |
| yugabytedb-1-1-4-1-8  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       8 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.92 |                        5.89 |         9.66 |                                                     190064.00 |                                             810467.00 |
| yugabytedb-1-1-4-1-9  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       9 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.94 |                        5.92 |         9.70 |                                                     195731.00 |                                             793686.00 |
| yugabytedb-1-1-4-1-10 | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |      10 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.86 |                        5.84 |         9.57 |                                                     189452.00 |                                             835158.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |    time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|--------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |      1280 |    16384 |          -1 | 1200.00 |        0 |                          59.07 |                       58.82 |        96.48 |                                                     144279.00 |                                             900870.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |        2 |               1 |           2 |      1280 |    16384 |          -1 | 1200.00 |        0 |                          58.90 |                       58.62 |        96.16 |                                                     170672.00 |                                             872248.50 |
| yugabytedb-1-1-3 | yugabytedb-1-1-3 |                1 |        3 |               1 |           5 |      1280 |    16380 |          -1 | 1200.00 |        0 |                          58.79 |                       58.55 |        96.03 |                                                     183082.00 |                                             859725.60 |
| yugabytedb-1-1-4 | yugabytedb-1-1-4 |                1 |        4 |               1 |          10 |      1280 |    16380 |          -1 | 1200.00 |        0 |                          58.88 |                       58.60 |        96.13 |                                                     200999.00 |                                             815348.10 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     27341.84 |     38.05 |          16.52 |                 48.03 |
| yugabytedb-1-1-2-1 |     27341.84 |     38.05 |          16.52 |                 48.03 |
| yugabytedb-1-1-3-1 |     27341.84 |     38.05 |          16.52 |                 48.03 |
| yugabytedb-1-1-4-1 |     27341.84 |     38.05 |          16.52 |                 48.03 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        93.12 |      0.18 |           0.31 |                  0.34 |
| yugabytedb-1-1-2-1 |        93.12 |      0.18 |           0.31 |                  0.34 |
| yugabytedb-1-1-3-1 |        93.12 |      0.18 |           0.31 |                  0.34 |
| yugabytedb-1-1-4-1 |        93.12 |      0.18 |           0.31 |                  0.34 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |    124286.53 |    120.13 |           0.39 |                  0.39 |
| yugabytedb-1-1-2-1 |    124286.53 |    120.13 |           0.39 |                  0.39 |
| yugabytedb-1-1-3-1 |    124286.53 |    120.13 |           0.39 |                  0.39 |
| yugabytedb-1-1-4-1 |    124286.53 |    120.13 |           0.39 |                  0.39 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     15064.28 |     21.15 |          39.85 |                 48.04 |
| yugabytedb-1-1-2-1 |     16959.70 |     22.74 |          40.56 |                 47.90 |
| yugabytedb-1-1-3-1 |     17581.21 |     24.17 |          41.02 |                 48.04 |
| yugabytedb-1-1-4-1 |     17620.29 |     24.72 |          41.92 |                 48.04 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       430.12 |      4.01 |           0.40 |                  0.43 |
| yugabytedb-1-1-2-1 |       432.89 |      4.01 |           0.41 |                  0.43 |
| yugabytedb-1-1-3-1 |       430.55 |      4.01 |           0.43 |                  0.45 |
| yugabytedb-1-1-4-1 |       427.82 |      4.01 |           0.43 |                  0.46 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       582.76 |      1.56 |           3.97 |                  3.97 |
| yugabytedb-1-1-2-1 |       583.59 |      2.01 |           2.10 |                  2.10 |
| yugabytedb-1-1-3-1 |       833.57 |      5.58 |           0.98 |                  0.98 |
| yugabytedb-1-1-4-1 |      1236.26 |     10.32 |           0.63 |                  0.63 |

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
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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

### Application Metrics

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
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  run &>$LOG_DIR/docs_benchbase_yugabytedb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_yugabytedb_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_yugabytedb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1541s 
* Code: 1794908443
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 1 processes (pods).
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
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:553740
  * datadisk:39
  * volume_size:879G
  * volume_used:541G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:553740
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1058593
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406344
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:553740
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1058594
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406344
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794908443
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:554332
  * datadisk:39
  * volume_size:879G
  * volume_used:542G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:554319
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1059236
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406976
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:554319
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1059236
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406976
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794908443

### Ingestion
* YugabyteDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794908443-57b6b9fb97-nhjxh: 0
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

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| YugabyteDB-1-1 |                1 |   16 |      441.00 |         305.00 |            0.00 |        134.00 |            2.00 |              1 |         1 |             | None           |             0 | False         |              130.61 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         223.16 |                      222.25 |         0.00 |                                                     183890.00 |                                              71679.00 |
| yugabytedb-1-1-2-1-1 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                         143.28 |                      142.56 |         0.00 |                                                     142508.00 |                                              55806.00 |
| yugabytedb-1-1-2-1-2 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        1 |                         156.12 |                      155.45 |         0.00 |                                                     128837.00 |                                              51218.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         223.16 |                      222.25 |         0.00 |                                                     183890.00 |                                              71679.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        1 |                         299.40 |                      298.01 |         0.00 |                                                     142508.00 |                                              53512.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      3039.45 |     33.04 |           8.40 |                 17.32 |
| yugabytedb-1-1-2-1 |      3039.45 |     33.04 |           8.40 |                 17.32 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        34.29 |      0.21 |           0.38 |                  0.40 |
| yugabytedb-1-1-2-1 |        34.29 |      0.21 |           0.38 |                  0.40 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       630.95 |     10.07 |           0.26 |                  0.26 |
| yugabytedb-1-1-2-1 |       630.95 |     10.07 |           0.26 |                  0.26 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      9600.51 |     34.03 |          10.45 |                 19.24 |
| yugabytedb-1-1-2-1 |     10121.34 |     37.61 |          11.51 |                 20.24 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        21.31 |      0.16 |           0.43 |                  0.46 |
| yugabytedb-1-1-2-1 |        22.95 |      0.18 |           0.46 |                  0.49 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        79.77 |      0.30 |           0.29 |                  0.29 |
| yugabytedb-1-1-2-1 |       175.00 |      0.78 |           0.27 |                  0.27 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                     239.46 |                                        0.77 |                                        10.48 |                     16.00 |                      614.00 |
| yugabytedb-1-1-2-1 |                                     239.46 |                                        0.77 |                                        10.48 |                     16.00 |                      614.00 |

#### Loading phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               1.78 |                                         1.41 |                                0.04 |                       500.80 |                               1.78 |
| yugabytedb-1-1-2-1 |                               1.78 |                                         1.41 |                                0.04 |                       500.80 |                               1.78 |

#### Benchmarking phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                    7877.99 |                                        0.55 |                                         8.00 |                     16.00 |                      620.00 |
| yugabytedb-1-1-2-1 |                                   10785.08 |                                        0.55 |                                         1.88 |                     16.00 |                      611.00 |

#### Benchmarking phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               0.02 |                                         0.10 |                                0.00 |                       500.84 |                               0.02 |
| yugabytedb-1-1-2-1 |                               0.00 |                                         0.10 |                                0.00 |                       501.01 |                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
