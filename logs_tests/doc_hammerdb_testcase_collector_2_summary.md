## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2866s 
* Code: 1781299113
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
  * Database is persisted to disk of type shared and size 15Gi. Persistent storage is removed at experiment start.
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
  * disk:921716
  * volume_size:15G
  * volume_used:2.6G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781299113
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921717
  * volume_size:15G
  * volume_used:2.6G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781299113
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921719
  * volume_size:15G
  * volume_used:2.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781299113
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921721
  * volume_size:15G
  * volume_used:2.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781299113

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      382.00 |           2.00 |            0.00 |        179.00 |          201.00 |              1 |          16 |          | None           |             0 | False         |              150.79 |
| PostgreSQL-1-2 |                2 |   16 |      382.00 |           2.00 |            0.00 |        179.00 |          201.00 |              1 |          16 |          | None           |             0 | False         |              150.79 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |   TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|------:|-------------:|-----------:|---------:|-----------:|-----------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       32 |        1 |               1 |       1 |   4380 | 10285 |         0.00 |          5 |        0 |     291.74 |     871.80 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |       16 |        2 |               1 |       1 |   5529 | 13002 |         0.00 |          5 |        0 |     338.26 |     819.36 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |       16 |        2 |               1 |       1 |   5544 | 13013 |         0.00 |          5 |        0 |     342.31 |     825.05 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |       32 |        1 |               1 |       1 |   4240 |  9932 |         0.00 |          5 |        0 |     312.21 |     858.04 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |       16 |        2 |               1 |       1 |   4536 | 10682 |         0.00 |          5 |        0 |     375.61 |    1070.33 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |       16 |        2 |               1 |       1 |   4536 | 10682 |         0.00 |          5 |        0 |     351.47 |    1077.57 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |    NOPM |      TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|--------:|---------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       32 |        1 |               1 |           1 |     291.74 |     871.80 |         0.00 | 4380.00 | 10285.00 |          5 |        0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |       32 |        2 |               1 |           2 |     342.31 |     825.05 |         0.00 | 5536.50 | 13007.50 |          5 |        0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |       32 |        1 |               1 |           1 |     312.21 |     858.04 |         0.00 | 4240.00 |  9932.00 |          5 |        0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |       32 |        2 |               1 |           2 |     375.61 |    1077.57 |         0.00 | 4536.00 | 10682.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        45.45 |      0.29 |           0.26 |                  2.78 |
| PostgreSQL-1-1-2-1 |        45.45 |      0.29 |           0.26 |                  2.78 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       282.81 |      5.19 |           0.16 |                  0.16 |
| PostgreSQL-1-1-2-1 |       282.81 |      5.19 |           0.16 |                  0.16 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        56.81 |      0.19 |           0.37 |                  3.03 |
| PostgreSQL-1-1-2-1 |        74.39 |      0.24 |           0.38 |                  3.13 |
| PostgreSQL-1-2-1-1 |       178.26 |      0.20 |           0.38 |                  3.14 |
| PostgreSQL-1-2-2-1 |        67.40 |      0.26 |           0.39 |                  3.25 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        14.74 |      0.07 |           0.15 |                  0.15 |
| PostgreSQL-1-1-2-1 |        14.74 |      0.08 |           0.15 |                  0.15 |
| PostgreSQL-1-2-1-1 |        19.25 |      0.08 |           0.15 |                  0.15 |
| PostgreSQL-1-2-2-1 |        14.91 |      0.13 |           0.15 |                  0.15 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       19.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                     16.00 |                                     0.00 |                                             0.00 |                       19.00 |                                    0.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      2.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                      5.00 |                                     0.00 |                                             0.00 |                       34.00 |                                    0.00 |
| PostgreSQL-1-2-1-1 |                      2.00 |                                     0.00 |                                             0.00 |                       33.00 |                                    0.00 |
| PostgreSQL-1-2-2-1 |                     13.00 |                                     0.00 |                                             0.00 |                       35.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
