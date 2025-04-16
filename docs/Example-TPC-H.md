# Benchmark: TPC-H

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TPC-H does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients for the loading test and the throughput test [2].

This example shows how to benchmark 22 reading queries Q1-Q22 derived from TPC-H in PostgreSQL, MonetDB, MySQL and MariaDB.

> The query file is derived from the TPC-H and as such is not comparable to published TPC-H results, as the query file results do not comply with the TPC-H Specification.

1. Official TPC-H benchmark - http://www.tpc.org/tpch
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

## Perform Benchmark - Power Test

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example:
```bash
nohup python tpch.py -ms 4 -dt -tr \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_compare.log &
```

This
* starts a clean instance of PostgreSQL, MonetDB, MySQL and MariaDB (at the same time, `-ms`)
  * data directory inside a Docker container
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

Make sure your cluster can handle 4 DBMS at the same time.
Otherwise adjust die parameter `-ms`.

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
    Duration: 6725s 
    Code: 1728389632
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
    disk:251113752
    datadisk:2139464
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251815148
    datadisk:2841024
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-8-8-1-1 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:260415136
    datadisk:11440660
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251797000
    datadisk:2822864
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-8-8-1-1  PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             27660.48            1195.45           29452.34               2491.43
Minimum Cost Supplier Query (TPC-H Q2)                         1527.71              30.78             373.00                428.29
Shipping Priority (TPC-H Q3)                                   5285.81             112.39            4463.43                746.72
Order Priority Checking Query (TPC-H Q4)                       1144.48              52.90            1644.53               1261.50
Local Supplier Volume (TPC-H Q5)                               3273.95              81.78            4185.27                643.54
Forecasting Revenue Change (TPC-H Q6)                          3289.18              31.37            4168.40                511.22
Forecasting Revenue Change (TPC-H Q7)                          3535.49              84.65            6021.04                765.56
National Market Share (TPC-H Q8)                               6231.84             371.46            9612.94                614.88
Product Type Profit Measure (TPC-H Q9)                         5378.82             112.37            7102.57               1074.75
Forecasting Revenue Change (TPC-H Q10)                         2947.99             178.36            3501.02               1240.03
Important Stock Identification (TPC-H Q11)                      356.00              30.96             535.31                244.32
Shipping Modes and Order Priority (TPC-H Q12)                 11702.51              62.57            7128.72                912.36
Customer Distribution (TPC-H Q13)                              9843.53             595.00           13632.00               2023.34
Forecasting Revenue Change (TPC-H Q14)                        29899.36              54.28            5035.54                533.13
Top Supplier Query (TPC-H Q15)                                 7138.53              39.10           42495.29                547.83
Parts/Supplier Relationship (TPC-H Q16)                         754.75             102.03            1048.20                577.86
Small-Quantity-Order Revenue (TPC-H Q17)                        153.25              52.15            1165.42               2026.63
Large Volume Customer (TPC-H Q18)                             10168.78             195.65            6178.18               6797.82
Discounted Revenue (TPC-H Q19)                                  305.53              85.33             434.37                688.31
Potential Part Promotion (TPC-H Q20)                            534.16              91.67             810.81                651.63
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          200201.66            1741.57           18959.21                907.32
Global Sales Opportunity Query (TPC-H Q22)                      401.78              57.55             483.53                233.61

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1              0.0          353.0         2.0     1676.0    2039.0
MonetDB-BHT-8-1-1              1.0           20.0         8.0       28.0      63.0
MySQL-BHT-8-8-1-1              0.0          527.0         3.0     2230.0    2767.0
PostgreSQL-BHT-8-1-1           1.0           28.0         1.0       87.0     124.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              3.30
MonetDB-BHT-8-1-1              0.13
MySQL-BHT-8-8-1-1              3.52
PostgreSQL-BHT-8-1-1           0.87

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1               1124.93
MonetDB-BHT-8-1-1              32939.32
MySQL-BHT-8-8-1-1               1053.60
PostgreSQL-BHT-8-1-1            4294.04

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
MariaDB-BHT-8-1    1  1              1                336      1   1                   235.71
MonetDB-BHT-8-1    1  1              1                  8      1   1                  9900.00
MySQL-BHT-8-8-1    1  1              1                172      1   1                   460.47
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
  -sf 3 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_monitoring.log &
