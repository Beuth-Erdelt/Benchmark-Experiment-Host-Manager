# Test Cases


## TPC-H

### TPC-H Simple

`python tpch.py -dt -nlp 8 -nlt 8 -sf 1 -ii -ic -is -dbms PostgreSQL run`

* SF=1, loaded by 8 pods, indexed, into PostgreSQL
* 1 execution stream (power test)

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    TPC-H Queries SF=1
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS. TPC-H (SF=1) data is loaded and benchmark is executed. Query ordering is Q1 - Q22. All instances use the same query parameters. Import sets indexes and constraints after loading and recomputes statistics. Benchmark is limited to DBMS PostgreSQL. Import is handled by 8 processes (pods).

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541031743488
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.4.0-105-generic
    node:cl-worker13
    disk:1385092992
    datadisk:2821956
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2601.87
Minimum Cost Supplier Query (TPC-H Q2)                             431.58
Shipping Priority (TPC-H Q3)                                       781.74
Order Priority Checking Query (TPC-H Q4)                          1275.76
Local Supplier Volume (TPC-H Q5)                                   680.63
Forecasting Revenue Change (TPC-H Q6)                              525.88
Forecasting Revenue Change (TPC-H Q7)                              794.17
National Market Share (TPC-H Q8)                                   660.05
Product Type Profit Measure (TPC-H Q9)                            1130.91
Forecasting Revenue Change (TPC-H Q10)                            1275.62
Important Stock Identification (TPC-H Q11)                         254.10
Shipping Modes and Order Priority (TPC-H Q12)                     1043.09
Customer Distribution (TPC-H Q13)                                 2024.57
Forecasting Revenue Change (TPC-H Q14)                             559.11
Top Supplier Query (TPC-H Q15)                                     560.91
Parts/Supplier Relationship (TPC-H Q16)                            562.22
Small-Quantity-Order Revenue (TPC-H Q17)                          2109.44
Large Volume Customer (TPC-H Q18)                                 7686.77
Discounted Revenue (TPC-H Q19)                                     711.37
Potential Part Promotion (TPC-H Q20)                               682.24
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                910.92
Global Sales Opportunity Query (TPC-H Q22)                         239.39

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           36.0         1.0       99.0     146.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1            0.9

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4128.12

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 1  1              1                 30      1   1                   2640.0
```


### TPC-H Monitoring

`python tpch.py -dt -nlp 8 -nlt 8 -sf 1 -ii -ic -is -dbms PostgreSQL -m -mc run`

* SF=1, loaded by 8 pods, indexed, into PostgreSQL
* 1 execution stream (power test)

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    TPC-H Queries SF=1
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS. System metrics are monitored by a cluster-wide installation. TPC-H (SF=1) data is loaded and benchmark is executed. Query ordering is Q1 - Q22. All instances use the same query parameters. Import sets indexes and constraints after loading and recomputes statistics. Benchmark is limited to DBMS PostgreSQL. Import is handled by 8 processes (pods).

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541037633536
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.4.0-81-generic
    node:cl-worker11
    disk:481544128
    datadisk:2822656
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2528.85
Minimum Cost Supplier Query (TPC-H Q2)                             482.59
Shipping Priority (TPC-H Q3)                                       708.84
Order Priority Checking Query (TPC-H Q4)                          1196.86
Local Supplier Volume (TPC-H Q5)                                   629.17
Forecasting Revenue Change (TPC-H Q6)                              475.77
Forecasting Revenue Change (TPC-H Q7)                              736.05
National Market Share (TPC-H Q8)                                   574.13
Product Type Profit Measure (TPC-H Q9)                            1050.75
Forecasting Revenue Change (TPC-H Q10)                            1205.52
Important Stock Identification (TPC-H Q11)                         297.17
Shipping Modes and Order Priority (TPC-H Q12)                      981.64
Customer Distribution (TPC-H Q13)                                 1924.88
Forecasting Revenue Change (TPC-H Q14)                             514.42
Top Supplier Query (TPC-H Q15)                                     520.62
Parts/Supplier Relationship (TPC-H Q16)                            542.13
Small-Quantity-Order Revenue (TPC-H Q17)                          1955.76
Large Volume Customer (TPC-H Q18)                                 6925.62
Discounted Revenue (TPC-H Q19)                                     666.19
Potential Part Promotion (TPC-H Q20)                               748.62
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                877.59
Global Sales Opportunity Query (TPC-H Q22)                         225.91

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           0.0           29.0         1.0       89.0     128.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.86

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1             4320.0

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 1  1              1                 28      1   1                  2828.57

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      150.57     0.69          3.75                 4.93

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        0.88        0          0.22                 0.42

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       14.36     0.27          3.75                 4.93

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1           0        0           0.0                  0.0

```




## Benchbase

### Benchbase Simple

`python benchbase.py -ltf 16 -dbms PostgreSQL -nvu 16 -sf 16 -nbp 1 run`

* 16 warehouses
* 16 terminals in 1 pod
* target is 16384 ops

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    Benchbase Workload SF=16 (warehouses for TPC-C)
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS. Benchbase data is generated and loaded using several threads. Benchmark is limited to DBMS PostgreSQL. Benchmark is tpcc.

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541031743488
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.4.0-105-generic
    node:cl-worker13
    disk:1386631412
    datadisk:4409168
    requests_cpu:4
    requests_memory:16Gi

