## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 853s 
* Code: 1794607790
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1129609
  * datadisk:5791
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794607790
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1132177
  * datadisk:5791
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794607790
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1132177
  * datadisk:5791
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794607790

### Ingestion
* PostgreSQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794607790-67c88fbc64-rggwr: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       97.00 |           5.00 |            1.00 |         45.00 |           38.00 |              8 |         0 |             | None           |             0 | False         |               37.11 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        163 |            0.32 |            11452.18 |           2186.50 |          -1 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               99 |                  99 |        176 |            0.37 |            10038.95 |           2025.00 |          -1 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 | 1.00 |               99 |                  99 |        174 |            0.37 |             9940.59 |           2048.28 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        163 |            0.32 |            11452.18 |           2186.50 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        176 |            0.37 |             9989.65 |           4050.00 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |
|:--------------|-----------------------:|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  86.73 |                  92.20 |                  86.07 |
| TPC-DS Q2     |                 325.48 |                 325.35 |                 331.25 |
| TPC-DS Q3     |                 103.25 |                  97.90 |                 105.68 |
| TPC-DS Q4     |                5518.15 |                5430.23 |                5798.33 |
| TPC-DS Q5     |                 466.75 |                 458.55 |                 466.32 |
| TPC-DS Q6     |               50066.76 |               50388.75 |               50923.73 |
| TPC-DS Q7     |                 334.23 |                 300.75 |                 317.49 |
| TPC-DS Q8     |                  48.78 |                  50.41 |                  54.42 |
| TPC-DS Q9     |                1909.52 |                1861.43 |                1929.26 |
| TPC-DS Q10    |                 878.82 |                 859.55 |                 980.01 |
| TPC-DS Q11    |                3157.06 |                3806.66 |                3306.80 |
| TPC-DS Q12    |                  57.05 |                  52.26 |                 105.46 |
| TPC-DS Q13    |                 588.27 |                 831.47 |                 663.74 |
| TPC-DS Q14a+b |                2202.97 |                3236.87 |                2559.16 |
| TPC-DS Q15    |                 103.02 |                  94.88 |                 101.00 |
| TPC-DS Q16    |                 193.05 |                 411.85 |                 186.67 |
| TPC-DS Q17    |                 275.88 |                 413.32 |                 332.59 |
| TPC-DS Q18    |                 358.60 |                 336.72 |                 651.19 |
| TPC-DS Q19    |                 125.55 |                 124.25 |                 130.93 |
| TPC-DS Q20    |                  89.40 |                  86.21 |                  84.14 |
| TPC-DS Q21    |                 231.34 |                 258.02 |                 229.53 |
| TPC-DS Q22    |                2726.59 |                3100.28 |                2891.59 |
| TPC-DS Q23a+b |                3214.04 |                3226.20 |                3521.00 |
| TPC-DS Q24a+b |                 496.92 |                 514.20 |                 570.01 |
| TPC-DS Q25    |                 273.36 |                 257.38 |                 255.53 |
| TPC-DS Q26    |                 203.07 |                 201.94 |                 201.51 |
| TPC-DS Q27    |                 323.43 |                 328.86 |                 300.24 |
| TPC-DS Q28    |                1467.50 |                1439.51 |                1390.76 |
| TPC-DS Q29    |                 384.03 |                 272.19 |                 277.38 |
| TPC-DS Q30    |                7694.58 |                7830.05 |                7839.44 |
| TPC-DS Q31    |                1325.95 |                1479.87 |                1302.90 |
| TPC-DS Q32    |                  89.65 |                 115.08 |                 163.63 |
| TPC-DS Q33    |                 337.20 |                 446.17 |                 497.63 |
| TPC-DS Q34    |                  19.49 |                  22.35 |                  23.50 |
| TPC-DS Q35    |                1141.18 |                 977.92 |                1074.66 |
| TPC-DS Q36    |                 265.88 |                 261.78 |                 263.11 |
| TPC-DS Q37    |                 278.22 |                 278.89 |                 276.42 |
| TPC-DS Q38    |                 766.52 |                1259.45 |                 757.34 |
| TPC-DS Q39a+b |                2168.88 |                2333.45 |                2787.23 |
| TPC-DS Q40    |                 110.46 |                  96.77 |                 105.18 |
| TPC-DS Q41    |                 747.36 |                 743.08 |                 760.44 |
| TPC-DS Q42    |                  93.43 |                  86.95 |                  92.74 |
| TPC-DS Q43    |                  21.36 |                  19.06 |                  23.49 |
| TPC-DS Q44    |                 341.50 |                 335.49 |                 346.15 |
| TPC-DS Q45    |                  66.65 |                  71.75 |                  68.27 |
| TPC-DS Q46    |                  28.00 |                  30.13 |                  26.33 |
| TPC-DS Q47    |                1327.01 |                1308.96 |                1378.19 |
| TPC-DS Q48    |                 479.70 |                 468.61 |                 466.65 |
| TPC-DS Q49    |                 431.79 |                 587.71 |                 588.54 |
| TPC-DS Q50    |                 316.58 |                 311.39 |                 311.27 |
| TPC-DS Q51    |                 708.74 |                 886.01 |                 887.24 |
| TPC-DS Q52    |                  99.73 |                  92.52 |                  92.04 |
| TPC-DS Q53    |                 117.18 |                 308.71 |                 304.65 |
| TPC-DS Q54    |                  66.42 |                 130.35 |                 143.86 |
| TPC-DS Q55    |                  91.69 |                 213.50 |                 201.34 |
| TPC-DS Q56    |                 280.98 |                 315.77 |                 364.43 |
| TPC-DS Q57    |                 715.85 |                 701.07 |                 760.58 |
| TPC-DS Q58    |                 300.69 |                 372.29 |                 343.86 |
| TPC-DS Q59    |                 412.41 |                 414.11 |                 415.78 |
| TPC-DS Q60    |                 531.20 |                 328.04 |                 328.08 |
| TPC-DS Q61    |                 121.13 |                 102.04 |                 104.01 |
| TPC-DS Q62    |                  97.05 |                  85.01 |                  85.25 |
| TPC-DS Q63    |                 129.55 |                 113.48 |                 118.43 |
| TPC-DS Q64    |                 573.36 |                 685.27 |                 617.04 |
| TPC-DS Q65    |                 511.13 |                 677.83 |                 525.41 |
| TPC-DS Q66    |                 152.76 |                 160.55 |                 158.87 |
| TPC-DS Q67    |                2588.28 |                2554.63 |                2635.12 |
| TPC-DS Q68    |                  30.41 |                  28.30 |                  30.17 |
| TPC-DS Q69    |                 110.63 |                 179.49 |                 117.01 |
| TPC-DS Q70    |                 359.06 |                 413.07 |                 348.01 |
| TPC-DS Q71    |                 273.48 |                 525.34 |                 261.69 |
| TPC-DS Q72    |                 809.30 |                1269.89 |                1414.68 |
| TPC-DS Q73    |                  21.19 |                  22.04 |                  40.53 |
| TPC-DS Q74    |                 853.27 |                 856.56 |                 905.95 |
| TPC-DS Q75    |                 602.29 |                 602.88 |                 594.56 |
| TPC-DS Q76    |                 234.21 |                 214.13 |                 233.17 |
| TPC-DS Q77    |                 288.13 |                 301.71 |                 284.50 |
| TPC-DS Q78    |                1004.58 |                1381.29 |                1520.96 |
| TPC-DS Q79    |                 119.73 |                 121.00 |                 149.88 |
| TPC-DS Q80    |                 365.19 |                 362.01 |                 359.29 |
| TPC-DS Q81    |               32791.17 |               34760.03 |               35644.25 |
| TPC-DS Q82    |                 331.59 |                 514.98 |                 588.42 |
| TPC-DS Q83    |                  69.83 |                 136.83 |                 142.99 |
| TPC-DS Q84    |                  18.39 |                  41.32 |                  41.72 |
| TPC-DS Q85    |                 272.39 |                 496.94 |                 984.18 |
| TPC-DS Q86    |                 156.29 |                 264.34 |                 221.01 |
| TPC-DS Q87    |                 818.73 |                 993.35 |                1032.26 |
| TPC-DS Q88    |                2001.02 |                2535.06 |                2530.23 |
| TPC-DS Q89    |                 133.27 |                 145.42 |                 135.60 |
| TPC-DS Q90    |                  93.76 |                 107.98 |                 106.33 |
| TPC-DS Q91    |                 113.29 |                 121.74 |                 123.48 |
| TPC-DS Q92    |                  56.90 |                  57.67 |                  59.17 |
| TPC-DS Q93    |                 203.38 |                 258.02 |                 286.30 |
| TPC-DS Q94    |                 138.19 |                 143.43 |                 146.29 |
| TPC-DS Q95    |                2645.61 |                2556.65 |                2554.16 |
| TPC-DS Q96    |                  95.21 |                 102.47 |                 102.64 |
| TPC-DS Q97    |                 328.53 |                 353.61 |                 429.57 |
| TPC-DS Q98    |                 140.07 |                 256.00 |                 424.37 |
| TPC-DS Q99    |                 161.89 |                 403.37 |                 167.73 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
