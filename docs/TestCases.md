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
python tpch.py -ms 1 -dt -sf 1 -ii -ic -is \
    -nlp 8 -nlt 8 \
    -nc 1 -ne 1 \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -t 1200 \
    -dbms PostgreSQL \
    run
```

* SF = 1
* PostgreSQL 8 loader, indexed
* 1x(1) benchmarker = 1 execution stream (power test)
* no persistent storage
* no monitoring

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    TPC-H Queries SF=1
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS. TPC-H (SF=1) data is loaded and benchmark is executed. Query ordering is Q1 - Q22. All instances use the same query parameters. Import sets indexes and constraints after loading and recomputes statistics. Benchmark is limited to DBMS PostgreSQL. Import is handled by 8 processes (pods). Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:220519300
    datadisk:2823008
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2459.21
Minimum Cost Supplier Query (TPC-H Q2)                             413.46
Shipping Priority (TPC-H Q3)                                       716.13
Order Priority Checking Query (TPC-H Q4)                          1243.77
Local Supplier Volume (TPC-H Q5)                                   619.78
Forecasting Revenue Change (TPC-H Q6)                              466.62
Forecasting Revenue Change (TPC-H Q7)                              734.01
National Market Share (TPC-H Q8)                                   582.93
Product Type Profit Measure (TPC-H Q9)                            1055.72
Forecasting Revenue Change (TPC-H Q10)                            1213.50
Important Stock Identification (TPC-H Q11)                         241.65
Shipping Modes and Order Priority (TPC-H Q12)                      960.81
Customer Distribution (TPC-H Q13)                                 1958.87
Forecasting Revenue Change (TPC-H Q14)                             521.75
Top Supplier Query (TPC-H Q15)                                     526.39
Parts/Supplier Relationship (TPC-H Q16)                            563.39
Small-Quantity-Order Revenue (TPC-H Q17)                          2014.23
Large Volume Customer (TPC-H Q18)                                 7054.77
Discounted Revenue (TPC-H Q19)                                     668.20
Potential Part Promotion (TPC-H Q20)                               655.87
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                867.57
Global Sales Opportunity Query (TPC-H Q22)                         230.59

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           24.0         1.0       85.0     119.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.86

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4392.06

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 1  1              1                 28      1   1                  2828.57
```


### TPC-H Monitoring

```
python tpch.py -ms 1 -dt -sf 3 -ii -ic -is \
    -nlp 8 -nlt 8 \
    -nc 1 -ne 1 \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -t 1200 \
    -dbms PostgreSQL \
    -m -mc \
    -rst shared -rss 100Gi \
    run
```

* SF = 3
* PostgreSQL 8 loader, indexed
* 1x(1) benchmarker = 1 execution stream (power test)
* persistent storage of class shared
* monitoring all components

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    TPC-H Queries SF=3
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS. System metrics are monitored by a cluster-wide installation. TPC-H (SF=3) data is loaded and benchmark is executed. Database is persistent on a volume of type shared. Query ordering is Q1 - Q22. All instances use the same query parameters. Import sets indexes and constraints after loading and recomputes statistics. Benchmark is limited to DBMS PostgreSQL. Import is handled by 8 processes (pods). Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217696288
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
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 6566.38
Minimum Cost Supplier Query (TPC-H Q2)                            3157.68
Shipping Priority (TPC-H Q3)                                      2957.50
Order Priority Checking Query (TPC-H Q4)                          3064.26
Local Supplier Volume (TPC-H Q5)                                  2213.43
Forecasting Revenue Change (TPC-H Q6)                             1183.87
Forecasting Revenue Change (TPC-H Q7)                             3903.30
National Market Share (TPC-H Q8)                                  1747.39
Product Type Profit Measure (TPC-H Q9)                            5530.70
Forecasting Revenue Change (TPC-H Q10)                            2992.43
Important Stock Identification (TPC-H Q11)                         546.42
Shipping Modes and Order Priority (TPC-H Q12)                     2357.28
Customer Distribution (TPC-H Q13)                                 6113.69
Forecasting Revenue Change (TPC-H Q14)                            1242.04
Top Supplier Query (TPC-H Q15)                                    1346.50
Parts/Supplier Relationship (TPC-H Q16)                           1305.64
Small-Quantity-Order Revenue (TPC-H Q17)                          5250.17
Large Volume Customer (TPC-H Q18)                                18569.68
Discounted Revenue (TPC-H Q19)                                    1848.44
Potential Part Promotion (TPC-H Q20)                              1093.66
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               2756.80
Global Sales Opportunity Query (TPC-H Q22)                        1040.01

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           80.0         1.0      211.0     300.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           2.58

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4330.06

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 3  1              1                 82      1   3                  2897.56

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      394.92     1.34          6.25                10.84

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        7.02        0          0.52                 2.28

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       358.7      4.0          6.52                 7.62

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       14.39        0          0.27                 0.27
```

### TPC-H Throughput Test

```
python tpch.py -ms 1 -dt -sf 1 -ii -ic -is \
    -nlp 8 -nlt 8 \
    -nc 2 -ne 1,2 \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -t 1200 \
    -dbms PostgreSQL \
    -m -mc \
    -rst shared -rss 100Gi \
    run
