## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2842s 
* Code: 1781296243
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
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921706
  * volume_size:15G
  * volume_used:2.6G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781296243
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921708
  * volume_size:15G
  * volume_used:2.6G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781296243
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921710
  * volume_size:15G
  * volume_used:2.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781296243
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:921712
  * volume_size:15G
  * volume_used:2.8G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781296243

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      362.00 |           1.00 |            0.00 |        160.00 |          201.00 |              1 |          16 |          | None           |             0 | False         |              159.12 |
| PostgreSQL-1-2 |                2 |   16 |      362.00 |           1.00 |            0.00 |        160.00 |          201.00 |              1 |          16 |          | None           |             0 | False         |              159.12 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |   TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|------:|-------------:|-----------:|---------:|-----------:|-----------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       16 |        1 |               1 |       1 |   4139 |  9563 |         0.00 |          5 |        0 |     280.83 |     729.04 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        8 |        2 |               1 |       1 |   3410 |  7937 |         0.00 |          5 |        0 |     261.15 |    1384.66 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        8 |        2 |               1 |       1 |   3410 |  7937 |         0.00 |          5 |        1 |       0.00 |       0.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |       16 |        1 |               1 |       1 |   3172 |  7456 |         0.00 |          5 |        0 |     324.81 |    1886.90 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        8 |        2 |               1 |       1 |   5333 | 12544 |         0.00 |          5 |        0 |       0.00 |       0.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        8 |        2 |               1 |       1 |   5331 | 12500 |         0.00 |          5 |        0 |       0.00 |       0.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |    NOPM |      TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|--------:|---------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       16 |        1 |               1 |           1 |     280.83 |     729.04 |         0.00 | 4139.00 |  9563.00 |          5 |        0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |       16 |        2 |               1 |           2 |     261.15 |    1384.66 |         0.00 | 3410.00 |  7937.00 |          5 |        1 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |       16 |        1 |               1 |           1 |     324.80 |    1886.90 |         0.00 | 3172.00 |  7456.00 |          5 |        0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |       16 |        2 |               1 |           2 |       0.00 |       0.00 |         0.00 | 5332.00 | 12522.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        46.45 |      0.36 |           0.22 |                  2.78 |
| PostgreSQL-1-1-2-1 |        46.45 |      0.36 |           0.22 |                  2.78 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       310.83 |      2.73 |           0.16 |                  0.16 |
| PostgreSQL-1-1-2-1 |       310.83 |      2.73 |           0.16 |                  0.16 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        46.01 |      0.18 |           0.28 |                  2.92 |
| PostgreSQL-1-1-2-1 |        46.34 |      0.20 |           0.28 |                  2.99 |
| PostgreSQL-1-2-1-1 |       144.85 |      0.14 |           0.27 |                  2.90 |
| PostgreSQL-1-2-2-1 |        60.09 |      0.16 |           0.30 |                  3.10 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        15.60 |      0.07 |           0.10 |                  0.10 |
| PostgreSQL-1-1-2-1 |        15.21 |      0.12 |           0.10 |                  0.10 |
| PostgreSQL-1-2-1-1 |         9.95 |      0.04 |           0.09 |                  0.09 |
| PostgreSQL-1-2-2-1 |        10.60 |      0.06 |           0.09 |                  0.09 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     18.00 |                                     0.00 |                                             0.00 |                       19.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                     18.00 |                                     0.00 |                                             0.00 |                       19.00 |                                    0.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      4.00 |                                     0.00 |                                             0.00 |                       18.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                      3.00 |                                     0.00 |                                             0.00 |                       18.00 |                                    0.00 |
| PostgreSQL-1-2-1-1 |                      3.00 |                                     0.00 |                                             0.00 |                       17.00 |                                    0.00 |
| PostgreSQL-1-2-2-1 |                      7.00 |                                     0.00 |                                             0.00 |                       18.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
