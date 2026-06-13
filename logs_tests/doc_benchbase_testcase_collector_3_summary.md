## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2339s 
* Code: 1781342386
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
  * disk:926335
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781342386
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:928629
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781342386
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:926344
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781342386
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:928926
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781342386
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
| PostgreSQL-1-1 |                1 |   16 |      243.00 |           0.00 |            0.00 |        104.00 |          139.00 |              1 |           1 |          |                |             0 | False         |              237.04 |
| PostgreSQL-1-2 |                2 |   16 |      372.00 |           1.00 |            0.00 |        167.00 |          204.00 |              1 |           1 |          |                |             0 | False         |              154.84 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       1 | 300.00 |            3 |                        1890.44 |                     1865.66 |         0.00 |                                                      66950.00 |                                              21149.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       2 | 300.00 |            5 |                        1883.74 |                     1858.98 |         0.00 |                                                      67074.00 |                                              21225.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       3 | 300.00 |           11 |                        1883.81 |                     1858.67 |         0.00 |                                                      67870.00 |                                              21225.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     5120 |        1 |               1 |       4 | 300.00 |            6 |                        1887.42 |                     1862.05 |         0.00 |                                                      67103.00 |                                              21184.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       1 | 300.00 |            6 |                         888.57 |                      875.15 |         0.00 |                                                      74547.00 |                                              22497.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       2 | 300.00 |            4 |                         881.40 |                      868.45 |         0.00 |                                                      76064.00 |                                              22680.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       3 | 300.00 |            8 |                         907.31 |                      893.50 |         0.00 |                                                      72929.00 |                                              22028.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       4 | 300.00 |            5 |                         913.78 |                      899.95 |         0.00 |                                                      71772.00 |                                              21877.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       5 | 300.00 |            5 |                         901.45 |                      887.65 |         0.00 |                                                      73327.00 |                                              22161.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       6 | 300.00 |            3 |                         903.34 |                      889.60 |         0.00 |                                                      73457.00 |                                              22130.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       7 | 300.00 |            1 |                         908.14 |                      894.45 |         0.00 |                                                      73281.00 |                                              22012.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          20 |     2560 |        2 |               1 |       8 | 300.00 |            4 |                         900.25 |                      886.90 |         0.00 |                                                      73243.00 |                                              22201.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       1 | 300.00 |            8 |                        1954.92 |                     1929.06 |         0.00 |                                                      65244.00 |                                              20453.00 |
| PostgreSQL-1-2-1-1-2 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       2 | 300.00 |            5 |                        1956.59 |                     1930.63 |         0.00 |                                                      64612.00 |                                              20426.00 |
| PostgreSQL-1-2-1-1-3 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       3 | 300.00 |            7 |                        1957.44 |                     1931.09 |         0.00 |                                                      64993.00 |                                              20426.00 |
| PostgreSQL-1-2-1-1-4 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     5120 |        1 |               1 |       4 | 300.00 |           11 |                        1928.32 |                     1902.52 |         0.00 |                                                      66180.00 |                                              20735.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       1 | 300.00 |            2 |                         910.54 |                      897.07 |         0.00 |                                                      74696.00 |                                              21955.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       2 | 300.00 |            1 |                         887.43 |                      874.15 |         0.00 |                                                      76786.00 |                                              22522.00 |
| PostgreSQL-1-2-2-1-3 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       3 | 300.00 |            1 |                         908.42 |                      894.92 |         0.00 |                                                      73997.00 |                                              22004.00 |
| PostgreSQL-1-2-2-1-4 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       4 | 300.00 |            7 |                         888.95 |                      875.63 |         0.00 |                                                      75877.00 |                                              22488.00 |
| PostgreSQL-1-2-2-1-5 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       5 | 300.00 |            3 |                         885.62 |                      872.74 |         0.00 |                                                      77545.00 |                                              22570.00 |
| PostgreSQL-1-2-2-1-6 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       6 | 300.00 |            0 |                         894.56 |                      881.28 |         0.00 |                                                      74908.00 |                                              22347.00 |
| PostgreSQL-1-2-2-1-7 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       7 | 300.00 |            6 |                         901.24 |                      887.65 |         0.00 |                                                      74916.00 |                                              22176.00 |
| PostgreSQL-1-2-2-1-8 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |          20 |     2560 |        2 |               1 |       8 | 300.00 |            6 |                         895.68 |                      882.15 |         0.00 |                                                      74472.00 |                                              22318.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |    20480 |               1 |           4 | 300.00 |           25 |                        7545.41 |                     7445.36 |         0.00 |                                                      67870.00 |                                              21195.75 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         160 |    20480 |               1 |           8 | 300.00 |           36 |                        7204.24 |                     7095.64 |         0.00 |                                                      76064.00 |                                              22198.25 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |         160 |    20480 |               1 |           4 | 300.00 |           31 |                        7797.27 |                     7693.30 |         0.00 |                                                      66180.00 |                                              20510.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |         160 |    20480 |               1 |           8 | 300.00 |           26 |                        7172.43 |                     7065.58 |         0.00 |                                                      77545.00 |                                              22297.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       207.30 |      3.25 |           0.36 |                  2.88 |
| PostgreSQL-1-1-2-1 |       207.30 |      3.25 |           0.36 |                  2.88 |
| PostgreSQL-1-2-1-1 |      6722.71 |      6.31 |           0.40 |                  7.11 |
| PostgreSQL-1-2-2-1 |      6722.71 |      6.31 |           0.40 |                  7.11 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1021.01 |     14.39 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2-1 |      1021.01 |     14.39 |           0.25 |                  0.25 |
| PostgreSQL-1-2-1-1 |      1925.89 |     15.59 |           0.25 |                  0.25 |
| PostgreSQL-1-2-2-1 |      1925.89 |     15.59 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3249.86 |     11.92 |           0.96 |                  5.81 |
| PostgreSQL-1-1-2-1 |      2929.25 |     11.23 |           1.01 |                  7.63 |
| PostgreSQL-1-2-1-1 |      3045.64 |     12.81 |           0.98 |                  6.01 |
| PostgreSQL-1-2-2-1 |      2998.01 |     10.46 |           1.01 |                  7.99 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3686.51 |     13.50 |           0.43 |                  0.43 |
| PostgreSQL-1-1-2-1 |      3491.13 |     27.89 |           0.43 |                  0.43 |
| PostgreSQL-1-2-1-1 |      3543.14 |     14.07 |           0.41 |                  0.41 |
| PostgreSQL-1-2-2-1 |      3255.51 |     26.73 |           0.41 |                  0.41 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       12.00 |                                   11.00 |
| PostgreSQL-1-1-2-1 |                     16.00 |                                     0.00 |                                             0.00 |                       12.00 |                                   11.00 |
| PostgreSQL-1-2-1-1 |                     17.00 |                                     0.00 |                                             0.00 |                       13.00 |                                   12.00 |
| PostgreSQL-1-2-2-1 |                     17.00 |                                     0.00 |                                             0.00 |                       13.00 |                                   12.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     15.00 |                                    49.00 |                                             0.00 |                      162.00 |                                  160.00 |
| PostgreSQL-1-1-2-1 |                     18.00 |                                    59.00 |                                             0.00 |                      162.00 |                                  160.00 |
| PostgreSQL-1-2-1-1 |                     19.00 |                                    50.00 |                                             0.00 |                      162.00 |                                  160.00 |
| PostgreSQL-1-2-2-1 |                      6.00 |                                    46.00 |                                             0.00 |                      162.00 |                                  160.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
