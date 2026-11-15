## Show Summary

### Workload
Benchbase Workload twitter SF=16
* Type: benchbase
* Duration: 643s 
* Code: 1792706079
* Benchbase runs the Twitter benchmark.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'twitter'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma ve- waiting 30s -               : done
PostgreSQL-1                  : has running benchmarks
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 20 API requests 0.6s)
- waiting 30s -               : done
PostgreSQL-1                  : has running benchmarks
postgresql-1-1-2-1            : wrote benchmarking_timespans to D:/data/benchmarks/1794594384/postgresql-1-1-2-1.config
postgresql-1-1-2-1            : showing benchmarker times
postgresql-1-1-2-1            : benchmarker timespan job from 1794594897 to 1794595092
postgresql-1-1-2-1            : benchmarker timespan pods from 1794594901 to 1794595084
postgresql-1-1-2-1            : benchmarker timespan (start to end single container [s]) = 183
postgresql-1-1-2-1            : benchmarker times (start/end per pod and container) = [(1794594902, 1794595084), (1794594901, 1794595084)]
postgresql-1-1-2-1            : found and updated times {'benchmarker': [(1794594902, 1794595084), (1794594901, 1794595084)]}
Loop pass                     : took 9.4s (6 kubectl calls 7.5s, 28 API requests 1.2s)
PostgreSQL-1                  : can be stopped
PostgreSQL-1                  : had 0 restarts at worker bexhoma-sut-postgresql-1-1794594384-864bc64f97-2kw8t
Loop pass                     : took 5.5s (4 kubectl calls 4.1s, 29 API requests 0.9s)
Experiment                    : ends at 2026-11-13 19:38:20.461023 (231643.5947378) - 715.37s total
Experiment                    : downloading partial results
Experiment                    : uploading full results
Experiment                    : uploading workload file
Result workflow complete

## Show Summary

### Workload
Benchbase Workload tpcc SF=4
* Type: benchbase
* Duration: 716s 
* Code: 1794594384
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 4. Target is unlimited. Factors for benchmarking are [1]. Benchmarking runs for 2 minutes. Each benchmarker has a warmup of 60 seconds before that, which is not part of the results.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [40] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1151268
  * datadisk:1132
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794594384
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1155992
  * datadisk:3615
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794594384
    * TENANT_VOL:False

### Ingestion
* PostgreSQL-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794594384-864bc64f97-2kw8t: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    4 |       43.00 |           4.00 |            0.00 |         32.00 |            7.00 |              1 |         1 |             |                |             0 | False         |              334.88 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 |        40 |        0 |           0 | 120.00 |       14 |                        3726.20 |                     5990.24 |         0.00 |                                                      33894.00 |                                              10723.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 |        20 |        0 |           0 | 120.00 |        5 |                        1895.57 |                     2799.75 |         0.00 |                                                      31475.00 |                                              10535.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 |        20 |        0 |           0 | 120.00 |        7 |                        1919.91 |                     2831.21 |         0.00 |                                                      31294.00 |                                              10401.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 |        40 |        0 |           0 | 120.00 |       14 |                        3726.20 |                     5990.24 |         0.00 |                                                      33894.00 |                                              10723.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 |        40 |        0 |           0 | 120.00 |       12 |                        3815.48 |                     5630.96 |         0.00 |                                                      31475.00 |                                              10468.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
