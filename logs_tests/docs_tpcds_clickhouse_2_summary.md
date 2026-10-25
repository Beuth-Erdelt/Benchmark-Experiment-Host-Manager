## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 639s 
* Code: 1792778136
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:958498
  * datadisk:172
  * volume_size:49G
  * volume_used:172M
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:64Gi
  * limits_cpu:16
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:958498
    * datadisk:225
    * volume_size:49G
    * volume_used:226M
    * cpu_list:0-223
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:472175
    * datadisk:354
    * volume_size:49G
    * volume_used:354M
    * cpu_list:0-127
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:350158
    * datadisk:291
    * volume_size:49G
    * volume_used:291M
    * cpu_list:0-127
  * resources_total: 64.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 16.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 48.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792778136
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-clickhousecluster-1-1792778136-7f679756c-cgn9c: 0
* bexhoma-worker-clickhousecluster-nvme-tpcds-1-0: 0
* bexhoma-worker-clickhousecluster-nvme-tpcds-1-1: 0
* bexhoma-worker-clickhousecluster-nvme-tpcds-1-2: 0

### Workflow

#### Actual

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS ClickHouseCluster-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                       |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| ClickHouseCluster-1-1 |                1 |    1 |       53.00 |          16.00 |            1.00 |         14.00 |            5.00 |              8 |           0 |             | None           |             0 | False         |               67.92 | False               |

### Benchmarking

#### Per Connection

| DBMS                        | configuration       | phase                   | job                       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                         |
|:----------------------------|:--------------------|:------------------------|:--------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------------------|
| clickhousecluster-1-1-1-1-1 | ClickHouseCluster-1 | clickhousecluster-1-1-1 | clickhousecluster-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        112 |            0.43 |             8535.91 |           3182.14 |          -1 | clickhousecluster-1-1-1-1-1 |

#### Per Phase

|                         | phase                   |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------------------|:------------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| clickhousecluster-1-1-1 | clickhousecluster-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        112 |            0.43 |             8535.91 |           3182.14 |          -1 |

#### Query Completion per Phase

