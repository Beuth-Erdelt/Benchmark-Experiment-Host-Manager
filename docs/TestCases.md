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
    disk:249196752
    datadisk:2823016
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2493.16
Minimum Cost Supplier Query (TPC-H Q2)                             414.27
Shipping Priority (TPC-H Q3)                                       724.43
Order Priority Checking Query (TPC-H Q4)                          1239.55
Local Supplier Volume (TPC-H Q5)                                   619.84
Forecasting Revenue Change (TPC-H Q6)                              478.67
Forecasting Revenue Change (TPC-H Q7)                              744.60
National Market Share (TPC-H Q8)                                   587.28
Product Type Profit Measure (TPC-H Q9)                            1065.18
Forecasting Revenue Change (TPC-H Q10)                            1214.05
Important Stock Identification (TPC-H Q11)                         247.10
Shipping Modes and Order Priority (TPC-H Q12)                      984.09
Customer Distribution (TPC-H Q13)                                 2038.24
Forecasting Revenue Change (TPC-H Q14)                             517.57
Top Supplier Query (TPC-H Q15)                                     532.80
Parts/Supplier Relationship (TPC-H Q16)                            558.68
Small-Quantity-Order Revenue (TPC-H Q17)                          1947.05
Large Volume Customer (TPC-H Q18)                                 7059.62
Discounted Revenue (TPC-H Q19)                                     667.85
Potential Part Promotion (TPC-H Q20)                               657.55
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                902.79
Global Sales Opportunity Query (TPC-H Q22)                         232.66

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
PostgreSQL-BHT-8-1-1            4356.34

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
TPC-H (SF=3) data is loaded and benchmark is executed.
Query ordering is Q1 - Q22.
All instances use the same query parameters.
Import sets indexes and constraints after loading and recomputes statistics.
System metrics are monitored by a cluster-wide installation.
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
    disk:254757072
    datadisk:8383336
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 6188.20
Minimum Cost Supplier Query (TPC-H Q2)                            2074.19
Shipping Priority (TPC-H Q3)                                      2375.46
Order Priority Checking Query (TPC-H Q4)                          3025.23
Local Supplier Volume (TPC-H Q5)                                  2212.66
Forecasting Revenue Change (TPC-H Q6)                             1149.08
Forecasting Revenue Change (TPC-H Q7)                             2265.09
National Market Share (TPC-H Q8)                                  1397.82
Product Type Profit Measure (TPC-H Q9)                            3202.67
Forecasting Revenue Change (TPC-H Q10)                            3122.82
Important Stock Identification (TPC-H Q11)                         559.37
Shipping Modes and Order Priority (TPC-H Q12)                     2431.24
Customer Distribution (TPC-H Q13)                                 6557.62
Forecasting Revenue Change (TPC-H Q14)                            1239.35
Top Supplier Query (TPC-H Q15)                                    1362.21
Parts/Supplier Relationship (TPC-H Q16)                           1294.57
Small-Quantity-Order Revenue (TPC-H Q17)                          5782.30
Large Volume Customer (TPC-H Q18)                                20626.61
Discounted Revenue (TPC-H Q19)                                    1866.65
Potential Part Promotion (TPC-H Q20)                              1192.11
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               2850.45
Global Sales Opportunity Query (TPC-H Q22)                         462.22

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          104.0         1.0      212.0     325.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1            2.3

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4822.01

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 3  1              1                 77      1   3                  3085.71

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      392.24     1.41          6.39                10.64

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        8.52     0.06          0.76                 2.28

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      173.81     3.51          6.63                10.87

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       11.17        0          0.24                 0.25
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
TPC-H (SF=1) data is loaded and benchmark is executed.
Query ordering is Q1 - Q22.
All instances use the same query parameters.
Import sets indexes and constraints after loading and recomputes statistics.
System metrics are monitored by a cluster-wide installation.
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
    disk:246373904
    datadisk:2822984
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
    disk:246373904
    datadisk:2822984
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
    disk:246373904
    datadisk:2822984
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
    disk:246373884
    datadisk:2822984
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
    disk:246373884
    datadisk:2822984
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
    disk:246373884
    datadisk:2822984
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
Pricing Summary Report (TPC-H Q1)                                   2672.44                 2525.77                 2543.15                14990.48                 2508.68                 2512.74
Minimum Cost Supplier Query (TPC-H Q2)                               807.42                  416.50                  419.34                 3454.00                  414.38                  423.96
Shipping Priority (TPC-H Q3)                                        1302.45                  729.22                  725.37                 4798.06                  752.29                  758.35
Order Priority Checking Query (TPC-H Q4)                            1233.78                 1210.91                 1230.73                 1237.82                 1262.13                 1237.96
Local Supplier Volume (TPC-H Q5)                                     622.07                  642.54                  633.58                  641.07                  669.24                  663.98
Forecasting Revenue Change (TPC-H Q6)                                471.98                  493.60                  486.25                  489.24                  505.34                  508.09
Forecasting Revenue Change (TPC-H Q7)                               1270.33                  732.61                  725.63                 1003.42                  765.38                  751.80
National Market Share (TPC-H Q8)                                     836.68                  598.53                  589.10                  713.36                  612.28                  612.50
Product Type Profit Measure (TPC-H Q9)                              1838.59                 1036.77                 1047.79                 1570.29                 1082.44                 1036.73
Forecasting Revenue Change (TPC-H Q10)                              1191.01                 1175.82                 1191.82                 1218.83                 1236.26                 1221.05
Important Stock Identification (TPC-H Q11)                           239.93                  244.18                  246.99                  243.92                  251.36                  250.40
Shipping Modes and Order Priority (TPC-H Q12)                        984.48                  992.87                  989.47                  992.03                 1014.93                  993.86
Customer Distribution (TPC-H Q13)                                   1902.72                 1908.29                 1890.49                 1944.39                 1963.85                 1955.49
Forecasting Revenue Change (TPC-H Q14)                               509.20                  512.61                  509.94                  523.72                  549.72                  538.19
Top Supplier Query (TPC-H Q15)                                       524.90                  540.52                  536.65                  541.40                  553.32                  551.25
Parts/Supplier Relationship (TPC-H Q16)                              563.82                  562.94                  561.51                  558.85                  559.16                  560.83
Small-Quantity-Order Revenue (TPC-H Q17)                            1783.72                 1840.77                 1818.46                 1840.48                 2064.88                 1893.64
Large Volume Customer (TPC-H Q18)                                   7326.47                 7453.61                 7426.17                 6149.28                 8190.63                 7986.14
Discounted Revenue (TPC-H Q19)                                       657.22                  671.44                  662.57                  680.59                  688.21                  690.03
Potential Part Promotion (TPC-H Q20)                                 643.95                  633.65                  632.16                  634.58                  660.55                  648.07
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                 1912.28                  869.46                  850.06                 1782.10                  876.62                  850.13
Global Sales Opportunity Query (TPC-H Q22)                           261.03                  217.09                  215.63                  261.08                  213.14                  215.21

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           26.0         2.0       98.0     133.0
PostgreSQL-BHT-8-1-2-1           1.0           26.0         2.0       98.0     133.0
PostgreSQL-BHT-8-1-2-2           1.0           26.0         2.0       98.0     133.0
PostgreSQL-BHT-8-2-1-1           1.0           26.0         2.0       98.0     133.0
PostgreSQL-BHT-8-2-2-1           1.0           26.0         2.0       98.0     133.0
PostgreSQL-BHT-8-2-2-2           1.0           26.0         2.0       98.0     133.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           1.00
PostgreSQL-BHT-8-1-2-1           0.85
PostgreSQL-BHT-8-1-2-2           0.85
PostgreSQL-BHT-8-2-1-1           1.19
PostgreSQL-BHT-8-2-2-1           0.89
PostgreSQL-BHT-8-2-2-2           0.87

