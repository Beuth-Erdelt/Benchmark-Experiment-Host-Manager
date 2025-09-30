# Example: Application Metrics

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

In the following we demonstrate how to collect application metrics, that is, metrics of a DBMS.


## Perform Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

## PostgreSQL

### Benchbase's TPC-C

Example:
```bash
nohup python benchbase.py -m -mc -ma -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_postgresql_appmetrics.log &
```

This
* activates monitoring (`-m`) cluster-wide (`-mc`)
* starts a clean instance of PostgreSQL (`-dbms`)
  * with a sidecar container for monitoring (`-ma`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-sd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-tb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Evaluate Results


doc_benchbase_run_postgresql_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1274s 
    Code: 1758633612
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:440088376
    datadisk:4307
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758633612
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:440766148
    datadisk:4969
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758633612

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1        160   16384       1      1  300.0           3                   1969.699193                1951.909200         0.0                                                     279561.0                                              81186.0
PostgreSQL-1-1-1024-2-2               1         80    8192       2      1  300.0           1                    903.579693                 895.726362         0.0                                                     316165.0                                              88501.0
PostgreSQL-1-1-1024-2-1               1         80    8192       2      2  300.0           1                    903.306563                 895.543231         0.0                                                     316789.0                                              88526.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1        160   16384          1  300.0           3                       1969.70                    1951.91         0.0                                                     279561.0                                              81186.0
PostgreSQL-1-1-1024-2               1        160   16384          2  300.0           2                       1806.89                    1791.27         0.0                                                     316789.0                                              88513.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      304.0        1.0   1.0         189.473684
PostgreSQL-1-1-1024-2      304.0        1.0   2.0         189.473684

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       636.7     4.38          8.06                 9.67
PostgreSQL-1-1-1024-2       636.7     4.38          8.06                 9.67

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      930.28     5.64          0.26                 0.26
PostgreSQL-1-1-1024-2      930.28     5.64          0.26                 0.26

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     2563.32     8.96         10.23                12.45
PostgreSQL-1-1-1024-2     2113.64     8.20         10.81                13.49

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1129.76     4.67          1.17                 1.17
PostgreSQL-1-1-1024-2     1129.76     6.64          1.17                 1.17

### Application Metrics
                       Active Backends Waiting on I/O  Active Backends Waiting on WAL  Active Backends Waiting on Locks  Max Transaction Duration (I/O Wait)  Max Transaction Duration (WAL Wait)
PostgreSQL-1-1-1024-1                             2.0                            42.0                             123.0                                 0.15                                 1.23
PostgreSQL-1-1-1024-2                             1.0                            48.0                             124.0                                 0.27                                 0.94

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

The summary shows the first 5 application metrics aggregated per execution run.
An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/dev).



### HammerDB's TPC-C

Example:
```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_appmetrics.log &
```

doc_hammerdb_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1399s 
    Code: 1758999982
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [16] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:439060008
    datadisk:3281
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758999982
PostgreSQL-BHT-16-1-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:439983052
    datadisk:4183
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758999982

### Execution
                       experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1      16       1          1     33.72     51.10         0.0  14403.0  33264.0         5       0
PostgreSQL-BHT-16-1-2               1      16       2          2     68.47    117.84         0.0   8840.0  20704.5         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       84.0        1.0   1.0                 685.714286
PostgreSQL-BHT-16-1-2       84.0        1.0   2.0                 685.714286

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       127.7     1.16          7.63                 8.32
PostgreSQL-BHT-16-1-2       127.7     1.16          7.63                 8.32

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      330.51     5.82          0.15                 0.15
PostgreSQL-BHT-16-1-2      330.51     5.82          0.15                 0.15

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      301.04     1.16          8.23                 9.07
PostgreSQL-BHT-16-1-2      237.55     0.91          8.55                 9.52

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       76.57     0.17          0.16                 0.16
PostgreSQL-BHT-16-1-2       76.57     0.39          0.16                 0.16

### Application Metrics
                       Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-BHT-16-1-1                      8.0                                     0.0                                             0.0                       16.0                                    0.0
