## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 611s 
* Code: 1782305705
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [64] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220793
  * datadisk:330
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782305705
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (8 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (8 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |       60.00 |           0.00 |            0.00 |         24.00 |           36.00 |              1 |           1 |             |                |             0 | False         |               60.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       1 |           0 | 300.00 |            0 |                          52.83 |                       52.35 |         0.00 |                                                     755417.00 |                                             151346.00 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       2 |           0 | 300.00 |            0 |                          53.23 |                       52.70 |         0.00 |                                                     755040.00 |                                             150160.00 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       3 |           0 | 300.00 |            0 |                          50.55 |                       50.09 |         0.00 |                                                     784752.00 |                                             157853.00 |
| PostgreSQL-1-1-1-1-4 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       4 |           0 | 300.00 |            0 |                          52.24 |                       51.75 |         0.00 |                                                     760276.00 |                                             153034.00 |
| PostgreSQL-1-1-1-1-5 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       5 |           0 | 300.00 |            2 |                          51.42 |                       51.00 |         0.00 |                                                     768047.00 |                                             155439.00 |
| PostgreSQL-1-1-1-1-6 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       6 |           0 | 300.00 |            1 |                          51.52 |                       51.08 |         0.00 |                                                     780820.00 |                                             154906.00 |
| PostgreSQL-1-1-1-1-7 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       7 |           0 | 300.00 |            0 |                          51.63 |                       51.27 |         0.00 |                                                     774322.00 |                                             154791.00 |
| PostgreSQL-1-1-1-1-8 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |           8 |      128 |        1 |               1 |       8 |           0 | 300.00 |            0 |                          52.21 |                       51.68 |         0.00 |                                                     769977.00 |                                             152923.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |          64 |     1024 |               1 |           8 |           0 | 300.00 |            3 |                         415.62 |                      411.92 |         0.00 |                                                     784752.00 |                                             153806.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        19.28 |      0.85 |           0.51 |                  0.66 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         7.32 |      0.00 |           0.24 |                  0.24 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       712.35 |      2.66 |           0.90 |                  1.18 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       196.11 |      1.73 |           0.23 |                  0.23 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
