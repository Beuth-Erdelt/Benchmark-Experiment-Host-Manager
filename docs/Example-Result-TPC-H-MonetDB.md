## Example: TPC-H SF=100 MonetDB

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

This example shows how to run Q1-Q22 derived from TPC-H in MonetDB at SF=100.
It covers the power and the throughput test.
The refresh stream is not included.

> The query file is derived from the TPC-H and as such is not comparable to published TPC-H results, as the query file results do not comply with the TPC-H Specification.

Official TPC-H benchmark - http://www.tpc.org/tpch

**The results are not official benchmark results. The exact performance depends on a collection of parameters.
The purpose of this example is to illustrate the usage of bexhoma and to show how to evaluate results.**



### Generate and Load Data

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
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR

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
  run &>$LOG_DIR/doc_tpch_monetdb_1.log &
```

### Status Data Disk

You can watch the status of the data disk via `bexperiments data`.

In the following example output we see we have generated TPC-H at SF=100 using 8 generators.
The data set is split into 8 parts, each of about 14G size.
In total the data set has a size of 106G.

```bash
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

You can watch the status of experiments via `bexperiments status`.

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

```bash
## Show Summary

### Workload
TPC-H Queries SF=100
    Type: tpch
    Duration: 1847s 
    Code: 1728337600
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
    disk:248971704
    datadisk:219980828
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
Pricing Summary Report (TPC-H Q1)                            637721.03
Minimum Cost Supplier Query (TPC-H Q2)                        28708.97
Shipping Priority (TPC-H Q3)                                  79925.53
Order Priority Checking Query (TPC-H Q4)                      89958.19
Local Supplier Volume (TPC-H Q5)                              47184.89
Forecasting Revenue Change (TPC-H Q6)                          8206.29
Forecasting Revenue Change (TPC-H Q7)                         10794.91
National Market Share (TPC-H Q8)                             134400.81
Product Type Profit Measure (TPC-H Q9)                        34328.54
Forecasting Revenue Change (TPC-H Q10)                        63909.34
Important Stock Identification (TPC-H Q11)                     6428.52
Shipping Modes and Order Priority (TPC-H Q12)                 13313.75
Customer Distribution (TPC-H Q13)                            230882.81
Forecasting Revenue Change (TPC-H Q14)                         7139.99
Top Supplier Query (TPC-H Q15)                                10173.02
Parts/Supplier Relationship (TPC-H Q16)                       13641.87
Small-Quantity-Order Revenue (TPC-H Q17)                      42008.34
Large Volume Customer (TPC-H Q18)                             52259.31
Discounted Revenue (TPC-H Q19)                                14101.50
Potential Part Promotion (TPC-H Q20)                          11211.91
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           23796.97
Global Sales Opportunity Query (TPC-H Q22)                     6541.88

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0         1686.0         7.0     5358.0    7061.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          29.77

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           12333.63

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               1587      1  100                  4990.55

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     6613.58    23.16         46.78                85.29

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       22.14     0.02          0.33                 0.35

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

To see the summary again you can simply call `bexperiments summary -e 1708411664` with the experiment code.

### List local results

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
This is repeated 2 times (`-nc`).


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
  -nc 2 -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 1200 -dt \
  -rst shared -rss 300Gi \
  run &>$LOG_DIR/doc_tpch_monetdb_2.log &
```

yields