PostgreSQL-BHT-16-1-2                      4.0                                     0.0                                             0.0                       16.0                                    0.0

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```


### TPC-H

Example:
```bash
nohup python tpch.py -ms 1 -dt -tr -lr 64Gi \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_appmetrics.log &
```

doc_tpch_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 778s 
    Code: 1759052328
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:435703624
    datadisk:8186
    volume_size:30G
    volume_used:8.0G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1759052328

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 5967.70
Minimum Cost Supplier Query (TPC-H Q2)                            1454.78
Shipping Priority (TPC-H Q3)                                      1585.57
Order Priority Checking Query (TPC-H Q4)                           785.76
Local Supplier Volume (TPC-H Q5)                                  1530.92
Forecasting Revenue Change (TPC-H Q6)                             1032.65
Forecasting Revenue Change (TPC-H Q7)                             1833.38
National Market Share (TPC-H Q8)                                  1046.70
Product Type Profit Measure (TPC-H Q9)                            2624.27
Forecasting Revenue Change (TPC-H Q10)                            3623.58
Important Stock Identification (TPC-H Q11)                         560.87
Shipping Modes and Order Priority (TPC-H Q12)                     1781.32
Customer Distribution (TPC-H Q13)                                 6646.51
Forecasting Revenue Change (TPC-H Q14)                            1710.70
Top Supplier Query (TPC-H Q15)                                    1265.26
Parts/Supplier Relationship (TPC-H Q16)                           1312.32
Small-Quantity-Order Revenue (TPC-H Q17)                          5702.20
Large Volume Customer (TPC-H Q18)                                15935.12
Discounted Revenue (TPC-H Q19)                                     267.17
Potential Part Promotion (TPC-H Q20)                               875.76
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               1728.79
Global Sales Opportunity Query (TPC-H Q22)                         441.84

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1          19.0          117.0         2.0      413.0     554.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           1.73

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            6412.73

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1 3.0 1              1                 66      1  3.0           3600.0

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  3.0     8               1           1       1759052956     1759053022

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      364.92     1.57         10.82                15.73

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       28.16     0.49           0.0                  0.0

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      146.82     2.21         10.78                15.58

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       12.43        0          0.24                 0.24

### Application Metrics
                    Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-BHT-8-1                      0.0                                     0.0                                             0.0                        5.0                                    5.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```


### TPC-DS

Example:
```bash
nohup python tpcds.py -ms 1 -dt -tr -lr 64Gi \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_appmetrics.log &
```

doc_tpcds_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 3902s 
    Code: 1758995122
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:435700240
    datadisk:14253
    volume_size:30G
    volume_used:14G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1758995122

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-8-1-1
TPC-DS Q1                    618.66
TPC-DS Q2                   2035.03
TPC-DS Q3                   1492.07
TPC-DS Q4                  52140.16
TPC-DS Q5                   3001.64
TPC-DS Q6                 965160.21
TPC-DS Q7                   2051.94
TPC-DS Q8                    299.36
TPC-DS Q9                   7999.82
TPC-DS Q10                  3445.52
TPC-DS Q11                 29070.17
TPC-DS Q12                   462.60
TPC-DS Q13                  4184.03
TPC-DS Q14a+b              23108.22
TPC-DS Q15                   950.03
TPC-DS Q16                  1356.62
TPC-DS Q17                  2261.66
TPC-DS Q18                  2096.28
TPC-DS Q19                  1295.38
TPC-DS Q20                   827.16
TPC-DS Q21                  1311.17
TPC-DS Q22                 23952.88
TPC-DS Q23a+b              30108.19
TPC-DS Q24a+b               3392.01
TPC-DS Q25                  2211.39
TPC-DS Q26                  1720.96
TPC-DS Q27                   123.81
TPC-DS Q28                  6304.16
TPC-DS Q29                  2532.56
TPC-DS Q30                266038.74
TPC-DS Q31                 13597.25
TPC-DS Q32                  1832.35
TPC-DS Q33                  2492.78
TPC-DS Q34                   103.06
TPC-DS Q35                  4084.66
TPC-DS Q36                   110.09
TPC-DS Q37                  1532.80
TPC-DS Q38                  6716.45
TPC-DS Q39a+b              13989.94
TPC-DS Q40                   797.38
TPC-DS Q41                 13618.33
TPC-DS Q42                   580.20
TPC-DS Q43                   156.88
TPC-DS Q44                   158.31
TPC-DS Q45                   560.21
TPC-DS Q46                   181.99
TPC-DS Q47                  8831.48
TPC-DS Q48                  3939.75
TPC-DS Q49                  3849.45
TPC-DS Q50                  3959.03
TPC-DS Q51                  7111.18
TPC-DS Q52                   583.72
TPC-DS Q53                   744.80
TPC-DS Q54                   193.89
TPC-DS Q55                   568.41
TPC-DS Q56                  2529.80
TPC-DS Q57                  6510.40
TPC-DS Q58                  2777.87
TPC-DS Q59                  2918.52
TPC-DS Q60                  2962.51
TPC-DS Q61                  3017.30
TPC-DS Q62                   630.13
TPC-DS Q63                   699.14
TPC-DS Q64                  3007.18
TPC-DS Q65                  4148.53
TPC-DS Q66                  1948.54
TPC-DS Q67                 21655.93
TPC-DS Q68                   187.76
TPC-DS Q69                   656.63
TPC-DS Q70                  2773.45
TPC-DS Q71                  2623.84
TPC-DS Q72                  8153.58
TPC-DS Q73                   102.77
TPC-DS Q74                  7491.15
TPC-DS Q75                 10701.00
TPC-DS Q76                  1140.96
TPC-DS Q77                  5361.28
TPC-DS Q78                 13058.95
TPC-DS Q79                   710.18
TPC-DS Q80                  2500.01
TPC-DS Q81               1138970.73
TPC-DS Q82                  1563.29
TPC-DS Q83                   519.79
TPC-DS Q84                   291.10
TPC-DS Q85                  1356.71
TPC-DS Q86                  1518.81
TPC-DS Q87                  6768.65
TPC-DS Q88                  8051.99
TPC-DS Q89                   820.65
TPC-DS Q90                  2031.66
TPC-DS Q91                   684.55
TPC-DS Q92                   462.21
TPC-DS Q93                  1377.14
TPC-DS Q94                  1091.13
TPC-DS Q95                 26062.51
TPC-DS Q96                   584.30
TPC-DS Q97                  2549.77
TPC-DS Q98                  1309.40
TPC-DS Q99                   978.96

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          377.0         2.0      727.0    1114.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           2.33

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4680.78

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1 3.0 1              1               2857      1  3.0           374.24

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  3.0     8               1           1       1758996090     1758998947

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      854.07     2.27         12.57                 16.0

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        12.5     0.07           0.0                  0.0

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1     3563.56     2.54         13.37                15.81

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       26.22      0.2          0.25                 0.26

