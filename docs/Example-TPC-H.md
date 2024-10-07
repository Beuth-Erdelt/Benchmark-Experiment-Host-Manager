# Example: TPC-H

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TPC-H does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients for the loading test and the throughput test [2].

This example shows how to benchmark 22 reading queries Q1-Q22 derived from TPC-H in MonetDB and PostgreSQL.

> The query file is derived from the TPC-H and as such is not comparable to published TPC-H results, as the query file results do not comply with the TPC-H Specification.

1. Official TPC-H benchmark - http://www.tpc.org/tpch
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Perform Benchmark - Power Test

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
```

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example:
```bash
nohup python tpch.py -ms 1 -dt -tr \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_compare.log &
```

This
* starts a clean instance of PostgreSQL, MonetDB, MySQL and MariaDB
  * data directory inside a Docker container
  * with a maximum of 1 DBMS per time (`-ms`)
* creates TPC-H schema in each database
* starts 8 loader pods per DBMS (`-nlp`)
  * with a data generator (init) container each
    * each generating a portion of TPC-H data of scaling factor 1 (`-sf`)
    * storing the data in a distributed filesystem (shared disk)
    * if data is already present: do nothing
  * with a loading container each
    * importing TPC-H data from the distributed filesystem
    * MySQL: only one pod active and it loads with 8 threads (`-nlt`)
* creates contraints (`-ic`) and indexes (`-ii`) and updates table statistics (`-is`) in each DBMS after ingestion
* runs 1 stream of TPC-H queries per DBMS
  * all DBMS use the same parameters
  * data transfer is also measured (`-dt`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```bash
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
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

The code `1706255897` is the unique identifier of the experiment.
You can find the number also in the output of `tpch.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1706255897` (removes everything that is related to experiment `1706255897`).

## Evaluate Results

At the end of a benchmark you will see a summary like

