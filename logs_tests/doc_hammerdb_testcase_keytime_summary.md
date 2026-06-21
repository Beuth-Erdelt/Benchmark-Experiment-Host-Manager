## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 6887s 
* Code: 1781984894
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 20 minutes. Benchmarking has keying and thinking times activated. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 30Gi.
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
  * disk:214714
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781984894
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214906
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781984894
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214906
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781984894
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:217663
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781984894

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      321.00 |           1.00 |            0.00 |        150.00 |          170.00 |              1 |           8 |             | None           |             0 | False         |              179.44 |
| PostgreSQL-1-2 |                2 |   16 |      321.00 |           1.00 |            0.00 |        150.00 |          170.00 |              1 |           8 |             | None           |             0 | False         |              179.44 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |      160 |        1 |               1 |       1 |    200 |   465 |        97.20 |         20 |        0 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |       80 |        2 |               1 |       1 |    204 |   468 |       198.29 |         20 |        0 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |       80 |        2 |               1 |       1 |    204 |   468 |       198.29 |         20 |        0 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |      160 |        1 |               1 |       1 |    201 |   464 |        97.69 |         20 |        0 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |       80 |        2 |               1 |       1 |    201 |   467 |       195.37 |         20 |        0 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |       80 |        2 |               1 |       1 |    201 |   466 |       195.37 |         20 |        0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |   NOPM |    TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|-------:|-------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |      160 |        1 |               1 |           1 |        97.20 | 200.00 | 465.00 |         20 |        0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |      160 |        2 |               1 |           2 |        99.14 | 204.00 | 468.00 |         20 |        0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |      160 |        1 |               1 |           1 |        97.69 | 201.00 | 464.00 |         20 |        0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |      160 |        2 |               1 |           2 |        97.69 | 201.00 | 466.50 |         20 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        90.29 |      0.64 |           1.67 |                  2.37 |
| PostgreSQL-1-1-2-1 |        90.29 |      0.64 |           1.67 |                  2.37 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       276.71 |      5.80 |           0.08 |                  0.09 |
| PostgreSQL-1-1-2-1 |       276.71 |      5.80 |           0.08 |                  0.09 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        40.44 |      0.06 |           2.74 |                  3.46 |
| PostgreSQL-1-1-2-1 |        39.14 |      0.08 |           2.88 |                  3.62 |
| PostgreSQL-1-2-1-1 |       178.42 |      0.10 |           1.93 |                  3.18 |
| PostgreSQL-1-2-2-1 |        42.98 |      0.09 |           1.80 |                  2.43 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        21.37 |      0.13 |           0.58 |                  0.58 |
| PostgreSQL-1-1-2-1 |        21.37 |      0.19 |           0.58 |                  0.58 |
| PostgreSQL-1-2-1-1 |        20.50 |      0.10 |           0.58 |                  0.58 |
| PostgreSQL-1-2-2-1 |        20.50 |      0.16 |           0.58 |                  0.58 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
