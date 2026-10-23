## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1134s 
* Code: 1792709181
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920048
  * datadisk:5794
  * volume_size:49G
  * volume_used:5.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792709181
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:920018
  * datadisk:5794
  * volume_size:49G
  * volume_used:5.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792709181

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1792709181-7bc865bb85-76vzf: 0
* bexhoma-sut-postgresql-1-1792709181-86566ccf8f-f7gz8: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |      101.00 |           7.00 |            1.00 |         43.00 |           42.00 |              8 |           0 |             | None           |             0 | False         |               35.64 | False               |
| PostgreSQL-1-2 |                2 |    1 |      101.00 |           7.00 |            1.00 |         43.00 |           42.00 |              8 |           0 |             | None           |             0 | False         |               35.64 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        160 |            0.29 |            12744.12 |           2227.50 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        168 |            0.32 |            11676.30 |           2121.43 |          -1 | postgresql-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        160 |            0.29 |            12744.12 |           2227.50 |          -1 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        168 |            0.32 |            11676.30 |           2121.43 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-2-1-1-1 |
|:--------------|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  83.00 |                1639.93 |
| TPC-DS Q2     |                 328.66 |                 435.69 |
| TPC-DS Q3     |                  95.66 |                 224.87 |
| TPC-DS Q4     |                5404.33 |                5601.19 |
| TPC-DS Q5     |                 461.25 |                 527.55 |
| TPC-DS Q6     |               48854.02 |               48292.68 |
| TPC-DS Q7     |                 303.64 |                 373.05 |
| TPC-DS Q8     |                  49.02 |                  50.83 |
| TPC-DS Q9     |                1846.80 |                1868.25 |
| TPC-DS Q10    |                 873.83 |                2690.03 |
| TPC-DS Q11    |                3049.11 |                3158.64 |
| TPC-DS Q12    |                  54.72 |                  56.14 |
| TPC-DS Q13    |                 482.72 |                 473.96 |
| TPC-DS Q14a+b |                2144.67 |                2153.59 |
| TPC-DS Q15    |                  93.03 |                 106.86 |
| TPC-DS Q16    |                 175.58 |                 205.71 |
| TPC-DS Q17    |                 244.03 |                 263.61 |
| TPC-DS Q18    |                 310.39 |                 342.01 |
| TPC-DS Q19    |                 121.64 |                 122.74 |
| TPC-DS Q20    |                  78.53 |                  81.95 |
| TPC-DS Q21    |                 233.41 |                 310.20 |
| TPC-DS Q22    |                2560.65 |                2655.79 |
| TPC-DS Q23a+b |                3615.45 |                3541.90 |
| TPC-DS Q24a+b |                 646.92 |                 661.22 |
| TPC-DS Q25    |                 259.27 |                 253.64 |
| TPC-DS Q26    |                 193.84 |                 206.05 |
| TPC-DS Q27    |                  40.43 |                  37.46 |
| TPC-DS Q28    |                1343.76 |                1329.40 |
| TPC-DS Q29    |                 268.86 |                 279.32 |
| TPC-DS Q30    |                7687.49 |                7608.32 |
| TPC-DS Q31    |                1300.76 |                1308.44 |
| TPC-DS Q32    |                 101.96 |                 111.28 |
| TPC-DS Q33    |                 329.18 |                 326.42 |
| TPC-DS Q34    |                  18.42 |                  21.32 |
| TPC-DS Q35    |                 969.84 |                 989.42 |
| TPC-DS Q36    |                 284.61 |                 285.48 |
| TPC-DS Q37    |                 324.12 |                 333.45 |
| TPC-DS Q38    |                 958.22 |                 965.90 |
| TPC-DS Q39a+b |                1933.71 |                1960.22 |
| TPC-DS Q40    |                 102.62 |                 107.28 |
| TPC-DS Q41    |                 744.67 |                 746.10 |
| TPC-DS Q42    |                  92.10 |                  86.67 |
| TPC-DS Q43    |                  20.79 |                  17.96 |
| TPC-DS Q44    |                   2.35 |                   4.36 |
| TPC-DS Q45    |                  73.66 |                  71.55 |
| TPC-DS Q46    |                  24.95 |                  22.97 |
| TPC-DS Q47    |                1152.17 |                1160.27 |
| TPC-DS Q48    |                 476.95 |                 477.76 |
| TPC-DS Q49    |                 426.08 |                 424.85 |
| TPC-DS Q50    |                 383.02 |                 383.00 |
| TPC-DS Q51    |                 692.25 |                 684.41 |
| TPC-DS Q52    |                  80.66 |                  90.40 |
| TPC-DS Q53    |                 103.10 |                 109.34 |
| TPC-DS Q54    |                  62.30 |                  67.54 |
| TPC-DS Q55    |                  80.22 |                  80.42 |
| TPC-DS Q56    |                 313.38 |                 312.30 |
| TPC-DS Q57    |                 622.50 |                 588.30 |
| TPC-DS Q58    |                 296.78 |                 317.13 |
| TPC-DS Q59    |                 410.26 |                 416.67 |
| TPC-DS Q60    |                 303.86 |                 300.83 |
| TPC-DS Q61    |                 105.67 |                 106.04 |
| TPC-DS Q62    |                  92.37 |                 101.88 |
| TPC-DS Q63    |                 103.31 |                 109.41 |
| TPC-DS Q64    |                 589.87 |                 581.91 |
| TPC-DS Q65    |                 503.70 |                 512.04 |
| TPC-DS Q66    |                 166.93 |                 187.43 |
| TPC-DS Q67    |                2084.58 |                2126.38 |
| TPC-DS Q68    |                  30.00 |                  34.92 |
| TPC-DS Q69    |                 114.55 |                 121.95 |
| TPC-DS Q70    |                 341.50 |                 340.63 |
| TPC-DS Q71    |                 263.06 |                 276.72 |
| TPC-DS Q72    |                 792.00 |                 829.22 |
| TPC-DS Q73    |                  20.86 |                  21.20 |
| TPC-DS Q74    |                 845.76 |                 817.94 |
| TPC-DS Q75    |                 604.96 |                 586.65 |
| TPC-DS Q76    |                 198.53 |                 206.74 |
| TPC-DS Q77    |                 281.85 |                 289.19 |
| TPC-DS Q78    |                 946.73 |                1036.25 |
| TPC-DS Q79    |                 143.91 |                 155.42 |
| TPC-DS Q80    |                 351.15 |                 359.40 |
| TPC-DS Q81    |               31507.87 |               31646.11 |
| TPC-DS Q82    |                 348.41 |                 361.89 |
| TPC-DS Q83    |                  67.78 |                  71.24 |
| TPC-DS Q84    |                  18.18 |                  19.75 |
| TPC-DS Q85    |                 275.60 |                 265.13 |
| TPC-DS Q86    |                 159.21 |                 150.52 |
| TPC-DS Q87    |                1011.85 |                1027.39 |
| TPC-DS Q88    |                1935.71 |                1938.40 |
| TPC-DS Q89    |                 129.54 |                 130.49 |
| TPC-DS Q90    |                  94.05 |                  97.63 |
| TPC-DS Q91    |                  86.38 |                  93.09 |
| TPC-DS Q92    |                  49.65 |                  50.62 |
| TPC-DS Q93    |                 238.30 |                 237.87 |
| TPC-DS Q94    |                 124.71 |                 137.63 |
| TPC-DS Q95    |                2627.93 |                2605.66 |
| TPC-DS Q96    |                  93.53 |                  97.88 |
| TPC-DS Q97    |                 336.12 |                 332.55 |
| TPC-DS Q98    |                 131.58 |                 135.74 |
| TPC-DS Q99    |                 161.26 |                 164.67 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                      |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:---------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| postgresql-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
