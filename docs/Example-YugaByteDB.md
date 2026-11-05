# Example: Benchmark YugabyteDB

This example shows how to benchmark YugabyteDB with YCSB and Benchbase's TPC-C.
This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that is not managed by bexhoma, but exists in the Kubernetes cluster in the same namespace**.

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
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
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
* tests if results match workflow (`-tr`)
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
* Duration: 305s 
* Code: 1793710976
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
  * Experiment uses bexhoma version 0.11.12.
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
  * disk:797930
  * datadisk:39
  * volume_size:1.8T
  * volume_used:780G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:797957
    * cpu_list:0-223
  * yb-tserver 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:616851
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:629329
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:797220
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:629432
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:616438
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793710976

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793710976-99df487fc-s4nhm: 0
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
| yugabytedb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2533.60 |                49337.00 |            125000.00 |                              5619.00 | 1.00 |               72.97 |
| yugabytedb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2488.90 |                50223.00 |            125000.00 |                              5635.00 | 1.00 |               71.68 |
| yugabytedb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2528.98 |                49427.00 |            125000.00 |                              5623.00 | 1.00 |               72.83 |
| yugabytedb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2527.04 |                49465.00 |            125000.00 |                              5703.00 | 1.00 |               72.78 |
| yugabytedb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2516.51 |                49672.00 |            125000.00 |                              5567.00 | 1.00 |               72.48 |
| yugabytedb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2558.38 |                48859.00 |            125000.00 |                              5715.00 | 1.00 |               73.68 |
| yugabytedb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2499.90 |                50002.00 |            125000.00 |                              5611.00 | 1.00 |               72.00 |
| yugabytedb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2527.09 |                49464.00 |            125000.00 |                              5699.00 | 1.00 |               72.78 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               71.68 |                        20180.40 |                50223.00 |           1000000.00 |                              5646.50 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 | YugabyteDB-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        24597.83 |                40654.00 |             500206 |                           33951.00 |               499794 |                             41855.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        24597.83 |                40654.00 |             500206 |                           33951.00 |               499794 |                             41855.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
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

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).
Metrics are sampled every few seconds, so the benchmarking phase should take at least a minute.
This run uses 10.000.000 operations (`-xop`).

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 tservers of the YugabyteDB cluster.

The `-mc` option is mandatory here: the sidecar container approach does not work (since bexhoma does not manage the deployment), so either you have Prometheus / Node exporter already installed in your cluster or a daemonset is needed.
See [Monitoring](Monitoring.html) for further explanation.

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

### Application Metrics

Collecting application metrics for YugabyteDB is supported.
It can be activated by `-m -mc -ma`.
Prometheus discovers the master pods (port 7000) and the tserver pods (port 9000) and scrapes the native endpoint `/prometheus-metrics` of YugabyteDB, with the metric sets `yb-master` and `yb-tserver`.
See [Metrics](Example-Metrics.html) for application metrics of all DBMS.

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
  -tr \
  run &>$LOG_DIR/docs_ycsb_yugabytedb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_yugabytedb_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_yugabytedb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 944s 
* Code: 1793234190
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
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1225130
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:418584
    * cpu_list:0-223
  * yb-tserver 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:514878
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:492025
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:418584
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:514878
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:492025
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793234190

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793234190-68c9c6667c-gj678: 0
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
| yugabytedb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2705.57 |                46201.00 |            125000.00 |                             12063.00 | 1.00 |               77.92 |
| yugabytedb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2732.54 |                45745.00 |            125000.00 |                             12319.00 | 1.00 |               78.70 |
| yugabytedb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2741.95 |                45588.00 |            125000.00 |                             12375.00 | 1.00 |               78.97 |
| yugabytedb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2675.97 |                46712.00 |            125000.00 |                             11503.00 | 1.00 |               77.07 |
| yugabytedb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2752.58 |                45412.00 |            125000.00 |                             12023.00 | 1.00 |               79.27 |
| yugabytedb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2695.36 |                46376.00 |            125000.00 |                             11975.00 | 1.00 |               77.63 |
| yugabytedb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2710.85 |                46111.00 |            125000.00 |                             11975.00 | 1.00 |               78.07 |
| yugabytedb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         2694.95 |                46383.00 |            125000.00 |                             11799.00 | 1.00 |               77.61 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |               77.07 |                        21709.77 |                46712.00 |           1000000.00 |                             12004.00 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 | YugabyteDB-1    |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        22875.91 |               437141.00 |            5001815 |                           38751.00 |              4998185 |                             44927.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        22875.91 |               437141.00 |            5001815 |                           38751.00 |              4998185 |                             44927.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      1471.84 |     29.24 |           5.81 |                 12.64 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |         7.06 |      0.06 |           0.25 |                  0.27 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        47.29 |      1.32 |           0.20 |                  0.21 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     16400.40 |     41.01 |          10.88 |                 22.45 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        18.63 |      0.10 |           0.29 |                  0.32 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       390.09 |      1.33 |           0.54 |                  0.54 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Active YSQL Connections for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverbenchmarking.log)
* Active YSQL Connections for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverloading.log)

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                    3753.28 |                                        0.42 |                                         2.30 |                      0.00 |                      572.00 |

