# Test Cases

There is a variety of combinations of options to be tested.

We here list some more basic use cases to test the functionality of bexhoma.

See [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/test.sh) for implementations.
You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
```

See also [more test cases](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/test-more.sh) for more and longer running test cases.

See the [log folder](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/logs_tests) for some demo test logs.
The folder also contains `*_summary.txt` files containing only the result summary.

## TPC-H

### TPC-H Simple

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
  run </dev/null &>$LOG_DIR/test_tpch_testcase_1.log &
```

yields (after ca. 10 minutes) something like

```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 395s 
    Code: 1728361603
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
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
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251795692
    datadisk:2822920
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2549.74
Minimum Cost Supplier Query (TPC-H Q2)                             415.74
Shipping Priority (TPC-H Q3)                                       733.29
Order Priority Checking Query (TPC-H Q4)                          1254.07
Local Supplier Volume (TPC-H Q5)                                   639.37
Forecasting Revenue Change (TPC-H Q6)                              482.92
Forecasting Revenue Change (TPC-H Q7)                              740.74
National Market Share (TPC-H Q8)                                   598.07
Product Type Profit Measure (TPC-H Q9)                            1078.12
Forecasting Revenue Change (TPC-H Q10)                            1232.80
Important Stock Identification (TPC-H Q11)                         240.49
Shipping Modes and Order Priority (TPC-H Q12)                     1005.48
Customer Distribution (TPC-H Q13)                                 1950.84
Forecasting Revenue Change (TPC-H Q14)                             529.70
Top Supplier Query (TPC-H Q15)                                     540.08
Parts/Supplier Relationship (TPC-H Q16)                            558.28
Small-Quantity-Order Revenue (TPC-H Q17)                          1881.90
Large Volume Customer (TPC-H Q18)                                 6610.72
Discounted Revenue (TPC-H Q19)                                     676.85
Potential Part Promotion (TPC-H Q20)                               660.39
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                882.81
Global Sales Opportunity Query (TPC-H Q22)                         233.04

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           28.0         1.0       85.0     123.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.87

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1             4353.6

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 1  1              1                 29      1   1                  2731.03

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Workflow as planned
```


### TPC-H Monitoring

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 3 \
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
  run </dev/null &>$LOG_DIR/test_tpch_testcase_2.log &
```

yields (after ca. 15 minutes) something like

```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 697s 
    Code: 1728362203
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
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
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:257355516
    datadisk:8382744
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 6188.25
Minimum Cost Supplier Query (TPC-H Q2)                            2139.91
Shipping Priority (TPC-H Q3)                                      2465.94
Order Priority Checking Query (TPC-H Q4)                          3098.34
Local Supplier Volume (TPC-H Q5)                                  2234.01
Forecasting Revenue Change (TPC-H Q6)                             1169.42
Forecasting Revenue Change (TPC-H Q7)                             2308.18
National Market Share (TPC-H Q8)                                  1403.55
Product Type Profit Measure (TPC-H Q9)                            3196.47
Forecasting Revenue Change (TPC-H Q10)                            3050.28
Important Stock Identification (TPC-H Q11)                         564.12
Shipping Modes and Order Priority (TPC-H Q12)                     2465.84
Customer Distribution (TPC-H Q13)                                 6394.45
Forecasting Revenue Change (TPC-H Q14)                            1279.43
Top Supplier Query (TPC-H Q15)                                    1383.83
Parts/Supplier Relationship (TPC-H Q16)                           1237.19
Small-Quantity-Order Revenue (TPC-H Q17)                          5813.28
Large Volume Customer (TPC-H Q18)                                18993.96
Discounted Revenue (TPC-H Q19)                                    1900.15
Potential Part Promotion (TPC-H Q20)                              1140.97
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               2740.64
Global Sales Opportunity Query (TPC-H Q22)                         461.98

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          114.0         1.0      214.0     338.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           2.31

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4827.78

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 3  1              1                 76      1   3                  3126.32

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      394.27     1.19           6.4                10.64

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       12.29     0.02          0.68                  2.2

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      233.77     3.81           6.6                10.84

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       10.68        0          0.23                 0.23

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

### TPC-H Throughput Test

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 3 \
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
  run </dev/null &>$LOG_DIR/test_tpch_testcase_3.log &
