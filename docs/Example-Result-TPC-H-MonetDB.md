# Example Result: MonetDB running TPC-H at SF=100

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

This example shows how to run Q1-Q22 derived from TPC-H in MonetDB at SF=100.
It covers the power and the throughput test.
The refresh stream is not included.

> The query file is derived from the TPC-H and as such is not comparable to published TPC-H results, as the query file results do not comply with the TPC-H Specification.

Official TPC-H benchmark - http://www.tpc.org/tpch

**The results are not official benchmark results. The exact performance depends on a collection of parameters.
The purpose of this example is to illustrate the usage of bexhoma and to show how to evaluate results.**



## Generate and Load Data

At first we generate TPC-H data at SF=100 (`-sf`) with 8 parallel generators (`-nlp`).
The generated data is stored at the shared disk `data`.
Moreover the data is loaded into an instance of MonetDB using again 8 parallel loaders.
Afterwards the script creates contraints (`-ic`) and indexes (`-ii`) and updates table statistics (`-is`).
The database is located in another shared disk of storageClass shared (`-rst`) and of size 300Gi (`-rss`).

The script also runs a power test (`-ne` set to 1) with timeout 1200s (`-t`) and data transfer activated (`-dt`) once (`-nc` set to 1).
To avoid conflicts with other experiments we set a maximum of 1 DBMS per time (`-ms`).
Monitoring is activated (`-m`) for all components (`-mc`).
The components, that is the SUT (`-rnn`) and the loader (`-rnl`) and the benchmark driver (`-rnb`), are fixed to specific nodes in the cluster.

```bash
mkdir -p ./logs_tests/

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"

nohup python tpch.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 1200 -dt \
  -rst shared -rss 300Gi \
  run &>logs_tests/test_tpch_monetdb_1.log &
```

### Status Data Disk

You can watch the status of the data disk via `bexperiments data`.

In the following example output we see we have generated TPC-H at SF=100 using 8 generators.
The data set is split into 8 parts, each of about 14G size.
In total the data set has a size of 106G.

```
14G     /data/tpch/SF100/8/8
14G     /data/tpch/SF100/8/3
14G     /data/tpch/SF100/8/2
14G     /data/tpch/SF100/8/4
14G     /data/tpch/SF100/8/1
14G     /data/tpch/SF100/8/5
14G     /data/tpch/SF100/8/7
14G     /data/tpch/SF100/8/6
106G    /data/tpch/SF100/8
106G    /data/tpch/SF100
```

### Status Database and Benchmark

You can watch the status of experiments via `bexperiments status`

In the following example output we see all components of bexhoma are up and running.
The cluster stores a MonetDB database corresponding to TPC-H of SF=100.
The disk is of storageClass shared and of size 300Gi and 210G of that space is used.
It took about 7000s to build this database.
Currently no DBMS is running.

```
Dashboard: Running
Message Queue: Running
Data directory: Running
Result directory: Running
Cluster Prometheus: Running
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                            | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+====================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-monetdb-tpch-100   | monetdb         | tpch-100     | True         |              7061 | MonetDB    | shared               | 300Gi     | Bound    | 300G   | 210G   |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

### Summary of Results

At the end of a benchmark you will see a summary like

```
## Show Summary

