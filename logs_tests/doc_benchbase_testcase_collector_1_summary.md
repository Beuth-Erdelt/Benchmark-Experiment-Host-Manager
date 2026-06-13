## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 3018s 
* Code: 1781349568
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.11.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1021447
  * volume_size:100G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781349568
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1021464
  * volume_size:100G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781349568
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1021483
  * volume_size:100G
  * volume_used:2.9G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781349568
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1021496
  * volume_size:100G
  * volume_used:2.9G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781349568
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |     2063.00 |           1.00 |            0.00 |       1002.00 |         1060.00 |              1 |           1 |          |                |             0 | False         |               27.92 |
| PostgreSQL-1-2 |                2 |   16 |     2063.00 |           1.00 |            0.00 |       1002.00 |         1060.00 |              1 |           1 |          |                |             0 | False         |               27.92 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 | 300.00 |            0 |                         341.71 |                      339.94 |         0.00 |                                                    1807954.00 |                                             467031.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 | 300.00 |            0 |                         177.27 |                      176.35 |         0.00 |                                                    1646729.00 |                                             450834.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 | 300.00 |            1 |                         176.76 |                      175.85 |         0.00 |                                                    1653965.00 |                                             452403.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |         160 |    16384 |        1 |               1 |       1 | 300.00 |            2 |                         371.62 |                      369.49 |         0.00 |                                                    1687279.00 |                                             429852.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          80 |     8192 |        2 |               1 |       1 | 300.00 |            1 |                         188.96 |                      187.96 |         0.00 |                                                    1568383.00 |                                             419134.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          80 |     8192 |        2 |               1 |       2 | 300.00 |            0 |                         187.93 |                      186.96 |         0.00 |                                                    1562053.00 |                                             420315.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |    16384 |               1 |           1 | 300.00 |            0 |                         341.71 |                      339.94 |         0.00 |                                                    1807954.00 |                                             467031.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         160 |    16384 |               1 |           2 | 300.00 |            1 |                         354.03 |                      352.20 |         0.00 |                                                    1653965.00 |                                             451618.50 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |         160 |    16384 |               1 |           1 | 300.00 |            2 |                         371.62 |                      369.49 |         0.00 |                                                    1687279.00 |                                             429852.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |         160 |    16384 |               1 |           2 | 300.00 |            1 |                         376.89 |                      374.92 |         0.00 |                                                    1568383.00 |                                             419724.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       282.53 |      0.49 |           0.34 |                  2.90 |
| PostgreSQL-1-1-2-1 |       282.53 |      0.49 |           0.34 |                  2.90 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1452.64 |      9.11 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2-1 |      1452.64 |      9.11 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       159.50 |      0.79 |           0.80 |                  3.57 |
| PostgreSQL-1-1-2-1 |       165.01 |      0.79 |           0.79 |                  3.65 |
| PostgreSQL-1-2-1-1 |       640.07 |      1.01 |           0.79 |                  3.74 |
| PostgreSQL-1-2-2-1 |       204.76 |      0.88 |           0.78 |                  3.82 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       148.76 |      0.99 |           0.68 |                  0.68 |
| PostgreSQL-1-1-2-1 |       148.76 |      1.32 |           0.68 |                  0.68 |
| PostgreSQL-1-2-1-1 |       164.03 |      0.83 |           0.66 |                  0.66 |
| PostgreSQL-1-2-2-1 |       164.03 |      1.22 |           0.66 |                  0.66 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       18.00 |                                   16.00 |
| PostgreSQL-1-1-2-1 |                     16.00 |                                     0.00 |                                             0.00 |                       18.00 |                                   16.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     12.00 |                                    15.00 |                                             0.00 |                      163.00 |                                  160.00 |
| PostgreSQL-1-1-2-1 |                      4.00 |                                    11.00 |                                             0.00 |                      161.00 |                                  160.00 |
| PostgreSQL-1-2-1-1 |                      1.00 |                                    42.00 |                                             0.00 |                      161.00 |                                  160.00 |
| PostgreSQL-1-2-2-1 |                     12.00 |                                    14.00 |                                             0.00 |                      161.00 |                                  160.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