```bash
## Show Summary

### Workload
    TPC-H Queries SF=1
    Type: tpch
    Duration: 4682s 
    Code: 1728069223
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
TPC-H (SF=1) data is loaded and benchmark is executed.
Query ordering is Q1 - Q22.
All instances use the same query parameters.
Import sets indexes and constraints after loading and recomputes statistics.
Import is handled by 8 processes (pods).
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Loading is tested with [8] threads, split into [8] pods.
Benchmarking is tested with [1] threads, split into [1] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
MariaDB-BHT-8-1-1 uses docker image mariadb:11.4.2
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251086408
    datadisk:2140488
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251786944
    datadisk:2841020
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-8-8-1-1 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:259487904
    datadisk:10541792
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251768784
    datadisk:2823016
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
                                                     MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-8-8-1-1  PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                False              False              False                 False
Minimum Cost Supplier Query (TPC-H Q2)                           False              False               True                 False
Shipping Priority (TPC-H Q3)                                     False              False               True                 False
Order Priority Checking Query (TPC-H Q4)                         False              False               True                 False
Local Supplier Volume (TPC-H Q5)                                 False              False               True                 False
Forecasting Revenue Change (TPC-H Q6)                            False              False              False                 False
Forecasting Revenue Change (TPC-H Q7)                            False              False               True                 False
National Market Share (TPC-H Q8)                                 False              False               True                 False
Product Type Profit Measure (TPC-H Q9)                           False              False               True                 False
Forecasting Revenue Change (TPC-H Q10)                           False              False               True                 False
Important Stock Identification (TPC-H Q11)                       False              False               True                 False
Shipping Modes and Order Priority (TPC-H Q12)                    False              False               True                 False
Customer Distribution (TPC-H Q13)                                False              False               True                 False
Forecasting Revenue Change (TPC-H Q14)                           False              False               True                 False
Top Supplier Query (TPC-H Q15)                                   False              False               True                 False
Parts/Supplier Relationship (TPC-H Q16)                          False              False               True                 False
Small-Quantity-Order Revenue (TPC-H Q17)                         False              False               True                 False
Large Volume Customer (TPC-H Q18)                                False              False               True                 False
Discounted Revenue (TPC-H Q19)                                   False              False               True                 False
Potential Part Promotion (TPC-H Q20)                             False              False               True                 False
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)              False              False               True                 False
Global Sales Opportunity Query (TPC-H Q22)                       False              False               True                 False

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-8-8-1-1  PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             28053.05            1171.02           29542.84               2527.16
Minimum Cost Supplier Query (TPC-H Q2)                         1335.66              27.68               4.66                418.43
Shipping Priority (TPC-H Q3)                                   5105.25             120.12               2.60                730.04
Order Priority Checking Query (TPC-H Q4)                       1164.98              53.54               1.82               1237.57
Local Supplier Volume (TPC-H Q5)                               3303.78              65.26               1.84                637.49
Forecasting Revenue Change (TPC-H Q6)                          3336.59              32.82            4268.15                483.90
Forecasting Revenue Change (TPC-H Q7)                          3635.53              85.34               3.60                746.23
National Market Share (TPC-H Q8)                               6356.12             356.32               3.39                592.97
Product Type Profit Measure (TPC-H Q9)                         5814.68              95.44               2.74               1078.96
Forecasting Revenue Change (TPC-H Q10)                         2975.16             161.08               2.79               1251.70
Important Stock Identification (TPC-H Q11)                      397.30              26.16               2.34                237.40
Shipping Modes and Order Priority (TPC-H Q12)                 11683.31              71.59               2.31               1010.08
Customer Distribution (TPC-H Q13)                             10086.02             577.43               2.11               1961.89
Forecasting Revenue Change (TPC-H Q14)                        29701.76              42.08               2.01                523.22
Top Supplier Query (TPC-H Q15)                                 7414.86              42.43            4929.67                532.74
Parts/Supplier Relationship (TPC-H Q16)                         747.53             117.88               2.86                573.74
Small-Quantity-Order Revenue (TPC-H Q17)                        146.08              62.49               1.89               1798.55
Large Volume Customer (TPC-H Q18)                             10234.30             237.23               2.37               6203.08
Discounted Revenue (TPC-H Q19)                                  285.17              74.13               2.96                685.24
Potential Part Promotion (TPC-H Q20)                            523.18              78.22               2.84                644.63
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          203790.97            1760.64               3.28                873.61
Global Sales Opportunity Query (TPC-H Q22)                      425.33              53.83             354.53                231.75

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1              1.0          360.0         2.0     1616.0    1986.0
MonetDB-BHT-8-1-1              1.0           22.0         8.0       29.0      66.0
MySQL-BHT-8-8-1-1              1.0          350.0         3.0      391.0     752.0
PostgreSQL-BHT-8-1-1           1.0           25.0         1.0       86.0     120.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              3.32
MonetDB-BHT-8-1-1              0.13
MySQL-BHT-8-8-1-1              0.01
PostgreSQL-BHT-8-1-1           0.86

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1               1118.89
MonetDB-BHT-8-1-1              33852.42
MySQL-BHT-8-8-1-1             366329.50
PostgreSQL-BHT-8-1-1            4382.28

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
MariaDB-BHT-8-1    1  1              1                340      1   1                   232.94
MonetDB-BHT-8-1    1  1              1                  9      1   1                  8800.00
MySQL-BHT-8-8-1    1  1              1                 41      1   1                  1931.71
PostgreSQL-BHT-8-1 1  1              1                 29      1   1                  2731.03

### Workflow

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1]]
DBMS MonetDB-BHT-8 - Pods [[1]]
DBMS MySQL-BHT-8-8 - Pods [[1]]
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]
DBMS MonetDB-BHT-8 - Pods [[1]]
DBMS MariaDB-BHT-8 - Pods [[1]]
DBMS MySQL-BHT-8-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Workflow as planned
```

This gives a survey about the errors and warnings (result set mismatch) and the latencies of execution per query.
Moreover the loading times (schema creation, ingestion and indexing), the geometric mean of query execution times and the TPC-H metrics power and throughput are reported.
Please note that the results are not suitable for being published as official TPC-H results.
In particular the refresh streams are missing.

To see the summary again you can simply call `bexperiments summary -e 1708411664` with the experiment code.

### Detailed Evaluation

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

