# Example: Benchmark TiDB

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.
TiDB is a disaggregated DBMS.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TiDB offers several installation methods, including an operator [1].
We here rely on a [manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-TiDB.yml) for a version that is suitable for bexhoma.
TiDB clusters consist of three core components: TiDB, PD (Placement Driver), and TiKV.
Unlike traditional databases, TiDB does not require a single coordinator node - PD handles cluster metadata management and scheduling.
In Bexhoma, TiDB pods are deployed as a Deployment, PD as a StatefulSet, and TiKV as another StatefulSet to ensure stable identities and persistent storage.
A Kubernetes Service exposes TiDB for external communication within the cluster, while headless Services enable internal discovery and communication between PD and TiKV pods.

This can be managed by bexhoma.

## Scaling TiDB Components

TiDB has three independently deployed components, and bexhoma exposes an independent scaling flag for each of them:

| Component | Kubernetes kind | Flag | Default | Notes |
|---|---|---|---|---|
| TiKV (storage) | StatefulSet, `component: tikv` | `-nw` / `--num-worker` | 0 | The storage/sharding layer - this is the "worker" count used for every distributed DBMS in bexhoma. |
| PD (Placement Driver) | StatefulSet, `component: pd` | `-xnpd` / `--xnum-pd-nodes` | 3 | Cluster metadata/scheduling nodes. Sized independently of `-nw`, since PD and TiKV serve different roles and typically need different counts (PD is usually kept at a small odd number for quorum, e.g. 3 or 5; TiKV scales with storage/throughput needs). |
| TiDB server (SQL frontend) | Deployment, `component: sut` | `-xnsr` / `--xnum-sut-replicas` | 1 | Stateless SQL frontend; scales independently of storage. |

Example: `-nw 6 -xnpd 3 -xnsr 2` deploys 6 TiKV nodes, 3 PD nodes, and 2 `tidb-server` pods.

