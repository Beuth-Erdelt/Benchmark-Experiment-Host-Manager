## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 766s 
* Code: 1793872761
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:887125
  * datadisk:5791
  * volume_size:1.8T
  * volume_used:867G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793872761
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:855511
  * datadisk:5791
  * volume_size:1.8T
  * volume_used:836G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793872761
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:855511
  * datadisk:5791
  * volume_size:1.8T
  * volume_used:836G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793872761

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793872761-797d65bbc5-77shs: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       94.00 |           2.00 |            1.00 |         43.00 |           34.00 |              8 |           0 |             | None           |             0 | False         |               38.30 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        187 |            0.34 |            10935.88 |           1905.88 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        183 |            0.37 |            10020.16 |           1947.54 |          -1 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        179 |            0.36 |            10142.11 |           1991.06 |          -1 | postgresql-1-1-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        187 |            0.34 |            10935.88 |           1905.88 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        183 |            0.37 |            10080.95 |           3895.08 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |
|:--------------|-----------------------:|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  93.46 |                 340.01 |                 234.79 |
| TPC-DS Q2     |                 366.66 |                1429.43 |                1323.70 |
| TPC-DS Q3     |                 114.52 |                 394.50 |                 328.39 |
| TPC-DS Q4     |                6354.55 |                9563.13 |                9050.97 |
| TPC-DS Q5     |                 458.32 |                 455.67 |                 593.54 |
| TPC-DS Q6     |               62436.34 |               54442.17 |               54893.08 |
| TPC-DS Q7     |                 323.57 |                 532.80 |                 506.75 |
| TPC-DS Q8     |                  48.49 |                  49.73 |                  45.53 |
| TPC-DS Q9     |                2019.88 |                2052.53 |                2048.58 |
| TPC-DS Q10    |                 920.74 |                 894.55 |                 883.12 |
| TPC-DS Q11    |                4080.73 |                3409.79 |                3279.23 |
| TPC-DS Q12    |                  51.61 |                  56.22 |                  51.81 |
| TPC-DS Q13    |                 508.50 |                 494.08 |                 489.56 |
| TPC-DS Q14a+b |                2979.93 |                3185.99 |                2569.78 |
| TPC-DS Q15    |                 285.06 |                  97.22 |                  95.37 |
| TPC-DS Q16    |                 253.44 |                 187.95 |                 184.68 |
| TPC-DS Q17    |                 291.46 |                 262.85 |                 259.64 |
| TPC-DS Q18    |                 332.87 |                 326.16 |                 355.87 |
| TPC-DS Q19    |                 136.19 |                 136.40 |                 129.86 |
| TPC-DS Q20    |                  89.03 |                  89.29 |                  82.52 |
| TPC-DS Q21    |                 255.42 |                 246.16 |                 241.98 |
| TPC-DS Q22    |                3051.00 |                3004.91 |                3027.87 |
| TPC-DS Q23a+b |                4101.80 |                4392.67 |                4282.44 |
| TPC-DS Q24a+b |                 592.42 |                 523.22 |                 587.65 |
| TPC-DS Q25    |                 273.82 |                 275.36 |                 257.78 |
| TPC-DS Q26    |                 197.29 |                 206.20 |                 203.00 |
| TPC-DS Q27    |                 311.73 |                 345.23 |                 320.61 |
| TPC-DS Q28    |                1698.12 |                1417.50 |                1488.87 |
| TPC-DS Q29    |                 528.06 |                 451.86 |                 282.28 |
| TPC-DS Q30    |                 758.68 |                 784.82 |                 971.78 |
| TPC-DS Q31    |                1304.72 |                1406.66 |                1385.60 |
| TPC-DS Q32    |                 147.58 |                 154.48 |                 152.48 |
| TPC-DS Q33    |                 309.38 |                 334.09 |                 331.67 |
| TPC-DS Q34    |                  19.37 |                  20.39 |                  24.65 |
| TPC-DS Q35    |                 946.46 |                 972.08 |                 962.99 |
| TPC-DS Q36    |                 661.11 |                 270.57 |                 286.53 |
| TPC-DS Q37    |                 486.13 |                 292.44 |                 279.83 |
| TPC-DS Q38    |                 974.15 |                1290.97 |                1075.37 |
| TPC-DS Q39a+b |                2584.40 |                2613.78 |                2730.16 |
| TPC-DS Q40    |                 110.39 |                 103.05 |                 124.16 |
| TPC-DS Q41    |                 869.47 |                1113.23 |                 966.34 |
| TPC-DS Q42    |                  90.67 |                 111.43 |                  93.77 |
| TPC-DS Q43    |                  19.03 |                  27.35 |                  23.54 |
| TPC-DS Q44    |                   1.77 |                   2.32 |                   1.97 |
| TPC-DS Q45    |                  74.85 |                  75.41 |                  79.02 |
| TPC-DS Q46    |                  31.87 |                  29.33 |                  33.64 |
| TPC-DS Q47    |                1291.47 |                1367.50 |                1521.89 |
| TPC-DS Q48    |                 800.67 |                 765.39 |                 529.34 |
| TPC-DS Q49    |                 945.25 |                 963.14 |                 792.64 |
| TPC-DS Q50    |                 462.81 |                 370.00 |                 536.61 |
| TPC-DS Q51    |                 740.87 |                 849.77 |                 762.94 |
| TPC-DS Q52    |                  91.84 |                 104.06 |                 109.95 |
| TPC-DS Q53    |                 119.01 |                 134.84 |                 139.21 |
| TPC-DS Q54    |                  69.58 |                  81.49 |                  85.53 |
| TPC-DS Q55    |                  91.51 |                 101.26 |                  97.13 |
| TPC-DS Q56    |                 321.66 |                 298.45 |                 366.12 |
| TPC-DS Q57    |                 783.12 |                 927.49 |                 841.39 |
| TPC-DS Q58    |                 328.27 |                 401.05 |                 363.04 |
| TPC-DS Q59    |                 808.51 |                 544.73 |                 542.52 |
| TPC-DS Q60    |                 776.86 |                 512.64 |                 368.40 |
| TPC-DS Q61    |                 111.58 |                 110.13 |                 144.53 |
| TPC-DS Q62    |                  94.53 |                 109.66 |                 120.69 |
| TPC-DS Q63    |                 142.95 |                 380.46 |                 131.05 |
| TPC-DS Q64    |                 696.72 |                 900.98 |                 874.77 |
| TPC-DS Q65    |                 569.32 |                1097.41 |                 735.63 |
| TPC-DS Q66    |                 182.95 |                 253.45 |                 220.58 |
| TPC-DS Q67    |                2981.52 |                3299.44 |                3397.28 |
| TPC-DS Q68    |                  35.66 |                  35.14 |                  42.68 |
| TPC-DS Q69    |                 312.49 |                 449.30 |                 502.51 |
| TPC-DS Q70    |                 357.51 |                 510.18 |                 427.67 |
| TPC-DS Q71    |                 306.95 |                 325.60 |                 325.55 |
| TPC-DS Q72    |                1309.31 |                1091.93 |                1112.48 |
| TPC-DS Q73    |                  23.46 |                  24.08 |                  25.00 |
| TPC-DS Q74    |                1160.99 |                1349.37 |                1051.34 |
| TPC-DS Q75    |                1011.05 |                 878.99 |                 737.94 |
| TPC-DS Q76    |                 238.28 |                 267.23 |                 249.47 |
| TPC-DS Q77    |                 294.82 |                 361.38 |                 360.63 |
| TPC-DS Q78    |                1088.56 |                1349.49 |                1594.62 |
| TPC-DS Q79    |                 186.13 |                 189.72 |                 174.17 |
| TPC-DS Q80    |                 429.81 |                 511.17 |                 408.30 |
| TPC-DS Q81    |               38188.01 |               40849.44 |               41235.62 |
| TPC-DS Q82    |                 362.88 |                 377.25 |                 381.78 |
| TPC-DS Q83    |                  72.12 |                  86.27 |                  76.58 |
| TPC-DS Q84    |                  21.43 |                  20.61 |                  22.67 |
| TPC-DS Q85    |                 268.70 |                 297.62 |                 285.26 |
| TPC-DS Q86    |                 175.74 |                 192.65 |                 180.45 |
| TPC-DS Q87    |                 841.71 |                 993.28 |                 930.66 |
| TPC-DS Q88    |                2302.86 |                2602.75 |                2274.75 |
| TPC-DS Q89    |                  19.93 |                  23.95 |                  30.66 |
| TPC-DS Q90    |                 101.16 |                 108.86 |                 222.69 |
| TPC-DS Q91    |                  87.72 |                 103.90 |                 199.13 |
| TPC-DS Q92    |                  53.77 |                  63.18 |                 151.80 |
| TPC-DS Q93    |                 263.38 |                 289.51 |                 312.96 |
| TPC-DS Q94    |                 150.17 |                 155.85 |                 171.74 |
| TPC-DS Q95    |                3237.27 |                3404.04 |                3120.19 |
| TPC-DS Q96    |                  98.02 |                 111.57 |                 105.98 |
| TPC-DS Q97    |                 346.14 |                 412.71 |                 411.30 |
| TPC-DS Q98    |                 154.47 |                 168.12 |                 215.40 |
| TPC-DS Q99    |                 167.04 |                 179.12 |                 175.36 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
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
