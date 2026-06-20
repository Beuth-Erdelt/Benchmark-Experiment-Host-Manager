# Example: Benchmark Dragonfly

This differs from the default behaviour of bexhoma, since we benchmark **a distributed NoSQL DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Dragonfly is a Key / Value store and a drop-in replacement for Redis [1].
There is a single-host and a cluster version.
In the cluster version, there are several pods deployed for the worker nodes using a stateful set.
Dragonfly cluster does not require a coordinator.
Bexhoma still deploys a main pod (called master) as a substitute for a single point of contact and to annotate status of experiments.
Bexhoma also deploys a service for communication external to Dragonfly (from within the cluster) and a headless service for communication between the pods of the Dragonfly cluster.
See [dummy manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Dragonfly.yml) for a single-host version that is suitable for bexhoma and see [dummy manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-DragonflyCluster.yml) for a multi-host version that is suitable for bexhoma.

This can be managed by bexhoma.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Dragonfly: https://www.dragonflydb.io/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9


## Perform YCSB Benchmark - Ingestion of Data Included

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1

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
  -xop 10 \
  -m \
  -ma \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_dragonfly_1.log
```

This
* loops over `n` in [8] and `t` in [12]
  * starts a clean instance of Dragonfly (`-dbms`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=1, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [4]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 10.000.000 operations (i.e., SF=10, `-xop`)
      * workload A = 50% read / 50% write (`--workload`)
      * target throughput is `s` * 16384
      * threads = 64/`m` (`-nbt`)
    * with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* monitors (`-m`) all components (`-mc`), including application metrics ( `-ma`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

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
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1774020403` (removes everything that is related to experiment `1774020403`).

## Evaluate Results

At the end of a benchmark you will see a summary like

doc_ycsb_dragonfly_1.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 425s 
* Code: 1781947318
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
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Dragonfly-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:217100
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781947318

### Workflow

#### Actual

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| Dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10544.07 |                11855.00 |            125000.00 |                              1765.00 | 1.00 |              303.67 |
| Dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9939.57 |                12576.00 |            125000.00 |                              2012.00 | 1.00 |              286.26 |
| Dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10401.07 |                12018.00 |            125000.00 |                              1935.00 | 1.00 |              299.55 |
| Dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10303.33 |                12132.00 |            125000.00 |                              2059.00 | 1.00 |              296.74 |
| Dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9921.42 |                12599.00 |            125000.00 |                              1833.00 | 1.00 |              285.74 |
| Dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10830.01 |                11542.00 |            125000.00 |                              1730.00 | 1.00 |              311.90 |
| Dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9906.48 |                12618.00 |            125000.00 |                              1841.00 | 1.00 |              285.31 |
| Dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10382.92 |                12039.00 |            125000.00 |                              1948.00 | 1.00 |              299.03 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              285.31 |                        82228.88 |                12618.00 |           1000000.00 |                              1890.38 |

### Execution

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1-1-1-1 | Dragonfly-1-1-1 | Dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65502.04 |               152667.00 |            5001040 |                            1877.00 |              4998960 |                              1831.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1-1 | Dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65502.04 |               152667.00 |            5001040 |                            1877.00 |              4998960 |                              1831.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |       269.94 |      8.13 |           1.69 |                  1.69 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |      1799.35 |     15.46 |           1.76 |                  1.76 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |       751.53 |      5.15 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-1-1-1-1 |             2000000.00 |                1.54 |                           9930.00 |                     6.27 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-1-1-1-1 |             8584639.00 |                1.54 |                          30387.49 |                     3.20 |                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

To see the summary again you can simply call `bexperiments summary -e 1742224433` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexperiments jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888




## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components.
In the following example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the Dragonfly cluster.


## Distributed DBMS