Two more scaling-related flags exist but are **not** pod-count knobs for TiDB:
* `-nwr` / `--num-worker-replicas` sets PD's `max-replicas` raft configuration (`SET CONFIG pd max-replicas = {num_worker_replicas}`, run once as part of the init schema) - the number of Raft replicas TiKV keeps per data region, a data-durability setting independent of how many TiKV/PD pods are actually running. It is exposed as `BEXHOMA_REPLICAS` on the SUT pods and in the eval summary, but no container in the TiDB manifest uses it as a pod count.
* `-nws` / `--num-worker-shards` currently has **no effect** for TiDB - it's a DDL parameter only wired up for Citus (`SET citus.shard_count = ...`). It is still parsed (shared across all entry scripts) but the TiDB init schema does not reference it.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Get started with TiDB:  https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/
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
  -dbms TiDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xnsr 3 \
  -nw 3 \
  -xnpd 3 \
  -nwr 3 \
  -xop 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_ycsb_tidb_1.log
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of TiDB (`-dbms`) with 3 TiKV nodes (`-nw`), 3 PD nodes (`-xnpd`), 3 tidb-server pods (`-xnsr`), and a PD raft replication factor of 3 (`-nwr`) - see [Scaling TiDB Components](#scaling-tidb-components)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=10, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [1]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 1.000.000 operations (`-xop`)
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
+-----------------+--------------+--------------+------------+-------------+
| 1761748555      | sut          |   loaded [s] | use case   | worker      |
+=================+==============+==============+============+=============+
| TiDB-64-8-16384 | (1. Running) |          409 | ycsb       | (3 Running) |
+-----------------+--------------+--------------+------------+-------------+
```

The code `1761748555` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1761748555` (removes everything that is related to experiment `1761748555`).

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_tidb_1_summary.md" target="_blank" rel="noopener">docs_ycsb_tidb_1.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 540s 
* Code: 1792416543
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Experiment uses bexhoma version 0.11.7.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
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
* tidb-1-1-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:580770
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
    * disk:580770
    * cpu_list:0-127
  * sut 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161052
    * cpu_list:0-127
  * sut 2
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:172487
    * cpu_list:0-95
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:580770
    * datadisk:123
    * cpu_list:0-127
  * pd 1
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:847447
    * datadisk:123
    * cpu_list:0-223
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:349185
    * datadisk:123
    * cpu_list:0-127
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:580770
    * datadisk:11934
    * cpu_list:0-127
  * tikv 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:349186
    * datadisk:21040
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:847817
    * datadisk:20931
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * eval_parameters
    * code:1792416543
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-tidb-1-1792416543-6b46755454-p77t8: 0
* bexhoma-sut-tidb-1-1792416543-6b46755454-qsnpr: 0
* bexhoma-sut-tidb-1-1792416543-6b46755454-tgzpx: 0
* bexhoma-pd-tidb-ycsb-1-0: 0
* bexhoma-pd-tidb-ycsb-1-1: 0
* bexhoma-pd-tidb-ycsb-1-2: 0
* bexhoma-tikv-tidb-ycsb-1-0: 0
* bexhoma-tikv-tidb-ycsb-1-1: 0
* bexhoma-tikv-tidb-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection     |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| tidb-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2017.01 |                61973.00 |            125000.00 |                             14015.00 | 1.00 |               58.09 |
| tidb-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2033.35 |                61475.00 |            125000.00 |                             13407.00 | 1.00 |               58.56 |
| tidb-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2009.65 |                62200.00 |            125000.00 |                             13839.00 | 1.00 |               57.88 |
| tidb-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2011.98 |                62128.00 |            125000.00 |                             14103.00 | 1.00 |               57.94 |
| tidb-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2017.89 |                61946.00 |            125000.00 |                             14151.00 | 1.00 |               58.12 |
| tidb-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2011.72 |                62136.00 |            125000.00 |                             13855.00 | 1.00 |               57.94 |
| tidb-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2013.11 |                62093.00 |            125000.00 |                             13471.00 | 1.00 |               57.98 |
| tidb-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2009.90 |                62192.00 |            125000.00 |                             13903.00 | 1.00 |               57.89 |

#### Per Run

| DBMS     |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               57.88 |                        16124.59 |                62200.00 |           1000000.00 |                             13843.00 |

### Benchmarking

#### Per Connection

| DBMS           | phase      | job          | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:-----------|:-------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 | TiDB-1          |                1 |        1 |               1 |       1 |        64 |    16384 |           1 |            0 |                        16263.07 |                61489.00 |             500138 |                            2449.00 |               499862 |                             26383.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------|:-----------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |        64 |    16384 |               1 |           1 |            0 |                        16263.07 |                61489.00 |             500138 |                            2449.00 |               499862 |                             26383.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       947.41 |     15.43 |           1.09 |                  1.62 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        43.67 |      0.55 |           0.21 |                  0.22 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       869.88 |     14.60 |           8.28 |                 17.26 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        93.21 |      1.57 |           0.21 |                  0.22 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       581.30 |     13.23 |           1.83 |                  2.37 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        23.65 |      0.54 |           0.22 |                  0.22 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      1027.81 |     18.69 |          10.19 |                 22.56 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        76.18 |      1.24 |           0.57 |                  0.58 |

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

### Tests
* TEST passed: Loading measured in this experiment
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
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

To see the summary again you can simply call `bexhoma summary -e 1761748555` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888




## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components of the same type.
In this example, this means that used memory, CPU time, etc. are summed across all nodes of the TiDB cluster for the components PD, TiKV and TiDB resp.

### Application Metrics

Collecting application metrics for TiDB is supported.
It can be activated by `-m -mc -ma`.
Metrics are defined per component: the tidb-server pods (SUT deployment), PD and TiKV.
See [example configuration](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config) for the definitions and [Metrics](Example-Metrics.html) for more examples.

```bash
bexhoma ycsb \
  -dbms TiDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xnsr 3 \
  -nw 3 \
  -xnpd 3 \
  -nwr 3 \
  -xop 1 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_ycsb_tidb_3.log
```

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_tidb_3_summary.md" target="_blank" rel="noopener">docs_ycsb_tidb_3.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 574s 
* Code: 1792418486
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Experiment uses bexhoma version 0.11.7.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
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
* tidb-1-1-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:540579299328
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker22
  * disk:161066
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161066
    * cpu_list:0-127
  * sut 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:584593
    * cpu_list:0-127
  * sut 2
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:170937
    * cpu_list:0-95
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:584593
    * datadisk:123
    * cpu_list:0-127
  * pd 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:349157
    * datadisk:123
    * cpu_list:0-127
  * pd 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:847541
    * datadisk:123
    * cpu_list:0-223
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:584593
    * datadisk:11984
    * cpu_list:0-127
  * tikv 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:349157
    * datadisk:21011
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:847542
    * datadisk:20991
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * eval_parameters
    * code:1792418486
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-tidb-1-1792418486-54ddb58c66-cx8t9: 0
* bexhoma-sut-tidb-1-1792418486-54ddb58c66-ggt86: 0
* bexhoma-sut-tidb-1-1792418486-54ddb58c66-vf6c2: 0
* bexhoma-pd-tidb-ycsb-1-0: 0
* bexhoma-pd-tidb-ycsb-1-1: 0
* bexhoma-pd-tidb-ycsb-1-2: 0
* bexhoma-tikv-tidb-ycsb-1-0: 0
* bexhoma-tikv-tidb-ycsb-1-1: 0
* bexhoma-tikv-tidb-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection     |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| tidb-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1759.92 |                71026.00 |            125000.00 |                             15447.00 | 1.00 |               50.69 |
| tidb-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1764.89 |                70826.00 |            125000.00 |                             15591.00 | 1.00 |               50.83 |
| tidb-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1758.09 |                71100.00 |            125000.00 |                             15495.00 | 1.00 |               50.63 |
| tidb-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1745.83 |                71599.00 |            125000.00 |                             15223.00 | 1.00 |               50.28 |
| tidb-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1747.30 |                71539.00 |            125000.00 |                             15415.00 | 1.00 |               50.32 |
| tidb-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1755.22 |                71216.00 |            125000.00 |                             15751.00 | 1.00 |               50.55 |
| tidb-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1760.29 |                71011.00 |            125000.00 |                             15695.00 | 1.00 |               50.70 |
| tidb-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1762.97 |                70903.00 |            125000.00 |                             15607.00 | 1.00 |               50.77 |

#### Per Run

| DBMS     |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               50.28 |                        14054.51 |                71599.00 |           1000000.00 |                             15528.00 |

### Benchmarking

#### Per Connection

| DBMS           | phase      | job          | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:-----------|:-------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 | TiDB-1          |                1 |        1 |               1 |       1 |        64 |    16384 |           1 |            0 |                        12444.62 |                80356.00 |             499694 |                            3063.00 |               500306 |                            131071.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------|:-----------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |        64 |    16384 |               1 |           1 |            0 |                        12444.62 |                80356.00 |             499694 |                            3063.00 |               500306 |                            131071.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       927.39 |     13.67 |           1.74 |                  2.27 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        80.83 |      0.98 |           0.22 |                  0.22 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       777.68 |     10.67 |           8.24 |                 16.75 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        82.93 |      1.52 |           0.33 |                  0.33 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       711.76 |     11.83 |           2.03 |                  2.57 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        49.57 |      1.03 |           0.22 |                  0.22 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       732.08 |     12.16 |           9.86 |                 22.48 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        56.37 |      1.08 |           0.55 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* PD Leader Balance Actions [count] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-pdbenchmarking.log)
* PD Leader Balance Actions [count] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-pdloading.log)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS         |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration since Start [ms] |
|:-------------|----------------------------------------:|-------------------------------------------:|
| tidb-1-1-1-1 |                                 4031.89 |                                       4.19 |

