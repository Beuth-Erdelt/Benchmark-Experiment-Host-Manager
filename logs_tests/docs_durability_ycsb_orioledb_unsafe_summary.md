## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 451s 
* Code: 1795425170
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * Load durability is unsafe (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * Experiment is limited to DBMS ['OrioleDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
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
  * disk:1030993
  * volume_size:1.7T
  * volume_used:1006.8G
  * cpu_list:0-223
  * args:['-c', 'listen_addresses=*', '-c', 'shared_preload_libraries=orioledb', '-c', 'default_table_access_method=orioledb', '-c', 'orioledb.main_buffers=16GB', '-c', 'orioledb.undo_buffers=256MB', '-c', 'orioledb.checkpoint_completion_ratio=1.0', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=1GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: unsafe
  * eval_parameters
    * code:1795425170

### Ingestion
* OrioleDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-orioledb-1-1795425170-58b88dd9bd-2x7hf: 0

### Workflow

#### Actual

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS OrioleDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection         |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:-------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| orioledb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8068.16 |                15493.00 |            125000.00 |                               650.00 | 1.00 |              232.36 |
| orioledb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8078.07 |                15474.00 |            125000.00 |                               647.00 | 1.00 |              232.65 |
| orioledb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8079.63 |                15471.00 |            125000.00 |                               575.00 | 1.00 |              232.69 |
| orioledb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8085.38 |                15460.00 |            125000.00 |                               582.00 | 1.00 |              232.86 |
| orioledb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8080.68 |                15469.00 |            125000.00 |                               539.00 | 1.00 |              232.72 |
| orioledb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8075.46 |                15479.00 |            125000.00 |                               580.00 | 1.00 |              232.57 |
| orioledb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8077.02 |                15476.00 |            125000.00 |                               567.00 | 1.00 |              232.62 |
| orioledb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8076.50 |                15477.00 |            125000.00 |                               647.00 | 1.00 |              232.60 |

#### Per Run

| DBMS         |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| OrioleDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |              232.36 |                        64620.90 |                15493.00 |           1000000.00 |                               598.38 |

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1-1-1 | orioledb-1-1-1 | orioledb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    16384 |        0 |                        16290.09 |                61387.00 |             500299 |                             597.00 |               499701 |                              1244.00 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| orioledb-1-1-1 | orioledb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    16384 |        0 |                        16290.09 |                61387.00 |             500299 |                             597.00 |               499701 |                              1244.00 |

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