```

* SF = 1
* PostgreSQL 8 loader, indexed
* 2x(1,2) benchmarker = 1 and 2 execution streams (run twice)
* persistent storage of class shared
* monitoring all components

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    TPC-H Queries SF=1
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS. System metrics are monitored by a cluster-wide installation. TPC-H (SF=1) data is loaded and benchmark is executed. Database is persistent on a volume of type shared. Query ordering is Q1 - Q22. All instances use the same query parameters. Import sets indexes and constraints after loading and recomputes statistics. Benchmark is limited to DBMS PostgreSQL. Import is handled by 8 processes (pods). Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217696268
    datadisk:2822608
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
    disk:217696440
    datadisk:2822608
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
    disk:217696440
    datadisk:2822608
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
    disk:217696440
    datadisk:2822608
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
    disk:217696440
    datadisk:2822608
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
    disk:217696440
    datadisk:2822608
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
Pricing Summary Report (TPC-H Q1)                                  13257.74                 2589.36                 2602.81                 6418.42                 2572.30                 2655.10
Minimum Cost Supplier Query (TPC-H Q2)                              4031.91                  425.58                  418.04                 1607.49                  426.32                  414.46
Shipping Priority (TPC-H Q3)                                        5936.66                  738.32                  756.21                 2166.32                  744.43                  752.35
Order Priority Checking Query (TPC-H Q4)                            1238.28                 1244.39                 1226.99                 1267.13                 1236.31                 1225.05
Local Supplier Volume (TPC-H Q5)                                     643.34                  642.07                  651.66                  651.81                  665.66                  648.42
Forecasting Revenue Change (TPC-H Q6)                                481.48                  495.62                  496.70                  536.54                  493.67                  491.10
Forecasting Revenue Change (TPC-H Q7)                                965.08                  753.55                  762.77                  777.54                  756.03                  743.64
National Market Share (TPC-H Q8)                                    1596.33                  599.79                  605.87                  620.09                  608.16                  601.09
Product Type Profit Measure (TPC-H Q9)                              1725.83                 1067.27                 1036.56                 1197.90                 1039.89                 1036.67
Forecasting Revenue Change (TPC-H Q10)                              1221.29                 1261.78                 1236.42                 1230.95                 1214.73                 1222.89
Important Stock Identification (TPC-H Q11)                           243.73                  252.96                  245.01                  244.37                  250.41                  249.33
Shipping Modes and Order Priority (TPC-H Q12)                        998.13                 1010.73                  992.50                 1014.33                 1011.12                 1017.56
Customer Distribution (TPC-H Q13)                                   2009.51                 2052.86                 2044.96                 2008.00                 2060.07                 1989.80
Forecasting Revenue Change (TPC-H Q14)                               524.00                  536.41                  538.43                  525.13                  535.18                  540.81
Top Supplier Query (TPC-H Q15)                                       534.63                  553.73                  557.53                  538.89                  540.58                  545.75
Parts/Supplier Relationship (TPC-H Q16)                              560.50                  576.10                  568.59                  554.11                  560.23                  568.41
Small-Quantity-Order Revenue (TPC-H Q17)                            1798.11                 1944.26                 1843.98                 1885.14                 1810.29                 1836.71
Large Volume Customer (TPC-H Q18)                                   6437.35                 6703.77                 7257.39                 6828.56                 7008.83                 6395.23
Discounted Revenue (TPC-H Q19)                                       679.13                  688.72                  691.35                  686.28                  686.92                  692.58
Potential Part Promotion (TPC-H Q20)                                 844.35                  651.30                  637.95                  685.04                  632.79                  628.11
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                 1963.34                  853.77                  865.35                 1325.26                  873.98                  865.06
Global Sales Opportunity Query (TPC-H Q22)                           282.79                  219.53                  211.45                  232.00                  209.25                  210.55

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           43.0         2.0       93.0     148.0
PostgreSQL-BHT-8-1-2-1           1.0           43.0         2.0       93.0     148.0
PostgreSQL-BHT-8-1-2-2           1.0           43.0         2.0       93.0     148.0
PostgreSQL-BHT-8-2-1-1           1.0           43.0         2.0       93.0     148.0
PostgreSQL-BHT-8-2-2-1           1.0           43.0         2.0       93.0     148.0
PostgreSQL-BHT-8-2-2-2           1.0           43.0         2.0       93.0     148.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           1.29
PostgreSQL-BHT-8-1-2-1           0.87
PostgreSQL-BHT-8-1-2-2           0.87
PostgreSQL-BHT-8-2-1-1           1.04
PostgreSQL-BHT-8-2-2-1           0.86
PostgreSQL-BHT-8-2-2-2           0.87

### Power@Size
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            2905.30
PostgreSQL-BHT-8-1-2-1            4307.58
PostgreSQL-BHT-8-1-2-2            4324.06
PostgreSQL-BHT-8-2-1-1            3596.34
PostgreSQL-BHT-8-2-2-1            4339.26
PostgreSQL-BHT-8-2-2-2            4364.94

### Throughput@Size
                                                   time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                 SF num_experiment num_client                                              
PostgreSQL-BHT-8-1-1 1  1              1                 51      1   1                  1552.94
PostgreSQL-BHT-8-1-2 1  1              2                 29      2   1                  5462.07
PostgreSQL-BHT-8-2-1 1  2              1                 36      1   1                  2200.00
PostgreSQL-BHT-8-2-2 1  2              2                 29      2   1                  5462.07

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       92.44     2.09          7.08                 8.82
PostgreSQL-BHT-8-1-2      235.54     3.79          7.08                 8.82
PostgreSQL-BHT-8-2-1      111.70     0.01          7.56                11.21
PostgreSQL-BHT-8-2-2      330.85     0.00          7.56                11.18

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       11.62      0.0          0.24                 0.25
PostgreSQL-BHT-8-1-2        0.00      0.0          0.24                 0.25
PostgreSQL-BHT-8-2-1       13.30      0.0          0.25                 0.27
PostgreSQL-BHT-8-2-2        0.00      0.0          0.25                 0.27
```


