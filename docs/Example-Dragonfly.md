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
* Duration: 184s 
* Code: 1794039483
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
  * Experiment uses bexhoma version 0.11.13.
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
  * disk:805934
  * datadisk:1086
  * volume_size:1.8T
  * volume_used:788G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794039483

### Init Scripts Not in Folder
* Dragonfly-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonfly-1-1794039483-797b84d4f6-vb952: 0

### Workflow

#### Actual

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24281.27 |                 5148.00 |            125000.00 |                               603.00 | 1.00 |              699.30 |
| dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24163.93 |                 5173.00 |            125000.00 |                               655.00 | 1.00 |              695.92 |
| dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24271.84 |                 5150.00 |            125000.00 |                               571.00 | 1.00 |              699.03 |
| dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24314.34 |                 5141.00 |            125000.00 |                               637.00 | 1.00 |              700.25 |
| dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24262.42 |                 5152.00 |            125000.00 |                               735.00 | 1.00 |              698.76 |
| dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24234.20 |                 5158.00 |            125000.00 |                               615.00 | 1.00 |              697.94 |
| dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24314.34 |                 5141.00 |            125000.00 |                               594.00 | 1.00 |              700.25 |
| dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24300.16 |                 5144.00 |            125000.00 |                               692.00 | 1.00 |              699.84 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              695.92 |                       194142.50 |                 5173.00 |           1000000.00 |                               637.75 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1-1-1 | dragonfly-1-1-1 | dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64968.81 |                15392.00 |             500819 |                             868.00 |               499181 |                               747.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1 | dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64968.81 |                15392.00 |             500819 |                             868.00 |               499181 |                               747.00 |

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
* Duration: 408s 
* Code: 1794039683
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
  * Experiment uses bexhoma version 0.11.13.
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
  * disk:808106
  * datadisk:3256
  * volume_size:1.8T
  * volume_used:790G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794039683

### Init Scripts Not in Folder
* Dragonfly-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonfly-1-1794039683-768b9db68b-lsgl5: 0

### Workflow

#### Actual

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24482.60 |                15317.00 |            375000.00 |                               560.00 | 3.00 |              705.10 |
| dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24489.00 |                15313.00 |            375000.00 |                               632.00 | 3.00 |              705.28 |
| dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24479.40 |                15319.00 |            375000.00 |                               718.00 | 3.00 |              705.01 |
| dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24482.60 |                15317.00 |            375000.00 |                               630.00 | 3.00 |              705.10 |
| dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24474.61 |                15322.00 |            375000.00 |                               558.00 | 3.00 |              704.87 |
| dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24450.67 |                15337.00 |            375000.00 |                               568.00 | 3.00 |              704.18 |
| dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24482.60 |                15317.00 |            375000.00 |                               637.00 | 3.00 |              705.10 |
| dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24476.21 |                15321.00 |            375000.00 |                               583.00 | 3.00 |              704.91 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 3.00 |              704.18 |                       195817.70 |                15337.00 |           3000000.00 |                               610.75 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1-1-1 | dragonfly-1-1-1 | dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65461.31 |               152762.00 |            4999894 |                             839.00 |              5000106 |                               790.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1 | dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65461.31 |               152762.00 |            4999894 |                             839.00 |              5000106 |                               790.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       168.29 |      5.44 |           4.69 |                  4.69 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 | n/a          |         0 |           0.53 |                  0.53 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       414.15 |      3.09 |           4.63 |                  4.63 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       583.96 |      6.15 |           1.04 |                  1.04 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
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
| dragonfly-1-1-1-1 |             6000000.00 |                 4.54 |                     29766.67 |                   18.79 |                    0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonfly-1-1-1-1 |             9713914.00 |                 4.54 |                     53153.83 |                   16.88 |                    0.00 |

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
* Duration: 728s 
* Code: 1794040133
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
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
* dragonfly-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:804842
  * datadisk:1086
  * volume_size:49G
  * volume_used:1.1G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794040133
