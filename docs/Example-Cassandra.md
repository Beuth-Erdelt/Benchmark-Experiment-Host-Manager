# Example: Benchmark Cassandra

This example shows how to benchmark Apache Cassandra with YCSB, as a single node and as a cluster managed by bexhoma.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[Apache Cassandra](https://cassandra.apache.org/) is a wide-column store, licensed under Apache 2.0 (which has no restriction on publishing benchmark results).
This page uses the image `cassandra:5.0.9`.
Bexhoma runs it as a single node (one SUT pod) or as a cluster (`-nw`), where every node is a worker pod of a stateful set.
Cassandra has no coordinator node, every node answers clients.
Bexhoma still deploys a main pod as a single point of contact, to run `cqlsh` for the scripts and to annotate the status of experiments.
YCSB runs its `cassandra-cql` binding, not JDBC.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [Apache Cassandra](https://cassandra.apache.org/)
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. [cassandra_exporter](https://github.com/criteo/cassandra_exporter)
1. Test script of this page: [test-docs-cassandra.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cassandra.sh), [test-docs-cassandra.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cassandra.ps1)


## Perform YCSB Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker36"
BEXHOMA_NODE_LOAD="cl-worker38"
BEXHOMA_NODE_BENCHMARK="cl-worker38"
BEXHOMA_NODES_WORKER="cl-worker36+cl-worker37+cl-worker29"
LOG_DIR="./logs_tests"
BEXHOMA_STORAGE_CLASS="nvme"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example:
```bash
bexhoma ycsb \
  -dbms Cassandra \
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
  -ar \
  -lr 16Gi \
  -rr 16Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cassandra.log
```

This
* starts a clean instance of Cassandra (`-dbms`)
  * data directory inside a Docker container
* creates the keyspace `ycsb` and the table `usertable`
* starts 8 loader pods (`-nlp`)
  * threads = 64/8 per pod (`-nlt`)
  * target throughput is 12 * 16384 (`-xnlf`, `-xtb`)
  * generates YCSB data = 1.000.000 rows (i.e., SF=1, `-sf`)
  * imports it into the DBMS
* flushes the data and waits for the compactions, after loading and before each benchmarking round (`-ar`)
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
+--------------+--------------+--------------+------------+--------------+-------------------+-----------------------------------+
| 1793442538   | sut          |   loaded [s] | use case   | monitoring   | benchmarker       | phase                             |
+==============+==============+==============+============+==============+===================+===================================+
| Cassandra-1  | (1. Running) |           24 | ycsb       | (Running)    | 1x (1. Succeeded) | Benchmarking (run 1/1, round 1/1) |
+--------------+--------------+--------------+------------+--------------+-------------------+-----------------------------------+
```

The code `1793442538` is the unique identifier of the experiment.
You can find the number also in the output of the benchmark script.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1793442538` (removes everything that is related to experiment `1793442538`).

### Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 261s 
* Code: 1793706227
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['Cassandra'].
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
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* cassandra-1-1-1-1 uses docker image cassandra:5.0.9
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:792871
  * datadisk:1090
  * volume_size:1.8T
  * volume_used:775G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793706227

### SUT Container Restarts
* bexhoma-sut-cassandra-1-1793706227-548dd7596d-qwqvl: 0

### Workflow

#### Actual

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandra-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11799.13 |                10594.00 |            125000.00 |                              1427.00 | 1.00 |              339.81 |
| cassandra-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12572.92 |                 9942.00 |            125000.00 |                              1430.00 | 1.00 |              362.10 |
| cassandra-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13035.77 |                 9589.00 |            125000.00 |                              1293.00 | 1.00 |              375.43 |
| cassandra-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        14290.61 |                 8747.00 |            125000.00 |                              1199.00 | 1.00 |              411.57 |
| cassandra-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12957.40 |                 9647.00 |            125000.00 |                              1272.00 | 1.00 |              373.17 |
| cassandra-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        14306.97 |                 8737.00 |            125000.00 |                              1106.00 | 1.00 |              412.04 |
| cassandra-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11743.71 |                10644.00 |            125000.00 |                              1332.00 | 1.00 |              338.22 |
| cassandra-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11651.75 |                10728.00 |            125000.00 |                              1257.00 | 1.00 |              335.57 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Cassandra-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              335.57 |                       102358.26 |                10728.00 |           1000000.00 |                              1289.50 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1-1-1 | cassandra-1-1-1 | cassandra-1-1-1-1 | Cassandra-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        50231.06 |                19908.00 |             499653 |                            5219.00 |               500347 |                              4507.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1 | cassandra-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        50231.06 |                19908.00 |             499653 |                            5219.00 |               500347 |                              4507.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |         2.00 |                |

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
* TEST passed: Reset scripts ran without errors
```

</details>

To see the summary again you can simply call `bexhoma summary -e 1793442538` with the experiment code.

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
For a Cassandra cluster, this means that used memory, CPU time, etc. are summed across all nodes.

```bash
bexhoma ycsb \
  -dbms Cassandra \
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
  -ar \
  -lr 16Gi \
  -rr 16Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cassandra_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 389s 
* Code: 1793705776
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Cassandra'].
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
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* cassandra-1-1-1-1 uses docker image cassandra:5.0.9
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:798442
  * datadisk:3205
  * volume_size:1.8T
  * volume_used:780G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793705776

### SUT Container Restarts
* bexhoma-sut-cassandra-1-1793705776-787f4dc8c4-hgvpq: 0

### Workflow

#### Actual

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandra-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12457.64 |                30102.00 |            375000.00 |                              1412.00 | 3.00 |              358.78 |
| cassandra-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12907.45 |                29053.00 |            375000.00 |                              1343.00 | 3.00 |              371.73 |
| cassandra-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16389.14 |                22881.00 |            375000.00 |                              1069.00 | 3.00 |              472.01 |
| cassandra-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12023.86 |                31188.00 |            375000.00 |                              1489.00 | 3.00 |              346.29 |
| cassandra-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13821.83 |                27131.00 |            375000.00 |                              1236.00 | 3.00 |              398.07 |
| cassandra-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        14694.93 |                25519.00 |            375000.00 |                              1238.00 | 3.00 |              423.21 |
| cassandra-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12509.17 |                29978.00 |            375000.00 |                              1402.00 | 3.00 |              360.26 |
| cassandra-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12481.28 |                30045.00 |            375000.00 |                              1422.00 | 3.00 |              359.46 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Cassandra-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 3.00 |              346.29 |                       107285.30 |                31188.00 |           3000000.00 |                              1326.38 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1-1-1 | cassandra-1-1-1 | cassandra-1-1-1-1 | Cassandra-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        58703.70 |               170347.00 |            4999793 |                            4355.00 |              5000207 |                              4151.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1 | cassandra-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        58703.70 |               170347.00 |            4999793 |                            4355.00 |              5000207 |                              4151.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |         1.00 |                |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       389.54 |     15.55 |           5.13 |                  8.11 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 | n/a          |         0 |           1.07 |                  1.08 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       833.44 |      5.60 |           5.36 |                  8.82 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |      1027.15 |      7.48 |           1.61 |                  1.61 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                    0.00 |                     0.00 |                                 20.50 |                                   6.87 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                50827.33 |                100000.00 |                                  1.92 |                                   0.54 |                              0.00 |

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

### Application Metrics

Collecting application metrics for Cassandra is supported and included in the run above, for a single node and for a cluster.
It is activated by `-m -mc -ma`.
A [cassandra_exporter](https://github.com/criteo/cassandra_exporter) sidecar next to each node reads JMX on `127.0.0.1:7199` and exposes the metrics on port 8080.
The request rates need a phase longer than the scrape interval of 30 s; they show 0 for shorter ones.
The metric set `cassandra` in [cluster.config](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s-cluster.config) contains:

| Metric | Title |
|---|---|
| `cassandra_read_rate` | Read Requests [ops/s] |
| `cassandra_write_rate` | Write Requests [ops/s] |
| `cassandra_read_latency_p99` | Read Latency p99, Slowest Node [ms] |
| `cassandra_write_latency_p99` | Write Latency p99, Slowest Node [ms] |
| `cassandra_timeouts` | Read and Write Timeouts [count] |
| `cassandra_unavailables` | Read and Write Unavailables [count] |
| `cassandra_compaction_pending` | Pending Compactions [count] |
| `cassandra_sstables` | Live SSTables of usertable [count] |
| `cassandra_mutation_pending` | Pending Mutations [count] |
| `cassandra_read_pending` | Pending Reads [count] |
| `cassandra_keycache_hit_rate` | Key Cache Hit Rate [0..1] |
| `cassandra_load` | Data on Disk [GiB] |
| `cassandra_commitlog_size` | Commit Log Size [GiB] |

See [Metrics](Example-Metrics.html) for application metrics of all DBMS.


## Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

`-rst` puts the data on a volume, here for a single node.
`-rsr` removes an existing volume at the start, and `-nc 2` repeats the experiment, so the second repetition runs on the data loaded by the first:

```bash
bexhoma ycsb \
  -dbms Cassandra \
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
  -xop 5 \
  -m \
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 16Gi \
  -rr 16Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cassandra_storage.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 738s 
* Code: 1793444325
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 5000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Cassandra'].
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
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* cassandra-1-1-1-1 uses docker image cassandra:5.0.9
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:862510
  * datadisk:1090
  * volume_size:49G
  * volume_used:1.1G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793444325
* cassandra-1-2-1-1 uses docker image cassandra:5.0.9
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861708
  * datadisk:1267
  * volume_size:49G
  * volume_used:1.3G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793444325

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Cassandra-1-2

### Data Parameters of Reused Volumes
* Cassandra-1: DDL values of the volume: num_worker_replicas=1
* Cassandra-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-cassandra-1-1793444325-5dfc894d9d-ckffq: 0
* bexhoma-sut-cassandra-1-1793444325-5f5f866b9c-wr87q: 0

### Workflow

#### Actual

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Cassandra-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Cassandra-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandra-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10608.50 |                11783.00 |            125000.00 |                              1480.00 | 1.00 |              305.52 |
| cassandra-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10235.00 |                12213.00 |            125000.00 |                              1492.00 | 1.00 |              294.77 |
| cassandra-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12345.68 |                10125.00 |            125000.00 |                              1479.00 | 1.00 |              355.56 |
| cassandra-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12051.68 |                10372.00 |            125000.00 |                              1545.00 | 1.00 |              347.09 |
| cassandra-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10068.47 |                12415.00 |            125000.00 |                              1641.00 | 1.00 |              289.97 |
| cassandra-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9788.57 |                12770.00 |            125000.00 |                              1626.00 | 1.00 |              281.91 |
| cassandra-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12989.71 |                 9623.00 |            125000.00 |                              1223.00 | 1.00 |              374.10 |
| cassandra-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11650.67 |                10729.00 |            125000.00 |                              1520.00 | 1.00 |              335.54 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Cassandra-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              281.91 |                        89738.27 |                12770.00 |           1000000.00 |                              1500.75 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1-1-1 | cassandra-1-1-1 | cassandra-1-1-1-1 | Cassandra-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        57827.54 |                86464.00 |            2502102 |                            4911.00 |              2497898 |                              4539.00 |
| cassandra-1-2-1-1-1 | cassandra-1-2-1 | cassandra-1-2-1-1 | Cassandra-1     |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        60016.08 |                83311.00 |            2500420 |                            5291.00 |              2499580 |                              4319.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1 | cassandra-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        57827.54 |                86464.00 |            2502102 |                            4911.00 |              2497898 |                              4539.00 |
| cassandra-1-2-1 | cassandra-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        60016.08 |                83311.00 |            2500420 |                            5291.00 |              2499580 |                              4319.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |         3.00 |                |
| cassandra-1-2-1 | cassandra-1-2-1-1 |                2 |        1 |               1 |         3.00 |                |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       150.57 |      4.35 |           5.10 |                  6.00 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       424.93 |      5.34 |           5.28 |                  6.49 |
| cassandra-1-2-1-1 |       386.67 |      6.53 |           5.06 |                  6.35 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       415.21 |      7.27 |           1.42 |                  1.42 |
| cassandra-1-2-1-1 |       406.20 |      6.10 |           1.40 |                  1.40 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU System Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-2-1-1 (bexhoma-metrics-cassandra-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-2-1-1 (bexhoma-metrics-cassandra-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-2-1-1 (bexhoma-metrics-cassandra-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-2-1-1 (bexhoma-metrics-cassandra-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                    0.87 |                 29730.10 |                                 14.24 |                                   5.72 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                47674.63 |                 47712.70 |                                  1.60 |                                   0.54 |                              0.00 |
| cassandra-1-2-1-1 |                24250.73 |                 24330.93 |                                  1.92 |                                   0.54 |                              0.00 |

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

If you want to deploy Cassandra as a cluster, you can set the number of workers `-nw`.
The nodes start one after the other, loading starts when the last one has joined.
`-rnw` schedules the worker pods on the given nodes, one pod per node:

```bash
bexhoma ycsb \
  -dbms Cassandra \
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
  -xop 5 \
  -m \
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 16Gi \
  -rr 16Gi \
  -rss 50Gi \
  -rnw $BEXHOMA_NODES_WORKER \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cassandra_cluster.log
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_cluster_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra_cluster.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 594s 
* Code: 1793443002
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 5000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Cassandra'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* cassandracluster-1-1-1-1 uses docker image cassandra:5.0.9
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1276698
  * datadisk:1
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-95
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:863054
    * datadisk:379
    * volume_size:1.8T
    * volume_used:843G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:539381
    * datadisk:393
    * volume_size:879G
    * volume_used:527G
    * cpu_list:0-127
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:574988
    * datadisk:417
    * volume_size:1.8T
    * volume_used:562G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793443002
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cassandracluster-1-1793443002-67475b988d-29h5c: 0
* bx-w-cassandracluster-1-1793443002-0: 0
* bx-w-cassandracluster-1-1793443002-1: 0
* bx-w-cassandracluster-1-1793443002-2: 0

### Workflow

#### Actual

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandracluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11091.39 |                11270.00 |            125000.00 |                              1860.00 | 1.00 |              319.43 |
| cassandracluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8674.53 |                14410.00 |            125000.00 |                              1871.00 | 1.00 |              249.83 |
| cassandracluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8953.51 |                13961.00 |            125000.00 |                              1842.00 | 1.00 |              257.86 |
| cassandracluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11137.84 |                11223.00 |            125000.00 |                              1767.00 | 1.00 |              320.77 |
| cassandracluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8829.55 |                14157.00 |            125000.00 |                              2031.00 | 1.00 |              254.29 |
| cassandracluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10641.01 |                11747.00 |            125000.00 |                              1732.00 | 1.00 |              306.46 |
| cassandracluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9246.93 |                13518.00 |            125000.00 |                              1951.00 | 1.00 |              266.31 |
| cassandracluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9083.64 |                13761.00 |            125000.00 |                              2020.00 | 1.00 |              261.61 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CassandraCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              249.83 |                        77658.42 |                14410.00 |           1000000.00 |                              1884.25 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1-1-1 | cassandracluster-1-1-1 | cassandracluster-1-1-1-1 | CassandraCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        63057.27 |                79293.00 |            2499474 |                            3419.00 |              2500526 |                              2993.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1 | cassandracluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        63057.27 |                79293.00 |            2499474 |                            3419.00 |              2500526 |                              2993.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandracluster-1-1-1 | cassandracluster-1-1-1-1 |                1 |        1 |               1 |        11.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       324.24 |      9.15 |          14.78 |                 15.65 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       987.96 |     13.21 |          15.63 |                 16.71 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       375.98 |      7.29 |           1.44 |                  1.45 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                    1.23 |                 20539.60 |                                 51.01 |                                   0.64 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                33858.53 |                 33872.50 |                                  2.30 |                                   0.64 |                              0.00 |

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

`-nwr` sets the replication factor of the keyspace (default 1):

```bash
bexhoma ycsb \
  -dbms Cassandra \
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
  -nwr 3 \
  -xop 5 \
  -m \
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 16Gi \
  -rr 16Gi \
  -rss 50Gi \
  -rnw $BEXHOMA_NODES_WORKER \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cassandra_replica.log
```

Reads and writes use consistency level `ONE`, the default of the YCSB binding: a request is answered by one replica, the others are written in the background.

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_replica_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra_replica.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 609s 
* Code: 1793443655
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 5000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Cassandra'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* cassandracluster-1-1-1-1 uses docker image cassandra:5.0.9
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1276862
  * datadisk:1
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-95
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:863604
    * datadisk:1090
    * volume_size:1.8T
    * volume_used:844G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:540104
    * datadisk:1090
    * volume_size:879G
    * volume_used:528G
    * cpu_list:0-127
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:575663
    * datadisk:1090
    * volume_size:1.8T
    * volume_used:563G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793443655
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cassandracluster-1-1793443655-5b9b775659-n6qk8: 0
* bx-w-cassandracluster-1-1793443655-0: 0
* bx-w-cassandracluster-1-1793443655-1: 0
* bx-w-cassandracluster-1-1793443655-2: 0

### Workflow

#### Actual

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandracluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9312.37 |                13423.00 |            125000.00 |                              1918.00 | 1.00 |              268.20 |
| cassandracluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9477.59 |                13189.00 |            125000.00 |                              1709.00 | 1.00 |              272.95 |
| cassandracluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7450.68 |                16777.00 |            125000.00 |                              2227.00 | 1.00 |              214.58 |
| cassandracluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7408.29 |                16873.00 |            125000.00 |                              2629.00 | 1.00 |              213.36 |
| cassandracluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7839.45 |                15945.00 |            125000.00 |                              2145.00 | 1.00 |              225.78 |
| cassandracluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7436.93 |                16808.00 |            125000.00 |                              2145.00 | 1.00 |              214.18 |
| cassandracluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7755.79 |                16117.00 |            125000.00 |                              1921.00 | 1.00 |              223.37 |
| cassandracluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9536.16 |                13108.00 |            125000.00 |                              2307.00 | 1.00 |              274.64 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CassandraCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              213.36 |                        66217.26 |                16873.00 |           1000000.00 |                              2125.12 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1-1-1 | cassandracluster-1-1-1 | cassandracluster-1-1-1-1 | CassandraCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        62988.95 |                79379.00 |            2500811 |                            4627.00 |              2499189 |                              3575.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1 | cassandracluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        62988.95 |                79379.00 |            2500811 |                            4627.00 |              2499189 |                              3575.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandracluster-1-1-1 | cassandracluster-1-1-1-1 |                1 |        1 |               1 |        12.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       802.20 |     25.46 |          15.24 |                 17.96 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 | n/a          |         0 |           0.63 |                  0.63 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |      1341.37 |     24.67 |          15.88 |                 19.26 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       422.70 |      7.78 |           1.45 |                  1.46 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                    1.00 |                 22250.63 |                                 51.01 |                                   0.92 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                43403.67 |                 43430.17 |                                  5.72 |                                   0.92 |                              0.00 |

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

#### Replication on Persistent Storage

With workers, each node gets a volume of its own:

```bash
bexhoma ycsb \
  -dbms Cassandra \
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
  -nwr 3 \
  -xop 5 \
  -m \
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 16Gi \
  -rr 16Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnw $BEXHOMA_NODES_WORKER \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cassandra_replica_storage.log
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_replica_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra_replica_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1100s 
* Code: 1793446418
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 5000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Cassandra'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* cassandracluster-1-1-1-1 uses docker image cassandra:5.0.9
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1277015
  * datadisk:1
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-95
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:861765
    * datadisk:1090
    * volume_size:49G
    * volume_used:1.1G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:539030
    * datadisk:1090
    * volume_size:49G
    * volume_used:1.1G
    * cpu_list:0-127
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:574576
    * datadisk:1090
    * volume_size:49G
    * volume_used:1.1G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793446418
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cassandracluster-1-2-1-1 uses docker image cassandra:5.0.9
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1277184
  * datadisk:1
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-95
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:861766
    * datadisk:1268
    * volume_size:49G
    * volume_used:1.3G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:539029
    * datadisk:1268
    * volume_size:49G
    * volume_used:1.3G
    * cpu_list:0-127
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:574574
    * datadisk:1268
    * volume_size:49G
    * volume_used:1.3G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793446418
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
    * ddl_num_worker_replicas:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: CassandraCluster-1-2

### Data Parameters of Reused Volumes
* CassandraCluster-1: DDL values of the volume: num_worker_replicas=3
* CassandraCluster-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-cassandracluster-1-1793446418-6c9fd645fc-5rddd: 0
* bx-w-ca-nvme-ycsb-1-0: 0
* bx-w-ca-nvme-ycsb-1-1: 0
* bx-w-ca-nvme-ycsb-1-2: 0
* bexhoma-sut-cassandracluster-1-1793446418-9f9967867-l62dh: 0

### Workflow

#### Actual

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CassandraCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CassandraCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandracluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7925.44 |                15772.00 |            125000.00 |                              2303.00 | 1.00 |              228.25 |
| cassandracluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7987.22 |                15650.00 |            125000.00 |                              1915.00 | 1.00 |              230.03 |
| cassandracluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7706.06 |                16221.00 |            125000.00 |                              2093.00 | 1.00 |              221.93 |
| cassandracluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7682.38 |                16271.00 |            125000.00 |                              2093.00 | 1.00 |              221.25 |
| cassandracluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8234.52 |                15180.00 |            125000.00 |                              2157.00 | 1.00 |              237.15 |
| cassandracluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8476.30 |                14747.00 |            125000.00 |                              2169.00 | 1.00 |              244.12 |
| cassandracluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8629.62 |                14485.00 |            125000.00 |                              2137.00 | 1.00 |              248.53 |
| cassandracluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8469.41 |                14759.00 |            125000.00 |                              2187.00 | 1.00 |              243.92 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CassandraCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              221.25 |                        65110.94 |                16271.00 |           1000000.00 |                              2131.75 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1-1-1 | cassandracluster-1-1-1 | cassandracluster-1-1-1-1 | CassandraCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        63099.44 |                79240.00 |            2500077 |                            3851.00 |              2499923 |                              2727.00 |
| cassandracluster-1-2-1-1-1 | cassandracluster-1-2-1 | cassandracluster-1-2-1-1 | CassandraCluster-1 |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        62576.66 |                79902.00 |            2500333 |                            6647.00 |              2499667 |                              3409.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1 | cassandracluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        63099.44 |                79240.00 |            2500077 |                            3851.00 |              2499923 |                              2727.00 |
| cassandracluster-1-2-1 | cassandracluster-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        62576.66 |                79902.00 |            2500333 |                            6647.00 |              2499667 |                              3409.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandracluster-1-1-1 | cassandracluster-1-1-1-1 |                1 |        1 |               1 |        11.00 |                |
| cassandracluster-1-2-1 | cassandracluster-1-2-1-1 |                2 |        1 |               1 |        11.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       867.70 |     21.36 |          15.13 |                 17.80 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |      1706.30 |     25.51 |          15.92 |                 19.39 |
| cassandracluster-1-2-1-1 |      1854.32 |     27.84 |          15.36 |                 18.34 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       476.69 |      9.33 |           1.42 |                  1.43 |
| cassandracluster-1-2-1-1 |       592.20 |     10.01 |           1.47 |                  1.47 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-2-1-1 (bexhoma-metrics-cassandracluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-2-1-1 (bexhoma-metrics-cassandracluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-2-1-1 (bexhoma-metrics-cassandracluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-2-1-1 (bexhoma-metrics-cassandracluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                    1.00 |                 29777.97 |                                 51.01 |                                   1.11 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                36726.70 |                 36713.17 |                                  4.77 |                                   1.11 |                              0.00 |
| cassandracluster-1-2-1-1 |                45201.10 |                 45422.17 |                                  5.72 |                                   0.77 |                              0.00 |

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

There are two configuration keys, chosen by `-nw` with `-dbms Cassandra`:

- `Cassandra` (`-nw 0`): a single node in the SUT pod.
- `CassandraCluster` (`-nw` > 0): a stateful set of nodes with a headless service.

In `cluster.config` there is a section:

```python
'Cassandra': {
    'abbreviation': 'ca',
    'loadData': 'cqlsh {service_name} 9091 --request-timeout=600 -f {scriptname}',
    'delay_prepare': 10,
    'template': {
        'version': '5.0.9',
        'alias': 'Wide-Column-1',
        'docker_alias': 'WC1',
        'auth': ["cassandra", ""],
    },
    'logfile': '/var/log/cassandra/system.log',
    'datadir': '/var/lib/cassandra',
    'priceperhourdollar': 0.0,
    'monitor': { ... },  # Prometheus discovery of the SUT pod on port 8080 (cassandra_exporter)
},
```

where
* `abbreviation`: short name in the names of volumes and worker pods
* `loadData`: `cqlsh` of the SUT pod; CQL scripts have the suffix `.sql` to run through this command
* `delay_prepare`: the service needs a moment to list a pod that just got ready
* `monitor`: Prometheus discovery of the SUT pod (single node) or the worker pods (cluster), scraping the `cassandra_exporter` on port 8080

There is no JDBC driver: YCSB runs its `cassandra-cql` binding, selected by `BEXHOMA_DBMS_TYPE = "cassandra"`.
The binding uses the DataStax driver 3.0.0, which works with Cassandra 5.
DBMSBenchmarker cannot connect, so only YCSB is offered.

### Deployment

* Single node: [deploymenttemplate-Cassandra.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Cassandra.yml), one SUT pod with Cassandra, a `cassandra_exporter` and a cAdvisor sidecar.
* Cluster (`-nw` > 0): [deploymenttemplate-CassandraCluster.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-CassandraCluster.yml), a stateful set of nodes with a headless service.
  * The first worker is the seed.
  * The nodes start one after the other, as Cassandra refuses to bootstrap them in parallel, and bexhoma starts loading when the last one has joined.
  * The SUT pod is a placeholder that runs `cqlsh` for the scripts.
* The driver connects to every node it discovers on the port of its contact points. So YCSB reaches a cluster through the workers on port 9042 and a single node through the SUT service on port 9091.
* The heap is a quarter of the memory limit of the container, at most 31 GiB, because `cassandra-env.sh` would size it from the RAM of the node. Change it per run with `--set deployment[bexhoma-deployment-cassandra].container[dbms].env.MAX_HEAP_SIZE=8G` (for the cluster workers: `statefulset[bexhoma-worker]`). Do not set `HEAP_NEWSIZE`, which must stay unset with G1.

### Schema and Scripts

The scripts in [experiments/ycsb/Cassandra](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Cassandra) are CQL with the suffix `.sql`, because bexhoma runs only that suffix through `loadData`:

* `initschema-ycsb.sql` creates the keyspace `ycsb` and the table `usertable`.
* `checkschema-ycsb.sql` shows keyspace, table and ring. It counts no rows, since `SELECT count(*)` scans the table and runs into the range timeout of the server.
* `save-snapshot.sh` flushes and waits for the compactions after the load, and logs `nodetool tablestats` with the estimated rows per node.

A loader thread of YCSB ends at its first failed insert, and a busy node answers with a write timeout after 2 s.
So `generator.sh` retries a failed insert for Cassandra up to 10 times, 3 s apart; each retry is a line `Retrying insertion` in the log of the loader.
The test `Loading Phase: all rows inserted` fails for every DBMS when rows are missing.

`-xsbs` has no effect: the binding writes single statements.

DDL parameters (`-xddl`, see [DDL parameters](DBMS.md#ddl-parameters--xddl)):

| Key | Workload | Values | Default | Meaning |
|---|---|---|---|---|
| `num_worker_replicas` | YCSB | integer | `1` | replication_factor of the keyspace ycsb, also set by `-nwr`; reads and writes use consistency level ONE |

### Load Durability

`-xld` has no effect, since a keyspace does not exist yet when the durability scripts run: writes go to the commit log, which is synced every 10 s (`commitlog_sync: periodic`) unless set otherwise.

### Reset Scripts

With `-ar`, [save-snapshot.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/ycsb/Cassandra/save-snapshot.sh) runs after the load and before each benchmarking round, in the SUT pod (single node) or in every worker (cluster):

1. Statistics: n/a (no optimizer statistics)
2. Persist: `nodetool flush`, then waits until no compactions are pending (at most 1800 s)
3. Counters: n/a (the JMX metrics cannot be reset)

All runs on this page use `-ar`, so compactions caused by the load do not run during the benchmark.
See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract.
There is no test run for Cassandra in [Test: Reset Scripts](Test-Reset.md) yet.
