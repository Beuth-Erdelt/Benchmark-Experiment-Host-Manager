## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2498s 
* Code: 1793594796
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685325
  * datadisk:3304
  * volume_size:49G
  * volume_used:3.3G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793594796
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685327
  * datadisk:12018
  * volume_size:49G
  * volume_used:12G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793594796
* postgresql-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685329
  * datadisk:14874
  * volume_size:49G
  * volume_used:15G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793594796
* postgresql-1-2-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:685330
  * datadisk:15486
  * volume_size:49G
  * volume_used:16G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793594796

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793594796-6f6688df9f-7s8lj: 0
* bexhoma-sut-postgresql-1-1793594796-547c8964d9-nkjjr: 0

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

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   16 |       44.00 |           4.00 |            0.00 |         30.00 |           10.00 |              1 |          16 |             | None           |             0 | False         |             1309.09 | False               |
| PostgreSQL-1-2 |                2 |   16 |       44.00 |           4.00 |            0.00 |         30.00 |           10.00 |              1 |          16 |             | None           |             0 | False         |             1309.09 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 163778 | 377587 |         0.00 |          5 |        0 |       2.96 |       4.01 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        8 |        2 |               1 |       1 |  49241 | 113739 |         0.00 |          5 |        0 |       2.84 |       3.56 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        8 |        2 |               1 |       2 |  49194 | 113605 |         0.00 |          5 |        0 |       2.88 |       3.56 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |       16 |        1 |               1 |       1 |  46610 | 107507 |         0.00 |          5 |        0 |       3.32 |       4.61 |
| postgresql-1-2-2-1-1 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        8 |        2 |               1 |       1 |  43959 | 101172 |         0.00 |          5 |        0 |       3.00 |       3.98 |
| postgresql-1-2-2-1-2 | postgresql-1-2-2 | postgresql-1-2-2-1 |                2 |        8 |        2 |               1 |       2 |  43931 | 101187 |         0.00 |          5 |        0 |       3.01 |       3.84 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |       16 |        1 |               1 |           1 |       2.96 |       4.01 |         0.00 | 163778.00 | 377587.00 |          5 |        0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |       16 |        2 |               1 |           2 |       2.88 |       3.56 |         0.00 |  49217.50 | 113672.00 |          5 |        0 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |       16 |        1 |               1 |           1 |       3.32 |       4.61 |         0.00 |  46610.00 | 107507.00 |          5 |        0 |
| postgresql-1-2-2 | postgresql-1-2-2 |                2 |       16 |        2 |               1 |           2 |       3.01 |       3.98 |         0.00 |  43945.00 | 101179.50 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        30.71 |      0.89 |           1.67 |                  2.39 |
| postgresql-1-1-2-1 |        30.71 |      0.89 |           1.67 |                  2.39 |

### Loading phase: component loader

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.14 |                  0.15 |
| postgresql-1-1-2-1 | n/a          |         0 |           0.14 |                  0.15 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1794.64 |      5.37 |           4.26 |                  7.89 |
| postgresql-1-1-2-1 |      5406.01 |     13.15 |           5.29 |                  9.70 |
| postgresql-1-2-1-1 |      5286.18 |     13.12 |           2.57 |                  4.52 |
| postgresql-1-2-2-1 |      5502.89 |     13.83 |           3.37 |                  6.06 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       733.87 |      1.84 |           0.28 |                  0.28 |
| postgresql-1-1-2-1 |       243.39 |      0.67 |           0.11 |                  0.12 |
| postgresql-1-2-1-1 |       248.82 |      0.68 |           0.21 |                  0.21 |
| postgresql-1-2-2-1 |       238.47 |      0.62 |           0.12 |                  0.12 |

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
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Active Backends Waiting on Locks [sessions] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Max Transaction Duration (Lock Wait) [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Index Scan Count [scans] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log)
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
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-2-1-1 (bexhoma-metrics-postgresql-1-2-1-1-benchmarking.log)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* Number of Active Application Sessions [sessions] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Scan Count [scans] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Tuple Fetch Count [rows] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Index Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Buffer Hits [blocks] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Blocks Read outside Shared Buffers [blocks] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Table Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Total Cache Hit Ratio since Stats Reset [0..1] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Autoanalyze Run Count for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Autovacuum Run Count for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)
* Dead Tuples, Estimated [rows] for connection postgresql-1-2-2-1 (bexhoma-metrics-postgresql-1-2-2-1-benchmarking.log)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                18.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               1.00 |
| postgresql-1-1-2-1 |                                18.00 |                                                0.00 |                                                        0.00 |                                   6.00 |                                               1.00 |

#### Benchmarking phase: SUT deployment

| DBMS               |   Number of Idle Sessions [sessions] |   Number of Idle-in-transaction Sessions [sessions] |   Number of Idle-in-transaction Aborted Sessions [sessions] |   Number of Active Sessions [sessions] |   Number of Active Application Sessions [sessions] |
|:-------------------|-------------------------------------:|----------------------------------------------------:|------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------:|
| postgresql-1-1-1-1 |                                12.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |
| postgresql-1-1-2-1 |                                18.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |
| postgresql-1-2-1-1 |                                 9.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |
| postgresql-1-2-2-1 |                                10.00 |                                                0.00 |                                                        0.00 |                                  16.00 |                                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
