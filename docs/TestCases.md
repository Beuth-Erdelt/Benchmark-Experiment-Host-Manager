# Test Cases

There is a variety of combinations of options that can be tested.

We here list some more basic use cases to test the functionality of bexhoma.

See [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/test.sh) for implementations.
You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):

```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

See also [more test cases](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/test-more.sh) for more and longer running test cases and other DBMS.

See the [log folder](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/logs_tests) for some demo test logs.
The folder also contains `*_summary.txt` files containing only the result summary.


## TPC-H

### PostgreSQL

#### TPC-H Simple

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_postgresql_1.log &
```

yields (after ca. 10 minutes) something like

test_tpch_testcase_postgresql_1.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 538s 
    Code: 1749122827
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:362769364
    datadisk:2756
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749122827

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2540.59
Minimum Cost Supplier Query (TPC-H Q2)                             423.60
Shipping Priority (TPC-H Q3)                                       772.73
Order Priority Checking Query (TPC-H Q4)                          1285.82
Local Supplier Volume (TPC-H Q5)                                   678.53
Forecasting Revenue Change (TPC-H Q6)                              519.56
Forecasting Revenue Change (TPC-H Q7)                              779.08
National Market Share (TPC-H Q8)                                   623.15
Product Type Profit Measure (TPC-H Q9)                            1134.14
Forecasting Revenue Change (TPC-H Q10)                            1295.38
Important Stock Identification (TPC-H Q11)                         249.07
Shipping Modes and Order Priority (TPC-H Q12)                     1033.07
Customer Distribution (TPC-H Q13)                                 2003.98
Forecasting Revenue Change (TPC-H Q14)                             553.40
Top Supplier Query (TPC-H Q15)                                     567.45
Parts/Supplier Relationship (TPC-H Q16)                            570.43
Small-Quantity-Order Revenue (TPC-H Q17)                          2051.46
Large Volume Customer (TPC-H Q18)                                 7064.36
Discounted Revenue (TPC-H Q19)                                     704.61
Potential Part Promotion (TPC-H Q20)                               746.82
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                910.08
Global Sales Opportunity Query (TPC-H Q22)                         240.62

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           27.0         1.0       89.0     125.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.91

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4160.37

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-8-1 1  1              1                 31      1   1          2554.84

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```


#### TPC-H Monitoring

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 10 \
  -dt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_postgresql_2.log &
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_postgresql_2.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 513s 
    Code: 1749123427
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:362467200
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749123427

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2593.30
Minimum Cost Supplier Query (TPC-H Q2)                             436.83
Shipping Priority (TPC-H Q3)                                       736.10
Order Priority Checking Query (TPC-H Q4)                          1272.38
Local Supplier Volume (TPC-H Q5)                                   659.77
Forecasting Revenue Change (TPC-H Q6)                              496.73
Forecasting Revenue Change (TPC-H Q7)                              775.38
National Market Share (TPC-H Q8)                                   617.19
Product Type Profit Measure (TPC-H Q9)                            1088.37
Forecasting Revenue Change (TPC-H Q10)                            1254.81
Important Stock Identification (TPC-H Q11)                         249.06
Shipping Modes and Order Priority (TPC-H Q12)                     1041.05
Customer Distribution (TPC-H Q13)                                 2081.47
Forecasting Revenue Change (TPC-H Q14)                             541.66
Top Supplier Query (TPC-H Q15)                                     556.87
Parts/Supplier Relationship (TPC-H Q16)                            554.41
Small-Quantity-Order Revenue (TPC-H Q17)                          2036.83
Large Volume Customer (TPC-H Q18)                                 7942.95
Discounted Revenue (TPC-H Q19)                                     686.88
Potential Part Promotion (TPC-H Q20)                               671.08
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                906.43
Global Sales Opportunity Query (TPC-H Q22)                         244.90

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           29.0         1.0       90.0     129.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.89

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4198.36

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-8-1 1  1              1                 31      1   1          2554.84

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      122.17     0.96          3.72                 4.91

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        5.55        0          0.02                 0.49

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       89.74        0          3.82                 5.01

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       11.91        0          0.24                 0.25

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### TPC-H Throughput Test

```
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
```


```bash
nohup python tpch.py -ms 1 -tr \
  -sf 10 \
  -dt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_postgresql_3.log &
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_postgresql_3.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 1136s 
    Code: 1749124058
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359468664
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359468728
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359468728
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359469096
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058
PostgreSQL-BHT-8-2-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359469184
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058
PostgreSQL-BHT-8-2-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359469184
    datadisk:2756
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749124058

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                                   2614.52                 2642.39                 2604.84                18633.87                 2624.48                 2675.74
Minimum Cost Supplier Query (TPC-H Q2)                               445.02                  441.96                  447.43                 5703.12                  433.16                  435.90
Shipping Priority (TPC-H Q3)                                         779.34                  774.85                  762.82                 7519.57                  789.58                  792.43
Order Priority Checking Query (TPC-H Q4)                            1281.22                 1286.58                 1342.62                 1306.41                 1309.83                 1313.99
Local Supplier Volume (TPC-H Q5)                                     665.83                  674.82                  686.17                  690.62                  699.38                  698.48
Forecasting Revenue Change (TPC-H Q6)                                507.17                  520.35                  520.19                  526.88                  535.80                  538.53
Forecasting Revenue Change (TPC-H Q7)                                785.13                  788.03                  798.76                 1295.23                  805.37                  797.96
National Market Share (TPC-H Q8)                                     624.63                  632.75                  647.12                  740.64                  658.46                  665.55
Product Type Profit Measure (TPC-H Q9)                              1132.25                 1164.79                 1117.45                 2016.87                 1103.52                 1110.77
Forecasting Revenue Change (TPC-H Q10)                              1265.15                 1267.20                 1286.72                 1275.40                 1300.60                 1297.94
Important Stock Identification (TPC-H Q11)                           262.01                  260.05                  265.42                  250.19                  265.08                  255.87
Shipping Modes and Order Priority (TPC-H Q12)                       1057.55                 1046.59                 1058.06                 1044.35                 1077.73                 1064.54
Customer Distribution (TPC-H Q13)                                   2065.25                 2072.03                 2072.19                 1989.10                 2001.56                 1998.74
Forecasting Revenue Change (TPC-H Q14)                               546.77                  562.86                  573.69                  560.21                  579.82                  571.89
Top Supplier Query (TPC-H Q15)                                       573.94                  582.73                  583.57                  586.54                  584.55                  586.18
Parts/Supplier Relationship (TPC-H Q16)                              586.59                  580.33                  577.89                  575.69                  576.60                  563.90
Small-Quantity-Order Revenue (TPC-H Q17)                            2033.42                 2051.03                 2053.55                 2060.93                 2111.37                 2039.19
Large Volume Customer (TPC-H Q18)                                   8056.48                 7307.63                 8689.75                 7420.83                 7240.46                 7213.62
Discounted Revenue (TPC-H Q19)                                       708.21                  717.10                  710.97                  714.35                  721.29                  718.50
Potential Part Promotion (TPC-H Q20)                                 653.03                  730.87                  638.75                  652.84                  639.70                  638.02
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  939.45                  915.25                  907.94                 2708.81                  916.32                  913.78
Global Sales Opportunity Query (TPC-H Q22)                           266.10                  231.33                  227.50                  375.23                  216.86                  217.63

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           44.0         1.0       87.0     141.0
PostgreSQL-BHT-8-1-2-1           1.0           44.0         1.0       87.0     141.0
PostgreSQL-BHT-8-1-2-2           1.0           44.0         1.0       87.0     141.0
PostgreSQL-BHT-8-2-1-1           1.0           44.0         1.0       87.0     141.0
PostgreSQL-BHT-8-2-2-1           1.0           44.0         1.0       87.0     141.0
PostgreSQL-BHT-8-2-2-2           1.0           44.0         1.0       87.0     141.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           0.92
PostgreSQL-BHT-8-1-2-1           0.91
PostgreSQL-BHT-8-1-2-2           0.92
PostgreSQL-BHT-8-2-1-1           1.40
PostgreSQL-BHT-8-2-2-1           0.91
PostgreSQL-BHT-8-2-2-2           0.91

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            4107.36
PostgreSQL-BHT-8-1-2-1            4111.74
PostgreSQL-BHT-8-1-2-2            4092.11
PostgreSQL-BHT-8-2-1-1            2678.56
PostgreSQL-BHT-8-2-2-1            4115.93
PostgreSQL-BHT-8-2-2-2            4131.74

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                   time [s]  count  SF  Throughput@Size
DBMS                 SF num_experiment num_client                                      
PostgreSQL-BHT-8-1-1 1  1              1                 32      1   1           2475.0
PostgreSQL-BHT-8-1-2 1  1              2                 33      2   1           4800.0
PostgreSQL-BHT-8-2-1 1  2              1                 64      1   1           1237.5
PostgreSQL-BHT-8-2-2 1  2              2                 32      2   1           4950.0

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      118.56     1.12          3.69                 5.36
PostgreSQL-BHT-8-1-2      118.56     1.12          3.69                 5.36

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1        2.08        0          0.02                 0.21
PostgreSQL-BHT-8-1-2        2.08        0          0.02                 0.21

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       57.45     0.98          3.69                 5.36
PostgreSQL-BHT-8-1-2      206.36     0.00          7.43                 9.05
PostgreSQL-BHT-8-2-1      402.41     0.00          6.15                 8.02
PostgreSQL-BHT-8-2-2      112.61     2.09          3.98                 5.78

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       14.05      0.0          0.27                 0.28
PostgreSQL-BHT-8-1-2        0.00      0.0          0.27                 0.28
PostgreSQL-BHT-8-2-1        0.02      0.0          0.00                 0.00
PostgreSQL-BHT-8-2-2        0.00      0.0          0.00                 0.00

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```







### MySQL

#### TPC-H Simple

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mysql_1.log &
```

