## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 2511s 
* Code: 1795435533
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run 2 times.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:540492869632
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker38
  * disk:498211
  * datadisk:330
  * volume_size:49G
  * volume_used:330M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795435533
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:540492869632
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker38
  * disk:498212
  * datadisk:331
  * volume_size:49G
  * volume_used:331M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795435533
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:540492869632
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker38
  * disk:498212
  * datadisk:331
  * volume_size:49G
  * volume_used:331M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795435533
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:540492869632
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker38
  * disk:498214
  * datadisk:332
  * volume_size:49G
  * volume_used:332M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795435533
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-2-1-1-1 uses docker image postgres:18.6
  * RAM:540492869632
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker38
  * disk:498211
  * datadisk:330
  * volume_size:49G
  * volume_used:330M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795435533
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* postgresql-2-1-2-1 uses docker image postgres:18.6
  * RAM:540492869632
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker38
  * disk:498212
  * datadisk:331
  * volume_size:49G
  * volume_used:331M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795435533
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* postgresql-2-2-1-1 uses docker image postgres:18.6
  * RAM:540492869632
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker38
  * disk:498212
  * datadisk:331
  * volume_size:49G
  * volume_used:331M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795435533
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* postgresql-2-2-2-1 uses docker image postgres:18.6
  * RAM:540492869632
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker38
  * disk:498214
  * datadisk:332
  * volume_size:49G
  * volume_used:332M
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795435533
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2, PostgreSQL-2-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks
* PostgreSQL-2: loading values of the volume: script=Schema, indexing=Checks

