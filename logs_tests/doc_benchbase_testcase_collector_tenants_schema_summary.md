## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2363s 
* Code: 1781333299
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.11.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 20Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921677
  * volume_size:20G
  * volume_used:652M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333299
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921677
  * volume_size:20G
  * volume_used:652M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333299
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921679
  * volume_size:20G
  * volume_used:652M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333299
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921680
  * volume_size:20G
  * volume_used:652M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333299
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      378.00 |           2.00 |            0.00 |        162.00 |          214.00 |              2 |           1 |          | schema         |             2 | False         |                9.52 |
| PostgreSQL-1-2 |                2 |    1 |      378.00 |           2.00 |            0.00 |        162.00 |          214.00 |              2 |           1 |          | schema         |             2 | False         |                9.52 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 | 300.00 |            0 |                           0.57 |                        0.57 |       119.67 |                                                      75406.00 |                                              19572.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 | 300.00 |            0 |                           0.48 |                        0.48 |       101.48 |                                                      60710.00 |                                              18888.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 | 300.00 |            0 |                           0.43 |                        0.43 |        90.98 |                                                     110145.00 |                                              49951.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 | 300.00 |            0 |                           0.44 |                        0.45 |        93.78 |                                                     146040.00 |                                              53004.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 | 300.00 |            0 |                           0.48 |                        0.48 |       100.78 |                                                     481174.00 |                                              83920.00 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       2 | 300.00 |            0 |                           0.42 |                        0.42 |        87.48 |                                                     517770.00 |                                              83629.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 | 300.00 |            0 |                           0.46 |                        0.46 |        97.28 |                                                      92212.00 |                                              34073.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       2 | 300.00 |            0 |                           0.46 |                        0.46 |        97.28 |                                                      87170.00 |                                              31773.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |          20 |     2048 |               1 |           2 | 300.00 |            0 |                           1.05 |                        1.05 |         0.00 |                                                      75406.00 |                                              19230.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |          20 |     2048 |               1 |           2 | 300.00 |            0 |                           0.88 |                        0.88 |         0.00 |                                                     146040.00 |                                              51477.50 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |          20 |     2048 |               1 |           2 | 300.00 |            0 |                           0.89 |                        0.90 |         0.00 |                                                     517770.00 |                                              83774.50 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |          20 |     2048 |               1 |           2 | 300.00 |            0 |                           0.92 |                        0.93 |         0.00 |                                                      92212.00 |                                              32923.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        27.65 |      0.27 |           0.20 |                  0.81 |
| PostgreSQL-1-1-2-1 |        27.65 |      0.27 |           0.20 |                  0.81 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        16.60 |      0.13 |           0.24 |                  0.24 |
| PostgreSQL-1-1-2-1 |        16.60 |      0.13 |           0.24 |                  0.24 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         2.66 |      0.08 |           0.23 |                  0.87 |
| PostgreSQL-1-1-2-1 |         2.12 |      0.02 |           0.23 |                  0.87 |
| PostgreSQL-1-2-1-1 |        35.98 |      0.02 |           0.17 |                  0.81 |
| PostgreSQL-1-2-2-1 |         2.21 |      0.01 |           0.15 |                  0.41 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        57.35 |      1.23 |           0.23 |                  0.23 |
| PostgreSQL-1-1-2-1 |        78.59 |      1.68 |           0.23 |                  0.23 |
| PostgreSQL-1-2-1-1 |        57.16 |      1.14 |           0.23 |                  0.23 |
| PostgreSQL-1-2-2-1 |        55.31 |      1.75 |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    2.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    2.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     21.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-1-1-2-1 |                     21.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-1-2-1-1 |                     21.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    4.00 |
| PostgreSQL-1-2-2-1 |                     21.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