## Benchbase

### Benchbase Simple

```
python benchbase.py -ms 1 -tr \
    -sf 16 \
    -ltf 16 \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -dbms PostgreSQL \
    -nvu 16 \
    -nbp 1 \
    run
```

* 16 warehouses
* 16 terminals in 1 pod at execution
* target is 16384 ops
* no persistent storage

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    Benchbase Workload SF=16 (warehouses for TPC-C)
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS. Benchbase data is generated and loaded using several threads. Benchmark is limited to DBMS PostgreSQL. Benchmark is tpcc. Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19. SUT is fixed to cl-worker11.

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:222106168
    datadisk:4409556
    requests_cpu:4
    requests_memory:16Gi

### Execution
                    experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-BHT-1-1               1         16   16384          1  300.0                       2644.12                                                      13523.0                                               6045.0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Loading
                    time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1      129.0        1.0   1.0                 446.511628
```


### Benchbase Monitoring

```
python benchbase.py -ms 1 -tr \
    -sf 16 \
    -ltf 16 \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -dbms PostgreSQL \
    -nvu 16 \
    -nbp 1 \
    -m -mc \
    -rst shared -rss 50Gi \
    run
```

* 16 warehouses
* 16 terminals in 1 pod at execution
* target is 16384 ops
* monitoring of all components activated
* data is stored persistently in a PV of type shared and size 50Gi

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    Benchbase Workload SF=16 (warehouses for TPC-C)
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS. Benchbase data is generated and loaded using several threads. Benchmark is limited to DBMS PostgreSQL. Benchmark is tpcc. Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19. SUT is fixed to cl-worker11.

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217698780
    datadisk:4408528
    volume_size:50G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                    experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-BHT-1-1               1         16   16384          1  300.0                       2636.29                                                      13427.0                                               6063.0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Loading
                    time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1      132.0        1.0   1.0                 436.363636

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1       657.6     1.56          3.85                 5.23

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      938.94    10.93          1.31                 1.31

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1     2456.61     7.58           4.7                 6.03

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1     1494.24     5.01          1.43                 1.43
```