If you want to deploy Dragonfly as a cluster, you can adjust the number of workers `-nw` when calling the script:
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
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_dragonfly_2.log
```

yields something like

doc_ycsb_dragonfly_2.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 452s 
* Code: 1781947773
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
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
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
  * disk:214909
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1077381271552
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1416152
    * cpu_list:0-255
  * worker 1
    * RAM:1081649803264
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:306119
    * cpu_list:0-55
  * worker 2
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1324157
    * cpu_list:0-223
  * eval_parameters
    * code:1781947773
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| DragonflyCluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10766.58 |                11610.00 |            125000.00 |                              2157.00 | 1.00 |              310.08 |
| DragonflyCluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10590.53 |                11803.00 |            125000.00 |                              2125.00 | 1.00 |              305.01 |
| DragonflyCluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10456.75 |                11954.00 |            125000.00 |                              2012.00 | 1.00 |              301.15 |
| DragonflyCluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10423.62 |                11992.00 |            125000.00 |                              2003.00 | 1.00 |              300.20 |
| DragonflyCluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10512.15 |                11891.00 |            125000.00 |                              1957.00 | 1.00 |              302.75 |
| DragonflyCluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10764.73 |                11612.00 |            125000.00 |                              2177.00 | 1.00 |              310.02 |
| DragonflyCluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10437.54 |                11976.00 |            125000.00 |                              1996.00 | 1.00 |              300.60 |
| DragonflyCluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10617.51 |                11773.00 |            125000.00 |                              1859.00 | 1.00 |              305.78 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              300.20 |                        84569.41 |                11992.00 |           1000000.00 |                              2035.75 |

### Execution

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1-1-1 | DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64511.13 |               155012.00 |            4998880 |                             938.00 |              5001120 |                               918.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64511.13 |               155012.00 |            4998880 |                             938.00 |              5001120 |                               918.00 |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       134.19 |      3.58 |           1.64 |                  1.67 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |        40.34 |      0.00 |           0.12 |                  0.12 |

### Execution phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       716.04 |      4.96 |           1.65 |                  1.68 |

### Execution phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       739.68 |      5.22 |           0.29 |                  0.29 |

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             2001602.00 |                1.52 |                          10638.18 |                     6.26 |                    0.00 |

#### Execution phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             9273089.00 |                1.52 |                          32105.73 |                     3.21 |                    0.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

## Replication

We can set the number of replicas with the parameter `-nwr`.
However, only the basic master-copy replication is implemented in bexhoma.
Whenever `-nwr` is greater than 0, it is set to the number of workers minus 1.

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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_dragonfly_3.log
```

yields something like

doc_ycsb_dragonfly_3.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 514s 
* Code: 1781948251
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
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
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
  * disk:214955
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1324192
    * cpu_list:0-223
  * worker 1
    * RAM:1077381271552
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1416155
    * cpu_list:0-255
  * worker 2
    * RAM:1081649803264
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:306119
    * cpu_list:0-55
  * eval_parameters
    * code:1781948251
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| DragonflyCluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11772.46 |                10618.00 |            125000.00 |                              1697.00 | 1.00 |              339.05 |
| DragonflyCluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11232.93 |                11128.00 |            125000.00 |                              1663.00 | 1.00 |              323.51 |
| DragonflyCluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11478.42 |                10890.00 |            125000.00 |                              1829.00 | 1.00 |              330.58 |
| DragonflyCluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11001.58 |                11362.00 |            125000.00 |                              1766.00 | 1.00 |              316.85 |
| DragonflyCluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11528.17 |                10843.00 |            125000.00 |                              1706.00 | 1.00 |              332.01 |
| DragonflyCluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11250.11 |                11111.00 |            125000.00 |                              1733.00 | 1.00 |              324.00 |
| DragonflyCluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11191.69 |                11169.00 |            125000.00 |                              1804.00 | 1.00 |              322.32 |
| DragonflyCluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11415.53 |                10950.00 |            125000.00 |                              1816.00 | 1.00 |              328.77 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              316.85 |                        90870.90 |                11362.00 |           1000000.00 |                              1751.75 |

### Execution

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1-1-1 | DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65500.75 |               152670.00 |            5002198 |                            1793.00 |              4997802 |                              1733.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65500.75 |               152670.00 |            5002198 |                            1793.00 |              4997802 |                              1733.00 |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       127.52 |      2.98 |           4.96 |                  4.96 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |         0.18 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       499.20 |      3.96 |           4.95 |                  4.95 |

### Execution phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       601.76 |      5.09 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             2000021.00 |                4.60 |                          28240.73 |                     4.83 |                 1962.00 |

#### Execution phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             8133644.00 |                4.60 |                          59952.60 |                     3.37 |                 2056.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

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
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst shared \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_dragonfly_4.log
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

