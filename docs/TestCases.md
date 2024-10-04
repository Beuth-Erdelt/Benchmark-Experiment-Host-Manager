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

```
python tpch.py -ms 1 -tr \
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
    run
```

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    TPC-H Queries SF=1
    Type: tpch
    Duration: 396s 
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
    disk:250350012
    datadisk:2822128
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2518.05
Minimum Cost Supplier Query (TPC-H Q2)                             425.98
Shipping Priority (TPC-H Q3)                                       728.71
Order Priority Checking Query (TPC-H Q4)                          1223.85
Local Supplier Volume (TPC-H Q5)                                   636.65
Forecasting Revenue Change (TPC-H Q6)                              485.96
Forecasting Revenue Change (TPC-H Q7)                              752.28
National Market Share (TPC-H Q8)                                   600.46
Product Type Profit Measure (TPC-H Q9)                            1057.89
Forecasting Revenue Change (TPC-H Q10)                            1200.26
Important Stock Identification (TPC-H Q11)                         238.03
Shipping Modes and Order Priority (TPC-H Q12)                      980.31
Customer Distribution (TPC-H Q13)                                 1944.32
Forecasting Revenue Change (TPC-H Q14)                             518.97
Top Supplier Query (TPC-H Q15)                                     534.09
Parts/Supplier Relationship (TPC-H Q16)                            562.49
Small-Quantity-Order Revenue (TPC-H Q17)                          1911.99
Large Volume Customer (TPC-H Q18)                                 6459.88
Discounted Revenue (TPC-H Q19)                                     673.38
Potential Part Promotion (TPC-H Q20)                               654.71
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                887.67
Global Sales Opportunity Query (TPC-H Q22)                         229.98

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           28.0         1.0       85.0     123.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.86

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4380.38

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 1  1              1                 28      1   1                  2828.57

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

```
python tpch.py -ms 1 -tr \
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
    run
```

yields (after ca. 15 minutes) something like

```
## Show Summary

### Workload
    TPC-H Queries SF=3
    Type: tpch
    Duration: 689s 
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
    disk:257273840
    datadisk:8383832
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 6192.75
Minimum Cost Supplier Query (TPC-H Q2)                            2091.15
Shipping Priority (TPC-H Q3)                                      2424.71
Order Priority Checking Query (TPC-H Q4)                          3061.48
Local Supplier Volume (TPC-H Q5)                                  2210.63
Forecasting Revenue Change (TPC-H Q6)                             1139.04
Forecasting Revenue Change (TPC-H Q7)                             2284.62
National Market Share (TPC-H Q8)                                  1404.12
Product Type Profit Measure (TPC-H Q9)                            3123.02
Forecasting Revenue Change (TPC-H Q10)                            3004.63
Important Stock Identification (TPC-H Q11)                         551.70
Shipping Modes and Order Priority (TPC-H Q12)                     2425.46
Customer Distribution (TPC-H Q13)                                 6418.72
Forecasting Revenue Change (TPC-H Q14)                            1257.36
Top Supplier Query (TPC-H Q15)                                    1368.61
Parts/Supplier Relationship (TPC-H Q16)                           1267.73
Small-Quantity-Order Revenue (TPC-H Q17)                          5629.60
Large Volume Customer (TPC-H Q18)                                20725.30
Discounted Revenue (TPC-H Q19)                                    1924.23
Potential Part Promotion (TPC-H Q20)                              1164.31
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               2731.14
Global Sales Opportunity Query (TPC-H Q22)                         459.42

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          111.0         1.0      215.0     335.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1            2.3

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4848.96

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 3  1              1                 80      1   3                   2970.0

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      398.22     2.09          6.51                10.76

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        8.63        0          0.77                 2.28

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      384.69     3.64          6.82                11.07

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        11.5        0          0.23                 0.24

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

```
python tpch.py -ms 1 -tr \
    -sf 1 \
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
    run
```

yields (after ca. 15 minutes) something like

```
## Show Summary

### Workload
    TPC-H Queries SF=1
    Type: tpch
    Duration: 929s 
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
TPC-H (SF=1) data is loaded and benchmark is executed.
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
    disk:248936652
    datadisk:2822736
    volume_size:100G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248936860
    datadisk:2822736
    volume_size:100G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248936860
    datadisk:2822736
    volume_size:100G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248936840
    datadisk:2822736
    volume_size:100G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-2-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248936840
    datadisk:2822736
    volume_size:100G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-2-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248936840
    datadisk:2822736
    volume_size:100G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                                   2756.00                 2534.75                 2535.25                14119.18                 2565.51                 2571.79