| phase                   |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:------------------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| clickhousecluster-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   clickhousecluster-1-1-1-1-1 |
|:--------------|------------------------------:|
| TPC-DS Q1     |                        203.56 |
| TPC-DS Q2     |                       2233.75 |
| TPC-DS Q3     |                        378.04 |
| TPC-DS Q4     |                      16257.28 |
| TPC-DS Q5     |                        277.68 |
| TPC-DS Q6     |                        645.06 |
| TPC-DS Q7     |                        754.81 |
| TPC-DS Q8     |                        226.60 |
| TPC-DS Q9     |                        317.15 |
| TPC-DS Q10    |                       1731.29 |
| TPC-DS Q11    |                       4922.21 |
| TPC-DS Q12    |                        119.16 |
| TPC-DS Q13    |                        698.35 |
| TPC-DS Q14a+b |                       8152.53 |
| TPC-DS Q15    |                        178.21 |
| TPC-DS Q16    |                        235.85 |
| TPC-DS Q17    |                        800.89 |
| TPC-DS Q18    |                       1054.75 |
| TPC-DS Q19    |                        775.05 |
| TPC-DS Q20    |                        146.58 |
| TPC-DS Q21    |                        123.49 |
| TPC-DS Q22    |                        180.00 |
| TPC-DS Q23a+b |                       2538.06 |
| TPC-DS Q24a+b |                       1157.43 |
| TPC-DS Q25    |                        791.71 |
| TPC-DS Q26    |                        782.09 |
| TPC-DS Q27    |                        650.71 |
| TPC-DS Q28    |                        219.04 |
| TPC-DS Q29    |                        738.53 |
| TPC-DS Q30    |                        293.03 |
| TPC-DS Q31    |                       1035.12 |
| TPC-DS Q32    |                        163.49 |
| TPC-DS Q33    |                        215.84 |
| TPC-DS Q34    |                        120.47 |
| TPC-DS Q35    |                       1156.79 |
| TPC-DS Q36    |                         94.13 |
| TPC-DS Q37    |                        891.66 |
| TPC-DS Q38    |                        377.54 |
| TPC-DS Q39a+b |                       1007.35 |
| TPC-DS Q40    |                        180.36 |
| TPC-DS Q41    |                         60.94 |
| TPC-DS Q42    |                        312.53 |
| TPC-DS Q43    |                        282.64 |
| TPC-DS Q44    |                         64.33 |
| TPC-DS Q45    |                        188.30 |
| TPC-DS Q46    |                        152.83 |
| TPC-DS Q47    |                       2686.37 |
| TPC-DS Q48    |                        560.90 |
| TPC-DS Q49    |                        225.97 |
| TPC-DS Q50    |                        285.70 |
| TPC-DS Q51    |                        320.33 |
| TPC-DS Q52    |                        362.30 |
| TPC-DS Q53    |                        464.61 |
| TPC-DS Q54    |                        241.39 |
| TPC-DS Q55    |                        334.75 |
| TPC-DS Q56    |                        200.84 |
| TPC-DS Q57    |                       1538.44 |
| TPC-DS Q58    |                        272.91 |
| TPC-DS Q59    |                        318.00 |
| TPC-DS Q60    |                        200.77 |
| TPC-DS Q61    |                        310.68 |
| TPC-DS Q62    |                        128.23 |
| TPC-DS Q63    |                        505.89 |
| TPC-DS Q64    |                       6879.08 |
| TPC-DS Q65    |                        410.44 |
| TPC-DS Q66    |                        532.38 |
| TPC-DS Q67    |                        553.10 |
| TPC-DS Q68    |                        173.22 |
| TPC-DS Q69    |                       1531.05 |
| TPC-DS Q70    |                        247.91 |
| TPC-DS Q71    |                        242.08 |
| TPC-DS Q72    |                       5149.27 |
| TPC-DS Q73    |                        126.50 |
| TPC-DS Q74    |                       3982.77 |
| TPC-DS Q75    |                        721.56 |
| TPC-DS Q76    |                        139.54 |
| TPC-DS Q77    |                        289.41 |
| TPC-DS Q78    |                        701.44 |
| TPC-DS Q79    |                        182.54 |
| TPC-DS Q80    |                        439.49 |
| TPC-DS Q81    |                        243.04 |
| TPC-DS Q82    |                        912.08 |
| TPC-DS Q83    |                        339.73 |
| TPC-DS Q84    |                        343.09 |
| TPC-DS Q85    |                       1657.09 |
| TPC-DS Q86    |                        108.40 |
| TPC-DS Q87    |                        375.06 |
| TPC-DS Q88    |                        787.69 |
| TPC-DS Q89    |                        498.33 |
| TPC-DS Q90    |                        146.02 |
| TPC-DS Q91    |                        528.01 |
| TPC-DS Q92    |                        143.65 |
| TPC-DS Q93    |                        161.73 |
| TPC-DS Q94    |                        230.09 |
| TPC-DS Q95    |                       1005.21 |
| TPC-DS Q96    |                         88.72 |
| TPC-DS Q97    |                        276.92 |
| TPC-DS Q98    |                        143.64 |
| TPC-DS Q99    |                        127.26 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        24.03 |      0.18 |           0.41 |                  0.47 |

### Loading phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       116.13 |      0.81 |           1.72 |                  2.11 |

### Loading phase: component data generator

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |         1.36 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |         0.65 |      0.00 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       101.11 |      1.38 |           1.10 |                  1.20 |

### Benchmarking phase: component worker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |       534.47 |      6.21 |           5.41 |                  6.40 |

### Benchmarking phase: component benchmarker

| DBMS                      |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------------|-------------:|----------:|---------------:|----------------------:|
| clickhousecluster-1-1-1-1 |        23.25 |      0.14 |           0.34 |                  0.34 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log)
* CPU Throttled Time [s] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection clickhousecluster-1-1-1-1 (bexhoma-metrics-clickhousecluster-1-1-1-1-loader.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                  1.68 |                      1.00 |                     0.00 |            228768.26 |                             12.64 |

#### Benchmarking phase: component worker

| DBMS                      |   Queries [queries/s] |   Running Queries [count] |   Failed Queries [count] |   Rows Read [rows/s] |   Data Read, uncompressed [MiB/s] |
|:--------------------------|----------------------:|--------------------------:|-------------------------:|---------------------:|----------------------------------:|
| clickhousecluster-1-1-1-1 |                 10.31 |                      2.00 |                     0.00 |          23900254.22 |                            480.73 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
