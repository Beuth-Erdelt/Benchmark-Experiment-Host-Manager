## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1076s 
* Code: 1794608769
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
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
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
  * disk:1123941
  * datadisk:5787
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
    * code:1794608769
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1129408
  * datadisk:5787
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
    * code:1794608769

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* PostgreSQL-1: 39 of 39 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794608769-5d57dd5db-qrfdc: 0
* bexhoma-sut-postgresql-1-1794608769-f6f56fff6-snlzr: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       97.00 |           5.00 |            0.00 |         42.00 |           38.00 |              8 |         0 |             | None           |             0 | False         |               37.11 | False               |
| PostgreSQL-1-2 |                2 |    1 |       97.00 |           5.00 |            0.00 |         42.00 |           38.00 |              8 |         0 |             | None           |             0 | False         |               37.11 | True                |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        168 |            0.31 |            11740.21 |           2121.43 |          -1 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               99 |                  99 |        163 |            0.32 |            11739.08 |           2186.50 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        168 |            0.31 |            11740.21 |           2121.43 |          -1 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        163 |            0.32 |            11739.08 |           2186.50 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-2-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   postgresql-1-1-1-1-1 |   postgresql-1-2-1-1-1 |
|:--------------|-----------------------:|-----------------------:|
| TPC-DS Q1     |                 253.34 |                 173.00 |
| TPC-DS Q2     |                 340.78 |                 418.77 |
| TPC-DS Q3     |                 102.24 |                 222.96 |
| TPC-DS Q4     |                5436.24 |                5564.68 |
| TPC-DS Q5     |                 451.50 |                 490.61 |
| TPC-DS Q6     |               50569.19 |               49048.67 |
| TPC-DS Q7     |                 304.80 |                 365.77 |
| TPC-DS Q8     |                  46.36 |                  70.60 |
| TPC-DS Q9     |                1904.54 |                1948.43 |
| TPC-DS Q10    |                 879.24 |                2344.49 |
| TPC-DS Q11    |                3303.65 |                4154.22 |
| TPC-DS Q12    |                  54.87 |                  52.33 |
| TPC-DS Q13    |                 488.00 |                 504.59 |
| TPC-DS Q14a+b |                2219.71 |                2276.03 |
| TPC-DS Q15    |                  97.31 |                 100.94 |
| TPC-DS Q16    |                 199.70 |                 203.42 |
| TPC-DS Q17    |                 274.51 |                 268.03 |
| TPC-DS Q18    |                 346.46 |                 335.66 |
| TPC-DS Q19    |                 126.51 |                 124.95 |
| TPC-DS Q20    |                  96.86 |                  84.46 |
| TPC-DS Q21    |                 239.16 |                 316.90 |
| TPC-DS Q22    |                2680.32 |                2888.61 |
| TPC-DS Q23a+b |                3259.05 |                3160.03 |
| TPC-DS Q24a+b |                 568.04 |                 564.32 |
| TPC-DS Q25    |                 256.41 |                 250.42 |
| TPC-DS Q26    |                 205.15 |                 192.61 |
| TPC-DS Q27    |                 326.84 |                 322.98 |
| TPC-DS Q28    |                1358.29 |                1329.16 |
| TPC-DS Q29    |                 274.49 |                 265.34 |
| TPC-DS Q30    |                7542.38 |                7648.03 |
| TPC-DS Q31    |                1350.10 |                1298.30 |
| TPC-DS Q32    |                 142.44 |                 158.25 |
| TPC-DS Q33    |                 319.48 |                 327.79 |
| TPC-DS Q34    |                  22.28 |                  21.68 |
| TPC-DS Q35    |                 965.95 |                 957.78 |
| TPC-DS Q36    |                 264.10 |                 264.45 |
| TPC-DS Q37    |                 328.87 |                 329.63 |
| TPC-DS Q38    |                 780.27 |                 789.30 |
| TPC-DS Q39a+b |                2087.37 |                2110.59 |
| TPC-DS Q40    |                 100.60 |                  99.11 |
| TPC-DS Q41    |                 336.16 |                 344.43 |
| TPC-DS Q42    |                  87.27 |                  84.73 |
| TPC-DS Q43    |                  20.74 |                  19.08 |
| TPC-DS Q44    |                   2.87 |                   4.92 |
| TPC-DS Q45    |                  80.13 |                  75.30 |
| TPC-DS Q46    |                  27.97 |                  28.59 |
| TPC-DS Q47    |                1224.19 |                1466.62 |
| TPC-DS Q48    |                 476.19 |                 475.64 |
| TPC-DS Q49    |                 454.94 |                 421.14 |
| TPC-DS Q50    |                 568.69 |                 365.78 |
| TPC-DS Q51    |                 708.75 |                 695.38 |
| TPC-DS Q52    |                  88.97 |                  89.85 |
| TPC-DS Q53    |                 110.45 |                 107.55 |
| TPC-DS Q54    |                  70.60 |                  64.78 |
| TPC-DS Q55    |                  86.31 |                  80.32 |
| TPC-DS Q56    |                 334.24 |                 301.61 |
| TPC-DS Q57    |                 697.07 |                 646.43 |
| TPC-DS Q58    |                 315.35 |                 332.89 |
| TPC-DS Q59    |                 418.49 |                 410.36 |
| TPC-DS Q60    |                 306.93 |                 295.25 |
| TPC-DS Q61    |                 107.81 |                 103.39 |
| TPC-DS Q62    |                  93.03 |                  93.32 |
| TPC-DS Q63    |                 113.14 |                 105.20 |
| TPC-DS Q64    |                 594.74 |                 587.50 |
| TPC-DS Q65    |                 510.95 |                 503.08 |
| TPC-DS Q66    |                 164.48 |                 172.07 |
| TPC-DS Q67    |                2622.65 |                2521.80 |
| TPC-DS Q68    |                  31.98 |                  29.08 |
| TPC-DS Q69    |                 306.46 |                 277.81 |
| TPC-DS Q70    |                 358.49 |                 427.81 |
| TPC-DS Q71    |                 268.81 |                 259.15 |
| TPC-DS Q72    |                1017.04 |                 749.64 |
| TPC-DS Q73    |                  21.87 |                  21.48 |
| TPC-DS Q74    |                 838.27 |                 772.91 |
| TPC-DS Q75    |                 625.89 |                 548.76 |
| TPC-DS Q76    |                 141.54 |                 125.52 |
| TPC-DS Q77    |                 291.96 |                 269.04 |
| TPC-DS Q78    |                1075.08 |                 933.02 |
| TPC-DS Q79    |                 166.19 |                 164.19 |
| TPC-DS Q80    |                 383.00 |                 349.12 |
| TPC-DS Q81    |               33398.43 |               32803.41 |
| TPC-DS Q82    |                 566.23 |                 351.76 |
| TPC-DS Q83    |                  73.45 |                  63.92 |
| TPC-DS Q84    |                  21.13 |                  17.67 |
| TPC-DS Q85    |                 260.28 |                 263.00 |
| TPC-DS Q86    |                 155.95 |                 169.91 |
| TPC-DS Q87    |                 832.71 |                 786.34 |
| TPC-DS Q88    |                2036.86 |                2055.24 |
| TPC-DS Q89    |                 131.43 |                 126.28 |
| TPC-DS Q90    |                 111.93 |                  93.28 |
| TPC-DS Q91    |                  90.73 |                  85.02 |
| TPC-DS Q92    |                  53.88 |                  47.00 |
| TPC-DS Q93    |                 272.54 |                 197.59 |
| TPC-DS Q94    |                 134.41 |                 126.92 |
| TPC-DS Q95    |                2518.15 |                2507.61 |
| TPC-DS Q96    |                 101.37 |                  95.76 |
| TPC-DS Q97    |                 340.42 |                 325.32 |
| TPC-DS Q98    |                 144.33 |                 250.61 |
| TPC-DS Q99    |                 164.64 |                 162.04 |

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
