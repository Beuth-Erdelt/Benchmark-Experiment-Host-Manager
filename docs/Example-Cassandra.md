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
* Duration: 297s 
* Code: 1794817263
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
  * Experiment uses bexhoma version 0.11.18.
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
  * disk:1056542
  * datadisk:1090
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794817263

### Ingestion
* Cassandra-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cassandra-1-1794817263-858bcd889b-bvwj5: 0

### Workflow

#### Actual

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandra-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10470.77 |                11938.00 |            125000.00 |                              1635.00 | 1.00 |              301.56 |
| cassandra-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10650.08 |                11737.00 |            125000.00 |                              1598.00 | 1.00 |              306.72 |
| cassandra-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10544.07 |                11855.00 |            125000.00 |                              1713.00 | 1.00 |              303.67 |
| cassandra-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10118.18 |                12354.00 |            125000.00 |                              1869.00 | 1.00 |              291.40 |
| cassandra-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10210.75 |                12242.00 |            125000.00 |                              1677.00 | 1.00 |              294.07 |
| cassandra-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10298.24 |                12138.00 |            125000.00 |                              1626.00 | 1.00 |              296.59 |
| cassandra-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10560.11 |                11837.00 |            125000.00 |                              1545.00 | 1.00 |              304.13 |
| cassandra-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        11428.05 |                10938.00 |            125000.00 |                              1484.00 | 1.00 |              329.13 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Cassandra-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              291.40 |                        84280.25 |                12354.00 |           1000000.00 |                              1643.38 |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1-1-1 | cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        52416.40 |                19078.00 |             499969 |                            4847.00 |               500031 |                              4195.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1 | cassandra-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        52416.40 |                19078.00 |             499969 |                            4847.00 |               500031 |                              4195.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |         2.00 |                |

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

[Monitoring](Monitoring.md) can be activated for DBMS only (`-m`) or for all components (`-mc`).
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
* Duration: 452s 
* Code: 1794817575
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
  * Experiment uses bexhoma version 0.11.18.
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
  * disk:1057047
  * datadisk:3239
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794817575

### Ingestion
* Cassandra-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cassandra-1-1794817575-746cfddd86-xwtfg: 0

### Workflow

#### Actual

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandra-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        13227.98 |                28349.00 |            375000.00 |                              1396.00 | 3.00 |              380.97 |
| cassandra-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        11696.45 |                32061.00 |            375000.00 |                              1397.00 | 3.00 |              336.86 |
| cassandra-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        11270.74 |                33272.00 |            375000.00 |                              1451.00 | 3.00 |              324.60 |
| cassandra-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        11296.54 |                33196.00 |            375000.00 |                              1531.00 | 3.00 |              325.34 |
| cassandra-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        13782.71 |                27208.00 |            375000.00 |                              1274.00 | 3.00 |              396.94 |
| cassandra-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        13821.32 |                27132.00 |            375000.00 |                              1272.00 | 3.00 |              398.05 |
| cassandra-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        12936.83 |                28987.00 |            375000.00 |                              1376.00 | 3.00 |              372.58 |
| cassandra-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10164.25 |                36894.00 |            375000.00 |                              1619.00 | 3.00 |              292.73 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Cassandra-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 3.00 |              292.73 |                        98196.83 |                36894.00 |           3000000.00 |                              1414.50 |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1-1-1 | cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        61904.56 |               161539.00 |            5001605 |                            4315.00 |              4998395 |                              4093.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1 | cassandra-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        61904.56 |               161539.00 |            5001605 |                            4315.00 |              4998395 |                              4093.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |         3.00 |                |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       399.69 |     13.49 |           5.17 |                  8.25 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       191.32 |      0.00 |           1.02 |                  1.02 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       704.77 |      6.44 |           5.54 |                  8.84 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |      1095.12 |      7.71 |           1.38 |                  1.38 |

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
| cassandra-1-1-1-1 |                    0.87 |                 99391.33 |                                 17.08 |                                   5.72 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                51447.43 |                 51371.87 |                                  1.33 |                                   0.45 |                              0.00 |

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

See [Metrics](Example-Metrics.md) for application metrics of all DBMS.


## Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.md).

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
* Duration: 687s 
* Code: 1794818068
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
  * Experiment uses bexhoma version 0.11.18.
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
  * disk:1085959
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
    * code:1794818068
* cassandra-1-2-1-1 uses docker image cassandra:5.0.9
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1087773
  * datadisk:1268
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
    * code:1794818068

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Cassandra-1-2

