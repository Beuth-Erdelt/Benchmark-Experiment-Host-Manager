## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 3086s 
* Code: 1781352619
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [20]. Benchmarking runs for 5 minutes.
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
  * Benchmarking is tested with [160] threads, split into [4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1022338
  * volume_size:100G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781352619
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1022349
  * volume_size:100G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781352619
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1022362
  * volume_size:100G
  * volume_used:2.9G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781352619
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1022370
  * volume_size:100G
  * volume_used:2.9G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781352619
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[4, 8], [4, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[4, 8], [4, 8]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |     2127.00 |           2.00 |            0.00 |       1039.00 |         1086.00 |              1 |           1 |          |                |             0 | False         |               27.08 |
| PostgreSQL-1-2 |                2 |   16 |     2127.00 |           2.00 |            0.00 |       1039.00 |         1086.00 |              1 |           1 |          |                |             0 | False         |               27.08 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       1 | 300.00 |            0 |                          74.28 |                       73.94 |         0.00 |                                                    2104109.00 |                                             531643.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       2 | 300.00 |            0 |                          74.97 |                       74.55 |         0.00 |                                                    2094214.00 |                                             526638.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       3 | 300.00 |            0 |                          74.08 |                       73.73 |         0.00 |                                                    2055077.00 |                                             532042.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       4 | 300.00 |            0 |                          75.00 |                       74.68 |         0.00 |                                                    2057236.00 |                                             525215.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       1 | 300.00 |            0 |                          34.77 |                       34.63 |         0.00 |                                                    2362856.00 |                                             573852.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       2 | 300.00 |            0 |                          36.91 |                       36.72 |         0.00 |                                                    2146078.00 |                                             540749.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       3 | 300.00 |            1 |                          37.07 |                       36.91 |         0.00 |                                                    2158108.00 |                                             537738.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       4 | 300.00 |            0 |                          34.75 |                       34.58 |         0.00 |                                                    2288798.00 |                                             574238.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       5 | 300.00 |            0 |                          36.56 |                       36.38 |         0.00 |                                                    2179861.00 |                                             545772.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       6 | 300.00 |            0 |                          35.59 |                       35.41 |         0.00 |                                                    2193951.00 |                                             560910.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       7 | 300.00 |            0 |                          36.15 |                       36.01 |         0.00 |                                                    2266309.00 |                                             552171.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       8 | 300.00 |            0 |                          36.70 |                       36.55 |         0.00 |                                                    2281409.00 |                                             544439.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       1 | 300.00 |           40 |                          87.79 |                       85.86 |         0.00 |                                                    1893568.00 |                                             454413.00 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       2 | 300.00 |           40 |                          87.85 |                       85.93 |         0.00 |                                                    1904512.00 |                                             453953.00 |
| PostgreSQL-1-2-1-1-3 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       3 | 300.00 |           40 |                          88.01 |                       86.15 |         0.00 |                                                    1892580.00 |                                             453089.00 |
| PostgreSQL-1-2-1-1-4 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       4 | 300.00 |           41 |                          88.50 |                       86.63 |         0.00 |                                                    1879887.00 |                                             450435.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       1 | 300.00 |            0 |                          35.24 |                       35.06 |         0.00 |                                                    2298567.00 |                                             567015.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       2 | 300.00 |            0 |                          34.83 |                       34.66 |         0.00 |                                                    2276171.00 |                                             571412.00 |
| PostgreSQL-1-2-2-1-3 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       3 | 300.00 |            0 |                          36.35 |                       36.17 |         0.00 |                                                    2275828.00 |                                             548491.00 |
| PostgreSQL-1-2-2-1-4 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       4 | 300.00 |            0 |                          35.42 |                       35.25 |         0.00 |                                                    2345178.00 |                                             562383.00 |
| PostgreSQL-1-2-2-1-5 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       5 | 300.00 |            0 |                          35.67 |                       35.46 |         0.00 |                                                    2219336.00 |                                             558042.00 |
| PostgreSQL-1-2-2-1-6 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       6 | 300.00 |            0 |                          36.15 |                       35.95 |         0.00 |                                                    2218591.00 |                                             552874.00 |
| PostgreSQL-1-2-2-1-7 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       7 | 300.00 |            0 |                          36.09 |                       35.92 |         0.00 |                                                    2161909.00 |                                             551018.00 |
| PostgreSQL-1-2-2-1-8 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       8 | 300.00 |            0 |                          35.67 |                       35.52 |         0.00 |                                                    2168164.00 |                                             558995.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |    20480 |               1 |           4 | 300.00 |            0 |                         298.33 |                      296.89 |         0.00 |                                                    2104109.00 |                                             528884.50 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         160 |    20480 |               1 |           8 | 300.00 |            1 |                         288.50 |                      287.20 |         0.00 |                                                    2362856.00 |                                             553733.62 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |         160 |    20480 |               1 |           4 | 300.00 |          161 |                         352.14 |                      344.57 |         0.00 |                                                    1904512.00 |                                             452972.50 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |         160 |    20480 |               1 |           8 | 300.00 |            0 |                         285.42 |                      283.99 |         0.00 |                                                    2345178.00 |                                             558778.75 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       343.58 |      0.62 |           0.34 |                  2.89 |
| PostgreSQL-1-1-2-1 |       343.58 |      0.62 |           0.34 |                  2.89 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1325.62 |      8.43 |           0.27 |                  0.27 |
| PostgreSQL-1-1-2-1 |      1325.62 |      8.43 |           0.27 |                  0.27 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       157.90 |      0.94 |           0.81 |                  3.58 |
| PostgreSQL-1-1-2-1 |       168.87 |      1.04 |           0.80 |                  3.68 |
| PostgreSQL-1-2-1-1 |       689.98 |      1.07 |           0.78 |                  3.68 |
| PostgreSQL-1-2-2-1 |       165.52 |      0.76 |           0.80 |                  3.84 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       186.20 |      1.21 |           0.32 |                  0.32 |
| PostgreSQL-1-1-2-1 |       165.50 |      3.54 |           0.32 |                  0.32 |
| PostgreSQL-1-2-1-1 |       206.24 |      1.37 |           0.31 |                  0.32 |
| PostgreSQL-1-2-2-1 |       201.72 |      1.58 |           0.31 |                  0.31 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     17.00 |                                     0.00 |                                             0.00 |                       18.00 |                                   16.00 |
| PostgreSQL-1-1-2-1 |                     17.00 |                                     0.00 |                                             0.00 |                       18.00 |                                   16.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                    15.00 |                                             0.00 |                      161.00 |                                  160.00 |
| PostgreSQL-1-1-2-1 |                      1.00 |                                    18.00 |                                             0.00 |                      162.00 |                                  160.00 |
| PostgreSQL-1-2-1-1 |                      1.00 |                                     8.00 |                                             0.00 |                      162.00 |                                  160.00 |
| PostgreSQL-1-2-2-1 |                      1.00 |                                    14.00 |                                             0.00 |                      162.00 |                                  160.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