### Ingestion
* PostgreSQL-1: 1 of 1 units ok
* PostgreSQL-2: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795435533-7fb65544d4-jz54h: 0
* bexhoma-sut-postgresql-1-1795435533-5d696b95c5-fs9vs: 0
* bexhoma-sut-postgresql-2-1795435533-6867f4554b-thbx8: 0
* bexhoma-sut-postgresql-2-1795435533-7b7b566d47-cj2bn: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 2: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-2 - Experiment 2 Client 2: benchbase (1 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|--------------------:|:--------------------|
| 1795435533-PostgreSQL-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |       38.00 |           3.00 |            0.00 |         30.00 |            5.00 |              1 |         1 |               94.74 | False               |
| 1795435533-PostgreSQL-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |       36.00 |           3.00 |            0.00 |         28.00 |            5.00 |              1 |         1 |              100.00 | False               |
| 1795435533-PostgreSQL-1-2-0 |                2 | container      | False         |             2 |           0 |    1 |       38.00 |           3.00 |            0.00 |         30.00 |            5.00 |              1 |         1 |               94.74 | True                |
| 1795435533-PostgreSQL-2-2-1 |                2 | container      | False         |             2 |           1 |    1 |       36.00 |           3.00 |            0.00 |         28.00 |            5.00 |              1 |         1 |              100.00 | True                |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.52 |                        0.52 |       109.18 |                                                      41751.00 |                                              14564.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.51 |                        0.51 |       107.08 |                                                      43198.00 |                                              15957.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |       1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.45 |                        0.45 |        95.18 |                                                      99755.00 |                                              38925.00 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        2 |               1 |       1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.46 |                        0.47 |        97.98 |                                                      42919.00 |                                              18941.00 |
| postgresql-2-1-1-1-1 | postgresql-2-1-1 | postgresql-2-1-1-1 |                1 |        1 |               1 |       1 |        10 |     1024 |           1 | 300.00 |        0 |                           0.50 |                        0.49 |       102.18 |                                                      35385.00 |                                              15266.00 |
| postgresql-2-1-2-1-1 | postgresql-2-1-2 | postgresql-2-1-2-1 |                1 |        2 |               1 |       1 |        10 |     1024 |           1 | 300.00 |        0 |                           0.47 |                        0.47 |        97.98 |                                                      32377.00 |                                              16105.00 |
| postgresql-2-2-1-1-1 | postgresql-2-2-1 | postgresql-2-2-1-1 |                2 |        1 |               1 |       1 |        10 |     1024 |           1 | 300.00 |        0 |                           0.46 |                        0.46 |        97.28 |                                                      88661.00 |                                              35935.00 |
| postgresql-2-2-2-1-1 | postgresql-2-2-2 | postgresql-2-2-2-1 |                2 |        2 |               1 |       1 |        10 |     1024 |           1 | 300.00 |        0 |                           0.47 |                        0.47 |        98.68 |                                                      41949.00 |                                              19225.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-0 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.52 |                        0.52 |       109.18 |                                                      41751.00 |                                              14564.00 |
| postgresql-1-1-2-0 | postgresql-1-1-2 |                1 |        2 |               1 |           1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.51 |                        0.51 |       107.08 |                                                      43198.00 |                                              15957.00 |
| postgresql-1-2-1-0 | postgresql-1-2-1 |                2 |        1 |               1 |           1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.45 |                        0.45 |        95.18 |                                                      99755.00 |                                              38925.00 |
| postgresql-1-2-2-0 | postgresql-1-2-2 |                2 |        2 |               1 |           1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.46 |                        0.47 |        97.98 |                                                      42919.00 |                                              18941.00 |
| postgresql-2-1-1-1 | postgresql-2-1-1 |                1 |        1 |               1 |           1 |        10 |     1024 |           1 | 300.00 |        0 |                           0.50 |                        0.49 |       102.18 |                                                      35385.00 |                                              15266.00 |
| postgresql-2-1-2-1 | postgresql-2-1-2 |                1 |        2 |               1 |           1 |        10 |     1024 |           1 | 300.00 |        0 |                           0.47 |                        0.47 |        97.98 |                                                      32377.00 |                                              16105.00 |
| postgresql-2-2-1-1 | postgresql-2-2-1 |                2 |        1 |               1 |           1 |        10 |     1024 |           1 | 300.00 |        0 |                           0.46 |                        0.46 |        97.28 |                                                      88661.00 |                                              35935.00 |
| postgresql-2-2-2-1 | postgresql-2-2-2 |                2 |        2 |               1 |           1 |        10 |     1024 |           1 | 300.00 |        0 |                           0.47 |                        0.47 |        98.68 |                                                      41949.00 |                                              19225.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        24.94 |      0.69 |           0.51 |                  0.66 |
| postgresql-1-1-2-1 |        24.94 |      0.69 |           0.51 |                  0.66 |
| postgresql-2-1-1-1 |        11.78 |      0.40 |           0.49 |                  0.61 |
| postgresql-2-1-2-1 |        11.78 |      0.40 |           0.49 |                  0.61 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-2-1-1-1 | n/a          |      0.00 |           0.25 |                  0.25 |
| postgresql-2-1-2-1 | n/a          |      0.00 |           0.25 |                  0.25 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         3.85 |      0.03 |           0.54 |                  0.67 |
| postgresql-1-1-2-1 |         3.31 |      0.02 |           0.54 |                  0.68 |
| postgresql-1-2-1-1 |         4.69 |      0.04 |           0.43 |                  0.47 |
| postgresql-1-2-2-1 |         3.26 |      0.02 |           0.44 |                  0.48 |
| postgresql-2-1-1-1 |         3.81 |      0.03 |           0.54 |                  0.68 |
| postgresql-2-1-2-1 |         3.29 |      0.02 |           0.54 |                  0.68 |
| postgresql-2-2-1-1 |         4.17 |      0.04 |           0.43 |                  0.46 |
| postgresql-2-2-2-1 |         3.49 |      0.02 |           0.44 |                  0.48 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |         9.33 |      0.03 |           0.10 |                  0.10 |
| postgresql-1-1-2-1 |        27.67 |      0.62 |           0.11 |                  0.11 |
| postgresql-1-2-1-1 |        65.16 |      1.01 |           0.29 |                  0.29 |
| postgresql-1-2-2-1 |        22.27 |      0.37 |           0.27 |                  0.27 |
| postgresql-2-1-1-1 |        25.14 |      0.62 |           0.11 |                  0.11 |
| postgresql-2-1-2-1 |         9.52 |      0.24 |           0.11 |                  0.11 |
| postgresql-2-2-1-1 |        44.66 |      1.02 |           0.28 |                  0.28 |
| postgresql-2-2-2-1 |        15.17 |      0.24 |           0.28 |                  0.28 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-1-1 (bexhoma-metrics-postgresql-2-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-1-2-1 (bexhoma-metrics-postgresql-2-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-2-1-1 (bexhoma-metrics-postgresql-2-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on I/O [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on WAL [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (I/O Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Max Transaction Duration (WAL Wait) [s] for connection postgresql-2-2-2-1 (bexhoma-metrics-postgresql-2-2-2-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-1-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-1-1-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |
| postgresql-2-1-2-1 |                                 1.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-2-1-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-1-2-2-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   1.00 |                                               0.00 |
| postgresql-2-1-1-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-2-1-2-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-2-2-1-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |
| postgresql-2-2-2-1 |                                11.00 |                                                0.00 |                                                        0.00 |                                   0.00 |                                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: efficiency contains no 0 or NaN
* TEST passed: Workflow as planned
