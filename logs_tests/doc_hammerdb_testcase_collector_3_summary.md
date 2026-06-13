## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2620s 
* Code: 1781302011
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.9.11.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [32] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:924272
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781302011
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:927400
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781302011
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:924287
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781302011
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:927341
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781302011

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      116.00 |           1.00 |            0.00 |         44.00 |           71.00 |              1 |          16 |          | None           |             0 | False         |              496.55 |
| PostgreSQL-1-2 |                2 |   16 |      115.00 |           0.00 |            0.00 |         44.00 |           71.00 |              1 |          16 |          | None           |             0 | False         |              500.87 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       32 |        1 |               1 |       1 | 215005 | 495183 |         0.00 |          5 |        0 |       3.35 |      16.39 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |       16 |        2 |               1 |       1 | 203050 | 466413 |         0.00 |          5 |        0 |       4.79 |      25.43 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |       16 |        2 |               1 |       1 | 202991 | 467694 |         0.00 |          5 |        0 |       4.70 |      24.93 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |       32 |        1 |               1 |       1 | 212934 | 490505 |         0.00 |          5 |        0 |       3.56 |      20.55 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |       16 |        2 |               1 |       1 | 208750 | 481376 |         0.00 |          5 |        0 |       5.07 |      25.58 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |       16 |        2 |               1 |       1 | 209024 | 480427 |         0.00 |          5 |        0 |       4.89 |      25.25 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       32 |        1 |               1 |           1 |       3.34 |      16.39 |         0.00 | 215005.00 | 495183.00 |          5 |        0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |       32 |        2 |               1 |           2 |       4.79 |      25.43 |         0.00 | 203020.50 | 467053.50 |          5 |        0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |       32 |        1 |               1 |           1 |       3.56 |      20.56 |         0.00 | 212934.00 | 490505.00 |          5 |        0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |       32 |        2 |               1 |           2 |       5.07 |      25.58 |         0.00 | 208887.00 | 480901.50 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        36.22 |      0.78 |           0.29 |                  2.82 |
| PostgreSQL-1-1-2-1 |        36.22 |      0.78 |           0.29 |                  2.82 |
| PostgreSQL-1-2-1-1 |        40.66 |      1.40 |           0.45 |                  8.70 |
| PostgreSQL-1-2-2-1 |        40.66 |      1.40 |           0.45 |                  8.70 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       193.90 |      0.00 |           0.15 |                  0.15 |
| PostgreSQL-1-1-2-1 |       193.90 |      0.00 |           0.15 |                  0.15 |
| PostgreSQL-1-2-1-1 |       312.30 |      9.19 |           0.15 |                  0.15 |
| PostgreSQL-1-2-2-1 |       312.30 |      9.19 |           0.15 |                  0.15 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      2624.52 |     10.00 |           0.73 |                  6.35 |
| PostgreSQL-1-1-2-1 |      2395.46 |      7.25 |           0.85 |                  9.05 |
| PostgreSQL-1-2-1-1 |      2664.82 |     12.21 |           0.78 |                  6.12 |
| PostgreSQL-1-2-2-1 |      2568.93 |      6.85 |           0.74 |                  8.79 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       526.42 |      1.49 |           1.28 |                  1.28 |
| PostgreSQL-1-1-2-1 |       526.42 |      2.92 |           1.28 |                  1.28 |
| PostgreSQL-1-2-1-1 |       522.80 |      1.50 |           1.53 |                  1.53 |
| PostgreSQL-1-2-2-1 |       522.80 |      2.95 |           1.53 |                  1.53 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     17.00 |                                     0.00 |                                             0.00 |                       11.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                     17.00 |                                     0.00 |                                             0.00 |                       11.00 |                                    0.00 |
| PostgreSQL-1-2-1-1 |                     17.00 |                                     0.00 |                                             0.00 |                       12.00 |                                    0.00 |
| PostgreSQL-1-2-2-1 |                     17.00 |                                     0.00 |                                             0.00 |                       12.00 |                                    0.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     13.00 |                                     0.00 |                                             0.00 |                       34.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                     11.00 |                                     0.00 |                                             0.00 |                       35.00 |                                    0.00 |
| PostgreSQL-1-2-1-1 |                      8.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |
| PostgreSQL-1-2-2-1 |                     15.00 |                                     0.00 |                                             0.00 |                       34.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
