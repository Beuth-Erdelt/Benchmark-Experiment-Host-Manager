# Example: Benchmark Redis

This example shows how to benchmark Redis with YCSB, as a single host and as a cluster managed by bexhoma.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[Redis](https://redis.io/) is an in-memory key-value store.
Bexhoma runs it as a single host (one SUT pod) or as a Redis cluster (`-nw`), where every shard and every replica is a worker pod of a stateful set.
A Redis cluster has no coordinator; bexhoma still deploys a main pod as a single point of contact and to annotate the status of experiments.
YCSB talks to Redis via the Redis wire protocol, not via JDBC.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [Redis](https://redis.io/)
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. Test script of this page: [test-docs-redis.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-redis.sh), [test-docs-redis.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-redis.ps1)


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

The experiment is run with the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example:
```bash
bexhoma ycsb \
  -dbms Redis \
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_redis.log
```

This
* starts a clean instance of Redis (`-dbms`)
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
* shows a summary

### Status

You can watch the status while benchmark is running via `bexhoma status`

```bash
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+-------------------+--------------+------------+------------------------+
| 1741876409        | sut          | use case   | loading                |
+===================+==============+============+========================+
| Redis-64-8-196608 | (1. Running) | ycsb       | (7 Running)(1 Pending) |
+-------------------+--------------+------------+------------------------+
```

The code `1741876409` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1741876409` (removes everything that is related to experiment `1741876409`).

### Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_redis_summary.md" target="_blank" rel="noopener">docs_ycsb_redis.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 184s 
* Code: 1794695478
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
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['Redis'].
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
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046314
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
    * code:1794695478

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Redis-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-redis-1-1794695478-659c4c95b9-xdqwz: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8961.22 |                13949.00 |            125000.00 |                              2044.00 | 1.00 |              258.08 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9159.52 |                13647.00 |            125000.00 |                              2000.00 | 1.00 |              263.79 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9645.06 |                12960.00 |            125000.00 |                              2002.00 | 1.00 |              277.78 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9150.81 |                13660.00 |            125000.00 |                              2010.00 | 1.00 |              263.54 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9467.55 |                13203.00 |            125000.00 |                              1975.00 | 1.00 |              272.67 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10030.49 |                12462.00 |            125000.00 |                              1972.00 | 1.00 |              288.88 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9782.44 |                12778.00 |            125000.00 |                              1973.00 | 1.00 |              281.73 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9654.75 |                12947.00 |            125000.00 |                              1971.00 | 1.00 |              278.06 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              258.08 |                        75851.83 |                13949.00 |           1000000.00 |                              1993.38 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        65082.98 |                15365.00 |             499904 |                            1120.00 |               500096 |                              1056.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        65082.98 |                15365.00 |             499904 |                            1120.00 |               500096 |                              1056.00 |

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

To see the summary again you can simply call `bexhoma summary -e 1741876409` with the experiment code.

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example the [Jupyter notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/notebooks/), in particular [Collector-YCSB.ipynb](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/notebooks/Collector-YCSB.ipynb).

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Monitoring

[Monitoring](Monitoring.md) can be activated for DBMS only (`-m`) or for all components (`-mc`).
Metrics are sampled every few seconds, so the benchmarking phase should take at least a minute.
This run uses SF=3 and 10.000.000 operations (`-xop`).

All metrics in monitoring are summed across all matching components.
For a Redis cluster, this means that used memory, CPU time, etc. are summed across all worker pods.

```bash
bexhoma ycsb \
  -dbms Redis \
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_redis_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_redis_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_redis_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 397s 
* Code: 1794695677
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
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Redis'].
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
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1049920
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
    * code:1794695677

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Redis-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-redis-1-1794695677-5f7577c74d-qqgbk: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7499.25 |                50005.00 |            375000.00 |                              2509.00 | 3.00 |              215.98 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7558.66 |                49612.00 |            375000.00 |                              2527.00 | 3.00 |              217.69 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7520.00 |                49867.00 |            375000.00 |                              2533.00 | 3.00 |              216.58 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7510.36 |                49931.00 |            375000.00 |                              2523.00 | 3.00 |              216.30 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7554.09 |                49642.00 |            375000.00 |                              2513.00 | 3.00 |              217.56 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7536.48 |                49758.00 |            375000.00 |                              2519.00 | 3.00 |              217.05 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7516.69 |                49889.00 |            375000.00 |                              2531.00 | 3.00 |              216.48 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7507.36 |                49951.00 |            375000.00 |                              2511.00 | 3.00 |              216.21 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 3.00 |              215.98 |                        60202.88 |                50005.00 |           3000000.00 |                              2520.75 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        65480.59 |               152717.00 |            4996918 |                            2269.00 |              5003082 |                              2241.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        65480.59 |               152717.00 |            4996918 |                            2269.00 |              5003082 |                              2241.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       297.40 |      4.21 |           4.49 |                  4.50 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       218.24 |      4.53 |           0.28 |                  0.28 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       492.27 |      3.92 |           6.33 |                  6.33 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       488.57 |      4.81 |           1.02 |                  1.03 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
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

Collecting application metrics for Redis is supported for a cluster (`-nw`).
It can be activated by `-m -mc -ma`.
A `redis_exporter` sidecar in every worker pod exposes the metrics on port 9121.
Prometheus discovers the worker pods only, so a single host has no application metrics.
See [Metrics](Example-Metrics.md) for application metrics of all DBMS.

```bash
bexhoma ycsb \
  -dbms Redis \
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
  -nw 3 \
  -nwr 1 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_redis_appmetrics.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_redis_appmetrics_summary.md" target="_blank" rel="noopener">docs_ycsb_redis_appmetrics.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 521s 
* Code: 1794776408
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
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Redis'].
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
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053145
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1388002
    * datadisk:2172
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:638916
    * datadisk:2324
    * cpu_list:0-127
  * worker 2
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:300332
    * datadisk:2182
    * cpu_list:0-255
  * worker 3
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:161733
    * datadisk:2156
    * cpu_list:0-95
  * worker 4
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:890622
    * datadisk:2202
    * cpu_list:0-255
  * worker 5
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:223105
    * datadisk:2431
    * cpu_list:0-127
  * resources_total: 24.25 CPU, 96.5 GiB RAM requested in 7 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 6 x, 24.0 CPU, 96.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794776408
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Redis-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-redis-1-1794776408-6c4df58d44-6jw5n: 0
* bx-w-rd-1-1794776408-0: 0
* bx-w-rd-1-1794776408-1: 0
* bx-w-rd-1-1794776408-2: 0
* bx-w-rd-1-1794776408-3: 0
* bx-w-rd-1-1794776408-4: 0
* bx-w-rd-1-1794776408-5: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6003.36 |                62465.00 |            375000.00 |                              2739.00 | 3.00 |              172.90 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6025.65 |                62234.00 |            375000.00 |                              2741.00 | 3.00 |              173.54 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6010.58 |                62390.00 |            375000.00 |                              2737.00 | 3.00 |              173.10 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         5998.08 |                62520.00 |            375000.00 |                              2737.00 | 3.00 |              172.74 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6042.44 |                62061.00 |            375000.00 |                              2739.00 | 3.00 |              174.02 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6039.23 |                62094.00 |            375000.00 |                              2745.00 | 3.00 |              173.93 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6010.87 |                62387.00 |            375000.00 |                              2733.00 | 3.00 |              173.11 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6010.67 |                62389.00 |            375000.00 |                              2737.00 | 3.00 |              173.11 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 3.00 |              172.74 |                        48140.88 |                62520.00 |           3000000.00 |                              2738.50 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        52073.03 |               192038.00 |            4999208 |                            1679.00 |              5000792 |                              1666.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        52073.03 |               192038.00 |            4999208 |                            1679.00 |              5000792 |                              1666.00 |

### Monitoring

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       444.12 |      5.28 |           9.08 |                  9.09 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       219.80 |      7.00 |           0.94 |                  0.94 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       539.91 |      5.03 |          10.30 |                 10.32 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       837.73 |      5.18 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS          |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [GiB] |   Redis Master Link Status |   Redis Operations Rate, Busiest Instance [ops/s] |
|:--------------|----------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------------------------------:|
| redis-1-1-1-1 |                  6.00 |                      201.00 |                      8.71 |                       3.00 |                                          17745.79 |

#### Benchmarking phase: component worker

| DBMS          |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [GiB] |   Redis Master Link Status |   Redis Operations Rate, Busiest Instance [ops/s] |
|:--------------|----------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------------------------------:|
| redis-1-1-1-1 |                  6.00 |                      393.00 |                      8.71 |                       3.00 |                                          16579.48 |

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
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.md).

Example:
```bash
bexhoma ycsb \
  -dbms Redis \
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
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_redis_storage.log
```

The following status shows a volume of type `shared`.
Every single-host Redis experiment running YCSB of SF=1 will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of Redis mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```bash
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-redis-ycsb-1           | redis           | ycsb-1       | True         |                50 | Redis           | shared               | 50Gi      | Bound    | 50G    | 0      |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_redis_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_redis_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 661s 
* Code: 1794696117
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
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Redis'].
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
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046241
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
    * code:1794696117
* redis-1-2-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1047368
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
    * code:1794696117

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Redis-1-2

### Data Parameters of Reused Volumes
* Redis-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Redis-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-redis-1-1794696117-5fc9bbd9d8-zs72l: 0
* bexhoma-sut-redis-1-1794696117-866b759887-tlbsr: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Redis-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Redis-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10725.01 |                11655.00 |            125000.00 |                              1924.00 | 1.00 |              308.88 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10702.05 |                11680.00 |            125000.00 |                              1947.00 | 1.00 |              308.22 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10634.68 |                11754.00 |            125000.00 |                              1900.00 | 1.00 |              306.28 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10753.61 |                11624.00 |            125000.00 |                              1892.00 | 1.00 |              309.70 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10539.63 |                11860.00 |            125000.00 |                              1951.00 | 1.00 |              303.54 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10310.98 |                12123.00 |            125000.00 |                              1930.00 | 1.00 |              296.96 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10760.09 |                11617.00 |            125000.00 |                              1929.00 | 1.00 |              309.89 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10173.35 |                12287.00 |            125000.00 |                              1951.00 | 1.00 |              292.99 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              292.99 |                        84599.41 |                12287.00 |           1000000.00 |                              1928.00 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        65493.03 |               152688.00 |            4996917 |                             889.00 |              5003083 |                               822.00 |
| redis-1-2-1-1-1 | redis-1-2-1 | redis-1-2-1-1 |                2 |        1 |               1 |       1 |       128 |    65536 |        0 |                        65484.45 |               152708.00 |            4998804 |                            1203.00 |              5001196 |                              1166.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        65493.03 |               152688.00 |            4996917 |                             889.00 |              5003083 |                               822.00 |
| redis-1-2-1 | redis-1-2-1 |                2 |        1 |               1 |           1 |       128 |    65536 |        0 |                        65484.45 |               152708.00 |            4998804 |                            1203.00 |              5001196 |                              1166.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |        76.11 |      2.15 |           1.52 |                  1.53 |

### Loading phase: component loader

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| redis-1-1-1-1 | n/a          |         0 |           0.28 |                  0.28 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       350.46 |      2.62 |           2.18 |                  2.19 |
| redis-1-2-1-1 |       343.50 |      3.97 |           1.73 |                  1.74 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       703.93 |      4.91 |           1.03 |                  1.04 |
| redis-1-2-1-1 |       630.56 |      4.96 |           1.05 |                  1.05 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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


## Variants

### Cluster

If you want to deploy Redis as a cluster, you can set the number of workers `-nw`.
Each worker is a shard of the database.

```bash
bexhoma ycsb \
  -dbms Redis \
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_redis_cluster.log
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_redis_cluster_summary.md" target="_blank" rel="noopener">docs_ycsb_redis_cluster.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 391s 
* Code: 1794696820
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
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Redis'].
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
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1049313
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:668988
    * datadisk:721
    * cpu_list:0-127
  * worker 1
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:889294
    * datadisk:792
    * cpu_list:0-255
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1387365
    * datadisk:719
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794696820
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Redis-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-redis-1-1794696820-5ccb75ffdb-8kfcw: 0
* bx-w-rd-1-1794696820-0: 0
* bx-w-rd-1-1794696820-1: 0
* bx-w-rd-1-1794696820-2: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4193.79 |                29806.00 |            125000.00 |                              4183.00 | 1.00 |              120.78 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4211.45 |                29681.00 |            125000.00 |                              4127.00 | 1.00 |              121.29 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4186.20 |                29860.00 |            125000.00 |                              4147.00 | 1.00 |              120.56 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4193.51 |                29808.00 |            125000.00 |                              4119.00 | 1.00 |              120.77 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4212.16 |                29676.00 |            125000.00 |                              4095.00 | 1.00 |              121.31 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4185.22 |                29867.00 |            125000.00 |                              4115.00 | 1.00 |              120.53 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4162.23 |                30032.00 |            125000.00 |                              4131.00 | 1.00 |              119.87 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4165.14 |                30011.00 |            125000.00 |                              4131.00 | 1.00 |              119.96 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              119.87 |                        33509.69 |                30032.00 |           1000000.00 |                              4131.00 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        60934.37 |               164111.00 |            4993725 |                            1839.00 |              5006275 |                              1823.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        60934.37 |               164111.00 |            4993725 |                            1839.00 |              5006275 |                              1823.00 |

### Monitoring

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |        90.69 |      2.18 |           1.49 |                  1.49 |

### Loading phase: component loader

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| redis-1-1-1-1 | n/a          |         0 |           0.18 |                  0.18 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       276.17 |      2.16 |           1.80 |                  1.87 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       556.29 |      5.43 |           1.49 |                  1.49 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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

A Redis cluster can store the database in persistent storage, too.
This removes existing storage via `-rsr` to start with a clean copy.

```bash
bexhoma ycsb \
  -dbms Redis \
  -sf 3 \
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
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_redis_cluster_storage.log
```

The first volume is attached to the (dummy) coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.

```bash
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-redis-ycsb-1           | redis           | ycsb-1       | True         |                48 | Redis           | shared               | 50Gi      | Bound    | 0      | 0      |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+

+-------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| Volumes of Workers      | configuration     |   experiment | dbms   | storage_class_name   | storage   | status   | size   | used   |
+=========================+===================+==============+========+======================+===========+==========+========+========+
| bxw-bx-w-redis-ycsb-1-0 | Redis-64-8-196608 |   1742468798 | Redis  | shared               | 50Gi      | Bound    | 50G    | 708M   |
+-------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bxw-bx-w-redis-ycsb-1-1 | Redis-64-8-196608 |   1742468798 | Redis  | shared               | 50Gi      | Bound    | 50G    | 800M   |
+-------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bxw-bx-w-redis-ycsb-1-2 | Redis-64-8-196608 |   1742468798 | Redis  | shared               | 50Gi      | Bound    | 50G    | 708M   |
+-------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_redis_cluster_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_redis_cluster_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 840s 
* Code: 1794697258
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
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Redis'].
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
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1076545
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:888229
    * datadisk:2169
    * volume_size:49G
    * volume_used:2.2G
    * cpu_list:0-255
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662475
    * datadisk:2445
    * volume_size:49G
    * volume_used:2.4G
    * cpu_list:0-127
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381310
    * datadisk:2172
    * volume_size:49G
    * volume_used:2.2G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794697258
    * BEXHOMA_WORKERS:3
* redis-1-2-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1078137
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662333
    * datadisk:2424
    * volume_size:49G
    * volume_used:2.4G
    * cpu_list:0-127
  * worker 1
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:888229
    * datadisk:3077
    * volume_size:49G
    * volume_used:3.1G
    * cpu_list:0-255
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381310
    * datadisk:2435
    * volume_size:49G
    * volume_used:2.4G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794697258
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Redis-1-2

### Data Parameters of Reused Volumes
* Redis-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Redis-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-redis-1-1794697258-fcfff9cd5-2z6hm: 0
* bx-w-rd-nvme-ycsb-3-0: 0
* bx-w-rd-nvme-ycsb-3-1: 0
* bx-w-rd-nvme-ycsb-3-2: 0
* bexhoma-sut-redis-1-1794697258-578d9fb567-7zqm2: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Redis-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Redis-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6247.81 |                60021.00 |            375000.00 |                              2787.00 | 3.00 |              179.94 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6172.43 |                60754.00 |            375000.00 |                              2789.00 | 3.00 |              177.77 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6173.86 |                60740.00 |            375000.00 |                              2793.00 | 3.00 |              177.81 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6149.56 |                60980.00 |            375000.00 |                              2791.00 | 3.00 |              177.11 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6199.58 |                60488.00 |            375000.00 |                              2777.00 | 3.00 |              178.55 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6183.83 |                60642.00 |            375000.00 |                              2793.00 | 3.00 |              178.09 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6172.43 |                60754.00 |            375000.00 |                              2789.00 | 3.00 |              177.77 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6234.00 |                60154.00 |            375000.00 |                              2785.00 | 3.00 |              179.54 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 3.00 |              177.11 |                        49533.50 |                60980.00 |           3000000.00 |                              2788.00 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        62299.86 |               160514.00 |            4999806 |                            2012.00 |              5000194 |                              2001.00 |
| redis-1-2-1-1-1 | redis-1-2-1 | redis-1-2-1-1 |                2 |        1 |               1 |       1 |       128 |    65536 |        0 |                        63919.00 |               156448.00 |            5001439 |                            2855.00 |              4998561 |                              2865.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        62299.86 |               160514.00 |            4999806 |                            2012.00 |              5000194 |                              2001.00 |
| redis-1-2-1 | redis-1-2-1 |                2 |        1 |               1 |           1 |       128 |    65536 |        0 |                        63919.00 |               156448.00 |            5001439 |                            2855.00 |              4998561 |                              2865.00 |

### Monitoring

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       221.60 |      3.25 |           4.47 |                  4.48 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       243.18 |      6.73 |           0.80 |                  0.80 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       342.03 |      3.28 |           4.89 |                  4.91 |
| redis-1-2-1-1 |       354.55 |      3.68 |           4.51 |                  4.52 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       670.00 |      5.10 |           1.49 |                  1.49 |
| redis-1-2-1-1 |       639.28 |      4.99 |           1.47 |                  1.48 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

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

### Replication

The parameter `-nwr` sets the number of replicas.
Redis requires a worker per replicated shard, so `-nw 3` and `-nwr 1` create 6 worker pods, 3 for sharding and another 3 for the (single) replicas.

```bash
bexhoma ycsb \
  -dbms Redis \
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_redis_replica.log
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_redis_replica_summary.md" target="_blank" rel="noopener">docs_ycsb_redis_replica.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 485s 
* Code: 1794698141
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
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Redis'].
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
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046400
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:667921
    * datadisk:721
    * cpu_list:0-127
  * worker 1
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:889014
    * datadisk:785
    * cpu_list:0-255
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1385139
    * datadisk:720
    * cpu_list:0-127
  * worker 3
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:298670
    * datadisk:722
    * cpu_list:0-255
  * worker 4
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:129533
    * datadisk:719
    * cpu_list:0-95
  * worker 5
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:212213
    * datadisk:802
    * cpu_list:0-127
  * resources_total: 24.25 CPU, 384.5 GiB RAM requested in 7 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 6 x, 24.0 CPU, 384.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794698141
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Redis-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-redis-1-1794698141-865769db75-fmjlf: 0
* bx-w-rd-1-1794698141-0: 0
* bx-w-rd-1-1794698141-1: 0
* bx-w-rd-1-1794698141-2: 0
* bx-w-rd-1-1794698141-3: 0
* bx-w-rd-1-1794698141-4: 0
* bx-w-rd-1-1794698141-5: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4290.08 |                29137.00 |            125000.00 |                              3569.00 | 1.00 |              123.55 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4250.69 |                29407.00 |            125000.00 |                              3545.00 | 1.00 |              122.42 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4224.11 |                29592.00 |            125000.00 |                              3551.00 | 1.00 |              121.65 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4232.41 |                29534.00 |            125000.00 |                              3545.00 | 1.00 |              121.89 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4270.29 |                29272.00 |            125000.00 |                              3551.00 | 1.00 |              122.98 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4247.08 |                29432.00 |            125000.00 |                              3551.00 | 1.00 |              122.32 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4221.97 |                29607.00 |            125000.00 |                              3577.00 | 1.00 |              121.59 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4254.88 |                29378.00 |            125000.00 |                              3555.00 | 1.00 |              122.54 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              121.59 |                        33991.52 |                29607.00 |           1000000.00 |                              3555.50 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        52003.97 |               192293.00 |            4998178 |                            8967.00 |              5001822 |                              8999.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        52003.97 |               192293.00 |            4998178 |                            8967.00 |              5001822 |                              8999.00 |

### Monitoring

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       168.01 |      3.74 |           3.09 |                  3.12 |

### Loading phase: component loader

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| redis-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       422.98 |      3.34 |           3.50 |                  3.52 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       733.93 |      5.40 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
'Redis': {
    'abbreviation': 'rd',
    'loadData': 'redis-cli --host bexhoma-service.{namespace}.svc.cluster.local < {scriptname}',
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
    'monitor': { ... },  # Prometheus discovery for worker pods on port 9121 (redis_exporter)
},
```

where
* `abbreviation`: short name in the names of volumes and worker pods
* `loadData`: command to run a script, here via `redis-cli` against the bexhoma service
* `monitor`: Prometheus discovery of the worker pods of a cluster, scraping the `redis_exporter` on port 9121

There is no `JDBC` section, as Redis has no JDBC driver.

### Deployment

* Single host: [deploymenttemplate-Redis.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Redis.yml), one SUT pod with Redis, a `redis_exporter` and a cAdvisor sidecar.
* Cluster (`-nw` > 0): [deploymenttemplate-RedisCluster.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-RedisCluster.yml), a stateful set of `-nw` * (1 + `-nwr`) worker pods with `--cluster-enabled yes` and `--appendonly yes`, and a job that creates the cluster with `redis-cli --cluster create` once all workers answer.
  * The SUT pod is a placeholder: the data lives in the workers, and the SUT pod is not monitored.
  * Shell scripts run on every worker (script target `workers`).
  * Redis expects a fully qualified domain name (FQDN) for each pod, while the length of hostnames is limited. Therefore bexhoma shortens the names of the worker pods and their volumes.
* Bexhoma also deploys a service for communication external to Redis (from within the cluster) and a headless service for communication between the pods of the Redis cluster.

### Schema and Scripts

Redis has no schema; YCSB writes the keys directly via the Redis wire protocol.
The experiment folder [experiments/ycsb/Redis](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Redis) contains only the reset script.

### Load Durability

`-xld` has no effect on Redis: there are no durability scripts for it.
The single host keeps the default persistence (RDB snapshots), the cluster also writes an append-only file (`--appendonly yes`).

### Reset Scripts

With `-ar`, [save-snapshot.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/ycsb/Redis/save-snapshot.sh) runs before each benchmarking round, in the SUT pod (single host) or in every worker (cluster):

1. Statistics: n/a (no optimizer statistics)
2. Persist: waits for a running background save, then `SAVE` writes an RDB snapshot synchronously
3. Counters: `CONFIG RESETSTAT`

See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract and [Test: Reset Scripts](Test-Reset.md#redis) for the test runs, with results for the [single host](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_redis_summary.md) and the [cluster](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_redis_cluster_summary.md).
