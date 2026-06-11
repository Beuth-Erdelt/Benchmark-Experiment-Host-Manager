## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1192s 
* Code: 1780839075
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.10.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:208183
  * cpu_list:0-127
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780839075
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214002
  * cpu_list:0-127
  * args:['-c', 'max_connections=640']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780839075

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      117.00 |           1.00 |            0.00 |         44.00 |           72.00 |              1 |          16 |          | None           |             0 | False         |              492.31 |

### Execution

#### Per Connection

| DBMS                     |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:-------------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 212692 | 489825 |         0.00 |          5 |        0 |
| PostgreSQL-1-1-2-1-2-1-1 |                1 |        8 |        2 |               1 |       1 | 236730 | 545049 |         0.00 |          5 |        0 |
| PostgreSQL-1-1-2-1-2-1-1 |                1 |        8 |        2 |               1 |       1 | 236728 | 544809 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS               |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-------------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|----------:|----------:|-----------:|---------:|
| PostgreSQL-1-1-1-1 |             1.00 |    16.00 |     1.00 |            1.00 |        1.00 |         0.00 | 212692.00 | 489825.00 |       5.00 |     0.00 |
| PostgreSQL-1-1-2-1 |             1.00 |    16.00 |     2.00 |            1.00 |        2.00 |         0.00 | 236729.00 | 544929.00 |       5.00 |     0.00 |

### Tests
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
