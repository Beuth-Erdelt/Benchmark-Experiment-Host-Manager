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
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
TPC-H (SF=1) data is loaded and benchmark is executed.
Query ordering is Q1 - Q22.
All instances use the same query parameters.
Import sets indexes and constraints after loading and recomputes statistics.
Benchmark is limited to DBMS PostgreSQL.
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
    disk:249171616
    datadisk:2822200
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2567.07
Minimum Cost Supplier Query (TPC-H Q2)                             419.22
Shipping Priority (TPC-H Q3)                                       729.37
Order Priority Checking Query (TPC-H Q4)                          1236.64
Local Supplier Volume (TPC-H Q5)                                   627.87
Forecasting Revenue Change (TPC-H Q6)                              479.27
Forecasting Revenue Change (TPC-H Q7)                              747.93
National Market Share (TPC-H Q8)                                   590.71
Product Type Profit Measure (TPC-H Q9)                            1064.58
Forecasting Revenue Change (TPC-H Q10)                            1231.34
Important Stock Identification (TPC-H Q11)                         238.82
Shipping Modes and Order Priority (TPC-H Q12)                      973.56
Customer Distribution (TPC-H Q13)                                 1940.84
Forecasting Revenue Change (TPC-H Q14)                             529.18
Top Supplier Query (TPC-H Q15)                                     531.58
Parts/Supplier Relationship (TPC-H Q16)                            571.33
Small-Quantity-Order Revenue (TPC-H Q17)                          1957.44
Large Volume Customer (TPC-H Q18)                                 6674.42
Discounted Revenue (TPC-H Q19)                                     674.23
Potential Part Promotion (TPC-H Q20)                               661.18
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                870.81
Global Sales Opportunity Query (TPC-H Q22)                         234.54

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           29.0         1.0       85.0     123.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.86

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4362.63

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 1  1              1                 29      1   1                  2731.03
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
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
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
System metrics are monitored by a cluster-wide installation.
TPC-H (SF=3) data is loaded and benchmark is executed.
Query ordering is Q1 - Q22.
All instances use the same query parameters.
Import sets indexes and constraints after loading and recomputes statistics.
Benchmark is limited to DBMS PostgreSQL.
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
    disk:254732816
    datadisk:8383400
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 6349.65
Minimum Cost Supplier Query (TPC-H Q2)                            2134.14
Shipping Priority (TPC-H Q3)                                      2396.38
Order Priority Checking Query (TPC-H Q4)                          3057.87
Local Supplier Volume (TPC-H Q5)                                  2227.72
Forecasting Revenue Change (TPC-H Q6)                             1144.35
Forecasting Revenue Change (TPC-H Q7)                             2282.60
National Market Share (TPC-H Q8)                                  1357.72
Product Type Profit Measure (TPC-H Q9)                            3112.36
Forecasting Revenue Change (TPC-H Q10)                            2970.65
Important Stock Identification (TPC-H Q11)                         555.70
Shipping Modes and Order Priority (TPC-H Q12)                     2397.45
Customer Distribution (TPC-H Q13)                                 6406.64
Forecasting Revenue Change (TPC-H Q14)                            1231.32
Top Supplier Query (TPC-H Q15)                                    1373.38
Parts/Supplier Relationship (TPC-H Q16)                           1242.01
Small-Quantity-Order Revenue (TPC-H Q17)                          5704.67
Large Volume Customer (TPC-H Q18)                                20286.70
Discounted Revenue (TPC-H Q19)                                    1870.36
Potential Part Promotion (TPC-H Q20)                              1162.16
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               2747.41
Global Sales Opportunity Query (TPC-H Q22)                         456.92

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          102.0         1.0      221.0     332.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           2.28

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4868.08

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 3  1              1                 78      1   3                  3046.15

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      413.06     1.04           6.6                10.65

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        9.45     0.05          0.92                 2.28

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       280.2     4.22         14.48                18.73

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       12.49        0          0.27                 0.28
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
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
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
System metrics are monitored by a cluster-wide installation.
TPC-H (SF=1) data is loaded and benchmark is executed.
Query ordering is Q1 - Q22.
All instances use the same query parameters.
Import sets indexes and constraints after loading and recomputes statistics.
Benchmark is limited to DBMS PostgreSQL.
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
    disk:246349412
    datadisk:2822088
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
    disk:246349412
    datadisk:2822088
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
    disk:246349412
    datadisk:2822088
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
    disk:246349560
    datadisk:2822088
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
    disk:246349560
    datadisk:2822088
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
    disk:246349560
    datadisk:2822088
    volume_size:100G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
                                                     PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                                     False                   False                   False                   False                   False                   False
