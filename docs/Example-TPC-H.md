# Example: TPC-H

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

This example shows how to benchmark 22 reading queries Q1-Q22 derived from TPC-H in MonetDB and PostgreSQL.

> The query file is derived from the TPC-H and as such is not comparable to published TPC-H results, as the query file results do not comply with the TPC-H Specification.

Official TPC-H benchmark - http://www.tpc.org/tpch

## Perform Benchmark - Power Test

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example: `python tpch.py -dt -nlp 8 -nlt 16 -sf 1 -ii -ic -is run`

This
* starts a clean instance of PostgreSQL, MonetDB, MySQL
  * data directory inside a Docker container
* creates TPC-H schema in each database
* starts 8 loader pods per DBMS
  * with a data generator (init) container each
    * each generating a portion of TPC-H data of scaling factor 1
    * storing the data in a distributed filesystem (shared disk)
    * if data is already present: do nothing
  * with a loading container each
    * importing TPC-H data from the distributed filesystem
    * MySQL: only one pod active and it loads with 16 threads
* creates contraints and indexes and updates table statistics in each DBMS after ingestion
* runs 1 stream of TPC-H queries per DBMS
  * all DBMS use the same parameters
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```
+------------------+--------------+--------------+---------------+
| 1706255897       | sut          |   loaded [s] | loading       |
+==================+==============+==============+===============+
| MonetDB-BHT-8    | (1. Running) |       253.23 |               |
+------------------+--------------+--------------+---------------+
| MySQL-BHT-8-8    | (1. Running) |         0.61 | (8 Succeeded) |
+------------------+--------------+--------------+---------------+
| PostgreSQL-BHT-8 | (1. Running) |       219.08 |               |
+------------------+--------------+--------------+---------------+
```


## Evaluate Results

At the end of a benchmark you will see a summary like

```
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
Q1              1214.78           31836.03               2818.04
Q2                32.96             354.24                448.22
Q3               152.26            3773.37                772.58
Q4                56.77            1925.58               1320.62
Q5                96.40            2700.64                694.82
Q6                43.42            4317.21                522.64
Q7                95.72            7200.93                807.61
Q8               453.65            6742.41                646.12
Q9               138.02            5596.61               1567.34
Q10              186.51            3093.87               1327.04
Q11               28.54             338.07                253.88
Q12               71.91            7169.19               1030.47
Q13              611.46            9030.91               2092.40
Q14               50.75            5017.37                560.41
Q15               51.14           22967.24                560.97
Q16              112.46            1106.00                596.19
Q17              135.30             787.69               2087.18
Q18              235.09            6354.27               8261.32
Q19               82.74             384.85                716.25
Q20              106.50             578.54                727.58
Q21             1970.25           17064.63                908.25
Q22               60.29             529.73                249.55

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1              0.0           20.0       30.47      30.42    120.89
MySQL-BHT-8-8-1-1              3.0            1.0        7.04    1743.71   1761.74
PostgreSQL-BHT-8-1-1           1.0           73.0        1.53      93.26    179.79

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS
MonetDB-BHT-8-1-1              0.15
MySQL-BHT-8-8-1-1              3.09
PostgreSQL-BHT-8-1-1           0.96

### TPC-H Power@Size
                      TPC-H Power@Size [~Q/h]
DBMS
MonetDB-BHT-8-1-1                    28311.40
MySQL-BHT-8-8-1-1                     1218.11
PostgreSQL-BHT-8-1-1                  3986.41

### TPC-H Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
orig_name          SF num_experiment num_client
MonetDB-BHT-8-1    1  1              1                 18      1   1                  4400.00
MySQL-BHT-8-8-1    1  1              1                156      1   1                   507.69
PostgreSQL-BHT-8-1 1  1              1                 46      1   1                  1721.74
```
This gives a survey about the errors and warnings (result set mismatch), the geometric mean (in seconds) and the loading times (schema creation, ingestion and indexing) and the latencies of execution per query.