#### Loading phase: component pd

| DBMS         |   PD Cluster Leader Count |   PD Leader Balance Actions [count] |
|:-------------|--------------------------:|------------------------------------:|
| tidb-1-1-1-1 |                     22.00 |                                0.00 |

#### Loading phase: component tikv

| DBMS         |   TiKV Store Size Used [GiB] |   TiKV Store Used [%] |   TiKV Compaction Time Median, Max over Instances [s] |   TiKV Compaction Flow [GiB] |   TiKV Compaction Pending [GiB] |
|:-------------|-----------------------------:|----------------------:|------------------------------------------------------:|-----------------------------:|--------------------------------:|
| tidb-1-1-1-1 |                        50.54 |                  1.15 |                                                  1.90 |                         7.17 |                            0.48 |

#### Benchmarking phase: SUT deployment

| DBMS         |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration since Start [ms] |
|:-------------|----------------------------------------:|-------------------------------------------:|
| tidb-1-1-1-1 |                                 6063.76 |                                       4.45 |

#### Benchmarking phase: component pd

| DBMS         |   PD Cluster Leader Count |   PD Leader Balance Actions [count] |
|:-------------|--------------------------:|------------------------------------:|
| tidb-1-1-1-1 |                     22.00 |                                0.00 |

#### Benchmarking phase: component tikv

