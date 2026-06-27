## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 529s 
* Code: 1782070506
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
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Redis'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Redis-1-1-1-1 uses docker image redis:7.4.2
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:238737
  * cpu_list:0-127
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1336737
    * cpu_list:0-255
  * worker 1
    * RAM:540590809088
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:208565
    * cpu_list:0-95
  * worker 2
    * RAM:540579295232
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-124-generic
    * node:cl-worker22
    * disk:400278
    * cpu_list:0-127
  * eval_parameters
    * code:1782070506
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| Redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2403.98 |                51997.00 |            125000.00 |                              6767.00 | 1.00 |               69.23 |
| Redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2402.60 |                52027.00 |            125000.00 |                              6751.00 | 1.00 |               69.19 |
| Redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2412.06 |                51823.00 |            125000.00 |                              6751.00 | 1.00 |               69.47 |
| Redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2405.09 |                51973.00 |            125000.00 |                              6791.00 | 1.00 |               69.27 |
| Redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2406.90 |                51934.00 |            125000.00 |                              6779.00 | 1.00 |               69.32 |
| Redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2415.37 |                51752.00 |            125000.00 |                              6719.00 | 1.00 |               69.56 |
| Redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2395.28 |                52186.00 |            125000.00 |                              6815.00 | 1.00 |               68.98 |
| Redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2460.78 |                50797.00 |            125000.00 |                              6767.00 | 1.00 |               70.87 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |               68.98 |                        19302.06 |                52186.00 |           1000000.00 |                              6767.50 |

### Execution

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1-1-1-1 | Redis-1-1-1 | Redis-1-1-1-1 | Redis-1         |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64721.15 |               154509.00 |            4999396 |                            4579.00 |              5000604 |                              4567.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1-1 | Redis-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        64721.15 |               154509.00 |            4999396 |                            4579.00 |              5000604 |                              4567.00 |

### Monitoring

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       126.23 |      1.86 |           1.78 |                  1.78 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       117.46 |      3.89 |           0.12 |                  0.12 |

### Execution phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       439.22 |      3.29 |           1.81 |                  1.81 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       806.89 |      6.35 |           0.29 |                  0.29 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
