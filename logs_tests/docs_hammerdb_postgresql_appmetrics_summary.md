## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1722s 
* Code: 1792323545
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:824366
  * volume_size:1.8T
  * volume_used:806G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792323545
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:839114
  * volume_size:1.8T
  * volume_used:820G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792323545

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792323545-74774b4bf7-bw298: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       63.00 |           4.00 |            0.00 |         49.00 |           10.00 |              1 |          16 |             | None           |             0 | False         |              914.29 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 246600 | 567759 |         0.00 |          5 |        0 |       2.07 |       2.58 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        8 |        2 |               1 |       1 |  61219 | 140745 |         0.00 |          5 |        0 |       1.59 |       1.94 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        8 |        2 |               1 |       2 |  61184 | 140813 |         0.00 |          5 |        0 |       1.60 |       1.96 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |       16 |        1 |               1 |           1 |       2.07 |       2.58 |         0.00 | 246600.00 | 567759.00 |          5 |        0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |       16 |        2 |               1 |           2 |       1.60 |       1.96 |         0.00 |  61201.50 | 140779.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        40.23 |      0.97 |           1.73 |                  2.40 |
| postgresql-1-1-2-1 |        40.23 |      0.97 |           1.73 |                  2.40 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       184.76 |      0.00 |           0.15 |                  0.15 |
| postgresql-1-1-2-1 |       184.76 |      0.00 |           0.15 |                  0.15 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      2568.39 |      8.22 |           5.57 |                 10.39 |
| postgresql-1-1-2-1 |      5898.68 |     14.42 |           6.68 |                 12.41 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       598.93 |      1.62 |           0.35 |                  0.35 |
| postgresql-1-1-2-1 |       598.93 |      1.29 |           0.35 |                  0.35 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Index Scan Count [scans] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Autoanalyze Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Autovacuum Run Count for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarking.log)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                   18 |                                                   0 |                                                           0 |                                     15 |                                                  1 |
| postgresql-1-1-2-1 |                                   18 |                                                   0 |                                                           0 |                                     15 |                                                  1 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                 9.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                 7.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
