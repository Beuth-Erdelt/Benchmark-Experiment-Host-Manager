## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2341s 
* Code: 1781363250
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
  * Number of tenants is 2, one schema per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1064844
  * volume_size:20G
  * volume_used:732M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781363250
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1127350
  * volume_size:20G
  * volume_used:732M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781363250
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1127346
  * volume_size:20G
  * volume_used:716M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781363250
    * TENANT_BY:schema
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1126551
  * volume_size:20G
  * volume_used:716M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781363250
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

|                            |   experiment_run | type_tenants   | vol_tenants   |   num_tenants | tenant_id   |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:---------------------------|-----------------:|:---------------|:--------------|--------------:|:------------|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781363250-PostgreSQL-1-1- |                1 | schema         | False         |             2 |             |    1 |      329.00 |           3.00 |            0.00 |        143.00 |          183.00 |              2 |           1 |               10.94 |
| 1781363250-PostgreSQL-1-2- |                2 | schema         | False         |             2 |             |    1 |      329.00 |           3.00 |            0.00 |        143.00 |          183.00 |              2 |           1 |               10.94 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.48 |                        0.49 |       102.18 |                                                     101346.00 |                                              34564.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.45 |                        0.44 |        93.08 |                                                      88367.00 |                                              35675.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.51 |                        0.52 |       108.48 |                                                     129938.00 |                                              40953.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        97.28 |                                                      99525.00 |                                              46359.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.50 |                        0.50 |       105.68 |                                                     877941.00 |                                              95753.00 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.48 |                        0.48 |       100.08 |                                                     270192.00 |                                              58594.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.51 |                        0.52 |       109.18 |                                                     100384.00 |                                              34672.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.49 |                        0.48 |       101.48 |                                                      68012.00 |                                              26995.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-0 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.48 |                        0.49 |       102.18 |                                                     101346.00 |                                              34564.00 |
| PostgreSQL-1-1-1-1 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.45 |                        0.44 |        93.08 |                                                      88367.00 |                                              35675.00 |
| PostgreSQL-1-1-2-0 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.51 |                        0.52 |       108.48 |                                                     129938.00 |                                              40953.00 |
| PostgreSQL-1-1-2-1 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        97.28 |                                                      99525.00 |                                              46359.00 |
| PostgreSQL-1-2-1-0 | PostgreSQL-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.50 |                        0.50 |       105.68 |                                                     877941.00 |                                              95753.00 |
| PostgreSQL-1-2-1-1 | PostgreSQL-1-2-1 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.48 |                        0.48 |       100.08 |                                                     270192.00 |                                              58594.00 |
| PostgreSQL-1-2-2-0 | PostgreSQL-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.51 |                        0.52 |       109.18 |                                                     100384.00 |                                              34672.00 |
| PostgreSQL-1-2-2-1 | PostgreSQL-1-2-2 |                2 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.49 |                        0.48 |       101.48 |                                                      68012.00 |                                              26995.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        43.75 |      0.54 |           0.19 |                  0.89 |
| PostgreSQL-1-1-2-1 |        43.75 |      0.54 |           0.19 |                  0.89 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        17.76 |      0.17 |           0.26 |                  0.26 |
| PostgreSQL-1-1-2-1 |        17.76 |      0.17 |           0.26 |                  0.26 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         2.56 |      0.01 |           0.23 |                  0.95 |
| PostgreSQL-1-1-2-1 |         2.78 |      0.03 |           0.23 |                  0.95 |
| PostgreSQL-1-2-1-1 |        52.83 |      0.02 |           0.17 |                  0.89 |
| PostgreSQL-1-2-2-1 |         2.70 |      0.01 |           0.15 |                  0.41 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        40.39 |      0.74 |           0.23 |                  0.23 |
| PostgreSQL-1-1-2-1 |        47.36 |      1.28 |           0.23 |                  0.23 |
| PostgreSQL-1-2-1-1 |        70.30 |      1.24 |           0.23 |                  0.23 |
| PostgreSQL-1-2-2-1 |        69.75 |      1.42 |           0.23 |                  0.23 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        3.00 |                                    2.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     21.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                     21.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    1.00 |
| PostgreSQL-1-2-1-1 |                     21.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-1-2-2-1 |                     21.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