The result looks something like

doc_ycsb_dragonfly_4.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 813s 
* Code: 1781948791
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
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 50Gi. Persistent storage is removed at experiment start.
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
  * disk:214909
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781948791
* Dragonfly-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214909
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781948791

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
| Dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10702.97 |                11679.00 |            125000.00 |                              1654.00 | 1.00 |              308.25 |
| Dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10108.36 |                12366.00 |            125000.00 |                              1837.00 | 1.00 |              291.12 |
| Dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10558.32 |                11839.00 |            125000.00 |                              1597.00 | 1.00 |              304.08 |
| Dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10126.38 |                12344.00 |            125000.00 |                              1855.00 | 1.00 |              291.64 |
| Dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10102.64 |                12373.00 |            125000.00 |                              1662.00 | 1.00 |              290.96 |
| Dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10700.22 |                11682.00 |            125000.00 |                              1653.00 | 1.00 |              308.17 |
| Dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10198.25 |                12257.00 |            125000.00 |                              1668.00 | 1.00 |              293.71 |
| Dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9934.04 |                12583.00 |            125000.00 |                              1753.00 | 1.00 |              286.10 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              286.10 |                        82431.19 |                12583.00 |           1000000.00 |                              1709.88 |

### Execution

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1-1-1-1 | Dragonfly-1-1-1 | Dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65500.75 |               152670.00 |            4998399 |                            2027.00 |              5001601 |                              2000.00 |
| Dragonfly-1-2-1-1-1 | Dragonfly-1-2-1 | Dragonfly-1-2-1-1 | Dragonfly-1     |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65499.04 |               152674.00 |            4998165 |                            1782.00 |              5001835 |                              1741.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1-1 | Dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65500.75 |               152670.00 |            4998399 |                            2027.00 |              5001601 |                              2000.00 |
| Dragonfly-1-2-1 | Dragonfly-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        65499.04 |               152674.00 |            4998165 |                            1782.00 |              5001835 |                              1741.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |       329.37 |      5.57 |           1.80 |                  1.80 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |        15.93 |      0.00 |           0.09 |                  0.10 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |      1783.13 |     15.33 |           1.76 |                  1.76 |
| Dragonfly-1-2-1-1 |      2265.23 |     19.92 |           1.83 |                  2.90 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-1-1-1-1 |       772.65 |      6.66 |           0.13 |                  0.13 |
| Dragonfly-1-2-1-1 |       620.37 |     10.30 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-1-1-1-1 |             2000001.00 |                1.54 |                           9958.44 |                     6.29 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-1-1-1-1 |             8480569.00 |                1.54 |                          30323.95 |                     3.22 |                    0.00 |
| Dragonfly-1-2-1-1 |             9393762.00 |                1.63 |                          18395.62 |                     1.86 |                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

### Dragonfly as a Cluster

Similarly we can make a Dragonfly cluster to store the database in persistent storage.
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
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst shared \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_dragonfly_5.log
```

We copied the following behaviour from Redis:
Redis expects fully qualified domain name (FQDN) for each pod.
At the same time, the length of hostnames is limited.
Therefore bexhoma will shorten the name of the pods and pvcs in this case.
The first volume is attached to the (dummy) coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.


```bash
+--------------------------------------------+---------------------+--------------+--------------+-------------------+---------------------+----------------------+-----------+----------+--------+--------+
| Volumes                                    | configuration       | experiment   | loaded [s]   |   timeLoading [s] | dbms                | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
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

The result looks something like

doc_ycsb_dragonfly_5.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 976s 
* Code: 1781949630
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
  * Experiment uses bexhoma version 0.9.16.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 50Gi. Persistent storage is removed at experiment start.
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
  * disk:214909
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
    * disk:1344408
    * cpu_list:0-223
  * worker 1
    * RAM:1077381271552
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1416354
    * cpu_list:0-255
  * worker 2
    * RAM:1081649803264
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:306121
    * cpu_list:0-55
  * eval_parameters
    * code:1781949630
    * BEXHOMA_WORKERS:3
