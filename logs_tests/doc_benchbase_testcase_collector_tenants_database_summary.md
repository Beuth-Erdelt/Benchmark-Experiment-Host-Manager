## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2356s 
* Code: 1781365622
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.12.
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
  * Number of tenants is 2, one database per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1058828
  * volume_size:20G
  * volume_used:748M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781365622
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1051532
  * volume_size:20G
  * volume_used:748M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781365622
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1058831
  * volume_size:20G
  * volume_used:732M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781365622
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1058834
  * volume_size:20G
  * volume_used:732M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781365622
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[2, 2], [2, 2]]

### Loading

#### Per Run

|                            |   experiment_run | type_tenants   | vol_tenants   |   num_tenants | tenant_id   |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:---------------------------|-----------------:|:---------------|:--------------|--------------:|:------------|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781365622-PostgreSQL-1-1- |                1 | database       | False         |             2 |             |    1 |      336.00 |           3.00 |            0.00 |        150.00 |          183.00 |              2 |           1 |               10.71 |
| 1781365622-PostgreSQL-1-2- |                2 | database       | False         |             2 |             |    1 |      336.00 |           3.00 |            0.00 |        150.00 |          183.00 |              2 |           1 |               10.71 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.45 |                        0.45 |        93.78 |                                                     157986.00 |                                              30510.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.47 |                        0.48 |       100.08 |                                                     120466.00 |                                              30365.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        96.58 |                                                      64443.00 |                                              25982.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.51 |                        0.51 |       106.38 |                                                      64894.00 |                                              28926.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.50 |                        0.49 |       102.88 |                                                     718407.00 |                                             121635.00 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.52 |                        0.52 |       108.48 |                                                     376034.00 |                                              79215.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.47 |                        0.47 |        98.68 |                                                      53545.00 |                                              19002.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.56 |                        0.57 |       118.97 |                                                      55120.00 |                                              17660.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-0 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.45 |                        0.45 |        93.78 |                                                     157986.00 |                                              30510.00 |
| PostgreSQL-1-1-1-1 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.47 |                        0.48 |       100.08 |                                                     120466.00 |                                              30365.00 |
| PostgreSQL-1-1-2-0 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        96.58 |                                                      64443.00 |                                              25982.00 |
| PostgreSQL-1-1-2-1 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.51 |                        0.51 |       106.38 |                                                      64894.00 |                                              28926.00 |
| PostgreSQL-1-2-1-0 | PostgreSQL-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.50 |                        0.49 |       102.88 |                                                     718407.00 |                                             121635.00 |
| PostgreSQL-1-2-1-1 | PostgreSQL-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.52 |                        0.52 |       108.48 |                                                     376034.00 |                                              79215.00 |
| PostgreSQL-1-2-2-0 | PostgreSQL-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.47 |                        0.47 |        98.68 |                                                      53545.00 |                                              19002.00 |
| PostgreSQL-1-2-2-1 | PostgreSQL-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.56 |                        0.57 |       118.97 |                                                      55120.00 |                                              17660.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        34.37 |      0.31 |           0.20 |                  0.90 |
| PostgreSQL-1-1-2-1 |        34.37 |      0.31 |           0.20 |                  0.90 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        15.99 |      0.16 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2-1 |        15.99 |      0.16 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         4.67 |      0.10 |           0.23 |                  0.96 |
| PostgreSQL-1-1-2-1 |         4.24 |      0.02 |           0.23 |                  0.96 |
| PostgreSQL-1-2-1-1 |        49.56 |      0.02 |           0.17 |                  0.91 |
| PostgreSQL-1-2-2-1 |         4.47 |      0.02 |           0.16 |                  0.43 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        32.86 |      0.42 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |        32.00 |      0.60 |           0.23 |                  0.23 |
| PostgreSQL-1-2-1-1 |        36.28 |      0.43 |           0.23 |                  0.23 |
| PostgreSQL-1-2-2-1 |        45.39 |      1.40 |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      3.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    5.00 |
| PostgreSQL-1-1-2-1 |                      3.00 |                                     0.00 |                                             0.00 |                        6.00 |                                    5.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     22.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                     22.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-1-2-1-1 |                     22.00 |                                     1.00 |                                             0.00 |                        4.00 |                                    4.00 |
| PostgreSQL-1-2-2-1 |                     23.00 |                                     1.00 |                                             0.00 |                        3.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
