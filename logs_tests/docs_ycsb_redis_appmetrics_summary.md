## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 632s 
* Code: 1783892151
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
  * Experiment uses bexhoma version 0.10.5.
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

### Connections
* Redis-1-1-1-1 uses docker image redis:7.4.2
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1086940
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077382598656
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1058-nvidia
    * node:cl-worker28
    * disk:578614
    * cpu_list:0-255
  * worker 1
    * RAM:540590841856
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:161323
    * cpu_list:0-95
  * worker 2
    * RAM:1077381287936
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1371668
    * cpu_list:0-255
  * worker 3
    * RAM:540590804992
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-124-generic
    * node:cl-worker24
    * disk:134433
    * cpu_list:0-95
  * worker 4
    * RAM:540597907456
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-124-generic
    * node:cl-worker39
    * disk:321198
    * cpu_list:0-255
  * worker 5
    * RAM:1081742745600
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:942030
    * cpu_list:0-127
  * eval_parameters
    * code:1783892151
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-redis-1-1783892151-65474664c6-5kghb: 0
* bx-w-redis-ycsb-1-0: 0 0
* bx-w-redis-ycsb-1-1: 0 0
* bx-w-redis-ycsb-1-2: 0 0
* bx-w-redis-ycsb-1-3: 0 0
* bx-w-redis-ycsb-1-4: 0 0
* bx-w-redis-ycsb-1-5: 0 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| Redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         1836.16 |                68077.00 |            125000.00 |                              9303.00 | 1.00 |               52.88 |
| Redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         1833.38 |                68180.00 |            125000.00 |                              9463.00 | 1.00 |               52.80 |
| Redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         1842.43 |                67845.00 |            125000.00 |                              9487.00 | 1.00 |               53.06 |
| Redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         1834.38 |                68143.00 |            125000.00 |                              9439.00 | 1.00 |               52.83 |
| Redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         1835.72 |                68093.00 |            125000.00 |                              9599.00 | 1.00 |               52.87 |
| Redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         1838.51 |                67990.00 |            125000.00 |                              9359.00 | 1.00 |               52.95 |
| Redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         1833.70 |                68168.00 |            125000.00 |                              9447.00 | 1.00 |               52.81 |
| Redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         1858.18 |                67270.00 |            125000.00 |                              9447.00 | 1.00 |               53.52 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |               52.80 |                        14712.47 |                68180.00 |           1000000.00 |                              9443.00 |

### Execution

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1-1-1-1 | Redis-1-1-1 | Redis-1-1-1-1 | Redis-1         |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        55248.62 |               181000.00 |            4999079 |                            6587.00 |              5000921 |                              6555.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1-1 | Redis-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        55248.62 |               181000.00 |            4999079 |                            6587.00 |              5000921 |                              6555.00 |

### Monitoring

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       225.56 |      3.38 |           3.59 |                  3.59 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       153.24 |      2.77 |           0.12 |                  0.12 |

### Execution phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       565.16 |      4.29 |           4.04 |                  4.06 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       547.77 |      4.29 |           0.30 |                  0.30 |

### Application Metrics

#### Loading phase: component worker

| DBMS          |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [Gi] |   Redis Master Link Status |   Redis Operations Rate [ops/s] |
|:--------------|----------------------:|----------------------------:|-------------------------:|---------------------------:|--------------------------------:|
| Redis-1-1-1-1 |                  6.00 |                      201.00 |                     3.46 |                       3.00 |                         5530.00 |

#### Execution phase: component worker

| DBMS          |   Redis Cluster State |   Connected Clients [count] |   Redis Memory Used [Gi] |   Redis Master Link Status |   Redis Operations Rate [ops/s] |
|:--------------|----------------------:|----------------------------:|-------------------------:|---------------------------:|--------------------------------:|
| Redis-1-1-1-1 |                  6.00 |                      393.00 |                     3.50 |                       3.00 |                         6813.02 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
