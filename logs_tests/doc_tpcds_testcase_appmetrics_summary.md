## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 3505s 
* Code: 1773476529
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker14.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-BHT-8-1-1 uses docker image postgres:18.3
  * RAM:541008474112
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:5.15.0-164-generic
  * node:cl-worker14
  * disk:162906
  * cpu_list:0-63
  * args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'effective_io_concurrency=64', '-c', 'io_method=worker', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1773476529

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Latency of Timer Execution [ms]
| DBMS          |   PostgreSQL-BHT-8-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 431.48 |
| TPC-DS Q2     |                1809.93 |
| TPC-DS Q3     |                1192.46 |
| TPC-DS Q4     |               47140.5  |
| TPC-DS Q5     |                2721.35 |
| TPC-DS Q6     |              744388    |
| TPC-DS Q7     |                1816.06 |
| TPC-DS Q8     |                 745.72 |
| TPC-DS Q9     |                8052.96 |
| TPC-DS Q10    |                3360.02 |
| TPC-DS Q11    |               26695.3  |
| TPC-DS Q12    |                 414.74 |
| TPC-DS Q13    |                4006.61 |
| TPC-DS Q14a+b |               20319.1  |
| TPC-DS Q15    |                 842.54 |
| TPC-DS Q16    |                1275.1  |
| TPC-DS Q17    |                2049.1  |
| TPC-DS Q18    |                1960.9  |
| TPC-DS Q19    |                1177.36 |
| TPC-DS Q20    |                 738.85 |
| TPC-DS Q21    |                1064.61 |
| TPC-DS Q22    |               23817.7  |
| TPC-DS Q23a+b |               27624.3  |
| TPC-DS Q24a+b |                4108.64 |
| TPC-DS Q25    |                1985.79 |
| TPC-DS Q26    |                1405.8  |
| TPC-DS Q27    |                 118.29 |
| TPC-DS Q28    |                6132.13 |
| TPC-DS Q29    |                2345.22 |
| TPC-DS Q30    |              218284    |
| TPC-DS Q31    |               12086.6  |
| TPC-DS Q32    |                 805.89 |
| TPC-DS Q33    |                2179.55 |
| TPC-DS Q34    |                 102.06 |
| TPC-DS Q35    |                3919.19 |
| TPC-DS Q36    |                 107.69 |
| TPC-DS Q37    |                1086.69 |
| TPC-DS Q38    |                8373.61 |
| TPC-DS Q39a+b |               13855.1  |
| TPC-DS Q40    |                 699.13 |
| TPC-DS Q41    |                1175.42 |
| TPC-DS Q42    |                 527.42 |
| TPC-DS Q43    |                 153.13 |
| TPC-DS Q44    |                1613.14 |
| TPC-DS Q45    |                 502.49 |
| TPC-DS Q46    |                 170.07 |
| TPC-DS Q47    |               11849.4  |
| TPC-DS Q48    |                3743.14 |
| TPC-DS Q49    |                3665.53 |
| TPC-DS Q50    |                3791.37 |
| TPC-DS Q51    |                7321.6  |
| TPC-DS Q52    |                 527.65 |
| TPC-DS Q53    |                 688.64 |
| TPC-DS Q54    |                1512.05 |
| TPC-DS Q55    |                 514.78 |
| TPC-DS Q56    |                2311.74 |
| TPC-DS Q57    |                6522.51 |
| TPC-DS Q58    |                2336.14 |
| TPC-DS Q59    |                2653.46 |
| TPC-DS Q60    |                2690.35 |
| TPC-DS Q61    |                 338.49 |
| TPC-DS Q62    |                 588.64 |
| TPC-DS Q63    |                 624.02 |
| TPC-DS Q64    |                2820.97 |
| TPC-DS Q65    |                3969.52 |
| TPC-DS Q66    |                1818.87 |
| TPC-DS Q67    |               25929.2  |
| TPC-DS Q68    |                 172.36 |
| TPC-DS Q69    |                1155.62 |
| TPC-DS Q70    |                2666.99 |
| TPC-DS Q71    |                2333.16 |
| TPC-DS Q72    |                6635.73 |
| TPC-DS Q73    |                  99.87 |
| TPC-DS Q74    |                6957.67 |
| TPC-DS Q75    |                9929.31 |
| TPC-DS Q76    |                1083.05 |
| TPC-DS Q77    |                1373.71 |
| TPC-DS Q78    |               11992.2  |
| TPC-DS Q79    |                1050.4  |
| TPC-DS Q80    |                2192.85 |
| TPC-DS Q81    |              959109    |
| TPC-DS Q82    |                1421.3  |
| TPC-DS Q83    |                 451.99 |
| TPC-DS Q84    |                  77.46 |
| TPC-DS Q85    |                 947.48 |
| TPC-DS Q86    |                1478.15 |
| TPC-DS Q87    |                8705.83 |
| TPC-DS Q88    |                7779.7  |
| TPC-DS Q89    |                 668.97 |
| TPC-DS Q90    |                1044.16 |
| TPC-DS Q91    |                 471.11 |
| TPC-DS Q92    |                 493.26 |
| TPC-DS Q93    |                1299.33 |
| TPC-DS Q94    |                1040.82 |
| TPC-DS Q95    |               24829.8  |
| TPC-DS Q96    |                 531.04 |
| TPC-DS Q97    |                2407.08 |
| TPC-DS Q98    |                1179.47 |
| TPC-DS Q99    |                 912.51 |

### Loading [s]

| DBMS                 |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:---------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-8-1-1 |              0 |             371 |            3 |         790 |       1170 |

### Geometric Mean of Medians of Timer Run [s]

| DBMS                 |   Geo Times [s] |
|:---------------------|----------------:|
| PostgreSQL-BHT-8-1-1 |            2.11 |

### Power@Size ((3600*SF)/(geo times))

| DBMS                 |   Power@Size [~Q/h] |
|:---------------------|--------------------:|
| PostgreSQL-BHT-8-1-1 |             5159.26 |

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))

| DBMS               |   time [s] |   count |   SF |   Throughput@Size |
|:-------------------|-----------:|--------:|-----:|------------------:|
| PostgreSQL-BHT-8-1 |       2374 |       1 |    3 |            450.38 |

### Workflow

| DBMS                 | orig_name          |   SF |   pods |   num_experiment |   num_client |   benchmark_start |   benchmark_end |
|:---------------------|:-------------------|-----:|-------:|-----------------:|-------------:|------------------:|----------------:|
| PostgreSQL-BHT-8-1-1 | PostgreSQL-BHT-8-1 |    3 |      8 |                1 |            1 |        1773477562 |      1773479936 |

#### Actual

* DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned

* DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-8-1 |       824.83 |      2.22 |          11.67 |                 18.38 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-8-1 |            0 |         0 |              0 |                     0 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-8-1 |        31.93 |      0.27 |           0.01 |                  2.65 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-8-1 |      2904.13 |      2.39 |           12.4 |                 19.11 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-BHT-8-1 |        20.75 |      0.03 |           0.33 |                  0.33 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-8-1 |                         1 |                                        0 |                                                0 |                           9 |                                       8 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-BHT-8-1 |                         2 |                                        0 |                                                0 |                           9 |                                       8 |

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
