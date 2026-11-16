# Example: Benchmark CockroachDB

This example shows how to benchmark CockroachDB with YCSB and Benchbase's TPC-C, as a cluster managed by bexhoma.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[CockroachDB](https://www.cockroachlabs.com/) is a distributed, PostgreSQL wire-compatible DBMS.
CockroachDB offers several installation methods; we here rely on *CockroachDB insecure test cluster in a single Kubernetes cluster*.
The benefit of this approach is we can use a [manifest](https://github.com/cockroachdb/cockroach/blob/master/cloud/kubernetes/cockroachdb-statefulset.yaml) for a stateful set provided by CockroachDB.
A CockroachDB cluster does not require a coordinator; every worker pod is a node of the cluster.
Bexhoma still deploys a main pod (called master) as a substitute for a single point of contact and to annotate status of experiments.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [Install CockroachDB](https://www.cockroachlabs.com/docs/v24.2/install-cockroachdb-linux.html)
1. [Deploy CockroachDB in a Single Kubernetes Cluster (Insecure)](https://www.cockroachlabs.com/docs/v24.2/deploy-cockroachdb-with-kubernetes-insecure)
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. [Benchbase Repository](https://github.com/cmu-db/benchbase/wiki/TPC-C)
1. [OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases](http://www.vldb.org/pvldb/vol7/p277-difallah.pdf)
1. Test script of this page: [test-docs-cockroachdb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cockroachdb.sh), [test-docs-cockroachdb.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cockroachdb.ps1)


## Perform YCSB Benchmark

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
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_ycsb_cockroachdb.log
```

This
* starts a clean instance of CockroachDB (`-dbms`) with 3 workers (`-nw`) on the given nodes (`-rnw`) and replication factor 3 (`-nwr`)
  * data directory inside a Docker container
* creates the YCSB schema
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
```

The code `1730133803` is the unique identifier of the experiment.
You can find the number also in the output of the benchmark script.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1730133803` (removes everything that is related to experiment `1730133803`).

### Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cockroachdb_summary.md" target="_blank" rel="noopener">docs_ycsb_cockroachdb.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 463s 
* Code: 1794695469
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
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1047383
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:666729
    * datadisk:2460
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1047383
    * datadisk:2255
    * cpu_list:0-223
  * worker 2
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383563
    * datadisk:2256
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794695469
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Ingestion
* CockroachDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794695469-75fb6f44bd-fls7q: 0
* bx-w-cr-1-1794695469-0: 0
* bx-w-cr-1-1794695469-1: 0
* bx-w-cr-1-1794695469-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2077.97 |                60155.00 |            125000.00 |                              9927.00 | 1.00 |               59.85 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2084.41 |                59969.00 |            125000.00 |                              9887.00 | 1.00 |               60.03 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2102.01 |                59467.00 |            125000.00 |                              9743.00 | 1.00 |               60.54 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2083.75 |                59988.00 |            125000.00 |                              9711.00 | 1.00 |               60.01 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2086.18 |                59918.00 |            125000.00 |                             10015.00 | 1.00 |               60.08 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2102.82 |                59444.00 |            125000.00 |                              9895.00 | 1.00 |               60.56 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2087.12 |                59891.00 |            125000.00 |                              9967.00 | 1.00 |               60.11 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2080.80 |                60073.00 |            125000.00 |                              9967.00 | 1.00 |               59.93 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |               59.85 |                        16705.06 |                60155.00 |           1000000.00 |                              9889.00 |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        14292.45 |                69967.00 |             499806 |                            6955.00 |               500194 |                            123135.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        14292.45 |                69967.00 |             499806 |                            6955.00 |               500194 |                            123135.00 |

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

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).
Metrics are sampled every few seconds, so the benchmarking phase should take at least a minute.
This run uses 10.000.000 operations (`-xop`).

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the CockroachDB cluster.

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
  run &>$LOG_DIR/docs_ycsb_cockroachdb_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cockroachdb_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_cockroachdb_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1150s 
* Code: 1794695948
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
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046242
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:667147
    * datadisk:2490
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1046242
    * datadisk:2257
    * cpu_list:0-223
  * worker 2
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383566
    * datadisk:2259
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794695948
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Ingestion
* CockroachDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794695948-55c5d5487d-sntdn: 0
* bx-w-cr-1-1794695948-0: 0
* bx-w-cr-1-1794695948-1: 0
* bx-w-cr-1-1794695948-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2296.19 |                54438.00 |            125000.00 |                              9623.00 | 1.00 |               66.13 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2287.79 |                54638.00 |            125000.00 |                              9351.00 | 1.00 |               65.89 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2286.49 |                54669.00 |            125000.00 |                              9359.00 | 1.00 |               65.85 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2279.52 |                54836.00 |            125000.00 |                              8895.00 | 1.00 |               65.65 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2297.46 |                54408.00 |            125000.00 |                              9231.00 | 1.00 |               66.17 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2296.78 |                54424.00 |            125000.00 |                              9223.00 | 1.00 |               66.15 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2283.56 |                54739.00 |            125000.00 |                              9479.00 | 1.00 |               65.77 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2282.48 |                54765.00 |            125000.00 |                              9279.00 | 1.00 |               65.74 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |               65.65 |                        18310.27 |                54836.00 |           1000000.00 |                              9305.00 |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        14565.86 |               686537.00 |            4998616 |                            6679.00 |              5001384 |                            115327.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        14565.86 |               686537.00 |            4998616 |                            6679.00 |              5001384 |                            115327.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      1831.72 |     32.10 |           6.36 |                 10.06 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |        82.06 |      1.52 |           0.10 |                  0.10 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     24813.61 |     39.15 |          10.75 |                 25.20 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       643.53 |      1.42 |           0.33 |                  0.33 |

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
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
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

Collecting application metrics for CockroachDB is supported.
It can be activated by `-m -mc -ma`.
Prometheus discovers the worker pods and scrapes the built-in endpoint of CockroachDB (`/_status/vars`, port 8080), with the metric set `cockroachdb` of [cluster.config](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config).
See [Metrics](Example-Metrics.html) for application metrics of all DBMS.

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
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_ycsb_cockroachdb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cockroachdb_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_cockroachdb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 1635s 
* Code: 1794773455
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1064695
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1397428
    * datadisk:11687
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1064695
    * datadisk:11538
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:648328
    * datadisk:11467
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794773455
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Ingestion
* CockroachDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794773455-6d44767854-kx8rm: 0
* bx-w-cr-1-1794773455-0: 0
* bx-w-cr-1-1794773455-1: 0
* bx-w-cr-1-1794773455-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    SF |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2217.59 |               563675.00 |           1250000.00 |                             12751.00 | 10.00 |               63.87 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2209.96 |               565620.00 |           1250000.00 |                             12695.00 | 10.00 |               63.65 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2214.21 |               564535.00 |           1250000.00 |                             12663.00 | 10.00 |               63.77 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2210.10 |               565584.00 |           1250000.00 |                             12543.00 | 10.00 |               63.65 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2215.63 |               564173.00 |           1250000.00 |                             12679.00 | 10.00 |               63.81 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2212.89 |               564871.00 |           1250000.00 |                             12759.00 | 10.00 |               63.73 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2215.68 |               564162.00 |           1250000.00 |                             12599.00 | 10.00 |               63.81 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2225.23 |               561740.00 |           1250000.00 |                             12831.00 | 10.00 |               64.09 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   errors |    SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 10.00 |               63.65 |                        17721.30 |               565620.00 |          10000000.00 |                             12690.00 |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        14199.38 |               704256.00 |            4998021 |                            6395.00 |              5001979 |                            122943.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        14199.38 |               704256.00 |            4998021 |                            6395.00 |              5001979 |                            122943.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     23039.75 |     46.78 |          19.66 |                 47.97 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       834.44 |      1.99 |           0.10 |                  0.10 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     24347.83 |     37.76 |          23.50 |                 47.95 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       765.50 |      1.33 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                    66267.31 |             51295992.67 |                              0.00 |                                      0.00 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                    38181.27 |             28410188.27 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
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
  run &>$LOG_DIR/docs_ycsb_cockroachdb_storage.log
```

Every CockroachDB experiment of the same size will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of CockroachDB mounts the volume and generates the data.
All other instances just use the database without generating and loading data.
Bexhoma uses two types of volumes.
The first volume is attached to the (dummy) coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.
Here, we remove existing storage via `-rsr` to start with a clean copy.

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cockroachdb_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_cockroachdb_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 901s 
* Code: 1794697142
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
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1076544
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381310
    * datadisk:2077
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662475
    * datadisk:1741
    * volume_size:49G
    * volume_used:1.7G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1076544
    * datadisk:1741
    * volume_size:49G
    * volume_used:1.7G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794697142
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-2-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1078020
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662333
    * datadisk:2075
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381310
    * datadisk:2075
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1078069
    * datadisk:2146
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-223
  * worker 3
    * node:cl-worker39
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794697142
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
    * ddl_num_worker_replicas:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: CockroachDB-1-2

### Data Parameters of Reused Volumes
* CockroachDB-1: DDL values of the volume: num_worker_replicas=3, pk_hash=hash, bucket_count=default, range_max_bytes=default, column_families=one, pre_split=none
* CockroachDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Ingestion
* CockroachDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794697142-65f89f577f-479tw: 0
* bx-w-cr-nvme-ycsb-1-0: 0
* bx-w-cr-nvme-ycsb-1-1: 0
* bx-w-cr-nvme-ycsb-1-2: 0
* bexhoma-sut-cockroachdb-1-1794697142-795d64bf77-8km5r: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1769.64 |                70636.00 |            125000.00 |                             11071.00 | 1.00 |               50.97 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1782.81 |                70114.00 |            125000.00 |                             11391.00 | 1.00 |               51.34 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1786.35 |                69975.00 |            125000.00 |                             11375.00 | 1.00 |               51.45 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1771.64 |                70556.00 |            125000.00 |                             11463.00 | 1.00 |               51.02 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1773.33 |                70489.00 |            125000.00 |                             11415.00 | 1.00 |               51.07 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1769.03 |                70660.00 |            125000.00 |                             11279.00 | 1.00 |               50.95 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1782.33 |                70133.00 |            125000.00 |                             11015.00 | 1.00 |               51.33 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1768.88 |                70666.00 |            125000.00 |                             11399.00 | 1.00 |               50.94 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |               50.94 |                        14204.02 |                70666.00 |           1000000.00 |                             11301.00 |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        11327.08 |                88284.00 |             499380 |                            7063.00 |               500620 |                            167935.00 |
| cockroachdb-1-2-1-1-1 | cockroachdb-1-2-1 | cockroachdb-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |    65536 |        0 |                        10252.20 |                97540.00 |             500159 |                            7275.00 |               499841 |                            187647.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        11327.08 |                88284.00 |             499380 |                            7063.00 |               500620 |                            167935.00 |
| cockroachdb-1-2-1 | cockroachdb-1-2-1 |                2 |        1 |               1 |           1 |        64 |    65536 |        0 |                        10252.20 |                97540.00 |             500159 |                            7275.00 |               499841 |                            187647.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      2024.87 |     33.09 |           5.69 |                  9.52 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       112.68 |      1.86 |           0.10 |                  0.10 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      2161.31 |     27.99 |           7.47 |                 12.26 |
| cockroachdb-1-2-1-1 |      1754.17 |     23.92 |           5.31 |                  9.91 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |        65.76 |      1.40 |           0.32 |                  0.32 |
| cockroachdb-1-2-1-1 |        62.36 |      0.75 |           0.31 |                  0.31 |

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
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
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
'CockroachDB': {
    'abbreviation': 'cr',
    'loadData': 'cockroach sql --host {service_name} --port 9091 --insecure --file {scriptname}',
    'delay_prepare': 120,
    'attachWorker': "",
    'template': {
        'version': 'v24.2.4',
        'alias': 'Cloud-Native-2',
        'docker_alias': 'CN2',
        'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["root", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/defaultdb?reWriteBatchedInserts=true&sslmode=disable',
            'jar': 'postgresql-42.5.0.jar',
            'database': 'defaultdb',
            'explain': ['EXPLAIN (VERBOSE) {query}'],
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/cockroach/cockroach-data',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery for worker pods, built-in endpoint /_status/vars on port 8080
},
```

where
* `abbreviation`: short name in the names of volumes and worker pods
* `loadData`: command to create the schema, via `cockroach sql` against the service of bexhoma
* `delay_prepare`: seconds to wait after the cluster is up before the schema is created
* `JDBC`: used to configure YCSB and Benchbase; CockroachDB uses the PostgreSQL JDBC driver
* `monitor`: Prometheus discovery of the worker pods, scraping the built-in endpoint `/_status/vars` on port 8080

### Deployment

* [deploymenttemplate-CockroachDB.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-CockroachDB.yml), derived from the [manifest](https://github.com/cockroachdb/cockroach/blob/master/cloud/kubernetes/cockroachdb-statefulset.yaml) of CockroachDB: the workers are a stateful set, the SUT pod is a placeholder.
* Bexhoma also deploys a service for communication external to CockroachDB (from within the cluster) and a headless service for communication between the pods of the CockroachDB cluster.

### Schema and Scripts

If data should be loaded, bexhoma at first creates a schema. DDL scripts per benchmark:
- [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/CockroachDB)
- [TPC-C](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcc/CockroachDB)

DDL parameters (`-xddl`, see [DDL parameters](DBMS.md#ddl-parameters--xddl)):

| Key | Benchmarks | Values | Default | Effect |
|---|---|---|---|---|
| `num_worker_replicas` | YCSB | integer | `3` | zone num_replicas of usertable (CockroachDB default 3) |
| `pk_hash` | YCSB | `hash`, `none` | `hash` | hash-sharded primary key: spreads sequential inserts (-xio ordered) over ranges, costs range scans (workload e) |
| `bucket_count` | YCSB | `default`, `4`, `8`, `16`, `32`, `64` | `default` | buckets of the hash-sharded primary key (default: cluster setting sql.defaults.default_hash_sharded_index_bucket_count, 16 in v24.2): write spread vs. scan fan-out. Requires `pk_hash` = `hash` |
| `range_max_bytes` | YCSB | `default`, `64MiB`, `128MiB`, `256MiB` | `default` | zone range_max_bytes of usertable (default 512 MiB, range_min_bytes 128 MiB; a smaller value sets range_min_bytes to a quarter): more, smaller ranges spread leaseholders at small data sizes |
| `column_families` | YCSB | `one`, `per_field` | `one` | column families of usertable: one family per row, or one per field, so updating one field writes one KV pair instead of the whole row (workloads a, b, f); costs reads of whole rows |
| `pre_split` | YCSB | `none`, `9`, `90` | `none` | ranges of usertable before the load, split at the first digits of the YCSB keys (hashed insert order): avoids splitting and rebalancing during the load; a hash-sharded key has its buckets instead. Requires `pk_hash` = `none` |

### Load Durability

`-xld` has no effect on CockroachDB: there are no durability scripts for it.

### Reset Scripts

With `-ar`, the reset script `reset-<benchmark>.sql` runs before each benchmarking round:

1. Statistics: `ANALYZE` (cluster-wide)
2. Persist: n/a (Pebble flushes on its own)
3. Counters: `crdb_internal.reset_sql_stats()` (cluster-wide)

See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract and [Test: Reset Scripts](Test-Reset.md) for the test runs, with results for [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_cockroachdb_summary.md), [Benchbase](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_cockroachdb_summary.md).


## YCSB with More Data

YCSB at SF=10, that is 10.000.000 rows (`-sf`), and 10.000.000 operations (`-xop`):

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
  run &>$LOG_DIR/docs_ycsb_cockroachdb_scale.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cockroachdb_scale_summary.md" target="_blank" rel="noopener">docs_ycsb_cockroachdb_scale.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 1584s 
* Code: 1794698093
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1055111
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:677891
    * datadisk:11678
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1392776
    * datadisk:11465
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1055111
    * datadisk:11457
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794698093
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Ingestion
* CockroachDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794698093-55dd585f64-lxccf: 0
* bx-w-cr-1-1794698093-0: 0
* bx-w-cr-1-1794698093-1: 0
* bx-w-cr-1-1794698093-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    SF |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2251.11 |               555282.00 |           1250000.00 |                             12815.00 | 10.00 |               64.83 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2262.73 |               552430.00 |           1250000.00 |                             12903.00 | 10.00 |               65.17 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2256.35 |               553992.00 |           1250000.00 |                             12735.00 | 10.00 |               64.98 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2245.89 |               556573.00 |           1250000.00 |                             12799.00 | 10.00 |               64.68 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2256.92 |               553851.00 |           1250000.00 |                             12855.00 | 10.00 |               65.00 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2260.67 |               552933.00 |           1250000.00 |                             12839.00 | 10.00 |               65.11 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2249.05 |               555789.00 |           1250000.00 |                             12879.00 | 10.00 |               64.77 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         2249.51 |               555677.00 |           1250000.00 |                             12615.00 | 10.00 |               64.79 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   errors |    SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 10.00 |               64.68 |                        18032.24 |               556573.00 |          10000000.00 |                             12805.00 |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        15485.70 |               645757.00 |            4999515 |                            6043.00 |              5000485 |                            101567.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        15485.70 |               645757.00 |            4999515 |                            6043.00 |              5000485 |                            101567.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     21246.91 |     46.57 |          22.15 |                 53.14 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      1018.96 |      2.74 |           0.10 |                  0.10 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     22204.04 |     39.26 |          24.44 |                 67.66 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       784.82 |      1.57 |           0.34 |                  0.34 |

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
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## Benchbase's TPC-C

The setup is the same as for YCSB (see above).

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
  run &>$LOG_DIR/docs_benchbase_cockroachdb.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_cockroachdb_summary.md" target="_blank" rel="noopener">docs_benchbase_cockroachdb.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1164s 
* Code: 1794699720
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045940
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383819
    * datadisk:2507
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:666318
    * datadisk:2297
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1045940
    * datadisk:2296
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794699720
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046214
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384092
    * datadisk:2779
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:666702
    * datadisk:2567
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1046214
    * datadisk:2568
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794699720
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* CockroachDB-1: skipped initschema-benchbase.sql

### Ingestion
* CockroachDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794699720-65457d676b-zdcvt: 0
* bx-w-cr-1-1794699720-0: 0
* bx-w-cr-1-1794699720-1: 0
* bx-w-cr-1-1794699720-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS            |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |   16 |      196.00 |           1.00 |            0.00 |        192.00 |            3.00 |              1 |         1 |             | None           |             0 | False         |              293.88 | False               |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         435.81 |                      433.89 |         0.00 |                                                      93891.00 |                                              36688.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                         194.85 |                      194.00 |         0.00 |                                                     103486.00 |                                              41029.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        0 |                         216.83 |                      215.95 |         0.00 |                                                     101070.00 |                                              36870.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         435.81 |                      433.89 |         0.00 |                                                      93891.00 |                                              36688.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        0 |                         411.68 |                      409.95 |         0.00 |                                                     103486.00 |                                              38949.50 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

### More Complex Run

TPC-C is performed at 128 warehouses.
The 1280 threads of the client are split into a cascading sequence of 1, 2, 4 and 8 pods.
This run also collects application metrics (`-ma`).

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
  run &>$LOG_DIR/docs_benchbase_cockroachdb_scale.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_cockroachdb_scale_summary.md" target="_blank" rel="noopener">docs_benchbase_cockroachdb_scale.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 4589s 
* Code: 1794700900
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1185955
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:673180
    * datadisk:10024
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1391243
    * datadisk:9926
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1185985
    * datadisk:9738
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794700900
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1193840
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:676146
    * datadisk:12979
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1394076
    * datadisk:12758
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1193932
    * datadisk:12776
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794700900
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1198525
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:678563
    * datadisk:15387
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1396480
    * datadisk:15162
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1198525
    * datadisk:15195
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794700900
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1200427
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:680514
    * datadisk:17320
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1398399
    * datadisk:17081
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1200431
    * datadisk:17097
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794700900
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* CockroachDB-1: skipped initschema-benchbase.sql

### Ingestion
* CockroachDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794700900-586d54c45c-ntw59: 0
* bx-w-cr-1-1794700900-0: 0
* bx-w-cr-1-1794700900-1: 0
* bx-w-cr-1-1794700900-2: 0

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

| DBMS            |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |  128 |     1608.00 |           1.00 |            0.00 |       1604.00 |            3.00 |              1 |         1 |             | None           |             0 | False         |              286.57 | False               |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2985.80 |                     2974.32 |         0.00 |                                                    1079972.00 |                                             428222.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       1 |       640 |     8192 |          -1 | 600.00 |        0 |                        1485.75 |                     1479.92 |         0.00 |                                                    1116480.00 |                                             430350.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       2 |       640 |     8192 |          -1 | 600.00 |        0 |                        1483.92 |                     1478.16 |         0.00 |                                                    1117800.00 |                                             431160.00 |
| cockroachdb-1-1-3-1-1 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       1 |       320 |     4096 |          -1 | 600.00 |        0 |                         725.66 |                      722.82 |         0.00 |                                                    1547691.00 |                                             440437.00 |
| cockroachdb-1-1-3-1-2 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       2 |       320 |     4096 |          -1 | 600.00 |        0 |                         724.00 |                      721.16 |         0.00 |                                                    1549123.00 |                                             441720.00 |
| cockroachdb-1-1-3-1-3 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       3 |       320 |     4096 |          -1 | 600.00 |        0 |                         720.65 |                      717.71 |         0.00 |                                                    1550585.00 |                                             443707.00 |
| cockroachdb-1-1-3-1-4 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       4 |       320 |     4096 |          -1 | 600.00 |        0 |                         722.13 |                      719.22 |         0.00 |                                                    1554894.00 |                                             442773.00 |
| cockroachdb-1-1-4-1-1 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       1 |       160 |     2048 |          -1 | 600.00 |        0 |                         340.34 |                      338.86 |         0.00 |                                                    1870724.00 |                                             469658.00 |
| cockroachdb-1-1-4-1-2 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       2 |       160 |     2048 |          -1 | 600.00 |        0 |                         343.87 |                      342.34 |         0.00 |                                                    1854932.00 |                                             465146.00 |
| cockroachdb-1-1-4-1-3 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       3 |       160 |     2048 |          -1 | 600.00 |        0 |                         343.19 |                      341.71 |         0.00 |                                                    1859900.00 |                                             465830.00 |
| cockroachdb-1-1-4-1-4 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       4 |       160 |     2048 |          -1 | 600.00 |        0 |                         341.11 |                      339.70 |         0.00 |                                                    1868516.00 |                                             468350.00 |
| cockroachdb-1-1-4-1-5 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       5 |       160 |     2048 |          -1 | 600.00 |        0 |                         345.48 |                      343.98 |         0.00 |                                                    1849422.00 |                                             462361.00 |
| cockroachdb-1-1-4-1-6 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       6 |       160 |     2048 |          -1 | 600.00 |        0 |                         342.12 |                      340.63 |         0.00 |                                                    1864028.00 |                                             467444.00 |
| cockroachdb-1-1-4-1-7 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       7 |       160 |     2048 |          -1 | 600.00 |        0 |                         343.88 |                      342.43 |         0.00 |                                                    1849495.00 |                                             464580.00 |
| cockroachdb-1-1-4-1-8 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       8 |       160 |     2048 |          -1 | 600.00 |        0 |                         338.34 |                      336.84 |         0.00 |                                                    1869567.00 |                                             472164.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2985.80 |                     2974.32 |         0.00 |                                                    1079972.00 |                                             428222.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        2 |               1 |           2 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2969.68 |                     2958.08 |         0.00 |                                                    1117800.00 |                                             430755.00 |
| cockroachdb-1-1-3 | cockroachdb-1-1-3 |                1 |        3 |               1 |           4 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2892.45 |                     2880.92 |         0.00 |                                                    1554894.00 |                                             442159.25 |
| cockroachdb-1-1-4 | cockroachdb-1-1-4 |                1 |        4 |               1 |           8 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2738.34 |                     2726.48 |         0.00 |                                                    1870724.00 |                                             466941.62 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     15757.80 |     43.71 |          24.70 |                 54.84 |
| cockroachdb-1-1-2-1 |     15757.80 |     43.71 |          24.70 |                 54.84 |
| cockroachdb-1-1-3-1 |     15757.80 |     43.71 |          24.70 |                 54.84 |
| cockroachdb-1-1-4-1 |     15757.80 |     43.71 |          24.70 |                 54.84 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |    172985.97 |    118.95 |           0.39 |                  0.39 |
| cockroachdb-1-1-2-1 |    172985.97 |    118.95 |           0.39 |                  0.39 |
| cockroachdb-1-1-3-1 |    172985.97 |    118.95 |           0.39 |                  0.39 |
| cockroachdb-1-1-4-1 |    172985.97 |    118.95 |           0.39 |                  0.39 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |    106843.22 |    191.72 |          35.15 |                 69.67 |
| cockroachdb-1-1-2-1 |    109186.03 |    185.85 |          36.16 |                 77.01 |
| cockroachdb-1-1-3-1 |    108797.93 |    186.03 |          40.54 |                 87.93 |
| cockroachdb-1-1-4-1 |    108491.63 |    185.24 |          45.49 |                 97.88 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      2279.51 |      4.63 |           4.28 |                  4.28 |
| cockroachdb-1-1-2-1 |      2571.23 |      5.36 |           2.99 |                  2.99 |
| cockroachdb-1-1-3-1 |      2735.73 |      5.37 |           1.84 |                  1.84 |
| cockroachdb-1-1-4-1 |      3019.51 |     10.44 |           1.47 |                  1.47 |

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
| cockroachdb-1-1-1-1 |                                     5953.31 |             36435403.00 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                     5953.31 |             36435403.00 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-3-1 |                                     5953.31 |             36435403.00 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-4-1 |                                     5953.31 |             36435403.00 |                              0.00 |                                      0.00 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                   152605.64 |             60621460.94 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                   154392.77 |             60664622.23 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-3-1 |                                   157217.72 |             61356218.70 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-4-1 |                                   159404.12 |             62394968.73 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

### With Persistent Storage

The same on persistent storage (`-rst`), removing an existing volume first (`-rsr`):

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
  run &>$LOG_DIR/docs_benchbase_cockroachdb_scale_storage.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_cockroachdb_scale_storage_summary.md" target="_blank" rel="noopener">docs_benchbase_cockroachdb_scale_storage.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 4625s 
* Code: 1794705531
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1044397
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381323
    * datadisk:9938
    * volume_size:98G
    * volume_used:9.8G
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1044397
    * datadisk:9706
    * volume_size:98G
    * volume_used:9.5G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662999
    * datadisk:9774
    * volume_size:98G
    * volume_used:9.6G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794705531
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045212
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381324
    * datadisk:12752
    * volume_size:98G
    * volume_used:13G
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1045212
    * datadisk:12539
    * volume_size:98G
    * volume_used:13G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:663011
    * datadisk:12536
    * volume_size:98G
    * volume_used:13G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794705531
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045205
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381325
    * datadisk:14888
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1045205
    * datadisk:14668
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:663022
    * datadisk:14660
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794705531
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045208
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381326
    * datadisk:17985
    * volume_size:98G
    * volume_used:18G
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1045208
    * datadisk:16474
    * volume_size:98G
    * volume_used:17G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:663051
    * datadisk:16499
    * volume_size:98G
    * volume_used:17G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794705531
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* CockroachDB-1: skipped initschema-benchbase.sql

### Ingestion
* CockroachDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794705531-bd5b6b5b5-gn59l: 0
* bx-w-cr-nvme-benchbase-tpcc-128-0: 0
* bx-w-cr-nvme-benchbase-tpcc-128-1: 0
* bx-w-cr-nvme-benchbase-tpcc-128-2: 0

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

| DBMS            |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |  128 |     1713.00 |           2.00 |            0.00 |       1707.00 |            4.00 |              1 |         1 |             | None           |             0 | False         |              269.00 | False               |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2871.62 |                     2847.70 |         0.00 |                                                    2355994.00 |                                             444720.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       1 |       640 |     8192 |          -1 | 600.00 |        0 |                        1399.20 |                     1391.18 |         0.00 |                                                    2365752.00 |                                             456580.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       2 |       640 |     8192 |          -1 | 600.00 |        0 |                        1403.20 |                     1395.22 |         0.00 |                                                    2365486.00 |                                             455616.00 |
| cockroachdb-1-1-3-1-1 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       1 |       320 |     4096 |          -1 | 600.00 |        0 |                         661.60 |                      658.56 |         0.00 |                                                    2139641.00 |                                             482960.00 |
| cockroachdb-1-1-3-1-2 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       2 |       320 |     4096 |          -1 | 600.00 |        0 |                         663.23 |                      660.18 |         0.00 |                                                    2138966.00 |                                             482021.00 |
| cockroachdb-1-1-3-1-3 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       3 |       320 |     4096 |          -1 | 600.00 |        0 |                         665.87 |                      662.76 |         0.00 |                                                    2145533.00 |                                             480138.00 |
| cockroachdb-1-1-3-1-4 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       4 |       320 |     4096 |          -1 | 600.00 |        0 |                         660.88 |                      657.77 |         0.00 |                                                    2144677.00 |                                             483755.00 |
| cockroachdb-1-1-4-1-1 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       1 |       160 |     2048 |          -1 | 600.00 |        0 |                         330.61 |                      328.95 |         0.00 |                                                    1947662.00 |                                             483412.00 |
| cockroachdb-1-1-4-1-2 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       2 |       160 |     2048 |          -1 | 600.00 |        0 |                         332.23 |                      330.60 |         0.00 |                                                    1955637.00 |                                             481499.00 |
| cockroachdb-1-1-4-1-3 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       3 |       160 |     2048 |          -1 | 600.00 |        0 |                         329.79 |                      328.18 |         0.00 |                                                    1957572.00 |                                             484657.00 |
| cockroachdb-1-1-4-1-4 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       4 |       160 |     2048 |          -1 | 600.00 |        0 |                         330.58 |                      329.02 |         0.00 |                                                    1956024.00 |                                             483616.00 |
| cockroachdb-1-1-4-1-5 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       5 |       160 |     2048 |          -1 | 600.00 |        0 |                         331.43 |                      329.90 |         0.00 |                                                    1951266.00 |                                             482269.00 |
| cockroachdb-1-1-4-1-6 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       6 |       160 |     2048 |          -1 | 600.00 |        0 |                         329.69 |                      328.11 |         0.00 |                                                    1958370.00 |                                             484851.00 |
| cockroachdb-1-1-4-1-7 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       7 |       160 |     2048 |          -1 | 600.00 |        0 |                         331.57 |                      329.85 |         0.00 |                                                    1948739.00 |                                             482145.00 |
| cockroachdb-1-1-4-1-8 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       8 |       160 |     2048 |          -1 | 600.00 |        0 |                         330.99 |                      329.50 |         0.00 |                                                    1951355.00 |                                             482870.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2871.62 |                     2847.70 |         0.00 |                                                    2355994.00 |                                             444720.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        2 |               1 |           2 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2802.41 |                     2786.40 |         0.00 |                                                    2365752.00 |                                             456098.00 |
| cockroachdb-1-1-3 | cockroachdb-1-1-3 |                1 |        3 |               1 |           4 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2651.57 |                     2639.28 |         0.00 |                                                    2145533.00 |                                             482218.50 |
| cockroachdb-1-1-4 | cockroachdb-1-1-4 |                1 |        4 |               1 |           8 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2646.89 |                     2634.12 |         0.00 |                                                    1958370.00 |                                             483164.88 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     15791.25 |     44.63 |          21.95 |                 47.21 |
| cockroachdb-1-1-2-1 |     15791.25 |     44.63 |          21.95 |                 47.21 |
| cockroachdb-1-1-3-1 |     15791.25 |     44.63 |          21.95 |                 47.21 |
| cockroachdb-1-1-4-1 |     15791.25 |     44.63 |          21.95 |                 47.21 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |    188831.13 |    121.08 |           0.36 |                  0.36 |
| cockroachdb-1-1-2-1 |    188831.13 |    121.08 |           0.36 |                  0.36 |
| cockroachdb-1-1-3-1 |    188831.13 |    121.08 |           0.36 |                  0.36 |
| cockroachdb-1-1-4-1 |    188831.13 |    121.08 |           0.36 |                  0.36 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |    104697.97 |    191.46 |          34.68 |                 67.63 |
| cockroachdb-1-1-2-1 |    105556.06 |    181.41 |          37.53 |                 77.59 |
| cockroachdb-1-1-3-1 |    100791.74 |    177.42 |          39.31 |                 84.37 |
| cockroachdb-1-1-4-1 |    104238.23 |    177.56 |          39.88 |                 92.12 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      2242.13 |      7.94 |           4.25 |                  4.25 |
| cockroachdb-1-1-2-1 |      2422.76 |      7.57 |           3.57 |                  3.57 |
| cockroachdb-1-1-3-1 |      2333.41 |      4.20 |           2.07 |                  2.07 |
| cockroachdb-1-1-4-1 |      2903.18 |      7.00 |           1.57 |                  1.57 |

### Missing Monitoring Metrics
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
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
| cockroachdb-1-1-1-1 |                                     7933.31 |             47190224.72 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                     7933.31 |             47190224.72 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-3-1 |                                     7933.31 |             47190224.72 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-4-1 |                                     7933.31 |             47190224.72 |                              0.00 |                                      0.00 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                   153131.36 |             58223903.91 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                   153833.04 |             58673019.62 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-3-1 |                                   152963.29 |             58051039.01 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-4-1 |                                   154448.71 |             59590821.83 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

### Application Metrics

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
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_benchbase_cockroachdb_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_cockroachdb_appmetrics_summary.md" target="_blank" rel="noopener">docs_benchbase_cockroachdb_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1230s 
* Code: 1794775134
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1057984
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1388334
    * datadisk:2500
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:639026
    * datadisk:2433
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1058005
    * datadisk:2296
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794775134
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1055714
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1388623
    * datadisk:2786
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:639307
    * datadisk:2712
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1055714
    * datadisk:2573
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794775134
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* CockroachDB-1: skipped initschema-benchbase.sql

### Ingestion
* CockroachDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794775134-7458d645fd-ghjc6: 0
* bx-w-cr-1-1794775134-0: 0
* bx-w-cr-1-1794775134-1: 0
* bx-w-cr-1-1794775134-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS            |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |   16 |      228.00 |           1.00 |            0.00 |        223.00 |            4.00 |              1 |         1 |             | None           |             0 | False         |              252.63 | False               |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         435.88 |                      433.91 |         0.00 |                                                      92361.00 |                                              36687.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                         193.12 |                      192.29 |         0.00 |                                                     101845.00 |                                              41395.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        0 |                         188.36 |                      187.49 |         0.00 |                                                     103613.00 |                                              42443.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         435.88 |                      433.91 |         0.00 |                                                      92361.00 |                                              36687.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        0 |                         381.49 |                      379.78 |         0.00 |                                                     103613.00 |                                              41919.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      3347.01 |     25.29 |           7.98 |                 11.57 |
| cockroachdb-1-1-2-1 |      3347.01 |     25.29 |           7.98 |                 11.57 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       854.40 |     12.16 |           0.27 |                  0.27 |
| cockroachdb-1-1-2-1 |       854.40 |     12.16 |           0.27 |                  0.27 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      7217.51 |     26.23 |           8.61 |                 12.80 |
| cockroachdb-1-1-2-1 |      6606.97 |     23.62 |           8.72 |                 13.67 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       305.37 |      1.31 |           0.32 |                  0.32 |
| cockroachdb-1-1-2-1 |       303.92 |      1.34 |           0.27 |                  0.27 |

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

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                     1235.25 |             12206491.00 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                     1235.25 |             12206491.00 |                              0.00 |                                      0.00 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                    24365.21 |             12204661.27 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                    21419.36 |              8707094.30 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>