* dragonfly-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:804843
  * datadisk:1086
  * volume_size:49G
  * volume_used:1.1G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794040133

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Dragonfly-1-2

### Data Parameters of Reused Volumes
* Dragonfly-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Dragonfly-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonfly-1-1794040133-546c48698f-vzdg5: 0
* bexhoma-sut-dragonfly-1-1794040133-567b5f5bbd-67xnl: 0

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
| dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        23941.77 |                 5221.00 |            125000.00 |                               711.00 | 1.00 |              689.52 |
| dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24304.88 |                 5143.00 |            125000.00 |                               586.00 | 1.00 |              699.98 |
| dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24267.13 |                 5151.00 |            125000.00 |                               614.00 | 1.00 |              698.89 |
| dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24281.27 |                 5148.00 |            125000.00 |                               878.00 | 1.00 |              699.30 |
| dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24323.80 |                 5139.00 |            125000.00 |                               638.00 | 1.00 |              700.53 |
| dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24267.13 |                 5151.00 |            125000.00 |                               652.00 | 1.00 |              698.89 |
| dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24262.42 |                 5152.00 |            125000.00 |                               621.00 | 1.00 |              698.76 |
| dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24271.84 |                 5150.00 |            125000.00 |                               623.00 | 1.00 |              699.03 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              689.52 |                       193920.26 |                 5221.00 |           1000000.00 |                               665.38 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1-1-1 | dragonfly-1-1-1 | dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65481.45 |               152715.00 |            4996545 |                             781.00 |              5003455 |                               762.00 |
| dragonfly-1-2-1-1-1 | dragonfly-1-2-1 | dragonfly-1-2-1-1 | Dragonfly-1     |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65448.88 |               152791.00 |            5000110 |                             793.00 |              4999890 |                               772.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1 | dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65481.45 |               152715.00 |            4996545 |                             781.00 |              5003455 |                               762.00 |
| dragonfly-1-2-1 | dragonfly-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        65448.88 |               152791.00 |            5000110 |                             793.00 |              4999890 |                               772.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonfly-1-1-1 | dragonfly-1-1-1-1 |                1 |        1 |               1 |        12.00 |                |
| dragonfly-1-2-1 | dragonfly-1-2-1-1 |                2 |        1 |               1 |        12.00 |                |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |        63.88 |      1.72 |           1.65 |                  1.65 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       457.38 |      3.03 |           1.60 |                  1.60 |
| dragonfly-1-2-1-1 |       426.73 |      3.97 |           1.69 |                  2.75 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       639.74 |      5.23 |           1.37 |                  1.37 |
| dragonfly-1-2-1-1 |       730.85 |      6.69 |           1.05 |                  1.05 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonfly-1-1-1-1 |             2000000.00 |                 1.53 |                     13177.01 |                    8.32 |                    0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonfly-1-1-1-1 |             8531554.00 |                 1.53 |                     37933.12 |                    7.65 |                    0.00 |
| dragonfly-1-2-1-1 |             8474139.00 |                 1.63 |                     31871.08 |                    3.22 |                    0.00 |

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
* TEST passed: Reset scripts ran without errors
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
* Duration: 415s 
* Code: 1794040924
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
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
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* dragonflycluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:804836
  * datadisk:1
  * volume_size:1.8T
  * volume_used:786G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:206328
    * datadisk:356
    * volume_size:879G
    * volume_used:202G
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:717392
    * datadisk:377
    * volume_size:1.8T
    * volume_used:701G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:663359
    * datadisk:355
    * volume_size:1.8T
    * volume_used:648G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794040924
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* DragonflyCluster-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1794040924-665fd78dbd-wjc6k: 0
* bx-w-dragonflycluster-1-1794040924-0: 0
* bx-w-dragonflycluster-1-1794040924-1: 0
* bx-w-dragonflycluster-1-1794040924-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonflycluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17700.37 |                 7062.00 |            125000.00 |                               774.00 | 1.00 |              509.77 |
| dragonflycluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17864.80 |                 6997.00 |            125000.00 |                               763.00 | 1.00 |              514.51 |
| dragonflycluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18910.74 |                 6610.00 |            125000.00 |                               631.00 | 1.00 |              544.63 |
| dragonflycluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        19180.60 |                 6517.00 |            125000.00 |                               652.00 | 1.00 |              552.40 |
| dragonflycluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18808.31 |                 6646.00 |            125000.00 |                               696.00 | 1.00 |              541.68 |
| dragonflycluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        19549.58 |                 6394.00 |            125000.00 |                               633.00 | 1.00 |              563.03 |
| dragonflycluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17775.88 |                 7032.00 |            125000.00 |                               763.00 | 1.00 |              511.95 |
| dragonflycluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        19275.25 |                 6485.00 |            125000.00 |                               660.00 | 1.00 |              555.13 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              509.77 |                       149065.53 |                 7062.00 |           1000000.00 |                               696.50 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1-1-1 | dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        61335.39 |               163038.00 |            4999755 |                             267.00 |              5000245 |                               251.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        61335.39 |               163038.00 |            4999755 |                             267.00 |              5000245 |                               251.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 |                1 |        1 |               1 |        15.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       109.17 |      3.68 |           1.64 |                  1.64 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       554.43 |      3.77 |           1.68 |                  2.03 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       632.02 |      4.93 |           1.48 |                  1.48 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log)
* Replica Lag [records] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             2001602.00 |                 1.52 |                     10258.04 |                    7.23 |                    0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             9179925.00 |                 1.52 |                     38832.80 |                    7.49 |                    0.00 |

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
* TEST failed: Monitoring metrics missing
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Reset scripts ran without errors
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
* Duration: 815s 
* Code: 1794041379
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
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
* dragonflycluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:804839
  * datadisk:1
  * volume_size:1.8T
  * volume_used:786G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:204333
    * datadisk:356
    * volume_size:49G
    * volume_used:356M
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716984
    * datadisk:377
    * volume_size:49G
    * volume_used:377M
    * cpu_list:0-127
  * worker 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:663004
    * datadisk:355
    * volume_size:49G
    * volume_used:355M
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794041379
    * BEXHOMA_WORKERS:3