| DBMS         |   TiKV Store Size Used [GiB] |   TiKV Store Used [%] |   TiKV Compaction Time Median, Max over Instances [s] |   TiKV Compaction Flow [GiB] |   TiKV Compaction Pending [GiB] |
|:-------------|-----------------------------:|----------------------:|------------------------------------------------------:|-----------------------------:|--------------------------------:|
| tidb-1-1-1-1 |                        52.08 |                  1.18 |                                                  0.00 |                         0.94 |                            0.48 |

### Tests
* TEST passed: Loading measured in this experiment
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
* TEST failed: Monitoring metrics missing
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

Example:
```bash
bexhoma ycsb \
  -dbms TiDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xnsr 3 \
  -nw 3 \
  -xnpd 3 \
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
  -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_ycsb_tidb_2.log
```

TiDB keeps its data in the PD and TiKV StatefulSets, so each of their pods gets a volume of the requested class and size (`-rst`, `-rss`).
The tidb-server pods are stateless and get no volume.
The name of each volume contains the storage class, so data loaded on one storage class is never reused on another.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of TiDB mounts the volumes and loads the data.
The second instance reuses the volumes and skips loading.
Here, we remove existing storage via `-rsr` to start with a clean copy.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_tidb_2_summary.md" target="_blank" rel="noopener">docs_ycsb_tidb_2.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1241s 
* Code: 1792417158
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Experiment uses bexhoma version 0.11.7.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
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
* tidb-1-1-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:540590800896
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker24
  * disk:172622
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:172524
    * cpu_list:0-95
  * sut 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:568717
    * cpu_list:0-127
  * sut 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161057
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:568717
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:328024
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:826405
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-223
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:568717
    * datadisk:4179
    * volume_size:49G
    * volume_used:4.1G
    * cpu_list:0-127
  * tikv 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:328024
    * datadisk:3980
    * volume_size:49G
    * volume_used:3.9G
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:826406
    * datadisk:3991
    * volume_size:49G
    * volume_used:3.9G
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * eval_parameters
    * code:1792417158
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-2-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:540590800896
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker24
  * disk:170919
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:172480
    * cpu_list:0-95
  * sut 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161061
    * cpu_list:0-127
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:568717
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:568717
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:826416
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
    * disk:328024
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
    * disk:568717
    * datadisk:4182
    * volume_size:49G
    * volume_used:4.1G
    * cpu_list:0-127
  * tikv 1
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:826416
    * datadisk:4165
    * volume_size:49G
    * volume_used:4.1G
    * cpu_list:0-223
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:328024
    * datadisk:4158
    * volume_size:49G
    * volume_used:4.1G
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * eval_parameters
    * code:1792417158
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: TiDB-1-2

### SUT Container Restarts
* bexhoma-sut-tidb-1-1792417158-68c466bb8c-b9sj8: 0
* bexhoma-sut-tidb-1-1792417158-68c466bb8c-spw76: 0
* bexhoma-sut-tidb-1-1792417158-68c466bb8c-tphv7: 0
* bexhoma-pd-tidb-nvme-ycsb-1-0: 0
* bexhoma-pd-tidb-nvme-ycsb-1-1: 0
* bexhoma-pd-tidb-nvme-ycsb-1-2: 0
* bexhoma-tikv-tidb-nvme-ycsb-1-0: 0
* bexhoma-tikv-tidb-nvme-ycsb-1-1: 0
* bexhoma-tikv-tidb-nvme-ycsb-1-2: 0
* bexhoma-sut-tidb-1-1792417158-784b6598b5-57p47: 0
* bexhoma-sut-tidb-1-1792417158-784b6598b5-8s5mp: 0
* bexhoma-sut-tidb-1-1792417158-784b6598b5-9p62r: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS TiDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS TiDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection     |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| tidb-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1029.91 |               121370.00 |            125000.00 |                             11719.00 | 1.00 |               29.66 |
| tidb-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1028.92 |               121487.00 |            125000.00 |                             12071.00 | 1.00 |               29.63 |
| tidb-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1031.45 |               121189.00 |            125000.00 |                             11967.00 | 1.00 |               29.71 |
| tidb-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1025.60 |               121880.00 |            125000.00 |                             12263.00 | 1.00 |               29.54 |
| tidb-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1030.35 |               121318.00 |            125000.00 |                             11959.00 | 1.00 |               29.67 |
| tidb-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1031.52 |               121180.00 |            125000.00 |                             11863.00 | 1.00 |               29.71 |
| tidb-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1027.61 |               121642.00 |            125000.00 |                             12207.00 | 1.00 |               29.60 |
| tidb-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         1027.84 |               121614.00 |            125000.00 |                             12407.00 | 1.00 |               29.60 |