yields (after ca. 10 minutes) something like

test_tpch_testcase_mysql_1.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 517s 
    Code: 1748911530
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-8-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:325868760
    datadisk:8286
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748911530

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MySQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                              89.12
Minimum Cost Supplier Query (TPC-H Q2)                          4.14
Shipping Priority (TPC-H Q3)                                    2.14
Order Priority Checking Query (TPC-H Q4)                        1.66
Local Supplier Volume (TPC-H Q5)                                2.79
Forecasting Revenue Change (TPC-H Q6)                           1.98
Forecasting Revenue Change (TPC-H Q7)                           2.48
National Market Share (TPC-H Q8)                                3.75
Product Type Profit Measure (TPC-H Q9)                          2.91
Forecasting Revenue Change (TPC-H Q10)                          3.04
Important Stock Identification (TPC-H Q11)                      2.40
Shipping Modes and Order Priority (TPC-H Q12)                   2.37
Customer Distribution (TPC-H Q13)                               2.12
Forecasting Revenue Change (TPC-H Q14)                          2.35
Top Supplier Query (TPC-H Q15)                                 13.23
Parts/Supplier Relationship (TPC-H Q16)                         2.49
Small-Quantity-Order Revenue (TPC-H Q17)                        2.41
Large Volume Customer (TPC-H Q18)                               2.79
Discounted Revenue (TPC-H Q19)                                  2.51
Potential Part Promotion (TPC-H Q20)                            2.87
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)             3.61
Global Sales Opportunity Query (TPC-H Q22)                      2.64

### Loading [s]
                 timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-8-1-1           0.0            5.0         3.0       11.0      28.0

### Geometric Mean of Medians of Timer Run [s]
                 Geo Times [s]
DBMS                          
MySQL-BHT-8-1-1            0.0

### Power@Size ((3600*SF)/(geo times))
                 Power@Size [~Q/h]
DBMS                              
MySQL-BHT-8-1-1         1091047.59

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                            time [s]  count  SF  Throughput@Size
DBMS          SF num_experiment num_client                                      
MySQL-BHT-8-1 1  1              1                  3      1   1          26400.0

### Workflow

#### Actual
DBMS MySQL-BHT-8 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```


#### TPC-H Monitoring

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 10 \
  -dt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mysql_2.log &
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_mysql_2.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 506s 
    Code: 1748912070
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-8-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:325868736
    datadisk:8286
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912070

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MySQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                              77.77
Minimum Cost Supplier Query (TPC-H Q2)                          4.66
Shipping Priority (TPC-H Q3)                                    2.98
Order Priority Checking Query (TPC-H Q4)                        2.88
Local Supplier Volume (TPC-H Q5)                                2.64
Forecasting Revenue Change (TPC-H Q6)                           2.56
Forecasting Revenue Change (TPC-H Q7)                           3.44
National Market Share (TPC-H Q8)                                4.37
Product Type Profit Measure (TPC-H Q9)                          2.82
Forecasting Revenue Change (TPC-H Q10)                          2.66
Important Stock Identification (TPC-H Q11)                      2.85
Shipping Modes and Order Priority (TPC-H Q12)                   2.43
Customer Distribution (TPC-H Q13)                               2.19
Forecasting Revenue Change (TPC-H Q14)                          2.56
Top Supplier Query (TPC-H Q15)                                  4.68
Parts/Supplier Relationship (TPC-H Q16)                         2.91
Small-Quantity-Order Revenue (TPC-H Q17)                        1.92
Large Volume Customer (TPC-H Q18)                               2.34
Discounted Revenue (TPC-H Q19)                                  2.55
Potential Part Promotion (TPC-H Q20)                            3.07
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)             3.07
Global Sales Opportunity Query (TPC-H Q22)                      2.61

### Loading [s]
                 timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-8-1-1           1.0            4.0         3.0       12.0      27.0

### Geometric Mean of Medians of Timer Run [s]
                 Geo Times [s]
DBMS                          
MySQL-BHT-8-1-1            0.0

### Power@Size ((3600*SF)/(geo times))
                 Power@Size [~Q/h]
DBMS                              
MySQL-BHT-8-1-1         1074975.18

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                            time [s]  count  SF  Throughput@Size
DBMS          SF num_experiment num_client                                      
MySQL-BHT-8-1 1  1              1                  2      1   1          39600.0

### Workflow

#### Actual
DBMS MySQL-BHT-8 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
               CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1        3.61     0.03         37.45                37.48

### Ingestion - Loader
               CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1           0        0           0.0                  0.0

### Execution - SUT
               CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1        7.33        0         37.73                37.77

### Execution - Benchmarker
               CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1           0        0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### TPC-H Throughput Test

```
kubectl delete pvc bexhoma-storage-mysql-tpch-1
```

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 10 \
  -dt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mysql_3.log &
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_mysql_3.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 1241s 
    Code: 1748912641
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-BHT-8-1-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-1-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-1-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384416
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384420
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384420
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MySQL-BHT-8-1-1-1  MySQL-BHT-8-1-2-1  MySQL-BHT-8-1-2-2  MySQL-BHT-8-2-1-1  MySQL-BHT-8-2-2-1  MySQL-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                                77.71              71.17             113.27              90.10              68.93              81.12
Minimum Cost Supplier Query (TPC-H Q2)                            4.07               3.44               3.64              16.93               4.26               3.92
Shipping Priority (TPC-H Q3)                                      2.18               1.87               2.57               3.00               1.75               2.78
Order Priority Checking Query (TPC-H Q4)                          1.64               1.53               3.12               3.66               1.49               2.79
Local Supplier Volume (TPC-H Q5)                                  1.87               1.74               3.57               2.56               1.77               3.41
Forecasting Revenue Change (TPC-H Q6)                             1.33               1.32               2.57               2.35               1.45               2.29
Forecasting Revenue Change (TPC-H Q7)                             1.90               2.24               3.55               2.75               1.87               2.75
National Market Share (TPC-H Q8)                                  3.18               1.92               3.07               3.26               2.51               2.98
Product Type Profit Measure (TPC-H Q9)                            1.94               1.69               2.81               2.76               1.92               2.73
Forecasting Revenue Change (TPC-H Q10)                            2.34               1.73               2.02               3.02               1.69               2.82
Important Stock Identification (TPC-H Q11)                        2.17               1.62               2.62               2.36               1.46               2.78
Shipping Modes and Order Priority (TPC-H Q12)                     2.92               1.41               3.14               2.75               1.71               2.73
Customer Distribution (TPC-H Q13)                                 2.79               1.47               2.62               2.19               1.32               2.65
Forecasting Revenue Change (TPC-H Q14)                            1.91               1.28               2.55               2.31               1.13               2.48
Top Supplier Query (TPC-H Q15)                                    4.25               2.78               4.84               5.21               3.27               4.68
Parts/Supplier Relationship (TPC-H Q16)                           2.79               1.84               3.10               2.31               2.02               3.30
Small-Quantity-Order Revenue (TPC-H Q17)                          2.13               1.24               5.14               2.00               1.73               2.81
Large Volume Customer (TPC-H Q18)                                 2.22               1.51               2.48               2.56               2.05               3.17
Discounted Revenue (TPC-H Q19)                                    2.26               1.71               2.63               2.48               2.09               2.37
Potential Part Promotion (TPC-H Q20)                              2.61               1.49               3.36               2.88               1.79               3.23
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               3.06               1.52               3.19               3.00               1.87               3.14
Global Sales Opportunity Query (TPC-H Q22)                        2.52               1.74               2.90               2.54               2.01               2.95

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-8-1-1-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-1-2-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-1-2-2           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-1-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-2-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-2-2           1.0            4.0         9.0       20.0      41.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MySQL-BHT-8-1-1-1            0.0
MySQL-BHT-8-1-2-1            0.0
MySQL-BHT-8-1-2-2            0.0
MySQL-BHT-8-2-1-1            0.0
MySQL-BHT-8-2-2-1            0.0
MySQL-BHT-8-2-2-2            0.0

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MySQL-BHT-8-1-1-1         1287048.59
MySQL-BHT-8-1-2-1         1775137.53
MySQL-BHT-8-1-2-2         1003150.78
MySQL-BHT-8-2-1-1         1034211.47
MySQL-BHT-8-2-2-1         1630827.76
MySQL-BHT-8-2-2-2         1050194.94

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MySQL-BHT-8-1-1 1  1              1                  2      1   1          39600.0
MySQL-BHT-8-1-2 1  1              2                  3      2   1          52800.0
MySQL-BHT-8-2-1 1  2              1                  2      1   1          39600.0
MySQL-BHT-8-2-2 1  2              2                  3      2   1          52800.0

### Workflow

#### Actual
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        4.72     0.02         37.47                45.51
MySQL-BHT-8-1-2        4.72     0.02         37.47                45.51

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1           0        0           0.0                  0.0
MySQL-BHT-8-1-2           0        0           0.0                  0.0

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00     0.00         37.47                45.51
MySQL-BHT-8-1-2        1.35     0.00         37.75                45.78
MySQL-BHT-8-2-1      255.00     0.00         75.20                91.06
MySQL-BHT-8-2-2        0.00     0.02         37.46                45.29

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-1-2        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-2        0.03      0.0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```






