## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 380s 
* Code: 1793617549
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['DatabaseService'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 2.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* databaseservice-1-1-1-1 uses docker image postgres:16.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:741412
  * datadisk:39
  * volume_size:1.8T
  * volume_used:725G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 1.0 CPU, 1.0 GiB RAM requested in 1 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793617549

### Init Scripts Not in Folder
* DatabaseService-1: skipped checkschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-databaseservice-1-1793617549-7dfc479b6b-x5pbq: 0

### Workflow

#### Actual

* DBMS DatabaseService-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DatabaseService-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| databaseservice-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6936.74 |                18020.00 |            125000.00 |                              4695.00 | 1.00 |              199.78 |
| databaseservice-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7003.59 |                17848.00 |            125000.00 |                              4895.00 | 1.00 |              201.70 |
| databaseservice-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6949.46 |                17987.00 |            125000.00 |                              4935.00 | 1.00 |              200.14 |
| databaseservice-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6959.14 |                17962.00 |            125000.00 |                              4943.00 | 1.00 |              200.42 |
| databaseservice-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6951.01 |                17983.00 |            125000.00 |                              4799.00 | 1.00 |              200.19 |
| databaseservice-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6950.24 |                17985.00 |            125000.00 |                              4951.00 | 1.00 |              200.17 |
| databaseservice-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6848.94 |                18251.00 |            125000.00 |                              4807.00 | 1.00 |              197.25 |
| databaseservice-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         6753.11 |                18510.00 |            125000.00 |                              4811.00 | 1.00 |              194.49 |

#### Per Run

| DBMS                |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DatabaseService-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              194.49 |                        55352.21 |                18510.00 |           1000000.00 |                              4854.50 |

### Benchmarking

#### Per Connection

| DBMS                      | phase                 | job                     | configuration     |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------------|:----------------------|:------------------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| databaseservice-1-1-1-1-1 | databaseservice-1-1-1 | databaseservice-1-1-1-1 | DatabaseService-1 |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        63922.27 |                15644.00 |             499360 |                             436.00 |               500640 |                              1663.00 |

#### Per Phase

| DBMS                  | phase                 |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| databaseservice-1-1-1 | databaseservice-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        63922.27 |                15644.00 |             499360 |                             436.00 |               500640 |                              1663.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
