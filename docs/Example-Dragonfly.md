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

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
nohup python ycsb.py -tr \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_dragonfly_1.log &
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
nohup python ycsb.py -ms 1 -tr \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_dragonfly_2.log &
```

yields something like

doc_ycsb_dragonfly_2.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 483s 
* Code: 1774190846
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
  * disk:150092
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:563532
    * cpu_list:0-223
  * worker 1
    * RAM:540590817280
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-90-generic
    * node:cl-worker23
    * disk:1243559
    * cpu_list:0-95
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-90-generic
    * node:cl-worker37
    * disk:471258
    * cpu_list:0-127
  * eval_parameters
    * code:1774190846
    * BEXHOMA_WORKERS:3

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                        87951.16 |                11775.00 |           1000000.00 |                              1297.25 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        64158.09 |               155865.00 |         5002355.00 |                             432.00 |           4997645.00 |                               419.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component worker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |        66.00 |      0.91 |           0.85 |                  0.85 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       453.56 |      3.90 |           1.64 |                  1.64 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       659.18 |      4.97 |           0.29 |                  0.29 |

### Application Metrics

#### Loading phase: component worker

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             2001600.00 |                1.52 |                           8800.16 |                     5.52 |                    0.00 |

#### Execution phase: component worker

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             9250041.00 |                1.52 |                          31710.06 |                     3.33 |                    0.00 |

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
nohup python ycsb.py -tr \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_dragonfly_3.log &
```

yields something like

doc_ycsb_dragonfly_3.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 422s 
* Code: 1774195450
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
  * disk:150092
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:563544
    * cpu_list:0-223
  * worker 1
    * RAM:540590817280
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-90-generic
    * node:cl-worker23
    * disk:1243561
    * cpu_list:0-95
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-90-generic
    * node:cl-worker37
    * disk:471261
    * cpu_list:0-127
  * eval_parameters
    * code:1774195450
    * BEXHOMA_REPLICAS:2
    * BEXHOMA_WORKERS:3

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                       116343.06 |                 8768.00 |           1000000.00 |                              1255.25 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        65502.04 |               152667.00 |         5001651.00 |                             355.00 |           4998349.00 |                               347.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component worker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       126.30 |      2.17 |           4.98 |                  4.98 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       412.26 |      3.42 |           4.99 |                  4.99 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1 |       460.48 |      4.51 |           0.12 |                  0.12 |

### Application Metrics

#### Loading phase: component worker

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             2000019.00 |                4.60 |                          30806.44 |                     5.23 |                 1655.00 |

#### Execution phase: component worker

| DBMS                    |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1 |             8551628.00 |                4.60 |                          63055.22 |                     3.20 |                 1995.00 |

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


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python ycsb.py -tr \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_dragonfly_4.log &
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
* Duration: 896s 
* Code: 1774191794
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
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* Dragonfly-64-8-196608-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:150092
  * volume_size:50G
  * volume_used:2.2G
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1774191794
* Dragonfly-64-8-196608-2-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:150091
  * volume_size:50G
  * volume_used:4.3G
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1774191794

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                        45002.67 |                22352.00 |           1000000.00 |                              1936.12 |

### Execution

