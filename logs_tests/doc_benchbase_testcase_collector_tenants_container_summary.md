## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2405s 
* Code: 1781333318
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
  * Database is persisted to disk of type shared and size 10Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921677
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333318
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921677
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333318
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921679
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333318
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921680
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333318
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* PostgreSQL-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921677
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333318
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-2-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921677
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333318
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-2-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921679
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333318
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* PostgreSQL-2-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921680
  * volume_size:10G
  * volume_used:328M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781333318
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-2 - Pods [[1, 1], [1, 1]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 1], [1, 1]]
* DBMS PostgreSQL-2 - Pods [[1, 1], [1, 1]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   tenant | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|---------:|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      210.00 |           1.00 |            0.00 |         88.00 |          121.00 |              1 |           1 |        0 | container      |             2 | False         |               17.14 |
| PostgreSQL-1-2 |                2 |    1 |      210.00 |           1.00 |            0.00 |         88.00 |          121.00 |              1 |           1 |        0 | container      |             2 | False         |               17.14 |
| PostgreSQL-2-1 |                1 |    1 |      189.00 |           1.00 |            0.00 |         70.00 |          118.00 |              1 |           1 |        1 | container      |             2 | False         |               19.05 |
| PostgreSQL-2-2 |                2 |    1 |      189.00 |           1.00 |            0.00 |         70.00 |          118.00 |              1 |           1 |        1 | container      |             2 | False         |               19.05 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 | 300.00 |            0 |                           0.48 |                        0.48 |       101.48 |                                                      55107.00 |                                              28783.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 | 300.00 |            0 |                           0.47 |                        0.46 |        96.58 |                                                      56462.00 |                                              19337.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 | 300.00 |            0 |                           0.46 |                        0.46 |        97.28 |                                                     285632.00 |                                              62161.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 | 300.00 |            0 |                           0.48 |                        0.48 |       100.08 |                                                      76694.00 |                                              26373.00 |
| PostgreSQL-2-1-1-1-1 | PostgreSQL-2-1-1 | PostgreSQL-2-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 | 300.00 |            0 |                           0.45 |                        0.45 |        95.18 |                                                      38880.00 |                                              15079.00 |
| PostgreSQL-2-1-2-1-1 | PostgreSQL-2-1-2 | PostgreSQL-2-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 | 300.00 |            0 |                           0.52 |                        0.52 |       109.18 |                                                      69047.00 |                                              19742.00 |
| PostgreSQL-2-2-1-1-1 | PostgreSQL-2-2-1 | PostgreSQL-2-2-1-1 |                2 |          10 |     1024 |        1 |               1 |       1 | 300.00 |            0 |                           0.46 |                        0.45 |        95.18 |                                                     407824.00 |                                              85501.00 |
| PostgreSQL-2-2-2-1-1 | PostgreSQL-2-2-2 | PostgreSQL-2-2-2-1 |                2 |          10 |     1024 |        2 |               1 |       1 | 300.00 |            0 |                           0.47 |                        0.47 |        98.68 |                                                      71703.00 |                                              23470.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 | 300.00 |            0 |                           0.48 |                        0.48 |       101.48 |                                                      55107.00 |                                              28783.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 | 300.00 |            0 |                           0.47 |                        0.46 |        96.58 |                                                      56462.00 |                                              19337.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |          10 |     1024 |               1 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        97.28 |                                                     285632.00 |                                              62161.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |          10 |     1024 |               1 |           1 | 300.00 |            0 |                           0.48 |                        0.48 |       100.08 |                                                      76694.00 |                                              26373.00 |
| PostgreSQL-2-1-1 | PostgreSQL-2-1-1 |                1 |          10 |     1024 |               1 |           1 | 300.00 |            0 |                           0.45 |                        0.45 |        95.18 |                                                      38880.00 |                                              15079.00 |
| PostgreSQL-2-1-2 | PostgreSQL-2-1-2 |                1 |          10 |     1024 |               1 |           1 | 300.00 |            0 |                           0.52 |                        0.52 |       109.18 |                                                      69047.00 |                                              19742.00 |
| PostgreSQL-2-2-1 | PostgreSQL-2-2-1 |                2 |          10 |     1024 |               1 |           1 | 300.00 |            0 |                           0.46 |                        0.45 |        95.18 |                                                     407824.00 |                                              85501.00 |
| PostgreSQL-2-2-2 | PostgreSQL-2-2-2 |                2 |          10 |     1024 |               1 |           1 | 300.00 |            0 |                           0.47 |                        0.47 |        98.68 |                                                      71703.00 |                                              23470.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        20.29 |      0.26 |           0.16 |                  0.48 |
| PostgreSQL-1-1-2-1 |        20.29 |      0.26 |           0.16 |                  0.48 |
| PostgreSQL-2-1-1-1 |        10.81 |      0.21 |           0.16 |                  0.48 |
| PostgreSQL-2-1-2-1 |        10.81 |      0.21 |           0.16 |                  0.48 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         7.48 |      0.17 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2-1 |         7.48 |      0.17 |           0.25 |                  0.25 |
| PostgreSQL-2-1-1-1 |         8.87 |      0.20 |           0.26 |                  0.26 |
| PostgreSQL-2-1-2-1 |         8.87 |      0.20 |           0.26 |                  0.26 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         1.60 |      0.01 |           0.19 |                  0.52 |
| PostgreSQL-1-1-2-1 |         1.52 |      0.01 |           0.19 |                  0.51 |
| PostgreSQL-1-2-1-1 |        26.50 |      0.01 |           0.16 |                  0.49 |
| PostgreSQL-1-2-2-1 |         1.82 |      0.01 |           0.10 |                  0.24 |
| PostgreSQL-2-1-1-1 |         1.84 |      0.01 |           0.19 |                  0.51 |
| PostgreSQL-2-1-2-1 |         1.70 |      0.01 |           0.19 |                  0.52 |
| PostgreSQL-2-2-1-1 |        17.27 |      0.01 |           0.16 |                  0.49 |
| PostgreSQL-2-2-2-1 |         1.66 |      0.01 |           0.10 |                  0.23 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        20.00 |      0.37 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |        26.50 |      0.70 |           0.11 |                  0.11 |
| PostgreSQL-1-2-1-1 |        17.36 |      0.30 |           0.11 |                  0.11 |
| PostgreSQL-1-2-2-1 |        17.56 |      0.42 |           0.11 |                  0.11 |
| PostgreSQL-2-1-1-1 |        45.92 |      1.01 |           0.23 |                  0.23 |
| PostgreSQL-2-1-2-1 |        62.39 |      1.12 |           0.23 |                  0.23 |
| PostgreSQL-2-2-1-1 |        18.25 |      0.37 |           0.11 |                  0.11 |
| PostgreSQL-2-2-2-1 |        18.25 |      0.48 |           0.11 |                  0.11 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-2-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-2-1-2-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-1-2-1-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-1-2-2-1 |                     11.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |
| PostgreSQL-2-1-1-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-2-1-2-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-2-2-1-1 |                     11.00 |                                     0.00 |                                             0.00 |                        1.00 |                                    0.00 |
| PostgreSQL-2-2-2-1 |                     11.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    1.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