Minimum Cost Supplier Query (TPC-H Q2)                               464.38                  432.43                  431.94                 5324.89                  434.76                  431.71
Shipping Priority (TPC-H Q3)                                         770.36                  723.43                  730.39                 6792.36                  760.45                  776.70
Order Priority Checking Query (TPC-H Q4)                            1334.68                 1309.18                 1300.62                 1246.18                 1256.42                 1251.28
Local Supplier Volume (TPC-H Q5)                                     668.90                  632.22                  637.11                  653.33                  661.63                  679.79
Forecasting Revenue Change (TPC-H Q6)                                511.75                  486.05                  488.62                  500.62                  510.86                  520.06
Forecasting Revenue Change (TPC-H Q7)                                833.18                  743.39                  747.72                 1150.01                  741.63                  769.24
National Market Share (TPC-H Q8)                                     675.09                  590.59                  601.45                  674.49                  607.47                  623.72
Product Type Profit Measure (TPC-H Q9)                              1167.95                 1090.70                 1111.11                 1533.60                 1086.91                 1087.04
Forecasting Revenue Change (TPC-H Q10)                              1324.00                 1242.58                 1251.42                 1248.54                 1276.28                 1273.38
Important Stock Identification (TPC-H Q11)                           263.13                  251.19                  248.92                  242.83                  251.04                  251.12
Shipping Modes and Order Priority (TPC-H Q12)                       1062.88                 1003.16                 1006.56                 1016.53                 1032.74                 1034.17
Customer Distribution (TPC-H Q13)                                   2215.76                 2038.91                 2046.91                 2043.55                 2053.20                 2037.29
Forecasting Revenue Change (TPC-H Q14)                               556.32                  525.59                  532.72                  535.73                  561.66                  547.04
Top Supplier Query (TPC-H Q15)                                       603.09                  531.66                  539.34                  545.08                  566.37                  556.02
Parts/Supplier Relationship (TPC-H Q16)                              608.66                  572.70                  576.08                  559.47                  571.74                  569.10
Small-Quantity-Order Revenue (TPC-H Q17)                            2104.29                 2007.04                 2029.72                 1850.03                 1913.35                 1902.69
Large Volume Customer (TPC-H Q18)                                   7351.66                 7261.50                 7169.16                 6362.48                 7198.30                 7305.13
Discounted Revenue (TPC-H Q19)                                       693.49                  681.62                  680.98                  686.90                  696.24                  700.38
Potential Part Promotion (TPC-H Q20)                                 712.03                  643.07                  657.41                  925.62                  639.74                  630.51
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  903.24                  848.23                  849.80                 1991.62                  851.09                  848.94
Global Sales Opportunity Query (TPC-H Q22)                           256.00                  227.17                  226.61                  256.98                  216.10                  215.28

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           28.0         1.0      102.0     139.0
PostgreSQL-BHT-8-1-2-1           1.0           28.0         1.0      102.0     139.0
PostgreSQL-BHT-8-1-2-2           1.0           28.0         1.0      102.0     139.0
PostgreSQL-BHT-8-2-1-1           1.0           28.0         1.0      102.0     139.0
PostgreSQL-BHT-8-2-2-1           1.0           28.0         1.0      102.0     139.0
PostgreSQL-BHT-8-2-2-2           1.0           28.0         1.0      102.0     139.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           0.94
PostgreSQL-BHT-8-1-2-1           0.87
PostgreSQL-BHT-8-1-2-2           0.88
PostgreSQL-BHT-8-2-1-1           1.28
PostgreSQL-BHT-8-2-2-1           0.88
PostgreSQL-BHT-8-2-2-2           0.88

### Power@Size
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            4021.39
PostgreSQL-BHT-8-1-2-1            4308.46
PostgreSQL-BHT-8-1-2-2            4285.89
PostgreSQL-BHT-8-2-1-1            2923.32
PostgreSQL-BHT-8-2-2-1            4260.41
PostgreSQL-BHT-8-2-2-2            4249.41