### Power@Size
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            3735.71
PostgreSQL-BHT-8-1-2-1            4393.11
PostgreSQL-BHT-8-1-2-2            4409.71
PostgreSQL-BHT-8-2-1-1            3125.54
PostgreSQL-BHT-8-2-2-1            4252.42
PostgreSQL-BHT-8-2-2-2            4303.51

### Throughput@Size
                                                   time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                 SF num_experiment num_client                                              
PostgreSQL-BHT-8-1-1 1  1              1                 37      1   1                  2140.54
PostgreSQL-BHT-8-1-2 1  1              2                 29      2   1                  5462.07
PostgreSQL-BHT-8-2-1 1  2              1                 50      1   1                  1584.00
PostgreSQL-BHT-8-2-2 1  2              2                 31      2   1                  5109.68

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      108.89     0.02          3.69                 5.37
PostgreSQL-BHT-8-1-2      108.89     0.02          3.69                 5.37

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1           0        0           0.0                  0.0
PostgreSQL-BHT-8-1-2           0        0           0.0                  0.0

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       93.63     0.00          7.28                 7.55
PostgreSQL-BHT-8-1-2       13.61     0.00          7.28                 7.55
PostgreSQL-BHT-8-2-1        0.56     0.01          6.15                 6.70
PostgreSQL-BHT-8-2-2      484.46     0.00          7.58                 9.75

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       11.81      0.0          0.22                 0.23
PostgreSQL-BHT-8-1-2        0.00      0.0          0.22                 0.23
PostgreSQL-BHT-8-2-1        0.00      0.0          0.00                 0.00
PostgreSQL-BHT-8-2-2        0.00      0.0          0.00                 0.00
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
Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [].
Benchmark is limited to DBMS PostgreSQL.
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
    disk:250783132
    datadisk:4409244
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0                       2640.05                                                      13265.0                                               6054.0

Warehouses: 16