### Benchbase Complex

```
python benchbase.py -ms 1 -tr \
    -sf 16 \
    -ltf 16 \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -dbms PostgreSQL \
    -nvu 16 \
    -nbp 1,2 \
    -m -mc \
    -rst shared -rss 50Gi \
    -nc 2 \
    run
```

* 16 warehouses
* 16 terminals in 1 pod and 16 terminals in 2 pods (8 each)
* target is 16384 ops
* data is stored persistently in a PV of type shared and size 50Gi
* monitoring of all components activated
* run twice

yields (after ca. 30 minutes) something like

```
## Show Summary

### Workload
    Benchbase Workload SF=16 (warehouses for TPC-C)
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS. Benchbase data is generated and loaded using several threads. Benchmark is limited to DBMS PostgreSQL. Benchmark is tpcc. Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19. SUT is fixed to cl-worker11.

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217698780
    datadisk:7684824
    volume_size:50G
    volume_used:7.4G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-1-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217698952
    datadisk:8304512
    volume_size:50G
    volume_used:8.0G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-2-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217698952
    datadisk:8910600
    volume_size:50G
    volume_used:8.5G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-2-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217698952
    datadisk:9490424
    volume_size:50G
    volume_used:9.1G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                      experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-BHT-1-1-1               1         16   16384          1  300.0                       2360.26                                                      13816.0                                               6773.0
PostgreSQL-BHT-1-2-1               2         16   16384          1  300.0                       2318.62                                                      13639.0                                               6894.0
PostgreSQL-BHT-2-1-1               1         16   16384          2  300.0                       2240.81                                                      15362.0                                               7133.5
PostgreSQL-BHT-2-2-1               2         16   16384          2  300.0                       2089.21                                                      16000.0                                               7652.5

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-1 - Pods [[1], [1]]
DBMS PostgreSQL-BHT-2 - Pods [[2], [2]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1-1      132.0        1.0   1.0                 436.363636
PostgreSQL-BHT-1-2-1      132.0        1.0   1.0                 436.363636
PostgreSQL-BHT-2-1-1      132.0        1.0   2.0                 436.363636
PostgreSQL-BHT-2-2-1      132.0        1.0   2.0                 436.363636

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1     2056.56     7.61          4.59                 7.80
PostgreSQL-BHT-1-2-1     2125.67     7.77          8.27                14.84
PostgreSQL-BHT-2-1-1     1700.43     7.02          4.15                 8.38
PostgreSQL-BHT-2-2-1     1907.63     7.11          7.46                16.03

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1     1284.23     4.89          1.39                 1.39
PostgreSQL-BHT-1-2-1     1284.23     4.91          2.73                 2.73
PostgreSQL-BHT-2-1-1     1116.75     2.38          2.69                 2.69
PostgreSQL-BHT-2-2-1     1116.75     4.77          4.47                 4.47
```



