## Show Summary

### Workload
YCSB Data Loading SF=1
* Type: ycsb
* Duration: 339s 
* Code: 1782304350
* YCSB driver runs the experiment.
* This imports YCSB data sets.
  * Workload is 'C'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Experiment is run once.

### Services
PostgreSQL-1
* kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1782304350 9091:9091

### Connections
* PostgreSQL-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222854
  * datadisk:2391
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782304350

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.95 |                61276.00 |            125000.00 |                              1477.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2039.98 |                61275.00 |            125000.00 |                              1497.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.08 |                61272.00 |            125000.00 |                              1497.00 | 1.00 |               58.75 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.18 |                61269.00 |            125000.00 |                              1495.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.28 |                61266.00 |            125000.00 |                              1545.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.22 |                61268.00 |            125000.00 |                              1497.00 | 1.00 |               58.76 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.62 |                61256.00 |            125000.00 |                              1506.00 | 1.00 |               58.77 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |         0.00 |                         2040.38 |                61263.00 |            125000.00 |                              1508.00 | 1.00 |               58.76 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |         0.00 | 1.00 |               58.75 |                        16321.70 |                61276.00 |           1000000.00 |                              1502.75 |

### Monitoring

### Loading phase: SUT deployment

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |       241.19 |      3.91 |           1.71 |                  2.70 |

### Loading phase: component loader

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1 |        82.91 |      1.44 |           0.11 |                  0.11 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
