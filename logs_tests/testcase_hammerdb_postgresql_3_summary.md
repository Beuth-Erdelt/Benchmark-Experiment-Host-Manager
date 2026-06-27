## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 3463s 
* Code: 1782364015
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:277941
  * volume_size:30G
  * volume_used:4.1G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222745
  * volume_size:30G
  * volume_used:4.1G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:4.1G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:4.1G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:4.8G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:4.8G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-2-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:4.8G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-2-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:4.8G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: hammerdb (4 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: hammerdb (4 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      364.00 |           2.00 |            0.00 |        165.00 |          197.00 |              0 |           8 |             | None           |             0 | False         |              158.24 |
| PostgreSQL-1-2 |                2 |   16 |      364.00 |           2.00 |            0.00 |        165.00 |          197.00 |              0 |           8 |             | None           |             0 | False         |              158.24 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       16 |        1 |               1 |       1 |  13209 | 30504 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |       16 |        2 |               1 |       1 |  15790 | 36578 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |       16 |        2 |               1 |       1 |  15782 | 36339 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |        8 |        3 |               1 |       1 |  11178 | 25963 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |        8 |        3 |               1 |       1 |  11180 | 25823 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |        8 |        4 |               1 |       1 |  13528 | 31357 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |        8 |        4 |               1 |       1 |  13555 | 31424 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |        8 |        4 |               1 |       1 |  13558 | 31395 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |        8 |        4 |               1 |       1 |  13582 | 31502 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |       16 |        1 |               1 |       1 |   8849 | 20432 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |       16 |        2 |               1 |       1 |  13977 | 32490 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |       16 |        2 |               1 |       1 |  13912 | 32276 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-3-1-1 | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 |                2 |        8 |        3 |               1 |       1 |  11789 | 27254 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-3-1-1 | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 |                2 |        8 |        3 |               1 |       1 |  11806 | 27287 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |        8 |        4 |               1 |       1 |  14962 | 34299 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |        8 |        4 |               1 |       1 |  14852 | 33988 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |        8 |        4 |               1 |       1 |  14883 | 34103 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |        8 |        4 |               1 |       1 |  14925 | 34225 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |     NOPM |      TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|---------:|---------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 13209.00 | 30504.00 |          2 |        0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |       32 |        2 |               1 |           2 |         0.00 | 15786.00 | 36458.50 |          2 |        0 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |       16 |        3 |               1 |           2 |         0.00 | 11179.00 | 25893.00 |          2 |        0 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |       32 |        4 |               1 |           4 |         0.00 | 13555.75 | 31419.50 |          2 |        0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |       16 |        1 |               1 |           1 |         0.00 |  8849.00 | 20432.00 |          2 |        0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |       32 |        2 |               1 |           2 |         0.00 | 13944.50 | 32383.00 |          2 |        0 |
| PostgreSQL-1-2-3 | PostgreSQL-1-2-3 |                2 |       16 |        3 |               1 |           2 |         0.00 | 11797.50 | 27270.50 |          2 |        0 |
| PostgreSQL-1-2-4 | PostgreSQL-1-2-4 |                2 |       32 |        4 |               1 |           4 |         0.00 | 14905.50 | 34153.75 |          2 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       165.55 |      0.82 |           1.26 |                  2.95 |
| PostgreSQL-1-1-2-1 |       135.36 |      1.02 |           1.82 |                  3.76 |
| PostgreSQL-1-1-3-1 |       325.31 |      1.74 |           2.19 |                  4.24 |
| PostgreSQL-1-1-4-1 |      1809.44 |     11.38 |           2.74 |                  4.91 |
| PostgreSQL-1-2-1-1 |      2484.00 |      5.72 |           2.15 |                  4.34 |
| PostgreSQL-1-2-2-1 |      2138.16 |     11.27 |           2.27 |                  4.59 |
| PostgreSQL-1-2-3-1 |      1298.34 |      7.16 |           2.18 |                  4.59 |
| PostgreSQL-1-2-4-1 |      2151.17 |     12.22 |           2.72 |                  5.27 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        13.46 |      0.08 |           0.07 |                  0.07 |
| PostgreSQL-1-1-2-1 |        13.82 |      0.20 |           0.07 |                  0.07 |
| PostgreSQL-1-1-3-1 |        21.41 |      0.19 |           0.07 |                  0.07 |
| PostgreSQL-1-1-4-1 |        18.60 |      0.28 |           0.04 |                  0.05 |
| PostgreSQL-1-2-1-1 |         9.53 |      0.05 |           0.07 |                  0.07 |
| PostgreSQL-1-2-2-1 |        13.03 |      0.12 |           0.07 |                  0.07 |
| PostgreSQL-1-2-3-1 |        21.69 |      0.14 |           0.07 |                  0.07 |
| PostgreSQL-1-2-4-1 |        17.99 |      0.24 |           0.04 |                  0.05 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