### Workload
    TPC-H Queries SF=100
    Type: tpch
    Duration: 1561s 
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
TPC-H (SF=100) data is loaded and benchmark is executed.
Query ordering is Q1 - Q22.
All instances use the same query parameters.
Import sets indexes and constraints after loading and recomputes statistics.
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS ['MonetDB'].
Import is handled by 8 processes (pods).
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Database is persisted to disk of type shared and size 300Gi.
Loading is tested with [8] threads, split into [8] pods.
Benchmarking is tested with [1] threads, split into [1] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248937336
    datadisk:219980774
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                            508802.09
Minimum Cost Supplier Query (TPC-H Q2)                        24962.95
Shipping Priority (TPC-H Q3)                                  71313.39
Order Priority Checking Query (TPC-H Q4)                      80403.50
Local Supplier Volume (TPC-H Q5)                              40913.30
Forecasting Revenue Change (TPC-H Q6)                          7938.59
Forecasting Revenue Change (TPC-H Q7)                          9985.11
National Market Share (TPC-H Q8)                             107720.65
Product Type Profit Measure (TPC-H Q9)                        25396.84
Forecasting Revenue Change (TPC-H Q10)                        62786.26
Important Stock Identification (TPC-H Q11)                     5700.47
Shipping Modes and Order Priority (TPC-H Q12)                 11409.59
Customer Distribution (TPC-H Q13)                            197643.30
Forecasting Revenue Change (TPC-H Q14)                         5568.05
Top Supplier Query (TPC-H Q15)                                 6033.67
Parts/Supplier Relationship (TPC-H Q16)                       14113.55
Small-Quantity-Order Revenue (TPC-H Q17)                      39230.91
Large Volume Customer (TPC-H Q18)                             50969.62
Discounted Revenue (TPC-H Q19)                                14224.12
Potential Part Promotion (TPC-H Q20)                           7437.25
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           21842.68
Global Sales Opportunity Query (TPC-H Q22)                     6557.48

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0         1686.0         7.0     5358.0    7061.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           25.8

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           14220.39

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               1338      1  100                  5919.28

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     6415.92    17.61         45.33                 85.6

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       21.96     0.02          0.33                 0.35

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]

TEST passed: Workflow as planned
```

To see the summary again you can simply call `bexperiments summary -e 1708411664` with the experiment code.

### Status Data Disk

You can inspect a preview list of results via `bexperiments localresults`.

```
+------------+----------------------+------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+-------------+---------------------+
|   index    |         name         |                                                                                           info |                       intro                       | queries | connections |         time        |
+------------+----------------------+------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+-------------+---------------------+
| 1708411664 | TPC-H Queries SF=100 | This experiment compares run time and resource consumption of TPC-H queries in different DBMS. |    This includes the reading queries of TPC-H.    |    22   |      28     | 2024-02-20 11:37:30 |
|            |                      |                                TPC-H data is loaded from a filesystem using several processes. |                                                   |         |             |                     |
|            |                      |                                                             Import is limited to DBMS MonetDB. |                                                   |         |             |                     |
|            |                      |                                                              Import is handled by 1 processes. |                                                   |         |             |                     |
|            |                      |                                                               Loading is fixed to cl-worker19. |                                                   |         |             |                     |
|            |                      |                                                          Benchmarking is fixed to cl-worker19. |                                                   |         |             |                     |
+------------+----------------------+------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+-------------+---------------------+
```

## Perform Benchmark - Power Test

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other (`-ne 1,1`), and shut down the DBMS.
This is repeated 3 times (`-nc`).


```bash
mkdir -p ./logs/

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"

nohup python tpch.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 3 -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 1200 -dt \
  -rst shared -rss 300Gi \
  run &>logs_tests/test_tpch_monetdb_2.log &
```

yields

```
## Show Summary

### Workload
    TPC-H Queries SF=100
    Type: tpch
    Duration: 4675s 
    Code: 1728050276
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
TPC-H (SF=100) data is loaded and benchmark is executed.
Query ordering is Q1 - Q22.
All instances use the same query parameters.
Import sets indexes and constraints after loading and recomputes statistics.
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS ['MonetDB'].
Import is handled by 8 processes (pods).
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Database is persisted to disk of type shared and size 300Gi.
Loading is tested with [8] threads, split into [8] pods.
Benchmarking is tested with [1] threads, split into [1] pods.
Benchmarking is run as [1, 1] times the number of benchmarking pods.
Experiment is run 2 times.

### Connections
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944868
    datadisk:219980808
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248945040
    datadisk:219980810
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248945040
    datadisk:219980811
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248945040
    datadisk:219980813
    volume_size:300G
    volume_used:215G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
