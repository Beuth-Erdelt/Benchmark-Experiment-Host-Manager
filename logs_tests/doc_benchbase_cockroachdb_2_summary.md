## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 4530s 
* Code: 1782200972
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Experiment uses bexhoma version 0.9.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 100Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219933
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:945056
    * datadisk:713090
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:653288
    * datadisk:712889
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1346530
    * datadisk:712955
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782200972
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219933
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:945907
    * datadisk:714733
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:654951
    * datadisk:714552
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1348075
    * datadisk:714586
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782200972
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219933
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:947230
    * datadisk:716042
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:656205
    * datadisk:715803
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1349387
    * datadisk:715892
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782200972
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:219933
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:947853
    * datadisk:716638
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:656830
    * datadisk:716420
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1350100
    * datadisk:716527
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * eval_parameters
    * code:1782200972
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 4: benchbase (8 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 4: benchbase (8 pods)

### Loading

#### Per Run

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| CockroachDB-1-1 |                1 |  128 |     1834.00 |           2.00 |            0.00 |        895.00 |          937.00 |              1 |           1 |             | None           |             0 | False         |              251.25 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 600.00 |            0 |                        1433.76 |                     1429.40 |         0.00 |                                                    2140035.00 |                                             891948.00 |
| CockroachDB-1-1-2-1-1 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 600.00 |            0 |                         681.77 |                      679.52 |         0.00 |                                                    2255359.00 |                                             937254.00 |
| CockroachDB-1-1-2-1-2 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 600.00 |            0 |                         679.37 |                      677.29 |         0.00 |                                                    2255904.00 |                                             940441.00 |
| CockroachDB-1-1-3-1-1 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       1 |          -1 | 600.00 |          135 |                         190.19 |                      189.40 |         0.00 |                                                    1838032.00 |                                             430662.00 |
| CockroachDB-1-1-3-1-2 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       2 |          -1 | 600.00 |          130 |                         192.82 |                      192.01 |         0.00 |                                                    1817723.00 |                                             420804.00 |
| CockroachDB-1-1-3-1-3 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       3 |          -1 | 600.00 |          116 |                         191.45 |                      190.66 |         0.00 |                                                    1844212.00 |                                             428645.00 |
| CockroachDB-1-1-3-1-4 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       4 |          -1 | 600.00 |          125 |                         192.21 |                      191.50 |         0.00 |                                                    1829561.00 |                                             422160.00 |
| CockroachDB-1-1-4-1-1 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       1 |          -1 | 600.00 |            0 |                         162.08 |                      161.39 |         0.00 |                                                    2953853.00 |                                             985895.00 |
| CockroachDB-1-1-4-1-2 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       2 |          -1 | 600.00 |            0 |                         163.61 |                      162.91 |         0.00 |                                                    2969501.00 |                                             977120.00 |
| CockroachDB-1-1-4-1-3 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       3 |          -1 | 600.00 |            0 |                         161.40 |                      160.65 |         0.00 |                                                    2990804.00 |                                             990396.00 |
| CockroachDB-1-1-4-1-4 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       4 |          -1 | 600.00 |            0 |                         163.49 |                      162.72 |         0.00 |                                                    2957625.00 |                                             976775.00 |
| CockroachDB-1-1-4-1-5 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       5 |          -1 | 600.00 |            0 |                         164.38 |                      163.66 |         0.00 |                                                    2953000.00 |                                             971489.00 |
| CockroachDB-1-1-4-1-6 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       6 |          -1 | 600.00 |            0 |                         164.46 |                      163.81 |         0.00 |                                                    2928477.00 |                                             971520.00 |
| CockroachDB-1-1-4-1-7 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       7 |          -1 | 600.00 |            0 |                         161.81 |                      161.13 |         0.00 |                                                    2974160.00 |                                             988162.00 |
| CockroachDB-1-1-4-1-8 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       8 |          -1 | 600.00 |            0 |                         161.48 |                      160.75 |         0.00 |                                                    2971232.00 |                                             989138.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 600.00 |            0 |                        1433.76 |                     1429.40 |         0.00 |                                                    2140035.00 |                                             891948.00 |
| CockroachDB-1-1-2 | CockroachDB-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 600.00 |            0 |                        1361.14 |                     1356.81 |         0.00 |                                                    2255904.00 |                                             938847.50 |
| CockroachDB-1-1-3 | CockroachDB-1-1-3 |                1 |        1280 |    16384 |               1 |           4 |          -1 | 600.00 |          506 |                         766.67 |                      763.57 |         0.00 |                                                    1844212.00 |                                             425567.75 |
| CockroachDB-1-1-4 | CockroachDB-1-1-4 |                1 |        1280 |    16384 |               1 |           8 |          -1 | 600.00 |            0 |                        1302.71 |                     1297.04 |         0.00 |                                                    2990804.00 |                                             981311.88 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     22636.06 |     38.32 |          17.40 |                 42.76 |
| CockroachDB-1-1-2-1 |     22636.06 |     38.32 |          17.40 |                 42.76 |
| CockroachDB-1-1-3-1 |     22636.06 |     38.32 |          17.40 |                 42.76 |
| CockroachDB-1-1-4-1 |     22636.06 |     38.32 |          17.40 |                 42.76 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     11759.89 |     31.93 |           0.29 |                  0.29 |
| CockroachDB-1-1-2-1 |     11759.89 |     31.93 |           0.29 |                  0.29 |
| CockroachDB-1-1-3-1 |     11759.89 |     31.93 |           0.29 |                  0.29 |
| CockroachDB-1-1-4-1 |     11759.89 |     31.93 |           0.29 |                  0.29 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     24959.14 |     45.01 |          26.77 |                 56.83 |
| CockroachDB-1-1-2-1 |     25592.87 |     44.51 |          31.65 |                 65.54 |
| CockroachDB-1-1-3-1 |     21441.38 |     42.99 |          31.67 |                 67.45 |
| CockroachDB-1-1-4-1 |     25938.91 |     44.74 |          37.95 |                 76.70 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |      1068.67 |      2.18 |           4.18 |                  4.18 |
| CockroachDB-1-1-2-1 |      1038.04 |      4.01 |           4.18 |                  4.18 |
| CockroachDB-1-1-3-1 |      3067.58 |      6.66 |           2.40 |                  2.40 |
| CockroachDB-1-1-4-1 |      3352.71 |      6.79 |           1.84 |                  1.84 |

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                     8568.43 |                   73447301.51 |                                    0.00 |                                      0.41 |                              0.00 |
| CockroachDB-1-1-2-1 |                                     8568.43 |                   73447301.51 |                                    0.00 |                                      0.41 |                              0.00 |
| CockroachDB-1-1-3-1 |                                     8568.43 |                   73447301.51 |                                    0.00 |                                      0.41 |                              0.00 |
| CockroachDB-1-1-4-1 |                                     8568.43 |                   73447301.51 |                                    0.00 |                                      0.41 |                              0.00 |

#### Execution phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                    35982.12 |                   32959116.01 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-2-1 |                                    12003.49 |                    7357817.68 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-3-1 |                                    42754.44 |                   19414843.58 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-4-1 |                                    44243.44 |                   27651289.76 |                                    0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