#### Per Run

| DBMS     |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               29.54 |                         8233.19 |               121880.00 |           1000000.00 |                             12057.00 |

### Benchmarking

#### Per Connection

| DBMS           | phase      | job          | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:-----------|:-------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 | TiDB-1          |                1 |        1 |               1 |       1 |        64 |    16384 |           1 |            0 |                         7963.24 |               125577.00 |             499994 |                            5499.00 |               500006 |                            213375.00 |
| tidb-1-2-1-1-1 | tidb-1-2-1 | tidb-1-2-1-1 | TiDB-1          |                2 |        1 |               1 |       1 |        64 |    16384 |           1 |            0 |                         8009.68 |               124849.00 |             499298 |                            5643.00 |               500702 |                            237439.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------|:-----------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |        64 |    16384 |               1 |           1 |            0 |                         7963.24 |               125577.00 |             499994 |                            5499.00 |               500006 |                            213375.00 |
| tidb-1-2-1 | tidb-1-2-1 |                2 |        64 |    16384 |               1 |           1 |            0 |                         8009.68 |               124849.00 |             499298 |                            5643.00 |               500702 |                            237439.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      1079.21 |      9.85 |           3.09 |                  3.62 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       107.15 |      0.86 |           0.21 |                  0.22 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       808.87 |      6.72 |           8.44 |                 17.07 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       101.31 |      0.83 |           0.21 |                  0.22 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      1002.19 |      9.17 |           1.55 |                  2.08 |
| tidb-1-2-1-1 |       776.37 |      6.88 |           1.07 |                  1.61 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        96.83 |      0.99 |           0.22 |                  0.22 |
| tidb-1-2-1-1 |        85.42 |      0.92 |           0.25 |                  0.25 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       944.98 |      9.04 |          10.44 |                 23.21 |
| tidb-1-2-1-1 |      1253.16 |     12.40 |          11.48 |                 22.05 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        64.64 |      0.92 |           0.55 |                  0.55 |
| tidb-1-2-1-1 |        64.58 |      1.12 |           0.54 |                  0.54 |

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
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
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
'TiDB': {
    'loadData': 'mysql --local-infile -h 127.0.0.1 -P 4000 < {scriptname}',
    'delay_prepare': 60,
    'template': {
        'version': 'CE 8.0.22',
        'alias': 'General-C',
        'docker_alias': 'GP-C',
        'dialect': 'MySQL',
        'JDBC': {
            'driver': "com.mysql.cj.jdbc.Driver",
            'auth': ["root", ""],
            'url': 'jdbc:mysql://{serverip}:9091/{dbname}',
            'jar': ['mysql-connector-j-8.0.31.jar', 'slf4j-simple-1.7.21.jar'],
            'database': 'test',
        }
    },
    'logfile': '/var/log/mysqld.log',
    'datadir': '/var/lib/mysql/',
    'priceperhourdollar': 0.0,
    'worker_port': 2379,
    'store_args': False,
},
```

where
* `loadData`: This command is used to create the schema
* `JDBC`: These infos are used to configure YCSB. A new TiDB cluster creates the user `root` without a password, so the password is empty.
* `worker_port`: This tells bexhoma what the port for internal communication is
* `store_args`: This tells bexhoma not to log args of the containers, since they do not contain parameters

TiDB uses the MySQL JDBC driver.



### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/TiDB







## Benchbase's TPC-C

### Simple Run

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
TiDB has 3 tidb-server pods (`-xnsr`), 3 TiKV nodes (`-nw`), and 3 PD nodes (`-xnpd`) - see [Scaling TiDB Components](#scaling-tidb-components).

```bash
bexhoma benchbase \
  -dbms TiDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -xnsr 3 \
  -nw 3 \
  -xnpd 3 \
  -nwr 3 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_benchbase_tidb_1.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_tidb_1_summary.md" target="_blank" rel="noopener">docs_benchbase_tidb_1.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1144s 