```

If monitoring is activated, the summary also contains a section like
```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 680s 
    Code: 1728378203
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
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
    disk:257355956
    datadisk:8382332
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 6144.58
Minimum Cost Supplier Query (TPC-H Q2)                            2129.20
Shipping Priority (TPC-H Q3)                                      2477.78
Order Priority Checking Query (TPC-H Q4)                          3102.17
Local Supplier Volume (TPC-H Q5)                                  2245.79
Forecasting Revenue Change (TPC-H Q6)                             1149.58
Forecasting Revenue Change (TPC-H Q7)                             2305.58
National Market Share (TPC-H Q8)                                  1429.89
Product Type Profit Measure (TPC-H Q9)                            3185.34
Forecasting Revenue Change (TPC-H Q10)                            3055.83
Important Stock Identification (TPC-H Q11)                         557.39
Shipping Modes and Order Priority (TPC-H Q12)                     2436.77
Customer Distribution (TPC-H Q13)                                 6535.50
Forecasting Revenue Change (TPC-H Q14)                            1266.75
Top Supplier Query (TPC-H Q15)                                    1385.89
Parts/Supplier Relationship (TPC-H Q16)                           1240.27
Small-Quantity-Order Revenue (TPC-H Q17)                          5807.32
Large Volume Customer (TPC-H Q18)                                19196.50
Discounted Revenue (TPC-H Q19)                                    1923.09
Potential Part Promotion (TPC-H Q20)                              1133.39
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               2760.21
Global Sales Opportunity Query (TPC-H Q22)                         458.75

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          114.0         1.0      216.0     339.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           2.31

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4826.71

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
PostgreSQL-BHT-8-1 3  1              1                 75      1   3                   3168.0

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      391.92      1.0          6.38                10.62

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       13.95     0.03          1.32                 3.01

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      355.85     3.27          6.82                11.07

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       11.12        0          0.23                 0.24

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
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
    Duration: 682s 
    Code: 1728337000
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
    disk:248971580
    datadisk:2821768
    volume_size:50G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:248971560
    datadisk:2821768
    volume_size:50G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-2-1-1
Pricing Summary Report (TPC-H Q1)                                   2577.22                11440.86
Minimum Cost Supplier Query (TPC-H Q2)                               994.22                 3865.61
Shipping Priority (TPC-H Q3)                                        1394.24                 6878.50
Order Priority Checking Query (TPC-H Q4)                            1248.14                 1274.40
Local Supplier Volume (TPC-H Q5)                                     761.01                  653.66
Forecasting Revenue Change (TPC-H Q6)                                476.76                  498.91
Forecasting Revenue Change (TPC-H Q7)                               1039.67                  811.60
National Market Share (TPC-H Q8)                                     757.33                  672.12
Product Type Profit Measure (TPC-H Q9)                              2026.31                 3169.53
Forecasting Revenue Change (TPC-H Q10)                              1238.08                 1248.64
Important Stock Identification (TPC-H Q11)                           242.20                  248.26
Shipping Modes and Order Priority (TPC-H Q12)                       1015.09                 1021.58
Customer Distribution (TPC-H Q13)                                   2033.41                 2053.73
Forecasting Revenue Change (TPC-H Q14)                               512.76                  539.77
Top Supplier Query (TPC-H Q15)                                       528.55                  549.37
Parts/Supplier Relationship (TPC-H Q16)                              562.45                  564.45
Small-Quantity-Order Revenue (TPC-H Q17)                            2006.01                 1926.38
Large Volume Customer (TPC-H Q18)                                   6906.77                 8203.75
Discounted Revenue (TPC-H Q19)                                       663.41                  691.74
Potential Part Promotion (TPC-H Q20)                                 650.63                  631.71
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                 2272.23                 1162.69
Global Sales Opportunity Query (TPC-H Q22)                           299.65                  238.90

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           26.0         1.0       99.0     133.0
PostgreSQL-BHT-8-2-1-1           1.0           26.0         1.0       99.0     133.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           1.04
PostgreSQL-BHT-8-2-1-1           1.25

### Power@Size
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            3601.39
PostgreSQL-BHT-8-2-1-1            3026.05

### Throughput@Size
                                                   time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                 SF num_experiment num_client                                              
PostgreSQL-BHT-8-1-1 1  1              1                 33      1   1                   2400.0
PostgreSQL-BHT-8-2-1 1  2              1                 55      1   1                   1440.0

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


The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.


























## Example: MonetDB TPC-H@100

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
  run </dev/null &>$LOG_DIR/doc_tpch_monetdb_1.log &
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

### Perform Benchmark - Power Test

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
  run </dev/null &>$LOG_DIR/doc_tpch_monetdb_2.log &
```

### Evaluate Results

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

### Perform Benchmark - Throughput Test

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
  run </dev/null &>$LOG_DIR/doc_tpch_monetdb_3.log &
```

### Evaluate Results

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