```

yields (after ca. 15 minutes) something like

```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 1072s 
    Code: 1728362814
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248972920
    datadisk:8382736
    volume_size:100G
    volume_used:8.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248972920
    datadisk:8382736
    volume_size:100G
    volume_used:8.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248972920
    datadisk:8382736
    volume_size:100G
    volume_used:8.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248972920
    datadisk:8382736
    volume_size:100G
    volume_used:8.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-2-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248972920
    datadisk:8382736
    volume_size:100G
    volume_used:8.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-2-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248972920
    datadisk:8382736
    volume_size:100G
    volume_used:8.0G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                                  28774.53                 6255.83                 6330.59                25671.58                 6201.49                 6195.51
Minimum Cost Supplier Query (TPC-H Q2)                             10413.84                 2126.42                 2099.33                10460.83                 2110.79                 2127.59
Shipping Priority (TPC-H Q3)                                       14378.16                 2383.16                 2406.74                13388.90                 2355.14                 2402.92
Order Priority Checking Query (TPC-H Q4)                            3008.56                 3046.99                 3050.63                 3029.97                 2993.34                 3110.61
Local Supplier Volume (TPC-H Q5)                                    2157.27                 2187.72                 2191.40                 2133.28                 2161.12                 2198.97
Forecasting Revenue Change (TPC-H Q6)                               1263.05                 1099.11                 1101.23                 1058.01                 1076.21                 1096.33
Forecasting Revenue Change (TPC-H Q7)                               3264.66                 2248.22                 2241.62                 3076.43                 2228.75                 2265.50
National Market Share (TPC-H Q8)                                    1435.47                 1357.67                 1364.25                 1423.41                 1338.03                 1363.09
Product Type Profit Measure (TPC-H Q9)                              5380.11                 3079.21                 3043.65                 4835.81                 3089.72                 3096.31
Forecasting Revenue Change (TPC-H Q10)                              2920.44                 2973.00                 2986.13                 2959.76                 2995.91                 3010.49
Important Stock Identification (TPC-H Q11)                           555.18                  574.33                  564.39                  556.34                  567.54                  570.27
Shipping Modes and Order Priority (TPC-H Q12)                       2374.47                 2419.13                 2393.08                 2345.71                 2414.94                 2339.50
Customer Distribution (TPC-H Q13)                                   6205.70                 6213.67                 6204.13                 6421.12                 6292.80                 6245.61
Forecasting Revenue Change (TPC-H Q14)                              1165.72                 1191.91                 1181.76                 1163.81                 1171.56                 1222.00
Top Supplier Query (TPC-H Q15)                                      1316.85                 1364.25                 1339.85                 1304.56                 1332.20                 1353.76
Parts/Supplier Relationship (TPC-H Q16)                             1288.95                 1267.52                 1262.29                 1288.17                 1300.14                 1296.08
Small-Quantity-Order Revenue (TPC-H Q17)                            5593.77                 6037.71                 5787.40                 5574.56                 5673.59                 5540.64
Large Volume Customer (TPC-H Q18)                                  19132.35                19143.66                21471.62                18510.24                19988.95                18155.58
Discounted Revenue (TPC-H Q19)                                      1807.32                 1839.16                 1805.40                 1823.37                 1841.21                 1862.83
Potential Part Promotion (TPC-H Q20)                                1123.15                 1134.22                 1133.96                 1139.19                 1090.33                 1079.45
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                 4054.44                 2640.55                 2614.18                 4015.19                 2681.75                 2626.07
Global Sales Opportunity Query (TPC-H Q22)                           674.49                  440.10                  430.68                  635.75                  439.70                  448.26

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           80.0         1.0      211.0     300.0
PostgreSQL-BHT-8-1-2-1           1.0           80.0         1.0      211.0     300.0
PostgreSQL-BHT-8-1-2-2           1.0           80.0         1.0      211.0     300.0
PostgreSQL-BHT-8-2-1-1           1.0           80.0         1.0      211.0     300.0
PostgreSQL-BHT-8-2-2-1           1.0           80.0         1.0      211.0     300.0
PostgreSQL-BHT-8-2-2-2           1.0           80.0         1.0      211.0     300.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           3.05
PostgreSQL-BHT-8-1-2-1           2.26
PostgreSQL-BHT-8-1-2-2           2.26
PostgreSQL-BHT-8-2-1-1           2.99
PostgreSQL-BHT-8-2-2-1           2.24
PostgreSQL-BHT-8-2-2-2           2.26