Pricing Summary Report (TPC-H Q1)                              505174.61            225816.02            504923.89            220729.45
Minimum Cost Supplier Query (TPC-H Q2)                          24963.25             10460.09             25758.95              9824.44
Shipping Priority (TPC-H Q3)                                    69786.37             18405.81             66668.69             11038.47
Order Priority Checking Query (TPC-H Q4)                        79890.52              9662.41             78152.62             12436.11
Local Supplier Volume (TPC-H Q5)                                41142.95              4567.03             39594.81              6131.07
Forecasting Revenue Change (TPC-H Q6)                            6896.89              4090.36              6668.81              2608.60
Forecasting Revenue Change (TPC-H Q7)                            6556.63              3193.75              8955.74              2814.76
National Market Share (TPC-H Q8)                               111989.66             31936.32            160026.78             27055.97
Product Type Profit Measure (TPC-H Q9)                          23644.96             19728.72             26571.27             14346.01
Forecasting Revenue Change (TPC-H Q10)                          57943.90             30986.14             58281.73             24621.33
Important Stock Identification (TPC-H Q11)                       6186.01              1098.22              6121.36               933.75
Shipping Modes and Order Priority (TPC-H Q12)                   11159.33              1044.30             11683.17              1645.67
Customer Distribution (TPC-H Q13)                              191400.91            153886.67            204990.53             99235.57
Forecasting Revenue Change (TPC-H Q14)                           4849.71              1929.96              5293.94              1092.17
Top Supplier Query (TPC-H Q15)                                   5307.21              4391.66              6300.97              4867.53
Parts/Supplier Relationship (TPC-H Q16)                         13796.50             11741.23             15827.69             12475.68
Small-Quantity-Order Revenue (TPC-H Q17)                        44204.81             45007.60             41865.09             41020.78
Large Volume Customer (TPC-H Q18)                               57608.52            110672.15             49518.73            103647.20
Discounted Revenue (TPC-H Q19)                                  13604.58              8477.58             13426.63              4019.95
Potential Part Promotion (TPC-H Q20)                            10365.46              3516.04              8477.78              3297.92
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)             20833.77             17521.73             20971.12             17658.79
Global Sales Opportunity Query (TPC-H Q22)                       6256.54              8119.35              6710.01              6663.57

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-1-2-1           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-2-1-1           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-2-2-1           1.0         1686.0         7.0     5358.0    7061.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1          25.15
MonetDB-BHT-8-1-2-1          12.11
MonetDB-BHT-8-2-1-1          26.11
MonetDB-BHT-8-2-2-1          10.53

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           14567.42
MonetDB-BHT-8-1-2-1           31555.75
MonetDB-BHT-8-2-1-1           14021.90
MonetDB-BHT-8-2-2-1           36249.36

### Throughput@Size
                                                 time [s]  count   SF  Throughput@Size [~GB/h]
DBMS              SF  num_experiment num_client                                               
MonetDB-BHT-8-1-1 100 1              1               1330      1  100                  5954.89
MonetDB-BHT-8-1-2 100 1              2                737      1  100                 10746.27
MonetDB-BHT-8-2-1 100 2              1               1383      1  100                  5726.68
MonetDB-BHT-8-2-2 100 2              2                639      1  100                 12394.37

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1     5777.03    15.25         45.07                91.43
MonetDB-BHT-8-1-2     3707.17    12.35         36.87               140.22
MonetDB-BHT-8-2-1     9830.07    18.48         43.82                85.06
MonetDB-BHT-8-2-2     4480.58    14.62         54.91               140.84

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       23.65     0.06          0.32                 0.33
MonetDB-BHT-8-1-2       23.65     0.08          0.56                 0.58
MonetDB-BHT-8-2-1       21.65     0.01          0.55                 0.58
MonetDB-BHT-8-2-2       22.54     0.07          0.55                 0.57

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]

TEST passed: Workflow as planned
```

## Perform Benchmark - Throughput Test

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other, and then a throughput test with 5 parallel driver (`-ne 1,1,5`). and shut down the DBMS.
This is repeated 3 times (`-nc`).


```bash
mkdir -p ./logs/

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"

nohup python tpch.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 3 -ne 1,1,5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 1200 -dt \
  -rst shared -rss 300Gi \
  run &>logs_tests/test_tpch_monetdb_3.log &
```

yields something like

```
This tool helps managing running Bexhoma experiments in a Kubernetes cluster.
    

## Show Summary