### Application Metrics
                    Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-BHT-8-1                      0.0                                     0.0                                             0.0                        6.0                                    6.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```



### YCSB

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_appmetrics.log &
```

doc_ycsb_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=3
    Type: ycsb
    Duration: 8579s 
    Code: 1759053161
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 3000000.
    Ordering of inserts is hashed.
    Number of operations is 3000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [2, 3].
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:442966724
    datadisk:7093
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1759053161
PostgreSQL-64-8-65536-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:444795004
    datadisk:8879
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1759053161
PostgreSQL-64-8-65536-3 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:445820828
    datadisk:9880
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1759053161
PostgreSQL-64-8-65536-4 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:446703628
    datadisk:10742
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1759053161

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8           0                    3390.547889               884853.0             3000000                             45703.0

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   32768          1           0                        2310.03              1298685.0           1500284                             832.0             1499716                            990207.0
PostgreSQL-64-8-65536-2               1       64   32768          8           0                        1319.17              2282672.0           1500726                             843.0             1499274                           1897471.0
PostgreSQL-64-8-65536-3               1       64   49152          1           0                        1923.59              1559582.0           1498778                             783.0             1501222                           1180671.0
PostgreSQL-64-8-65536-4               1       64   49152          8           0                        1597.60              1882872.0           1498843                             823.0             1501157                           1514495.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[1, 8, 1, 8]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[1, 8, 1, 8]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1007.43      1.4         10.41                12.08
PostgreSQL-64-8-65536-2     1007.43      1.4         10.41                12.08
PostgreSQL-64-8-65536-3     1007.43      1.4         10.41                12.08
PostgreSQL-64-8-65536-4     1007.43      1.4         10.41                12.08

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      632.78     0.73          0.11                 0.11
PostgreSQL-64-8-65536-2      632.78     0.73          0.11                 0.11
PostgreSQL-64-8-65536-3      632.78     0.73          0.11                 0.11
PostgreSQL-64-8-65536-4      632.78     0.73          0.11                 0.11

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      941.31     0.96         11.46                13.99
PostgreSQL-64-8-65536-2      896.63     0.86         11.90                14.84
PostgreSQL-64-8-65536-3      903.22     0.89         12.32                15.63
PostgreSQL-64-8-65536-4      908.05     0.90         12.69                16.00

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      442.01     0.57          0.13                 0.13
PostgreSQL-64-8-65536-2      466.62     0.45          0.12                 0.12
PostgreSQL-64-8-65536-3      475.49     0.99          0.13                 0.13
PostgreSQL-64-8-65536-4      446.18     0.51          0.12                 0.13

