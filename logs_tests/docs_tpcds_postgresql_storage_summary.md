## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1077s 
* Code: 1793872554
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:878780
  * datadisk:5790
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
    * code:1793872554
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:893631
  * datadisk:5790
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
    * code:1793872554

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1793872554-858cd4cb9b-4mm7t: 0
* bexhoma-sut-postgresql-1-1793872554-544fd7d6d9-qxb5g: 0

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
| PostgreSQL-1-1 |                1 |    1 |      104.00 |           2.00 |            0.00 |         56.00 |           37.00 |              8 |           0 |             | None           |             0 | False         |               34.62 | False               |
| PostgreSQL-1-2 |                2 |    1 |      104.00 |           2.00 |            0.00 |         56.00 |           37.00 |              8 |           0 |             | None           |             0 | False         |               34.62 | True                |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        204 |            0.36 |            10277.17 |           1747.06 |          -1 | postgresql-1-1-1-1-1 |
| postgresql-1-2-1-1-1 | PostgreSQL-1    | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        201 |            0.40 |             9279.48 |           1773.13 |          -1 | postgresql-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        204 |            0.36 |            10277.17 |           1747.06 |          -1 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        201 |            0.40 |             9279.48 |           1773.13 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-2-1-1-1 |
|:--------------|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  78.57 |                3406.38 |
| TPC-DS Q2     |                 343.67 |                1429.11 |
| TPC-DS Q3     |                 105.03 |                 678.32 |
| TPC-DS Q4     |                6250.10 |                7425.21 |
| TPC-DS Q5     |                 773.17 |                 670.86 |
| TPC-DS Q6     |               59432.00 |               62316.77 |
| TPC-DS Q7     |                 372.86 |                1061.78 |
| TPC-DS Q8     |                 101.85 |                  50.84 |
| TPC-DS Q9     |                2326.82 |                2210.19 |
| TPC-DS Q10    |                 906.38 |                6629.32 |
| TPC-DS Q11    |                4203.30 |                3632.85 |
| TPC-DS Q12    |                  56.20 |                  59.03 |
| TPC-DS Q13    |                 481.33 |                 514.34 |
| TPC-DS Q14a+b |                2268.85 |                2921.00 |
| TPC-DS Q15    |                 106.57 |                 106.00 |
| TPC-DS Q16    |                 204.20 |                 354.32 |
| TPC-DS Q17    |                 261.86 |                 302.60 |
| TPC-DS Q18    |                 327.07 |                 401.41 |
| TPC-DS Q19    |                 122.87 |                 136.34 |
| TPC-DS Q20    |                  81.05 |                  88.48 |
| TPC-DS Q21    |                 422.52 |                 686.87 |
| TPC-DS Q22    |                3896.81 |                3545.15 |
| TPC-DS Q23a+b |                4487.89 |                4258.04 |
| TPC-DS Q24a+b |                 468.85 |                 722.40 |
| TPC-DS Q25    |                 254.98 |                 271.84 |
| TPC-DS Q26    |                 241.10 |                 268.56 |
| TPC-DS Q27    |                 304.38 |                 343.93 |
| TPC-DS Q28    |                1491.02 |                2144.30 |
| TPC-DS Q29    |                 443.79 |                 313.62 |
| TPC-DS Q30    |                8306.46 |                8611.32 |
| TPC-DS Q31    |                1750.15 |                1613.82 |
| TPC-DS Q32    |                  99.04 |                 227.90 |
| TPC-DS Q33    |                 308.89 |                 335.38 |
| TPC-DS Q34    |                  18.83 |                  21.91 |
| TPC-DS Q35    |                1104.94 |                1025.50 |
| TPC-DS Q36    |                 267.51 |                 301.63 |
| TPC-DS Q37    |                 281.89 |                 274.07 |
| TPC-DS Q38    |                1358.88 |                 878.28 |
| TPC-DS Q39a+b |                2579.46 |                2661.56 |
| TPC-DS Q40    |                 104.47 |                 140.08 |
| TPC-DS Q41    |                 754.34 |                 808.10 |
| TPC-DS Q42    |                  93.63 |                  89.50 |
| TPC-DS Q43    |                  22.50 |                  22.36 |
| TPC-DS Q44    |                   2.77 |                   8.75 |
| TPC-DS Q45    |                  70.72 |                  75.08 |
| TPC-DS Q46    |                  34.52 |                  28.60 |
| TPC-DS Q47    |                2462.33 |                1331.88 |
| TPC-DS Q48    |                 462.23 |                 542.14 |
| TPC-DS Q49    |                 448.91 |                 661.17 |
| TPC-DS Q50    |                 320.75 |                 505.55 |
| TPC-DS Q51    |                 848.84 |                 794.29 |
| TPC-DS Q52    |                 105.73 |                  98.14 |
| TPC-DS Q53    |                 129.56 |                 135.33 |
| TPC-DS Q54    |                  67.44 |                  76.86 |
| TPC-DS Q55    |                  86.98 |                 100.41 |
| TPC-DS Q56    |                 273.24 |                 350.45 |
| TPC-DS Q57    |                 705.35 |                 779.87 |
| TPC-DS Q58    |                 320.41 |                 345.58 |
| TPC-DS Q59    |                 431.32 |                 463.86 |
| TPC-DS Q60    |                 313.83 |                 343.68 |
| TPC-DS Q61    |                 211.69 |                 137.23 |
| TPC-DS Q62    |                 157.56 |                 149.29 |
| TPC-DS Q63    |                 225.37 |                 166.36 |
| TPC-DS Q64    |                1247.39 |                 817.97 |
| TPC-DS Q65    |                 508.87 |                 552.27 |
| TPC-DS Q66    |                 154.69 |                 208.91 |
| TPC-DS Q67    |                2512.72 |                2991.78 |
| TPC-DS Q68    |                  38.77 |                  32.70 |
| TPC-DS Q69    |                 117.93 |                 131.43 |
| TPC-DS Q70    |                 362.42 |                 355.01 |
| TPC-DS Q71    |                 707.54 |                 263.71 |
| TPC-DS Q72    |                1304.07 |                 833.87 |
| TPC-DS Q73    |                  22.93 |                  22.17 |
| TPC-DS Q74    |                1141.86 |                1165.25 |
| TPC-DS Q75    |                 957.68 |                 633.99 |
| TPC-DS Q76    |                 223.04 |                 249.57 |
| TPC-DS Q77    |                 291.18 |                 275.68 |
| TPC-DS Q78    |                 909.38 |                1028.32 |
| TPC-DS Q79    |                 129.75 |                 153.13 |
| TPC-DS Q80    |                 420.74 |                 451.05 |
| TPC-DS Q81    |               41625.53 |               35871.32 |
| TPC-DS Q82    |                 424.15 |                 344.28 |
| TPC-DS Q83    |                  99.29 |                  69.86 |
| TPC-DS Q84    |                  77.34 |                  68.96 |
| TPC-DS Q85    |                 287.57 |                 256.54 |
| TPC-DS Q86    |                 162.28 |                 260.11 |
| TPC-DS Q87    |                1119.58 |                1077.82 |
| TPC-DS Q88    |                2194.86 |                2215.90 |
| TPC-DS Q89    |                 141.82 |                 103.70 |
| TPC-DS Q90    |                 101.84 |                  95.05 |
| TPC-DS Q91    |                 148.51 |                 118.98 |
| TPC-DS Q92    |                  95.70 |                  62.10 |
| TPC-DS Q93    |                 366.70 |                 248.83 |
| TPC-DS Q94    |                 150.15 |                 143.31 |
| TPC-DS Q95    |                2931.78 |                2713.11 |
| TPC-DS Q96    |                  90.43 |                  94.16 |
| TPC-DS Q97    |                 351.45 |                 348.42 |
| TPC-DS Q98    |                 165.27 |                 141.13 |
| TPC-DS Q99    |                 370.88 |                 230.47 |

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
