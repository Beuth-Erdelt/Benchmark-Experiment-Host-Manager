# Test Cases

There is a variety of combination of options to be tested.

We here list some more basic use cases to test the functionality of bexhoma.

See [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/test.sh) for implementations.
You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
```


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
    Duration: 414s 
    Code: 1728147496
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
    disk:251785300
    datadisk:2822552
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2698.29
Minimum Cost Supplier Query (TPC-H Q2)                             451.18
Shipping Priority (TPC-H Q3)                                       776.51
Order Priority Checking Query (TPC-H Q4)                          1311.21
Local Supplier Volume (TPC-H Q5)                                   697.93
Forecasting Revenue Change (TPC-H Q6)                              518.67
Forecasting Revenue Change (TPC-H Q7)                              810.92
National Market Share (TPC-H Q8)                                   635.76
Product Type Profit Measure (TPC-H Q9)                            1228.00
Forecasting Revenue Change (TPC-H Q10)                            1329.29
Important Stock Identification (TPC-H Q11)                         264.15
Shipping Modes and Order Priority (TPC-H Q12)                     1083.43
Customer Distribution (TPC-H Q13)                                 2048.55
Forecasting Revenue Change (TPC-H Q14)                             575.75
Top Supplier Query (TPC-H Q15)                                     601.07
Parts/Supplier Relationship (TPC-H Q16)                            609.70
Small-Quantity-Order Revenue (TPC-H Q17)                          2138.69
Large Volume Customer (TPC-H Q18)                                 6857.13
Discounted Revenue (TPC-H Q19)                                     753.24
Potential Part Promotion (TPC-H Q20)                               727.70
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                964.69
Global Sales Opportunity Query (TPC-H Q22)                         258.75

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           44.0         1.0       90.0     143.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.93

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4008.99

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 1  1              1                 30      1   1                   2640.0

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
    Duration: 689s 
    Code: 1728148096
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
    disk:257345816
    datadisk:8383076
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 6244.23
Minimum Cost Supplier Query (TPC-H Q2)                            2130.48
Shipping Priority (TPC-H Q3)                                      2441.53
Order Priority Checking Query (TPC-H Q4)                          3118.84
Local Supplier Volume (TPC-H Q5)                                  2249.99
Forecasting Revenue Change (TPC-H Q6)                             1154.10
Forecasting Revenue Change (TPC-H Q7)                             2327.41
National Market Share (TPC-H Q8)                                  1392.31
Product Type Profit Measure (TPC-H Q9)                            3122.15
Forecasting Revenue Change (TPC-H Q10)                            3025.70
Important Stock Identification (TPC-H Q11)                         559.61
Shipping Modes and Order Priority (TPC-H Q12)                     2460.50
Customer Distribution (TPC-H Q13)                                 6165.40
Forecasting Revenue Change (TPC-H Q14)                            1266.88
Top Supplier Query (TPC-H Q15)                                    1381.41
Parts/Supplier Relationship (TPC-H Q16)                           1272.46
Small-Quantity-Order Revenue (TPC-H Q17)                          5535.95
Large Volume Customer (TPC-H Q18)                                20719.70
Discounted Revenue (TPC-H Q19)                                    1887.54
Potential Part Promotion (TPC-H Q20)                              1146.13
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               2761.80
Global Sales Opportunity Query (TPC-H Q22)                         454.70

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          129.0         1.0      219.0     359.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1            2.3

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4836.26

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 3  1              1                 77      1   3                  3085.71

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      448.08     1.32          6.39                10.63

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       13.09     0.07          1.29                 2.76

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      363.81     1.42          7.04                11.29

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       13.77        0          0.27                 0.27

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
    Duration: 891s 
    Code: 1728312757
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
    disk:248970540
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
    disk:248970540
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
    disk:248970540
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
    disk:248970540
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
    disk:248970540
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
    disk:248970540
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
Pricing Summary Report (TPC-H Q1)                                  23157.86                 5980.27                 6095.96                19587.35                 6121.09                 6010.60
Minimum Cost Supplier Query (TPC-H Q2)                              9531.24                 2118.82                 2101.45                10425.32                 2107.33                 2111.57
Shipping Priority (TPC-H Q3)                                       13390.17                 2376.80                 2400.88                11021.70                 2433.13                 2377.52
Order Priority Checking Query (TPC-H Q4)                            3050.48                 3006.11                 3007.64                 3061.74                 3051.72                 3075.27
Local Supplier Volume (TPC-H Q5)                                    2171.41                 2180.48                 2205.50                 2149.66                 2208.18                 2198.94
Forecasting Revenue Change (TPC-H Q6)                               1089.17                 1112.82                 1086.41                 1114.39                 1124.15                 1133.55
Forecasting Revenue Change (TPC-H Q7)                               2910.69                 2221.58                 2203.67                 2802.01                 2228.57                 2231.46
National Market Share (TPC-H Q8)                                    1315.77                 1310.74                 1302.77                 1301.54                 1310.28                 1301.75
Product Type Profit Measure (TPC-H Q9)                              4357.16                 3136.03                 3167.76                 4486.49                 3163.53                 3191.25
Forecasting Revenue Change (TPC-H Q10)                              3062.12                 2964.80                 2945.27                 2915.87                 2970.63                 2945.60
Important Stock Identification (TPC-H Q11)                           559.74                  571.92                  566.22                  560.26                  570.24                  577.96
Shipping Modes and Order Priority (TPC-H Q12)                       2369.27                 2393.61                 2350.99                 2349.98                 2382.86                 2401.62
Customer Distribution (TPC-H Q13)                                   6449.74                 6277.40                 6238.73                 6314.22                 6149.98                 6189.48
Forecasting Revenue Change (TPC-H Q14)                              1168.77                 1202.09                 1160.92                 1167.54                 1198.51                 1196.87
Top Supplier Query (TPC-H Q15)                                      1325.56                 1331.05                 1348.85                 1315.20                 1342.89                 1345.28
Parts/Supplier Relationship (TPC-H Q16)                             1253.35                 1322.20                 1280.61                 1292.25                 1304.83                 1299.72
Small-Quantity-Order Revenue (TPC-H Q17)                            5945.32                 5970.66                 5659.44                 5651.47                 5697.80                 5957.67
Large Volume Customer (TPC-H Q18)                                  18198.08                18059.26                18400.25                21541.35                20931.06                18540.88
Discounted Revenue (TPC-H Q19)                                      1811.50                 1831.34                 1811.47                 1804.31                 1815.79                 1818.26
Potential Part Promotion (TPC-H Q20)                                1177.44                 1084.80                 1080.48                 1141.35                 1124.05                 1160.01
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                 4607.63                 2668.06                 2617.49                 3261.69                 2644.11                 2606.13
Global Sales Opportunity Query (TPC-H Q22)                           540.30                  427.52                  433.20                  611.50                  424.44                  431.61

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
PostgreSQL-BHT-8-1-1-1           2.93
PostgreSQL-BHT-8-1-2-1           2.23
PostgreSQL-BHT-8-1-2-2           2.23
PostgreSQL-BHT-8-2-1-1           2.87
PostgreSQL-BHT-8-2-2-1           2.26
PostgreSQL-BHT-8-2-2-2           2.26

### Power@Size
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            3785.39
PostgreSQL-BHT-8-1-2-1            4966.65
PostgreSQL-BHT-8-1-2-2            4999.53
PostgreSQL-BHT-8-2-1-1            3867.17
PostgreSQL-BHT-8-2-2-1            4928.67
PostgreSQL-BHT-8-2-2-2            4939.85

### Throughput@Size
                                                   time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                 SF num_experiment num_client                                              
PostgreSQL-BHT-8-1-1 3  1              1                114      1   3                  2084.21
PostgreSQL-BHT-8-1-2 3  1              2                 76      2   3                  6252.63
PostgreSQL-BHT-8-2-1 3  2              1                110      1   3                  2160.00
PostgreSQL-BHT-8-2-2 3  2              2                 76      2   3                  6252.63

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      147.48     2.51          6.42                10.91
PostgreSQL-BHT-8-1-2      650.25     1.70          7.12                11.84
PostgreSQL-BHT-8-2-1     1007.52     3.53         18.41                27.64
PostgreSQL-BHT-8-2-2      388.57     0.00          6.75                11.49

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       10.31     0.00          0.23                 0.25
PostgreSQL-BHT-8-1-2       27.24     0.51          0.78                 0.81
PostgreSQL-BHT-8-2-1       26.31     0.02          0.77                 0.80
PostgreSQL-BHT-8-2-2       21.65     0.00          0.69                 0.72

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
# Show Summary

### Workload
    Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 619s 
    Code: 1728288333
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
    disk:253378956
    datadisk:4409604
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0                       2622.86                                                      13505.0                                               6094.0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      143.0        1.0   1.0                 402.797203

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
    Code: 1728290056
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
    disk:248969348
    datadisk:4409584
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
    disk:248969520
    datadisk:5131336
    volume_size:50G
    volume_used:4.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  terminals  target  pod_count  time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1         16    8192          1  60.0                       2639.86                                                      13274.0                                               6049.0
PostgreSQL-1-1-1024-2-1               2         16    8192          1  60.0                       1302.11                                                      16165.0                                              12276.0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

### Loading
                         time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1-1      123.0        1.0   1.0                 468.292683
PostgreSQL-1-1-1024-2-1      123.0        1.0   1.0                 468.292683

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
    Duration: 650s 
    Code: 1728290778
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
    disk:253378808
    datadisk:4409284
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0                       2656.71                                                      13156.0                                               6017.0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      131.0        1.0   1.0                 439.694656

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      472.34     1.21          3.68                 4.86

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      977.22        0          1.34                 1.34

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     2590.76      7.5          4.75                 7.08

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1392.81      5.0          1.43                 1.43

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
    Duration: 1686s 
    Code: 1728291644
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
    disk:248969520
    datadisk:4184808
    volume_size:50G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248969520
    datadisk:4290672
    volume_size:50G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248969520
    datadisk:4535672
    volume_size:50G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248969520
    datadisk:4933624
    volume_size:50G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248969520
    datadisk:5852200
    volume_size:50G
    volume_used:5.6G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248969520
    datadisk:5954224
    volume_size:50G
    volume_used:5.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248969520
    datadisk:6205400
    volume_size:50G
    volume_used:5.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248969520
    datadisk:6338424
    volume_size:50G
    volume_used:5.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1          8    8192          1  120.0                       1008.85                                                      12609.0                                              7920.00
PostgreSQL-1-1-1024-1-2               1         16   16384          2  120.0                       2341.82                                                      15682.0                                              6821.00
PostgreSQL-1-1-1024-1-3               1          8    8192          2  120.0                       1318.82                                                      13570.0                                              6054.50
PostgreSQL-1-1-1024-1-4               1         16   16384          4  120.0                       1931.91                                                      18397.0                                              8259.25
PostgreSQL-1-1-1024-2-1               2          8    8192          1  120.0                        965.08                                                      12548.0                                              8279.00
PostgreSQL-1-1-1024-2-2               2         16   16384          2  120.0                       2438.01                                                      15505.0                                              6553.00
PostgreSQL-1-1-1024-2-3               2          8    8192          2  120.0                       1304.04                                                      14123.0                                              6124.50
PostgreSQL-1-1-1024-2-4               2         16   16384          4  120.0                       2031.83                                                      18230.0                                              7862.75

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 4, 2, 1], [4, 2, 2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                         time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1-1      123.0        1.0   1.0                 468.292683
PostgreSQL-1-1-1024-1-2      123.0        1.0   2.0                 468.292683
PostgreSQL-1-1-1024-1-3      123.0        1.0   2.0                 468.292683
PostgreSQL-1-1-1024-1-4      123.0        1.0   4.0                 468.292683
PostgreSQL-1-1-1024-2-1      123.0        1.0   1.0                 468.292683
PostgreSQL-1-1-1024-2-2      123.0        1.0   2.0                 468.292683
PostgreSQL-1-1-1024-2-3      123.0        1.0   2.0                 468.292683
PostgreSQL-1-1-1024-2-4      123.0        1.0   4.0                 468.292683

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      357.31     3.80          2.98                 5.23
PostgreSQL-1-1-1024-1-2      459.40     0.01          3.55                 5.99
PostgreSQL-1-1-1024-1-3      266.30     0.65          3.77                 6.40
PostgreSQL-1-1-1024-1-4      508.81     0.00          4.06                 6.88
PostgreSQL-1-1-1024-2-1      147.84     0.04          7.07                12.78
PostgreSQL-1-1-1024-2-2      853.18     7.09          3.77                 6.92
PostgreSQL-1-1-1024-2-3      367.62     3.69          4.01                 7.27
PostgreSQL-1-1-1024-2-4      702.96     0.00          4.35                 7.82

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      214.14     2.49          1.31                 1.31
PostgreSQL-1-1-1024-1-2      529.77     2.46          3.99                 3.99
PostgreSQL-1-1-1024-1-3      214.14     1.35          4.79                 4.79
PostgreSQL-1-1-1024-1-4      397.75     3.41          4.78                 4.78
PostgreSQL-1-1-1024-2-1      205.66     0.00          2.33                 2.34
PostgreSQL-1-1-1024-2-2      319.01     0.00          3.31                 3.31
PostgreSQL-1-1-1024-2-3      240.69     0.00          5.00                 5.00
PostgreSQL-1-1-1024-2-4      450.79     0.00          6.12                 6.12

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
    Duration: 737s 
    Code: 1728153517
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
    disk:252339876
    datadisk:3376808
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1  11922.0  36996.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1      115.0        1.0   1.0                 500.869565

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
    Duration: 800s 
    Code: 1728154427
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
    disk:248963064
    datadisk:3381973
    volume_size:30G
    volume_used:3.3G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1  11630.0  35956.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1      120.0        1.0   1.0                      480.0

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      134.05     1.55           3.6                 5.97

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      322.02        0          0.07                 0.07

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1    26313.24    62.83          5.16                 5.91

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       45.27     0.11          0.06                 0.06

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
    Duration: 3011s 
    Code: 1728313807
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
    disk:248970540
    datadisk:5346001
    volume_size:30G
    volume_used:5.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970540
    datadisk:5401973
    volume_size:30G
    volume_used:5.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970540
    datadisk:5486093
    volume_size:30G
    volume_used:5.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970540
    datadisk:5551797
    volume_size:30G
    volume_used:5.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970540
    datadisk:5630625
    volume_size:30G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970540
    datadisk:5680885
    volume_size:30G
    volume_used:5.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970708
    datadisk:5750181
    volume_size:30G
    volume_used:5.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970708
    datadisk:5807549
    volume_size:30G
    volume_used:5.6G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                        experiment_run  vusers  client  pod_count    NOPM       TPM  duration  errors
PostgreSQL-BHT-8-1-1-1               1      16       1          1  7680.0  24734.00         2       0
PostgreSQL-BHT-8-1-1-2               1      32       2          2  8949.5  25934.50         2       0
PostgreSQL-BHT-8-1-1-3               1      16       3          2  7227.5  23337.00         2       0
PostgreSQL-BHT-8-1-1-4               1      32       4          4  8070.5  23905.50         2       0
PostgreSQL-BHT-8-1-2-1               2      16       1          1  6596.0  21499.00         2       0
PostgreSQL-BHT-8-1-2-2               2      32       2          2  7463.0  22154.50         2       0
PostgreSQL-BHT-8-1-2-3               2      16       3          2  6707.0  21318.50         2       0
PostgreSQL-BHT-8-1-2-4               2      32       4          4  7200.0  21448.75         2       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[4, 2, 2, 1], [2, 4, 2, 1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1-1      120.0        1.0   1.0                      480.0
PostgreSQL-BHT-8-1-1-2      120.0        1.0   2.0                      480.0
PostgreSQL-BHT-8-1-1-3      120.0        1.0   2.0                      480.0
PostgreSQL-BHT-8-1-1-4      120.0        1.0   4.0                      480.0
PostgreSQL-BHT-8-1-2-1      120.0        1.0   1.0                      480.0
PostgreSQL-BHT-8-1-2-2      120.0        1.0   2.0                      480.0
PostgreSQL-BHT-8-1-2-3      120.0        1.0   2.0                      480.0
PostgreSQL-BHT-8-1-2-4      120.0        1.0   4.0                      480.0

### Execution - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1    12187.83    62.04          5.60                 8.70
PostgreSQL-BHT-8-1-1-2    16003.08    63.64          6.25                 9.46
PostgreSQL-BHT-8-1-1-3    15782.82    55.63          5.90                 9.08
PostgreSQL-BHT-8-1-1-4    15894.09    63.62          6.36                 9.61
PostgreSQL-BHT-8-1-2-1    61981.82    62.89         10.28                16.81
PostgreSQL-BHT-8-1-2-2    15696.92    34.02          6.41                 9.82
PostgreSQL-BHT-8-1-2-3    14798.53    63.03          6.11                 9.56
PostgreSQL-BHT-8-1-2-4    17115.46    63.60          6.55                10.08

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       13.17     0.07          0.06                 0.06
PostgreSQL-BHT-8-1-1-2       13.17     0.06          0.16                 0.17
PostgreSQL-BHT-8-1-1-3       21.22     0.05          0.18                 0.18
PostgreSQL-BHT-8-1-1-4       15.45     0.10          0.20                 0.20
PostgreSQL-BHT-8-1-2-1       21.06     0.06          0.13                 0.13
PostgreSQL-BHT-8-1-2-2       15.85     0.07          0.16                 0.16
PostgreSQL-BHT-8-1-2-3       13.99     0.03          0.18                 0.18
PostgreSQL-BHT-8-1-2-4       15.11     0.03          0.20                 0.20

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
    Duration: 922s 
    Code: 1728294637
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
    disk:251158144
    datadisk:2188444
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-32-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251092320
    datadisk:2139004
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-4-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251092552
    datadisk:2122852
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251206656
    datadisk:2236956
    requests_cpu:4
    requests_memory:16Gi

### Loading
                        experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-32-4-131072               1       32  131072          4                   80283.374645                13080.0             1000000                              2493.5
PostgreSQL-64-4-131072               1       64  131072          4                   99155.844328                10230.0             1000000                              4230.0
PostgreSQL-32-8-131072               1       32  131072          8                   82253.389980                12919.0             1000000                              2419.5
PostgreSQL-64-8-131072               1       64  131072          8                  103530.048470                 9826.0             1000000                              3868.0

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-32-4-131072-1               1       64  131072          1                      116076.61                 8615.0            499607                            1111.0              500393                              1774.0
PostgreSQL-32-8-131072-1               1       64  131072          1                      120322.46                 8311.0            500174                            1302.0              499826                              1839.0
PostgreSQL-64-4-131072-1               1       64  131072          1                      121212.12                 8250.0            498926                             875.0              501074                              1668.0
PostgreSQL-64-8-131072-1               1       64  131072          1                      119703.14                 8354.0            500032                            1341.0              499968                              1920.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-131072 - Pods [[1]]
DBMS PostgreSQL-32-4-131072 - Pods [[1]]
DBMS PostgreSQL-64-4-131072 - Pods [[1]]
DBMS PostgreSQL-32-8-131072 - Pods [[1]]

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
    Duration: 439s 
    Code: 1728295547
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
    disk:248969696
    datadisk:2220744
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
    disk:248969688
    datadisk:2904992
    volume_size:100G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi

### Loading
                        experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-131072               1       64  131072          8                    98820.33019                10300.0             1000000                              3976.0

### Execution
                            experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1-1               1       64  131072          1                      123380.63                 8105.0            500252                            1359.0              499748                              1891.0
PostgreSQL-64-8-131072-2-1               2       64  131072          1                       72040.92                13881.0            499882                            1428.0              500118                              1832.0

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
    Duration: 909s 
    Code: 1728310490
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
    disk:248970368
    datadisk:3227840
    volume_size:100G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970368
    datadisk:3230864
    volume_size:100G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970368
    datadisk:3653712
    volume_size:100G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970368
    datadisk:3836880
    volume_size:100G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970368
    datadisk:4128192
    volume_size:100G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970368
    datadisk:4131720
    volume_size:100G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970368
    datadisk:4277912
    volume_size:100G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248970368
    datadisk:4280752
    volume_size:100G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                            experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1-1               1       64  131072          1                       41480.01                24108.0            498871                           1344.00              501129                             1718.00
PostgreSQL-64-8-131072-1-3               1       64  131072          8                      127182.17                 7886.0            500092                           1056.00              499908                             1521.12
PostgreSQL-64-8-131072-1-2               1      128  262144          2                       88612.54                11354.0            499577                           2089.00              500423                            56719.00
PostgreSQL-64-8-131072-1-4               1      128  262144         16                      102044.13                10115.0            500637                           2847.25              499363                            39921.00
PostgreSQL-64-8-131072-2-1               2       64  131072          1                       32155.37                31099.0            500462                           1444.00              499538                             2121.00
PostgreSQL-64-8-131072-2-3               2       64  131072          8                      126908.33                 7915.0            500151                           1034.50              499849                             1533.38
PostgreSQL-64-8-131072-2-2               2      128  262144          2                       88046.05                11417.0            500312                           1986.00              499688                            61407.00
PostgreSQL-64-8-131072-2-4               2      128  262144         16                       98553.48                10576.0            499669                           2620.88              500331                            46513.00

### Workflow

#### Actual
DBMS PostgreSQL-64-8-131072 - Pods [[8, 16, 1, 2], [16, 8, 1, 2]]

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
    Duration: 262s 
    Code: 1728297047
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
    disk:248969688
    datadisk:3726752
    volume_size:100G
    volume_used:3.6G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)  [SCAN].Return=OK  [SCAN].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1               1       64  131072          8                       24068.35                42214.0               50154                             2958.25            949846                            5449.5

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
  -ne 1 \
  -nc 1 \
  -rst shared -rss 100Gi \
  -m -mc \
  -sf 10 \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_5.log &
```

yields (after ca. 10 minutes) something like

```bash
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 574s 
    Code: 1728297347
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
    disk:248969688
    datadisk:33568432
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
    disk:248969768
    datadisk:33824096
    volume_size:100G
    volume_used:33G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1               1       64  131072          1                       44852.10               222955.0           5001348                           1910.00             4998652                             4099.00
PostgreSQL-64-8-131072-2               1       64  131072          8                      123633.41                82090.0           5000619                           1243.88             4999381                             1676.25

### Workflow

#### Actual
DBMS PostgreSQL-64-8-131072 - Pods [[8, 1]]

#### Planned
DBMS PostgreSQL-64-8-131072 - Pods [[1, 8]]

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1     2008.97    13.49         16.37                33.20
PostgreSQL-64-8-131072-2     1298.10     0.00         18.77                37.93

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1      502.94     3.47          0.60                 0.61
PostgreSQL-64-8-131072-2      438.98     0.00          5.11                 5.14

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
