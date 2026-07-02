## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2632s 
* Code: 1782921706
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:641950
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:653020
    * volume_size:50G
    * volume_used:740M
    * cpu_list:0-127
  * worker 1
    * RAM:540590841856
    * Cores:96
    * host:6.8.0-117-generic
    * node:cl-worker25
    * disk:189091
    * volume_size:50G
    * volume_used:808M
    * cpu_list:0-95
  * worker 2
    * RAM:1081742745600
    * node:cl-worker29
    * disk:806887
    * volume_size:50G
    * volume_used:1012M
    * cpu_list:0-127
  * eval_parameters
    * code:1782921706
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-2-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173246464
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:610506
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:610563
    * volume_size:50G
    * volume_used:788M
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:653019
    * volume_size:50G
    * volume_used:792M
    * cpu_list:0-127
  * worker 2
    * RAM:1081742745600
    * Cores:128
    * host:6.8.0-117-generic
    * node:cl-worker29
    * disk:807192
    * volume_size:50G
    * volume_used:768M
    * cpu_list:0-127
  * worker 3
  * eval_parameters
    * code:1782921706
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1782921706-b76d675f6-mgrbb: 0
* bexhoma-worker-cockroachdb-ycsb-1-0: 0
* bexhoma-worker-cockroachdb-ycsb-1-1: 0
* bexhoma-worker-cockroachdb-ycsb-1-2: 1

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           54.77 |               171291.00 |              9381.00 |                            397823.00 | 1.00 |               21.02 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           41.28 |               540333.00 |             22307.00 |                            299519.00 | 1.00 |                6.66 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           55.84 |               172054.00 |              9607.00 |                            397311.00 | 1.00 |               20.92 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           70.72 |               539436.00 |             38149.00 |                            274687.00 | 1.00 |                6.67 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           54.96 |               171495.00 |              9426.00 |                            397311.00 | 1.00 |               20.99 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           74.01 |               171865.00 |             12720.00 |                            393471.00 | 1.00 |               20.95 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           68.29 |               540656.00 |             36921.00 |                            271103.00 | 1.00 |                6.66 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                           92.05 |               540842.00 |             49784.00 |                            257663.00 | 1.00 |                6.66 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |                6.66 |                          511.92 |               540842.00 |            188295.00 |                            336111.00 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [READ-FAILED].Operations |   [READ-FAILED].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|---------------------------:|------------------------------------------:|-----------------------------:|--------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |          128 |                            0.00 |                  251.00 |                  0 |                               0.00 |                    0 |                                 0.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| CockroachDB-1-2-1-1-1 | CockroachDB-1-2-1 | CockroachDB-1-2-1-1 | CockroachDB-1   |                2 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         3244.00 |               308261.00 |              72914 |                          136959.00 |                72505 |                           3612671.00 |                     426870 |                                   3537.00 |                       427711 |                                     3867.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [READ-FAILED].Operations |   [READ-FAILED].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|---------------------------:|------------------------------------------:|-----------------------------:|--------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |          128 |                            0.00 |                  251.00 |                  0 |                               0.00 |                    0 |                                 0.00 |                          0 |                                      0.00 |                            0 |                                        0.00 |
| CockroachDB-1-2-1 | CockroachDB-1-2-1 |                2 |        64 |    65536 |               1 |           1 |            0 |                         3244.00 |               308261.00 |              72914 |                          136959.00 |                72505 |                           3612671.00 |                     426870 |                                   3537.00 |                       427711 |                                     3867.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       847.72 |      3.16 |           3.49 |                  6.51 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |        51.53 |      0.65 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |         0.00 |      0.38 |           2.47 |                  3.86 |
| CockroachDB-1-2-1-1 |      1833.85 |     10.51 |           3.74 |                  4.96 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| CockroachDB-1-2-1-1 |        72.71 |      0.39 |           0.13 |                  0.13 |

### Tests
* TEST failed: No SUT container restarts
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component worker contains 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST failed: Execution Phase: [OVERALL].Throughput(ops/sec) contains 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
