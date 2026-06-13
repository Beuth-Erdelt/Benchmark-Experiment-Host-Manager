## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2306s 
* Code: 1781333310
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
  * Number of tenants is 2, one database per tenant.
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
  * volume_used:728M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333310
    * TENANT_BY:database
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
  * volume_used:728M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333310
    * TENANT_BY:database
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
  * volume_used:732M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333310
    * TENANT_BY:database
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
  * volume_used:732M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333310
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

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      325.00 |           3.00 |            0.00 |        139.00 |          183.00 |              2 |           1 |          | database       |             2 | False         |               11.08 |
| PostgreSQL-1-2 |                2 |    1 |      325.00 |           3.00 |            0.00 |        139.00 |          183.00 |              2 |           1 |          | database       |             2 | False         |               11.08 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 | 300.00 |            0 |                           0.51 |                        0.51 |       107.08 |                                                      46876.00 |                                              15979.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 | 300.00 |            0 |                           0.45 |                        0.46 |        95.88 |                                                      53148.00 |                                              16709.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 | 300.00 |            0 |                           0.48 |                        0.47 |        99.38 |                                                      88647.00 |                                              30534.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 | 300.00 |            0 |                           0.47 |                        0.48 |       100.08 |                                                      92283.00 |                                              31060.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 | 300.00 |            0 |                           0.45 |                        0.45 |        94.48 |                                                     814864.00 |                                              84822.00 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       2 | 300.00 |            0 |                           0.50 |                        0.50 |       104.98 |                                                     231557.00 |                                              46249.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 | 300.00 |            0 |                           0.50 |                        0.50 |       104.98 |                                                      62576.00 |                                              19643.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       2 | 300.00 |            0 |                           0.49 |                        0.49 |       102.88 |                                                      50769.00 |                                              17734.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |          20 |     2048 |               1 |           2 | 300.00 |            0 |                           0.96 |                        0.97 |         0.00 |                                                      53148.00 |                                              16344.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |          20 |     2048 |               1 |           2 | 300.00 |            0 |                           0.95 |                        0.95 |         0.00 |                                                      92283.00 |                                              30797.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |          20 |     2048 |               1 |           2 | 300.00 |            0 |                           0.95 |                        0.95 |         0.00 |                                                     814864.00 |                                              65535.50 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |          20 |     2048 |               1 |           2 | 300.00 |            0 |                           0.99 |                        0.99 |         0.00 |                                                      62576.00 |                                              18688.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        33.73 |      0.33 |           0.19 |                  0.89 |
| PostgreSQL-1-1-2-1 |        33.73 |      0.33 |           0.19 |                  0.89 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        16.19 |      0.22 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2-1 |        16.19 |      0.22 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         4.54 |      0.09 |           0.23 |                  0.95 |
| PostgreSQL-1-1-2-1 |         3.84 |      0.02 |           0.23 |                  0.95 |
| PostgreSQL-1-2-1-1 |        47.59 |      0.02 |           0.17 |                  0.89 |
| PostgreSQL-1-2-2-1 |         4.32 |      0.02 |           0.15 |                  0.42 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        49.56 |      1.04 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |        69.97 |      2.00 |           0.11 |                  0.11 |
| PostgreSQL-1-2-1-1 |        83.47 |      0.20 |           0.15 |                  0.15 |
| PostgreSQL-1-2-2-1 |        74.29 |      1.59 |           0.15 |                  0.15 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      3.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    5.00 |
| PostgreSQL-1-1-2-1 |                      3.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    5.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     23.00 |                                     1.00 |                                             0.00 |                        4.00 |                                    1.00 |
| PostgreSQL-1-1-2-1 |                     23.00 |                                     1.00 |                                             0.00 |                        4.00 |                                    1.00 |
| PostgreSQL-1-2-1-1 |                     23.00 |                                     0.00 |                                             0.00 |                       12.00 |                                   10.00 |
| PostgreSQL-1-2-2-1 |                     23.00 |                                     1.00 |                                             0.00 |                        4.00 |                                    1.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