## HammerDB

### HammerDB Simple

```
python hammerdb.py \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -dbms PostgreSQL \
    -nvu '8' \
    -su 16 \
    -sf 16 \
    -nbp 1 \
    run
```

* 16 warehouses
* 16 threads used for loading
* 8 terminals in 1 pod
* no persistent storage

yields (after ca. 10 minutes)

```
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS. TPC-C data is generated and loaded using several threads. Benchmark is limited to DBMS PostgreSQL. Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19. SUT is fixed to cl-worker11.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:221076240
    datadisk:3377616
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  vusers  client  pod_count    NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1       8       1          1  9813.0  30325.0         5       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-16-1 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       84.0       16.0   1.0                 685.714286
```


### HammerDB Monitoring

```
python hammerdb.py \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -dbms PostgreSQL \
    -nvu '8' \
    -su 16 \
    -sf 16 \
    -nbp 1 \
    -m -mc \
    -rst shared -rss 30Gi \
    run
```

* 16 warehouses
* 16 threads used for loading
* 8 terminals in 1 pod
* data is stored persistently in a PV of type shared and size 30Gi
* monitoring of all components activated

yields (after ca. 10 minutes)

```
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS. TPC-C data is generated and loaded using several threads. Benchmark is limited to DBMS PostgreSQL. Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19. SUT is fixed to cl-worker11.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217698788
    datadisk:3382313
    volume_size:30G
    volume_used:3.3G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  vusers  client  pod_count    NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1       8       1          1  9700.0  30240.0         5       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-16-1 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       89.0       16.0   1.0                 647.191011

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      121.48     1.95          3.86                 5.46

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      376.24     6.42          0.13                 0.13

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1    15241.89    36.25          4.73                 6.29

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       36.55     0.09          0.03                 0.03
```

### HammerDB Complex

```
python hammerdb.py \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -dbms PostgreSQL \
    -nvu '8' \
    -su 16 \
    -sf 16 \
    -nbp 1,2 \
    -m -mc \
    -rst shared -rss 30Gi \
    run
```

* 16 warehouses
* 16 threads used for loading
* 8 terminals in 1 pod and in 2 pods (4 terminals each)
* data is stored persistently in a PV of type shared and size 30Gi
* monitoring of all components activated

yields (after ca. 10 minutes)

```
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS. TPC-C data is generated and loaded using several threads. Benchmark is limited to DBMS PostgreSQL. Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19. SUT is fixed to cl-worker11.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217698888
    datadisk:4073833
    volume_size:30G
    volume_used:3.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-16-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217698888
    datadisk:4074253
    volume_size:30G
    volume_used:3.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  vusers  client  pod_count    NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1       8       1          1  5755.0  17903.0         5       0
PostgreSQL-BHT-16-2-1               1       8       1          2  5925.0  18297.5         5       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-16-2 - Pods [[2]]
DBMS PostgreSQL-BHT-16-1 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       89.0       16.0   1.0                 647.191011
PostgreSQL-BHT-16-2-1       89.0       16.0   2.0                 647.191011

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1    12832.23    31.41          5.06                 6.34
PostgreSQL-BHT-16-2-1    12815.67    31.46          4.39                 4.54

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       21.05     0.05          0.03                 0.03
PostgreSQL-BHT-16-2-1       21.95     0.05          0.05                 0.05
```




## YCSB


### YCSB Loader Test for Persistency

```
ython ycsb.py -ms 1 -tr \
    --workload a \
    -nlp 8 \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -ne 1,2 \
    -nc 2 \
    -ltf 1 \
    -rst shared -rss 100Gi \
    run
```