### Workload
    TPC-H Queries SF=100
    Type: tpch
    Duration: 4308s 
    Code: 1728043398
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
TPC-H (SF=100) data is loaded and benchmark is executed.
Query ordering is Q1 - Q22.
All instances use the same query parameters.
Import sets indexes and constraints after loading and recomputes statistics.
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS ['MonetDB'].
Import is handled by 8 processes (pods).
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Database is persisted to disk of type shared and size 300Gi.
Loading is tested with [8] threads, split into [8] pods.
Benchmarking is tested with [1] threads, split into [1] pods.
Benchmarking is run as [1, 1, 5, 5] times the number of benchmarking pods.
Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944528
    datadisk:219980804
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980806
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980806
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980806
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-3 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980806
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-4 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980806
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-5 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980806
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980807
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980807
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-3 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980807
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-4 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980807
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-5 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248944700
    datadisk:219980807
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
                                                     MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
Pricing Summary Report (TPC-H Q1)                                False              False               True               True               True               True               True               True               True               True               True               True
Minimum Cost Supplier Query (TPC-H Q2)                           False              False              False              False              False              False              False              False              False              False              False              False
Shipping Priority (TPC-H Q3)                                     False              False              False              False              False              False              False              False              False              False              False              False
Order Priority Checking Query (TPC-H Q4)                         False              False              False              False              False              False              False              False              False              False              False              False
Local Supplier Volume (TPC-H Q5)                                 False              False              False              False              False              False              False              False              False              False              False              False
Forecasting Revenue Change (TPC-H Q6)                            False              False              False              False              False              False              False              False              False              False              False              False
Forecasting Revenue Change (TPC-H Q7)                            False              False              False              False              False              False              False              False              False              False              False              False
National Market Share (TPC-H Q8)                                 False              False              False              False              False              False              False              False              False              False              False              False
Product Type Profit Measure (TPC-H Q9)                           False              False              False              False              False              False              False              False              False              False              False              False
Forecasting Revenue Change (TPC-H Q10)                           False              False              False              False              False              False              False              False              False              False              False              False
Important Stock Identification (TPC-H Q11)                       False              False              False              False              False              False              False              False              False              False              False              False
Shipping Modes and Order Priority (TPC-H Q12)                    False              False              False              False              False              False              False              False              False              False              False              False
Customer Distribution (TPC-H Q13)                                False              False              False              False              False              False              False              False              False              False              False              False
Forecasting Revenue Change (TPC-H Q14)                           False              False              False              False              False              False              False              False              False              False              False              False
Top Supplier Query (TPC-H Q15)                                   False              False              False              False              False              False              False              False              False              False              False              False
Parts/Supplier Relationship (TPC-H Q16)                          False              False              False              False              False              False              False              False              False              False              False              False
Small-Quantity-Order Revenue (TPC-H Q17)                         False              False              False              False              False              False              False              False              False              False              False              False
Large Volume Customer (TPC-H Q18)                                False              False              False              False              False              False              False              False              False              False              False              False
Discounted Revenue (TPC-H Q19)                                   False              False              False              False              False              False              False              False              False              False              False              False
Potential Part Promotion (TPC-H Q20)                             False              False              False              False              False              False              False              False              False              False              False              False
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)              False              False              False              False              False              False              False              False              False              False              False              False
Global Sales Opportunity Query (TPC-H Q22)                       False              False              False              False              False              False              False              False              False              False              False              False

### Warnings (result mismatch)
                                                     MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
