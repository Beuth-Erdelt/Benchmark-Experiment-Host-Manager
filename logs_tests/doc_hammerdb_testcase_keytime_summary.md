## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 6718s 
* Code: 1780843293
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 20 minutes. Benchmarking has keying and thinking times activated. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.9.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:202795
  * volume_size:30G
  * volume_used:2.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780843293
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:202795
  * volume_size:30G
  * volume_used:2.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780843293
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:202795
  * volume_size:30G
  * volume_used:2.2G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780843293
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:202795
  * volume_size:30G
  * volume_used:2.2G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780843293

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2], [1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      432.00 |           1.00 |            0.00 |        195.00 |          236.00 |              1 |           8 |          | None           |             0 | False         |              133.33 |
| PostgreSQL-1-2 |                2 |   16 |      432.00 |           1.00 |            0.00 |        195.00 |          236.00 |              1 |           8 |          | None           |             0 | False         |              133.33 |

### Execution

#### Per Connection

| DBMS                     |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:-------------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1-1-1 |                1 |      160 |        1 |               1 |       1 |    196 |   477 |        95.26 |         20 |        0 |
| PostgreSQL-1-1-2-1-2-1-1 |                1 |       80 |        2 |               1 |       1 |    201 |   485 |       195.37 |         20 |        0 |
| PostgreSQL-1-1-2-1-2-1-1 |                1 |       80 |        2 |               1 |       1 |    201 |   485 |       195.37 |         20 |        0 |
| PostgreSQL-1-2-1-1-1-1-1 |                2 |      160 |        1 |               1 |       1 |    201 |   477 |        97.69 |         20 |        0 |
| PostgreSQL-1-2-2-1-2-1-1 |                2 |       80 |        2 |               1 |       1 |    199 |   475 |       193.43 |         20 |        0 |
| PostgreSQL-1-2-2-1-2-1-1 |                2 |       80 |        2 |               1 |       1 |    199 |   475 |       193.43 |         20 |        0 |

#### Per Phase

| DBMS               |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |   NOPM |    TPM |   duration |   errors |
|:-------------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|-------:|-------:|-----------:|---------:|
| PostgreSQL-1-1-1-1 |             1.00 |   160.00 |     1.00 |            1.00 |        1.00 |        95.26 | 196.00 | 477.00 |      20.00 |     0.00 |
| PostgreSQL-1-1-2-1 |             1.00 |   160.00 |     2.00 |            1.00 |        2.00 |        97.69 | 201.00 | 485.00 |      20.00 |     0.00 |
| PostgreSQL-1-2-1-1 |             2.00 |   160.00 |     1.00 |            1.00 |        1.00 |        97.69 | 201.00 | 477.00 |      20.00 |     0.00 |
| PostgreSQL-1-2-2-1 |             2.00 |   160.00 |     2.00 |            1.00 |        2.00 |        96.71 | 199.00 | 475.00 |      20.00 |     0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       112.56 |      0.74 |           0.22 |                  2.78 |
| PostgreSQL-1-1-2-1 |       112.56 |      0.74 |           0.22 |                  2.78 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       250.22 |      4.29 |           0.09 |                  0.09 |
| PostgreSQL-1-1-2-1 |       250.22 |      4.29 |           0.09 |                  0.09 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        47.78 |      0.07 |           0.92 |                  3.48 |
| PostgreSQL-1-1-2-1 |        50.27 |      0.08 |           0.93 |                  3.17 |
| PostgreSQL-1-2-1-1 |       214.74 |      0.07 |           0.92 |                  2.86 |
| PostgreSQL-1-2-2-1 |        48.85 |      0.11 |           0.92 |                  2.83 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-2-1 |        22.00 |      0.16 |           0.58 |                  0.58 |
| PostgreSQL-1-2-2-1 |        22.42 |      0.13 |           0.58 |                  0.58 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
