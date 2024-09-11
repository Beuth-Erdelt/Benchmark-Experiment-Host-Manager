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
-
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

yields (after ca. 45 minutes)

```
-
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
-
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
    This experiment compares run time and resource consumption of YCSB queries. YCSB is performed using several threads and processes.
Workload is 'E'.
Number of rows to insert is 1000000.
Number of operations is 1000000.
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
    disk:245719468
    datadisk:3847736
    volume_size:100G
    volume_used:3.7G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)  [SCAN].Return=OK  [SCAN].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1               1       64  131072          8                        22546.0                45403.0               49981                             2948.25            950019                            5881.5
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
    This experiment compares run time and resource consumption of YCSB queries. YCSB is performed using several threads and processes.
Workload is 'A'.
Number of rows to insert is 10000000.
Number of operations is 10000000.
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
    disk:245719476
    datadisk:23872128
    volume_size:100G
    volume_used:23G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-64-8-131072-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:245719476
    datadisk:28726024
    volume_size:100G
    volume_used:23G
    requests_cpu:4
    requests_memory:16Gi

### Loading
                        experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-131072               1       64  131072          8                   47426.242222               213614.0            10000000                              7397.0

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-131072-1               1       64  131072          1                      102405.51                97651.0           5001309                           2539.00             4998691                             3671.00
PostgreSQL-64-8-131072-2               1       64  131072          8                      130365.03                77194.0           4997369                           1372.75             5002631                             1781.62

### Ingestion - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1     1758.64     8.51         14.44                 25.5
PostgreSQL-64-8-131072-2     1758.64     8.51         14.44                 25.5

### Ingestion - Loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1     1138.96      1.7          4.62                 4.64
PostgreSQL-64-8-131072-2     1138.96      1.7          4.62                 4.64

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1     1913.85     0.00         17.34                26.97
PostgreSQL-64-8-131072-2     1755.38     6.88         17.41                27.24

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-131072-1      568.84     0.00          0.60                 0.61
PostgreSQL-64-8-131072-2      685.63     4.89          5.17                 5.20
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