```bash
## Show Summary

### Workload
TPC-H Queries SF=100
    Type: tpch
    Duration: 4970s 
    Code: 1728339400
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
    Error: /home/perdelt/benchmarks/1728339400/bexhoma-benchmarker-monetdb-bht-8-1728339400-2-1-4q4t2.dbmsbenchmarker.log
        Temporary failure in name resolution

### Connections
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248971704
    datadisk:219980831
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
    disk:248971704
    datadisk:219980832
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
    disk:248971876
    datadisk:219980833
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
    disk:248971876
    datadisk:219980835
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
Pricing Summary Report (TPC-H Q1)                              518997.54            269815.24            531346.50            268930.95
Minimum Cost Supplier Query (TPC-H Q2)                          31899.42              5479.74             27818.68              4667.95
Shipping Priority (TPC-H Q3)                                    67110.07             22691.58             76128.46             19727.98
Order Priority Checking Query (TPC-H Q4)                        82799.30             10884.20             80725.38             13526.61
Local Supplier Volume (TPC-H Q5)                                42544.52              9453.73             48427.15              6903.62
Forecasting Revenue Change (TPC-H Q6)                            7406.74              5135.68              8458.45              2875.59
Forecasting Revenue Change (TPC-H Q7)                           10283.94              2999.89              8843.63              3188.79
National Market Share (TPC-H Q8)                               108473.82             47368.16            110799.09             28236.21
Product Type Profit Measure (TPC-H Q9)                          29168.84             24010.44             26821.05             18039.85
Forecasting Revenue Change (TPC-H Q10)                          86968.62             37707.34             64489.10             22146.30
Important Stock Identification (TPC-H Q11)                       6596.34              1546.81              5740.24               909.96
Shipping Modes and Order Priority (TPC-H Q12)                   12368.89              3291.52             13338.83              3901.12
Customer Distribution (TPC-H Q13)                              200641.69            157422.89            191430.59             93153.02
Forecasting Revenue Change (TPC-H Q14)                           7110.60             10879.84              6336.09              4634.55
Top Supplier Query (TPC-H Q15)                                   9954.75              6444.40              7196.80              5952.67
Parts/Supplier Relationship (TPC-H Q16)                         12595.28             12214.79             12492.90             12085.18
Small-Quantity-Order Revenue (TPC-H Q17)                        45575.76             97067.84             43363.49             15070.59
Large Volume Customer (TPC-H Q18)                              135744.59             54394.66             65622.97             17328.43
Discounted Revenue (TPC-H Q19)                                  12840.11              9649.97             13883.32              3452.47
Potential Part Promotion (TPC-H Q20)                            14185.28              8127.94             13833.44              3750.31
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)             23819.84             18137.41             23231.11             13798.45
Global Sales Opportunity Query (TPC-H Q22)                       8341.52              7321.66              7165.24              8220.74

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-1-2-1           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-2-1-1           1.0         1686.0         7.0     5358.0    7061.0
MonetDB-BHT-8-2-2-1           1.0         1686.0         7.0     5358.0    7061.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1          30.33
MonetDB-BHT-8-1-2-1          15.79
MonetDB-BHT-8-2-1-1          28.11
MonetDB-BHT-8-2-2-1          10.65

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           12086.24
MonetDB-BHT-8-1-2-1           23847.22
MonetDB-BHT-8-2-1-1           13070.31
MonetDB-BHT-8-2-2-1           35981.10

### Throughput@Size
                                                 time [s]  count   SF  Throughput@Size [~GB/h]
DBMS              SF  num_experiment num_client                                               
MonetDB-BHT-8-1-1 100 1              1               1492      1  100                  5308.31
MonetDB-BHT-8-1-2 100 1              2                834      1  100                  9496.40
MonetDB-BHT-8-2-1 100 2              1               1404      1  100                  5641.03
MonetDB-BHT-8-2-2 100 2              2                582      1  100                 13608.25

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1     6797.58     7.45         45.07                85.26
MonetDB-BHT-8-1-2     4426.81     5.26         45.31               111.35
MonetDB-BHT-8-2-1    11231.82    19.60         43.35                85.32
MonetDB-BHT-8-2-2     3777.18    19.01         65.94               132.02

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       22.25     0.00          0.32                 0.34
MonetDB-BHT-8-1-2       22.25     0.09          0.55                 0.58
MonetDB-BHT-8-2-1       21.36     0.01          0.56                 0.58
MonetDB-BHT-8-2-2       22.97     0.06          0.57                 0.59

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
We then run two power tests, one after the other, and then a throughput test with 3 parallel driver (`-ne 1,1,3`). and shut down the DBMS.


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
  -nc 1 -ne 1,1,3 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 1200 -dt \
  -rst shared -rss 300Gi \
  run &>$LOG_DIR/doc_tpch_monetdb_3.log &
```

