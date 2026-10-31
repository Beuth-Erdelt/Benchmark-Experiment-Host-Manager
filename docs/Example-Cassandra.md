# Example: Benchmark Cassandra

This differs from the default behaviour of bexhoma, since we benchmark **a distributed NoSQL DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Apache Cassandra is a wide-column store [1].
There is a single-host and a cluster version.
In the cluster version, there are several pods deployed for the nodes using a stateful set.
Cassandra has no coordinator node, every node answers clients.
Bexhoma still deploys a main pod as a single point of contact, to run `cqlsh` for the scripts and to annotate the status of experiments.
Bexhoma also deploys a service for clients and a headless service for communication between the nodes.
See [dummy manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Cassandra.yml) for a single-host version that is suitable for bexhoma and see [dummy manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-CassandraCluster.yml) for a multi-host version that is suitable for bexhoma.

This can be managed by bexhoma.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Apache Cassandra: https://cassandra.apache.org/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9


## Perform YCSB Benchmark - Ingestion of Data Included

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
  -xop 5 \
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
  run &>$LOG_DIR/docs_ycsb_cassandra_1.log
```

This
* starts a clean instance of Cassandra (`-dbms`)
  * data directory inside a Docker container
* creates the keyspace `ycsb` and the table `usertable`
* starts 8 loader pods (`-nlp`)
  * threads = 64/8 (`-nlt`)
  * target throughput is 12 * 16384 (`-xnlf`, `-xtb`)
  * generates YCSB data = 1.000.000 rows (i.e., SF=1, `-sf`)
  * imports it into the DBMS
* flushes the data and waits for the compactions, after loading and before each benchmarking round (`-ar`)
* runs 1 stream of YCSB queries
  * 5.000.000 operations (`-xop`)
  * workload A = 50% read / 50% write (`-xwl`)
  * target throughput is 4 * 16384 (`-xnbf`, `-xtb`)
  * threads = 128 (`-nbt`)
* tests if results match workflow (`-tr`)
* monitors (`-m`) all components (`-mc`) and Cassandra itself (`-ma`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexhoma status`

```bash
+--------------+--------------+--------------+------------+--------------+-------------------+-----------------------------------+
| 1793442538   | sut          |   loaded [s] | use case   | monitoring   | benchmarker       | phase                             |
+==============+==============+==============+============+==============+===================+===================================+
| Cassandra-1  | (1. Running) |           24 | ycsb       | (Running)    | 1x (1. Succeeded) | Benchmarking (run 1/1, round 1/1) |
+--------------+--------------+--------------+------------+--------------+-------------------+-----------------------------------+
```

The code `1793442538` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1793442538` (removes everything that is related to experiment `1793442538`).

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_1_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra_1.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 411s 
* Code: 1793442538
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
  * disk:863845
  * datadisk:1090
  * volume_size:1.8T
  * volume_used:844G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793442538

### SUT Container Restarts
* bexhoma-sut-cassandra-1-1793442538-6c7df97768-74kfc: 0

### Workflow

#### Actual

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandra-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10351.11 |                12076.00 |            125000.00 |                              1394.00 | 1.00 |              298.11 |
| cassandra-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10393.28 |                12027.00 |            125000.00 |                              1531.00 | 1.00 |              299.33 |
| cassandra-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10505.08 |                11899.00 |            125000.00 |                              1609.00 | 1.00 |              302.55 |
| cassandra-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10460.25 |                11950.00 |            125000.00 |                              1715.00 | 1.00 |              301.26 |
| cassandra-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12547.68 |                 9962.00 |            125000.00 |                              1559.00 | 1.00 |              361.37 |
| cassandra-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12946.66 |                 9655.00 |            125000.00 |                              1483.00 | 1.00 |              372.86 |
| cassandra-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12468.83 |                10025.00 |            125000.00 |                              1273.00 | 1.00 |              359.10 |
| cassandra-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10487.46 |                11919.00 |            125000.00 |                              1585.00 | 1.00 |              302.04 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Cassandra-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              298.11 |                        90160.35 |                12076.00 |           1000000.00 |                              1518.62 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1-1-1 | cassandra-1-1-1 | cassandra-1-1-1-1 | Cassandra-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        56945.01 |                87804.00 |            2498411 |                            5363.00 |              2501589 |                              4939.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1 | cassandra-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        56945.01 |                87804.00 |            2498411 |                            5363.00 |              2501589 |                              4939.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |         3.00 |                |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       157.76 |      4.35 |           5.16 |                  6.05 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       374.31 |      5.56 |           5.42 |                  6.58 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       431.16 |      7.16 |           1.41 |                  1.42 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                    0.93 |                 20779.83 |                                 17.08 |                                   5.72 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                51001.10 |                 51135.43 |                                  1.33 |                                   0.45 |                              0.00 |

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

To see the summary again you can simply call `bexhoma summary -e 1793442538` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888


## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).
`-ma` adds the metrics of Cassandra, read by a [cassandra_exporter](https://github.com/criteo/cassandra_exporter) sidecar next to each node.

All metrics in monitoring are summed across all matching components.
In the following examples, this means that used memory, CPU time, etc. are summed across all 3 nodes of the Cassandra cluster.
The request rates need a phase longer than the scrape interval of 30 s.


## Distributed DBMS

If you want to deploy Cassandra as a cluster, you can adjust the number of workers `-nw` when calling the script.
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
  run &>$LOG_DIR/docs_ycsb_cassandra_2.log
```

yields something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_2_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra_2.log</a></summary>

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


## Replication

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
  run &>$LOG_DIR/docs_ycsb_cassandra_3.log
```

yields something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_3_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra_3.log</a></summary>

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

Reads and writes use consistency level `ONE`, the default of the YCSB binding: a request is answered by one replica, the others are written in the background.


## Persistent Storage

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
  run &>$LOG_DIR/docs_ycsb_cassandra_4.log
```

yields something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_4_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra_4.log</a></summary>

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


## Persistent Storage of a Cluster

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
  run &>$LOG_DIR/docs_ycsb_cassandra_5.log
```

yields something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_cassandra_5_summary.md" target="_blank" rel="noopener">docs_ycsb_cassandra_5.log</a></summary>

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

See [Cassandra](DBMS.md#cassandra) for the configuration, the scripts and what has no effect (`-xld`, `-xsbs`).