* SF = 1 (1 million rows and operations)
* PostgreSQL
* Workload A
* 64 loader threads, split into 8 parallel pods
* persistent storage of class shared
* [1,2] execute (8 threads in 1 pod and 16 threads in 2 pods)
* target is 16384 ops
* run twice

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries. YCSB is performed using several threads and processes. Benchmark is limited to DBMS ['PostgreSQL']. YCSB data is loaded using several processes. Benchmark is limited to DBMS PostgreSQL. Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19.

### Connections
PostgreSQL-64-8-16384-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217696100
    datadisk:3010336
    volume_size:50G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217696100
    datadisk:3010456
    volume_size:50G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217696100
    datadisk:3010720
    volume_size:50G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217696100
    datadisk:3010808
    volume_size:50G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                           experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-16384-1-1               1        8    2048          1                        2032.52                61500.0             62437                             569.0               62563                               643.0
PostgreSQL-64-8-16384-1-2               1       16    4096          2                        4081.10                61270.0            124970                             542.0              125030                               620.5
PostgreSQL-64-8-16384-2-1               2        8    2048          1                        2039.85                61279.0             62725                             554.0               62275                               623.0
PostgreSQL-64-8-16384-2-2               2       16    4096          2                        4076.81                61362.0            125223                             548.0              124777                               622.5
```

### YCSB Execution

```
python ycsb.py -ms 1 --workload a -tr \
    -nlp 8 -su 64 \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -ne 1,8 \
    -nc 1 \
    -ltf 1 \
    -rst shared -rss 100Gi \
    run
```

* SF = 1 (1 million rows and operations)
* workload A
* 64 loader threads, split into 8 parallel pods, so each pod has 8 threads
* 8 execution threads, used 1x (=8 threads) and 8x (=64 threads)
* target is 16384 ops
* persistent storage of class shared

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries. YCSB is performed using several threads and processes. Benchmark is limited to DBMS ['PostgreSQL']. YCSB data is loaded using several processes. Benchmark is limited to DBMS PostgreSQL. Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19.

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217696268
    datadisk:3010848
    volume_size:50G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217696268
    datadisk:3011080
    volume_size:50G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-16384-1               1        8    2048          1                        2038.62                61316.0             62479                             532.0               62521                              600.00
PostgreSQL-64-8-16384-2               1       64   16384          8                       16318.74                61299.0            499792                             414.5              500208                              509.38
```

### YCSB Execution Monitoring

```
python ycsb.py -ms 1 --workload a -tr \
    -nlp 8 -su 64 \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -ne 1,8 \
    -nc 1 \
    -ltf 1 \
    -rst shared -rss 100Gi \
    -m -mc \
    run
```

* SF = 1 (1 million rows and operations)
* workload A
* 64 loader threads, split into 8 parallel pods, so each pod has 8 threads
* 8 execution threads, used 1x (=8 threads) and 8x (=64 threads)
* target is 16384 ops
* persistent storage of class shared
* monitoring of all components activated

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    YCSB SF=1
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries. YCSB is performed using several threads and processes. Benchmark is limited to DBMS ['PostgreSQL']. YCSB data is loaded using several processes. Benchmark is limited to DBMS PostgreSQL. Loading is fixed to cl-worker19. Benchmarking is fixed to cl-worker19.

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217696268
    datadisk:3011336
    volume_size:50G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-16384-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:217696268
    datadisk:3011376
    volume_size:50G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-16384-1               1        8    2048          1                         2035.7                61404.0             62697                             566.0               62303                              645.00
PostgreSQL-64-8-16384-2               1       64   16384          8                        16319.4                61300.0            499950                             458.5              500050                              575.25

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1       12.69      0.0          2.70                 4.28
PostgreSQL-64-8-16384-2      172.72      0.0          3.66                 5.20

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1        7.98     0.00          0.15                 0.15
PostgreSQL-64-8-16384-2      102.72     0.75          2.27                 2.30
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
