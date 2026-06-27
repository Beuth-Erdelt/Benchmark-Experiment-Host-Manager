## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 379s 
* Code: 1782070107
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
* Redis-1-1-1-1 uses docker image redis:8.6.1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:239801
  * cpu_list:0-127
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782070107

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| Redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7283.53 |                17162.00 |            125000.00 |                              2773.00 | 1.00 |              209.77 |
| Redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7181.02 |                17407.00 |            125000.00 |                              2855.00 | 1.00 |              206.81 |
| Redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7282.26 |                17165.00 |            125000.00 |                              2791.00 | 1.00 |              209.73 |
| Redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7257.32 |                17224.00 |            125000.00 |                              2769.00 | 1.00 |              209.01 |
| Redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7191.76 |                17381.00 |            125000.00 |                              2775.00 | 1.00 |              207.12 |
| Redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7451.12 |                16776.00 |            125000.00 |                              2791.00 | 1.00 |              214.59 |
| Redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7316.79 |                17084.00 |            125000.00 |                              2745.00 | 1.00 |              210.72 |
| Redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7130.63 |                17530.00 |            125000.00 |                              2801.00 | 1.00 |              205.36 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              205.36 |                        58094.43 |                17530.00 |           1000000.00 |                              2787.50 |

### Execution

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1-1-1-1 | Redis-1-1-1 | Redis-1-1-1-1 | Redis-1         |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65499.04 |               152674.00 |            5000103 |                            1084.00 |              4999897 |                              1066.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1-1 | Redis-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65499.04 |               152674.00 |            5000103 |                            1084.00 |              4999897 |                              1066.00 |

### Monitoring

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| Redis-1-1-1-1 |       628.62 |      5.85 |           0.12 |                  0.13 |

### Tests
* TEST failed: Loading phase: component loader contains 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