yields something like

```bash
## Show Summary

### Workload
TPC-H Queries SF=100
    Type: tpch
    Duration: 4645s 
    Code: 1728344200
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
    disk:248971876
    datadisk:219980836
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
    disk:248972044
    datadisk:219980838
    volume_size:300G
    volume_used:215G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248972044
    datadisk:219980838
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
    disk:248972044
    datadisk:219980838
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
    disk:248972044
    datadisk:219980838
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
    disk:248972044
    datadisk:219980838
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
    disk:248972044
    datadisk:219980838
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
    disk:248972044
    datadisk:219980838
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
    disk:248972044
    datadisk:219980838
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
    disk:248972044
    datadisk:219980838
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
    disk:248972044
    datadisk:219980838
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
    disk:248972044
    datadisk:219980838
    volume_size:300G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
                                   MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
Pricing Summary Report (TPC-H Q1)              False              False               True               True               True               True               True               True               True               True               True               True

### Warnings (result mismatch)
                                   MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
Pricing Summary Report (TPC-H Q1)               True               True              False              False              False              False              False              False              False              False              False              False

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
Minimum Cost Supplier Query (TPC-H Q2)                        30134.53           10578.11            5406.28            9980.43            3024.22            5176.07            2387.48            1789.32            9753.37            5705.30            9773.69           14574.39
Shipping Priority (TPC-H Q3)                                  67580.79           25698.05           46557.76           46370.75           49320.23           45416.18           45362.25           31233.79           30454.08           31259.65           30424.76           30375.93
Order Priority Checking Query (TPC-H Q4)                      91698.77           11893.55           35243.21           37739.37           37166.46           35694.38           38938.11           32907.28           32831.89           32644.26           27588.78           26600.38
Local Supplier Volume (TPC-H Q5)                              42356.45           23405.85           14273.01           12873.63           13771.20           10616.57           11414.28           13238.20            9538.38           11148.49            5713.39            5638.79
Forecasting Revenue Change (TPC-H Q6)                          6979.38            6474.77            7586.69            7219.52            1829.02            7133.17            7141.75            2513.76            1717.17            2157.18            7481.86            5105.98
Forecasting Revenue Change (TPC-H Q7)                          9479.14            4503.75           18936.04           16985.05           16079.15           16980.63           16875.12            2263.86            4210.82            4401.09            4585.22            6545.56
National Market Share (TPC-H Q8)                             124919.09           34815.08           29919.00           32683.54           33520.40           32824.93           32900.74           40744.31           44206.54           40028.67           45615.31           47838.36
Product Type Profit Measure (TPC-H Q9)                        27010.95           23491.12           26305.48           25381.16           24672.72           25276.88           25456.31           27874.10           30573.95           29781.77           29998.40           29597.50
Forecasting Revenue Change (TPC-H Q10)                        60492.50           25012.33           28753.05           29622.54           29660.99           30868.37           29417.25           30926.03           28312.16           30698.97           31125.68           30359.82
Important Stock Identification (TPC-H Q11)                     6028.91             932.46             825.79            1542.43            1277.07             876.36            1428.17            1945.76            1889.13            1931.84            1889.87            2000.42
Shipping Modes and Order Priority (TPC-H Q12)                 11307.35            2621.41            1710.38            2642.94            2779.78            1900.93            2869.94            2768.84            2998.39            2926.45            2800.23            2937.98
Customer Distribution (TPC-H Q13)                            190325.50          164930.66          217161.82          219644.59          226365.24          216754.40          219993.72          175236.69          175350.19          170707.75          171198.96          176848.87
Forecasting Revenue Change (TPC-H Q14)                         6670.95            8470.47            2604.21            1165.48             398.69            4036.26             853.85            1918.02            1917.13            4498.26            3462.18            2757.50
Top Supplier Query (TPC-H Q15)                                 7022.88            5735.63            7535.92            7523.65            6498.42            7176.53            8095.93            6691.07            6512.70            9886.72            8565.03            4511.89
Parts/Supplier Relationship (TPC-H Q16)                       12243.55           11797.44           12762.30           13071.74           13634.23           12866.09           13353.63           12712.35           13538.40           12986.89           12985.24           13513.09
Small-Quantity-Order Revenue (TPC-H Q17)                      41977.41           41483.16            4278.41            4680.46            4971.06            4236.86            4239.49           45401.00           44979.19           45713.73           46033.48           45350.79
Large Volume Customer (TPC-H Q18)                             52901.09           44818.46          112074.52          106100.02           98727.90          107275.32          106414.13           64158.52           66448.34           62007.52           63891.98           62786.14
Discounted Revenue (TPC-H Q19)                                13743.43           10395.17             720.51            2866.02            3010.24            2523.00            1619.37            2335.04            2288.03            3207.95            2406.02            2854.43
Potential Part Promotion (TPC-H Q20)                           8836.95            4337.89            6712.65            9215.44           14041.39           10318.73           10045.61           11168.04            8656.02           10799.23           10885.09           10903.41
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           22315.80           16588.82           63111.82           44683.70           74631.96           77369.56           73525.68           72813.04           60925.79           65623.86           73062.02           65005.98
Global Sales Opportunity Query (TPC-H Q22)                     6544.40            6281.95            9689.27            6456.37            7455.69            7572.83            7730.87            6762.60            6646.59            6835.29            6809.59            6880.30

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
MonetDB-BHT-8-1-1          23.21
MonetDB-BHT-8-2-1          13.26
MonetDB-BHT-8-3-1          12.86
MonetDB-BHT-8-3-2          13.71
MonetDB-BHT-8-3-3          12.14
MonetDB-BHT-8-3-4          14.01
MonetDB-BHT-8-3-5          12.67
MonetDB-BHT-8-4-1          12.25
MonetDB-BHT-8-4-2          13.01
MonetDB-BHT-8-4-3          14.09
MonetDB-BHT-8-4-4          14.47
MonetDB-BHT-8-4-5          14.22

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           15825.76
MonetDB-BHT-8-2-1           29039.24
MonetDB-BHT-8-3-1           30036.50
MonetDB-BHT-8-3-2           27609.43
MonetDB-BHT-8-3-3           31367.14
MonetDB-BHT-8-3-4           27636.09
MonetDB-BHT-8-3-5           29891.91
MonetDB-BHT-8-4-1           30715.98
MonetDB-BHT-8-4-2           28862.71
MonetDB-BHT-8-4-3           26648.35
MonetDB-BHT-8-4-4           26017.64
MonetDB-BHT-8-4-5           26424.98

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               1434      1  100                  5523.01
MonetDB-BHT-8-2 100 1              2                751      1  100                 10545.94
MonetDB-BHT-8-3 100 1              3                959      5  100                 41293.01
MonetDB-BHT-8-4 100 1              4                874      5  100                 45308.92

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 5, 5]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 5, 5]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     6761.29    19.67         49.45                86.90
MonetDB-BHT-8-2     3853.12    17.47         47.60               129.55
MonetDB-BHT-8-3    12567.38    46.21        133.36               218.49
MonetDB-BHT-8-4    12560.43    40.15        173.50               252.36

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       21.89     0.01          0.33                 0.35
MonetDB-BHT-8-2       21.89     0.09          0.55                 0.59
MonetDB-BHT-8-3       89.56     0.19          1.64                 1.71
MonetDB-BHT-8-4      109.02     0.18          2.76                 2.84

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.