* DragonflyCluster-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214909
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1077381271552
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1416324
    * cpu_list:0-255
  * worker 1
    * RAM:1081649803264
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:306122
    * cpu_list:0-55
  * worker 2
    * RAM:2164173246464
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1325025
    * cpu_list:0-223
  * eval_parameters
    * code:1781949630
    * BEXHOMA_WORKERS:3

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
| DragonflyCluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8567.51 |                14590.00 |            125000.00 |                              3641.00 | 1.00 |              246.74 |
| DragonflyCluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8138.02 |                15360.00 |            125000.00 |                              3619.00 | 1.00 |              234.38 |
| DragonflyCluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7978.55 |                15667.00 |            125000.00 |                              3643.00 | 1.00 |              229.78 |
| DragonflyCluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8039.62 |                15548.00 |            125000.00 |                              3969.00 | 1.00 |              231.54 |
| DragonflyCluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8938.79 |                13984.00 |            125000.00 |                              3293.00 | 1.00 |              257.44 |
| DragonflyCluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8536.50 |                14643.00 |            125000.00 |                              3753.00 | 1.00 |              245.85 |
| DragonflyCluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8782.41 |                14233.00 |            125000.00 |                              3747.00 | 1.00 |              252.93 |
| DragonflyCluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8407.88 |                14867.00 |            125000.00 |                              3991.00 | 1.00 |              242.15 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              229.78 |                        67389.29 |                15667.00 |           1000000.00 |                              3707.00 |

### Execution

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1-1-1 | DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64652.94 |               154672.00 |            4996223 |                            1054.00 |              5003777 |                              1023.00 |
| DragonflyCluster-1-2-1-1-1 | DragonflyCluster-1-2-1 | DragonflyCluster-1-2-1-1 | DragonflyCluster-1 |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64602.82 |               154792.00 |            5001172 |                            2549.00 |              4998828 |                              2513.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1-1 | DragonflyCluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64652.94 |               154672.00 |            4996223 |                            1054.00 |              5003777 |                              1023.00 |
| DragonflyCluster-1-2-1 | DragonflyCluster-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        64602.82 |               154792.00 |            5001172 |                            2549.00 |              4998828 |                              2513.00 |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       140.77 |      4.14 |           1.63 |                  1.63 |

### Loading phase: component loader

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |        15.19 |      0.00 |           0.12 |                  0.12 |

### Execution phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       682.13 |      4.90 |           1.64 |                  1.64 |
| DragonflyCluster-1-2-1-1 |       796.22 |      5.27 |           1.78 |                  2.85 |

### Execution phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| DragonflyCluster-1-1-1-1 |       694.90 |      5.57 |           0.29 |                  0.29 |
| DragonflyCluster-1-2-1-1 |       682.41 |      7.07 |           0.29 |                  0.29 |

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             2001604.00 |                1.52 |                          10984.24 |                     6.17 |                    0.00 |

#### Execution phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:-------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| DragonflyCluster-1-1-1-1 |             9166322.00 |                1.52 |                          27099.77 |                     3.43 |                    0.00 |
| DragonflyCluster-1-2-1-1 |             8597893.00 |                1.62 |                          31789.52 |                     3.21 |                    0.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```



## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
        'Dragonfly': {
            'loadData': 'redis-cli < {scriptname}',
            #'loadData': 'redis-cli --host bexhoma-service.{namespace}.svc.cluster.local < {scriptname}',
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
            'monitor': {
                'sut': {
                    'metrics': 'dragonfly',
                    'discovery': True,
                    'headless': True,
                    'discovery_config': """
  - job_name: 'dragonfly-pods'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_interval}
    metrics_path: /metrics
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ["{namespace}"]
    relabel_configs:
      # Only select pods by labels
      - source_labels: [__meta_kubernetes_pod_label_app,
                        __meta_kubernetes_pod_label_component,
                        __meta_kubernetes_pod_label_dbms]
        regex: bexhoma;sut;Dragonfly
        action: keep
      # Map pod IP -> address:port
      - source_labels: [__meta_kubernetes_pod_ip]
        target_label: __address__
        replacement: '$1:6379'
        action: replace
      # Optional: rename instance label to pod name
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: instance
      # Optional: drop pods that are not running
      - source_labels: [__meta_kubernetes_pod_phase]
        regex: Running
        action: keep"""
                },
            },
        },
```