### Power@Size
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            3637.33
PostgreSQL-BHT-8-1-2-1            4921.09
PostgreSQL-BHT-8-1-2-2            4927.84
PostgreSQL-BHT-8-2-1-1            3736.74
PostgreSQL-BHT-8-2-2-1            4954.87
PostgreSQL-BHT-8-2-2-2            4944.99

### Throughput@Size
                                                   time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                 SF num_experiment num_client                                              
PostgreSQL-BHT-8-1-1 3  1              1                122      1   3                  1947.54
PostgreSQL-BHT-8-1-2 3  1              2                 77      2   3                  6171.43
PostgreSQL-BHT-8-2-1 3  2              1                117      1   3                  2030.77
PostgreSQL-BHT-8-2-2 3  2              2                 75      2   3                  6336.00

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      289.51     4.17         17.97                22.46
PostgreSQL-BHT-8-1-2      711.02     7.90          7.29                11.99
PostgreSQL-BHT-8-2-1     1071.40     3.68         22.69                31.89
PostgreSQL-BHT-8-2-2      702.27     7.46          7.21                11.94

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       13.05     0.04          0.26                 0.27
PostgreSQL-BHT-8-1-2       27.11     0.04          0.79                 0.83
PostgreSQL-BHT-8-2-1       24.52     0.00          0.76                 0.79
PostgreSQL-BHT-8-2-2       25.94     0.00          0.80                 0.84

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


















## Benchbase

### Benchbase Simple

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
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_1.log &
```

yields (after ca. 10 minutes) something like

```bash
## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 619s 
    Code: 1728364014
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
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
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:253382488
    datadisk:4409564
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0                       2624.39                                                      13535.0                                               6091.0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      122.0        1.0   1.0                 472.131148

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### Benchbase Persistency


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
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_2.log &
```

yields (after ca. 10 minutes) something like

```bash
## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 615s 
    Code: 1728377399
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 1 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973600
    datadisk:4408496
    volume_size:50G
    volume_used:4.3G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973600
    datadisk:5128456
    volume_size:50G
    volume_used:4.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  terminals  target  pod_count  time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1         16    8192          1  60.0                       2580.81                                                      13774.0                                               6189.0
PostgreSQL-1-1-1024-2-1               2         16    8192          1  60.0                       1567.45                                                      15174.0                                              10196.0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

### Loading
                         time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1-1      124.0        1.0   1.0                 464.516129
PostgreSQL-1-1-1024-2-1      124.0        1.0   1.0                 464.516129

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### Benchbase Monitoring

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
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_3.log &
```

yields (after ca. 10 minutes) something like

```bash
## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 703s 
    Code: 1728365224
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
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
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:253381940
    datadisk:4409016
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0                        2636.1                                                      13278.0                                               6064.0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      134.0        1.0   1.0                 429.850746

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      659.59        0          3.86                 5.21

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      984.23        0          1.32                 1.32

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     2483.87      7.5           4.8                 7.07

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1220.75     5.13          1.42                 1.42

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

### Benchbase Complex

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
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_4.log &
```

yields (after ca. 30 minutes) something like

```bash
## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 1815s 
    Code: 1728365824
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 2 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [8] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248972920
    datadisk:4253224
    volume_size:50G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248972920
    datadisk:4360816
    volume_size:50G
    volume_used:4.2G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248972920
    datadisk:4610952
    volume_size:50G
    volume_used:4.2G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973088
    datadisk:4815168
    volume_size:50G
    volume_used:4.2G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973088
    datadisk:5757792
    volume_size:50G
    volume_used:5.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973088
    datadisk:5851808
    volume_size:50G
    volume_used:5.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973088
    datadisk:6107848
    volume_size:50G
    volume_used:5.8G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973088
    datadisk:6240536
    volume_size:50G
    volume_used:5.8G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1          8    8192          1  120.0                       1012.67                                                      12774.0                                              7890.00