### MariaDB

#### TPC-H Simple

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mariadb_1.log &
```

yields (after ca. 10 minutes) something like

test_tpch_testcase_mariadb_1.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 2425s 
    Code: 1748913961
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-BHT-8-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:319522064
    datadisk:2088
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748913961

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             25623.48
Minimum Cost Supplier Query (TPC-H Q2)                         1311.29
Shipping Priority (TPC-H Q3)                                   5029.67
Order Priority Checking Query (TPC-H Q4)                       1046.54
Local Supplier Volume (TPC-H Q5)                               3219.38
Forecasting Revenue Change (TPC-H Q6)                          2834.28
Forecasting Revenue Change (TPC-H Q7)                          3510.18
National Market Share (TPC-H Q8)                               6446.70
Product Type Profit Measure (TPC-H Q9)                         5876.47
Forecasting Revenue Change (TPC-H Q10)                         2743.25
Important Stock Identification (TPC-H Q11)                      380.72
Shipping Modes and Order Priority (TPC-H Q12)                 11065.87
Customer Distribution (TPC-H Q13)                             10172.68
Forecasting Revenue Change (TPC-H Q14)                        29375.73
Top Supplier Query (TPC-H Q15)                                 6631.28
Parts/Supplier Relationship (TPC-H Q16)                         627.04
Small-Quantity-Order Revenue (TPC-H Q17)                        155.25
Large Volume Customer (TPC-H Q18)                             10198.12
Discounted Revenue (TPC-H Q19)                                  265.01
Potential Part Promotion (TPC-H Q20)                            525.76
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          194729.73
Global Sales Opportunity Query (TPC-H Q22)                      392.40

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1           1.0          269.0         2.0     1496.0    1775.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MariaDB-BHT-8-1-1           3.18

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MariaDB-BHT-8-1-1            1172.82

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MariaDB-BHT-8-1 1  1              1                328      1   1           241.46

### Workflow

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MariaDB-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```


#### TPC-H Monitoring

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mariadb_2.log &
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_mariadb_2.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 2482s 
    Code: 1748916422
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-BHT-8-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:319525344
    datadisk:2091
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748916422

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             26007.81
Minimum Cost Supplier Query (TPC-H Q2)                         1424.68
Shipping Priority (TPC-H Q3)                                   5752.96
Order Priority Checking Query (TPC-H Q4)                       1470.50
Local Supplier Volume (TPC-H Q5)                               3638.64
Forecasting Revenue Change (TPC-H Q6)                          3132.16
Forecasting Revenue Change (TPC-H Q7)                          3854.64
National Market Share (TPC-H Q8)                               6830.26
Product Type Profit Measure (TPC-H Q9)                         6253.92
Forecasting Revenue Change (TPC-H Q10)                         2856.04
Important Stock Identification (TPC-H Q11)                      422.14
Shipping Modes and Order Priority (TPC-H Q12)                 11440.37
Customer Distribution (TPC-H Q13)                             10250.61
Forecasting Revenue Change (TPC-H Q14)                        30218.01
Top Supplier Query (TPC-H Q15)                                 6329.73
Parts/Supplier Relationship (TPC-H Q16)                         647.58
Small-Quantity-Order Revenue (TPC-H Q17)                        159.29
Large Volume Customer (TPC-H Q18)                             11382.62
Discounted Revenue (TPC-H Q19)                                  368.73
Potential Part Promotion (TPC-H Q20)                            734.58
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          196513.50
Global Sales Opportunity Query (TPC-H Q22)                      459.38

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1           1.0          259.0         2.0     1520.0    1790.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MariaDB-BHT-8-1-1            3.5

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MariaDB-BHT-8-1-1            1062.48

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MariaDB-BHT-8-1 1  1              1                335      1   1           236.42

### Workflow

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MariaDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1     1526.26     2.02          9.69                  9.7

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1        7.86     0.02          0.52                 1.16

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1      321.09      1.0          9.81                 9.82

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1       14.85     0.05          0.26                 0.26

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### TPC-H Throughput Test

```
kubectl delete pvc bexhoma-storage-mariadb-tpch-1
```

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mariadb_3.log &
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_mariadb_3.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 6081s 
    Code: 1748919033
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MariaDB-BHT-8-1-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515964
    datadisk:2090
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-1-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515968
    datadisk:2090
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-1-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515968
    datadisk:2090
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-2-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515956
    datadisk:2095
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-2-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515960
    datadisk:2095
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-2-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515960
    datadisk:2095
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1-1  MariaDB-BHT-8-1-2-1  MariaDB-BHT-8-1-2-2  MariaDB-BHT-8-2-1-1  MariaDB-BHT-8-2-2-1  MariaDB-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                               25974.35             24684.85             24739.11             25744.04             25961.78             25820.11
Minimum Cost Supplier Query (TPC-H Q2)                           1453.22              1677.86              1703.46              1762.40              1618.89              1619.03
Shipping Priority (TPC-H Q3)                                     5221.88              6529.53              6493.69              7216.41              6423.40              6417.20
Order Priority Checking Query (TPC-H Q4)                         1075.72              1336.18              1341.60              1323.22              1288.26              1287.75
Local Supplier Volume (TPC-H Q5)                                 3287.17              3783.79              3852.58              3482.38              3748.09              3748.27
Forecasting Revenue Change (TPC-H Q6)                            2801.76              3999.80              3944.80              3313.50              2961.49              2943.89
Forecasting Revenue Change (TPC-H Q7)                            3639.82              3945.00              4008.61              3805.95              4300.03              4300.00
National Market Share (TPC-H Q8)                                 6468.87              7603.58              7262.87              6879.16              7697.18              7697.15
Product Type Profit Measure (TPC-H Q9)                           5802.95              6661.06              6938.45              6114.94              6373.02              6372.93
Forecasting Revenue Change (TPC-H Q10)                           2955.81              2928.45              2966.85              2984.05              3205.20              3202.19
Important Stock Identification (TPC-H Q11)                        382.23               442.78               435.66               413.34               494.31               498.47
Shipping Modes and Order Priority (TPC-H Q12)                   11413.65             12428.21             12536.94             11768.67             12604.75             12604.79
Customer Distribution (TPC-H Q13)                                9852.55             11791.98             12055.63              9988.15             11283.96             11281.52
Forecasting Revenue Change (TPC-H Q14)                          31100.58             36921.43             40084.43             30354.96             35245.42             35245.52
Top Supplier Query (TPC-H Q15)                                   6228.19              6508.01              6396.66              6582.36              6575.85              6504.29
Parts/Supplier Relationship (TPC-H Q16)                           629.99               643.59               623.90               671.43               665.07               664.95
Small-Quantity-Order Revenue (TPC-H Q17)                          160.92               150.71               153.73               146.73               151.15               150.50
Large Volume Customer (TPC-H Q18)                               10162.65             11347.40             11718.83             10464.66             11239.03             11334.00
Discounted Revenue (TPC-H Q19)                                    264.98               285.77               294.18               287.03               272.64               275.01
Potential Part Promotion (TPC-H Q20)                              527.27               577.32               685.68               586.09               634.04               635.37
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)            194454.66            222543.33            222766.92            197089.34            213727.42            213737.84
Global Sales Opportunity Query (TPC-H Q22)                        402.35               395.79               372.82               397.17               442.14               441.05

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-1-2-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-1-2-2           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-2-1-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-2-2-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-2-2-2           1.0          696.0         5.0     3089.0    3797.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MariaDB-BHT-8-1-1-1           3.22
MariaDB-BHT-8-1-2-1           3.59
MariaDB-BHT-8-1-2-2           3.64
MariaDB-BHT-8-2-1-1           3.44
MariaDB-BHT-8-2-2-1           3.58
MariaDB-BHT-8-2-2-2           3.60

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MariaDB-BHT-8-1-1-1            1154.15
MariaDB-BHT-8-1-2-1            1035.86
MariaDB-BHT-8-1-2-2            1022.45
MariaDB-BHT-8-2-1-1            1080.60
MariaDB-BHT-8-2-2-1            1036.64
MariaDB-BHT-8-2-2-2            1036.84

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                time [s]  count  SF  Throughput@Size
DBMS              SF num_experiment num_client                                      
MariaDB-BHT-8-1-1 1  1              1                328      1   1           241.46
MariaDB-BHT-8-1-2 1  1              2                376      2   1           421.28
MariaDB-BHT-8-2-1 1  2              1                338      1   1           234.32
MariaDB-BHT-8-2-2 1  2              2                363      2   1           436.36