```bash
usage: tpch.py [-h] [-aws] [-dbms {PostgreSQL,MonetDB,MySQL,MariaDB}] [-lit LIMIT_IMPORT_TABLE] [-db] [-cx CONTEXT] [-e EXPERIMENT] [-m] [-mc] [-ms MAX_SUT] [-dt] [-nr NUM_RUN] [-nc NUM_CONFIG]
               [-ne NUM_QUERY_EXECUTORS] [-nls NUM_LOADING_SPLIT] [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS] [-nbp NUM_BENCHMARKING_PODS] [-nbt NUM_BENCHMARKING_THREADS] [-sf SCALING_FACTOR]
               [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE]
               [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING] [-rnb REQUEST_NODE_BENCHMARKING] [-tr] [-ii] [-ic] [-is] [-rcp] [-shq]
               {profiling,run,start,load,empty,summary}

Performs a TPC-H experiment. Data is generated and imported into a DBMS from a distributed filesystem (shared disk).

positional arguments:
  {profiling,run,start,load,empty,summary}
                        profile the import or run the TPC-H queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms {PostgreSQL,MonetDB,MySQL,MariaDB}, --dbms {PostgreSQL,MonetDB,MySQL,MariaDB}
                        DBMS
  -lit LIMIT_IMPORT_TABLE, --limit-import-table LIMIT_IMPORT_TABLE
                        limit import to one table, name of this table
  -db, --debug          dump debug informations
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
  -e EXPERIMENT, --experiment EXPERIMENT
                        sets experiment code for continuing started experiment
  -m, --monitoring      activates monitoring
  -mc, --monitoring-cluster
                        activates monitoring for all nodes of cluster
  -ms MAX_SUT, --max-sut MAX_SUT
                        maximum number of parallel DBMS configurations, default is no limit
  -dt, --datatransfer   activates transfer of data per query (not only execution)
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
  -nbp NUM_BENCHMARKING_PODS, --num-benchmarking-pods NUM_BENCHMARKING_PODS
                        comma separated list of number of benchmarkers per configuration
  -nbt NUM_BENCHMARKING_THREADS, --num-benchmarking-threads NUM_BENCHMARKING_THREADS
                        total number of threads per benchmarking process
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF)
  -t TIMEOUT, --timeout TIMEOUT
                        timeout for a run of a query
  -rr REQUEST_RAM, --request-ram REQUEST_RAM
                        request ram for sut, default 16Gi
  -rc REQUEST_CPU, --request-cpu REQUEST_CPU
                        request cpus for sut, default 4
  -rct REQUEST_CPU_TYPE, --request-cpu-type REQUEST_CPU_TYPE
                        request node for sut to have node label cpu=
  -rg REQUEST_GPU, --request-gpu REQUEST_GPU
                        request number of gpus for sut
  -rgt REQUEST_GPU_TYPE, --request-gpu-type REQUEST_GPU_TYPE
                        request node for sut to have node label gpu=
  -rst {None,,local-hdd,shared}, --request-storage-type {None,,local-hdd,shared}
                        request persistent storage of certain type
  -rss REQUEST_STORAGE_SIZE, --request-storage-size REQUEST_STORAGE_SIZE
                        request persistent storage of certain size
  -rnn REQUEST_NODE_NAME, --request-node-name REQUEST_NODE_NAME
                        request a specific node for sut
  -rnl REQUEST_NODE_LOADING, --request-node-loading REQUEST_NODE_LOADING
                        request a specific node for loading pods
  -rnb REQUEST_NODE_BENCHMARKING, --request-node-benchmarking REQUEST_NODE_BENCHMARKING
                        request a specific node for benchmarking pods
  -tr, --test-result    test if result fulfills some basic requirements
  -ii, --init-indexes   adds indexes to tables after ingestion
  -ic, --init-constraints
                        adds constraints to tables after ingestion
  -is, --init-statistics
                        recomputes statistics of tables after ingestion
  -rcp, --recreate-parameter
                        recreate parameter for randomized queries
  -shq, --shuffle-queries
                        have different orderings per stream
```

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

Example:
```bash
nohup python tpch.py -ms 1 -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_monitoring.log &
```

If monitoring is activated, the summary also contains a section like
```bash
## Show Summary

### Workload
    TPC-H Queries SF=1
    Type: tpch
    Duration: 388s 
    Code: 1728076423
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
Loading is tested with [8] threads, split into [8] pods.
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
    disk:251769124
    datadisk:2823016
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 2532.85
Minimum Cost Supplier Query (TPC-H Q2)                             420.58
Shipping Priority (TPC-H Q3)                                       733.52
Order Priority Checking Query (TPC-H Q4)                          1254.93
Local Supplier Volume (TPC-H Q5)                                   634.90
Forecasting Revenue Change (TPC-H Q6)                              496.66
Forecasting Revenue Change (TPC-H Q7)                              825.53
National Market Share (TPC-H Q8)                                   599.74
Product Type Profit Measure (TPC-H Q9)                            1101.86
Forecasting Revenue Change (TPC-H Q10)                            1250.83
Important Stock Identification (TPC-H Q11)                         240.31
Shipping Modes and Order Priority (TPC-H Q12)                      993.45
Customer Distribution (TPC-H Q13)                                 2028.24
Forecasting Revenue Change (TPC-H Q14)                             525.00
Top Supplier Query (TPC-H Q15)                                     539.90
Parts/Supplier Relationship (TPC-H Q16)                            587.83
Small-Quantity-Order Revenue (TPC-H Q17)                          1986.15
Large Volume Customer (TPC-H Q18)                                 7011.29
Discounted Revenue (TPC-H Q19)                                     680.12
Potential Part Promotion (TPC-H Q20)                               662.06
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                878.09
Global Sales Opportunity Query (TPC-H Q22)                         236.46

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           24.0         1.0       82.0     117.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.88

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4280.58

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 1  1              1                 29      1   1                  2731.03

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       128.3      1.3          3.72                 4.91

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1           0        0           0.0                  0.0

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       79.93        0          3.84                 5.02

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        0.01        0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]

TEST passed: Workflow as planned
```

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.
PostgreSQL is fast, so we cannot see a lot (metrics are fetched every 30 seconds).