Minimum Cost Supplier Query (TPC-H Q2)                                False                   False                   False                   False                   False                   False
Shipping Priority (TPC-H Q3)                                          False                   False                   False                   False                   False                   False
Order Priority Checking Query (TPC-H Q4)                              False                   False                   False                   False                   False                   False
Local Supplier Volume (TPC-H Q5)                                      False                   False                   False                   False                   False                   False
Forecasting Revenue Change (TPC-H Q6)                                 False                   False                   False                   False                   False                   False
Forecasting Revenue Change (TPC-H Q7)                                 False                   False                   False                   False                   False                   False
National Market Share (TPC-H Q8)                                      False                   False                   False                   False                   False                   False
Product Type Profit Measure (TPC-H Q9)                                False                   False                   False                   False                   False                   False
Forecasting Revenue Change (TPC-H Q10)                                False                   False                   False                    True                   False                   False
Important Stock Identification (TPC-H Q11)                            False                   False                   False                   False                   False                   False
Shipping Modes and Order Priority (TPC-H Q12)                         False                   False                   False                   False                   False                   False
Customer Distribution (TPC-H Q13)                                     False                   False                   False                   False                   False                   False
Forecasting Revenue Change (TPC-H Q14)                                False                   False                   False                   False                   False                   False
Top Supplier Query (TPC-H Q15)                                        False                   False                   False                   False                   False                   False
Parts/Supplier Relationship (TPC-H Q16)                               False                   False                   False                   False                   False                   False
Small-Quantity-Order Revenue (TPC-H Q17)                              False                   False                   False                   False                   False                   False
Large Volume Customer (TPC-H Q18)                                     False                   False                   False                   False                   False                   False
Discounted Revenue (TPC-H Q19)                                        False                   False                   False                   False                   False                   False
Potential Part Promotion (TPC-H Q20)                                  False                   False                   False                   False                   False                   False
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                   False                   False                   False                   False                   False                   False
Global Sales Opportunity Query (TPC-H Q22)                            False                   False                   False                   False                   False                   False

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                                   2711.71                 2534.10                 2546.08                14591.67                 2533.11                 2533.24
Minimum Cost Supplier Query (TPC-H Q2)                               652.68                  437.14                  436.45                 3639.37                  442.60                  440.81
Shipping Priority (TPC-H Q3)                                        1352.13                  738.41                  751.15                 6209.37                  760.21                  750.53
Order Priority Checking Query (TPC-H Q4)                            1257.23                 1266.21                 1242.31                 1254.06                 1237.36                 1242.37
Local Supplier Volume (TPC-H Q5)                                     645.61                  652.35                  654.06                  650.90                  674.30                  665.44
Forecasting Revenue Change (TPC-H Q6)                                508.86                  511.04                  523.48                  497.87                  514.85                  510.64
Forecasting Revenue Change (TPC-H Q7)                                992.52                  750.75                  761.88                  825.09                  775.12                  758.97
National Market Share (TPC-H Q8)                                     752.88                  606.99                  614.71                  662.78                  627.21                  613.82
Product Type Profit Measure (TPC-H Q9)                              1871.46                 1072.98                 1060.88                 1547.11                 1066.04                 1050.56
Forecasting Revenue Change (TPC-H Q10)                              1281.68                 1289.30                 1275.28                 1234.06                 1228.81                 1238.28
Important Stock Identification (TPC-H Q11)                           242.93                  254.51                  245.81                  244.38                  254.24                  253.05
Shipping Modes and Order Priority (TPC-H Q12)                        926.32                  924.94                  928.56                  908.04                  938.54                  923.71
Customer Distribution (TPC-H Q13)                                   1968.06                 2014.61                 2029.33                 1977.62                 1966.03                 1956.77
Forecasting Revenue Change (TPC-H Q14)                               528.24                  531.66                  543.08                  532.56                  550.96                  556.19
Top Supplier Query (TPC-H Q15)                                       537.84                  543.06                  551.92                  538.60                  558.53                  554.96
Parts/Supplier Relationship (TPC-H Q16)                              558.25                  560.65                  559.35                  539.17                  550.58                  552.13
Small-Quantity-Order Revenue (TPC-H Q17)                            1987.13                 2041.91                 2023.46                 1943.89                 2088.94                 2061.48
Large Volume Customer (TPC-H Q18)                                   6868.97                 7466.84                 8111.44                 6243.91                 8192.39                 7912.94
Discounted Revenue (TPC-H Q19)                                       686.24                  691.07                  679.76                  681.05                  697.44                  697.20
Potential Part Promotion (TPC-H Q20)                                 865.71                  677.05                  661.30                  734.23                  661.88                  637.55
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                 2031.52                  857.48                  862.46                 1164.87                  877.95                  867.36
Global Sales Opportunity Query (TPC-H Q22)                           340.41                  216.73                  215.40                  242.57                  212.67                  213.31

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           28.0         1.0       92.0     130.0
PostgreSQL-BHT-8-1-2-1           1.0           28.0         1.0       92.0     130.0
PostgreSQL-BHT-8-1-2-2           1.0           28.0         1.0       92.0     130.0
PostgreSQL-BHT-8-2-1-1           1.0           28.0         1.0       92.0     130.0
PostgreSQL-BHT-8-2-2-1           1.0           28.0         1.0       92.0     130.0
PostgreSQL-BHT-8-2-2-2           1.0           28.0         1.0       92.0     130.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           1.02
PostgreSQL-BHT-8-1-2-1           0.87
PostgreSQL-BHT-8-1-2-2           0.88
PostgreSQL-BHT-8-2-1-1           1.18
PostgreSQL-BHT-8-2-2-1           0.89
PostgreSQL-BHT-8-2-2-2           0.88

