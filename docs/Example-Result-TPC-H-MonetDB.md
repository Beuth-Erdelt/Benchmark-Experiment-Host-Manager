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
mkdir -p ./logs/

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
  run &>logs/test_tpch_monetdb_1.log &
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

```bash
## Show Summary
Read results
Connections:
MonetDB-BHT-8-1-1
MySQL-BHT-8-8-1-1
PostgreSQL-BHT-8-1-1
Queries:
0: Q1 = Pricing Summary Report (TPC-H Q1)
1: Q2 = Minimum Cost Supplier Query (TPC-H Q2)
2: Q3 = Shipping Priority (TPC-H Q3)
3: Q4 = Order Priority Checking Query (TPC-H Q4)
4: Q5 = Local Supplier Volume (TPC-H Q5)
5: Q6 = Forecasting Revenue Change (TPC-H Q6)
6: Q7 = Forecasting Revenue Change (TPC-H Q7)
7: Q8 = National Market Share (TPC-H Q8)
8: Q9 = Product Type Profit Measure (TPC-H Q9)
9: Q10 = Forecasting Revenue Change (TPC-H Q10)
10: Q11 = Important Stock Identification (TPC-H Q11)
11: Q12 = Shipping Modes and Order Priority (TPC-H Q12)
12: Q13 = Customer Distribution (TPC-H Q13)
13: Q14 = Forecasting Revenue Change (TPC-H Q14)
14: Q15 = Top Supplier Query (TPC-H Q15)
15: Q16 = Parts/Supplier Relationship (TPC-H Q16)
16: Q17 = Small-Quantity-Order Revenue (TPC-H Q17)
17: Q18 = Large Volume Customer (TPC-H Q18)
18: Q19 = Discounted Revenue (TPC-H Q19)
19: Q20 = Potential Part Promotion (TPC-H Q20)
20: Q21 = Suppliers Who Kept Orders Waiting Query (TPC-H Q21)
21: Q22 = Global Sales Opportunity Query (TPC-H Q22)
Load Evaluation

### Errors
     MonetDB-BHT-8-1-1  MySQL-BHT-8-8-1-1  PostgreSQL-BHT-8-1-1
Q1               False              False                 False
Q2               False              False                 False
Q3               False              False                 False
Q4               False              False                 False
Q5               False              False                 False
Q6               False              False                 False
Q7               False              False                 False
Q8               False              False                 False
Q9               False              False                 False
Q10              False              False                 False
Q11              False              False                 False
Q12              False              False                 False
Q13              False              False                 False
Q14              False              False                 False
Q15              False              False                 False
Q16              False              False                 False
Q17              False              False                 False
Q18              False              False                 False
Q19              False              False                 False
Q20              False              False                 False
Q21              False              False                 False
Q22              False              False                 False

### Warnings
     MonetDB-BHT-8-1-1  MySQL-BHT-8-8-1-1  PostgreSQL-BHT-8-1-1
Q1               False              False                 False
Q2               False              False                 False
Q3               False              False                 False
Q4               False              False                 False
Q5               False              False                 False
Q6               False              False                 False
Q7               False              False                 False
Q8               False              False                 False
Q9               False              False                 False
Q10              False              False                 False
Q11              False              False                 False
Q12              False              False                 False
Q13              False              False                 False
Q14              False              False                 False
Q15              False              False                 False
Q16              False              False                 False
Q17              False              False                 False
Q18              False              False                 False
Q19              False              False                 False
Q20              False              False                 False
Q21              False              False                 False
Q22              False              False                 False

### Latency of Timer Execution [ms]
DBMS  MonetDB-BHT-8-1-1  MySQL-BHT-8-8-1-1  PostgreSQL-BHT-8-1-1
Q1              2404.64           33934.30               2612.67
Q2                30.12             361.71                441.01
Q3               151.54            3897.70                794.99
Q4                52.34            1882.83               1311.89
Q5                73.99            3639.32                698.28
Q6                33.68            4465.72                539.06
Q7                95.63            7349.12                810.43
Q8               449.77            6828.98                656.06
Q9               111.96            5704.00               1145.25
Q10              175.70            3128.08               1321.12
Q11               31.90             363.01                258.32
Q12               67.53            7294.59               1069.99
Q13              555.90            8787.78               2008.54
Q14               41.45            5265.07                596.09
Q15               60.05           22688.57                583.01
Q16              116.17            1057.91                591.68
Q17               72.47             799.00               2024.25
Q18              964.94            6488.35               7099.96
Q19               91.28             387.99               1595.01
Q20               97.20             586.58                668.23
Q21             3185.97           16793.11                932.27
Q22               67.00             512.73                253.11

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1              1.0           22.0        8.80      34.36    102.16
MySQL-BHT-8-8-1-1              1.0          435.0        3.78    1793.84   2262.63
PostgreSQL-BHT-8-1-1           1.0           25.0        0.61      88.96    139.58

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS
MonetDB-BHT-8-1-1              0.16
MySQL-BHT-8-8-1-1              3.11
PostgreSQL-BHT-8-1-1           0.95

### TPC-H Power@Size
                      Power@Size [~Q/h]
DBMS
MonetDB-BHT-8-1-1              27011.62
MySQL-BHT-8-8-1-1               1187.97
PostgreSQL-BHT-8-1-1            3924.04

### TPC-H Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client
MonetDB-BHT-8-1    1  1              1                 13      1   1                  6092.31
MySQL-BHT-8-8-1    1  1              1                147      1   1                   538.78
PostgreSQL-BHT-8-1 1  1              1                 33      1   1                  2400.00

### Ingestion
                    SUT - CPU of Ingestion (via counter) [CPUs]  SUT - Max RAM of Ingestion [Gb]
DBMS
MonetDB-BHT-8-1                                          139.25                             1.23
MySQL-BHT-8-8-1                                         3015.80                            47.16
PostgreSQL-BHT-8-1                                       150.89                             3.74

### Execution
                    SUT - CPU of Execution (via counter) [CPUs]  SUT - Max RAM of Execution [Gb]
DBMS
MonetDB-BHT-8-1                                           17.13                             1.57
MySQL-BHT-8-8-1                                          130.73                            47.31
PostgreSQL-BHT-8-1                                        63.62                             3.78
```


### Status Data Disk

To see the summary of experiment `1708411664` again you can simply call `python tpch.py -e 1708411664 summary`.

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
This is repeated 5 times (`-nc`).


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
  -nc 5 -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 1200 -dt \
  -rst shared -rss 300Gi \
  run &>logs/test_tpch_monetdb_2.log &
```

## Perform Benchmark - Throughput Test

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other, and then a throughput test with 5 parallel driver (`-ne 1,1,5`). and shut down the DBMS.
This is repeated 5 times (`-nc`).


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
  -nc 5 -ne 1,1,5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 1200 -dt \
  -rst shared -rss 300Gi \
  run &>logs/test_tpch_monetdb_2.log &
```