## Perform Benchmark - Throughput Test

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example:
```bash
nohup python tpch.py -ms 1 -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -nc 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_throughput.log &
```

This runs 3 streams (`-ne`), the first one as a single stream and the following 2 in parallel.

```bash
## Show Summary

### Workload
    TPC-H Queries SF=1
    Type: tpch
    Duration: 481s 
    Code: 1728077023
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
Loading is tested with [8] threads, split into [8] pods.
Benchmarking is tested with [1] threads, split into [1] pods.
Benchmarking is run as [1, 2] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251769120
    datadisk:2822840
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-2-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251769120
    datadisk:2822840
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-2-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251769120
    datadisk:2822840
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-2-1  PostgreSQL-BHT-8-2-2
Pricing Summary Report (TPC-H Q1)                                 2557.89               2587.79               2616.25
Minimum Cost Supplier Query (TPC-H Q2)                             425.55                430.92                423.74
Shipping Priority (TPC-H Q3)                                       727.83                742.55                745.65
Order Priority Checking Query (TPC-H Q4)                          1262.40               1277.75               1244.39
Local Supplier Volume (TPC-H Q5)                                   630.60                644.58                657.68
Forecasting Revenue Change (TPC-H Q6)                              494.13                500.99                516.37
Forecasting Revenue Change (TPC-H Q7)                              764.74                758.54                768.85
National Market Share (TPC-H Q8)                                   624.95                614.48                617.31
Product Type Profit Measure (TPC-H Q9)                            1104.77               1095.17               1073.11
Forecasting Revenue Change (TPC-H Q10)                            1245.66               1263.72               1266.32
Important Stock Identification (TPC-H Q11)                         244.40                261.69                259.53
Shipping Modes and Order Priority (TPC-H Q12)                      988.33               1008.33                989.94
Customer Distribution (TPC-H Q13)                                 1986.26               1959.77               1964.81
Forecasting Revenue Change (TPC-H Q14)                             530.90                550.93                537.25
Top Supplier Query (TPC-H Q15)                                     543.15                560.40                549.18
Parts/Supplier Relationship (TPC-H Q16)                            572.73                571.39                571.61
Small-Quantity-Order Revenue (TPC-H Q17)                          2104.70               2137.37               1929.91
Large Volume Customer (TPC-H Q18)                                 6766.94               7818.25               7691.95
Discounted Revenue (TPC-H Q19)                                     677.64                688.48                683.38
Potential Part Promotion (TPC-H Q20)                               667.69                655.93                617.64
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                891.21                899.94                869.55
Global Sales Opportunity Query (TPC-H Q22)                         239.03                225.38                218.14

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           26.0         1.0       87.0     122.0
PostgreSQL-BHT-8-2-1           1.0           26.0         1.0       87.0     122.0
PostgreSQL-BHT-8-2-2           1.0           26.0         1.0       87.0     122.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.88
PostgreSQL-BHT-8-2-1           0.89
PostgreSQL-BHT-8-2-2           0.88

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4279.42
PostgreSQL-BHT-8-2-1            4217.17
PostgreSQL-BHT-8-2-2            4275.08

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 1  1              1                 29      1   1                  2731.03
PostgreSQL-BHT-8-2 1  1              2                 30      2   1                  5280.00

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1, 2]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Workflow as planned
```

All executions use the same database, so loading times are the same.

Per default, all 3 streams use the same random parameters (like DELTA in Q1) and run in ordering Q1-Q22.
You can change this via
* `-rcp`: Each stream has it's own random parameters
* `-shq`: Use the ordering per stream as required by the TPC-H specification

## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python tpch.py -ms 1 -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_storage.log &
```
The following status shows we have a volumes of type `shared`.
Every experiment running TPC-H of SF=1 at PostgreSQL will take the database from this volume and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of PostgreSQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                            | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+====================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-monetdb-tpch-10    | monetdb         | tpch-10      | True         |               576 | MonetDB    | shared               | 100Gi     | Bound    | 100G   | 21G    |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpch-100   | monetdb         | tpch-100     | True         |              7061 | MonetDB    | shared               | 300Gi     | Bound    | 300G   | 210G   |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpch-3     | monetdb         | tpch-3       | True         |               215 | MonetDB    | shared               | 100Gi     | Bound    | 100G   | 6.2G   |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpch-30    | monetdb         | tpch-30      | True         |              1734 | MonetDB    | shared               | 150Gi     | Bound    | 150G   | 63G    |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-mysql-tpch-1       | mysql           | tpch-1       | True         |              2178 | MySQL      | shared               | 30Gi      | Bound    | 30G    | 11G    |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-mysql-tpch-10      | mysql           | tpch-10      | True         |             33932 | MySQL      | shared               | 150Gi     | Bound    | 150G   | 36G    |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-tpch-1  | postgresql      | tpch-1       | True         |               148 | PostgreSQL | shared               | 100Gi     | Bound    | 50G    | 2.7G   |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-tpch-10 | postgresql      | tpch-10      | True         |              2581 | PostgreSQL | shared               | 100Gi     | Bound    | 100G   | 26G    |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-tpch-30 | postgresql      | tpch-30      | True         |             10073 | PostgreSQL | shared               | 150Gi     | Bound    | 150G   | 76G    |
+------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+

+------------------+--------------+--------------+---------------+
| 1707740320       | sut          |   loaded [s] | benchmarker   |
+==================+==============+==============+===============+
| PostgreSQL-BHT-8 | (1. Running) |       185.41 | (1. Running)  |
+------------------+--------------+--------------+---------------+
```

The result looks something like

```bash
## Show Summary

### Workload
    TPC-H Queries SF=1
    Type: tpch
    Duration: 472s 
    Code: 1728077623
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
Database is persisted to disk of type shared and size 50Gi.
Loading is tested with [8] threads, split into [8] pods.
Benchmarking is tested with [1] threads, split into [1] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248946256
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
    disk:248946256
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
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-2-1-1
Pricing Summary Report (TPC-H Q1)                                  14279.77                 6957.95
Minimum Cost Supplier Query (TPC-H Q2)                              6319.54                 1631.44
Shipping Priority (TPC-H Q3)                                        7480.49                 2500.14
Order Priority Checking Query (TPC-H Q4)                            1266.52                 1267.73
Local Supplier Volume (TPC-H Q5)                                     651.28                  659.57
Forecasting Revenue Change (TPC-H Q6)                                486.42                  496.89
Forecasting Revenue Change (TPC-H Q7)                               1326.14                  794.76
National Market Share (TPC-H Q8)                                     760.09                  647.31
Product Type Profit Measure (TPC-H Q9)                              1660.23                 1272.96
Forecasting Revenue Change (TPC-H Q10)                              1243.45                 1236.73
Important Stock Identification (TPC-H Q11)                           244.40                  247.95
Shipping Modes and Order Priority (TPC-H Q12)                       1032.65                 1016.44
Customer Distribution (TPC-H Q13)                                   1945.24                 1922.70
Forecasting Revenue Change (TPC-H Q14)                               538.45                  542.31
Top Supplier Query (TPC-H Q15)                                       542.72                  545.80
Parts/Supplier Relationship (TPC-H Q16)                              547.27                  551.54
Small-Quantity-Order Revenue (TPC-H Q17)                            1968.03                 2049.02
Large Volume Customer (TPC-H Q18)                                   7662.55                 7451.25
Discounted Revenue (TPC-H Q19)                                       687.44                  697.99
Potential Part Promotion (TPC-H Q20)                                 827.11                  655.38
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                 2351.43                 1244.68
Global Sales Opportunity Query (TPC-H Q22)                           267.75                  235.92

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           28.0         1.0      102.0     139.0
PostgreSQL-BHT-8-2-1-1           1.0           28.0         1.0      102.0     139.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           1.34
PostgreSQL-BHT-8-2-1-1           1.07

### Power@Size
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            2806.74
PostgreSQL-BHT-8-2-1-1            3529.06

### Throughput@Size
                                                   time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                 SF num_experiment num_client                                              
PostgreSQL-BHT-8-1-1 1  1              1                 58      1   1                  1365.52
PostgreSQL-BHT-8-2-1 1  2              1                 38      1   1                  2084.21

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1], [1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Workflow as planned
```