### Power@Size
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            3659.36
PostgreSQL-BHT-8-1-2-1            4280.64
PostgreSQL-BHT-8-1-2-2            4265.54
PostgreSQL-BHT-8-2-1-1            3171.19
PostgreSQL-BHT-8-2-2-1            4239.94
PostgreSQL-BHT-8-2-2-2            4278.30

### Throughput@Size
                                                   time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                 SF num_experiment num_client                                              
PostgreSQL-BHT-8-1-1 1  1              1                 34      1   1                  2329.41
PostgreSQL-BHT-8-1-2 1  1              2                 31      2   1                  5109.68
PostgreSQL-BHT-8-2-1 1  2              1                 50      1   1                  1584.00
PostgreSQL-BHT-8-2-2 1  2              2                 31      2   1                  5109.68

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      133.83     1.06           3.7                 5.37
PostgreSQL-BHT-8-1-2      133.83     1.06           3.7                 5.37

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1        0.12        0          0.02                 0.02
PostgreSQL-BHT-8-1-2        0.12        0          0.02                 0.02

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       21.95     0.40          3.70                 3.76
PostgreSQL-BHT-8-1-2       22.74     0.00          3.97                 4.31
PostgreSQL-BHT-8-2-1       18.30     0.00          7.19                 8.98
PostgreSQL-BHT-8-2-2      497.61     1.91          7.65                 9.82

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1        0.00      0.0          0.00                 0.00
PostgreSQL-BHT-8-1-2        0.03      0.0          0.01                 0.01
PostgreSQL-BHT-8-2-1        0.02      0.0          0.01                 0.01
PostgreSQL-BHT-8-2-2        7.41      0.0          0.12                 0.13
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
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
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
Benchbase data is generated and loaded using several threads.
Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 300 minutes.
Benchmark is limited to DBMS PostgreSQL.
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19. SUT is fixed to cl-worker11.
Loading is tested with [1] threads and [1] target factors of base 1024, split into [1] pods.
Benchmarking is tested with [16] threads and [8] target factors of base 1024, split into [1] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250758688
    datadisk:4409124
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0                       2630.71                                                      13258.0                                               6076.0

Warehouses: 16

