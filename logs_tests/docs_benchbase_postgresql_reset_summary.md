## Show Summary

### Workload
Benchbase Workload tpcc SF=4
* Type: benchbase
* Duration: 1150s 
* Code: 1785155087
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 4. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 2 minutes. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Experiment uses bexhoma version 0.10.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [40] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:837312
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785155087
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:810103
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1785155087
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785155087-66ff6c6869-5vk86: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    4 |      109.00 |           1.00 |            0.00 |         32.00 |           76.00 |              1 |           1 |             |                |             0 | False         |              132.11 |
| PostgreSQL-1-2 |                2 |    4 |      111.00 |           1.00 |            0.00 |         32.00 |           78.00 |              1 |           1 |             |                |             0 | False         |              129.73 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |          40 |     1024 |        1 |               1 |       1 |           0 | 120.00 |            1 |                        1023.96 |                     1016.69 |         0.00 |                                                      13414.00 |                                               5738.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |          40 |     1024 |        1 |               1 |       1 |           0 | 120.00 |            0 |                        1023.98 |                     1016.90 |         0.00 |                                                      11655.00 |                                               4395.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |          40 |     1024 |               1 |           1 |           0 | 120.00 |            1 |                        1023.96 |                     1016.69 |         0.00 |                                                      13414.00 |                                               5738.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |          40 |     1024 |               1 |           1 |           0 | 120.00 |            0 |                        1023.98 |                     1016.90 |         0.00 |                                                      11655.00 |                                               4395.00 |

#### Reset

| phase            | job                |   experiment_run |   client |   benchmark_run |   time_reset |
|:-----------------|:-------------------|-----------------:|---------:|----------------:|-------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |         2.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |         2.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
