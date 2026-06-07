## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1676s 
* Code: 1780841560
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.9.10.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:202796
  * volume_size:30G
  * volume_used:2.6G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780841560
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:202795
  * volume_size:30G
  * volume_used:2.7G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780841560

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1], [1]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1], [1]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      456.00 |           1.00 |            0.00 |        220.00 |          235.00 |              1 |           8 |          | None           |             0 | False         |              126.32 |
| PostgreSQL-1-2 |                2 |   16 |      456.00 |           1.00 |            0.00 |        220.00 |          235.00 |              1 |           8 |          | None           |             0 | False         |              126.32 |

### Execution

#### Per Connection

| DBMS                     |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |   TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:-------------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|------:|-------------:|-----------:|---------:|-----------:|-----------:|
| PostgreSQL-1-1-1-1-1-1-1 |                1 |       16 |        1 |               1 |       1 |   4879 | 11189 |         0.00 |          5 |        0 |     267.07 |     475.17 |
| PostgreSQL-1-2-1-1-1-1-1 |                2 |       16 |        1 |               1 |       1 |   4843 | 11194 |         0.00 |          5 |        0 |     214.16 |     418.23 |

#### Per Phase

| DBMS               |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |    NOPM |      TPM |   duration |   errors |
|:-------------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|--------:|---------:|-----------:|---------:|
| PostgreSQL-1-1-1-1 |             1.00 |    16.00 |     1.00 |            1.00 |        1.00 |     267.07 |     475.17 |         0.00 | 4879.00 | 11189.00 |       5.00 |     0.00 |
| PostgreSQL-1-2-1-1 |             2.00 |    16.00 |     1.00 |            1.00 |        1.00 |     214.16 |     418.23 |         0.00 | 4843.00 | 11194.00 |       5.00 |     0.00 |

### Tests
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