### Workflow
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      134.0        1.0   1.0                 429.850746
TEST passed: Throughput (requests/second) contains no 0 or NaN
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
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
Benchbase data is generated and loaded using several threads.
Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 60 minutes.
Benchmark is limited to DBMS PostgreSQL.
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19. SUT is fixed to cl-worker11.
Database is persisted to disk of type shared and size 50Gi.
Loading is tested with [1] threads and [1] target factors of base 1024, split into [1] pods.
Benchmarking is tested with [16] threads and [8] target factors of base 1024, split into [1] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246349560
    datadisk:4409032
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
    disk:246349560
    datadisk:5108384
    volume_size:50G
    volume_used:4.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  terminals  target  pod_count  time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1         16    8192          1  60.0                       2495.83                                                      13974.0                                               6400.0
PostgreSQL-1-1-1024-2-1               2         16    8192          1  60.0                       1396.38                                                      14976.0                                              11446.0

Warehouses: 16

### Workflow
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

### Loading
                         time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1-1      134.0        1.0   1.0                 429.850746
PostgreSQL-1-1-1024-2-1      134.0        1.0   1.0                 429.850746
TEST passed: Throughput (requests/second) contains no 0 or NaN
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
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
System metrics are monitored by a cluster-wide installation.
Benchbase data is generated and loaded using several threads.
Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 300 minutes.
Benchmark is limited to DBMS PostgreSQL.
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19. SUT is fixed to cl-worker11.
Loading is tested with [1] threads and [1] target factors of base 1024, split into [1] pods.
Benchmarking is tested with [16] threads and [8] target factors of base 1024, split into [1] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250758856
    datadisk:4409292
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0                       2613.37                                                      13747.0                                               6116.0

Warehouses: 16

### Workflow
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      133.0        1.0   1.0                 433.082707

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      431.09        0          3.54                 4.58

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      850.59    11.82           1.3                  1.3

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     2693.03     7.58          4.75                 7.06

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1379.28     4.87          1.44                 1.44
TEST passed: Throughput (requests/second) contains no 0 or NaN
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
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
System metrics are monitored by a cluster-wide installation.
Benchbase data is generated and loaded using several threads.
Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 120 minutes.
Benchmark is limited to DBMS PostgreSQL.
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19. SUT is fixed to cl-worker11.
Database is persisted to disk of type shared and size 50Gi.
Loading is tested with [1] threads and [1] target factors of base 1024, split into [1] pods.
Benchmarking is tested with [8] threads and [8] target factors of base 1024, split into [1, 2] pods.
Benchmarking is run as [1, 2] times the number of benchmarking pods.
Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352116
    datadisk:5310696
    volume_size:50G
    volume_used:5.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352116
    datadisk:5422320
    volume_size:50G
    volume_used:5.2G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352116
    datadisk:5674296
    volume_size:50G
    volume_used:5.2G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352116
    datadisk:6008840
    volume_size:50G
    volume_used:5.2G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352116
    datadisk:6988024
    volume_size:50G
    volume_used:6.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352116
    datadisk:7086352
    volume_size:50G
    volume_used:6.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352116
    datadisk:7334816
    volume_size:50G
    volume_used:6.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352116
    datadisk:7470464
    volume_size:50G
    volume_used:6.7G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1          8    8192          1  120.0                       1068.40                                                      12221.0                                              7478.00
PostgreSQL-1-1-1024-1-2               1         16   16384          2  120.0                       2457.01                                                      15348.0                                              6503.00
PostgreSQL-1-1-1024-1-3               1          8    8192          2  120.0                       1353.65                                                      13582.0                                              5899.50
PostgreSQL-1-1-1024-1-4               1         16   16384          4  120.0                       2090.96                                                      18082.0                                              7639.75
PostgreSQL-1-1-1024-2-1               2          8    8192          1  120.0                        934.17                                                      15306.0                                              8553.00
PostgreSQL-1-1-1024-2-2               2         16   16384          2  120.0                       2420.62                                                      15456.0                                              6599.50
PostgreSQL-1-1-1024-2-3               2          8    8192          2  120.0                       1336.14                                                      13901.0                                              5976.50
PostgreSQL-1-1-1024-2-4               2         16   16384          4  120.0                       2079.17                                                      18274.0                                              7683.25

Warehouses: 16

### Workflow
DBMS PostgreSQL-1-1-1024 - Pods [[4, 2, 1, 2], [2, 4, 2, 1]]