Notice how this does not have a JDBC section (as Dragonfly does not support this).

This section is for a single host deployment.
For a cluster there is another section:
```python
        'DragonflyCluster': {
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
            'monitor': {
                'worker': {
                    'metrics': 'dragonfly',
                    'discovery': True,
                    'headless': True,
                    'discovery_config': """
  - job_name: 'dragonfly-pods'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_interval}
    metrics_path: /metrics
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ["{namespace}"]
    relabel_configs:
      # Only select pods by labels
      - source_labels: [__meta_kubernetes_pod_label_app,
                        __meta_kubernetes_pod_label_component,
                        __meta_kubernetes_pod_label_dbms]
        regex: bexhoma;worker;DragonflyCluster
        action: keep
      # Map pod IP -> address:port
      - source_labels: [__meta_kubernetes_pod_ip]
        target_label: __address__
        replacement: '$1:6379'
        action: replace
      # Optional: rename instance label to pod name
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: instance
      # Optional: drop pods that are not running
      - source_labels: [__meta_kubernetes_pod_phase]
        regex: Running
        action: keep"""
                },
            },
        },
```

Both sections contain a reference to (the same) dict of application metrics, that can be collected if activated.
As of bexhoma v0.9.4, this is (see demo configuration):
```python
'dragonfly': {
    'metrics': {
        'dragonfly_reply_total': {
            # Gesamtzahl aller an Clients gesendeten Antworten (Replies)
            'type': 'application',
            'active': True,
            'metric': 'counter',
            'query': 'sum(dragonfly_reply_total)',
            'title': 'Replies Sent [count]'
        },
        'dragonfly_memory_used_bytes': {
            # Aktuell genutzter Arbeitsspeicher des Servers
            'type': 'application',
            'active': True,
            'metric': 'gauge',
            'query': 'sum(dragonfly_memory_used_bytes)/1024/1024/1024',
            'title': 'Memory Usage [Gi]'
        },
        'dragonfly_commands_processed_total': {
            # Gesamtzahl aller verarbeiteten Kommandos (Request Load)
            'type': 'application',
            'active': True,
            'metric': 'counter',
            'query': 'sum(rate(dragonfly_commands_processed_total[5m]))',
            'title': 'Processed Commands [per second]'
        },
        'dragonfly_net_input_bytes_total': {
            # Eingehende Netzwerkdaten von Clients
            'type': 'application',
            'active': True,
            'metric': 'counter',
            'query': 'sum(rate(dragonfly_net_input_bytes_total[5m]))/1024/1024',
            'title': 'Network Input [MB/sec]'
        },
        'dragonfly_connected_replica_lag_records': {
            # Rückstand eines Replicas in Datensätzen
            'type': 'application',
            'active': True,
            'metric': 'gauge',
            'query': 'sum(dragonfly_connected_replica_lag_records)',
            'title': 'Replica Lag [records]'
        },
        'dragonfly_moved_errors_total': {
            # Anzahl der Slot-Migrationsfehler im Cluster
            'type': 'application',
            'active': True,
            'metric': 'counter',
            'query': 'sum(dragonfly_moved_errors_total)',
            'title': 'Cluster Slot Moved Errors [count]'
        },
        'dragonfly_replication_streaming_bytes': {
            # Speicherverbrauch für laufende Streaming-Replikation
            'type': 'application',
            'active': True,
            'metric': 'gauge',
            'query': 'sum(dragonfly_replication_streaming_bytes)/1024/1024/1024',
            'title': 'Replication Streaming Memory [Gi]'
        },
        'dragonfly_replication_full_sync_bytes': {
            # Speicherverbrauch während voller Synchronisation (Full Sync)
            'type': 'application',
            'active': True,
            'metric': 'gauge',
            'query': 'sum(dragonfly_replication_full_sync_bytes)/1024/1024/1024',
            'title': 'Full Sync Replication Memory [Gi]'
        },
        'dragonfly_replication_psync_count': {
            # Anzahl der PSYNC-Replikationsereignisse
            'type': 'application',
            'active': True,
            'metric': 'counter',
            'query': 'sum(dragonfly_replication_psync_count)',
            'title': 'PSync Events [count]'
        },
    }
},
```