* Code: 1792419132
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Experiment uses bexhoma version 0.11.7.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 1 processes (pods).
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
* tidb-1-1-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:540590800896
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker24
  * disk:174562
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:174562
    * cpu_list:0-95
  * sut 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161072
    * cpu_list:0-127
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:588149
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:588149
    * datadisk:123
    * cpu_list:0-127
  * pd 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:351544
    * datadisk:123
    * cpu_list:0-127
  * pd 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:855794
    * datadisk:123
    * cpu_list:0-223
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:588149
    * datadisk:15534
    * cpu_list:0-127
  * tikv 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:351544
    * datadisk:23397
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:856174
    * datadisk:24472
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * eval_parameters
    * code:1792419132
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-1-2-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:540590800896
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker24
  * disk:176843
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:175334
    * cpu_list:0-95
  * sut 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:161074
    * cpu_list:0-127
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:587958
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:587958
    * datadisk:123
    * cpu_list:0-127
  * pd 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:351134
    * datadisk:123
    * cpu_list:0-127
  * pd 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:854957
    * datadisk:123
    * cpu_list:0-223
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:587958
    * datadisk:15343
    * cpu_list:0-127
  * tikv 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:351134
    * datadisk:22987
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:854957
    * datadisk:23628
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * eval_parameters
    * code:1792419132
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-tidb-1-1792419132-56ffbf5db8-4dcfk: 0
* bexhoma-sut-tidb-1-1792419132-56ffbf5db8-gkmqt: 0
* bexhoma-sut-tidb-1-1792419132-56ffbf5db8-wddbn: 0
* bexhoma-pd-tidb-benchbase-tpcc-16-0: 0
* bexhoma-pd-tidb-benchbase-tpcc-16-1: 0
* bexhoma-pd-tidb-benchbase-tpcc-16-2: 0
* bexhoma-tikv-tidb-benchbase-tpcc-16-0: 0
* bexhoma-tikv-tidb-benchbase-tpcc-16-1: 0
* bexhoma-tikv-tidb-benchbase-tpcc-16-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| TiDB-1-1 |                1 |   16 |      133.00 |           4.00 |            0.00 |        126.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              433.08 | False               |

### Benchmarking

#### Per Connection

| DBMS           | phase      | job          |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:-----------|:-------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         527.85 |                      525.37 |         0.00 |                                                      64127.00 |                                              30302.00 |
| tidb-1-1-2-1-1 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         244.37 |                      241.71 |         0.00 |                                                      72623.00 |                                              32725.00 |
| tidb-1-1-2-1-2 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         240.50 |                      237.94 |         0.00 |                                                      73776.00 |                                              33250.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------|:-----------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         527.85 |                      525.37 |         0.00 |                                                      64127.00 |                                              30302.00 |
| tidb-1-1-2 | tidb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         484.87 |                      479.65 |         0.00 |                                                      73776.00 |                                              32987.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       960.58 |      9.60 |           1.36 |                  1.90 |
| tidb-1-1-2-1 |       960.58 |      9.60 |           1.36 |                  1.90 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        34.78 |      0.28 |           0.21 |                  0.21 |
| tidb-1-1-2-1 |        34.78 |      0.28 |           0.21 |                  0.21 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      2181.06 |     21.60 |          12.45 |                 30.79 |
| tidb-1-1-2-1 |      2181.06 |     21.60 |          12.45 |                 30.79 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       111.81 |      1.82 |           0.68 |                  0.68 |
| tidb-1-1-2-1 |       111.81 |      1.82 |           0.68 |                  0.68 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      3314.79 |     11.59 |           2.98 |                  3.52 |
| tidb-1-1-2-1 |      3009.27 |     10.57 |           2.84 |                  3.38 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       185.90 |      0.65 |           0.22 |                  0.22 |
| tidb-1-1-2-1 |       176.40 |      0.64 |           0.22 |                  0.22 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      4967.56 |     18.33 |          15.82 |                 32.77 |
| tidb-1-1-2-1 |      4576.54 |     18.23 |          17.92 |                 35.75 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       253.18 |      1.23 |           0.33 |                  0.33 |
| tidb-1-1-2-1 |       281.48 |      0.99 |           0.31 |                  0.31 |

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