* dragonflycluster-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:804840
  * datadisk:1
  * volume_size:1.8T
  * volume_used:786G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:204333
    * datadisk:356
    * volume_size:49G
    * volume_used:356M
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716985
    * datadisk:377
    * volume_size:49G
    * volume_used:377M
    * cpu_list:0-127
  * worker 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:663004
    * datadisk:355
    * volume_size:49G
    * volume_used:355M
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794041379
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: DragonflyCluster-1-2

### Data Parameters of Reused Volumes
* DragonflyCluster-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* DragonflyCluster-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1794041379-6b877b8495-9ktgn: 0
* bx-w-df-nvme-ycsb-1-0: 0
* bx-w-df-nvme-ycsb-1-1: 0
* bx-w-df-nvme-ycsb-1-2: 0
* bexhoma-sut-dragonflycluster-1-1794041379-7554fbf7d5-bgvf6: 0

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
| dragonflycluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        20709.08 |                 6036.00 |            125000.00 |                               578.00 | 1.00 |              596.42 |
| dragonflycluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18862.23 |                 6627.00 |            125000.00 |                               671.00 | 1.00 |              543.23 |
| dragonflycluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        20193.86 |                 6190.00 |            125000.00 |                               580.00 | 1.00 |              581.58 |
| dragonflycluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18950.88 |                 6596.00 |            125000.00 |                               682.00 | 1.00 |              545.79 |
| dragonflycluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        20233.09 |                 6178.00 |            125000.00 |                               712.00 | 1.00 |              582.71 |
| dragonflycluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18976.77 |                 6587.00 |            125000.00 |                               681.00 | 1.00 |              546.53 |
| dragonflycluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        20538.94 |                 6086.00 |            125000.00 |                               581.00 | 1.00 |              591.52 |
| dragonflycluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17977.85 |                 6953.00 |            125000.00 |                               721.00 | 1.00 |              517.76 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              517.76 |                       156442.70 |                 6953.00 |           1000000.00 |                               650.75 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1-1-1 | dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        62484.77 |               160039.00 |            5001142 |                             256.00 |              4998858 |                               241.00 |
| dragonflycluster-1-2-1-1-1 | dragonflycluster-1-2-1 | dragonflycluster-1-2-1-1 | DragonflyCluster-1 |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        62119.52 |               160980.00 |            5002813 |                             259.00 |              4997187 |                               243.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        62484.77 |               160039.00 |            5001142 |                             256.00 |              4998858 |                               241.00 |
| dragonflycluster-1-2-1 | dragonflycluster-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        62119.52 |               160980.00 |            5002813 |                             259.00 |              4997187 |                               243.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 |                1 |        1 |               1 |        16.00 |                |
| dragonflycluster-1-2-1 | dragonflycluster-1-2-1-1 |                2 |        1 |               1 |        16.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       124.69 |      3.82 |           1.65 |                  1.65 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       485.40 |      4.02 |           1.67 |                  1.67 |
| dragonflycluster-1-2-1-1 |       559.74 |      4.30 |           1.78 |                  2.48 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       729.02 |      4.95 |           1.49 |                  1.49 |
| dragonflycluster-1-2-1-1 |       639.78 |      5.19 |           1.48 |                  1.49 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Tx Total [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Rx Total [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
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
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             2001631.00 |                 1.52 |                     12728.40 |                    7.70 |                    0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             9017601.00 |                 1.52 |                     33388.58 |                    6.95 |                    0.00 |
| dragonflycluster-1-2-1-1 |             9025007.00 |                 1.61 |                     32678.29 |                    3.30 |                    0.00 |

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
* TEST passed: Reset scripts ran without errors
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
* Duration: 431s 
* Code: 1794042234
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
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
  * Distributed DBMS uses 3 worker nodes, 1 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* dragonflycluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806433
  * datadisk:1
  * volume_size:1.8T
  * volume_used:788G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:207102
    * datadisk:1086
    * volume_size:879G
    * volume_used:203G
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:718071
    * datadisk:1086
    * volume_size:1.8T
    * volume_used:702G
    * cpu_list:0-127
  * worker 2
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:318358
    * datadisk:1086
    * volume_size:439G
    * volume_used:311G
    * cpu_list:0-255
  * resources_total: 13.0 CPU, 49.0 GiB RAM requested in 4 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794042234
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* DragonflyCluster-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1794042234-558cd9dffb-dbrsr: 0
* bx-w-dragonflycluster-1-1794042234-0: 0
* bx-w-dragonflycluster-1-1794042234-1: 0
* bx-w-dragonflycluster-1-1794042234-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonflycluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        19293.10 |                 6479.00 |            125000.00 |                               892.00 | 1.00 |              555.64 |
| dragonflycluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16747.05 |                 7464.00 |            125000.00 |                              1136.00 | 1.00 |              482.32 |
| dragonflycluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16443.04 |                 7602.00 |            125000.00 |                              1145.00 | 1.00 |              473.56 |
| dragonflycluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15603.55 |                 8011.00 |            125000.00 |                              1202.00 | 1.00 |              449.38 |
| dragonflycluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18293.58 |                 6833.00 |            125000.00 |                               904.00 | 1.00 |              526.85 |
| dragonflycluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        19722.31 |                 6338.00 |            125000.00 |                               867.00 | 1.00 |              568.00 |
| dragonflycluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18729.40 |                 6674.00 |            125000.00 |                               886.00 | 1.00 |              539.41 |
| dragonflycluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15169.90 |                 8240.00 |            125000.00 |                              1237.00 | 1.00 |              436.89 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              436.89 |                       140001.93 |                 8240.00 |           1000000.00 |                              1033.62 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1-1-1 | dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65495.61 |               152682.00 |            5001894 |                             212.00 |              4998106 |                               199.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65495.61 |               152682.00 |            5001894 |                             212.00 |              4998106 |                               199.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 |                1 |        1 |               1 |        20.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       197.03 |      4.26 |           6.05 |                  6.05 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       503.83 |      3.78 |           5.96 |                  5.96 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       575.54 |      4.86 |           1.03 |                  1.03 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Rx Total [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Tx Total [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             2000000.00 |                 4.60 |                     34302.75 |                    8.31 |                    0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             9897320.00 |                 4.60 |                     71739.01 |                    6.89 |                 2042.00 |

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
* TEST passed: Reset scripts ran without errors
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
* Duration: 655s 
* Code: 1794042705
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
  * Experiment uses bexhoma version 0.11.13.
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
  * Deployment parameter overrides: [({'kind': 'statefulset', 'workload': 'bexhoma-worker', 'config': '', 'container': 'dbms', 'param': 'env.DFLY_proactor_threads', 'target': 'container'}, '8')].
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* dragonflycluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808027
  * datadisk:1
  * volume_size:1.8T
  * volume_used:790G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:207850
    * datadisk:3549
    * volume_size:879G
    * volume_used:203G
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:720739
    * datadisk:3753
    * volume_size:1.8T
    * volume_used:704G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:666553
    * datadisk:3549
    * volume_size:1.8T
    * volume_used:651G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794042705
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* DragonflyCluster-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1794042705-6d8c6c9fcc-vngvq: 0
* bx-w-dragonflycluster-1-1794042705-0: 0
* bx-w-dragonflycluster-1-1794042705-1: 0
* bx-w-dragonflycluster-1-1794042705-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| dragonflycluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        14424.35 |                86659.00 |           1250000.00 |                              1310.00 | 10.00 |              415.42 |
| dragonflycluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        14498.47 |                86216.00 |           1250000.00 |                              1314.00 | 10.00 |              417.56 |
| dragonflycluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13667.77 |                91456.00 |           1250000.00 |                              1305.00 | 10.00 |              393.63 |
| dragonflycluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        14141.55 |                88392.00 |           1250000.00 |                              1313.00 | 10.00 |              407.28 |
| dragonflycluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13780.94 |                90705.00 |           1250000.00 |                              1308.00 | 10.00 |              396.89 |
| dragonflycluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        14217.31 |                87921.00 |           1250000.00 |                              1307.00 | 10.00 |              409.46 |
| dragonflycluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13914.71 |                89833.00 |           1250000.00 |                              1310.00 | 10.00 |              400.74 |
| dragonflycluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        14543.68 |                85948.00 |           1250000.00 |                              1307.00 | 10.00 |              418.86 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 10.00 |              393.63 |                       113188.78 |                91456.00 |          10000000.00 |                              1309.25 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1-1-1 | dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        61546.79 |               162478.00 |            5003327 |                             267.00 |              4996673 |                               251.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        61546.79 |               162478.00 |            5003327 |                             267.00 |              4996673 |                               251.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 |                1 |        1 |               1 |        72.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |      1082.14 |     10.44 |          15.71 |                 22.40 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       638.30 |      9.04 |           1.33 |                  1.34 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       432.45 |      3.34 |          15.59 |                 19.05 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       723.43 |      4.84 |           1.50 |                  1.50 |

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
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |            20001603.00 |                15.25 |                     81357.06 |                   51.80 |                    0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             8564923.00 |                15.25 |                     31325.90 |                    4.48 |                    0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
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