Results are transformed into pandas DataFrames and can be inspected in more detail.
Detailed evaluations can be done using DBMSBenchmarker
* [Dashboard](https://dbmsbenchmarker.readthedocs.io/en/latest/Dashboard.html)
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server in the cluster by `bexperiments dashboard`.
This forwards ports, so you have
* a DBMSBenchmarker dashboard in browser at http://localhost:8050
* a Jupyter notebook server at http://localhost:8888 containing the example notebooks

You can connect to a local evaluation server by `bexperiments localdashboard`.
This forwards ports, so you have
* a DBMSBenchmarker dashboard in browser at http://localhost:8050

You can connect to a local jupyter server by `bexperiments jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888 containing the example notebooks


## Adjust Parameters

The script supports
* exact repetitions for statistical confidence
* variations to scan a large parameters space
* combine results for easy evaluation

There are various ways to change parameters.

### Manifests

The YAML manifests for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch

### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/tpch

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python tpch.py -h`

```
usage: tpch.py [-h] [-aws] [-dbms {PostgreSQL,MonetDB,MySQL}] [-lit LIMIT_IMPORT_TABLE] [-db] [-cx CONTEXT] [-e EXPERIMENT] [-d] [-m] [-mc] [-ms MAX_SUT] [-dt] [-md MONITORING_DELAY] [-nr NUM_RUN] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS]
               [-nls NUM_LOADING_SPLIT] [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS] [-sf SCALING_FACTOR] [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME]
               [-tr] [-ii] [-ic] [-is] [-rcp RECREATE_PARAMETER]
               {profiling,run,start,load,empty}

Performs a TPC-H loading experiment. Data is generated and imported into a DBMS from a distributed filesystem.

positional arguments:
  {profiling,run,start,load,empty}
                        profile the import or run the TPC-H queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms {PostgreSQL,MonetDB,SingleStore,CockroachDB,MySQL,MariaDB,YugabyteDB,Kinetica}
                        DBMS to load the data
  -lit LIMIT_IMPORT_TABLE, --limit-import-table LIMIT_IMPORT_TABLE
                        limit import to one table, name of this table
  -db, --debug          dump debug informations
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
  -e EXPERIMENT, --experiment EXPERIMENT
                        sets experiment code for continuing started experiment
  -d, --detached        puts most of the experiment workflow inside the cluster
  -m, --monitoring      activates monitoring
  -mc, --monitoring-cluster
                        activates monitoring for all nodes of cluster
  -ms MAX_SUT, --max-sut MAX_SUT
                        maximum number of parallel DBMS configurations, default is no limit
  -dt, --datatransfer   activates datatransfer
  -md MONITORING_DELAY, --monitoring-delay MONITORING_DELAY
                        time to wait [s] before execution of the runs of a query
  -nr NUM_RUN, --num-run NUM_RUN
                        number of runs per query
  -nc NUM_CONFIG, --num-config NUM_CONFIG
                        number of runs per configuration
  -ne NUM_QUERY_EXECUTORS, --num-query-executors NUM_QUERY_EXECUTORS
                        comma separated list of number of parallel clients
  -nls NUM_LOADING_SPLIT, --num-loading-split NUM_LOADING_SPLIT
                        portion of loaders that should run in parallel
  -nlp NUM_LOADING_PODS, --num-loading-pods NUM_LOADING_PODS
                        total number of loaders per configuration
  -nlt NUM_LOADING_THREADS, --num-loading-threads NUM_LOADING_THREADS
                        total number of threads per loading process
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF)
  -t TIMEOUT, --timeout TIMEOUT
                        timeout for a run of a query
  -rr REQUEST_RAM, --request-ram REQUEST_RAM
                        request ram
  -rc REQUEST_CPU, --request-cpu REQUEST_CPU
                        request cpus
  -rct REQUEST_CPU_TYPE, --request-cpu-type REQUEST_CPU_TYPE
                        request node having node label cpu=
  -rg REQUEST_GPU, --request-gpu REQUEST_GPU
                        request number of gpus
  -rgt REQUEST_GPU_TYPE, --request-gpu-type REQUEST_GPU_TYPE
                        request node having node label gpu=
  -rst {None,,local-hdd,shared}, --request-storage-type {None,,local-hdd,shared}
                        request persistent storage of certain type
  -rss REQUEST_STORAGE_SIZE, --request-storage-size REQUEST_STORAGE_SIZE
                        request persistent storage of certain size
  -rnn REQUEST_NODE_NAME, --request-node-name REQUEST_NODE_NAME
                        request a specific node
  -tr, --test-result    test if result fulfills some basic requirements
  -ii, --init-indexes   adds indexes to tables after ingestion
  -ic, --init-constraints
                        adds constraints to tables after ingestion
  -is, --init-statistics
                        recomputes statistics of tables after ingestion
  -rcp RECREATE_PARAMETER, --recreate-parameter RECREATE_PARAMETER
                        recreate parameter for randomized queries
```

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

If monitoring is activated, the summary also contains a section like
```
### CPU of Ingestion (via counter) [CPUs]
                              0
DBMS
MonetDB-BHT-8-1      136.638103
MySQL-BHT-8-8-1     3223.236893
PostgreSQL-BHT-8-1   153.782876
### Max RAM of Ingestion [Mb]
                               0
DBMS
MonetDB-BHT-8-1      1244.855469
MySQL-BHT-8-8-1     48206.949219
PostgreSQL-BHT-8-1   3862.175781
### CPU of Execution (via counter) [CPUs]
                             0
DBMS
MonetDB-BHT-8-1      29.866166
MySQL-BHT-8-8-1     142.083743
PostgreSQL-BHT-8-1  115.545106
### Max RAM of Execution [Mb]
                               0
DBMS
MonetDB-BHT-8-1      1787.203125
MySQL-BHT-8-8-1     48321.277344
PostgreSQL-BHT-8-1   3939.746094
```

This gives a survey about CPU (in CPU seconds) and RAM usage (in Mb) during loading and execution of the benchmark.

## Perform Benchmark - Throughput Test

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example: `python tpch.py -dt -nlp 8 -ii -ic -is -ne 1,2 -dbms PostgreSQL -t 1200 run`

This runs 3 streams, the first one as a single stream and the following 2 in parallel.

```
### TPC-H Power@Size
                            Power@Size [~Q/h]
DBMS
PostgreSQL-BHT-8-1-1                  4150.78
PostgreSQL-BHT-8-2-1                  3756.33
PostgreSQL-BHT-8-2-2                  4190.57

### TPC-H Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
orig_name          SF num_experiment num_client
PostgreSQL-BHT-8-1 1  1              1                 45      1   1                  1760.00
PostgreSQL-BHT-8-2 1  1              2                 49      2   1                  3232.65

```