### Tests
* TEST passed: Loading measured in this experiment
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
* TEST passed: Workflow as planned
```

</details>


### Persistent Storage

The same run with the data of PD and TiKV on persistent volumes of the storage class `$BEXHOMA_STORAGE_CLASS` (`-rst`, see [Use Persistent Storage](#use-persistent-storage)).
Existing volumes are removed before the first repetition (`-rsr`), so the data is loaded fresh.
The experiment is repeated twice (`-nc 2`): the second instance of TiDB reuses the volumes and skips loading, which shows that the data survives a restart of the cluster.

```bash
bexhoma benchbase \
  -dbms TiDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -nc 2 \
  -xnsr 3 \
  -nw 3 \
  -xnpd 3 \
  -nwr 3 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_benchbase_tidb_2.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_tidb_2_summary.md" target="_blank" rel="noopener">docs_benchbase_tidb_2.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2354s 
* Code: 1792420341
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Experiment uses bexhoma version 0.11.7.
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
  * RAM:540590800896
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker24
  * disk:174163
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:174162
    * cpu_list:0-95
  * sut 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:628982
    * cpu_list:0-127
  * sut 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:162100
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:628837
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:831214
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
    * disk:328026
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
    * disk:628838
    * datadisk:7493
    * volume_size:49G
    * volume_used:7.4G
    * cpu_list:0-127
  * tikv 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:328026
    * datadisk:7487
    * volume_size:49G
    * volume_used:7.4G
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:831214
    * datadisk:7474
    * volume_size:49G
    * volume_used:7.3G
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * eval_parameters
    * code:1792420341
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-1-2-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:540590800896
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker24
  * disk:174204
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:174207
    * cpu_list:0-95
  * sut 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:628900
    * cpu_list:0-127
  * sut 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:162117
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:628900
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:831212
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
    * disk:328026
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
    * disk:628900
    * datadisk:5002
    * volume_size:49G
    * volume_used:4.9G
    * cpu_list:0-127
  * tikv 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:328026
    * datadisk:5011
    * volume_size:49G
    * volume_used:4.9G
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:831212
    * datadisk:4985
    * volume_size:49G
    * volume_used:4.9G
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * eval_parameters
    * code:1792420341
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-2-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:540590800896
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker24
  * disk:174245
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:174245
    * cpu_list:0-95
  * sut 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:162387
    * cpu_list:0-127
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:469461
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:469195
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:777717
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
    * disk:328027
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
    * disk:469299
    * datadisk:4892
    * volume_size:49G
    * volume_used:4.8G
    * cpu_list:0-127
  * tikv 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:328027
    * datadisk:4916
    * volume_size:49G
    * volume_used:4.8G
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:777718
    * datadisk:4877
    * volume_size:49G
    * volume_used:4.8G
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * eval_parameters
    * code:1792420341
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-2-2-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:540590800896
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker24
  * disk:174245
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:174245
    * cpu_list:0-95
  * sut 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:162386
    * cpu_list:0-127
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:468724
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:468727
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:777727
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
    * disk:328027
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
    * disk:468727
    * datadisk:6633
    * volume_size:49G
    * volume_used:6.5G
    * cpu_list:0-127
  * tikv 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:328027
    * datadisk:6665
    * volume_size:49G
    * volume_used:6.6G
    * cpu_list:0-127
  * tikv 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:777728
    * datadisk:6589
    * volume_size:49G
    * volume_used:6.5G
    * cpu_list:0-223
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * eval_parameters
    * code:1792420341
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: TiDB-1-2

### SUT Container Restarts
* bexhoma-sut-tidb-1-1792420341-78b7655bdf-5t8g8: 0
* bexhoma-sut-tidb-1-1792420341-78b7655bdf-hl544: 0
* bexhoma-sut-tidb-1-1792420341-78b7655bdf-q9kpx: 0
* bexhoma-pd-tidb-nvme-benchbase-tpcc-16-0: 0
* bexhoma-pd-tidb-nvme-benchbase-tpcc-16-1: 0
* bexhoma-pd-tidb-nvme-benchbase-tpcc-16-2: 0
* bexhoma-tikv-tidb-nvme-benchbase-tpcc-16-0: 0
* bexhoma-tikv-tidb-nvme-benchbase-tpcc-16-1: 0
* bexhoma-tikv-tidb-nvme-benchbase-tpcc-16-2: 0
* bexhoma-sut-tidb-1-1792420341-6f7dc8b584-fr2bl: 0
* bexhoma-sut-tidb-1-1792420341-6f7dc8b584-mrkcz: 0
* bexhoma-sut-tidb-1-1792420341-6f7dc8b584-rcnr9: 0

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