PostgreSQL-1-1-1024-1-2               1         16   16384          2  120.0                       2357.22                                                      15474.0                                              6777.50
PostgreSQL-1-1-1024-1-3               1          8    8192          2  120.0                       1336.68                                                      13740.0                                              5974.50
PostgreSQL-1-1-1024-1-4               1         16   16384          4  120.0                       2011.68                                                      18122.0                                              7941.00
PostgreSQL-1-1-1024-2-1               2          8    8192          1  120.0                        891.60                                                      12931.0                                              8962.00
PostgreSQL-1-1-1024-2-2               2         16   16384          2  120.0                       2492.58                                                      15034.0                                              6408.50
PostgreSQL-1-1-1024-2-3               2          8    8192          2  120.0                       1309.07                                                      13692.0                                              6101.00
PostgreSQL-1-1-1024-2-4               2         16   16384          4  120.0                       2114.70                                                      17884.0                                              7554.25

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[4, 1, 2, 2], [2, 4, 2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                         time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1-1      138.0        1.0   1.0                 417.391304
PostgreSQL-1-1-1024-1-2      138.0        1.0   2.0                 417.391304
PostgreSQL-1-1-1024-1-3      138.0        1.0   2.0                 417.391304
PostgreSQL-1-1-1024-1-4      138.0        1.0   4.0                 417.391304
PostgreSQL-1-1-1024-2-1      138.0        1.0   1.0                 417.391304
PostgreSQL-1-1-1024-2-2      138.0        1.0   2.0                 417.391304
PostgreSQL-1-1-1024-2-3      138.0        1.0   2.0                 417.391304
PostgreSQL-1-1-1024-2-4      138.0        1.0   4.0                 417.391304

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      307.76     0.79          3.17                 5.34
PostgreSQL-1-1-1024-1-2      800.87     5.16          3.68                 6.10
PostgreSQL-1-1-1024-1-3      379.59     3.71          3.79                 6.33
PostgreSQL-1-1-1024-1-4      645.62     0.00          4.10                 6.81
PostgreSQL-1-1-1024-2-1      200.40     0.00          7.12                12.57
PostgreSQL-1-1-1024-2-2      594.14     6.92          3.75                 6.68
PostgreSQL-1-1-1024-2-3      332.17     0.00          3.98                 7.07
PostgreSQL-1-1-1024-2-4      524.93     5.88          4.28                 7.56

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      156.04     2.42          1.30                 1.30
PostgreSQL-1-1-1024-1-2      439.22     2.33          3.98                 3.98
PostgreSQL-1-1-1024-1-3      137.94     1.17          4.99                 4.99
PostgreSQL-1-1-1024-1-4      403.18     2.03          5.69                 5.69
PostgreSQL-1-1-1024-2-1      286.30     0.00          3.48                 3.48
PostgreSQL-1-1-1024-2-2      400.56     4.87          3.46                 3.46
PostgreSQL-1-1-1024-2-3      185.68     1.21          4.84                 4.84
PostgreSQL-1-1-1024-2-4      376.12     1.07          5.69                 5.69

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```
















## HammerDB

### HammerDB Simple

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_1.log &
```

yields (after ca. 10 minutes)

```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 770s 
    Code: 1728367624
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Benchmark is limited to DBMS PostgreSQL.
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
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:252350208
    datadisk:3377108
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1  12327.0  38185.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1      100.0        1.0   1.0                      576.0

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```


### HammerDB Monitoring

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_2.log &
```

yields (after ca. 15 minutes)

```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 743s 
    Code: 1728368534
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS PostgreSQL.
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
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973096
    datadisk:3382309
    volume_size:30G
    volume_used:3.3G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1  11802.0  36290.0         5       0

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
PostgreSQL-BHT-8-1-1      132.63        0           3.6                 5.17

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      313.97     3.91          0.08                 0.08

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1    24028.25    62.68          5.23                 5.98

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       41.13     0.12          0.06                 0.06

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

### HammerDB Complex

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
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_3.log &
```

yields (after ca. 60 minutes)

```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 2952s 
    Code: 1728369434
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS PostgreSQL.
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
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973088
    datadisk:4271825
    volume_size:30G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973088
    datadisk:4381053
    volume_size:30G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973260
    datadisk:4518981
    volume_size:30G
    volume_used:4.4G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973260
    datadisk:4612853
    volume_size:30G
    volume_used:4.4G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973260
    datadisk:4723305
    volume_size:30G
    volume_used:4.6G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973260
    datadisk:4800493
    volume_size:30G
    volume_used:4.6G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973260
    datadisk:4896269
    volume_size:30G
    volume_used:4.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248973260
    datadisk:4973413
    volume_size:30G
    volume_used:4.7G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                        experiment_run  vusers  client  pod_count      NOPM       TPM  duration  errors
PostgreSQL-BHT-8-1-1-1               1      16       1          1  11270.00  34720.00         2       0
PostgreSQL-BHT-8-1-1-2               1      32       2          2  11911.00  34174.00         2       0
PostgreSQL-BHT-8-1-1-3               1      16       3          2   9501.00  30528.00         2       0
PostgreSQL-BHT-8-1-1-4               1      32       4          4  10493.75  30457.00         2       0
PostgreSQL-BHT-8-1-2-1               2      16       1          1   9321.00  29595.00         2       0
PostgreSQL-BHT-8-1-2-2               2      32       2          2   9774.50  29075.00         2       0
PostgreSQL-BHT-8-1-2-3               2      16       3          2   8431.50  27259.50         2       0
PostgreSQL-BHT-8-1-2-4               2      32       4          4   9388.50  27705.25         2       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[4, 2, 2, 1], [4, 2, 2, 1]]

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
PostgreSQL-BHT-8-1-1-1    12388.02    62.87          4.93                 7.08
PostgreSQL-BHT-8-1-1-2    15488.14    63.34          5.66                 6.45
PostgreSQL-BHT-8-1-1-3    13984.22    62.61          5.48                 6.07
PostgreSQL-BHT-8-1-1-4    16457.37    63.57          5.82                 6.55
PostgreSQL-BHT-8-1-2-1    62443.35    62.86          9.37                12.67
PostgreSQL-BHT-8-1-2-2    14557.97    63.59          5.82                 6.78
PostgreSQL-BHT-8-1-2-3    15711.78    62.81          5.62                 6.62
PostgreSQL-BHT-8-1-2-4    16178.21    56.23          6.21                 6.86

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       19.07     0.10          0.05                 0.06
PostgreSQL-BHT-8-1-1-2       19.07     0.07          0.16                 0.16
PostgreSQL-BHT-8-1-1-3       27.48     0.04          0.18                 0.18
PostgreSQL-BHT-8-1-1-4       17.28     0.08          0.20                 0.20
PostgreSQL-BHT-8-1-2-1       26.36     0.08          0.19                 0.19
PostgreSQL-BHT-8-1-2-2       18.35     0.09          0.17                 0.17
PostgreSQL-BHT-8-1-2-3       18.56     0.05          0.18                 0.18
PostgreSQL-BHT-8-1-2-4       16.30     0.06          0.20                 0.20

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
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_1.log &
```

yields (after ca. 15 minutes) something like

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
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_2.log &
```

