## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 994s 
* Code: 1793470117
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861702
  * datadisk:668
  * volume_size:49G
  * volume_used:668M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793470117
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861703
  * datadisk:669
  * volume_size:49G
  * volume_used:669M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793470117
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793470117-6f7998b486-xlqdm: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                             |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] | loading_inherited   |
|:----------------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|:--------------------|
| 1793470117-PostgreSQL-1-1-0 |                1 | database       | False         |             2 |           0 |    1 |       25.00 |           5.00 |            0.00 |         25.00 |            5.00 |              2 |           1 |              144.00 | False               |
| 1793470117-PostgreSQL-1-1-1 |                1 | database       | False         |             2 |           1 |    1 |       23.00 |           5.00 |            0.00 |         23.00 |            5.00 |              2 |           1 |              156.52 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        95.88 |                                                      31251.00 |                                              14791.00 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.49 |                        0.49 |       103.58 |                                                      29217.00 |                                              14476.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        96.58 |                                                      32201.00 |                                              14098.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.47 |                        0.47 |        97.98 |                                                      36657.00 |                                              15245.00 |

#### Per Phase

| DBMS               | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-------------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-0 | postgresql-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        95.88 |                                                      31251.00 |                                              14791.00 |
| postgresql-1-1-1-1 | postgresql-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.49 |                        0.49 |       103.58 |                                                      29217.00 |                                              14476.00 |
| postgresql-1-1-2-0 | postgresql-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.46 |                        0.46 |        96.58 |                                                      32201.00 |                                              14098.00 |
| postgresql-1-1-2-1 | postgresql-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.47 |                        0.47 |        97.98 |                                                      36657.00 |                                              15245.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: efficiency contains no 0 or NaN
* TEST passed: Workflow as planned
