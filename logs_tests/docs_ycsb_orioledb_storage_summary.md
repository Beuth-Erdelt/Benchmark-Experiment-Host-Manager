## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 754s 
* Code: 1795421060
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [2].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['OrioleDB'].
  * Import is handled by 4 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [16] threads, split into [4] pods.
  * Benchmarking is tested with [32] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* orioledb-1-1-1-1 uses docker image orioledb/orioledb:v1.10.3-pg18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1035873
  * volume_size:48.9G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'listen_addresses=*', '-c', 'shared_preload_libraries=orioledb', '-c', 'default_table_access_method=orioledb', '-c', 'orioledb.main_buffers=16GB', '-c', 'orioledb.undo_buffers=256MB', '-c', 'orioledb.checkpoint_completion_ratio=1.0', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=1GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795421060
* orioledb-1-2-1-1 uses docker image orioledb/orioledb:v1.10.3-pg18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1028349
  * volume_size:48.9G
  * volume_used:3.9G
  * cpu_list:0-223
  * args:['-c', 'listen_addresses=*', '-c', 'shared_preload_libraries=orioledb', '-c', 'default_table_access_method=orioledb', '-c', 'orioledb.main_buffers=16GB', '-c', 'orioledb.undo_buffers=256MB', '-c', 'orioledb.checkpoint_completion_ratio=1.0', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=1GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795421060

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: OrioleDB-1-2

### Data Parameters of Reused Volumes
* OrioleDB-1: DDL values of the volume: fillfactor=100, autovacuum_scale=0.2
* OrioleDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Ingestion
* OrioleDB-1: 4 of 4 units ok

### SUT Container Restarts
* bexhoma-sut-orioledb-1-1795421060-bcd57c65f-xqsgk: 0
* bexhoma-sut-orioledb-1-1795421060-55bb55ff56-xlgd7: 0

### Workflow

#### Actual

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS OrioleDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS OrioleDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection         |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:-------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| orioledb-1-1-0-1-1 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4080.50 |                61267.00 |            250000.00 |                               751.00 | 1.00 |               58.76 |
| orioledb-1-1-0-1-2 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4080.57 |                61266.00 |            250000.00 |                               710.00 | 1.00 |               58.76 |
| orioledb-1-1-0-1-3 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4080.23 |                61271.00 |            250000.00 |                               814.00 | 1.00 |               58.76 |
| orioledb-1-1-0-1-4 |             1.00 |      4.00 |  4096.00 |        4.00 |     0.00 |                         4080.10 |                61273.00 |            250000.00 |                               772.00 | 1.00 |               58.75 |

#### Per Run

| DBMS         |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| OrioleDB-1-1 |             1.00 |     16.00 | 16384.00 |        4.00 |     0.00 | 1.00 |               58.75 |                        16321.40 |                61273.00 |           1000000.00 |                               761.75 |

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1-1-1 | orioledb-1-1-1 | orioledb-1-1-1-1 |                1 |        1 |               1 |       1 |        32 |    32768 |        0 |                        32470.70 |                30797.00 |             500524 |                             503.00 |               499476 |                              5239.00 |
| orioledb-1-2-1-1-1 | orioledb-1-2-1 | orioledb-1-2-1-1 |                2 |        1 |               1 |       1 |        32 |    32768 |        0 |                        32467.53 |                30800.00 |             499593 |                            1006.00 |               500407 |                              4551.00 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1 | orioledb-1-1-1 |                1 |        1 |               1 |           1 |        32 |    32768 |        0 |                        32470.70 |                30797.00 |             500524 |                             503.00 |               499476 |                              5239.00 |
| orioledb-1-2-1 | orioledb-1-2-1 |                2 |        1 |               1 |           1 |        32 |    32768 |        0 |                        32467.53 |                30800.00 |             499593 |                            1006.00 |               500407 |                              4551.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