### Application Metrics
                         Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-64-8-65536-1                     29.0                                     0.0                                             0.0                       64.0                                   64.0
PostgreSQL-64-8-65536-2                      6.0                                     0.0                                             0.0                       64.0                                   64.0
PostgreSQL-64-8-65536-3                     18.0                                     0.0                                             0.0                       65.0                                   64.0
PostgreSQL-64-8-65536-4                     24.0                                     0.0                                             0.0                       64.0                                   64.0

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```



















## MySQL

### Benchbase's TPC-C

Example:
```bash
nohup python benchbase.py -m -mc -ma -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms MySQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_mysql_appmetrics.log &
```

This
* activates monitoring (`-m`) cluster-wide (`-mc`)
* starts a clean instance of MySQL (`-dbms`)
  * with a sidecar container for monitoring (`-ma`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-sd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-tb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary


### Evaluate Results

doc_benchbase_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1330s 
    Code: 1758634933
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-1-1-1024-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:442875080
    datadisk:7028
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758634933
MySQL-1-1-1024-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:445062304
    datadisk:9164
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758634933

### Execution

#### Per Pod
                    experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                
MySQL-1-1-1024-1-1               1        160   16384       1      1  300.0           0                   1171.889856                1146.926526         0.0                                                     663149.0                                             136404.0
MySQL-1-1-1024-2-1               1         80    8192       2      1  300.0           0                    619.296595                 606.789929         0.0                                                     730746.0                                             129150.0
MySQL-1-1-1024-2-2               1         80    8192       2      2  300.0           0                    618.576540                 606.673209         0.0                                                     730075.0                                             129302.0

#### Aggregated Parallel
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1        160   16384          1  300.0           0                       1171.89                    1146.93         0.0                                                     663149.0                                             136404.0
MySQL-1-1-1024-2               1        160   16384          2  300.0           0                       1237.87                    1213.46         0.0                                                     730746.0                                             129226.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1, 2]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1      355.0        1.0   1.0         162.253521
MySQL-1-1-1024-2      355.0        1.0   2.0         162.253521

### Ingestion - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1188.23     5.81          5.85                 9.31
MySQL-1-1-1024-2     1188.23     5.81          5.85                 9.31

### Ingestion - Loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1670.37     9.49          0.48                 0.48
MySQL-1-1-1024-2     1670.37     9.49          0.48                 0.48

### Execution - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     2224.78     9.78          6.37                11.99
MySQL-1-1-1024-2     3031.34    10.50          6.80                15.40

### Execution - Benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1247.45     5.46          1.16                 1.16
MySQL-1-1-1024-2     1247.45    10.74          1.16                 1.16

### Application Metrics
                  InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-1-1-1024-1                           1.0                  27807.47                    0.11               0.56                    0.0
MySQL-1-1-1024-2                           0.0                  29977.77                    0.11               0.55                    0.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

The summary shows the first 5 application metrics aggregated per execution run.
An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/dev).



### HammerDB's TPC-C

Example:
```bash
nohup python hammerdb.py -ms 1 -tr -lr 64Gi \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms MySQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_run_mysql_appmetrics.log &
```

doc_hammerdb_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1912s 
    Code: 1759143651
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [16] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-16-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:442655544
    datadisk:6784
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1759143651
MySQL-BHT-16-1-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:444625516
    datadisk:8708
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1759143651

### Execution
                  experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency     NOPM      TPM  duration  errors
MySQL-BHT-16-1-1               1      16       1          1     63.68    609.91         0.0  13537.0  31397.0         5       0
MySQL-BHT-16-1-2               1      16       2          2     71.10    677.15         0.0  12875.5  29962.5         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MySQL-BHT-16-1 - Pods [[1, 2]]

#### Planned
DBMS MySQL-BHT-16-1 - Pods [[1, 2]]

### Loading
                  time_load  terminals  pods  Imported warehouses [1/h]
MySQL-BHT-16-1-1      204.0        1.0   1.0                 282.352941
MySQL-BHT-16-1-2      204.0        1.0   2.0                 282.352941

### Ingestion - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-16-1-1      451.94     3.58         35.43                38.44
MySQL-BHT-16-1-2      489.43     3.58         35.45                38.54

### Ingestion - Loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-16-1-1       88.56     3.33          0.17                 0.17
MySQL-BHT-16-1-2       88.56     3.33          0.17                 0.17

### Execution - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-16-1-1     1343.39     6.36         35.64                41.32
MySQL-BHT-16-1-2     1297.46     6.45         35.85                44.17

### Execution - Benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-16-1-1      152.61     0.50          0.16                 0.16
MySQL-BHT-16-1-2      152.61     0.64          0.16                 0.16

### Application Metrics
                  InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-BHT-16-1-1                           1.0                 106701.09                    0.01                0.0                    0.0
MySQL-BHT-16-1-2                           0.0                 103927.65                    0.01                0.0                    0.0

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```


