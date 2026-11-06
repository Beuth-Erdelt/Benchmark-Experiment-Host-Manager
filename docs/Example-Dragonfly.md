# Example: Benchmark Dragonfly

This example shows how to benchmark Dragonfly with YCSB, as a single host, as a cluster and with replication, managed by bexhoma.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[Dragonfly](https://www.dragonflydb.io/) is an in-memory key-value store and a drop-in replacement for Redis.
Bexhoma runs it as a single host (one SUT pod), as a cluster of shards (`-nw`) or as a master with replicas (`-nw` with `-nwr`), where the data pods are workers of a stateful set.
In a cluster, bexhoma still deploys a main pod as a single point of contact and to annotate the status of experiments; it holds no data.
YCSB talks to Dragonfly via the Redis wire protocol, not via JDBC.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [Dragonfly](https://www.dragonflydb.io/)
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. Test script of this page: [test-docs-dragonfly.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-dragonfly.sh), [test-docs-dragonfly.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-dragonfly.ps1)


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
  -dbms Dragonfly \
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
  run &>$LOG_DIR/docs_ycsb_dragonfly.log
```

This
* starts a clean instance of Dragonfly (`-dbms`)
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
+-----------------------+--------------+--------------+------------+-------------+-------------+
| 1774020403            | sut          |   loaded [s] | use case   | worker      | loading     |
+=======================+==============+==============+============+=============+=============+
| Dragonfly-64-8-196608 | (1. Running) |            1 | ycsb       | (3 Running) | (8 Running) |
+-----------------------+--------------+--------------+------------+-------------+-------------+
```

The code `1774020403` is the unique identifier of the experiment.
You can find the number also in the output of the benchmark script.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1774020403` (removes everything that is related to experiment `1774020403`).

### Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_dragonfly_summary.md" target="_blank" rel="noopener">docs_ycsb_dragonfly.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 134s 
* Code: 1793705396
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
  * Experiment is limited to DBMS ['Dragonfly'].
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
* dragonfly-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:791656
  * datadisk:1086
  * volume_size:1.8T
  * volume_used:774G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793705396

### Init Scripts Not in Folder
* Dragonfly-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonfly-1-1793705396-86df8b6864-hrp89: 0

### Workflow

#### Actual

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24029.22 |                 5202.00 |            125000.00 |                               712.00 | 1.00 |              692.04 |
| dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24234.20 |                 5158.00 |            125000.00 |                               724.00 | 1.00 |              697.94 |
| dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24262.42 |                 5152.00 |            125000.00 |                               695.00 | 1.00 |              698.76 |
| dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24276.56 |                 5149.00 |            125000.00 |                               720.00 | 1.00 |              699.16 |
| dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        23549.36 |                 5308.00 |            125000.00 |                               817.00 | 1.00 |              678.22 |
| dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24267.13 |                 5151.00 |            125000.00 |                               709.00 | 1.00 |              698.89 |
| dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24309.61 |                 5142.00 |            125000.00 |                               733.00 | 1.00 |              700.12 |
| dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24319.07 |                 5140.00 |            125000.00 |                               754.00 | 1.00 |              700.39 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              678.22 |                       193247.57 |                 5308.00 |           1000000.00 |                               733.00 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1-1-1 | dragonfly-1-1-1 | dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65006.83 |                15383.00 |             499082 |                             865.00 |               500918 |                               773.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1 | dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65006.83 |                15383.00 |             499082 |                             865.00 |               500918 |                               773.00 |

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

To see the summary again you can simply call `bexhoma summary -e 1774020403` with the experiment code.

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
For a Dragonfly cluster, this means that used memory, CPU time, etc. are summed across all worker pods.

```bash
bexhoma ycsb \
  -dbms Dragonfly \
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
  -ma \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_dragonfly_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_dragonfly_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 362s 
* Code: 1793823429
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
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
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
* dragonfly-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:854201
  * datadisk:3256
  * volume_size:1.8T
  * volume_used:835G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793823429

### Init Scripts Not in Folder
* Dragonfly-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonfly-1-1793823429-685fff678b-k4rgm: 0

### Workflow

#### Actual

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24487.40 |                15314.00 |            375000.00 |                               579.00 | 3.00 |              705.24 |
| dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24485.80 |                15315.00 |            375000.00 |                               540.00 | 3.00 |              705.19 |
| dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24458.65 |                15332.00 |            375000.00 |                               600.00 | 3.00 |              704.41 |
| dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24484.20 |                15316.00 |            375000.00 |                               547.00 | 3.00 |              705.14 |
| dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24477.81 |                15320.00 |            375000.00 |                               573.00 | 3.00 |              704.96 |
| dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24474.61 |                15322.00 |            375000.00 |                               572.00 | 3.00 |              704.87 |
| dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24474.61 |                15322.00 |            375000.00 |                               545.00 | 3.00 |              704.87 |
| dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24497.00 |                15308.00 |            375000.00 |                               560.00 | 3.00 |              705.51 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 3.00 |              704.41 |                       195840.07 |                15332.00 |           3000000.00 |                               564.50 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1-1-1 | dragonfly-1-1-1 | dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65492.17 |               152690.00 |            4999051 |                             724.00 |              5000949 |                               705.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1 | dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65492.17 |               152690.00 |            4999051 |                             724.00 |              5000949 |                               705.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       187.33 |      5.36 |           4.68 |                  4.68 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 | n/a          |         0 |           0.53 |                  0.53 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       444.98 |      3.02 |           4.63 |                  4.63 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       608.10 |      4.96 |           1.02 |                  1.03 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonfly-1-1-1-1 |             6000001.00 |                 4.54 |                     29995.33 |                   18.93 |                    0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonfly-1-1-1-1 |             7864263.00 |                 4.54 |                     51989.37 |                   16.95 |                    0.00 |

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

Collecting application metrics for Dragonfly is supported and included in the run above.
It is activated by `-m -mc -ma`.
Dragonfly exposes its metrics natively at `/metrics` on port 6379, so no exporter sidecar is needed.
The metric set `dragonfly` in [cluster.config](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config) contains:

| Metric | Title |
|---|---|
| `dragonfly_reply_total` | Replies Sent [count] |
| `dragonfly_memory_used_bytes` | Memory Usage [GiB] |
| `dragonfly_commands_processed_total` | Processed Commands [ops/s] |
| `dragonfly_net_input_bytes_total` | Network Input [MiB/s] |
| `dragonfly_connected_replica_lag_records` | Replica Lag [records] |
| `dragonfly_moved_errors_total` | Cluster Slot Moved Errors [count] |
| `dragonfly_replication_streaming_bytes` | Replication Streaming Memory [GiB] |
| `dragonfly_replication_full_sync_bytes` | Full Sync Replication Memory [GiB] |
| `dragonfly_replication_psync_count` | PSync Events [count] |

See [Metrics](Example-Metrics.html) for application metrics of all DBMS.


## Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

Dragonfly keeps the data in memory and writes it to disk only on `SAVE` or on shutdown.
Therefore the runs on persistent storage use `-ar`: before each benchmarking round, `SAVE` writes a snapshot, so the volume holds the data that the round starts from (see [Reset Scripts](#reset-scripts)).

Example:
```bash
bexhoma ycsb \
  -dbms Dragonfly \
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
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly_storage.log
```

The following status shows we have one volume of type `shared`.
Every single-host Dragonfly experiment running YCSB of SF=1 will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of Dragonfly mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```bash
+--------------------------------------------+---------------------+--------------+--------------+-------------------+---------------------+----------------------+-----------+----------+--------+--------+
| Volumes                                    | configuration       | experiment   | loaded [s]   |   timeLoading [s] | dbms                | storage_class_name   | storage   | status   | size   | used   |
+============================================+=====================+==============+==============+===================+=====================+======================+===========+==========+========+========+
| bexhoma-storage-dragonfly-ycsb-1           | dragonfly           | ycsb-1       | True         |                50 | Dragonfly           | shared               | 50Gi      | Bound    | 50G    | 0      |
+--------------------------------------------+---------------------+--------------+--------------+-------------------+---------------------+----------------------+-----------+----------+--------+--------+
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_dragonfly_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_dragonfly_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 779s 
* Code: 1782826724
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
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* Dragonfly-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263492
  * volume_size:50G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782826724
* Dragonfly-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263492
  * datadisk:2191
  * volume_size:50G
  * volume_used:2.2G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782826724

### SUT Container Restarts
* bexhoma-sut-dragonfly-1-1782826724-5c9c9f865b-w7z9w: 0

### Workflow

#### Actual

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Dragonfly-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Dragonfly-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| Dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9391.44 |                13310.00 |            125000.00 |                              2515.00 | 1.00 |              270.47 |
| Dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9621.31 |                12992.00 |            125000.00 |                              2525.00 | 1.00 |              277.09 |
| Dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9418.32 |                13272.00 |            125000.00 |                              2487.00 | 1.00 |              271.25 |
| Dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9604.30 |                13015.00 |            125000.00 |                              2503.00 | 1.00 |              276.60 |
| Dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9058.63 |                13799.00 |            125000.00 |                              2791.00 | 1.00 |              260.89 |
| Dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9006.41 |                13879.00 |            125000.00 |                              2709.00 | 1.00 |              259.38 |
| Dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9054.69 |                13805.00 |            125000.00 |                              2485.00 | 1.00 |              260.78 |
| Dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9140.77 |                13675.00 |            125000.00 |                              2707.00 | 1.00 |              263.25 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              259.38 |                        74295.87 |                13879.00 |           1000000.00 |                              2590.25 |

### Execution

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-2-1-1-1 | Dragonfly-1-2-1 | Dragonfly-1-2-1-1 | Dragonfly-1     |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65499.47 |               152673.00 |            4999915 |                            2035.00 |              5000085 |                              1993.00 |
| Dragonfly-1-1-1-1-1 | Dragonfly-1-1-1 | Dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65502.90 |               152665.00 |            4999078 |                            2083.00 |              5000922 |                              2039.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1-1 | Dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65502.90 |               152665.00 |            4999078 |                            2083.00 |              5000922 |                              2039.00 |
| Dragonfly-1-2-1 | Dragonfly-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        65499.47 |               152673.00 |            4999915 |                            2035.00 |              5000085 |                              1993.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |       262.30 |      7.26 |           1.69 |                  1.69 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |        14.39 |      0.00 |           0.09 |                  0.10 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |      2176.60 |     15.42 |           1.71 |                  1.71 |
| Dragonfly-1-2-1-1 |      2788.43 |     18.31 |           1.84 |                  2.91 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |       677.51 |      4.85 |           0.13 |                  0.13 |
| Dragonfly-1-2-1-1 |       677.51 |      4.85 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-1-1-1-1 |             2000000.00 |                1.54 |                           9049.78 |                     5.71 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-1-1-1-1 |             8635927.00 |                1.54 |                          30315.84 |                     3.31 |                    0.00 |
| Dragonfly-1-2-1-1 |             9601197.00 |                1.63 |                          33278.43 |                     3.36 |                    0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## Variants

### Cluster

If you want to deploy Dragonfly as a cluster, you can set the number of workers `-nw`.
Each worker is a shard of the database.

```bash
bexhoma ycsb \
  -dbms Dragonfly \
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
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly_cluster.log
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_dragonfly_cluster_summary.md" target="_blank" rel="noopener">docs_ycsb_dragonfly_cluster.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 379s 
* Code: 1782825850
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
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 5Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* DragonflyCluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263492
  * datadisk:1
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:596146
    * datadisk:1
    * cpu_list:0-223
  * worker 1
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:145386
    * datadisk:1
    * cpu_list:0-95
  * worker 2
    * RAM:1081853939712
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:656846
    * datadisk:1
    * cpu_list:0-127
  * eval_parameters
    * code:1782825850
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1782825850-7477764444-n9m5v: 0
* bx-w-dragonfly-ycsb-1-0: 0
* bx-w-dragonfly-ycsb-1-1: 0
* bx-w-dragonfly-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| DragonflyCluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9745.83 |                12826.00 |            125000.00 |                              2373.00 | 1.00 |              280.68 |
| DragonflyCluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9067.17 |                13786.00 |            125000.00 |                              2573.00 | 1.00 |              261.13 |
| DragonflyCluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9693.68 |                12895.00 |            125000.00 |                              2445.00 | 1.00 |              279.18 |
| DragonflyCluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9811.62 |                12740.00 |            125000.00 |                              2345.00 | 1.00 |              282.57 |
| DragonflyCluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9431.83 |                13253.00 |            125000.00 |                              2481.00 | 1.00 |              271.64 |
| DragonflyCluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9545.63 |                13095.00 |            125000.00 |                              2433.00 | 1.00 |              274.91 |
| DragonflyCluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9295.06 |                13448.00 |            125000.00 |                              2431.00 | 1.00 |              267.70 |
| DragonflyCluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9390.73 |                13311.00 |            125000.00 |                              2639.00 | 1.00 |              270.45 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              261.13 |                        75981.54 |                13786.00 |           1000000.00 |                              2465.00 |

### Execution

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1-1-1 | DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64306.20 |               155506.00 |            4997977 |                            2731.00 |              5002023 |                              2707.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64306.20 |               155506.00 |            4997977 |                            2731.00 |              5002023 |                              2707.00 |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       260.30 |      8.28 |           2.34 |                  2.34 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |        19.92 |      0.00 |           0.12 |                  0.12 |

### Execution phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |      1122.54 |      8.86 |           2.36 |                  2.36 |

### Execution phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       681.65 |      5.14 |           0.29 |                  0.31 |

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             1855816.00 |                1.39 |                           9886.38 |                     5.95 |                    0.00 |

#### Execution phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             8760701.00 |                1.60 |                          31010.37 |                     3.04 |                    0.00 |

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

</details>

#### Cluster on Persistent Storage

A Dragonfly cluster can store the database in persistent storage, too.
Here, we remove existing storage via `-rsr` to start with a clean copy.

```bash
bexhoma ycsb \
  -dbms Dragonfly \
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
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly_cluster_storage.log
```

The first volume is attached to the (dummy) coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.

```bash
+--------------------------------------------+---------------------+--------------+--------------+-------------------+---------------------+----------------------+-----------+----------+--------+--------+
| Volumes                                    | configuration       | experiment   | loaded [s]   |   timeLoading [s] | dbms                | storage_class_name   | storage   | status   | size   | used   |
+============================================+=====================+==============+==============+===================+=====================+======================+===========+==========+========+========+
| bexhoma-storage-dragonfly-ycsb-1           | dragonfly           | ycsb-1       | True         |                48 | Dragonfly           | shared               | 50Gi      | Bound    | 0      | 0      |
+--------------------------------------------+---------------------+--------------+--------------+-------------------+---------------------+----------------------+-----------+----------+--------+--------+

+-----------------------------------------------+-----------------------+--------------+-----------+----------------------+-----------+----------+--------+--------+
| Volumes of Workers                            | configuration         |   experiment | dbms      | storage_class_name   | storage   | status   | size   | used   |
+===============================================+=======================+==============+===========+======================+===========+==========+========+========+
| bxw-bx-w-dragonfly-ycsb-1-0                   | Dragonfly-64-8-196608 |   1774015994 | Dragonfly | shared               | 50Gi      | Bound    | 50G    | 352M   |
+-----------------------------------------------+-----------------------+--------------+-----------+----------------------+-----------+----------+--------+--------+
| bxw-bx-w-dragonfly-ycsb-1-1                   | Dragonfly-64-8-196608 |   1774015994 | Dragonfly | shared               | 50Gi      | Bound    | 50G    | 384M   |
+-----------------------------------------------+-----------------------+--------------+-----------+----------------------+-----------+----------+--------+--------+
| bxw-bx-w-dragonfly-ycsb-1-2                   | Dragonfly-64-8-196608 |   1774015994 | Dragonfly | shared               | 50Gi      | Bound    | 50G    | 352M   |
+-----------------------------------------------+-----------------------+--------------+-----------+----------------------+-----------+----------+--------+--------+
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_dragonfly_cluster_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_dragonfly_cluster_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 787s 
* Code: 1782827530
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
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* DragonflyCluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263492
  * datadisk:1
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:596940
    * volume_size:50G
    * cpu_list:0-223
  * worker 1
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:145308
    * volume_size:50G
    * cpu_list:0-95
  * worker 2
    * RAM:1081853939712
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:685580
    * volume_size:50G
    * cpu_list:0-127
  * eval_parameters
    * code:1782827530
    * BEXHOMA_WORKERS:3
* DragonflyCluster-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:266867
  * datadisk:1
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:592122
    * datadisk:356
    * volume_size:50G
    * volume_used:352M
    * cpu_list:0-223
  * worker 1
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:145453
    * datadisk:386
    * volume_size:50G
    * volume_used:384M
    * cpu_list:0-95
  * worker 2
    * RAM:1081853939712
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:685657
    * datadisk:355
    * volume_size:50G
    * volume_used:352M
    * cpu_list:0-127
  * eval_parameters
    * code:1782827530
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1782827530-7876f9c4b6-v6mcg: 0
* bx-w-dragonfly-ycsb-1-0: 0
* bx-w-dragonfly-ycsb-1-1: 0
* bx-w-dragonfly-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS DragonflyCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS DragonflyCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| DragonflyCluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9203.36 |                13582.00 |            125000.00 |                              2873.00 | 1.00 |              265.06 |
| DragonflyCluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8873.43 |                14087.00 |            125000.00 |                              2875.00 | 1.00 |              255.55 |
| DragonflyCluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9780.91 |                12780.00 |            125000.00 |                              2819.00 | 1.00 |              281.69 |
| DragonflyCluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9202.68 |                13583.00 |            125000.00 |                              2797.00 | 1.00 |              265.04 |
| DragonflyCluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9115.44 |                13713.00 |            125000.00 |                              2885.00 | 1.00 |              262.52 |
| DragonflyCluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9268.18 |                13487.00 |            125000.00 |                              2925.00 | 1.00 |              266.92 |
| DragonflyCluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9049.45 |                13813.00 |            125000.00 |                              2735.00 | 1.00 |              260.62 |
| DragonflyCluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9123.42 |                13701.00 |            125000.00 |                              2987.00 | 1.00 |              262.75 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              255.55 |                        73616.86 |                14087.00 |           1000000.00 |                              2862.00 |

### Execution

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-2-1-1-1 | DragonflyCluster-1-2-1 | DragonflyCluster-1-2-1-1 | DragonflyCluster-1 |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64241.75 |               155662.00 |            4998467 |                            2815.00 |              5001533 |                              2787.00 |
| DragonflyCluster-1-1-1-1-1 | DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64252.07 |               155637.00 |            4997231 |                            2801.00 |              5002769 |                              2775.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64252.07 |               155637.00 |            4997231 |                            2801.00 |              5002769 |                              2775.00 |
| DragonflyCluster-1-2-1 | DragonflyCluster-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        64241.75 |               155662.00 |            4998467 |                            2815.00 |              5001533 |                              2787.00 |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       146.70 |      4.58 |           1.67 |                  1.67 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |         0.16 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |      1256.92 |      9.07 |           2.37 |                  2.37 |
| DragonflyCluster-1-2-1-1 |      1644.04 |      9.61 |           2.52 |                  3.59 |

### Execution phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       651.07 |      5.16 |           0.29 |                  0.29 |
| DragonflyCluster-1-2-1-1 |       651.07 |      5.63 |           0.29 |                  0.29 |

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             1924690.00 |                1.49 |                           8189.88 |                     5.59 |                    0.00 |

#### Execution phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             8824841.00 |                1.60 |                          31519.89 |                     3.06 |                    0.00 |
| DragonflyCluster-1-2-1-1 |             9214551.00 |                1.69 |                          32466.51 |                     3.28 |                    0.00 |

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

</details>

### Replication

We can set the number of replicas with the parameter `-nwr`.
However, only the basic master-copy replication is implemented in bexhoma.
Whenever `-nwr` is greater than 0, it is set to the number of workers minus 1.
The first worker pod is the master and receives all writes; the other workers replicate it.
As in the cluster, the main pod deployed by bexhoma holds no data.

```bash
bexhoma ycsb \
  -dbms Dragonfly \
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
  -ar \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly_replica.log
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_dragonfly_replica_summary.md" target="_blank" rel="noopener">docs_ycsb_dragonfly_replica.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 442s 
* Code: 1782826255
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
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 5Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* DragonflyCluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263492
  * datadisk:1
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:594803
    * datadisk:1
    * cpu_list:0-223
  * worker 1
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:145307
    * datadisk:1
    * cpu_list:0-95
  * worker 2
    * RAM:1081742745600
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:772228
    * datadisk:1
    * cpu_list:0-127
  * eval_parameters
    * code:1782826255
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1782826255-7794959675-djt9l: 0
* bx-w-dragonfly-ycsb-1-0: 0
* bx-w-dragonfly-ycsb-1-1: 0
* bx-w-dragonfly-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| DragonflyCluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4828.12 |                25890.00 |            125000.00 |                             37823.00 | 1.00 |              139.05 |
| DragonflyCluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4892.94 |                25547.00 |            125000.00 |                             37727.00 | 1.00 |              140.92 |
| DragonflyCluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4948.14 |                25262.00 |            125000.00 |                             37855.00 | 1.00 |              142.51 |
| DragonflyCluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4860.79 |                25716.00 |            125000.00 |                             37823.00 | 1.00 |              139.99 |
| DragonflyCluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4529.48 |                27597.00 |            125000.00 |                             37951.00 | 1.00 |              130.45 |
| DragonflyCluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4913.33 |                25441.00 |            125000.00 |                             37791.00 | 1.00 |              141.50 |
| DragonflyCluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4723.40 |                26464.00 |            125000.00 |                             37887.00 | 1.00 |              136.03 |
| DragonflyCluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         4748.88 |                26322.00 |            125000.00 |                             37823.00 | 1.00 |              136.77 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              130.45 |                        38445.08 |                27597.00 |           1000000.00 |                             37835.00 |

### Execution

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1-1-1 | DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65496.46 |               152680.00 |            5000064 |                            3409.00 |              4999936 |                              3379.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65496.46 |               152680.00 |            5000064 |                            3409.00 |              4999936 |                              3379.00 |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       372.30 |     10.66 |           5.52 |                  5.52 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |         0.17 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |      1417.89 |     11.17 |           7.50 |                  7.50 |

### Execution phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       715.41 |      4.85 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             1780822.00 |                4.06 |                          22447.59 |                     4.82 |                46756.00 |

#### Execution phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             8805442.00 |                4.59 |                          62564.37 |                     3.10 |                 1472.00 |

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

</details>


## Technical Details

### Configuration of Bexhoma

In `cluster.config` there are two sections, `Dragonfly` for a single host and `DragonflyCluster` for a cluster and for replication (`-nw` > 0):

```python
'Dragonfly': {
    'abbreviation': 'df',
    'loadData': 'redis-cli < {scriptname}',
    'delay_prepare': 0,
    'attachWorker': '',
    'template': {
        'version': 'xxx',
        'alias': 'Key-Value-1',
        'docker_alias': 'KV1',
        'auth': ["root", ""],
    },
    'logfile': '/var/log/redis/redis-server.log',
    'datadir': '/data',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery for sut pods on port 6379 at /metrics
},
'DragonflyCluster': {
    'loadData': 'redis-cli --host bexhoma-service.{namespace}.svc.cluster.local < {scriptname}',
    ...
    'monitor': { ... },  # Prometheus discovery for worker pods on port 6379 at /metrics
},
```

where
* `abbreviation`: short name in the names of volumes and worker pods
* `loadData`: command to run a script; the cluster targets the service of bexhoma instead of `localhost`
* `monitor`: Prometheus discovery of the SUT pod (single host) or the worker pods (cluster), scraping the native `/metrics` endpoint of Dragonfly

There is no `JDBC` section, as Dragonfly has no JDBC driver.
Both sections use the metric set `dragonfly`, see [Application Metrics](#application-metrics).

### Deployment

* Single host: [deploymenttemplate-Dragonfly.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Dragonfly.yml), one SUT pod.
* Cluster (`-nw` > 0): [deploymenttemplate-DragonflyCluster.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-DragonflyCluster.yml), a stateful set of `-nw` worker pods. YCSB uses a cluster-aware client (`redis-cluster`) that finds the right shard for each key.
* Replication (`-nw` > 0 and `-nwr` > 0): [deploymenttemplate-DragonflyReplica.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-DragonflyReplica.yml), worker 0 is the master (the service points there), the other workers replicate it. Its volumes have their own name (`dfr`), since they hold all data instead of a shard.
* In cluster and replication mode, the SUT pod is a placeholder: the data lives in the workers, and the SUT pod is not monitored. Shell scripts run on every worker (script target `workers`).
* We copied the following behaviour from Redis: Redis expects a fully qualified domain name (FQDN) for each pod, while the length of hostnames is limited. Therefore bexhoma shortens the names of the worker pods and their volumes.

### Settings of Dragonfly

The templates set Dragonfly's flags as environment variables `DFLY_<flag>`, not as command-line flags, because a flag on the command line would win over the variable:

| Variable | Value | Meaning |
|---|---|---|
| `DFLY_maxmemory` | `128GiB` (data pods) | memory limit of Dragonfly |
| `DFLY_dbfilename` | `dump` (data pods) | fixed snapshot name, see [Reset Scripts](#reset-scripts) |
| `DFLY_proactor_threads` | `16` | number of io threads, equal to the CPU limit of the container |

Without `DFLY_proactor_threads`, Dragonfly starts one io thread per core of the host, pinned to that core, regardless of the CPU request and limit of the pod.
On a node with 224 cores and other workloads, this made Dragonfly stall for up to 2 seconds, so that YCSB clients ran into read timeouts.

A setting can be changed per experiment with `--set`.
The name in `deployment[...]` or `statefulset[...]` is `metadata.name` of the workload in the template, the container is `dbms`:

```bash
# single host (k8s/deploymenttemplate-Dragonfly.yml)
bexhoma ycsb -dbms Dragonfly ... \
  --set deployment[bexhoma-deployment-redis].container[dbms].env.DFLY_proactor_threads=4 \
  run

# cluster and replication: the data pods (k8s/deploymenttemplate-DragonflyCluster.yml, -DragonflyReplica.yml)
bexhoma ycsb -dbms Dragonfly -nw 3 ... \
  --set statefulset[bexhoma-worker].container[dbms].env.DFLY_proactor_threads=8 \
  run
```

The output of bexhoma confirms each override, e.g. `updated deployment[bexhoma-deployment-redis].container[dbms].env.DFLY_proactor_threads = 4`.
A name that does not exist in the template only prints `... not found in file` and changes nothing.

Example: a cluster of 3 workers with 8 instead of 16 io threads per worker

```bash
bexhoma ycsb \
  -dbms Dragonfly \
  -sf 10 \
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
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set "statefulset[bexhoma-worker].container[dbms].env.DFLY_proactor_threads=8" \
  run &>$LOG_DIR/docs_ycsb_dragonfly_cluster_settings.log
```

bexhoma prints `updated statefulset[bexhoma-worker].container[dbms].env.DFLY_proactor_threads = 8`, the summary lists the override under "Deployment parameter overrides", and each worker logs `Running 8 io threads`.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_dragonfly_cluster_settings_summary.md" target="_blank" rel="noopener">docs_ycsb_dragonfly_cluster_settings.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 704s 
* Code: 1792720409
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'statefulset', 'workload': 'bexhoma-worker', 'config': '', 'container': 'dbms', 'param': 'env.DFLY_proactor_threads'}, '8')].
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* dragonflycluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:950859
  * datadisk:1
  * volume_size:1.8T
  * volume_used:929G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:153556
    * datadisk:3549
    * volume_size:219G
    * volume_used:150G
    * cpu_list:0-95
  * worker 1
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:159393
    * datadisk:3753
    * volume_size:219G
    * volume_used:156G
    * cpu_list:0-95
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:406533
    * datadisk:3549
    * volume_size:879G
    * volume_used:398G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792720409
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1792720409-7f6bbc7bf5-f8hf9: 0
* bx-w-dragonfly-ycsb-10-0: 0
* bx-w-dragonfly-ycsb-10-1: 0
* bx-w-dragonfly-ycsb-10-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| dragonflycluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15285.85 |                81775.00 |           1250000.00 |                              1166.00 | 10.00 |              440.23 |
| dragonflycluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15361.74 |                81371.00 |           1250000.00 |                              1165.00 | 10.00 |              442.42 |
| dragonflycluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15307.00 |                81662.00 |           1250000.00 |                              1166.00 | 10.00 |              440.84 |
| dragonflycluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15268.48 |                81868.00 |           1250000.00 |                              1163.00 | 10.00 |              439.73 |
| dragonflycluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15250.60 |                81964.00 |           1250000.00 |                              1169.00 | 10.00 |              439.22 |
| dragonflycluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15166.04 |                82421.00 |           1250000.00 |                              1164.00 | 10.00 |              436.78 |
| dragonflycluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15296.13 |                81720.00 |           1250000.00 |                              1165.00 | 10.00 |              440.53 |
| dragonflycluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15307.18 |                81661.00 |           1250000.00 |                              1165.00 | 10.00 |              440.85 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 10.00 |              436.78 |                       122243.01 |                82421.00 |          10000000.00 |                              1165.38 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1-1-1 | dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64364.98 |               155364.00 |            5000658 |                             226.00 |              4999342 |                               214.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64364.98 |               155364.00 |            5000658 |                             226.00 |              4999342 |                               214.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 |                1 |        1 |               1 |        63.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |      1036.54 |     11.33 |          15.53 |                 15.53 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       637.88 |     10.18 |           1.34 |                  1.35 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       487.56 |      3.54 |          15.48 |                 15.48 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       449.63 |      3.02 |           1.46 |                  1.46 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |            20001601.00 |                15.25 |                     79384.43 |                   49.91 |                    0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             9200775.00 |                15.25 |                     31953.21 |                    3.23 |                    0.00 |

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
* TEST passed: Reset scripts ran without errors
```

</details>

### Schema and Scripts

Dragonfly has no schema; YCSB writes the keys directly via the Redis wire protocol.
The experiment folder [experiments/ycsb/Dragonfly](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Dragonfly) contains the reset script, for single host, cluster and replication alike.

### Load Durability

`-xld` has no effect on Dragonfly: there are no durability scripts for it.
Dragonfly writes its data to disk only on `SAVE` or on shutdown.

### Reset Scripts

With `-ar`, [save-snapshot.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/ycsb/Dragonfly/save-snapshot.sh) runs before each benchmarking round, in the SUT pod (single host) or in every worker (cluster and replication):

1. Statistics: n/a (no optimizer statistics)
2. Persist: `SAVE` writes a snapshot
3. Counters: `CONFIG RESETSTAT`

`SAVE` is not replicated, so each replica writes its own snapshot.
The data pods save under the fixed name `dump` (`DFLY_dbfilename`), so each `SAVE` overwrites the previous snapshot and a restarted pod loads it.
The output of the script is stored per pod in the result folder (`...-reset_<run>_<client>_<benchmark>-...-save-snapshot-<pod>.sh.stdout.log`).

See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract and [Test: Reset Scripts](Test-Reset.md#dragonfly) for the test runs, with results for the [single host](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_dragonfly_summary.md) and [replication](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_dragonfly_replica_summary.md).
