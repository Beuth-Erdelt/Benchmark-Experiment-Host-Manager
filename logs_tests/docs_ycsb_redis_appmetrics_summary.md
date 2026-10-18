## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 585s 
* Code: 1792346117
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
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Redis'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:854802
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:143873
    * datadisk:717
    * cpu_list:0-95
  * worker 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:151397
    * datadisk:803
    * cpu_list:0-127
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:617872
    * datadisk:721
    * cpu_list:0-127
  * worker 3
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:878208
    * datadisk:714
    * cpu_list:0-255
  * worker 4
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:870689
    * datadisk:714
    * cpu_list:0-255
  * worker 5
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:854803
    * datadisk:806
    * cpu_list:0-223
  * resources_total: 24.25 CPU, 96.5 GiB RAM requested in 7 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 6 x, 24.0 CPU, 96.0 GiB RAM
  * eval_parameters
    * code:1792346117
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-redis-1-1792346117-958975b77-gh27h: 0
* bx-w-redis-ycsb-1-0: 0
* bx-w-redis-ycsb-1-1: 0
* bx-w-redis-ycsb-1-2: 0
* bx-w-redis-ycsb-1-3: 0
* bx-w-redis-ycsb-1-4: 0
* bx-w-redis-ycsb-1-5: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3859.93 |                32384.00 |            125000.00 |                              4683.00 | 1.00 |              111.17 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3840.36 |                32549.00 |            125000.00 |                              4675.00 | 1.00 |              110.60 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3973.05 |                31462.00 |            125000.00 |                              4687.00 | 1.00 |              114.42 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3861.60 |                32370.00 |            125000.00 |                              4683.00 | 1.00 |              111.21 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3841.31 |                32541.00 |            125000.00 |                              4683.00 | 1.00 |              110.63 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3896.75 |                32078.00 |            125000.00 |                              4699.00 | 1.00 |              112.23 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3858.98 |                32392.00 |            125000.00 |                              4703.00 | 1.00 |              111.14 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         3882.71 |                32194.00 |            125000.00 |                              4683.00 | 1.00 |              111.82 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              110.60 |                        31014.69 |                32549.00 |           1000000.00 |                              4687.00 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 | Redis-1         |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        60853.53 |               164329.00 |            4999181 |                            1623.00 |              5000819 |                              1615.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        60853.53 |               164329.00 |            4999181 |                            1623.00 |              5000819 |                              1615.00 |

### Monitoring

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       158.90 |      2.83 |           3.07 |                  3.07 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |        59.52 |      0.00 |           0.30 |                  0.31 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       420.73 |      3.42 |           3.27 |                  3.28 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |       593.24 |      3.94 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS          |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [GiB] |   Redis Master Link Status |   Redis Operations Rate, Busiest Instance [ops/s] |
|:--------------|----------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------------------------------:|
| redis-1-1-1-1 |                  6.00 |                      201.00 |                      2.90 |                       3.00 |                                           5913.96 |

#### Benchmarking phase: component worker

| DBMS          |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [GiB] |   Redis Master Link Status |   Redis Operations Rate, Busiest Instance [ops/s] |
|:--------------|----------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------------------------------:|
| redis-1-1-1-1 |                  6.00 |                      403.00 |                      2.91 |                       3.00 |                                          12275.30 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