### Throughput@Size
                                                   time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                 SF num_experiment num_client                                              
PostgreSQL-BHT-8-1-1 1  1              1                 31      1   1                  2554.84
PostgreSQL-BHT-8-1-2 1  1              2                 30      2   1                  5280.00
PostgreSQL-BHT-8-2-1 1  2              1                 54      1   1                  1466.67
PostgreSQL-BHT-8-2-2 1  2              2                 30      2   1                  5280.00

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[1, 1]]
DBMS PostgreSQL-BHT-8-2 - Pods [[1, 1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      107.31     1.01          3.69                 5.46
PostgreSQL-BHT-8-1-2      107.31     1.01          3.69                 5.46

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1           0        0           0.0                  0.0
PostgreSQL-BHT-8-1-2           0        0           0.0                  0.0

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      115.94     1.97          3.80                 5.26
PostgreSQL-BHT-8-1-2        0.27     0.01          3.80                 5.26
PostgreSQL-BHT-8-2-1      111.47     1.93          7.59                10.44
PostgreSQL-BHT-8-2-2      220.68     0.00          3.78                 5.18

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       13.50      0.0          0.26                 0.27
PostgreSQL-BHT-8-1-2        0.00      0.0          0.26                 0.27
PostgreSQL-BHT-8-2-1       13.50      0.0          0.26                 0.27
PostgreSQL-BHT-8-2-2       24.07      0.0          0.74                 0.77

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]

TEST failed: Workflow not as planned
```


















## Benchbase

### Benchbase Simple

```
python benchbase.py -ms 1 -tr \
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
    run
```

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 619s 
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
    disk:253346796
    datadisk:4409948
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0                       2638.88                                                      13239.0                                               6057.0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      129.0        1.0   1.0                 446.511628

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### Benchbase Persistency


Make sure, the database does not exist:
```
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 10
```

```
python benchbase.py -ms 1 -tr \
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
    run
```

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 644s 
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
    disk:248936844
    datadisk:4409008
    volume_size:50G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248936844
    datadisk:5110696
    volume_size:50G
    volume_used:4.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  terminals  target  pod_count  time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1         16    8192          1  60.0                       2570.31                                                      13837.0                                               6214.0
PostgreSQL-1-1-1024-2-1               2         16    8192          1  60.0                       1610.60                                                      15045.0                                               9922.0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

### Loading
                         time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1-1      140.0        1.0   1.0                 411.428571
PostgreSQL-1-1-1024-2-1      140.0        1.0   1.0                 411.428571

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### Benchbase Monitoring

```
python benchbase.py -ms 1 -tr \
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
    run
```

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 681s 
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
    disk:253346116
    datadisk:4409268
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0                        2639.3                                                      13377.0                                               6056.0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      137.0        1.0   1.0                 420.437956

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       563.1      7.7          3.74                 4.97

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      959.55        0           1.3                  1.3

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     2630.98     7.69          4.76                 7.07

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1420.86     5.03          1.42                 1.42

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]

TEST passed: Workflow as planned
```

### Benchbase Complex

```
python benchbase.py -ms 1 -tr \
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
    run
```

yields (after ca. 30 minutes) something like

```
## Show Summary

### Workload
    Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 1711s 
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
    disk:248937016
    datadisk:4327464
    volume_size:50G
    volume_used:4.2G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248937016
    datadisk:4440824
    volume_size:50G
    volume_used:4.3G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248937016
    datadisk:4683584
    volume_size:50G
    volume_used:4.3G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248937016
    datadisk:4928696
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
    disk:248937016
    datadisk:4927032
    volume_size:50G
    volume_used:4.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248937016
    datadisk:5026616
    volume_size:50G
    volume_used:4.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248937016
    datadisk:5267800
    volume_size:50G
    volume_used:5.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248937016
    datadisk:5446400
    volume_size:50G
    volume_used:5.2G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1          8    8192          1  120.0                       1077.29                                                      12160.0                                               7416.0
PostgreSQL-1-1-1024-1-2               1         16   16384          2  120.0                       2309.94                                                      15701.0                                               6915.0
PostgreSQL-1-1-1024-1-3               1          8    8192          2  120.0                       1266.49                                                      13966.0                                               6304.5
PostgreSQL-1-1-1024-2-1               2          8    8192          1  120.0                        948.15                                                      13195.0                                               8427.0
PostgreSQL-1-1-1024-2-2               2         16   16384          2  120.0                       2337.97                                                      15291.0                                               6831.5
PostgreSQL-1-1-1024-2-3               2          8    8192          2  120.0                       1265.16                                                      14275.0                                               6311.5
PostgreSQL-1-1-1024-2-4               2         16   16384          4  120.0                       1925.56                                                      18509.0                                               8298.5

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 1, 2], [4, 2, 2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                         time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1-1      140.0        1.0   1.0                 411.428571
PostgreSQL-1-1-1024-1-2      140.0        1.0   2.0                 411.428571
PostgreSQL-1-1-1024-1-3      140.0        1.0   2.0                 411.428571
PostgreSQL-1-1-1024-1-4      140.0        1.0   4.0                 411.428571
PostgreSQL-1-1-1024-2-1      140.0        1.0   1.0                 411.428571
PostgreSQL-1-1-1024-2-2      140.0        1.0   2.0                 411.428571
PostgreSQL-1-1-1024-2-3      140.0        1.0   2.0                 411.428571
PostgreSQL-1-1-1024-2-4      140.0        1.0   4.0                 411.428571

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      255.46     3.98          3.13                 5.44
PostgreSQL-1-1-1024-1-2      805.31     6.09          3.71                 6.26
PostgreSQL-1-1-1024-1-3      418.90     3.80          3.82                 6.51
PostgreSQL-1-1-1024-1-4       39.19     0.00          3.82                 6.51
PostgreSQL-1-1-1024-2-1      213.58     0.05          6.89                12.28
PostgreSQL-1-1-1024-2-2      646.89     3.61          3.74                 6.63
PostgreSQL-1-1-1024-2-3      330.78     3.72          3.91                 6.95
PostgreSQL-1-1-1024-2-4      631.96     2.96          4.22                 7.47

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      143.46     2.43          1.29                 1.29
PostgreSQL-1-1-1024-1-2      460.36     0.00          3.95                 3.95
PostgreSQL-1-1-1024-1-3      148.70     0.00          4.89                 4.89
PostgreSQL-1-1-1024-1-4      460.31     0.00          4.90                 4.90
PostgreSQL-1-1-1024-2-1       64.63     1.13          0.64                 0.64
PostgreSQL-1-1-1024-2-2      357.70     2.32          3.30                 3.30
PostgreSQL-1-1-1024-2-3      189.09     1.17          4.99                 4.99
PostgreSQL-1-1-1024-2-4      324.48     0.98          5.65                 5.65

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]

TEST failed: Workflow not as planned
```
















## HammerDB

### HammerDB Simple

```
python hammerdb.py -ms 1 -tr \
    -sf 16 \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -nlt 8 \
    -nbp 1 \
    -nbt 16 \
    -ne 1 \
    -nc 1 \
    run
```

yields (after ca. 10 minutes)

```
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
TPC-C data is generated and loaded using several threads.
Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
Benchmark is limited to DBMS P, o, s, t, g, r, e, S, Q, L.
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
    disk:249750592
    datadisk:3376528
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1  11500.0  35639.0         5       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1      100.0        1.0   1.0                      576.0
TEST passed: NOPM contains no 0 or NaN
```


### HammerDB Monitoring

```
python hammerdb.py -ms 1 -tr \
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
    run
```

yields (after ca. 20 minutes)

```
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
TPC-C data is generated and loaded using several threads.
Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS P, o, s, t, g, r, e, S, Q, L.
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
    disk:246374060
    datadisk:3381837
    volume_size:30G
    volume_used:3.3G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1  11758.0  36683.0         5       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1      100.0        1.0   1.0                      576.0

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       92.17     1.61          3.66                  5.3

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      302.34        0          0.08                 0.08

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1    26158.49    62.88          5.39                 7.07

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       44.65     0.11          0.06                 0.06
TEST passed: NOPM contains no 0 or NaN
```

### HammerDB Complex

```
python hammerdb.py -ms 1 -tr \
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
    run
```

yields (after ca. 60 minutes)

```
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
TPC-C data is generated and loaded using several threads.
Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS P, o, s, t, g, r, e, S, Q, L.
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
    disk:246374052
    datadisk:4290673
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
    disk:246374052
    datadisk:4396621
    volume_size:30G
    volume_used:4.2G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374224
    datadisk:4531061
    volume_size:30G
    volume_used:4.2G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374224
    datadisk:4624397
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
    disk:246374224
    datadisk:4726729
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
    disk:246374224
    datadisk:4804397
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
    disk:246374224
    datadisk:4909909
    volume_size:30G
    volume_used:4.6G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374224
    datadisk:4987269
    volume_size:30G
    volume_used:4.8G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                        experiment_run  vusers  client  pod_count      NOPM       TPM  duration  errors
PostgreSQL-BHT-8-1-1-1               1      16       1          1  10957.00  34241.00         2       0
PostgreSQL-BHT-8-1-1-2               1      32       2          2  11999.50  34535.50         2       0
PostgreSQL-BHT-8-1-1-3               1      16       3          2   9345.50  29973.00         2       0
PostgreSQL-BHT-8-1-1-4               1      32       4          4   9840.75  28867.75         2       0
PostgreSQL-BHT-8-1-2-1               2      16       1          1   9676.00  30576.00         2       0
PostgreSQL-BHT-8-1-2-2               2      32       2          2  10901.50  31587.00         2       0
PostgreSQL-BHT-8-1-2-3               2      16       3          2   8787.50  27795.00         2       0
PostgreSQL-BHT-8-1-2-4               2      32       4          4   9313.25  27692.25         2       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-8-1 - Pods [[2, 4, 2, 1], [4, 2, 2, 1]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1-1      100.0        1.0   1.0                      576.0
PostgreSQL-BHT-8-1-1-2      100.0        1.0   2.0                      576.0
PostgreSQL-BHT-8-1-1-3      100.0        1.0   2.0                      576.0
PostgreSQL-BHT-8-1-1-4      100.0        1.0   4.0                      576.0
PostgreSQL-BHT-8-1-2-1      100.0        1.0   1.0                      576.0
PostgreSQL-BHT-8-1-2-2      100.0        1.0   2.0                      576.0
PostgreSQL-BHT-8-1-2-3      100.0        1.0   2.0                      576.0
PostgreSQL-BHT-8-1-2-4      100.0        1.0   4.0                      576.0

### Execution - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1    14035.47    62.87          4.93                 7.14
PostgreSQL-BHT-8-1-1-2    15629.52    63.64          5.63                 6.48
PostgreSQL-BHT-8-1-1-3    15257.81    53.30          5.24                 6.19
PostgreSQL-BHT-8-1-1-4    14176.61    63.60          5.91                 6.94
PostgreSQL-BHT-8-1-2-1    60623.84    62.83          9.27                12.83
PostgreSQL-BHT-8-1-2-2    13874.96    63.60          5.85                 6.83
PostgreSQL-BHT-8-1-2-3    15682.67    62.78          5.50                 6.56
PostgreSQL-BHT-8-1-2-4    15723.85    63.53          6.05                 7.18

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       22.07     0.10          0.06                 0.06
PostgreSQL-BHT-8-1-1-2       23.76     0.11          0.17                 0.17
PostgreSQL-BHT-8-1-1-3       19.43     0.11          0.18                 0.18
PostgreSQL-BHT-8-1-1-4       17.06     0.05          0.20                 0.20
PostgreSQL-BHT-8-1-2-1       23.18     0.09          0.19                 0.19
PostgreSQL-BHT-8-1-2-2       18.83     0.05          0.16                 0.16
PostgreSQL-BHT-8-1-2-3       17.56     0.08          0.18                 0.18
PostgreSQL-BHT-8-1-2-4       18.60     0.05          0.20                 0.20
TEST passed: NOPM contains no 0 or NaN
```














## YCSB


### YCSB Loader Test for Scaling the Driver

```
python ycsb.py -ms 1 -tr \
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
    run
```

yields (after ca. 20 minutes) something like

```
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are []. Factors for benchmarking are [].
Benchmark is limited to DBMS PostgreSQL.
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
    disk:248565128
    datadisk:2188340
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-32-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248696368
    datadisk:2319580
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-4-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248647400
    datadisk:2270612
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246416160
    datadisk:39372
    requests_cpu:4
    requests_memory:16Gi

### Loading
                        experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-32-4-131072               1       32  131072          4                   82173.835235                12341.0             1000000                             2494.50
PostgreSQL-64-4-131072               1       64  131072          4                  102402.660586                 9886.0             1000000                             3860.00
PostgreSQL-32-8-131072               1       32  131072          8                   80125.026479                13504.0             1000000                             2439.75
PostgreSQL-64-8-131072               1       64  131072          8                       0.000000                    0.0                   0                                0.00

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-32-4-131072-1               1       64  131072          1                      114364.14                 8744.0            499806                            1407.0              500194                              2337.0
PostgreSQL-32-8-131072-1               1       64  131072          1                      119817.88                 8346.0            499265                            1412.0              500735                              2621.0
PostgreSQL-64-4-131072-1               1       64  131072          1                      119402.99                 8375.0            499833                            1376.0              500167                              1979.0
TEST failed: [OVERALL].Throughput(ops/sec) contains 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```

### YCSB Execution for Scaling and Repetition

```
python ycsb.py -ms 1 -tr \
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
    run
```

yields (after ca. 15 minutes) something like

```
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are []. Factors for benchmarking are [].
Benchmark is limited to DBMS PostgreSQL.
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
    disk:246374396
    datadisk:2931136
    volume_size:100G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374396
    datadisk:2940816
    volume_size:100G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374396
    datadisk:3138456
    volume_size:100G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374396
    datadisk:3288736
    volume_size:100G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374396
    datadisk:3520176
    volume_size:100G
    volume_used:3.4G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374396
    datadisk:3524128
    volume_size:100G
    volume_used:3.4G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374396
    datadisk:3646168
    volume_size:100G
    volume_used:3.4G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374396
    datadisk:3648904
    volume_size:100G
    volume_used:3.4G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                            experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1-1               1       64  131072          1                       63564.71                15732.0            500546                           1365.00              499454                             1713.00
PostgreSQL-64-8-131072-1-3               1       64  131072          8                      119634.40                 8507.0            500220                            968.25              499780                             1517.12
PostgreSQL-64-8-131072-1-2               1      128  262144          2                       92718.61                10958.0            499999                           1936.50              500001                            53647.00
PostgreSQL-64-8-131072-1-4               1      128  262144         16                      112027.76                 9416.0            499650                           2935.88              500350                            21887.50
PostgreSQL-64-8-131072-2-1               2       64  131072          1                       57032.05                17534.0            499642                           1364.00              500358                             1683.00
PostgreSQL-64-8-131072-2-3               2       64  131072          8                      127014.91                 7907.0            499572                            873.00              500428                             1386.50
PostgreSQL-64-8-131072-2-2               2      128  262144          2                       97432.97                10338.0            500001                           1822.50              499999                            44143.00
PostgreSQL-64-8-131072-2-4               2      128  262144         16                      140828.26                 7483.0            500423                           3146.62              499577                             5770.75
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```


### YCSB Execution Different Workload (TestCases.md)

```
python ycsb.py -ms 1 -tr \
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
    run
```

yields (after ca. 5 minutes) something like

```
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
Workload is 'E'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are []. Factors for benchmarking are [].
Benchmark is limited to DBMS PostgreSQL.
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
    disk:246374396
    datadisk:3678280
    volume_size:100G
    volume_used:3.6G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)  [SCAN].Return=OK  [SCAN].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1               1       64  131072          8                       25278.82                41289.0               50218                             3116.25            949782                            5919.5
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```


### YCSB Execution Monitoring

```
python ycsb.py -ms 1 -tr \
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
    run
```

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    YCSB SF=10
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
Workload is 'A'. Number of rows to insert is 10000000. Number of operations is 10000000. Batch size is ''.
YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are []. Factors for benchmarking are [].
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS PostgreSQL.
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
    disk:246374396
    datadisk:31728184
    volume_size:100G
    volume_used:31G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374396
    datadisk:31807712
    volume_size:100G
    volume_used:31G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1               1       64  131072          1                       64498.24               155043.0           4999842                           1383.00             5000158                             1808.00
PostgreSQL-64-8-131072-2               1       64  131072          8                      130431.05                77251.0           5000234                           1228.25             4999766                             1621.25

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1      634.69      9.1         12.99                27.89
PostgreSQL-64-8-131072-2     1636.94      0.0         17.51                32.41

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1      296.33     0.00          0.60                 0.60
PostgreSQL-64-8-131072-2      658.44     1.27          5.16                 5.19
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
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
