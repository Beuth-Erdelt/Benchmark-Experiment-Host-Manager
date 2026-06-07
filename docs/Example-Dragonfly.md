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
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms Dragonfly \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rr 64Gi -lr 64Gi \
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
      * 10.000.000 operations (i.e., SF=10, `-sfo`)
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
* Duration: 497s 
* Code: 1774190325
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
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Dragonfly-64-8-196608-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:152282
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1774190325

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                        54919.96 |                18773.00 |           1000000.00 |                              1548.25 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        65499.04 |               152674.00 |         5001346.00 |                             534.00 |           4998654.00 |                               513.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       308.22 |      3.92 |           1.68 |                  1.68 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |         0.14 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |      1299.60 |      8.81 |           1.68 |                  1.68 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       485.00 |      4.49 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             2000001.00 |                1.53 |                           9990.22 |                     6.31 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             8673876.00 |                1.53 |                          24921.94 |                     3.94 |                    0.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
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
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Dragonfly \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rr 64Gi -lr 64Gi \
  run &>$LOG_DIR/doc_ycsb_dragonfly_2.log
```

yields something like

doc_ycsb_dragonfly_2.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 432s 
* Code: 1775818177
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
  * Experiment uses bexhoma version 0.9.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Dragonfly-64-8-196608-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:150970
  * datadisk:1
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081965441024
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:5.15.0-1099-nvidia
    * node:cl-worker27
    * disk:1316851
    * datadisk:1
    * cpu_list:0-255
  * worker 1
    * RAM:540591206400
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-107-generic
    * node:cl-worker24
    * disk:150006
    * datadisk:1
    * cpu_list:0-95
  * worker 2
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:1166493
    * datadisk:1
    * cpu_list:0-223
  * eval_parameters
    * code:1775818177
    * BEXHOMA_WORKERS:3

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                        90554.34 |                11468.00 |           1000000.00 |                              1271.38 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        64242.58 |               155660.00 |         4999513.00 |                             423.00 |           5000487.00 |                               411.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component worker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |        21.55 |      0.50 |           0.59 |                  0.59 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       586.50 |      4.50 |           1.64 |                  1.64 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       541.39 |      4.98 |           0.29 |                  0.29 |

### Application Metrics

#### Loading phase: component worker

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             1813887.00 |                1.25 |                           6826.00 |                     4.14 |                    0.00 |

#### Execution phase: component worker

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             8877746.00 |                1.52 |                          31142.68 |                     3.11 |                    0.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

## Replication

We can set the number of replicas with the parameter `-nwr`.
However, only the basic master-copy replication is implemented in bexhoma.
Whenever `-nwr` is greater than 0, it is set to the number of workers minus 1.

```bash
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 2 \
  --workload a \
  -dbms Dragonfly \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_ycsb_dragonfly_3.log
```

yields something like

doc_ycsb_dragonfly_3.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 398s 
* Code: 1775817214
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
  * Experiment uses bexhoma version 0.9.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Dragonfly-64-8-196608-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:150969
  * datadisk:1
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081965441024
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:5.15.0-1099-nvidia
    * node:cl-worker27
    * disk:1317019
    * datadisk:1
    * cpu_list:0-255
  * worker 1
    * RAM:540591206400
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-107-generic
    * node:cl-worker24
    * disk:149843
    * datadisk:1
    * cpu_list:0-95
  * worker 2
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:1166438
    * datadisk:1
    * cpu_list:0-223
  * eval_parameters
    * code:1775817214
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                        75876.77 |                14270.00 |           1000000.00 |                              1504.25 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        65504.61 |               152661.00 |         4997409.00 |                             311.00 |           5002591.00 |                               299.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component worker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |        34.36 |      0.73 |           2.43 |                  2.43 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |         0.15 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       777.11 |      5.45 |           4.92 |                  4.92 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       452.00 |      4.48 |           0.12 |                  0.13 |

### Application Metrics

#### Loading phase: component worker

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             2000000.00 |                4.59 |                          25843.62 |                     4.34 |                    0.00 |

#### Execution phase: component worker

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             8386902.00 |                4.60 |                          62087.48 |                     3.25 |                 2019.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms Dragonfly \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rst shared -rss 50Gi -rsr \
  -rr 64Gi -lr 64Gi \
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

```

### Dragonfly as a Cluster

Similarly we can make a Dragonfly cluster to store the database in persistent storage.
Here, we remove existing storage via `-rsr` to start with a clean copy.

```bash
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Dragonfly \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rst shared -rss 50Gi -rsr \
  -rr 64Gi -lr 64Gi \
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