### Loading
                         time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1-1      134.0        1.0   1.0                 429.850746
PostgreSQL-1-1-1024-1-2      134.0        1.0   2.0                 429.850746
PostgreSQL-1-1-1024-1-3      134.0        1.0   2.0                 429.850746
PostgreSQL-1-1-1024-1-4      134.0        1.0   4.0                 429.850746
PostgreSQL-1-1-1024-2-1      134.0        1.0   1.0                 429.850746
PostgreSQL-1-1-1024-2-2      134.0        1.0   2.0                 429.850746
PostgreSQL-1-1-1024-2-3      134.0        1.0   2.0                 429.850746
PostgreSQL-1-1-1024-2-4      134.0        1.0   4.0                 429.850746

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      223.27     3.70          3.18                 6.19
PostgreSQL-1-1-1024-1-2      700.07     0.00          3.87                 7.14
PostgreSQL-1-1-1024-1-3      374.55     2.65          4.05                 7.49
PostgreSQL-1-1-1024-1-4      579.42     5.94          4.36                 7.97
PostgreSQL-1-1-1024-2-1      259.96     0.32          7.50                14.75
PostgreSQL-1-1-1024-2-2      724.89     7.08          3.91                 7.79
PostgreSQL-1-1-1024-2-3      373.37     3.76          4.14                 8.16
PostgreSQL-1-1-1024-2-4      694.12     0.00          4.54                 8.77

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      118.46     0.00          1.32                 1.32
PostgreSQL-1-1-1024-1-2      410.51     2.44          4.02                 4.02
PostgreSQL-1-1-1024-1-3      170.10     2.38          4.40                 4.40
PostgreSQL-1-1-1024-1-4      287.97     2.09          6.01                 6.01
PostgreSQL-1-1-1024-2-1      306.33     0.00          4.79                 4.79
PostgreSQL-1-1-1024-2-2      400.93     4.76          4.01                 4.01
PostgreSQL-1-1-1024-2-3      200.59     0.00          4.78                 4.78
PostgreSQL-1-1-1024-2-4      341.59     1.04          5.93                 5.93
TEST passed: Throughput (requests/second) contains no 0 or NaN
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
Benchmark is limited to DBMS PostgreSQL.
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
    disk:249727380
    datadisk:3377808
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1  11917.0  36568.0         5       0

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
System metrics are monitored by a cluster-wide installation.
TPC-C data is generated and loaded using several threads.
Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
Benchmark is limited to DBMS PostgreSQL.
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
    disk:246349848
    datadisk:3381845
    volume_size:30G
    volume_used:3.3G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1  11799.0  36283.0         5       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1      105.0        1.0   1.0                 548.571429

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       121.4     0.45          3.83                 5.51

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      329.94      5.2          0.07                 0.07

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1    25890.95     61.0          5.34                 7.01

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       45.74     0.11          0.05                 0.06
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

yields (after ca. 45 minutes)

