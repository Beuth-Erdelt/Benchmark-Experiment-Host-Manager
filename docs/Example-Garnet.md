# Example: Benchmark Garnet

This example shows how to benchmark Garnet with YCSB, as a single host and as a cluster managed by bexhoma.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

[Garnet](https://microsoft.github.io/garnet/) is a key-value cache store from Microsoft Research that speaks the Redis protocol (RESP). It is licensed under the MIT license (which has no restriction on publishing benchmark results).
This page uses the image `ghcr.io/microsoft/garnet:2.2.5`.
Bexhoma runs it as a single host (one SUT pod) or as a cluster (`-nw`, with optional replicas `-nwr`), where every shard and every replica is a worker pod of a stateful set.
In a cluster, bexhoma still deploys a main pod as a single point of contact and to annotate the status of experiments.
YCSB uses its Redis binding, so only the commands used by that binding must be supported by Garnet.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. [Garnet](https://microsoft.github.io/garnet/)
1. [YCSB Repository](https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload)
1. [Benchmarking cloud serving systems with YCSB](https://dl.acm.org/doi/10.1145/1807128.1807152)
1. [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
1. [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](https://doi.org/10.1007/978-3-031-68031-1_9)
1. Test script of this page: [test-docs-garnet.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-garnet.sh), [test-docs-garnet.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-garnet.ps1)


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
  -dbms Garnet \
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
  run &>$LOG_DIR/docs_ycsb_garnet.log
```

This
* starts a clean instance of Garnet (`-dbms`)
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
| Garnet-64-8-196608 | (1. Running) | ycsb       | (7 Running)(1 Pending) |
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
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_garnet_summary.md" target="_blank" rel="noopener">docs_ycsb_garnet.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 166s 
* Code: 1793706282
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
  * Experiment is limited to DBMS ['Garnet'].
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
* garnet-1-1-1-1 uses docker image ghcr.io/microsoft/garnet:2.2.5
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:794668
  * datadisk:1527
  * volume_size:1.8T
  * volume_used:777G
  * cpu_list:0-223
  * args:['--port', '6379', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793706282

### Init Scripts Not in Folder
* Garnet-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-garnet-1-1793706282-78f47cb7bf-kmt2r: 0

### Workflow

#### Actual

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| garnet-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18347.28 |                 6813.00 |            125000.00 |                              1437.00 | 1.00 |              528.40 |
| garnet-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18014.12 |                 6939.00 |            125000.00 |                              1335.00 | 1.00 |              518.81 |
| garnet-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18280.20 |                 6838.00 |            125000.00 |                              1383.00 | 1.00 |              526.47 |
| garnet-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18695.78 |                 6686.00 |            125000.00 |                              1437.00 | 1.00 |              538.44 |
| garnet-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18469.27 |                 6768.00 |            125000.00 |                              1406.00 | 1.00 |              531.91 |
| garnet-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        19337.87 |                 6464.00 |            125000.00 |                              1347.00 | 1.00 |              556.93 |
| garnet-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18540.49 |                 6742.00 |            125000.00 |                              1373.00 | 1.00 |              533.97 |
| garnet-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18845.17 |                 6633.00 |            125000.00 |                              1444.00 | 1.00 |              542.74 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Garnet-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              518.81 |                       148530.18 |                 6939.00 |           1000000.00 |                              1395.25 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1-1-1 | garnet-1-1-1 | garnet-1-1-1-1 | Garnet-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64804.61 |                15431.00 |             499134 |                            1549.00 |               500866 |                               490.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1 | garnet-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64804.61 |                15431.00 |             499134 |                            1549.00 |               500866 |                               490.00 |

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

Garnet has no Prometheus exporter in bexhoma, so only the cAdvisor metrics of the containers are available; there are no application metrics.
All metrics in monitoring are summed across all matching components.
For a Garnet cluster, this means that used memory, CPU time, etc. are summed across all worker pods.

```bash
bexhoma ycsb \
  -dbms Garnet \
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
  run &>$LOG_DIR/docs_ycsb_garnet_monitoring.log
```

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_garnet_monitoring_summary.md" target="_blank" rel="noopener">docs_ycsb_garnet_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 327s 
* Code: 1793705786
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
  * Experiment is limited to DBMS ['Garnet'].
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
* garnet-1-1-1-1 uses docker image ghcr.io/microsoft/garnet:2.2.5
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:807179
  * datadisk:4323
  * volume_size:1.8T
  * volume_used:789G
  * cpu_list:0-223
  * args:['--port', '6379', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793705786

### Init Scripts Not in Folder
* Garnet-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-garnet-1-1793705786-866446d75f-cdhqw: 0

### Workflow

#### Actual

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| garnet-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16605.41 |                22583.00 |            375000.00 |                               883.00 | 3.00 |              478.24 |
| garnet-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17168.76 |                21842.00 |            375000.00 |                               905.00 | 3.00 |              494.46 |
| garnet-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16505.28 |                22720.00 |            375000.00 |                               927.00 | 3.00 |              475.35 |
| garnet-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16761.27 |                22373.00 |            375000.00 |                               948.00 | 3.00 |              482.72 |
| garnet-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16762.77 |                22371.00 |            375000.00 |                               844.00 | 3.00 |              482.77 |
| garnet-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17401.39 |                21550.00 |            375000.00 |                               891.00 | 3.00 |              501.16 |
| garnet-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16239.39 |                23092.00 |            375000.00 |                               954.00 | 3.00 |              467.69 |
| garnet-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17293.06 |                21685.00 |            375000.00 |                               911.00 | 3.00 |              498.04 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Garnet-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 3.00 |              467.69 |                       134737.34 |                23092.00 |           3000000.00 |                               907.88 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1-1-1 | garnet-1-1-1 | garnet-1-1-1-1 | Garnet-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65463.88 |               152756.00 |            5000582 |                             521.00 |              4999418 |                               488.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1 | garnet-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65463.88 |               152756.00 |            5000582 |                             521.00 |              4999418 |                               488.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       481.17 |     16.56 |           8.59 |                  8.59 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 | n/a          |         0 |           0.52 |                  0.53 |

### Benchmarking phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       351.79 |      2.68 |           8.67 |                  8.67 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       616.14 |      5.86 |           1.03 |                  1.03 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loading.log, expected: series exists only while non-zero)

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


## Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

Garnet is started with a checkpoint directory and an append-only file on the volume (see [Deployment](#deployment)), so a reused persistent volume keeps its data.

Example:
```bash
bexhoma ycsb \
  -dbms Garnet \
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
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_garnet_storage.log
```

`bexhoma status` shows one volume of type `shared`.
Every single-host Garnet experiment running YCSB of SF=1 will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of Garnet mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_garnet_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_garnet_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 631s 
* Code: 1793531683
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
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Garnet'].
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
* garnet-1-1-1-1 uses docker image ghcr.io/microsoft/garnet:2.2.5
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:675148
  * datadisk:1527
  * volume_size:49G
  * volume_used:1.5G
  * cpu_list:0-223
  * args:['--port', '6379', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793531683
* garnet-1-2-1-1 uses docker image ghcr.io/microsoft/garnet:2.2.5
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:673792
  * datadisk:2513
  * volume_size:49G
  * volume_used:2.5G
  * cpu_list:0-223
  * args:['--port', '6379', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793531683

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Garnet-1-2

### Data Parameters of Reused Volumes
* Garnet-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Garnet-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-garnet-1-1793531683-5f49d776b5-qm97d: 0
* bexhoma-sut-garnet-1-1793531683-649bd899dd-fw6rj: 0

### Workflow

#### Actual

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Garnet-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Garnet-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| garnet-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15846.86 |                 7888.00 |            125000.00 |                              1382.00 | 1.00 |              456.39 |
| garnet-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17499.65 |                 7143.00 |            125000.00 |                              1369.00 | 1.00 |              503.99 |
| garnet-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15447.36 |                 8092.00 |            125000.00 |                              1390.00 | 1.00 |              444.88 |
| garnet-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        15118.53 |                 8268.00 |            125000.00 |                              1381.00 | 1.00 |              435.41 |
| garnet-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17667.84 |                 7075.00 |            125000.00 |                              1502.00 | 1.00 |              508.83 |
| garnet-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16960.65 |                 7370.00 |            125000.00 |                              1325.00 | 1.00 |              488.47 |
| garnet-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18184.46 |                 6874.00 |            125000.00 |                              1363.00 | 1.00 |              523.71 |
| garnet-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        16598.06 |                 7531.00 |            125000.00 |                              1426.00 | 1.00 |              478.02 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Garnet-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              435.41 |                       133323.41 |                 8268.00 |           1000000.00 |                              1392.25 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1-1-1 | garnet-1-1-1 | garnet-1-1-1-1 | Garnet-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65472.02 |               152737.00 |            5000715 |                             535.00 |              4999285 |                               440.00 |
| garnet-1-2-1-1-1 | garnet-1-2-1 | garnet-1-2-1-1 | Garnet-1        |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65491.32 |               152692.00 |            4998870 |                             418.00 |              5001130 |                               401.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1 | garnet-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65472.02 |               152737.00 |            5000715 |                             535.00 |              4999285 |                               440.00 |
| garnet-1-2-1 | garnet-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        65491.32 |               152692.00 |            4998870 |                             418.00 |              5001130 |                               401.00 |

#### Reset

| phase        | job            |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-------------|:---------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| garnet-1-1-1 | garnet-1-1-1-1 |                1 |        1 |               1 |         4.00 |                |
| garnet-1-2-1 | garnet-1-2-1-1 |                2 |        1 |               1 |         6.00 |                |

### Monitoring

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       707.94 |      4.84 |           1.03 |                  1.03 |
| garnet-1-2-1-1 |       725.93 |      5.05 |           1.03 |                  1.04 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-2-1-1 (bexhoma-metrics-garnet-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-2-1-1 (bexhoma-metrics-garnet-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
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

If you want to deploy Garnet as a cluster, you can set the number of workers `-nw`.
Each worker is a shard of the database.

```bash
bexhoma ycsb \
  -dbms Garnet \
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
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_garnet_cluster.log
```

A Garnet node that is not part of a cluster yet reports `cluster_state:ok` (with no slots assigned), so the init job of the template waits for `cluster_slots_assigned:16384` instead.

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_garnet_cluster_summary.md" target="_blank" rel="noopener">docs_ycsb_garnet_cluster.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 314s 
* Code: 1793814239
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
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Garnet'].
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
* garnet-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:850498
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:605538
    * datadisk:895
    * volume_size:1.8T
    * volume_used:592G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814239.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:609553
    * datadisk:1019
    * volume_size:879G
    * volume_used:596G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814239.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:247701
    * datadisk:894
    * volume_size:439G
    * volume_used:242G
    * cpu_list:0-255
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814239.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793814239
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Garnet-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-garnet-1-1793814239-75c689754c-c2nc7: 0
* bx-w-garnet-1-1793814239-0: 0
* bx-w-garnet-1-1793814239-1: 0
* bx-w-garnet-1-1793814239-2: 0

### Workflow

#### Actual

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| garnet-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12034.27 |                10387.00 |            125000.00 |                              2093.00 | 1.00 |              346.59 |
| garnet-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11803.59 |                10590.00 |            125000.00 |                              1983.00 | 1.00 |              339.94 |
| garnet-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12007.68 |                10410.00 |            125000.00 |                              2007.00 | 1.00 |              345.82 |
| garnet-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11868.59 |                10532.00 |            125000.00 |                              2109.00 | 1.00 |              341.82 |
| garnet-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11901.36 |                10503.00 |            125000.00 |                              2125.00 | 1.00 |              342.76 |
| garnet-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12557.77 |                 9954.00 |            125000.00 |                              1974.00 | 1.00 |              361.66 |
| garnet-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12090.14 |                10339.00 |            125000.00 |                              2015.00 | 1.00 |              348.20 |
| garnet-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11313.24 |                11049.00 |            125000.00 |                              2099.00 | 1.00 |              325.82 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Garnet-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              325.82 |                        95576.65 |                11049.00 |           1000000.00 |                              2050.62 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1-1-1 | garnet-1-1-1 | garnet-1-1-1-1 | Garnet-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        62476.96 |               160059.00 |            5000391 |                             798.00 |              4999609 |                               796.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1 | garnet-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        62476.96 |               160059.00 |            5000391 |                             798.00 |              4999609 |                               796.00 |

#### Reset

| phase        | job            |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-------------|:---------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| garnet-1-1-1 | garnet-1-1-1-1 |                1 |        1 |               1 |         5.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       304.83 |      9.09 |           3.88 |                  3.88 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |      1046.83 |      7.47 |           4.06 |                  4.06 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       681.88 |      5.22 |           1.49 |                  1.49 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

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
* TEST skipped: Monitoring metrics missing (phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Reset scripts ran without errors
```

</details>

### Cluster on Persistent Storage

A Garnet cluster can store the database in persistent storage, too.
Here, we remove existing storage via `-rsr` to start with a clean copy, and run two rounds (`-nc 2`): the second one restarts the cluster on the volumes of the first.
With `-ar`, a snapshot is saved in every worker before each benchmarking round.

```bash
bexhoma ycsb \
  -dbms Garnet \
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
  -tr \
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_garnet_cluster_storage.log
```

The first volume is attached to the (dummy) coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes, one per worker) are attached to the worker pods and store the actual data.

Garnet keeps the configuration of the cluster, that is the nodes and their slots, with the data.
The workers therefore announce the DNS name of their pod (`--cluster-preferred-endpoint-type hostname`), not its IP.
After a restart the pods have new IPs, but the names in the recovered configuration still resolve, so the cluster is complete again and the clients find all nodes.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_garnet_cluster_storage_summary.md" target="_blank" rel="noopener">docs_ycsb_garnet_cluster_storage.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 744s 
* Code: 1793813426
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
  * Experiment is limited to DBMS ['Garnet'].
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
* garnet-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:903953
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:604784
    * datadisk:1402
    * volume_size:49G
    * volume_used:1.4G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:607495
    * datadisk:1774
    * volume_size:49G
    * volume_used:1.8G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:244977
    * datadisk:1404
    * volume_size:49G
    * volume_used:1.4G
    * cpu_list:0-255
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793813426
    * BEXHOMA_WORKERS:3
* garnet-1-2-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:903957
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:604783
    * datadisk:1681
    * volume_size:49G
    * volume_used:1.7G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:607497
    * datadisk:2067
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:253305
    * datadisk:1690
    * volume_size:49G
    * volume_used:1.7G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793813426
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Garnet-1-2

### Data Parameters of Reused Volumes
* Garnet-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Garnet-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-garnet-1-1793813426-78956b9f65-xqbx6: 0
* bx-w-garnet-nvme-ycsb-3-0: 0
* bx-w-garnet-nvme-ycsb-3-1: 0
* bx-w-garnet-nvme-ycsb-3-2: 0
* bexhoma-sut-garnet-1-1793813426-665c6c7f4d-2jb7f: 0

### Workflow

#### Actual

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Garnet-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Garnet-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| garnet-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13379.48 |                28028.00 |            375000.00 |                              1447.00 | 3.00 |              385.33 |
| garnet-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13386.64 |                28013.00 |            375000.00 |                              1425.00 | 3.00 |              385.54 |
| garnet-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13038.49 |                28761.00 |            375000.00 |                              1453.00 | 3.00 |              375.51 |
| garnet-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13337.60 |                28116.00 |            375000.00 |                              1431.00 | 3.00 |              384.12 |
| garnet-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        14131.21 |                26537.00 |            375000.00 |                              1459.00 | 3.00 |              406.98 |
| garnet-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13473.22 |                27833.00 |            375000.00 |                              1447.00 | 3.00 |              388.03 |
| garnet-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13750.37 |                27272.00 |            375000.00 |                              1447.00 | 3.00 |              396.01 |
| garnet-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13606.18 |                27561.00 |            375000.00 |                              1466.00 | 3.00 |              391.86 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Garnet-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 3.00 |              375.51 |                       108103.19 |                28761.00 |           3000000.00 |                              1446.88 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1-1-1 | garnet-1-1-1 | garnet-1-1-1-1 | Garnet-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        62398.21 |               160261.00 |            4998231 |                             857.00 |              5001769 |                               854.00 |
| garnet-1-2-1-1-1 | garnet-1-2-1 | garnet-1-2-1-1 | Garnet-1        |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        61294.42 |               163147.00 |            5000499 |                             253.00 |              4999501 |                               247.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1 | garnet-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        62398.21 |               160261.00 |            4998231 |                             857.00 |              5001769 |                               854.00 |
| garnet-1-2-1 | garnet-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        61294.42 |               163147.00 |            5000499 |                             253.00 |              4999501 |                               247.00 |

#### Reset

| phase        | job            |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-------------|:---------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| garnet-1-1-1 | garnet-1-1-1-1 |                1 |        1 |               1 |         8.00 |                |
| garnet-1-2-1 | garnet-1-2-1-1 |                2 |        1 |               1 |         8.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       815.72 |     22.38 |           9.49 |                  9.49 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 | n/a          |         0 |           1.04 |                  1.04 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |      1079.19 |      7.85 |           9.70 |                  9.70 |
| garnet-1-2-1-1 |      1040.95 |      8.34 |           8.04 |                  8.05 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       766.39 |      5.25 |           1.49 |                  1.50 |
| garnet-1-2-1-1 |       736.43 |      4.93 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-2-1-1 (bexhoma-metrics-garnet-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-2-1-1 (bexhoma-metrics-garnet-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-2-1-1 (bexhoma-metrics-garnet-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-2-1-1 (bexhoma-metrics-garnet-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

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

The second round finds the data of the first and runs with the same throughput.


### Replication

We can set the number of replicas with the parameter `-nwr`.
Garnet requires a worker per replicated shard, so `-nw 3` and `-nwr 1` create 6 worker pods, 3 for sharding and another 3 for the (single) replicas.
The cluster is created with `valkey-cli --cluster create --cluster-replicas`, the replicas replicate their primary with `CLUSTER REPLICATE` and need the append-only file, which the template enables.

```bash
bexhoma ycsb \
  -dbms Garnet \
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
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_garnet_replica.log
```

#### Example Result

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_garnet_replica_summary.md" target="_blank" rel="noopener">docs_ycsb_garnet_replica.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 431s 
* Code: 1793814254
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
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Garnet'].
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
* garnet-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:850500
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:605854
    * datadisk:895
    * volume_size:1.8T
    * volume_used:592G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:609635
    * datadisk:1019
    * volume_size:879G
    * volume_used:596G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:515784
    * datadisk:894
    * volume_size:1.8T
    * volume_used:504G
    * cpu_list:0-255
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 3
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:252570
    * datadisk:894
    * volume_size:550G
    * volume_used:247G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 4
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:147241
    * datadisk:895
    * volume_size:219G
    * volume_used:144G
    * cpu_list:0-95
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 5
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:247817
    * datadisk:1019
    * volume_size:439G
    * volume_used:243G
    * cpu_list:0-255
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * resources_total: 24.25 CPU, 384.5 GiB RAM requested in 7 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 6 x, 24.0 CPU, 384.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793814254
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Garnet-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-garnet-1-1793814254-68dd5889b7-b8nnr: 0
* bx-w-garnet-1-1793814254-0: 0
* bx-w-garnet-1-1793814254-1: 0
* bx-w-garnet-1-1793814254-2: 0
* bx-w-garnet-1-1793814254-3: 0
* bx-w-garnet-1-1793814254-4: 0
* bx-w-garnet-1-1793814254-5: 0

### Workflow

#### Actual

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| garnet-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13020.83 |                 9600.00 |            125000.00 |                              2049.00 | 1.00 |              375.00 |
| garnet-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13354.70 |                 9360.00 |            125000.00 |                              1931.00 | 1.00 |              384.62 |
| garnet-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13337.60 |                 9372.00 |            125000.00 |                              2209.00 | 1.00 |              384.12 |
| garnet-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13228.91 |                 9449.00 |            125000.00 |                              2167.00 | 1.00 |              380.99 |
| garnet-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12960.08 |                 9645.00 |            125000.00 |                              2055.00 | 1.00 |              373.25 |
| garnet-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13313.45 |                 9389.00 |            125000.00 |                              2051.00 | 1.00 |              383.43 |
| garnet-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13302.12 |                 9397.00 |            125000.00 |                              2049.00 | 1.00 |              383.10 |
| garnet-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13094.49 |                 9546.00 |            125000.00 |                              2101.00 | 1.00 |              377.12 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Garnet-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              373.25 |                       105612.19 |                 9645.00 |           1000000.00 |                              2076.50 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1-1-1 | garnet-1-1-1 | garnet-1-1-1-1 | Garnet-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        49735.65 |               201063.00 |            4997532 |                             292.00 |              5002468 |                               281.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1 | garnet-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        49735.65 |               201063.00 |            4997532 |                             292.00 |              5002468 |                               281.00 |

#### Reset

| phase        | job            |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-------------|:---------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| garnet-1-1-1 | garnet-1-1-1-1 |                1 |        1 |               1 |         6.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       297.38 |      8.58 |           6.40 |                  6.40 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |      1142.18 |      8.46 |           8.35 |                  9.49 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       749.72 |      4.90 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

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
* TEST skipped: Monitoring metrics missing (phase shorter than scrape interval; series exists only while non-zero)
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

In `cluster.config` there is a section:

```python
'Garnet': {
    # no DDL scripts and no CLI in the image: loadData is only a placeholder
    'loadData': 'redis-cli --host bexhoma-service.{namespace}.svc.cluster.local < {scriptname}',
    'delay_prepare': 0,
    'attachWorker': '',
    'template': {
        'version': 'xxx',
        'alias': 'Key-Value-4',
        'docker_alias': 'KV4',
        'auth': ["root", ""],
    },
    'logfile': '/var/log/garnet/garnet.log',
    'datadir': '/data',
    'priceperhourdollar': 0.0,
},
```

There is no `JDBC` section, as Garnet has no JDBC driver, and no `monitor` section, as there is no exporter.

### Deployment

* Single host: [deploymenttemplate-Garnet.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Garnet.yml), one SUT pod.
* Cluster (`-nw` > 0): [deploymenttemplate-GarnetCluster.yml](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-GarnetCluster.yml), a stateful set of `-nw` * (1 + `-nwr`) worker pods with Garnet started with `--cluster`; an init job creates the cluster with `valkey-cli --cluster create`. Redis's cluster flags (`--cluster-enabled` etc.) are unknown to Garnet, so the Redis cluster template cannot be reused by swapping the image.
* Garnet is started with `--checkpointdir /data/checkpoints --aof --aof-commit-freq 1000 --recover` and as root (the volume is owned by root), so data on a persistent volume survives a restart and a repetition that reuses the volume finds its data.
* In a cluster, Garnet is started with `--cluster-preferred-endpoint-type hostname --cluster-announce-hostname <pod>.<service>.<namespace>.svc.cluster.local`: the recovered cluster configuration names the pods by DNS name, not by IP, so a cluster that restarts on its volumes finds its nodes at their new IPs. With the default (IP), the recovered configuration pointed to IPs of pods that no longer existed and the clients failed with `NoRouteToHostException`. The placeholder `{statefulset}` in the arguments of a stateful set is replaced by the name of its headless service.
* The image contains no command line client, so an init container copies `valkey-cli` (also as `redis-cli`) from the Valkey image into the pod; it serves the `SAVE` of the `preStop` hook and of the reset script.
* YCSB talks to Garnet with the Redis binding (`BEXHOMA_DBMS_TYPE=redis`, for a cluster `redis-cluster`).
* There is no `redis_exporter` sidecar, so only cAdvisor metrics are collected.

### Schema and Scripts

Garnet has no schema; YCSB writes the keys directly via the Redis wire protocol.
The experiment folder [experiments/ycsb/Garnet](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Garnet) contains only the reset script.

### Load Durability

`-xld` has no effect on Garnet: there are no durability scripts for it.
The append-only file is committed every 1000 ms (`--aof-commit-freq 1000`).

### Reset Scripts

With `-ar`, [save-snapshot.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/ycsb/Garnet/save-snapshot.sh) runs before each benchmarking round, in the SUT pod (single host) or in every worker (cluster):

1. Statistics: n/a (no optimizer statistics)
2. Persist: `SAVE` writes a checkpoint
3. Counters: n/a (Garnet does not support `CONFIG RESETSTAT`)

A replica can be busy with a checkpoint when the reset script runs `SAVE`, so `save-snapshot.sh` retries while Garnet answers that a checkpoint is already in progress.
The runs on persistent storage, the cluster and the replication on this page use `-ar`.
See [Reset scripts](DBMS.md#reset-scripts--ar) for the reset contract.
There is no test run for Garnet in [Test: Reset Scripts](Test-Reset.md) yet.