### Workflow
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      123.0        1.0   1.0                 468.292683
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
Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 1 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [].
Benchmark is limited to DBMS PostgreSQL.
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
    disk:246373884
    datadisk:4409104
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
    disk:246373884
    datadisk:5110288
    volume_size:50G
    volume_used:4.9G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  terminals  target  pod_count  time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1         16    8192          1  60.0                       2523.45                                                      14188.0                                               6329.0
PostgreSQL-1-1-1024-2-1               2         16    8192          1  60.0                       1540.08                                                      14727.0                                              10377.0

Warehouses: 16

### Workflow
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

### Loading
                         time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1-1      149.0        1.0   1.0                 386.577181
PostgreSQL-1-1-1024-2-1      149.0        1.0   1.0                 386.577181
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
Benchbase data is generated and loaded using several threads.
Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [].
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS PostgreSQL.
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
    disk:250783436
    datadisk:4409548
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0                       2645.79                                                      13363.0                                               6041.0

Warehouses: 16

### Workflow
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1      133.0        1.0   1.0                 433.082707

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      811.76        0          4.01                 5.64

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1111.02    11.38          1.34                 1.34

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     2065.99     7.49          4.84                 7.13

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1303.79     4.91          1.43                 1.43
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
Benchbase data is generated and loaded using several threads.
Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 2 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [].
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS PostgreSQL.
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
    disk:246373884
    datadisk:4274592
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
    disk:246373884
    datadisk:4382720
    volume_size:50G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-3 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246373884
    datadisk:4634176
    volume_size:50G
    volume_used:4.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-1-4 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374052
    datadisk:4964192
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
    disk:246374052
    datadisk:5901576
    volume_size:50G
    volume_used:5.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-1-1-1024-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:246374052
    datadisk:6016656
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
    disk:246374052
    datadisk:6274416
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
    disk:246374052
    datadisk:6411736
    volume_size:50G
    volume_used:5.8G
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1          8    8192          1  120.0                       1028.55                                                      12618.0                                              7768.00
PostgreSQL-1-1-1024-1-2               1         16   16384          2  120.0                       2408.42                                                      15433.0                                              6634.00
PostgreSQL-1-1-1024-1-3               1          8    8192          2  120.0                       1300.57                                                      13805.0                                              6140.00
PostgreSQL-1-1-1024-1-4               1         16   16384          4  120.0                       1992.49                                                      18331.0                                              8018.75
PostgreSQL-1-1-1024-2-1               2          8    8192          1  120.0                       1095.30                                                      12173.0                                              7294.00
PostgreSQL-1-1-1024-2-2               2         16   16384          2  120.0                       2488.65                                                      15011.0                                              6419.00
PostgreSQL-1-1-1024-2-3               2          8    8192          2  120.0                       1344.85                                                      13752.0                                              5937.50
PostgreSQL-1-1-1024-2-4               2         16   16384          4  120.0                       2103.45                                                      17977.0                                              7594.50

Warehouses: 16

### Workflow
DBMS PostgreSQL-1-1-1024 - Pods [[4, 2, 2, 1], [2, 4, 2, 1]]

### Loading
                         time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-1-1-1024-1-1      149.0        1.0   1.0                 386.577181
PostgreSQL-1-1-1024-1-2      149.0        1.0   2.0                 386.577181
PostgreSQL-1-1-1024-1-3      149.0        1.0   2.0                 386.577181
PostgreSQL-1-1-1024-1-4      149.0        1.0   4.0                 386.577181
PostgreSQL-1-1-1024-2-1      149.0        1.0   1.0                 386.577181
PostgreSQL-1-1-1024-2-2      149.0        1.0   2.0                 386.577181
PostgreSQL-1-1-1024-2-3      149.0        1.0   2.0                 386.577181
PostgreSQL-1-1-1024-2-4      149.0        1.0   4.0                 386.577181

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      147.29     0.04          3.00                 5.20
PostgreSQL-1-1-1024-1-2      507.27     7.11          3.58                 6.01
PostgreSQL-1-1-1024-1-3      305.77     1.43          3.79                 6.42
PostgreSQL-1-1-1024-1-4      516.16     0.00          4.07                 6.88
PostgreSQL-1-1-1024-2-1      189.92     3.48          7.14                12.87
PostgreSQL-1-1-1024-2-2      618.11     2.24          3.82                 6.94
PostgreSQL-1-1-1024-2-3      292.17     3.55          4.01                 7.28
PostgreSQL-1-1-1024-2-4      562.41     0.00          4.33                 7.82

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      230.76     1.06          1.32                 1.32
PostgreSQL-1-1-1024-1-2      297.47     2.55          3.97                 3.97
PostgreSQL-1-1-1024-1-3      230.76     0.00          4.88                 4.88
PostgreSQL-1-1-1024-1-4      315.54     2.08          5.08                 5.08
PostgreSQL-1-1-1024-2-1      233.12     0.00          3.05                 3.05
PostgreSQL-1-1-1024-2-2      357.43     2.48          3.47                 3.47
PostgreSQL-1-1-1024-2-3      167.33     1.27          4.75                 4.75
PostgreSQL-1-1-1024-2-4      310.40     0.00          5.77                 5.77
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