yields (after ca. 10 minutes) something like

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
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_3.log &
```

yields (after ca. 15 minutes) something like

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
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_4.log &
```

yields (after ca. 5 minutes) something like

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



















## Preinstalled YugabyteDB

### YCSB Execution

`python ycsb.py -ltf 1 -nlp 8 -su 64 -sf 1 -dbms YugabyteDB -wl a run`

* 1 million rows and operations
* workload A
* 64 loader threads, split into 8 parallel pods
* 64 execution threads, split into 8 parallel pods
* target is 16384 ops

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries. YCSB is performed using several threads and processes. Benchmark is limited to DBMS ['YugabyteDB']. YCSB data is loaded using several processes. Benchmark is limited to DBMS YugabyteDB.

### Connections
YugabyteDB-64-8-16384-1 uses docker image postgres:15.0
    RAM:540695855104
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.4.0-72-generic
    node:cl-worker25
    disk:938296156
    datadisk:39268
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-16384               1       64   16384          8                   11738.352404                 8986.0              100000                             71511.0

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-16384-1               1       64   16384          8                       15604.18                64635.0            499732                           68327.0              500268                             69399.0
```

### YCSB Execution Monitoring

`python ycsb.py -ltf 1 -nlp 8 -su 64 -sf 1 -dbms YugabyteDB -wl a -m -mc run`

* 1 million rows and operations
* workload A
* 64 loader threads, split into 8 parallel pods
* 64 execution threads, split into 8 parallel pods
* target is 16384 ops
* monitoring of all components activated

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries. YCSB is performed using several threads and processes. Benchmark is limited to DBMS ['YugabyteDB']. YCSB data is loaded using several processes. Benchmark is limited to DBMS YugabyteDB.

### Connections
YugabyteDB-64-8-16384-1 uses docker image postgres:15.0
    RAM:540695855104
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.4.0-72-generic
    node:cl-worker25
    disk:938298856
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-16384               1       64   16384          8                    12924.07433                 8054.0              100000                             70599.0

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-16384-1               1       64   16384          8                       15514.99                65317.0            500826                           68119.0              499174                             69303.0

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-16384-1        0.07      0.0          0.05                 0.08

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-16384-1        0.13        0          0.01                 0.01

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-16384-1        0.02      0.0          0.05                 0.08

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-16384-1       65.64        0          1.18                 1.21
```