#### Loading phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               0.05 |                                         0.48 |                                0.00 |                       500.20 |                               0.05 |

#### Benchmarking phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                   24114.72 |                                        0.62 |                                         1.95 |                      0.00 |                      641.00 |

#### Benchmarking phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               0.03 |                                         0.23 |                                0.00 |                       500.40 |                               0.03 |

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
* TEST failed: Monitoring metrics missing
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
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
  -tr \
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

### Bexhoma Status Volume

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

The above means there has been a YCSB loading process (managed by bexhoma) of size SF=1, that has been completed.
All following calls of such an experiment will skip loading, since the PVC tells it has been finished.
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
  -tr \
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

### More Complex Example

We now run Benchbase's TPC-C variant with more data, for a longer period of time, with keying and thinking time (`-xkey`) and with a varying number of pods for execution.
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
  -tr \
  run &>$LOG_DIR/docs_benchbase_yugabytedb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_yugabytedb_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_yugabytedb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1507s 
* Code: 1793235355
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
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
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1226303
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:365790
    * cpu_list:0-223
  * yb-tserver 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:492578
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:515504
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:365790
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:492578
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:515504
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793235355
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1226326
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:366717
    * cpu_list:0-223
  * yb-tserver 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:493602
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:516403
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:366717
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:493602
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:516403
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793235355

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793235355-57ff8f75b9-4jnqz: 0
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
| YugabyteDB-1-1 |                1 |   16 |      415.00 |         305.00 |            0.00 |        107.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              138.80 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         332.47 |                      330.97 |         0.00 |                                                     123369.00 |                                              48112.00 |
| yugabytedb-1-1-2-1-1 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         147.94 |                      147.23 |         0.00 |                                                     134383.00 |                                              54061.00 |
| yugabytedb-1-1-2-1-2 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            1 |                         141.30 |                      140.63 |         0.00 |                                                     138880.00 |                                              56600.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         332.47 |                      330.97 |         0.00 |                                                     123369.00 |                                              48112.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            1 |                         289.25 |                      287.85 |         0.00 |                                                     138880.00 |                                              55330.50 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      3055.70 |     35.08 |           8.63 |                 17.22 |
| yugabytedb-1-1-2-1 |      3055.70 |     35.08 |           8.63 |                 17.22 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        29.27 |      0.10 |           0.31 |                  0.34 |
| yugabytedb-1-1-2-1 |        29.27 |      0.10 |           0.31 |                  0.34 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        37.54 |      0.82 |           0.28 |                  0.28 |
| yugabytedb-1-1-2-1 |        37.54 |      0.82 |           0.28 |                  0.28 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     10423.52 |     39.36 |          10.29 |                 19.67 |
| yugabytedb-1-1-2-1 |     10342.54 |     37.25 |          11.89 |                 21.70 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        19.46 |      0.18 |           0.37 |                  0.40 |
| yugabytedb-1-1-2-1 |        22.67 |      0.17 |           0.41 |                  0.43 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       105.23 |      0.38 |           0.31 |                  0.31 |
| yugabytedb-1-1-2-1 |        99.24 |      0.64 |           0.26 |                  0.26 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Active YSQL Connections for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverbenchmarking.log)
* Active YSQL Connections for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverloading.log)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Active YSQL Connections for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-tserverbenchmarking.log)

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                     240.06 |                                        0.97 |                                        14.18 |                      0.00 |                      619.00 |
| yugabytedb-1-1-2-1 |                                     240.06 |                                        0.97 |                                        14.18 |                      0.00 |                      619.00 |

#### Loading phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               1.97 |                                         1.22 |                                0.04 |                       500.47 |                               1.97 |
| yugabytedb-1-1-2-1 |                               1.97 |                                         1.22 |                                0.04 |                       500.47 |                               1.97 |

#### Benchmarking phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                   11732.49 |                                        0.41 |                                        12.75 |                      0.00 |                      611.00 |
| yugabytedb-1-1-2-1 |                                   10444.97 |                                        0.45 |                                         1.79 |                      0.00 |                      597.00 |

#### Benchmarking phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               1.89 |                                         0.05 |                                0.00 |                       500.49 |                               1.89 |
| yugabytedb-1-1-2-1 |                               0.00 |                                         0.05 |                                0.00 |                       500.39 |                               0.00 |

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
* TEST failed: Monitoring metrics missing
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>