### Data Parameters of Reused Volumes
* Cassandra-1: DDL values of the volume: num_worker_replicas=1
* Cassandra-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Ingestion
* Cassandra-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cassandra-1-1794818068-6f994f468b-k644q: 0
* bexhoma-sut-cassandra-1-1794818068-6d99b95d69-qmt8m: 0

### Workflow

#### Actual

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Cassandra-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Cassandra-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandra-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9923.00 |                12597.00 |            125000.00 |                              1905.00 | 1.00 |              285.78 |
| cassandra-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8301.24 |                15058.00 |            125000.00 |                              1867.00 | 1.00 |              239.08 |
| cassandra-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9368.21 |                13343.00 |            125000.00 |                              1808.00 | 1.00 |              269.80 |
| cassandra-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8822.08 |                14169.00 |            125000.00 |                              1994.00 | 1.00 |              254.08 |
| cassandra-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8787.96 |                14224.00 |            125000.00 |                              1933.00 | 1.00 |              253.09 |
| cassandra-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9842.52 |                12700.00 |            125000.00 |                              1793.00 | 1.00 |              283.46 |
| cassandra-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9255.15 |                13506.00 |            125000.00 |                              1792.00 | 1.00 |              266.55 |
| cassandra-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9923.79 |                12596.00 |            125000.00 |                              1917.00 | 1.00 |              285.81 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Cassandra-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              239.08 |                        74223.93 |                15058.00 |           1000000.00 |                              1876.12 |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1-1-1 | cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        55881.53 |                89475.00 |            2500842 |                            4187.00 |              2499158 |                              4023.00 |
| cassandra-1-2-1-1-1 | cassandra-1-2-1 | cassandra-1-2-1-1 |                2 |        1 |               1 |       1 |       128 |    65536 |        0 |                        62985.78 |                79383.00 |            2499106 |                            4187.00 |              2500894 |                              3487.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1 | cassandra-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        55881.53 |                89475.00 |            2500842 |                            4187.00 |              2499158 |                              4023.00 |
| cassandra-1-2-1 | cassandra-1-2-1 |                2 |        1 |               1 |           1 |       128 |    65536 |        0 |                        62985.78 |                79383.00 |            2499106 |                            4187.00 |              2500894 |                              3487.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |         2.00 |                |
| cassandra-1-2-1 | cassandra-1-2-1-1 |                2 |        1 |               1 |         2.00 |                |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       149.46 |      3.53 |           5.09 |                  5.99 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       318.32 |      4.58 |           5.35 |                  6.47 |
| cassandra-1-2-1-1 |       496.69 |      8.87 |           5.09 |                  6.40 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       397.33 |      7.86 |           1.42 |                  1.42 |
| cassandra-1-2-1-1 |       355.45 |      8.17 |           1.44 |                  1.45 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Rx Total [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Tx Total [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
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
| cassandra-1-1-1-1 |                    0.87 |                 25359.90 |                                 14.24 |                                   4.77 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                51479.07 |                 51516.50 |                                  1.60 |                                   0.54 |                              0.00 |
| cassandra-1-2-1-1 |                47024.40 |                 47225.30 |                                 20.50 |                                   0.45 |                              0.00 |

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
* Duration: 535s 
* Code: 1794818794
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
  * Experiment uses bexhoma version 0.11.18.
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
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1388538
  * datadisk:1
  * volume_size:1.8T
  * volume_used:1.4T
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1388538
    * datadisk:381
    * volume_size:1.8T
    * volume_used:1.4T
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:642283
    * datadisk:393
    * volume_size:879G
    * volume_used:628G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1088193
    * datadisk:415
    * volume_size:1.8T
    * volume_used:1.1T
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794818794
    * BEXHOMA_WORKERS:3

### Ingestion
* CassandraCluster-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cassandracluster-1-1794818794-779545f4c-jwbjg: 0
* bx-w-cassandracluster-1-1794818794-0: 0
* bx-w-cassandracluster-1-1794818794-1: 0
* bx-w-cassandracluster-1-1794818794-2: 0

### Workflow

#### Actual

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandracluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9617.60 |                12997.00 |            125000.00 |                              1401.00 | 1.00 |              276.99 |
| cassandracluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10275.38 |                12165.00 |            125000.00 |                              1315.00 | 1.00 |              295.93 |
| cassandracluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9530.34 |                13116.00 |            125000.00 |                              1451.00 | 1.00 |              274.47 |
| cassandracluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        11585.87 |                10789.00 |            125000.00 |                              1280.00 | 1.00 |              333.67 |
| cassandracluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9344.40 |                13377.00 |            125000.00 |                              1562.00 | 1.00 |              269.12 |
| cassandracluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8850.81 |                14123.00 |            125000.00 |                              1524.00 | 1.00 |              254.90 |
| cassandracluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9841.74 |                12701.00 |            125000.00 |                              1405.00 | 1.00 |              283.44 |
| cassandracluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10762.87 |                11614.00 |            125000.00 |                              1333.00 | 1.00 |              309.97 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CassandraCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              254.90 |                        79809.03 |                14123.00 |           1000000.00 |                              1408.88 |

### Benchmarking

#### Per Connection

| connection                 | phase                  | job                      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1-1-1 | cassandracluster-1-1-1 | cassandracluster-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        62985.78 |                79383.00 |            2499686 |                            2791.00 |              2500314 |                              2549.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1 | cassandracluster-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        62985.78 |                79383.00 |            2499686 |                            2791.00 |              2500314 |                              2549.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandracluster-1-1-1 | cassandracluster-1-1-1-1 |                1 |        1 |               1 |         7.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       291.22 |      6.52 |          14.59 |                 15.53 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       687.35 |     10.97 |          15.14 |                 16.22 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       541.02 |      8.79 |           1.46 |                  1.46 |

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
| cassandracluster-1-1-1-1 |                    1.07 |                 22774.37 |                                 42.51 |                                   0.45 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                38318.43 |                 38407.17 |                                  2.30 |                                   0.45 |                              0.00 |

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
* Duration: 503s 
* Code: 1794826264
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
  * Experiment uses bexhoma version 0.11.18.
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
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:909538
  * datadisk:1
  * volume_size:1.8T
  * volume_used:889G
  * cpu_list:0-255
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1390892
    * datadisk:1090
    * volume_size:1.8T
    * volume_used:1.4T
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:647522
    * datadisk:1090
    * volume_size:879G
    * volume_used:633G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1160566
    * datadisk:1090
    * volume_size:1.8T
    * volume_used:1.2T
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794826264
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Ingestion
* CassandraCluster-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cassandracluster-1-1794826264-5c5bc47549-z4zt5: 0
* bx-w-cassandracluster-1-1794826264-0: 0
* bx-w-cassandracluster-1-1794826264-1: 0
* bx-w-cassandracluster-1-1794826264-2: 0

### Workflow

#### Actual

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandracluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7104.69 |                17594.00 |            125000.00 |                              2038.00 | 1.00 |              204.62 |
| cassandracluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8155.54 |                15327.00 |            125000.00 |                              1918.00 | 1.00 |              234.88 |
| cassandracluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8652.91 |                14446.00 |            125000.00 |                              1851.00 | 1.00 |              249.20 |
| cassandracluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7513.37 |                16637.00 |            125000.00 |                              1847.00 | 1.00 |              216.39 |
| cassandracluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6963.79 |                17950.00 |            125000.00 |                              2219.00 | 1.00 |              200.56 |
| cassandracluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7275.48 |                17181.00 |            125000.00 |                              2077.00 | 1.00 |              209.53 |
| cassandracluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9222.37 |                13554.00 |            125000.00 |                              2044.00 | 1.00 |              265.60 |
| cassandracluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         6979.73 |                17909.00 |            125000.00 |                              2415.00 | 1.00 |              201.02 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CassandraCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              200.56 |                        61867.89 |                17950.00 |           1000000.00 |                              2051.12 |

### Benchmarking

#### Per Connection

| connection                 | phase                  | job                      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1-1-1 | cassandracluster-1-1-1 | cassandracluster-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        63011.97 |                79350.00 |            2501093 |                            4187.00 |              2498907 |                              3031.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1 | cassandracluster-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        63011.97 |                79350.00 |            2501093 |                            4187.00 |              2498907 |                              3031.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandracluster-1-1-1 | cassandracluster-1-1-1-1 |                1 |        1 |               1 |         4.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       699.40 |     18.48 |          15.30 |                 18.03 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |      1551.66 |     24.21 |          15.77 |                 19.25 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       504.91 |     10.00 |           1.43 |                  1.44 |

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
| cassandracluster-1-1-1-1 |                    1.20 |                 22228.23 |                                 42.51 |                                   0.64 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                36858.53 |                 37043.30 |                                  3.31 |                                   0.64 |                              0.00 |

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
* Duration: 997s 
* Code: 1794819969
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
  * Experiment uses bexhoma version 0.11.18.
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
  * RAM:1081742753792
  * CPU:AMD EPYC 7502 32-Core Processor
  * Cores:128
  * host:6.8.0-146-generic
  * node:cl-worker29
  * disk:1388189
  * datadisk:1
  * volume_size:1.8T
  * volume_used:1.4T
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1388189
    * datadisk:1090
    * volume_size:49G
    * volume_used:1.1G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:645460
    * datadisk:1090
    * volume_size:49G
    * volume_used:1.1G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1053097
    * datadisk:1090
    * volume_size:49G
    * volume_used:1.1G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794819969
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cassandracluster-1-2-1-1 uses docker image cassandra:5.0.9
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:643024
  * datadisk:1
  * volume_size:879G
  * volume_used:628G
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:643024
    * datadisk:1268
    * volume_size:49G
    * volume_used:1.3G
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1388039
    * datadisk:1268
    * volume_size:49G
    * volume_used:1.3G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1053099
    * datadisk:1268
    * volume_size:49G
    * volume_used:1.3G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794819969
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
    * ddl_num_worker_replicas:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: CassandraCluster-1-2

### Data Parameters of Reused Volumes
* CassandraCluster-1: DDL values of the volume: num_worker_replicas=3
* CassandraCluster-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Ingestion
* CassandraCluster-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cassandracluster-1-1794819969-5989fcff77-nzhlh: 0
* bx-w-ca-nvme-ycsb-1-0: 0
* bx-w-ca-nvme-ycsb-1-1: 0
* bx-w-ca-nvme-ycsb-1-2: 0
* bexhoma-sut-cassandracluster-1-1794819969-6db66c48f-vgtwd: 0

### Workflow

#### Actual

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CassandraCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CassandraCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandracluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7856.69 |                15910.00 |            125000.00 |                              1633.00 | 1.00 |              226.27 |
| cassandracluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7878.48 |                15866.00 |            125000.00 |                              1695.00 | 1.00 |              226.90 |
| cassandracluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10068.47 |                12415.00 |            125000.00 |                              1602.00 | 1.00 |              289.97 |
| cassandracluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8670.32 |                14417.00 |            125000.00 |                              1476.00 | 1.00 |              249.71 |
| cassandracluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7652.75 |                16334.00 |            125000.00 |                              1658.00 | 1.00 |              220.40 |
| cassandracluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         7904.39 |                15814.00 |            125000.00 |                              1711.00 | 1.00 |              227.65 |
| cassandracluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8656.51 |                14440.00 |            125000.00 |                              1643.00 | 1.00 |              249.31 |
| cassandracluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9441.09 |                13240.00 |            125000.00 |                              1630.00 | 1.00 |              271.90 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CassandraCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              220.40 |                        68128.70 |                16334.00 |           1000000.00 |                              1631.00 |

### Benchmarking

#### Per Connection

| connection                 | phase                  | job                      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1-1-1 | cassandracluster-1-1-1 | cassandracluster-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        62965.95 |                79408.00 |            2500247 |                            3225.00 |              2499753 |                              2425.00 |
| cassandracluster-1-2-1-1-1 | cassandracluster-1-2-1 | cassandracluster-1-2-1-1 |                2 |        1 |               1 |       1 |       128 |    65536 |        0 |                        63043.75 |                79310.00 |            2498101 |                            5527.00 |              2501899 |                              2271.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1 | cassandracluster-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        62965.95 |                79408.00 |            2500247 |                            3225.00 |              2499753 |                              2425.00 |
| cassandracluster-1-2-1 | cassandracluster-1-2-1 |                2 |        1 |               1 |           1 |       128 |    65536 |        0 |                        63043.75 |                79310.00 |            2498101 |                            5527.00 |              2501899 |                              2271.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandracluster-1-1-1 | cassandracluster-1-1-1-1 |                1 |        1 |               1 |         7.00 |                |
| cassandracluster-1-2-1 | cassandracluster-1-2-1-1 |                2 |        1 |               1 |         7.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       743.20 |     17.38 |          15.19 |                 17.88 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |      1361.90 |     22.08 |          15.74 |                 19.30 |
| cassandracluster-1-2-1-1 |      1667.53 |     21.49 |          15.54 |                 17.57 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       430.77 |      8.82 |           1.47 |                  1.48 |
| cassandracluster-1-2-1-1 |       400.96 |      7.56 |           1.45 |                  1.46 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
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
| cassandracluster-1-1-1-1 |                    1.17 |                 28877.67 |                                 42.51 |                                   1.92 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                46953.00 |                 47012.07 |                                  2.30 |                                   0.77 |                              0.00 |
| cassandracluster-1-2-1-1 |                25993.90 |                 26011.83 |                                 42.51 |                                   0.54 |                              0.00 |

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