### Execution
                    experiment_run  terminals  target  pod_count  time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-BHT-1-1               1         16   16384          1  60.0                       2421.65                                                      11612.0                                               6561.0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Loading
                    time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1      253.0        1.0   1.0                 227.667984

```


### Benchbase Monitoring

`python benchbase.py -ltf 16 -dbms PostgreSQL -nvu 16 -sf 16 -nbp 1 -m -mc run`

* 16 warehouses
* 16 terminals in 1 pod
* target is 16384 ops
* monitoring of all components activated

yields (after ca. 10 minutes) something like

```
## Show Summary

### Workload
    Benchbase Workload SF=16 (warehouses for TPC-C)
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS. Benchbase data is generated and loaded using several threads. Benchmark is limited to DBMS PostgreSQL. Benchmark is tpcc.

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541031743488
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.4.0-105-generic
    node:cl-worker13
    disk:1386664796
    datadisk:4409156
    requests_cpu:4
    requests_memory:16Gi

### Execution
                    experiment_run  terminals  target  pod_count  time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-BHT-1-1               1         16   16384          1  60.0                       2323.43                                                      16084.0                                               6873.0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Loading
                    time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1      224.0        1.0   1.0                 257.142857

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      446.37     4.14          3.56                 4.65

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1     2334.13     5.74          1.32                 1.32

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      280.62        0          4.22                 5.95

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      193.35        0          1.41                 1.41
```



## HammerDB

### HammerDB Simple

`python hammerdb.py -dbms PostgreSQL -nvu "8" -su 16 -sf 16 -nbp 2 run`

* 16 warehouses
* 16 threads used for loading
* 8 terminals in 2 pod

yields (after ca. 10 minutes)

```
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS. TPC-C data is generated and loaded using several threads. Benchmark is limited to DBMS PostgreSQL.

### Connections
PostgreSQL-BHT-16-2-1 uses docker image postgres:16.1
    RAM:541037633536
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.4.0-81-generic
    node:cl-worker11
    disk:450769736
    datadisk:3376936
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  vusers  client  pod_count    NOPM      TPM  duration  errors
PostgreSQL-BHT-16-2-1               1       8       1          2  9728.0  30066.0         5       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-16-2 - Pods [[2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-2-1       94.0       16.0   2.0                 612.765957
```


### HammerDB Monitoring

`python hammerdb.py -dbms PostgreSQL -nvu "8" -su 16 -sf 16 -nbp 2 -m -mc run`

* 16 warehouses
* 16 threads used for loading
* 8 terminals in 2 pod
* monitoring of all components activated

yields (after ca. 10 minutes)

```
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS. TPC-C data is generated and loaded using several threads. Benchmark is limited to DBMS PostgreSQL.

### Connections
PostgreSQL-BHT-16-2-1 uses docker image postgres:16.1
    RAM:541037633536
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.4.0-81-generic
    node:cl-worker11
    disk:448286468
    datadisk:3376856
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  vusers  client  pod_count    NOPM      TPM  duration  errors
PostgreSQL-BHT-16-2-1               1       8       1          2  9223.5  28412.5         5       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-16-2 - Pods [[2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-2-1       84.0       16.0   2.0                 685.714286

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-2-1      118.88     2.02          3.73                 4.42

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-2-1      291.54        0          0.14                 0.14

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-2-1    15336.25    36.38          5.02                  5.6

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-2-1        7.32     0.01          0.05                 0.05
```


## YCSB


### YCSB Execution

`python ycsb.py -ltf 1 -nlp 8 -su 64 -sf 1 -dbms PostgreSQL -wl a run`

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
    This experiment compares run time and resource consumption of YCSB queries. YCSB is performed using several threads and processes. Benchmark is limited to DBMS ['PostgreSQL']. YCSB data is loaded using several processes. Benchmark is limited to DBMS PostgreSQL.

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541037633536
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.4.0-81-generic
    node:cl-worker11
    disk:449814036
    datadisk:2455656
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-16384               1       64   16384          8                   16336.733043                61226.0             1000000                            1075.375

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-16384-1               1       64   16384          8                       16334.03                61253.0            499897                            549.88              500103                               730.0
```

### YCSB Execution Monitoring

`python ycsb.py -ltf 1 -nlp 8 -su 64 -sf 1 -dbms PostgreSQL -wl a -m -mc run`

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
    This experiment compares run time and resource consumption of YCSB queries. YCSB is performed using several threads and processes. Benchmark is limited to DBMS ['PostgreSQL']. YCSB data is loaded using several processes. Benchmark is limited to DBMS PostgreSQL.

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541037633536
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.4.0-81-generic
    node:cl-worker11
    disk:449991980
    datadisk:2457792
    requests_cpu:4
    requests_memory:16Gi

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-16384               1       64   16384          8                   16334.332193                61247.0             1000000                              1690.5

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-16384-1               1       64   16384          8                        16336.5                61229.0            500216                            669.62              499784                              882.75

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      146.17     2.71          3.65                 4.31

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1        0.16        0          0.01                 0.01

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      177.59     2.78          3.99                 4.85

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1        13.6        0          0.32                 0.33
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
