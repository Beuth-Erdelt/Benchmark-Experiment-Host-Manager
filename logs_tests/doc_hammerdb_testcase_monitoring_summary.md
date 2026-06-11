## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1230s 
* Code: 1780840273
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.9.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:205427
  * cpu_list:0-127
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780840273
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:208821
  * cpu_list:0-127
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780840273

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      117.00 |           1.00 |            0.00 |         44.00 |           72.00 |              1 |          16 |          | None           |             0 | False         |              492.31 |

### Execution

#### Per Connection

| DBMS                     |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:-------------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| PostgreSQL-1-1-1-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 228975 | 527627 |         0.00 |          5 |        0 |       2.53 |       5.15 |
| PostgreSQL-1-1-2-1-2-1-1 |                1 |        8 |        2 |               1 |       1 | 209668 | 481435 |         0.00 |          5 |        0 |       3.06 |      12.66 |
| PostgreSQL-1-1-2-1-2-1-1 |                1 |        8 |        2 |               1 |       1 | 209664 | 481688 |         0.00 |          5 |        0 |       3.04 |      12.61 |

#### Per Phase

| DBMS               |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-------------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| PostgreSQL-1-1-1-1 |             1.00 |    16.00 |     1.00 |            1.00 |        1.00 |       2.53 |       5.15 |         0.00 | 228975.00 | 527627.00 |       5.00 |     0.00 |
| PostgreSQL-1-1-2-1 |             1.00 |    16.00 |     2.00 |            1.00 |        2.00 |       3.06 |      12.66 |         0.00 | 209666.00 | 481561.50 |       5.00 |     0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        81.92 |      2.13 |           0.28 |                  2.87 |
| PostgreSQL-1-1-2-1 |        81.92 |      2.13 |           0.28 |                  2.87 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       145.37 |      0.00 |           0.15 |                  0.15 |
| PostgreSQL-1-1-2-1 |       145.37 |      0.00 |           0.15 |                  0.15 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3788.82 |      9.94 |           0.58 |                  6.30 |
| PostgreSQL-1-1-2-1 |      3828.76 |     10.14 |           0.63 |                  9.07 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-2-1 |       572.44 |      2.79 |           1.30 |                  1.30 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
