## Show Summary

### Workload
Benchbase Workload tpcc SF=4
* Type: benchbase
* Duration: 825s 
* Code: 1792435792
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 4. Target is unlimited. Factors for benchmarking are [1]. Benchmarking runs for 2 minutes. Each benchmarker has a warmup of 60 seconds before that, which is not part of the results.
  * Experiment uses bexhoma version 0.11.7.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker39.
  * Benchmarking is fixed to cl-worker39.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:941091
  * datadisk:1132
  * volume_size:1.8T
  * volume_used:920G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792435792
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:946875
  * datadisk:2913
  * volume_size:1.8T
  * volume_used:925G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792435792
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792435792-6549d865d6-hpwpx: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    4 |       46.00 |           4.00 |            0.00 |         36.00 |            6.00 |              1 |           1 |             |                |             0 | False         |              313.04 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |        0 |        1 |               1 |       1 |           0 | 120.00 |           13 |                        2843.04 |                     4521.18 |         0.00 |                                                      38117.00 |                                              14049.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |        0 |        2 |               1 |       1 |           0 | 120.00 |            9 |                        1789.99 |                     2379.63 |         0.00 |                                                      32602.00 |                                              11163.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          20 |        0 |        2 |               1 |       2 |           0 | 120.00 |            2 |                        1824.17 |                     2422.02 |         0.00 |                                                      31776.00 |                                              10956.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |          40 |        0 |               1 |           1 |           0 | 120.00 |           13 |                        2843.04 |                     4521.18 |         0.00 |                                                      38117.00 |                                              14049.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |          40 |        0 |               1 |           2 |           0 | 120.00 |           11 |                        3614.16 |                     4801.65 |         0.00 |                                                      32602.00 |                                              11059.50 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
