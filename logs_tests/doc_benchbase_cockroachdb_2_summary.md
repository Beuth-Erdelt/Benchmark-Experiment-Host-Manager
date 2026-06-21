## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 4164s 
* Code: 1782055491
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
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
  * disk:216142
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1337281
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1345306
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:620263
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782055491
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:216142
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1339033
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1347039
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:622035
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782055491
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:216142
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1340410
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1347565
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:650929
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782055491
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* CockroachDB-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:216142
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1341594
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-223
  * worker 1
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1348705
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-255
  * worker 2
    * RAM:1081853939712
    * Cores:128
    * host:6.8.0-111-generic
    * node:cl-worker37
    * disk:652144
    * volume_size:1000G
    * volume_used:687G
    * cpu_list:0-127
  * eval_parameters
    * code:1782055491
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
| CockroachDB-1-1 |                1 |  128 |     1975.00 |           1.00 |            0.00 |        966.00 |         1008.00 |              1 |           1 |             | None           |             0 | False         |              233.32 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 600.00 |            0 |                        1541.05 |                     1535.52 |         0.00 |                                                    1871023.00 |                                             829782.00 |
| CockroachDB-1-1-2-1-1 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 600.00 |            0 |                         741.27 |                      738.71 |         0.00 |                                                    1981634.00 |                                             862151.00 |
| CockroachDB-1-1-2-1-2 | CockroachDB-1-1-2 | CockroachDB-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 600.00 |            0 |                         737.20 |                      734.65 |         0.00 |                                                    1988147.00 |                                             867463.00 |
| CockroachDB-1-1-3-1-1 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       1 |          -1 | 600.00 |            0 |                         339.66 |                      338.52 |         0.00 |                                                    2431388.00 |                                             941844.00 |
| CockroachDB-1-1-3-1-2 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       2 |          -1 | 600.00 |            0 |                         337.91 |                      336.83 |         0.00 |                                                    2427063.00 |                                             945364.00 |
| CockroachDB-1-1-3-1-3 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       3 |          -1 | 600.00 |            0 |                         337.73 |                      336.60 |         0.00 |                                                    2430128.00 |                                             946861.00 |
| CockroachDB-1-1-3-1-4 | CockroachDB-1-1-3 | CockroachDB-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       4 |          -1 | 600.00 |            0 |                         338.95 |                      337.86 |         0.00 |                                                    2432158.00 |                                             942643.00 |
| CockroachDB-1-1-4-1-1 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       1 |          -1 | 600.00 |            0 |                         154.23 |                      153.75 |         0.00 |                                                    3295750.00 |                                            1037129.00 |
| CockroachDB-1-1-4-1-2 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       2 |          -1 | 600.00 |            0 |                         151.53 |                      151.10 |         0.00 |                                                    3314576.00 |                                            1054383.00 |
| CockroachDB-1-1-4-1-3 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       3 |          -1 | 600.00 |            0 |                         153.01 |                      152.47 |         0.00 |                                                    3309776.00 |                                            1043854.00 |
| CockroachDB-1-1-4-1-4 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       4 |          -1 | 600.00 |            0 |                         153.94 |                      153.41 |         0.00 |                                                    3295236.00 |                                            1038736.00 |
| CockroachDB-1-1-4-1-5 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       5 |          -1 | 600.00 |            0 |                         152.09 |                      151.62 |         0.00 |                                                    3308383.00 |                                            1050320.00 |
| CockroachDB-1-1-4-1-6 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       6 |          -1 | 600.00 |            0 |                         151.54 |                      151.06 |         0.00 |                                                    3327774.00 |                                            1054468.00 |
| CockroachDB-1-1-4-1-7 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       7 |          -1 | 600.00 |            0 |                         152.09 |                      151.61 |         0.00 |                                                    3298953.00 |                                            1050350.00 |
| CockroachDB-1-1-4-1-8 | CockroachDB-1-1-4 | CockroachDB-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       8 |          -1 | 600.00 |            0 |                         154.04 |                      153.58 |         0.00 |                                                    3290726.00 |                                            1036986.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 600.00 |            0 |                        1541.05 |                     1535.52 |         0.00 |                                                    1871023.00 |                                             829782.00 |
| CockroachDB-1-1-2 | CockroachDB-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 600.00 |            0 |                        1478.47 |                     1473.36 |         0.00 |                                                    1988147.00 |                                             864807.00 |
| CockroachDB-1-1-3 | CockroachDB-1-1-3 |                1 |        1280 |    16384 |               1 |           4 |          -1 | 600.00 |            0 |                        1354.25 |                     1349.80 |         0.00 |                                                    2432158.00 |                                             944178.00 |
| CockroachDB-1-1-4 | CockroachDB-1-1-4 |                1 |        1280 |    16384 |               1 |           8 |          -1 | 600.00 |            0 |                        1222.47 |                     1218.62 |         0.00 |                                                    3327774.00 |                                            1045778.25 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     21373.55 |     38.83 |          21.31 |                 46.70 |
| CockroachDB-1-1-2-1 |     21373.55 |     38.83 |          21.31 |                 46.70 |
| CockroachDB-1-1-3-1 |     21373.55 |     38.83 |          21.31 |                 46.70 |
| CockroachDB-1-1-4-1 |     21373.55 |     38.83 |          21.31 |                 46.70 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     12581.27 |     32.88 |           0.29 |                  0.29 |
| CockroachDB-1-1-2-1 |     12581.27 |     32.88 |           0.29 |                  0.29 |
| CockroachDB-1-1-3-1 |     12581.27 |     32.88 |           0.29 |                  0.29 |
| CockroachDB-1-1-4-1 |     12581.27 |     32.88 |           0.29 |                  0.29 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     25952.19 |     45.76 |          32.96 |                 61.84 |
| CockroachDB-1-1-2-1 |     26576.81 |     45.78 |          33.26 |                 65.74 |
| CockroachDB-1-1-3-1 |     25718.20 |     45.43 |          35.73 |                 73.66 |
| CockroachDB-1-1-4-1 |     25137.44 |     44.15 |          36.94 |                 77.13 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |      1172.47 |      2.14 |           4.20 |                  4.20 |
| CockroachDB-1-1-2-1 |      1172.47 |      4.93 |           4.19 |                  4.19 |
| CockroachDB-1-1-3-1 |      1264.91 |      5.64 |           2.55 |                  2.55 |
| CockroachDB-1-1-4-1 |      1139.44 |      4.23 |           1.67 |                  1.67 |

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                     7133.99 |                   61682485.31 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-2-1 |                                     7133.99 |                   61682485.31 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-3-1 |                                     7133.99 |                   61682485.31 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-4-1 |                                     7133.99 |                   61682485.31 |                                    0.00 |                                      0.00 |                              0.00 |

#### Execution phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                    32361.26 |                   15892006.20 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-2-1 |                                    18769.58 |                   10597888.57 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-3-1 |                                    27171.11 |                   16531764.69 |                                    0.00 |                                      0.00 |                              0.00 |
| CockroachDB-1-1-4-1 |                                    22752.81 |                   12450659.53 |                                    0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