### Workflow

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MariaDB-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1     2263.77     2.11          9.81                 9.84
MariaDB-BHT-8-1-2     2263.77     2.11          9.81                 9.84

### Ingestion - Loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1        7.69     0.01           0.5                 1.16
MariaDB-BHT-8-1-2        7.69     0.01           0.5                 1.16

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1      318.25      1.0          9.88                 9.91
MariaDB-BHT-8-1-2      678.67      2.0          9.89                 9.92
MariaDB-BHT-8-2-1     3375.23      1.0         12.41                12.63
MariaDB-BHT-8-2-2      650.38      2.0          2.56                 2.81

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1       14.94     0.00          0.26                 0.26
MariaDB-BHT-8-1-2       25.00     0.01          0.72                 0.74
MariaDB-BHT-8-2-1       14.09     0.01          0.25                 0.27
MariaDB-BHT-8-2-2       31.69     0.06          0.75                 0.78

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


















## Benchbase

### PostgreSQL

#### Benchbase Simple

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_1.log &
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_postgresql_1.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 801s 
    Code: 1749126830
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:363141144
    datadisk:4324
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749126830

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0           0                       1838.93                    1830.73         0.0                                                      19784.0                                               8693.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      166.0        1.0   1.0         346.987952

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Benchbase Persistency


Make sure, the database does not exist:
```bash
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 10
```

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_2.log &
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_postgresql_2.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 676s 
    Code: 1749127700
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 1 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358233172
    datadisk:9476
    volume_size:30G
    volume_used:9.3G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749127700
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358233600
    datadisk:8733
    volume_size:30G
    volume_used:8.6G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1749127700

### Execution
                         experiment_run  terminals  target  pod_count  time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1         16    8192          1  60.0           0                        769.17                     765.82         0.0                                                      32679.0                                              20781.0
PostgreSQL-1-1-1024-2-1               2         16    8192          1  60.0           0                        877.26                     873.60         0.0                                                      30925.0                                              18222.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1-1      175.0        1.0   1.0         329.142857
PostgreSQL-1-1-1024-2-1      175.0        1.0   1.0         329.142857

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Benchbase Monitoring

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_3.log &
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_postgresql_3.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 858s 
    Code: 1749128420
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:362668492
    datadisk:4324
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749128420

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0           0                       1838.63                    1830.43         0.0                                                      20064.0                                               8695.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      173.0        1.0   1.0         332.947977

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      527.31     6.71          3.98                 5.37

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1592.36        0          0.98                 0.98

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1961.93     7.15          4.66                 6.75

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      980.15     3.38          1.42                 1.42

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### Benchbase Complex

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1,2 \
  -nbt 8 \
  -nbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_4.log &
```

yields (after ca. 30 minutes) something like

test_benchbase_testcase_postgresql_4.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1936s 
    Code: 1749129321
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 2 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [8] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358240476
    datadisk:7963
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358240992
    datadisk:8051
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-1-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358241380
    datadisk:8217
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-1-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358241172
    datadisk:8331
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358490124
    datadisk:8476
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358491144
    datadisk:8551
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358491472
    datadisk:8712
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358245748
    datadisk:8821
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
                code:1749129321

### Execution
                         experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1          8    8192          1  120.0           0                        856.82                     853.06         0.0                                                      15454.0                                              9325.00
PostgreSQL-1-1-1024-1-2               1         16   16384          2  120.0           1                       1650.73                    1635.38         0.0                                                      21337.0                                              9683.50
PostgreSQL-1-1-1024-1-3               1          8    8192          2  120.0           0                       1144.57                    1133.88         0.0                                                      14775.0                                              6976.50
PostgreSQL-1-1-1024-1-4               1         16   16384          4  120.0           2                       1488.36                    1466.36         0.0                                                      23439.0                                             10734.75
PostgreSQL-1-1-1024-2-1               2          8    8192          1  120.0           0                        733.64                     730.11         0.0                                                      21145.0                                             10892.00
PostgreSQL-1-1-1024-2-2               2         16   16384          2  120.0           0                       1622.52                    1607.08         0.0                                                      20943.0                                              9848.00
PostgreSQL-1-1-1024-2-3               2          8    8192          2  120.0           1                       1091.28                    1080.81         0.0                                                      15040.0                                              7317.00
PostgreSQL-1-1-1024-2-4               2         16   16384          4  120.0           1                       1434.22                    1412.25         0.0                                                      23812.0                                             11140.50

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[4, 2, 2, 1], [2, 4, 2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1-1      175.0        1.0   1.0         329.142857
PostgreSQL-1-1-1024-1-2      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-1-3      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-1-4      175.0        1.0   4.0         329.142857
PostgreSQL-1-1-1024-2-1      175.0        1.0   1.0         329.142857
PostgreSQL-1-1-1024-2-2      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-2-3      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-2-4      175.0        1.0   4.0         329.142857

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      329.70     0.76          3.23                 7.68
PostgreSQL-1-1-1024-1-2      691.98     6.95          3.72                 8.37
PostgreSQL-1-1-1024-1-3      448.58     3.44          3.89                 8.68
PostgreSQL-1-1-1024-1-4      727.81     5.49          4.17                 9.10
PostgreSQL-1-1-1024-2-1     2460.89     0.06          6.37                11.45
PostgreSQL-1-1-1024-2-2      631.05     0.00          3.66                 8.72
PostgreSQL-1-1-1024-2-3      349.81     0.00          3.87                 9.06
PostgreSQL-1-1-1024-2-4      545.74     6.33          4.17                 9.50

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      166.09     2.02          0.58                 0.58
PostgreSQL-1-1-1024-1-2      394.05     1.60          1.75                 1.75
PostgreSQL-1-1-1024-1-3      242.09     2.05          1.91                 1.91
PostgreSQL-1-1-1024-1-4      284.79     1.82          2.47                 2.47
PostgreSQL-1-1-1024-2-1       77.49     0.00          0.32                 0.32
PostgreSQL-1-1-1024-2-2      281.63     1.62          1.21                 1.21
PostgreSQL-1-1-1024-2-3      197.94     0.00          1.59                 1.59
PostgreSQL-1-1-1024-2-4      222.02     0.75          1.97                 1.98

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```











### MySQL

#### Benchbase Simple

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mysql_1.log &
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mysql_1.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1713s 
    Code: 1748932537
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-1-1-1024-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:328988352
    datadisk:11132
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748932537

### Execution
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1         16    8192          1  300.0           0                        104.93                     104.49         0.0                                                     477418.0                                             152341.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1      804.0        1.0   1.0          71.641791

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Benchbase Persistency


Make sure, the database does not exist:
```bash
kubectl delete pvc bexhoma-storage-mysql-benchbase-16
sleep 10
```

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mysql_2.log &
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mysql_2.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 8930s 
    Code: 1748934307
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 1 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-1-1-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590004
    datadisk:11132
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748934307
MySQL-1-1-1024-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590184
    datadisk:11165
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1748934307

### Execution
                    experiment_run  terminals  target  pod_count  time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1-1               1         16    8192          1  60.0           0                          1.00                       1.23         0.0                                                   47671586.0                                            8847058.0
