## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 899s 
* Code: 1794064480
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
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
  * disk:812221
  * datadisk:5790
  * volume_size:1.8T
  * volume_used:794G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794064480
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812183
  * datadisk:5790
  * volume_size:1.8T
  * volume_used:794G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794064480
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812183
  * datadisk:5790
  * volume_size:1.8T
  * volume_used:794G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794064480

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794064480-6df7956555-69722: 0

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
| PostgreSQL-1-1 |                1 |    1 |      100.00 |           5.00 |            1.00 |         46.00 |           40.00 |              8 |           0 |             | None           |             0 | False         |               36.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        188 |            0.34 |            10751.29 |           1895.74 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-1-2-1-1 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        204 |            0.43 |             8555.40 |           1747.06 |          -1 | postgresql-1-1-2-1-1 |
| postgresql-1-1-2-1-2 | PostgreSQL-1    | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |                  99 |        205 |            0.43 |             8607.32 |           1738.54 |          -1 | postgresql-1-1-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        188 |            0.34 |            10751.29 |           1895.74 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |                 198 |        205 |            0.43 |             8581.32 |           3477.07 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-1-2 |      2 | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2         | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2             | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | 2/2          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |
|:--------------|-----------------------:|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  82.32 |                 100.86 |                  93.04 |
| TPC-DS Q2     |                 363.62 |                 377.40 |                 368.31 |
| TPC-DS Q3     |                 105.32 |                 110.99 |                 114.33 |
| TPC-DS Q4     |                6934.86 |                7402.28 |                7982.37 |
| TPC-DS Q5     |                 520.44 |                 714.83 |                 537.94 |
| TPC-DS Q6     |               55431.05 |               55371.56 |               54797.45 |
| TPC-DS Q7     |                 336.93 |                 362.37 |                 374.01 |
| TPC-DS Q8     |                  47.17 |                  57.10 |                  61.48 |
| TPC-DS Q9     |                1820.02 |                2387.12 |                2591.46 |
| TPC-DS Q10    |                 867.08 |                1101.34 |                1669.82 |
| TPC-DS Q11    |                3296.02 |                4918.31 |                4695.32 |
| TPC-DS Q12    |                  52.37 |                  71.20 |                  84.11 |
| TPC-DS Q13    |                 484.95 |                 599.46 |                 570.61 |
| TPC-DS Q14a+b |                2977.82 |                3599.79 |                3074.25 |
| TPC-DS Q15    |                 101.57 |                 116.46 |                 120.96 |
| TPC-DS Q16    |                 186.72 |                 372.82 |                 253.87 |
| TPC-DS Q17    |                 246.18 |                 310.52 |                 339.97 |
| TPC-DS Q18    |                 336.35 |                 391.15 |                 405.41 |
| TPC-DS Q19    |                 129.63 |                 182.98 |                 183.61 |
| TPC-DS Q20    |                  79.25 |                 116.07 |                 104.27 |
| TPC-DS Q21    |                 234.00 |                 298.20 |                 285.30 |
| TPC-DS Q22    |                3244.62 |                3934.08 |                4505.75 |
| TPC-DS Q23a+b |                3971.72 |                6386.12 |                5138.12 |
| TPC-DS Q24a+b |                 318.66 |                 395.24 |                 404.40 |
| TPC-DS Q25    |                 277.20 |                 337.59 |                 335.19 |
| TPC-DS Q26    |                 205.08 |                 279.06 |                 326.87 |
| TPC-DS Q27    |                 312.02 |                 702.41 |                 675.12 |
| TPC-DS Q28    |                1400.08 |                2512.42 |                2542.97 |
| TPC-DS Q29    |                 262.89 |                 399.85 |                 383.99 |
| TPC-DS Q30    |                8105.04 |               11794.29 |               11765.55 |
| TPC-DS Q31    |                1394.24 |                2194.75 |                1997.66 |
| TPC-DS Q32    |                  88.57 |                 100.10 |                  92.71 |
| TPC-DS Q33    |                 303.81 |                 385.50 |                 381.00 |
| TPC-DS Q34    |                  16.65 |                  28.10 |                  27.46 |
| TPC-DS Q35    |                 954.72 |                1273.29 |                1308.76 |
| TPC-DS Q36    |                 265.66 |                 496.26 |                 503.04 |
| TPC-DS Q37    |                 269.75 |                 503.22 |                 382.98 |
| TPC-DS Q38    |                 815.93 |                1517.43 |                1454.84 |
| TPC-DS Q39a+b |                2531.97 |                3239.77 |                3219.05 |
| TPC-DS Q40    |                 108.22 |                 134.75 |                 128.31 |
| TPC-DS Q41    |                 775.41 |                1082.21 |                1157.52 |
| TPC-DS Q42    |                  91.19 |                 115.80 |                 103.07 |
| TPC-DS Q43    |                  18.98 |                  20.16 |                  29.15 |
| TPC-DS Q44    |                 376.34 |                 477.42 |                 464.81 |
| TPC-DS Q45    |                  63.90 |                  89.77 |                  83.96 |
| TPC-DS Q46    |                  23.52 |                  28.09 |                  30.47 |
| TPC-DS Q47    |                1268.57 |                1615.84 |                1687.19 |
| TPC-DS Q48    |                 637.07 |                 730.54 |                1311.89 |
| TPC-DS Q49    |                 432.88 |                1048.89 |                 794.53 |
| TPC-DS Q50    |                 409.32 |                 490.85 |                 461.26 |
| TPC-DS Q51    |                 690.31 |                1108.03 |                1332.17 |
| TPC-DS Q52    |                  87.15 |                 107.07 |                 102.78 |
| TPC-DS Q53    |                 105.27 |                 143.67 |                 150.94 |
| TPC-DS Q54    |                  60.83 |                  82.53 |                  80.84 |
| TPC-DS Q55    |                  82.14 |                 102.59 |                 103.13 |
| TPC-DS Q56    |                 299.94 |                 398.66 |                 403.07 |
| TPC-DS Q57    |                 740.47 |                1228.74 |                1462.36 |
| TPC-DS Q58    |                 610.90 |                 790.69 |                 420.45 |
| TPC-DS Q59    |                 554.89 |                 521.18 |                 588.86 |
| TPC-DS Q60    |                 410.09 |                 440.91 |                 436.69 |
| TPC-DS Q61    |                 127.62 |                 153.55 |                 135.21 |
| TPC-DS Q62    |                  99.06 |                 104.74 |                 113.63 |
| TPC-DS Q63    |                 112.29 |                 130.56 |                 136.77 |
| TPC-DS Q64    |                 643.08 |                 819.87 |                1007.34 |
| TPC-DS Q65    |                 509.05 |                 730.90 |                 956.13 |
| TPC-DS Q66    |                 171.22 |                 215.22 |                 214.60 |
| TPC-DS Q67    |                3007.08 |                4300.23 |                4317.02 |
| TPC-DS Q68    |                  29.44 |                  34.52 |                  39.34 |
| TPC-DS Q69    |                 299.58 |                 410.94 |                 389.48 |
| TPC-DS Q70    |                 339.59 |                 497.33 |                 585.65 |
| TPC-DS Q71    |                 265.37 |                 314.17 |                 588.17 |
| TPC-DS Q72    |                 825.52 |                1486.53 |                1369.41 |
| TPC-DS Q73    |                  23.64 |                  51.21 |                  29.17 |
| TPC-DS Q74    |                1563.00 |                1384.75 |                1101.72 |
| TPC-DS Q75    |                 571.65 |                 794.44 |                 866.89 |
| TPC-DS Q76    |                 206.46 |                 293.63 |                 250.90 |
| TPC-DS Q77    |                 277.08 |                 357.67 |                 574.63 |
| TPC-DS Q78    |                1106.27 |                1612.14 |                1567.41 |
| TPC-DS Q79    |                 120.05 |                 209.10 |                 149.59 |
| TPC-DS Q80    |                 531.08 |                 570.98 |                 527.96 |
| TPC-DS Q81    |               47514.05 |               41824.51 |               42209.39 |
| TPC-DS Q82    |                 419.02 |                 368.86 |                 361.36 |
| TPC-DS Q83    |                  74.44 |                  63.72 |                  63.63 |
| TPC-DS Q84    |                  83.20 |                  64.40 |                  68.06 |
| TPC-DS Q85    |                 348.48 |                 484.10 |                 427.28 |
| TPC-DS Q86    |                 193.39 |                 296.21 |                 153.79 |
| TPC-DS Q87    |                1064.61 |                 815.09 |                 844.53 |
| TPC-DS Q88    |                2920.21 |                1956.96 |                1950.43 |
| TPC-DS Q89    |                  25.10 |                  22.44 |                  21.93 |
| TPC-DS Q90    |                 122.59 |                  97.37 |                  86.81 |
| TPC-DS Q91    |                 140.38 |                 116.44 |                 111.43 |
| TPC-DS Q92    |                  58.86 |                  50.86 |                  41.75 |
| TPC-DS Q93    |                 272.43 |                 227.43 |                 197.81 |
| TPC-DS Q94    |                 166.02 |                 127.64 |                 330.92 |
| TPC-DS Q95    |                4487.29 |                3705.83 |                3418.82 |
| TPC-DS Q96    |                 105.62 |                  96.10 |                  94.67 |
| TPC-DS Q97    |                 442.97 |                 408.00 |                 334.45 |
| TPC-DS Q98    |                 169.81 |                 306.52 |                 310.21 |
| TPC-DS Q99    |                 195.71 |                 363.38 |                 280.74 |

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
