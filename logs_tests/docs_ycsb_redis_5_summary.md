## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1303s 
* Code: 1782072633
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
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* Redis-1-1-1-1 uses docker image redis:7.4.2
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:239137
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
    * disk:1336135
    * volume_size:50G
    * volume_used:708M
    * cpu_list:0-255
  * worker 1
    * RAM:540590809088
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:208791
    * volume_size:50G
    * volume_used:788M
    * cpu_list:0-95
  * worker 2
    * RAM:540579295232
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-124-generic
    * node:cl-worker22
    * disk:399604
    * volume_size:50G
    * volume_used:712M
    * cpu_list:0-127
  * eval_parameters
    * code:1782072633
    * BEXHOMA_WORKERS:3
* Redis-1-2-1-1 uses docker image redis:7.4.2
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222641
  * cpu_list:0-127
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540597927936
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:273113
    * volume_size:50G
    * volume_used:968M
    * cpu_list:0-255
  * worker 1
    * RAM:1077382602752
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1052-nvidia
    * node:cl-worker28
    * disk:375208
    * volume_size:50G
    * volume_used:768M
    * cpu_list:0-255
  * worker 2
    * RAM:1077381271552
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1336189
    * volume_size:50G
    * volume_used:884M
    * cpu_list:0-255
  * eval_parameters
    * code:1782072633
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Redis-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Redis-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| Redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2078.55 |                60138.00 |            125000.00 |                              7951.00 | 1.00 |               59.86 |
| Redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2083.96 |                59982.00 |            125000.00 |                              8279.00 | 1.00 |               60.02 |
| Redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2089.08 |                59835.00 |            125000.00 |                              8019.00 | 1.00 |               60.17 |
| Redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2087.93 |                59868.00 |            125000.00 |                              8111.00 | 1.00 |               60.13 |
| Redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2092.19 |                59746.00 |            125000.00 |                              7839.00 | 1.00 |               60.26 |
| Redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2075.31 |                60232.00 |            125000.00 |                              7923.00 | 1.00 |               59.77 |
| Redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2082.54 |                60023.00 |            125000.00 |                              7931.00 | 1.00 |               59.98 |
| Redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         2084.72 |                59960.00 |            125000.00 |                              7859.00 | 1.00 |               60.04 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |               59.77 |                        16674.27 |                60232.00 |           1000000.00 |                              7989.00 |

### Execution

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1-1-1-1 | Redis-1-1-1 | Redis-1-1-1-1 | Redis-1         |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        63969.70 |               156324.00 |            4998824 |                            5303.00 |              5001176 |                              5311.00 |
| Redis-1-2-1-1-1 | Redis-1-2-1 | Redis-1-2-1-1 | Redis-1         |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        64323.16 |               155465.00 |            5001491 |                            6263.00 |              4998509 |                              6275.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1-1 | Redis-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        63969.70 |               156324.00 |            4998824 |                            5303.00 |              5001176 |                              5311.00 |
| Redis-1-2-1 | Redis-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        64323.16 |               155465.00 |            5001491 |                            6263.00 |              4998509 |                              6275.00 |

### Monitoring

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       127.61 |      1.70 |           1.79 |                  1.80 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       101.97 |      3.78 |           0.12 |                  0.12 |

### Execution phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       400.64 |      2.94 |           2.41 |                  2.43 |
| Redis-1-2-1-1 |       329.28 |      2.86 |           2.04 |                  2.36 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       544.20 |      4.56 |           0.29 |                  0.29 |
| Redis-1-2-1-1 |       555.45 |      4.64 |           0.29 |                  0.29 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