MySQL-1-1-1024-2-1               2         16    8192          1  60.0           0                          4.52                       4.78         0.0                                                   15558733.0                                            3001960.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1], [1]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1-1     7641.0        1.0   1.0            7.53828
MySQL-1-1-1024-2-1     7641.0        1.0   1.0            7.53828

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Benchbase Monitoring

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mysql_3.log &
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mysql_3.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1530s 
    Code: 1748943250
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-1-1-1024-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:328989148
    datadisk:11132
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748943250

### Execution
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1         16    8192          1  300.0           0                        112.58                     112.09         0.0                                                     438246.0                                             142078.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1      765.0        1.0   1.0          75.294118

### Ingestion - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1542.16     2.22         37.43                37.47

### Ingestion - Loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1341.21     3.77          1.33                 1.33

### Execution - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1      436.01     1.81         23.42                27.21

### Execution - Benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1      167.69     0.59          0.82                 0.82

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### Benchbase Complex

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -tb 1024 \
  -nbp 1,2 \
  -nbt 8 \
  -nbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mysql_4.log &
```

yields (after ca. 30 minutes) something like

test_benchbase_testcase_mysql_4.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 2183s 
    Code: 1748944810
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 2 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [8] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-1-1-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590204
    datadisk:11187
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-1-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590204
    datadisk:11220
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-1-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590208
    datadisk:11256
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-1-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590208
    datadisk:11308
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590216
    datadisk:11339
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590216
    datadisk:11374
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590220
    datadisk:11458
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590396
    datadisk:11489
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
                code:1748944810

### Execution
                    experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1-1               1          8    8192          1  120.0           0                         36.02                      35.85         0.0                                                     610937.0                                            220741.00
MySQL-1-1-1024-1-2               1         16   16384          2  120.0           0                         39.64                      39.47         0.0                                                     820427.0                                            285537.50
MySQL-1-1-1024-1-3               1          8    8192          2  120.0           0                         69.92                      69.46         0.0                                                     394377.0                                            114272.50
MySQL-1-1-1024-1-4               1         16   16384          4  120.0           0                         37.22                      36.94         0.0                                                    1876083.0                                            429714.25
MySQL-1-1-1024-2-1               2          8    8192          1  120.0           0                         45.04                      44.85         0.0                                                     500014.0                                            177493.00
MySQL-1-1-1024-2-2               2         16   16384          2  120.0           0                        106.22                     105.62         0.0                                                     483418.0                                            150073.00
MySQL-1-1-1024-2-3               2          8    8192          2  120.0           0                         39.84                      39.67         0.0                                                     952677.0                                            200600.50
MySQL-1-1-1024-2-4               2         16   16384          4  120.0           0                         49.48                      49.02         0.0                                                     940977.0                                            213649.25

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1, 2, 2, 4], [4, 2, 2, 1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1-1     7641.0        1.0   1.0            7.53828
MySQL-1-1-1024-1-2     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-1-3     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-1-4     7641.0        1.0   4.0            7.53828
MySQL-1-1-1024-2-1     7641.0        1.0   1.0            7.53828
MySQL-1-1-1024-2-2     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-2-3     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-2-4     7641.0        1.0   4.0            7.53828

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1-1       50.42     0.79         37.96                45.81
MySQL-1-1-1024-1-2       78.16     0.28         38.17                46.08
MySQL-1-1-1024-1-3       86.48     0.10         38.23                46.20
MySQL-1-1-1024-1-4       49.59     0.73         38.27                46.26
MySQL-1-1-1024-2-1       51.82     0.00         37.95                45.98
MySQL-1-1-1024-2-2      112.04     1.48         38.17                46.30
MySQL-1-1-1024-2-3      100.06     0.47         38.21                46.40
MySQL-1-1-1024-2-4      123.16     1.35         38.26                46.51

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1-1       33.15     0.00          0.28                 0.28
MySQL-1-1-1024-1-2       61.65     0.00          0.80                 0.80
MySQL-1-1-1024-1-3       33.28     0.00          1.19                 1.19
MySQL-1-1-1024-1-4       38.84     0.08          1.45                 1.45
MySQL-1-1-1024-2-1       35.98     0.00          0.30                 0.30
MySQL-1-1-1024-2-2       87.11     0.37          0.97                 0.97
MySQL-1-1-1024-2-3       35.98     0.07          1.18                 1.18
MySQL-1-1-1024-2-4      117.93     0.51          4.46                 4.47

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```











### MariaDB

#### Benchbase Simple

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mariadb_1.log &
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mariadb_1.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1014s 
    Code: 1748947031
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-1-1-1024-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:319539432
    datadisk:1904
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748947031

### Execution
                    experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MariaDB-1-1-1024-1               1         16    8192          1  300.0           0                        157.65                     156.99         0.0                                                      31711.0                                              93467.0

### Workflow

#### Actual
DBMS MariaDB-1-1-1024 - Pods [[1]]

