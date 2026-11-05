## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 554s 
* Code: 1793782488
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by sidecar containers.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['ClickHouseCluster'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 16 CPU and 64Gi RAM. CPU limit is 16. RAM limit is 64Gi.

### Connections
* clickhousecluster-1-1-1-1-1 uses docker image clickhouse/clickhouse-server:26.8.34.13
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:793448
  * datadisk:153
  * volume_size:49G
  * volume_used:153M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:602227
    * datadisk:444
    * volume_size:49G
    * volume_used:444M
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:793448
    * datadisk:830
    * volume_size:49G
    * volume_used:830M
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:605346
    * datadisk:633
    * volume_size:49G
    * volume_used:633M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793782488
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1793782488-69dd989978-xbsqs: 0
* bx-w-clickhousecluster-nvme-tpcds-3-0: 0
* bx-w-clickhousecluster-nvme-tpcds-3-1: 0
* bx-w-clickhousecluster-nvme-tpcds-3-2: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |    3 |       50.00 |           7.00 |            1.00 |         31.00 |            2.00 |              8 |           0 |             | None           |             0 | False         |              216.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |        185 |            0.63 |            17782.07 |           5779.46 |          -1 | clickhousecluster-1-1-1-1-1 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |                  99 |        185 |            0.63 |            17782.07 |           5779.46 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| clickhousecluster-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   clickhousecluster-1-1-1-1-1 |
|:--------------|------------------------------:|
| TPC-DS Q1     |                        194.14 |
| TPC-DS Q2     |                        224.01 |
| TPC-DS Q3     |                        777.81 |
| TPC-DS Q4     |                      47363.72 |
| TPC-DS Q5     |                        515.27 |
| TPC-DS Q6     |                       1528.94 |
| TPC-DS Q7     |                        980.41 |
| TPC-DS Q8     |                        262.61 |
| TPC-DS Q9     |                        426.21 |
| TPC-DS Q10    |                       2001.50 |
| TPC-DS Q11    |                      11933.61 |
| TPC-DS Q12    |                        176.24 |
| TPC-DS Q13    |                        740.61 |
| TPC-DS Q14a+b |                       3912.35 |
| TPC-DS Q15    |                        216.40 |
| TPC-DS Q16    |                        326.33 |
| TPC-DS Q17    |                       1682.86 |
| TPC-DS Q18    |                       1085.19 |
| TPC-DS Q19    |                       2100.22 |
| TPC-DS Q20    |                        175.20 |
| TPC-DS Q21    |                        162.82 |
| TPC-DS Q22    |                        223.94 |
| TPC-DS Q23a+b |                       6624.36 |
| TPC-DS Q24a+b |                       2061.91 |
| TPC-DS Q25    |                       1737.64 |
| TPC-DS Q26    |                        763.98 |
| TPC-DS Q27    |                        806.66 |
| TPC-DS Q28    |                        385.67 |
| TPC-DS Q29    |                       1776.55 |
| TPC-DS Q30    |                        354.57 |
| TPC-DS Q31    |                       1384.93 |
| TPC-DS Q32    |                        175.47 |
| TPC-DS Q33    |                        225.24 |
| TPC-DS Q34    |                        123.77 |
| TPC-DS Q35    |                       1351.23 |
| TPC-DS Q36    |                        173.53 |
| TPC-DS Q37    |                       1947.52 |
| TPC-DS Q38    |                        623.56 |
| TPC-DS Q39a+b |                       1337.77 |
| TPC-DS Q40    |                        264.70 |
| TPC-DS Q41    |                         66.97 |
| TPC-DS Q42    |                        897.51 |
| TPC-DS Q43    |                        696.05 |
| TPC-DS Q44    |                         84.95 |
| TPC-DS Q45    |                        274.25 |
| TPC-DS Q46    |                        185.58 |
| TPC-DS Q47    |                       7704.11 |
| TPC-DS Q48    |                        656.17 |
| TPC-DS Q49    |                        342.47 |
| TPC-DS Q50    |                        551.57 |
| TPC-DS Q51    |                        438.20 |
| TPC-DS Q52    |                        853.32 |
| TPC-DS Q53    |                       1255.39 |
| TPC-DS Q54    |                        372.40 |
| TPC-DS Q55    |                        744.27 |
| TPC-DS Q56    |                        247.06 |
| TPC-DS Q57    |                       4298.12 |
| TPC-DS Q58    |                        306.27 |
| TPC-DS Q59    |                        483.67 |
| TPC-DS Q60    |                        302.65 |
| TPC-DS Q61    |                        401.03 |
| TPC-DS Q62    |                        134.73 |
| TPC-DS Q63    |                       1103.66 |
| TPC-DS Q64    |                       9721.62 |
| TPC-DS Q65    |                        644.84 |
| TPC-DS Q66    |                        604.82 |
| TPC-DS Q67    |                       1528.49 |
| TPC-DS Q68    |                        192.14 |
| TPC-DS Q69    |                       1665.21 |
| TPC-DS Q70    |                        373.10 |
| TPC-DS Q71    |                        354.96 |
| TPC-DS Q72    |                       8476.05 |
| TPC-DS Q73    |                        127.25 |
| TPC-DS Q74    |                       9988.71 |
| TPC-DS Q75    |                       1221.97 |
| TPC-DS Q76    |                        182.76 |
| TPC-DS Q77    |                        278.43 |
| TPC-DS Q78    |                       1145.74 |
| TPC-DS Q79    |                        175.50 |
| TPC-DS Q80    |                        706.44 |
| TPC-DS Q81    |                        289.70 |
| TPC-DS Q82    |                       1792.85 |
| TPC-DS Q83    |                        363.01 |
| TPC-DS Q84    |                        436.05 |
| TPC-DS Q85    |                       1757.49 |
| TPC-DS Q86    |                        105.58 |
| TPC-DS Q87    |                        654.51 |
| TPC-DS Q88    |                        901.63 |
| TPC-DS Q89    |                       1767.60 |
| TPC-DS Q90    |                        153.76 |
| TPC-DS Q91    |                        628.22 |
| TPC-DS Q92    |                        155.22 |
| TPC-DS Q93    |                        326.50 |
| TPC-DS Q94    |                        277.23 |
| TPC-DS Q95    |                       1746.25 |
| TPC-DS Q96    |                         91.87 |
| TPC-DS Q97    |                        356.07 |
| TPC-DS Q98    |                        178.71 |
| TPC-DS Q99    |                        155.95 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        22.87 |      0.36 |           0.51 |                  0.55 |

### Loading phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        95.81 |      1.29 |           1.54 |                  2.99 |

### Loading phase: component data generator

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                      | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|:-------------|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 | n/a          |         0 |           1.22 |                  3.42 |

### Benchmarking phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       275.58 |      2.30 |           3.41 |                  3.48 |

### Benchmarking phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       963.11 |      9.22 |           7.08 |                  9.01 |

### Benchmarking phase: component benchmarker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        23.06 |      0.10 |           0.36 |                  0.37 |

### Missing Monitoring Metrics
* Memory Usage, Working Set [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  1.68 |                      1.00 |                     0.00 |            543399.81 |                             32.27 |

#### Benchmarking phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  9.86 |                      5.00 |                     0.00 |          58005847.42 |                           1142.15 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