| DBMS                      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        65505.47 |               152659.00 |         4999551.00 |                             490.00 |           5000449.00 |                               468.00 |
| Dragonfly-64-8-196608-2-1 |             2.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        65502.47 |               152666.00 |         4997945.00 |                             497.00 |           5002055.00 |                               472.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1], [1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1], [1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |       297.74 |      4.07 |           1.68 |                  1.68 |

### Loading phase: component loader

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |       144.23 |      0.00 |           0.10 |                  0.10 |

### Execution phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |       955.43 |      8.70 |           1.65 |                  1.65 |
| Dragonfly-64-8-196608-2-1 |      1707.05 |      8.78 |           1.73 |                  3.02 |

### Execution phase: component benchmarker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |       554.91 |      4.60 |           0.13 |                  0.13 |
| Dragonfly-64-8-196608-2-1 |       619.47 |      4.45 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS                      |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:--------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1-1 |             2000001.00 |                1.53 |                          11970.32 |                     7.56 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS                      |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:--------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1-1 |             8360667.00 |                1.53 |                          23497.69 |                     3.48 |                    0.00 |
| Dragonfly-64-8-196608-2-1 |             8447210.00 |                1.63 |                          32522.16 |                     3.28 |                    0.00 |

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

### Dragonfly as a Cluster

Similarly we can make a Dragonfly cluster to store the database in persistent storage.
Here, we remove existing storage via `-rsr` to start with a clean copy.

```bash
nohup python ycsb.py -tr \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_dragonfly_5.log &
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
* Duration: 868s 
* Code: 1774192715
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
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* Dragonfly-64-8-196608-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:150092
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:563541
    * volume_size:50G
    * cpu_list:0-223
  * worker 1
    * RAM:540590817280
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-90-generic
    * node:cl-worker23
    * disk:1243560
    * volume_size:50G
    * cpu_list:0-95
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-90-generic
    * node:cl-worker37
    * disk:471259
    * volume_size:50G
    * cpu_list:0-127
  * eval_parameters
    * code:1774192715
    * BEXHOMA_WORKERS:3
* Dragonfly-64-8-196608-2-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:150092
  * cpu_list:0-63
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:563542
    * volume_size:50G
    * volume_used:352M
    * cpu_list:0-223
  * worker 1
    * RAM:540590817280
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-90-generic
    * node:cl-worker23
    * disk:1243560
    * volume_size:50G
    * volume_used:384M
    * cpu_list:0-95
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-90-generic
    * node:cl-worker37
    * disk:471260
    * volume_size:50G
    * volume_used:352M
    * cpu_list:0-127
  * eval_parameters
    * code:1774192715
    * BEXHOMA_WORKERS:3

### Loading

| DBMS                  |   experiment_run |   threads |    target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|----------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 |                        83108.24 |                13163.00 |           1000000.00 |                              2405.62 |

### Execution

| DBMS                      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-64-8-196608-1-1 |             1.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        64096.81 |               156014.00 |         4999363.00 |                             422.00 |           5000637.00 |                               410.00 |
| Dragonfly-64-8-196608-2-1 |             2.00 |    128.00 | 65536.00 |        1.00 |         0.00 |                        64196.80 |               155771.00 |         5000062.00 |                             426.00 |           4999938.00 |                               415.00 |

### Workflow

#### Actual

* DBMS Dragonfly-64-8-196608 - Pods [[1], [1]]

#### Planned

* DBMS Dragonfly-64-8-196608 - Pods [[1], [1]]

### Monitoring

### Loading phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |        57.91 |      0.96 |           0.82 |                  0.82 |

### Loading phase: component loader

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |       439.87 |      3.89 |           1.64 |                  1.64 |
| Dragonfly-64-8-196608-2-1 |       610.72 |      3.86 |           1.75 |                  2.81 |

### Execution phase: component benchmarker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| Dragonfly-64-8-196608-1-1 |       682.46 |      5.03 |           0.29 |                  0.29 |
| Dragonfly-64-8-196608-2-1 |       682.46 |      4.97 |           0.29 |                  0.29 |

### Application Metrics

#### Loading phase: component worker

| DBMS                      |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:--------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1-1 |             2001628.00 |                1.52 |                          11595.35 |                     7.01 |                    0.00 |

#### Execution phase: component worker

| DBMS                      |   Replies Sent [count] |   Memory Usage [Gi] |   Processed Commands [per second] |   Network Input [MB/sec] |   Replica Lag [records] |
|:--------------------------|-----------------------:|--------------------:|----------------------------------:|-------------------------:|------------------------:|
| Dragonfly-64-8-196608-1-1 |             8971540.00 |                1.52 |                          31530.00 |                     3.11 |                    0.00 |
| Dragonfly-64-8-196608-2-1 |             8969297.00 |                1.62 |                          32309.98 |                     3.26 |                    0.00 |

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



## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'Dragonfly': {
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
},
```

Notice how this does not have a JDBC section (as Dragonfly does not support this).