#### Planned
DBMS MariaDB-1-1-1024 - Pods [[1]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MariaDB-1-1-1024-1      327.0        1.0   1.0         176.146789

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Benchbase Persistency


Make sure, the database does not exist:
```bash
kubectl delete pvc bexhoma-storage-mariadb-benchbase-16
sleep 10
```

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mariadb_2.log &
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mariadb_2.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1253s 
    Code: 1748948081
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 1 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MariaDB-1-1-1024-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590408
    datadisk:1883
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748948081
MariaDB-1-1-1024-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590408
    datadisk:1927
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1748948081

### Execution
                      experiment_run  terminals  target  pod_count  time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MariaDB-1-1-1024-1-1               1         16    8192          1  60.0           0                        319.82                     318.58         0.0                                                      39237.0                                              49543.0
MariaDB-1-1-1024-2-1               2         16    8192          1  60.0           0                        424.30                     422.77         0.0                                                      22345.0                                              33410.0

### Workflow

#### Actual
DBMS MariaDB-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS MariaDB-1-1-1024 - Pods [[1], [1]]

### Loading
                      time_load  terminals  pods  Throughput [SF/h]
MariaDB-1-1-1024-1-1      471.0        1.0   1.0         122.292994
MariaDB-1-1-1024-2-1      471.0        1.0   1.0         122.292994

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Benchbase Monitoring

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mariadb_3.log &
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mariadb_3.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 948s 
    Code: 1748949342
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-1-1-1024-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:319535364
    datadisk:1900
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748949342

### Execution
                    experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MariaDB-1-1-1024-1               1         16    8192          1  300.0           0                         239.1                     238.09         0.0                                                      42707.0                                              66868.0

### Workflow

#### Actual
DBMS MariaDB-1-1-1024 - Pods [[1]]

#### Planned
DBMS MariaDB-1-1-1024 - Pods [[1]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MariaDB-1-1-1024-1      309.0        1.0   1.0         186.407767

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-1-1-1024-1      587.11     1.56          2.58                 2.59

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-1-1-1024-1     1556.21      7.1          1.29                 1.29

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-1-1-1024-1      436.84     1.85          2.67                 2.68

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-1-1-1024-1      194.51     0.97          0.75                 0.75

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### Benchbase Complex

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -tb 1024 \
  -nbp 1,2 \
  -nbt 8 \
  -nbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mariadb_4.log &
```

yields (after ca. 30 minutes) something like

test_benchbase_testcase_mariadb_4.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 2007s 
    Code: 1748950362
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 2 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [8] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MariaDB-1-1-1024-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590604
    datadisk:1943
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-1-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590604
    datadisk:1971
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-1-3 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590612
    datadisk:1995
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-1-4 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590612
    datadisk:2031
    volume_size:30G
    volume_used:1.9G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590612
    datadisk:2071
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317601456
    datadisk:2091
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-2-3 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317546068
    datadisk:2123
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
                code:1748950362
MariaDB-1-1-1024-2-4 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317534032
    datadisk:2147
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
                code:1748950362

### Execution
                      experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MariaDB-1-1-1024-1-1               1          8    8192          1  120.0           0                        313.33                     312.02         0.0                                                      15358.0                                              25516.0
MariaDB-1-1-1024-1-2               1         16   16384          2  120.0           0                        345.94                     342.71         0.0                                                      23169.0                                              36029.0
MariaDB-1-1-1024-1-3               1          8    8192          2  120.0           0                        417.55                     413.51         0.0                                                      18344.0                                              19118.5
MariaDB-1-1-1024-1-4               1         16   16384          4  120.0           0                        515.34                     507.25         0.0                                                      27275.0                                              28714.0
MariaDB-1-1-1024-2-1               2          8    8192          1  120.0           0                        315.81                     314.26         0.0                                                      16761.0                                              22922.0
MariaDB-1-1-1024-2-2               2         16   16384          2  120.0           0                        344.72                     341.32         0.0                                                      28206.0                                              38851.0
MariaDB-1-1-1024-2-3               2          8    8192          2  120.0           0                        356.69                     352.91         0.0                                                      17531.0                                              18927.5
MariaDB-1-1-1024-2-4               2         16   16384          4  120.0           0                        422.47                     415.79         0.0                                                      29895.0                                              33430.0

### Workflow

#### Actual
DBMS MariaDB-1-1-1024 - Pods [[2, 2, 4, 1], [4, 1, 2, 2]]

#### Planned
DBMS MariaDB-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                      time_load  terminals  pods  Throughput [SF/h]
MariaDB-1-1-1024-1-1      471.0        1.0   1.0         122.292994
MariaDB-1-1-1024-1-2      471.0        1.0   2.0         122.292994
MariaDB-1-1-1024-1-3      471.0        1.0   2.0         122.292994
MariaDB-1-1-1024-1-4      471.0        1.0   4.0         122.292994
MariaDB-1-1-1024-2-1      471.0        1.0   1.0         122.292994
MariaDB-1-1-1024-2-2      471.0        1.0   2.0         122.292994
MariaDB-1-1-1024-2-3      471.0        1.0   2.0         122.292994
MariaDB-1-1-1024-2-4      471.0        1.0   4.0         122.292994

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-1-1-1024-1-1      118.33     0.97          2.43                 2.74
MariaDB-1-1-1024-1-2      135.25     1.52          2.48                 2.79
MariaDB-1-1-1024-1-3      160.10     2.08          2.53                 2.84
MariaDB-1-1-1024-1-4      284.73     1.27          2.58                 2.89
MariaDB-1-1-1024-2-1      892.33     1.27          5.10                 5.60
MariaDB-1-1-1024-2-2      242.03     1.97          2.64                 2.94
MariaDB-1-1-1024-2-3      122.16     1.21          2.66                 2.96
MariaDB-1-1-1024-2-4      235.28     1.32          2.72                 3.02

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-1-1-1024-1-1       82.39     0.00          0.44                 0.44
MariaDB-1-1-1024-1-2      102.54     1.02          1.09                 1.09
MariaDB-1-1-1024-1-3      107.54     0.60          1.29                 1.29
MariaDB-1-1-1024-1-4      135.78     0.36          1.70                 1.70
MariaDB-1-1-1024-2-1       67.23     0.00          0.35                 0.35
MariaDB-1-1-1024-2-2      128.95     0.42          1.05                 1.05
MariaDB-1-1-1024-2-3       87.52     0.32          1.32                 1.32
MariaDB-1-1-1024-2-4       73.72     0.51          1.78                 1.78

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```
















## HammerDB

### PostgreSQL

#### HammerDB Simple

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_postgresql_1.log &
```

yields (after ca. 10 minutes)

test_hammerdb_testcase_postgresql_1.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 865s 
    Code: 1743784383
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:204804716
    datadisk:3298
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1     14.16     17.86         0.0  11286.0  35013.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1       90.0        1.0   1.0                      640.0

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```


#### HammerDB Monitoring

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_postgresql_2.log &
```

yields (after ca. 15 minutes)

test_hammerdb_testcase_postgresql_2.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 920s 
    Code: 1743785313
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201427648
    datadisk:3304
    volume_size:30G
    volume_used:3.3G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1     14.14     17.85         0.0  11171.0  34518.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1      105.0        1.0   1.0                 548.571429

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      132.23     1.15          3.72                 5.31

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      320.94        0          0.08                 0.08

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1    23615.01    56.16          5.37                  7.0

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       53.75     0.14           0.1                  0.1

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### HammerDB Complex

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_postgresql_3.log &
```

yields (after ca. 60 minutes)

test_hammerdb_testcase_postgresql_3.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 3220s 
    Code: 1743786274
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes. Benchmarking also logs latencies.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201507644
    datadisk:4147
    volume_size:30G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201455732
    datadisk:4245
    volume_size:30G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-3 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201507896
    datadisk:4379
    volume_size:30G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-4 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201455844
    datadisk:4472
    volume_size:30G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201455844
    datadisk:4577
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201455844
    datadisk:4648
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-3 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201507928
    datadisk:4743
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-4 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201455844
    datadisk:4815
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                        experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency      NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1-1               1      16       1          1     14.64     18.76         0.0  10672.00  32823.0         2       0
PostgreSQL-BHT-8-1-1-2               1      32       2          2     18.68     25.67         0.0  11106.00  32119.5         2       0
PostgreSQL-BHT-8-1-1-3               1      16       3          2     16.20     19.77         0.0   9620.00  30261.5         2       0
PostgreSQL-BHT-8-1-1-4               1      32       4          4     18.26     25.12         0.0   9579.75  28395.0         2       0
PostgreSQL-BHT-8-1-2-1               2      16       1          1     16.74     21.12         0.0   8528.00  27412.0         2       0
PostgreSQL-BHT-8-1-2-2               2      32       2          2     18.16     24.61         0.0   9384.50  27945.0         2       0
PostgreSQL-BHT-8-1-2-3               2      16       3          2     16.85     20.46         0.0   7836.00  25079.0         2       0
PostgreSQL-BHT-8-1-2-4               2      32       4          4     19.86     28.89         0.0   8515.75  24949.5         2       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[4, 2, 1, 2], [4, 2, 2, 1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1-1      105.0        1.0   1.0                 548.571429
PostgreSQL-BHT-8-1-1-2      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-1-3      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-1-4      105.0        1.0   4.0                 548.571429
PostgreSQL-BHT-8-1-2-1      105.0        1.0   1.0                 548.571429
PostgreSQL-BHT-8-1-2-2      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-2-3      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-2-4      105.0        1.0   4.0                 548.571429

### Execution - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1    11423.99    56.05          4.90                 7.12
PostgreSQL-BHT-8-1-1-2    14150.19    56.45          5.63                 7.94
PostgreSQL-BHT-8-1-1-3    13757.06    56.01          5.33                 7.73
PostgreSQL-BHT-8-1-1-4    14481.77    56.52          5.90                 8.41
PostgreSQL-BHT-8-1-2-1    55294.08    56.15          6.83                10.06
PostgreSQL-BHT-8-1-2-2    14692.67    56.43          5.92                 8.58
PostgreSQL-BHT-8-1-2-3    14194.71    56.04          5.52                 8.23
PostgreSQL-BHT-8-1-2-4    14203.89    56.35          6.11                 8.93

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       29.70     0.12          0.08                 0.08
PostgreSQL-BHT-8-1-1-2       31.54     0.13          0.22                 0.22
PostgreSQL-BHT-8-1-1-3       31.54     0.06          0.22                 0.22
PostgreSQL-BHT-8-1-1-4       22.78     0.06          0.25                 0.25
PostgreSQL-BHT-8-1-2-1       20.25     0.10          0.07                 0.07
PostgreSQL-BHT-8-1-2-2       18.29     0.08          0.20                 0.20
PostgreSQL-BHT-8-1-2-3       29.40     0.09          0.22                 0.22
PostgreSQL-BHT-8-1-2-4       23.50     0.07          0.25                 0.25

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```





### MySQL

#### HammerDB Simple

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mysql_1.log &
```

yields (after ca. 10 minutes)

test_hammerdb_testcase_mysql_1.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1343s 
    Code: 1728551101
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-8-1-1 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:260825196
    datadisk:11108008
    requests_cpu:4
    requests_memory:16Gi

### Execution
                 experiment_run  vusers  client  pod_count    NOPM     TPM  duration  errors
MySQL-BHT-8-1-1               1      16       1          1  3370.0  7789.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MySQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-8-1 - Pods [[1]]

### Loading
                 time_load  terminals  pods  Imported warehouses [1/h]
MySQL-BHT-8-1-1      385.0        1.0   1.0                  149.61039

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```


#### HammerDB Monitoring

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mysql_2.log &
```

yields (after ca. 15 minutes)

test_hammerdb_testcase_mysql_2.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 3696s 
    Code: 1729598045
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-8-1-1 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250540992
    datadisk:11115842
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                 experiment_run  vusers  client  pod_count    NOPM      TPM  duration  errors
MySQL-BHT-8-1-1               1      16       1          1  6218.0  14441.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MySQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-8-1 - Pods [[1]]

### Loading
                 time_load  terminals  pods  Imported warehouses [1/h]
MySQL-BHT-8-1-1     2790.0        1.0   1.0                  20.645161

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1     1277.89     1.02         37.45                45.49

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1      430.29     0.36          0.08                 0.08

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1      772.46     2.43         22.99                 31.5

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1       37.88     0.17          0.06                 0.06

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### HammerDB Complex

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mysql_3.log &
```

yields (after ca. 60 minutes)

test_hammerdb_testcase_mysql_3.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 3490s 
    Code: 1729601826
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-BHT-8-1-1-1 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250540988
    datadisk:11662779
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-8-1-1-2 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250540988
    datadisk:12037972
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-8-1-1-3 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250541160
    datadisk:12787230
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-8-1-1-4 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250541160
    datadisk:13271054
    volume_size:30G
    volume_used:13G
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-8-1-2-1 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250541160
    datadisk:13875869
    volume_size:30G
    volume_used:14G
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-8-1-2-2 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250541160
    datadisk:14505056
    volume_size:30G
    volume_used:14G
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-8-1-2-3 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250541160
    datadisk:15095337
    volume_size:30G
    volume_used:15G
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-8-1-2-4 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250541160
    datadisk:15683884
    volume_size:30G
    volume_used:15G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                   experiment_run  vusers  client  pod_count      NOPM       TPM  duration  errors
MySQL-BHT-8-1-1-1               1      16       1          1   6723.00  15643.00         2       0
MySQL-BHT-8-1-1-2               1      32       2          2  11297.50  26190.00         2       0
MySQL-BHT-8-1-1-3               1      16       3          2   6769.50  15507.50         2       0
MySQL-BHT-8-1-1-4               1      32       4          4   9152.75  21112.75         2       0
MySQL-BHT-8-1-2-1               2      16       1          1   9676.00  22665.00         2       0
MySQL-BHT-8-1-2-2               2      32       2          2   8227.50  19165.00         2       0
MySQL-BHT-8-1-2-3               2      16       3          2   8007.50  18717.00         2       0
MySQL-BHT-8-1-2-4               2      32       4          4   8291.25  19166.00         2       0

Warehouses: 16

### Workflow

#### Actual
DBMS MySQL-BHT-8-1 - Pods [[4, 2, 2, 1], [2, 4, 2, 1]]

#### Planned
DBMS MySQL-BHT-8-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                   time_load  terminals  pods  Imported warehouses [1/h]
MySQL-BHT-8-1-1-1     2790.0        1.0   1.0                  20.645161
MySQL-BHT-8-1-1-2     2790.0        1.0   2.0                  20.645161
MySQL-BHT-8-1-1-3     2790.0        1.0   2.0                  20.645161
MySQL-BHT-8-1-1-4     2790.0        1.0   4.0                  20.645161
MySQL-BHT-8-1-2-1     2790.0        1.0   1.0                  20.645161
MySQL-BHT-8-1-2-2     2790.0        1.0   2.0                  20.645161
MySQL-BHT-8-1-2-3     2790.0        1.0   2.0                  20.645161
MySQL-BHT-8-1-2-4     2790.0        1.0   4.0                  20.645161

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1-1      457.14     2.73         38.73                46.82
MySQL-BHT-8-1-1-2      852.95     3.75         38.95                47.75
MySQL-BHT-8-1-1-3      706.33     2.40         38.99                47.83
MySQL-BHT-8-1-1-4      710.77     3.16         39.06                47.82
MySQL-BHT-8-1-2-1      754.75     2.55         39.13                47.60
MySQL-BHT-8-1-2-2      638.56     3.34         39.19                48.09
MySQL-BHT-8-1-2-3      694.00     2.65         39.20                47.66
MySQL-BHT-8-1-2-4      754.95     3.12         39.22                48.29

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1-1       25.63     0.11          0.06                 0.06
MySQL-BHT-8-1-1-2       43.92     0.14          0.17                 0.17
MySQL-BHT-8-1-1-3       60.66     0.08          0.18                 0.18
MySQL-BHT-8-1-1-4       33.14     0.18          0.20                 0.20
MySQL-BHT-8-1-2-1       47.05     0.19          0.06                 0.06
MySQL-BHT-8-1-2-2       47.05     0.14          0.17                 0.17
MySQL-BHT-8-1-2-3       37.01     0.16          0.18                 0.18
MySQL-BHT-8-1-2-4       41.41     0.17          0.20                 0.20

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```




### MariaDB

#### HammerDB Simple

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mariadb_1.log &
```

yields (after ca. 10 minutes)

test_hammerdb_testcase_mariadb_1.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 994s 
    Code: 1748955374
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-BHT-8-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:333865940
    datadisk:1657
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748955374

### Execution
                   experiment_run  vusers  client  pod_count  efficiency    NOPM      TPM  duration  errors
MariaDB-BHT-8-1-1               1      16       1          1         0.0  7651.0  17791.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MariaDB-BHT-8-1 - Pods [[1]]

#### Planned
DBMS MariaDB-BHT-8-1 - Pods [[1]]

### Loading
                   time_load  terminals  pods  Imported warehouses [1/h]
MariaDB-BHT-8-1-1      230.0        1.0   1.0                 250.434783

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```


#### HammerDB Monitoring

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mariadb_2.log &
```

yields (after ca. 15 minutes)

test_hammerdb_testcase_mariadb_2.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1356s 
    Code: 1748956424
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-BHT-8-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332170252
    datadisk:1639
    volume_size:30G
    volume_used:1.6G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748956424

### Execution
                   experiment_run  vusers  client  pod_count  efficiency    NOPM      TPM  duration  errors
MariaDB-BHT-8-1-1               1      16       1          1         0.0  7101.0  16547.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MariaDB-BHT-8-1 - Pods [[1]]

#### Planned
DBMS MariaDB-BHT-8-1 - Pods [[1]]

### Loading
                   time_load  terminals  pods  Imported warehouses [1/h]
MariaDB-BHT-8-1-1      404.0        1.0   1.0                 142.574257

### Ingestion - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1      649.21     2.08          2.48                 2.51

### Ingestion - Loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1      406.82     1.22          0.09                 0.09

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1      513.03     1.48          2.67                  2.7

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1        48.5      0.1          0.06                 0.06

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### HammerDB Complex

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mariadb_3.log &
```

yields (after ca. 60 minutes)

test_hammerdb_testcase_mariadb_3.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 3244s 
    Code: 1748957864
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MariaDB-BHT-8-1-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332170552
    datadisk:1701
    volume_size:30G
    volume_used:1.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748957864
MariaDB-BHT-8-1-1-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332170556
    datadisk:1737
    volume_size:30G
    volume_used:1.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748957864
MariaDB-BHT-8-1-1-3 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332170560
    datadisk:1757
    volume_size:30G
    volume_used:1.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748957864
MariaDB-BHT-8-1-1-4 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332170656
    datadisk:1785
    volume_size:30G
    volume_used:1.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748957864
MariaDB-BHT-8-1-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332171792
    datadisk:1810
    volume_size:30G
    volume_used:1.8G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748957864
MariaDB-BHT-8-1-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332171796
    datadisk:1846
    volume_size:30G
    volume_used:1.8G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748957864
MariaDB-BHT-8-1-2-3 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332174248
    datadisk:1862
    volume_size:30G
    volume_used:1.8G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748957864
MariaDB-BHT-8-1-2-4 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:332174252
    datadisk:1886
    volume_size:30G
    volume_used:1.8G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748957864

### Execution
                     experiment_run  vusers  client  pod_count  efficiency    NOPM      TPM  duration  errors
MariaDB-BHT-8-1-1-1               1      16       1          1         0.0  7796.0  18205.0         2       0
MariaDB-BHT-8-1-1-2               1      32       2          2         0.0  5306.0  12450.0         2       0
MariaDB-BHT-8-1-1-3               1      16       3          2         0.0  5185.0  11960.0         2       0
MariaDB-BHT-8-1-1-4               1      32       4          4         0.0  5315.0  12280.5         2       0
MariaDB-BHT-8-1-2-1               2      16       1          1         0.0  6297.0  14608.0         2       0
MariaDB-BHT-8-1-2-2               2      32       2          2         0.0  3712.5   8581.0         2       0
MariaDB-BHT-8-1-2-3               2      16       3          2         0.0  6334.5  14797.0         2       0
MariaDB-BHT-8-1-2-4               2      32       4          4         0.0  5927.0  13791.0         2       0

Warehouses: 16

### Workflow

#### Actual
DBMS MariaDB-BHT-8-1 - Pods [[4, 2, 1, 2], [2, 4, 2, 1]]

#### Planned
DBMS MariaDB-BHT-8-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                     time_load  terminals  pods  Imported warehouses [1/h]
MariaDB-BHT-8-1-1-1      404.0        1.0   1.0                 142.574257
MariaDB-BHT-8-1-1-2      404.0        1.0   2.0                 142.574257
MariaDB-BHT-8-1-1-3      404.0        1.0   2.0                 142.574257
MariaDB-BHT-8-1-1-4      404.0        1.0   4.0                 142.574257
MariaDB-BHT-8-1-2-1      404.0        1.0   1.0                 142.574257
MariaDB-BHT-8-1-2-2      404.0        1.0   2.0                 142.574257
MariaDB-BHT-8-1-2-3      404.0        1.0   2.0                 142.574257
MariaDB-BHT-8-1-2-4      404.0        1.0   4.0                 142.574257

### Execution - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1-1      355.16     1.02          2.27                 2.60
MariaDB-BHT-8-1-1-2      335.14     1.44          2.38                 2.71
MariaDB-BHT-8-1-1-3      262.41     0.60          2.40                 2.73
MariaDB-BHT-8-1-1-4      424.14     1.83          2.47                 2.80
MariaDB-BHT-8-1-2-1     1460.46     1.45          4.75                 5.26
MariaDB-BHT-8-1-2-2      286.80     1.15          2.50                 2.81
MariaDB-BHT-8-1-2-3      285.42     1.49          2.53                 2.84
MariaDB-BHT-8-1-2-4      418.14     1.32          2.61                 2.92

### Execution - Benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1-1       32.61     0.09          0.06                 0.06
MariaDB-BHT-8-1-1-2       32.61     0.06          0.17                 0.17
MariaDB-BHT-8-1-1-3       25.25     0.05          0.18                 0.19
MariaDB-BHT-8-1-1-4       24.35     0.07          0.21                 0.21
MariaDB-BHT-8-1-2-1       29.12     0.11          0.06                 0.06
MariaDB-BHT-8-1-2-2       29.12     0.05          0.17                 0.17
MariaDB-BHT-8-1-2-3       21.54     0.06          0.18                 0.18
MariaDB-BHT-8-1-2-4       25.49     0.03          0.21                 0.21

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```
















## YCSB


### YCSB Loader Test for Scaling the Driver

```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 4,8 \
  -nlt 32,64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_1.log &
```

yields (after ca. 15 minutes) something like

test_ycsb_testcase_postgresql_1.log
```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 921s 
    Code: 1728372434
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are [1]. Factors for benchmarking are [1].
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 4 and 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [32, 64] threads, split into [4, 8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-32-4-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251145412
    datadisk:2172140
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-32-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251105492
    datadisk:2138756
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-4-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251129260
    datadisk:2155988
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251062676
    datadisk:2105788
    requests_cpu:4
    requests_memory:16Gi

### Loading
                        experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-32-4-131072               1       32  131072          4                   81569.178833                12610.0             1000000                             2384.50
PostgreSQL-64-4-131072               1       64  131072          4                  100089.555728                10166.0             1000000                             3845.00
PostgreSQL-32-8-131072               1       32  131072          8                   84950.617083                12602.0             1000000                             2431.75
PostgreSQL-64-8-131072               1       64  131072          8                  101721.119844                10182.0             1000000                             4253.25

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-32-4-131072-1               1       64  131072          1                      114586.91                 8727.0            499976                            1243.0              500024                              1796.0
PostgreSQL-32-8-131072-1               1       64  131072          1                      115620.30                 8649.0            499505                            1399.0              500495                              2289.0
PostgreSQL-64-4-131072-1               1       64  131072          1                      116577.29                 8578.0            499190                            1392.0              500810                              2037.0
PostgreSQL-64-8-131072-1               1       64  131072          1                      114390.30                 8742.0            499702                            1449.0              500298                              2749.0

### Workflow

#### Actual
DBMS PostgreSQL-32-8-131072 - Pods [[1]]
DBMS PostgreSQL-64-8-131072 - Pods [[1]]
DBMS PostgreSQL-32-4-131072 - Pods [[1]]
DBMS PostgreSQL-64-4-131072 - Pods [[1]]

#### Planned
DBMS PostgreSQL-32-4-131072 - Pods [[1]]
DBMS PostgreSQL-32-8-131072 - Pods [[1]]
DBMS PostgreSQL-64-4-131072 - Pods [[1]]
DBMS PostgreSQL-64-8-131072 - Pods [[1]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
```

### YCSB Loader Test for Persistency

```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_2.log &
```

yields (after ca. 10 minutes) something like

test_ycsb_testcase_postgresql_2.log
```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 440s 
    Code: 1728373344
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are [1]. Factors for benchmarking are [1].
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-64-8-131072-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973268
    datadisk:2122664
    volume_size:100G
    volume_used:2.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973260
    datadisk:2907528
    volume_size:100G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi

### Loading
                        experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-131072               1       64  131072          8                    95847.48652                10614.0             1000000                             3982.75

### Execution
                            experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1-1               1       64  131072          1                      114403.39                 8741.0            499485                            1400.0              500515                              2007.0
PostgreSQL-64-8-131072-2-1               2       64  131072          1                       57683.43                17336.0            499518                            1456.0              500482                              2014.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-131072 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-64-8-131072 - Pods [[1], [1]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
```


### YCSB Execution for Scaling and Repetition

```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1,2 \
  -nc 2 \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_3.log &
```

yields (after ca. 15 minutes) something like

test_ycsb_testcase_postgresql_3.log
```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 915s 
    Code: 1728373944
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are [1]. Factors for benchmarking are [1].
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-64-8-131072-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:2940752
    volume_size:100G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:2949784
    volume_size:100G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:3137448
    volume_size:100G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:3287608
    volume_size:100G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:3603192
    volume_size:100G
    volume_used:3.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:3606176
    volume_size:100G
    volume_used:3.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:3746688
    volume_size:100G
    volume_used:3.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:3749400
    volume_size:100G
    volume_used:3.5G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                            experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1-1               1       64  131072          1                       66216.40                15102.0            500545                           1352.00              499455                             1709.00
PostgreSQL-64-8-131072-1-3               1       64  131072          8                      112183.71                 9096.0            500166                            859.88              499834                             1405.62
PostgreSQL-64-8-131072-1-2               1      128  262144          2                       86896.65                11590.0            499359                           2025.00              500641                            61167.00
PostgreSQL-64-8-131072-1-4               1      128  262144         16                       95290.13                10945.0            498701                           2764.38              501299                            49865.00
PostgreSQL-64-8-131072-2-1               2       64  131072          1                       43685.29                22891.0            499900                           1355.00              500100                             1694.00
PostgreSQL-64-8-131072-2-3               2       64  131072          8                      125887.08                 8128.0            500524                           1014.38              499476                             1513.12
PostgreSQL-64-8-131072-2-2               2      128  262144          2                       89067.91                11263.0            500138                           2071.00              499862                            55167.00
PostgreSQL-64-8-131072-2-4               2      128  262144         16                      114367.93                 9263.0            499789                           3193.62              500211                            17544.00

### Workflow

#### Actual
DBMS PostgreSQL-64-8-131072 - Pods [[16, 8, 1, 2], [16, 8, 1, 2]]

#### Planned
DBMS PostgreSQL-64-8-131072 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
```


### YCSB Execution Different Workload

```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload e \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_4.log &
```

yields (after ca. 5 minutes) something like

test_ycsb_testcase_postgresql_4.log
```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 232s 
    Code: 1728374844
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'E'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are [1]. Factors for benchmarking are [1].
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:3822840
    volume_size:100G
    volume_used:3.7G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)  [SCAN].Return=OK  [SCAN].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1               1       64  131072          8                       25447.87                40124.0               50240                             2653.75            949760                            5053.5

### Workflow

#### Actual
DBMS PostgreSQL-64-8-131072 - Pods [[8]]

#### Planned
DBMS PostgreSQL-64-8-131072 - Pods [[8]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
```

### YCSB Execution Monitoring

```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 100Gi \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_5.log &
```

yields (after ca. 10 minutes) something like

test_ycsb_testcase_postgresql_5.log
```bash
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 544s 
    Code: 1728376053
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 10000000. Number of operations is 10000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are [1]. Factors for benchmarking are [1].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:34189800
    volume_size:100G
    volume_used:33G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973432
    datadisk:34542952
    volume_size:100G
    volume_used:33G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1               1       64  131072          1                       52891.86               189065.0           4999969                           1914.00             5000031                             3479.00
PostgreSQL-64-8-131072-2               1       64  131072          8                      129612.95                77810.0           4998786                           1210.12             5001214                             1617.88

### Workflow

#### Actual
DBMS PostgreSQL-64-8-131072 - Pods [[8, 1]]

#### Planned
DBMS PostgreSQL-64-8-131072 - Pods [[1, 8]]

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1     2058.53     11.3         16.43                33.51
PostgreSQL-64-8-131072-2      820.51      0.0         19.58                36.25

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1      691.78     1.63          0.60                 0.61
PostgreSQL-64-8-131072-2      282.36     0.00          4.86                 4.89

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