|          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| TiDB-1-1 |                1 |   16 |      202.00 |           4.00 |            0.00 |        196.00 |            2.00 |              1 |           1 |             | None           |             0 | False         |              285.15 | False               |
| TiDB-1-2 |                2 |   16 |      202.00 |           4.00 |            0.00 |        196.00 |            2.00 |              1 |           1 |             | None           |             0 | False         |              285.15 | True                |

### Benchmarking

#### Per Connection

| DBMS           | phase      | job          |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:-----------|:-------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         257.47 |                      256.39 |         0.00 |                                                     156943.00 |                                              62106.00 |
| tidb-1-1-2-1-1 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         126.26 |                      125.02 |         0.00 |                                                     155289.00 |                                              63328.00 |
| tidb-1-1-2-1-2 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         119.96 |                      118.75 |         0.00 |                                                     160869.00 |                                              66650.00 |
| tidb-1-2-1-1-1 | tidb-1-2-1 | tidb-1-2-1-1 |                2 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         292.79 |                      291.49 |         0.00 |                                                     131486.00 |                                              54623.00 |
| tidb-1-2-2-1-1 | tidb-1-2-2 | tidb-1-2-2-1 |                2 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         127.62 |                      126.29 |         0.00 |                                                     152494.00 |                                              62654.00 |
| tidb-1-2-2-1-2 | tidb-1-2-2 | tidb-1-2-2-1 |                2 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         129.78 |                      128.47 |         0.00 |                                                     147476.00 |                                              61609.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------|:-----------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         257.47 |                      256.39 |         0.00 |                                                     156943.00 |                                              62106.00 |
| tidb-1-1-2 | tidb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         246.23 |                      243.77 |         0.00 |                                                     160869.00 |                                              64989.00 |
| tidb-1-2-1 | tidb-1-2-1 |                2 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         292.79 |                      291.49 |         0.00 |                                                     131486.00 |                                              54623.00 |
| tidb-1-2-2 | tidb-1-2-2 |                2 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         257.40 |                      254.76 |         0.00 |                                                     152494.00 |                                              62131.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       905.48 |      6.97 |           4.47 |                  5.01 |
| tidb-1-1-2-1 |       905.48 |      6.97 |           4.47 |                  5.01 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        86.79 |      0.48 |           0.22 |                  0.22 |
| tidb-1-1-2-1 |        86.79 |      0.48 |           0.22 |                  0.22 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      2816.83 |     23.40 |          13.06 |                 31.39 |
| tidb-1-1-2-1 |      2816.83 |     23.40 |          13.06 |                 31.39 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       647.45 |      6.86 |           0.40 |                  0.40 |
| tidb-1-1-2-1 |       647.45 |      6.86 |           0.40 |                  0.40 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      2212.67 |      7.89 |           1.84 |                  2.38 |
| tidb-1-1-2-1 |      2294.31 |      8.13 |           2.22 |                  2.75 |
| tidb-1-2-1-1 |      2057.90 |      7.42 |           1.98 |                  2.52 |
| tidb-1-2-2-1 |      2107.48 |      7.81 |           2.34 |                  2.87 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       311.71 |      1.04 |           0.22 |                  0.22 |
| tidb-1-1-2-1 |       295.98 |      1.04 |           0.23 |                  0.23 |
| tidb-1-2-1-1 |       302.69 |      1.04 |           0.26 |                  0.26 |
| tidb-1-2-2-1 |       273.16 |      1.04 |           0.27 |                  0.27 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      3609.19 |     13.81 |          14.62 |                 34.20 |
| tidb-1-1-2-1 |      3771.48 |     15.61 |          16.79 |                 32.00 |
| tidb-1-2-1-1 |      4114.42 |     16.71 |          11.52 |                 25.06 |
| tidb-1-2-2-1 |      3847.25 |     15.67 |          13.86 |                 32.19 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       290.26 |      1.54 |           0.32 |                  0.32 |
| tidb-1-1-2-1 |       320.49 |      1.82 |           0.30 |                  0.30 |
| tidb-1-2-1-1 |       315.87 |      1.41 |           0.33 |                  0.33 |
| tidb-1-2-2-1 |       321.51 |      1.82 |           0.29 |                  0.29 |

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
* TEST passed: Workflow as planned
```

</details>