### TPC-H

Example:
```bash
nohup python tpch.py -ms 1 -dt -tr -lr 64Gi \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_run_mysql_appmetrics.log &
```



### TPC-DS

Example:
```bash
nohup python tpcds.py -ms 1 -dt -tr -lr 64Gi \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_run_mysql_appmetrics.log &
```




### YCSB

Example:
```bash
nohup python ycsb.py -ms 1 -tr -lr 64Gi \
  -sf 3 \
  --workload a \
  -dbms MySQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_run_mysql_appmetrics.log &
```

doc_ycsb_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=3
    Type: ycsb
    Duration: 4278s 
    Code: 1759124495
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 3000000.
    Ordering of inserts is hashed.
    Number of operations is 3000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [2, 3].
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-64-8-65536-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:449561384
    datadisk:13529
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1759124495
MySQL-64-8-65536-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:453121332
    datadisk:17006
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1759124495
MySQL-64-8-65536-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:456641904
    datadisk:20444
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1759124495
MySQL-64-8-65536-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:460165756
    datadisk:23885
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1759124495

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
MySQL-64-8-65536               1       64   65536          8           0                    1830.754943              1640487.0             3000000                           1085951.0

### Execution
                    experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)  [UPDATE-FAILED].Operations  [UPDATE-FAILED].99thPercentileLatency(us)
MySQL-64-8-65536-1               1       64   32768          1           0                       16941.21               177083.0           1498692                            2697.0             1501308                              7915.0                           0                                        0.0
MySQL-64-8-65536-2               1       64   32768          8           0                       14196.95               218650.0           1501509                            2297.0             1498491                              5823.0                           0                                        0.0
MySQL-64-8-65536-3               1       64   49152          1           0                        2701.77              1110382.0           1500096                            2409.0             1499814                              7443.0                          90                                 51019775.0
MySQL-64-8-65536-4               1       64   49152          8           0                       17554.62               174751.0           1498713                            2299.0             1501287                              5995.0                           0                                        0.0

### Workflow

#### Actual
DBMS MySQL-64-8-65536 - Pods [[1, 8, 1, 8]]

#### Planned
DBMS MySQL-64-8-65536 - Pods [[1, 8, 1, 8]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1     5255.23     5.61         23.98                31.75
MySQL-64-8-65536-2     5348.50     5.61         24.00                32.01
MySQL-64-8-65536-3     5348.50     5.61         24.00                32.01
MySQL-64-8-65536-4     5348.50     5.61         24.00                32.01

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1       719.7     2.12          0.13                 0.13
MySQL-64-8-65536-2       719.7     2.12          0.13                 0.13
MySQL-64-8-65536-3       719.7     2.12          0.13                 0.13
MySQL-64-8-65536-4       719.7     2.12          0.13                 0.13

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1     1328.37    10.16         24.10                35.10
MySQL-64-8-65536-2     1324.44     8.81         24.22                38.66
MySQL-64-8-65536-3     3921.37     9.95         24.38                41.77
MySQL-64-8-65536-4     1266.91     9.43         24.50                45.51

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1      817.12     3.79          0.16                 0.16
MySQL-64-8-65536-2      817.12     7.95          0.15                 0.16
MySQL-64-8-65536-3      686.07     2.81          0.17                 0.17
MySQL-64-8-65536-4      555.70     7.29          0.16                 0.17

### Application Metrics
                    InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-64-8-65536-1                           1.0                  10771.57                    0.04               0.49                    0.0
MySQL-64-8-65536-2                           1.0                  11113.40                    0.04               0.24                    0.0
MySQL-64-8-65536-3                           0.0                   6928.91                    0.04               1.33                    0.0
MySQL-64-8-65536-4                           0.0                  10471.19                    0.04               0.70                    0.0

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST failed: Result contains FAILED column
```