```
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
System metrics are monitored by a cluster-wide installation.
TPC-C data is generated and loaded using several threads.
Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
Benchmark is limited to DBMS PostgreSQL.
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
    disk:246349732
    datadisk:4294945
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
    disk:246349732
    datadisk:4401613
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
    disk:246349732
    datadisk:4527693
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
    disk:246349732
    datadisk:4611997
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
    disk:248309504
    datadisk:4717273
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246349900
    datadisk:4797477
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246349900
    datadisk:4897773
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246349900
    datadisk:4983101
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                        experiment_run  vusers  client  pod_count      NOPM       TPM  duration  errors
PostgreSQL-BHT-8-1-1-1               1      16       1          1  11054.00  34049.00         2       0
PostgreSQL-BHT-8-1-1-2               1      32       2          2  11097.00  31949.00         2       0
PostgreSQL-BHT-8-1-1-3               1      16       3          2   8856.50  28298.50         2       0
PostgreSQL-BHT-8-1-1-4               1      32       4          4   9957.25  28916.25         2       0
PostgreSQL-BHT-8-1-2-1               2      16       1          1   9245.00  30188.00         2       0
PostgreSQL-BHT-8-1-2-2               2      32       2          2  10132.00  30407.00         2       0
PostgreSQL-BHT-8-1-2-3               2      16       3          2   8986.50  28825.00         2       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-8-1 - Pods [[2, 1, 2], [2, 2, 4, 1]]

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
PostgreSQL-BHT-8-1-1-1    14181.81    62.81          4.99                 7.14
PostgreSQL-BHT-8-1-1-2    14824.60    63.63          5.47                 7.74
PostgreSQL-BHT-8-1-1-3    15411.30    33.44          5.44                 7.78
PostgreSQL-BHT-8-1-1-4    16935.32    63.60          6.02                 8.46
PostgreSQL-BHT-8-1-2-1    62425.80    62.90          9.32                14.30
PostgreSQL-BHT-8-1-2-2    15916.39    63.63          5.92                 8.50
PostgreSQL-BHT-8-1-2-3    15150.28    62.90          5.56                 8.21
PostgreSQL-BHT-8-1-2-4        0.00     0.00          4.46                 7.14

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       23.05     0.10          0.06                 0.06
PostgreSQL-BHT-8-1-1-2       20.12     0.05          0.16                 0.16
PostgreSQL-BHT-8-1-1-3       24.55     0.08          0.18                 0.18
PostgreSQL-BHT-8-1-1-4       18.31     0.07          0.20                 0.20
PostgreSQL-BHT-8-1-2-1       20.29     0.08          0.13                 0.13
PostgreSQL-BHT-8-1-2-2       20.16     0.10          0.16                 0.16
PostgreSQL-BHT-8-1-2-3       25.59     0.08          0.18                 0.18
PostgreSQL-BHT-8-1-2-4        0.00     0.00          0.07                 0.07
TEST passed: NOPM contains no 0 or NaN
```














## YCSB


### YCSB Loader Test for Scaling the Driver

```
python ycsb.py -ms 1 -tr \
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
YCSB is performed using several threads and processes.
Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000.
Benchmark is limited to DBMS PostgreSQL.
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Loading is tested with [32, 64] threads and [1] target factors of base 131072, split into [4, 8] pods.
Benchmarking is tested with [64] threads and [1] target factors of base 131072, split into [1] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-32-4-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248719104
    datadisk:2369252
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-32-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248488556
    datadisk:2155028
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-4-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248669748
    datadisk:2336108
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248620120
    datadisk:2270204
    requests_cpu:4
    requests_memory:16Gi

### Loading
                        experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-32-4-131072               1       32  131072          4                   82218.168751                12295.0             1000000                             2407.50
PostgreSQL-64-4-131072               1       64  131072          4                   94546.665011                10726.0             1000000                             3733.50
PostgreSQL-32-8-131072               1       32  131072          8                   83941.922729                12407.0             1000000                             2449.50
PostgreSQL-64-8-131072               1       64  131072          8                  103176.883355                 9889.0             1000000                             4141.25

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-32-4-131072-1               1       64  131072          1                      100452.03                 9955.0            499573                            1670.0              500427                              3375.0
PostgreSQL-32-8-131072-1               1       64  131072          1                      110485.03                 9051.0            499909                            1357.0              500091                              2012.0
PostgreSQL-64-4-131072-1               1       64  131072          1                       79321.01                12607.0            501186                            3247.0              498814                              6279.0
PostgreSQL-64-8-131072-1               1       64  131072          1                      114077.12                 8766.0            499293                            1355.0              500707                              2002.0
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```

### YCSB Loader Test for Persistency

Make sure, the database does not exist:
```
kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
sleep 10
```

Then run
```
python ycsb.py -ms 1 -tr \
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
    run
```

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
YCSB is performed using several threads and processes.
Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000.
Benchmark is limited to DBMS PostgreSQL.
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Database is persisted to disk of type shared and size 100Gi.
Loading is tested with [64] threads and [1] target factors of base 131072, split into [8] pods.
Benchmarking is tested with [64] threads and [1] target factors of base 131072, split into [1] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run 2 times.

### Connections
PostgreSQL-64-8-131072-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246349908
    datadisk:2204800
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
    disk:248456756
    datadisk:2901880
    volume_size:100G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi

### Loading
                        experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-131072               1       64  131072          8                   94013.022786                11024.0             1000000                             3919.75

### Execution
                            experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1-1               1       64  131072          1                      120206.76                 8319.0            499827                            1300.0              500173                              1755.0