Pricing Summary Report (TPC-H Q1)                                 True               True              False              False              False              False              False              False              False              False              False              False
Minimum Cost Supplier Query (TPC-H Q2)                           False              False              False              False              False              False              False              False              False              False              False              False
Shipping Priority (TPC-H Q3)                                     False              False              False              False              False              False              False              False              False              False              False              False
Order Priority Checking Query (TPC-H Q4)                         False              False              False              False              False              False              False              False              False              False              False              False
Local Supplier Volume (TPC-H Q5)                                 False              False              False              False              False              False              False              False              False              False              False              False
Forecasting Revenue Change (TPC-H Q6)                            False              False              False              False              False              False              False              False              False              False              False              False
Forecasting Revenue Change (TPC-H Q7)                            False              False              False              False              False              False              False              False              False              False              False              False
National Market Share (TPC-H Q8)                                 False              False              False              False              False              False              False              False              False              False              False              False
Product Type Profit Measure (TPC-H Q9)                           False              False              False              False              False              False              False              False              False              False              False              False
Forecasting Revenue Change (TPC-H Q10)                           False              False              False              False              False              False              False              False              False              False              False              False
Important Stock Identification (TPC-H Q11)                       False              False              False              False              False              False              False              False              False              False              False              False
Shipping Modes and Order Priority (TPC-H Q12)                    False              False              False              False              False              False              False              False              False              False              False              False
Customer Distribution (TPC-H Q13)                                False              False              False              False              False              False              False              False              False              False              False              False
Forecasting Revenue Change (TPC-H Q14)                           False              False              False              False              False              False              False              False              False              False              False              False
Top Supplier Query (TPC-H Q15)                                   False              False              False              False              False              False              False              False              False              False              False              False
Parts/Supplier Relationship (TPC-H Q16)                          False              False              False              False              False              False              False              False              False              False              False              False
Small-Quantity-Order Revenue (TPC-H Q17)                         False              False              False              False              False              False              False              False              False              False              False              False
Large Volume Customer (TPC-H Q18)                                False              False              False              False              False              False              False              False              False              False              False              False
Discounted Revenue (TPC-H Q19)                                   False              False              False              False              False              False              False              False              False              False              False              False
Potential Part Promotion (TPC-H Q20)                             False              False              False              False              False              False              False              False              False              False              False              False
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)              False              False              False              False              False              False              False              False              False              False              False              False
Global Sales Opportunity Query (TPC-H Q22)                       False              False              False              False              False              False              False              False              False              False              False              False

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
Minimum Cost Supplier Query (TPC-H Q2)                        26330.31            2736.92            7845.04           12447.81           15020.65           11374.97           13995.93             451.42             346.38             355.35            2883.63             455.77
Shipping Priority (TPC-H Q3)                                  68570.10           24565.37           33020.89           28709.15           28736.38           29039.90           32516.44           16091.13          117598.16           10023.42          137356.29           16793.08
Order Priority Checking Query (TPC-H Q4)                      78574.44           10965.15           25279.08           30541.52           25232.81           26482.57           24159.01           23350.26           15378.67           32458.56           28090.13           30736.41
Local Supplier Volume (TPC-H Q5)                              39935.17            7530.22           13476.28           12491.82           17769.52           16125.12           15772.73           10114.82           18648.28           12898.56            6583.51           11183.91
Forecasting Revenue Change (TPC-H Q6)                          7100.06           10416.63            8144.60            8322.73            7565.14            7947.88            7579.82            4667.93            7645.19            1336.15            5384.22            3536.87
Forecasting Revenue Change (TPC-H Q7)                          9001.90            4239.51           17942.01           15646.06           16416.90           18512.88           18649.81            3462.60            5650.81            2108.28            5020.29            3357.31
National Market Share (TPC-H Q8)                             104887.38           40399.26           34485.17           35269.92           35488.24           34408.60           32234.25           48092.85           40941.42           38501.47           40741.28           40306.03
Product Type Profit Measure (TPC-H Q9)                        25392.82           16575.08           26876.99           28868.38           28052.17           27349.07           32400.61           24613.31           25145.70           25562.25           26727.00           25253.83
Forecasting Revenue Change (TPC-H Q10)                        56980.27           35781.51           37142.02           36146.77           37205.00           35977.18           32334.94           39556.93           39907.04           39238.12           39183.14           39100.42
Important Stock Identification (TPC-H Q11)                     5645.43            1662.65            2561.74            2545.56            2602.78            2555.98            2598.93            1474.86            1440.60            1465.38            1196.02            1420.78
Shipping Modes and Order Priority (TPC-H Q12)                 12264.10            4409.41            3574.75            3604.07            3928.12            3502.90            3627.44            2627.93            2585.52            2667.46            2715.02            2506.68
Customer Distribution (TPC-H Q13)                            186099.76          150547.84          171751.24          170293.07          186535.72          182242.65          183056.48          180702.90          183622.15          183465.94          195396.54          180781.99
Forecasting Revenue Change (TPC-H Q14)                         5550.61            7406.02             742.86             747.27            6511.87           10633.09           10146.20            2494.30            2562.94            1202.04             286.14            2407.05
Top Supplier Query (TPC-H Q15)                                 6389.11            7023.07            9177.84            7104.92            7483.22            6874.58            6836.87           10372.21            6777.36            9105.12            6238.49           10590.83
Parts/Supplier Relationship (TPC-H Q16)                       13486.89           13036.67           21779.33           25171.27           13246.11           13589.39           13005.16           13660.68           14487.22           14800.86           13877.18           13555.73
Small-Quantity-Order Revenue (TPC-H Q17)                      44792.56           45711.34          139542.99          140349.18          129496.78          129484.35          130446.17            5993.30            5590.11            5319.92            4563.41            5278.95
Large Volume Customer (TPC-H Q18)                             49541.46           98669.23          111567.67          107561.88          108138.11          108765.34          107753.06           80701.62           80832.04           79291.57           73237.23           82186.96
Discounted Revenue (TPC-H Q19)                                14467.32            8406.96            4623.25            7860.13            8123.34            7443.62            8440.49            2622.69            2517.68            2944.98            2999.02            1875.47
Potential Part Promotion (TPC-H Q20)                          10716.70           10162.35           10060.29           10266.92           10627.83           10532.64           10302.06            5069.94            5582.50            5454.77            5744.07            5233.06
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           22017.28           18170.92           57189.36           75633.73           66516.55           78756.06           74659.60           36819.92           64551.47           60046.63           64894.50           58423.16
Global Sales Opportunity Query (TPC-H Q22)                     6912.36            9194.14            6364.61            7022.92            6559.37            6518.21            7035.13            6346.63            7146.63            6926.20            7217.71            6602.96

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-2-1           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-3-1           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-3-2           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-3-3           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-3-4           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-3-5           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-4-1           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-4-2           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-4-3           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-4-4           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-4-5           1.0         1686.0         7.0     5358.0    7061.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          22.62
MonetDB-BHT-8-2-1          13.63
MonetDB-BHT-8-3-1          16.85
MonetDB-BHT-8-3-2          17.82
MonetDB-BHT-8-3-3          19.46
MonetDB-BHT-8-3-4          19.63
MonetDB-BHT-8-3-5          19.83
MonetDB-BHT-8-4-1          10.20
MonetDB-BHT-8-4-2          11.82
MonetDB-BHT-8-4-3           9.16
MonetDB-BHT-8-4-4          11.24
MonetDB-BHT-8-4-5          10.21

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           16260.10
MonetDB-BHT-8-2-1           27513.77
MonetDB-BHT-8-3-1           22132.78
MonetDB-BHT-8-3-2           20930.72
MonetDB-BHT-8-3-3           19139.11
MonetDB-BHT-8-3-4           19038.74
MonetDB-BHT-8-3-5           18815.06
MonetDB-BHT-8-4-1           37269.35
MonetDB-BHT-8-4-2           32193.12
MonetDB-BHT-8-4-3           41400.78
MonetDB-BHT-8-4-4           33878.50
MonetDB-BHT-8-4-5           37377.79

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               1343      1  100                  5897.24
MonetDB-BHT-8-2 100 1              2                773      1  100                 10245.80
MonetDB-BHT-8-3 100 1              3                958      5  100                 41336.12
MonetDB-BHT-8-4 100 1              4                805      5  100                 49192.55

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 5, 5]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 5, 5]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     6604.14    26.81         58.07                94.60
MonetDB-BHT-8-2     4086.38    16.07         56.27               128.37
MonetDB-BHT-8-3    13175.53    24.50        116.25               195.32
MonetDB-BHT-8-4    10474.56    46.86        165.21               248.16

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       23.79     0.05          0.33                 0.34
MonetDB-BHT-8-2       23.79     0.04          0.56                 0.59
MonetDB-BHT-8-3       93.72     0.06          1.62                 1.68
MonetDB-BHT-8-4      113.63     0.35          2.74                 2.81

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]

TEST passed: Workflow as planned
```