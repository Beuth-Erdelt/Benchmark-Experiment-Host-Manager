# Example: Benchmark Valkey

This example shows how to benchmark Valkey with YCSB, as a single host and as a cluster managed by bexhoma.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[Valkey](https://valkey.io/) is an in-memory key-value store and a drop-in replacement for Redis: a Linux Foundation fork of Redis 7.2.4 under the BSD-3-Clause license (which has no restriction on publishing benchmark results).
This page uses the image `valkey/valkey:9.1.3`.
Bexhoma runs it as a single host (one SUT pod) or as a Valkey cluster (`-nw`), where every shard and every replica is a worker pod of a stateful set.
A Valkey cluster has no coordinator; bexhoma still deploys a main pod as a single point of contact and to annotate the status of experiments.
YCSB talks to Valkey via the Redis wire protocol, not via JDBC.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [Valkey](https://valkey.io/)
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. Test script of this page: [test-docs-valkey.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-valkey.sh), [test-docs-valkey.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-valkey.ps1)


## Perform YCSB Benchmark

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
  -dbms Valkey \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -xop 1 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_valkey.log
```

This
* starts a clean instance of Valkey (`-dbms`)
  * data directory inside a Docker container
* starts 8 loader pods (`-nlp`)
  * threads = 64/8 per pod (`-nlt`)
  * target throughput is 12 * 16384 (`-xnlf`, `-xtb`)
  * generates YCSB data = 1.000.000 rows (i.e., SF=1, `-sf`)
  * imports it into the DBMS
* runs 1 stream of YCSB queries (`-nbp`)
  * 1.000.000 operations (`-xop`)
  * workload A = 50% read / 50% update (`-xwl`)
  * target throughput is 4 * 16384 (`-xnbf`, `-xtb`)
  * threads = 128 (`-nbt`)
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
+--------------------+--------------+------------+------------------------+
| 1741876409         | sut          | use case   | loading                |
+====================+==============+============+========================+
| Valkey-64-8-196608 | (1. Running) | ycsb       | (7 Running)(1 Pending) |
+--------------------+--------------+------------+------------------------+
```

The code `1741876409` is the unique identifier of the experiment.
You can find the number also in the output of the benchmark script.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1741876409` (removes everything that is related to experiment `1741876409`).

### Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_valkey_summary.md" target="_blank" rel="noopener">docs_ycsb_valkey.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 165s 
* Code: 1793706311
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['Valkey'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* valkey-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:794491
  * datadisk:1095
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793706311

### Init Scripts Not in Folder
* Valkey-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-valkey-1-1793706311-6dfb7cb977-jwqr9: 0

### Workflow

#### Actual

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| valkey-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11167.69 |                11193.00 |            125000.00 |                              1740.00 | 1.00 |              321.63 |
| valkey-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10852.58 |                11518.00 |            125000.00 |                              1777.00 | 1.00 |              312.55 |
| valkey-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11304.03 |                11058.00 |            125000.00 |                              1742.00 | 1.00 |              325.56 |
| valkey-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11321.44 |                11041.00 |            125000.00 |                              1740.00 | 1.00 |              326.06 |
| valkey-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10989.98 |                11374.00 |            125000.00 |                              1724.00 | 1.00 |              316.51 |
| valkey-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10748.07 |                11630.00 |            125000.00 |                              1762.00 | 1.00 |              309.54 |
| valkey-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11305.06 |                11057.00 |            125000.00 |                              1772.00 | 1.00 |              325.59 |
| valkey-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11037.53 |                11325.00 |            125000.00 |                              1691.00 | 1.00 |              317.88 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Valkey-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              309.54 |                        88726.37 |                11630.00 |           1000000.00 |                              1743.50 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1-1-1 | valkey-1-1-1 | valkey-1-1-1-1 | Valkey-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64981.48 |                15389.00 |             499184 |                            1564.00 |               500816 |                              1417.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1 | valkey-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64981.48 |                15389.00 |             499184 |                            1564.00 |               500816 |                              1417.00 |

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

To see the summary again you can simply call `bexhoma summary -e 1741876409` with the experiment code.

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example the [Jupyter notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/notebooks/), in particular [Collector-YCSB.ipynb](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/notebooks/Collector-YCSB.ipynb).

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).
Metrics are sampled every few seconds, so the benchmarking phase should take at least a minute.
This run uses SF=3 and 10.000.000 operations (`-xop`).

All metrics in monitoring are summed across all matching components.
For a Valkey cluster, this means that used memory, CPU time, etc. are summed across all worker pods.

```bash
bexhoma ycsb \
  -dbms Valkey \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -xop 10 \
  -m \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_valkey_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_valkey_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_valkey_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 358s 
* Code: 1793706479
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Valkey'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* valkey-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:794019
  * datadisk:3284
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793706479

### Init Scripts Not in Folder
* Valkey-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-valkey-1-1793706479-76c6bbd458-4sphq: 0

### Workflow

#### Actual

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| valkey-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10544.07 |                35565.00 |            375000.00 |                              2019.00 | 3.00 |              303.67 |
| valkey-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10941.88 |                34272.00 |            375000.00 |                              1977.00 | 3.00 |              315.13 |
| valkey-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10798.51 |                34727.00 |            375000.00 |                              2042.00 | 3.00 |              311.00 |
| valkey-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10724.40 |                34967.00 |            375000.00 |                              2103.00 | 3.00 |              308.86 |
| valkey-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10924.35 |                34327.00 |            375000.00 |                              1949.00 | 3.00 |              314.62 |
| valkey-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10896.73 |                34414.00 |            375000.00 |                              1989.00 | 3.00 |              313.83 |
| valkey-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10984.18 |                34140.00 |            375000.00 |                              1970.00 | 3.00 |              316.34 |
| valkey-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10754.54 |                34869.00 |            375000.00 |                              1986.00 | 3.00 |              309.73 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Valkey-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 3.00 |              303.67 |                        86568.66 |                35565.00 |           3000000.00 |                              2004.38 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1-1-1 | valkey-1-1-1 | valkey-1-1-1-1 | Valkey-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65460.02 |               152765.00 |            5000864 |                            1490.00 |              4999136 |                              1426.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1 | valkey-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65460.02 |               152765.00 |            5000864 |                            1490.00 |              4999136 |                              1426.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       273.14 |      4.69 |           4.23 |                  4.24 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 | n/a          |         0 |           0.28 |                  0.28 |

### Benchmarking phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       402.32 |      3.60 |           5.64 |                  5.65 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       676.91 |      6.00 |           1.04 |                  1.04 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

### Application Metrics

Collecting application metrics for Valkey is supported for a cluster (`-nw`).
It is activated by `-m -mc -ma`.
A `redis_exporter` sidecar in every worker pod exposes the metrics on port 9121; Valkey uses the metric set `redis` of [Redis](Example-Redis.md#application-metrics).
Prometheus discovers the worker pods only, so a single host has no application metrics.
See [Metrics](Example-Metrics.html) for application metrics of all DBMS.

```bash
bexhoma ycsb \
  -dbms Valkey \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -nwr 1 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_valkey_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_valkey_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_valkey_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 437s 
* Code: 1793710913
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Valkey'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 1 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* valkey-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:796085
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:130906
    * datadisk:721
    * cpu_list:0-95
  * worker 1
    * RAM:540590821376
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-137-generic
    * node:cl-worker23
    * disk:1283667
    * datadisk:806
    * cpu_list:0-95
  * worker 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:268836
    * datadisk:720
    * cpu_list:0-127
  * worker 3
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:929650
    * datadisk:715
    * cpu_list:0-255
  * worker 4
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:796344
    * datadisk:723
    * cpu_list:0-223
  * worker 5
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:170798
    * datadisk:805
    * cpu_list:0-95
  * resources_total: 24.25 CPU, 384.5 GiB RAM requested in 7 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 6 x, 24.0 CPU, 384.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793710913
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Valkey-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-valkey-1-1793710913-589bdc759d-98m79: 0
* bx-w-valkey-1-1793710913-0: 0
* bx-w-valkey-1-1793710913-1: 0
* bx-w-valkey-1-1793710913-2: 0
* bx-w-valkey-1-1793710913-3: 0
* bx-w-valkey-1-1793710913-4: 0
* bx-w-valkey-1-1793710913-5: 0

### Workflow

#### Actual

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| valkey-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3686.12 |                33911.00 |            125000.00 |                              4411.00 | 1.00 |              106.16 |
| valkey-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3690.58 |                33870.00 |            125000.00 |                              4411.00 | 1.00 |              106.29 |
| valkey-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3696.48 |                33816.00 |            125000.00 |                              4447.00 | 1.00 |              106.46 |
| valkey-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3667.95 |                34079.00 |            125000.00 |                              4447.00 | 1.00 |              105.64 |
| valkey-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3699.21 |                33791.00 |            125000.00 |                              4403.00 | 1.00 |              106.54 |
| valkey-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3703.70 |                33750.00 |            125000.00 |                              4435.00 | 1.00 |              106.67 |
| valkey-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3684.49 |                33926.00 |            125000.00 |                              4427.00 | 1.00 |              106.11 |
| valkey-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3678.20 |                33984.00 |            125000.00 |                              4395.00 | 1.00 |              105.93 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Valkey-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              105.64 |                        29506.73 |                34079.00 |           1000000.00 |                              4422.00 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1-1-1 | valkey-1-1-1 | valkey-1-1-1-1 | Valkey-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        50794.94 |               196870.00 |            5001337 |                            1582.00 |              4998663 |                              1564.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1 | valkey-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        50794.94 |               196870.00 |            5001337 |                            1582.00 |              4998663 |                              1564.00 |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       121.68 |      2.94 |           2.97 |                  2.98 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 | n/a          |         0 |           0.30 |                  0.30 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       497.17 |      3.86 |           3.13 |                  3.14 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       641.96 |      5.18 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS           |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [GiB] |   Redis Master Link Status |   Redis Operations Rate, Busiest Instance [ops/s] |
|:---------------|----------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------------------------------:|
| valkey-1-1-1-1 |                  6.00 |                      201.00 |                      2.88 |                       3.00 |                                           6176.52 |

#### Benchmarking phase: component worker

| DBMS           |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [GiB] |   Redis Master Link Status |   Redis Operations Rate, Busiest Instance [ops/s] |
|:---------------|----------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------------------------------:|
| valkey-1-1-1-1 |                  6.00 |                      393.00 |                      2.88 |                       3.00 |                                          13122.77 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
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
  -dbms Valkey \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -xop 10 \
  -m \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_valkey_storage.log
```

`bexhoma status` shows one volume of type `shared`.
Every single-host Valkey experiment running YCSB of SF=1 will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of Valkey mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_valkey_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_valkey_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 526s 
* Code: 1793490360
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Valkey'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* valkey-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:755500
  * datadisk:1095
  * volume_size:49G
  * volume_used:1.1G
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793490360
* valkey-1-2-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:748972
  * datadisk:1095
  * volume_size:49G
  * volume_used:1.1G
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793490360

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Valkey-1-2

### Data Parameters of Reused Volumes
* Valkey-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Valkey-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-valkey-1-1793490360-7f84b44fb7-2czxp: 0
* bexhoma-sut-valkey-1-1793490360-85c8d5bbc5-rbsw7: 0

### Workflow

#### Actual

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Valkey-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Valkey-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| valkey-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12659.51 |                 9874.00 |            125000.00 |                              1694.00 | 1.00 |              364.59 |
| valkey-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13112.35 |                 9533.00 |            125000.00 |                              1473.00 | 1.00 |              377.64 |
| valkey-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12674.91 |                 9862.00 |            125000.00 |                              1558.00 | 1.00 |              365.04 |
| valkey-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12619.89 |                 9905.00 |            125000.00 |                              1649.00 | 1.00 |              363.45 |
| valkey-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12335.93 |                10133.00 |            125000.00 |                              1645.00 | 1.00 |              355.27 |
| valkey-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12649.26 |                 9882.00 |            125000.00 |                              1525.00 | 1.00 |              364.30 |
| valkey-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12742.10 |                 9810.00 |            125000.00 |                              1587.00 | 1.00 |              366.97 |
| valkey-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12230.92 |                10220.00 |            125000.00 |                              1653.00 | 1.00 |              352.25 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Valkey-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              352.25 |                       101024.87 |                10220.00 |           1000000.00 |                              1598.00 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1-1-1 | valkey-1-1-1 | valkey-1-1-1-1 | Valkey-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65488.31 |               152699.00 |            4998721 |                            1422.00 |              5001279 |                              1384.00 |
| valkey-1-2-1-1-1 | valkey-1-2-1 | valkey-1-2-1-1 | Valkey-1        |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65462.59 |               152759.00 |            4997740 |                            1337.00 |              5002260 |                              1306.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1 | valkey-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65488.31 |               152699.00 |            4998721 |                            1422.00 |              5001279 |                              1384.00 |
| valkey-1-2-1 | valkey-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        65462.59 |               152759.00 |            4997740 |                            1337.00 |              5002260 |                              1306.00 |

### Monitoring

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       611.55 |      4.85 |           1.03 |                  1.03 |
| valkey-1-2-1-1 |       656.67 |      4.66 |           1.36 |                  1.36 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-2-1-1 (bexhoma-metrics-valkey-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-2-1-1 (bexhoma-metrics-valkey-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## Variants

### Cluster

If you want to deploy Valkey as a cluster, you can set the number of workers `-nw`.
Each worker is a shard of the database.

```bash
bexhoma ycsb \
  -dbms Valkey \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -xop 10 \
  -m \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_valkey_cluster.log
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_valkey_cluster_summary.md" target="_blank" rel="noopener">docs_ycsb_valkey_cluster.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 398s 
* Code: 1793489406
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Valkey'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* valkey-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:755824
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:755825
    * datadisk:722
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:553083
    * datadisk:803
    * cpu_list:0-127
  * worker 2
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:2200343
    * datadisk:714
    * cpu_list:0-55
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793489406
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Valkey-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-valkey-1-1793489406-768c6865bf-p5vk7: 0
* bx-w-valkey-1-1793489406-0: 0
* bx-w-valkey-1-1793489406-1: 0
* bx-w-valkey-1-1793489406-2: 0

### Workflow

#### Actual

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| valkey-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5303.58 |                23569.00 |            125000.00 |                              4299.00 | 1.00 |              152.74 |
| valkey-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5417.35 |                23074.00 |            125000.00 |                              4279.00 | 1.00 |              156.02 |
| valkey-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5353.32 |                23350.00 |            125000.00 |                              4271.00 | 1.00 |              154.18 |
| valkey-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5329.35 |                23455.00 |            125000.00 |                              4303.00 | 1.00 |              153.49 |
| valkey-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5374.96 |                23256.00 |            125000.00 |                              4255.00 | 1.00 |              154.80 |
| valkey-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5374.96 |                23256.00 |            125000.00 |                              4351.00 | 1.00 |              154.80 |
| valkey-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5316.21 |                23513.00 |            125000.00 |                              4299.00 | 1.00 |              153.11 |
| valkey-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5347.82 |                23374.00 |            125000.00 |                              4335.00 | 1.00 |              154.02 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Valkey-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              152.74 |                        42817.55 |                23569.00 |           1000000.00 |                              4299.00 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1-1-1 | valkey-1-1-1 | valkey-1-1-1-1 | Valkey-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        61921.42 |               161495.00 |            5003173 |                            2055.00 |              4996827 |                              2045.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1 | valkey-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        61921.42 |               161495.00 |            5003173 |                            2055.00 |              4996827 |                              2045.00 |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |        59.23 |      2.24 |           1.44 |                  1.45 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 | n/a          |         0 |           0.54 |                  0.54 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       257.10 |      1.82 |           1.56 |                  1.57 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       678.60 |      5.01 |           1.48 |                  1.48 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

#### Cluster on Persistent Storage

A Valkey cluster can store the database in persistent storage, too.
Here, we remove existing storage via `-rsr` to start with a clean copy.

```bash
bexhoma ycsb \
  -dbms Valkey \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -xop 10 \
  -m \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_valkey_cluster_storage.log
```

The first volume is attached to the (dummy) coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_valkey_cluster_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_valkey_cluster_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 762s 
* Code: 1793490908
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Valkey'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* valkey-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:747430
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:747430
    * datadisk:720
    * volume_size:49G
    * volume_used:720M
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:555202
    * datadisk:799
    * volume_size:49G
    * volume_used:799M
    * cpu_list:0-127
  * worker 2
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:2199629
    * datadisk:716
    * volume_size:49G
    * volume_used:716M
    * cpu_list:0-55
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793490908
    * BEXHOMA_WORKERS:3
* valkey-1-2-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:669593
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:669594
    * datadisk:730
    * volume_size:49G
    * volume_used:730M
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:552552
    * datadisk:794
    * volume_size:49G
    * volume_used:794M
    * cpu_list:0-127
  * worker 2
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:2199630
    * datadisk:710
    * volume_size:49G
    * volume_used:710M
    * cpu_list:0-55
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793490908
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Valkey-1-2

### Data Parameters of Reused Volumes
* Valkey-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Valkey-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-valkey-1-1793490908-75d4db9bf5-2lfxz: 0
* bx-w-valkey-nvme-ycsb-1-0: 0
* bx-w-valkey-nvme-ycsb-1-1: 0
* bx-w-valkey-nvme-ycsb-1-2: 0
* bexhoma-sut-valkey-1-1793490908-75f99bb76b-tsjsb: 0

### Workflow

#### Actual

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Valkey-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Valkey-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| valkey-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         6204.09 |                20148.00 |            125000.00 |                              2677.00 | 1.00 |              178.68 |
| valkey-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         6226.65 |                20075.00 |            125000.00 |                              2673.00 | 1.00 |              179.33 |
| valkey-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         6279.20 |                19907.00 |            125000.00 |                              2659.00 | 1.00 |              180.84 |
| valkey-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         6213.65 |                20117.00 |            125000.00 |                              2679.00 | 1.00 |              178.95 |
| valkey-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         6360.03 |                19654.00 |            125000.00 |                              2649.00 | 1.00 |              183.17 |
| valkey-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         6290.57 |                19871.00 |            125000.00 |                              2667.00 | 1.00 |              181.17 |
| valkey-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         6227.58 |                20072.00 |            125000.00 |                              2641.00 | 1.00 |              179.35 |
| valkey-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         6226.03 |                20077.00 |            125000.00 |                              2651.00 | 1.00 |              179.31 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Valkey-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              178.68 |                        50027.80 |                20148.00 |           1000000.00 |                              2662.00 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1-1-1 | valkey-1-1-1 | valkey-1-1-1-1 | Valkey-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        61899.96 |               161551.00 |            4999673 |                            1318.00 |              5000327 |                              1316.00 |
| valkey-1-2-1-1-1 | valkey-1-2-1 | valkey-1-2-1-1 | Valkey-1        |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        61599.87 |               162338.00 |            4999619 |                            1090.00 |              5000381 |                              1071.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1 | valkey-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        61899.96 |               161551.00 |            4999673 |                            1318.00 |              5000327 |                              1316.00 |
| valkey-1-2-1 | valkey-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        61599.87 |               162338.00 |            4999619 |                            1090.00 |              5000381 |                              1071.00 |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |        51.47 |      1.51 |           1.44 |                  1.44 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 | n/a          |         0 |           0.45 |                  0.45 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       212.18 |      1.60 |           1.48 |                  1.49 |
| valkey-1-2-1-1 |       227.06 |      2.01 |           1.51 |                  2.26 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       618.76 |      4.88 |           1.49 |                  1.49 |
| valkey-1-2-1-1 |       647.85 |      4.96 |           1.48 |                  1.48 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-2-1-1 (bexhoma-metrics-valkey-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-2-1-1 (bexhoma-metrics-valkey-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-2-1-1 (bexhoma-metrics-valkey-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-2-1-1 (bexhoma-metrics-valkey-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

### Replication

We can set the number of replicas with the parameter `-nwr`.
Valkey requires a worker per replicated shard, so `-nw 3` and `-nwr 1` create 6 worker pods, 3 for sharding and another 3 for the (single) replicas.

```bash
bexhoma ycsb \
  -dbms Valkey \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -nwr 1 \
  -xop 10 \
  -m \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_valkey_replica.log
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_valkey_replica_summary.md" target="_blank" rel="noopener">docs_ycsb_valkey_replica.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 492s 
* Code: 1793489831
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Valkey'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 1 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* valkey-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:756946
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:756946
    * datadisk:721
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:553080
    * datadisk:804
    * cpu_list:0-127
  * worker 2
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:2200347
    * datadisk:718
    * cpu_list:0-55
  * worker 3
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:929128
    * datadisk:735
    * cpu_list:0-255
  * worker 4
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:241401
    * datadisk:719
    * cpu_list:0-255
  * worker 5
    * RAM:540492857344
    * CPU:Intel(R) Xeon(R) Gold 6430
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker38
    * disk:402051
    * datadisk:799
    * cpu_list:0-127
  * resources_total: 24.25 CPU, 384.5 GiB RAM requested in 7 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 6 x, 24.0 CPU, 384.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793489831
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Valkey-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-valkey-1-1793489831-65fbb9868-q6rh7: 0
* bx-w-valkey-1-1793489831-0: 0
* bx-w-valkey-1-1793489831-1: 0
* bx-w-valkey-1-1793489831-2: 0
* bx-w-valkey-1-1793489831-3: 0
* bx-w-valkey-1-1793489831-4: 0
* bx-w-valkey-1-1793489831-5: 0

### Workflow

#### Actual

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| valkey-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5144.46 |                24298.00 |            125000.00 |                              3441.00 | 1.00 |              148.16 |
| valkey-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5159.75 |                24226.00 |            125000.00 |                              3439.00 | 1.00 |              148.60 |
| valkey-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5197.51 |                24050.00 |            125000.00 |                              3501.00 | 1.00 |              149.69 |
| valkey-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5168.07 |                24187.00 |            125000.00 |                              3451.00 | 1.00 |              148.84 |
| valkey-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5156.34 |                24242.00 |            125000.00 |                              3457.00 | 1.00 |              148.50 |
| valkey-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5205.51 |                24013.00 |            125000.00 |                              3517.00 | 1.00 |              149.92 |
| valkey-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5170.84 |                24174.00 |            125000.00 |                              3471.00 | 1.00 |              148.92 |
| valkey-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5144.46 |                24298.00 |            125000.00 |                              3457.00 | 1.00 |              148.16 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Valkey-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              148.16 |                        41346.93 |                24298.00 |           1000000.00 |                              3466.75 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1-1-1 | valkey-1-1-1 | valkey-1-1-1-1 | Valkey-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        55998.25 |               178577.00 |            5003807 |                            1455.00 |              4996193 |                              1435.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1 | valkey-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        55998.25 |               178577.00 |            5003807 |                            1455.00 |              4996193 |                              1435.00 |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       130.10 |      3.05 |           3.06 |                  3.07 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 | n/a          |         0 |           0.53 |                  0.53 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       398.89 |      3.19 |           3.06 |                  3.09 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       730.72 |      5.09 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
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
'Valkey': {
    'loadData': 'valkey-cli --host bexhoma-service.{namespace}.svc.cluster.local < {scriptname}',
    'delay_prepare': 0,
    'attachWorker': '',
    'template': {
        'version': 'xxx',
        'alias': 'Key-Value-1',
        'docker_alias': 'KV1',
        'auth': ["root", ""],
    },
    'logfile': '/var/log/valkey/valkey-server.log',
    'datadir': '/data',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery for worker pods on port 9121 (redis_exporter)
},
```

It is the configuration of [Redis](Example-Redis.md#configuration-of-bexhoma) with `valkey-cli` instead of `redis-cli`.
There is no `JDBC` section, as Valkey has no JDBC driver.

### Deployment

* Single host: [deploymenttemplate-Valkey.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Valkey.yml), one SUT pod with Valkey, a `redis_exporter` and a cAdvisor sidecar.
* Cluster (`-nw` > 0): [deploymenttemplate-ValkeyCluster.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-ValkeyCluster.yml), a stateful set of `-nw` * (1 + `-nwr`) worker pods with `--appendonly yes`, and a job that creates the cluster once all workers answer.
  * The SUT pod is a placeholder: the data lives in the workers, and the SUT pod is not monitored.
  * Shell scripts run on every worker (script target `workers`).
  * Valkey expects a fully qualified domain name (FQDN) for each pod, while the length of hostnames is limited. Therefore bexhoma shortens the names of the worker pods and their volumes.
* Bexhoma also deploys a service for communication external to Valkey (from within the cluster) and a headless service for communication between the pods of the Valkey cluster.

### Schema and Scripts

Valkey has no schema; YCSB writes the keys directly via the Redis wire protocol.
The experiment folder [experiments/ycsb/Valkey](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Valkey) contains only the reset script.

### Load Durability

`-xld` has no effect on Valkey: there are no durability scripts for it.
The single host keeps the default persistence (RDB snapshots), the cluster also writes an append-only file (`--appendonly yes`).

### Reset Scripts

With `-ar`, [save-snapshot.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/ycsb/Valkey/save-snapshot.sh) runs before each benchmarking round, in the SUT pod (single host) or in every worker (cluster):

1. Statistics: n/a (no optimizer statistics)
2. Persist: `SAVE` writes an RDB snapshot
3. Counters: `CONFIG RESETSTAT`

See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract.
There is no test run for Valkey in [Test: Reset Scripts](Test-Reset.md) yet; the scripts are the ones of [Redis](Example-Redis.md#reset-scripts) with `valkey-cli`.