PostgreSQL-64-8-131072-2-1               2       64  131072          1                       53154.73                18813.0            500388                            3419.0              499612                              5699.0
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```

### YCSB Execution for Scaling and Repetition

```
python ycsb.py -ms 1 -tr \
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
YCSB is performed using several threads and processes.
Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000.
Benchmark is limited to DBMS PostgreSQL.
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Database is persisted to disk of type shared and size 100Gi.
Loading is tested with [64] threads and [1] target factors of base 131072, split into [8] pods.
Benchmarking is tested with [64] threads and [1] target factors of base 131072, split into [1, 8] pods.
Benchmarking is run as [1, 2] times the number of benchmarking pods.
Experiment is run 2 times.

### Connections
PostgreSQL-64-8-131072-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:4143128
    volume_size:100G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:4147232
    volume_size:100G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:4367960
    volume_size:100G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:4567488
    volume_size:100G
    volume_used:4.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:4883544
    volume_size:100G
    volume_used:4.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:4889384
    volume_size:100G
    volume_used:4.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:5031400
    volume_size:100G
    volume_used:4.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:5034192
    volume_size:100G
    volume_used:4.7G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                            experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1-1               1       64  131072          1                       56388.86                17734.0            499909                           1361.00              500091                             1870.00
PostgreSQL-64-8-131072-1-3               1       64  131072          8                      126932.13                 7907.0            500975                           1107.75              499025                             1545.12
PostgreSQL-64-8-131072-1-2               1      128  262144          2                       71441.34                14004.0            500636                           1978.50              499364                            67743.00
PostgreSQL-64-8-131072-1-4               1      128  262144         16                      101371.09                10113.0            500484                           2665.12              499516                            44803.00
PostgreSQL-64-8-131072-2-1               2       64  131072          1                       41179.38                24284.0            500180                           1405.00              499820                             2453.00
PostgreSQL-64-8-131072-2-3               2       64  131072          8                      127052.93                 7894.0            500392                           1072.12              499608                             1548.62
PostgreSQL-64-8-131072-2-2               2      128  262144          2                       88674.39                11399.0            499655                           1956.00              500345                            62319.00
PostgreSQL-64-8-131072-2-4               2      128  262144         16                      104821.01                 9983.0            499712                           2677.25              500288                            39187.00
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```


### YCSB Execution Different Workload (TestCases.md)

```
python ycsb.py -ms 1 -tr \
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
YCSB is performed using several threads and processes.
Workload is 'E'. Number of rows to insert is 1000000. Number of operations is 1000000.
Benchmark is limited to DBMS PostgreSQL.
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Database is persisted to disk of type shared and size 100Gi.
Loading is tested with [64] threads and [1] target factors of base 131072, split into [8] pods.
Benchmarking is tested with [64] threads and [1] target factors of base 131072, split into [8] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-64-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:5128856
    volume_size:100G
    volume_used:4.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)  [SCAN].Return=OK  [SCAN].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1               1       64  131072          8                       22246.73                47813.0                  93                               728.5            950279                            5316.5
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
```


### YCSB Execution Monitoring

```
python ycsb.py -ms 1 -tr \
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
System metrics are monitored by a cluster-wide installation.
YCSB is performed using several threads and processes.
Workload is 'A'. Number of rows to insert is 10000000. Number of operations is 10000000.
Benchmark is limited to DBMS PostgreSQL.
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Database is persisted to disk of type shared and size 100Gi.
Loading is tested with [64] threads and [1] target factors of base 131072, split into [8] pods.
Benchmarking is tested with [64] threads and [1] target factors of base 131072, split into [1, 8] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-64-8-131072-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:31274608
    volume_size:100G
    volume_used:30G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246352796
    datadisk:31343584
    volume_size:100G
    volume_used:30G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1               1       64  131072          1                       61102.29               163660.0           5001386                            1493.0             4998614                             2261.00
PostgreSQL-64-8-131072-2               1       64  131072          8                      123841.13                84979.0           4999519                            1344.5             5000481                             1730.88

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1     1567.69     0.31         16.83                31.27
PostgreSQL-64-8-131072-2     1638.59    10.74         17.76                32.17

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1      586.80     5.91          0.61                 0.61
PostgreSQL-64-8-131072-2      575.98     3.47          5.03                 5.06
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
