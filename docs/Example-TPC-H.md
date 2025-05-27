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

doc_tpch_testcase_compare.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 4536s 
    Code: 1748269844
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.5.
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-BHT-8-1-1 uses docker image mariadb:11.4.7
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:263554572
    datadisk:2091
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748269844
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:264365372
    datadisk:2883
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748269844
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:254872720
    datadisk:8286
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748269844
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:264236264
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748269844

### Errors (failed queries)
No errors

### Warnings (result mismatch)
                                                     MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                False              False              True                 False
Minimum Cost Supplier Query (TPC-H Q2)                           False              False              True                 False
Shipping Priority (TPC-H Q3)                                     False              False              True                 False
Order Priority Checking Query (TPC-H Q4)                         False              False              True                 False
Local Supplier Volume (TPC-H Q5)                                 False              False              True                 False
Forecasting Revenue Change (TPC-H Q6)                            False              False              True                 False
Forecasting Revenue Change (TPC-H Q7)                            False              False              True                 False
National Market Share (TPC-H Q8)                                 False              False              True                 False
Product Type Profit Measure (TPC-H Q9)                           False              False              True                 False
Forecasting Revenue Change (TPC-H Q10)                           False              False              True                 False
Important Stock Identification (TPC-H Q11)                       False              False              True                 False
Shipping Modes and Order Priority (TPC-H Q12)                    False              False              True                 False
Customer Distribution (TPC-H Q13)                                False              False              True                 False
Forecasting Revenue Change (TPC-H Q14)                           False              False              True                 False
Top Supplier Query (TPC-H Q15)                                   False              False              True                 False
Parts/Supplier Relationship (TPC-H Q16)                          False              False              True                 False
Small-Quantity-Order Revenue (TPC-H Q17)                         False              False              True                 False
Large Volume Customer (TPC-H Q18)                                False              False              True                 False
Discounted Revenue (TPC-H Q19)                                   False              False              True                 False
Potential Part Promotion (TPC-H Q20)                             False              False              True                 False
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)              False              False              True                 False
Global Sales Opportunity Query (TPC-H Q22)                       False              False              True                 False

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             25596.54            1008.13             89.67               2561.85
Minimum Cost Supplier Query (TPC-H Q2)                         1328.55              28.90              4.11                433.37
Shipping Priority (TPC-H Q3)                                   5018.42             108.74              1.98                736.75
Order Priority Checking Query (TPC-H Q4)                       1024.25              52.80              3.74               1253.14
Local Supplier Volume (TPC-H Q5)                               3231.62              77.29              2.89                638.80
Forecasting Revenue Change (TPC-H Q6)                          2767.43              29.64              2.47                480.65
Forecasting Revenue Change (TPC-H Q7)                          3529.83              91.27              3.04                747.68
National Market Share (TPC-H Q8)                               6326.09             440.18              3.10                604.27
Product Type Profit Measure (TPC-H Q9)                         5266.92             101.55              2.94               1097.71
Forecasting Revenue Change (TPC-H Q10)                         2668.91             177.44              2.72               1274.28
Important Stock Identification (TPC-H Q11)                      353.76              20.79              2.49                248.48
Shipping Modes and Order Priority (TPC-H Q12)                 11065.22              60.30              2.55                991.46
Customer Distribution (TPC-H Q13)                              9861.28             503.47              2.12               1884.18
Forecasting Revenue Change (TPC-H Q14)                        28531.73              59.32              2.18                523.29
Top Supplier Query (TPC-H Q15)                                 6768.26              43.30              4.42                548.79
Parts/Supplier Relationship (TPC-H Q16)                         637.48              92.40              2.81                562.44
Small-Quantity-Order Revenue (TPC-H Q17)                        162.26              56.54              2.01               2139.44
Large Volume Customer (TPC-H Q18)                             10197.10             193.56              3.36               7940.61
Discounted Revenue (TPC-H Q19)                                  287.46            6081.89              3.19                691.08
Potential Part Promotion (TPC-H Q20)                            565.24             104.37              2.82                644.61
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          191530.61            2177.42              3.04                878.67
Global Sales Opportunity Query (TPC-H Q22)                      392.77              53.19              2.62                240.65

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1              1.0          265.0         2.0     1660.0    1936.0
MonetDB-BHT-8-1-1              1.0           21.0         8.0       31.0      68.0
MySQL-BHT-64-1-1               1.0            5.0         3.0       11.0      28.0
PostgreSQL-BHT-8-1-1           1.0           28.0         1.0       85.0     122.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              3.17
MonetDB-BHT-8-1-1              0.16
MySQL-BHT-64-1-1               0.00
PostgreSQL-BHT-8-1-1           0.88

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1               1177.99
MonetDB-BHT-8-1-1              27642.07
MySQL-BHT-64-1-1             1090321.73
PostgreSQL-BHT-8-1-1            4266.21

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
MariaDB-BHT-8-1    1  1              1                322      1   1           245.96
MonetDB-BHT-8-1    1  1              1                 16      1   1          4950.00
MySQL-BHT-64-1     1  1              1                  3      1   1         26400.00
PostgreSQL-BHT-8-1 1  1              1                 32      1   1          2475.00

### Workflow

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1]]
DBMS MonetDB-BHT-8 - Pods [[1]]
DBMS MySQL-BHT-64 - Pods [[1]]
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]
DBMS MonetDB-BHT-8 - Pods [[1]]
DBMS MariaDB-BHT-8 - Pods [[1]]
DBMS MySQL-BHT-64 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST failed: SQL warnings (result mismatch)
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
  -sf 10 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_monitoring.log &
```

If monitoring is activated, the summary also contains a section like this:

doc_tpch_testcase_monitoring.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=10
    Type: tpch
    Duration: 1644s 
    Code: 1748331898
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.5.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:328756996
    datadisk:27209
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748331898

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                17596.74
Minimum Cost Supplier Query (TPC-H Q2)                            4769.56
Shipping Priority (TPC-H Q3)                                      5591.01
Order Priority Checking Query (TPC-H Q4)                          8796.42
Local Supplier Volume (TPC-H Q5)                                  5395.29
Forecasting Revenue Change (TPC-H Q6)                             3196.23
Forecasting Revenue Change (TPC-H Q7)                             4818.90
National Market Share (TPC-H Q8)                                  4973.95
Product Type Profit Measure (TPC-H Q9)                            7650.97
Forecasting Revenue Change (TPC-H Q10)                            5962.71
Important Stock Identification (TPC-H Q11)                        2216.07
Shipping Modes and Order Priority (TPC-H Q12)                     5912.02
Customer Distribution (TPC-H Q13)                                20759.99
Forecasting Revenue Change (TPC-H Q14)                            4685.57
Top Supplier Query (TPC-H Q15)                                    4265.11
Parts/Supplier Relationship (TPC-H Q16)                           3545.07
Small-Quantity-Order Revenue (TPC-H Q17)                         19429.96
Large Volume Customer (TPC-H Q18)                                55055.67
Discounted Revenue (TPC-H Q19)                                    4745.62
Potential Part Promotion (TPC-H Q20)                              3139.20
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               6177.27
Global Sales Opportunity Query (TPC-H Q22)                        1113.71

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          375.0         1.0      672.0    1056.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           6.15

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            5939.61

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-8-1 10 1              1                208      1  10          3807.69

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1     1450.92      2.3         16.63                31.21

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      135.11     0.12          0.04                 9.18

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1     1084.02     6.44         40.71                56.03

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       16.62     0.06          0.29                 0.29

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
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

doc_tpch_testcase_throughput.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 623s 
    Code: 1748275365
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.5.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:287190180
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748275365
PostgreSQL-BHT-8-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:294181468
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748275365
PostgreSQL-BHT-8-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:294181468
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748275365

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-2-1  PostgreSQL-BHT-8-2-2
Pricing Summary Report (TPC-H Q1)                                 2484.73               2488.54               2472.94
Minimum Cost Supplier Query (TPC-H Q2)                             451.11                432.09                432.69
Shipping Priority (TPC-H Q3)                                       727.66                726.99                714.11
Order Priority Checking Query (TPC-H Q4)                          1228.87               1271.94               1248.25
Local Supplier Volume (TPC-H Q5)                                   634.79                645.42                626.38
Forecasting Revenue Change (TPC-H Q6)                              490.74                483.18                481.71
Forecasting Revenue Change (TPC-H Q7)                              761.74                751.61                757.74
National Market Share (TPC-H Q8)                                   589.96                604.76                593.82
Product Type Profit Measure (TPC-H Q9)                            1095.19               1051.12               1037.42
Forecasting Revenue Change (TPC-H Q10)                            1245.43               1231.50               1228.87
Important Stock Identification (TPC-H Q11)                         242.91                249.12                243.82
Shipping Modes and Order Priority (TPC-H Q12)                      986.97                992.85                981.89
Customer Distribution (TPC-H Q13)                                 2001.40               2105.60               1987.64
Forecasting Revenue Change (TPC-H Q14)                             520.75                519.22                531.32
Top Supplier Query (TPC-H Q15)                                     536.79                536.61                535.15
Parts/Supplier Relationship (TPC-H Q16)                            562.93                604.19                569.30
Small-Quantity-Order Revenue (TPC-H Q17)                          2154.25               2134.13               2008.23
Large Volume Customer (TPC-H Q18)                                 7354.80               8313.35               6822.96
Discounted Revenue (TPC-H Q19)                                     678.66                676.15                666.90
Potential Part Promotion (TPC-H Q20)                               682.39                665.39                638.61
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                881.63                834.01                847.64
Global Sales Opportunity Query (TPC-H Q22)                         238.54                215.55                212.56

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           73.0         1.0       89.0     171.0
PostgreSQL-BHT-8-2-1           1.0           73.0         1.0       89.0     171.0
PostgreSQL-BHT-8-2-2           1.0           73.0         1.0       89.0     171.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.89
PostgreSQL-BHT-8-2-1           0.88
PostgreSQL-BHT-8-2-2           0.86

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4279.38
PostgreSQL-BHT-8-2-1            4273.76
PostgreSQL-BHT-8-2-2            4380.04

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-8-1 1  1              1                 33      1   1           2400.0
PostgreSQL-BHT-8-2 1  1              2                 33      2   1           4800.0

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1, 2]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
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

doc_tpch_testcase_storage.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 957s 
    Code: 1748276056
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.5.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:298541156
    datadisk:2757
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748276056
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:298541144
    datadisk:2757
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748276056

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-2-1-1
Pricing Summary Report (TPC-H Q1)                                   2546.83                49404.29
Minimum Cost Supplier Query (TPC-H Q2)                               414.65                 5987.18
Shipping Priority (TPC-H Q3)                                         724.71                 7592.02
Order Priority Checking Query (TPC-H Q4)                            1221.46                 1272.88
Local Supplier Volume (TPC-H Q5)                                     634.44                  662.15
Forecasting Revenue Change (TPC-H Q6)                                476.95                  493.89
Forecasting Revenue Change (TPC-H Q7)                                755.13                  979.40
National Market Share (TPC-H Q8)                                     594.46                  719.69
Product Type Profit Measure (TPC-H Q9)                              1065.38                 1958.27
Forecasting Revenue Change (TPC-H Q10)                              1221.30                 1254.67
Important Stock Identification (TPC-H Q11)                           250.25                  255.36
Shipping Modes and Order Priority (TPC-H Q12)                        899.39                  936.56
Customer Distribution (TPC-H Q13)                                   1927.53                 1933.35
Forecasting Revenue Change (TPC-H Q14)                               520.25                  535.45
Top Supplier Query (TPC-H Q15)                                       533.61                  538.72
Parts/Supplier Relationship (TPC-H Q16)                              547.75                  558.85
Small-Quantity-Order Revenue (TPC-H Q17)                            1964.18                 1964.26
Large Volume Customer (TPC-H Q18)                                   7146.87                 7350.19
Discounted Revenue (TPC-H Q19)                                       671.59                  692.50
Potential Part Promotion (TPC-H Q20)                                 655.28                  759.33
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  899.22                 2012.44
Global Sales Opportunity Query (TPC-H Q22)                           236.91                  303.03

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           44.0         1.0       87.0     140.0
PostgreSQL-BHT-8-2-1-1           1.0           44.0         1.0       87.0     140.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           0.86
PostgreSQL-BHT-8-2-1-1           1.38

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            4366.06
PostgreSQL-BHT-8-2-1-1            2700.42

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                   time [s]  count  SF  Throughput@Size
DBMS                 SF num_experiment num_client                                      
PostgreSQL-BHT-8-1-1 1  1              1                 30      1   1          2640.00
PostgreSQL-BHT-8-2-1 1  2              1                 93      1   1           851.61

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1], [1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
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
  -rst shared -rss 1000Gi \
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
The disk is of storageClass shared and of size 1000Gi and 210G of that space is used.
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

doc_tpch_monetdb_1.log
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
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_monetdb_2.log &
```

### Evaluate Results

doc_tpch_monetdb_2.log
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
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_monetdb_3.log &
```

### Evaluate Results

doc_tpch_monetdb_3.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=100
    Type: tpch
    Duration: 4073s 
    Code: 1748346455
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.5.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 500Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:300888312
    datadisk:218013
    volume_size:1000G
    volume_used:213G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748346455
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:300888332
    datadisk:214826
    volume_size:1000G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748346455
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:300888340
    datadisk:214826
    volume_size:1000G
    volume_used:219G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748346455
MonetDB-BHT-8-3-2 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:300888340
    datadisk:214826
    volume_size:1000G
    volume_used:219G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748346455
MonetDB-BHT-8-3-3 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:300888340
    datadisk:214826
    volume_size:1000G
    volume_used:219G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748346455

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
Pricing Summary Report (TPC-H Q1)                            671875.18          317169.26          551142.22          551908.15          539334.64
Minimum Cost Supplier Query (TPC-H Q2)                        35953.22            1856.15            2364.49            1647.61           13950.24
Shipping Priority (TPC-H Q3)                                  97322.40           13830.17           22054.60           19137.90           18259.82
Order Priority Checking Query (TPC-H Q4)                     360550.82           11787.08           21214.22           28415.49           21448.22
Local Supplier Volume (TPC-H Q5)                              15658.66            9914.87           10311.96           16270.26           10840.56
Forecasting Revenue Change (TPC-H Q6)                          7627.15            5880.63            2601.37            1770.02            5170.55
Forecasting Revenue Change (TPC-H Q7)                         10795.02            5743.49           10989.31            3870.12            8779.77
National Market Share (TPC-H Q8)                             109088.82           35832.02           37522.47           37717.44           40407.38
Product Type Profit Measure (TPC-H Q9)                        33004.76           18953.68           27769.01           25424.27           28464.20
Forecasting Revenue Change (TPC-H Q10)                        73687.54           31580.39           29758.43           29362.91           27369.57
Important Stock Identification (TPC-H Q11)                     6883.61            1322.37            1275.85            1883.44            2514.07
Shipping Modes and Order Priority (TPC-H Q12)                  4822.22            4612.66            5784.47            6404.49            5801.77
Customer Distribution (TPC-H Q13)                            325509.70          115125.25          135608.92          147092.09          131101.02
Forecasting Revenue Change (TPC-H Q14)                         6015.60            5783.98            2318.68             485.40            6775.62
Top Supplier Query (TPC-H Q15)                                 6525.95            6484.30            7694.76            5862.46            7569.85
Parts/Supplier Relationship (TPC-H Q16)                       17452.59           14054.08           14103.74           12534.97           15566.66
Small-Quantity-Order Revenue (TPC-H Q17)                     104161.88           14022.13           13538.29            7599.38           12533.53
Large Volume Customer (TPC-H Q18)                             44934.43           25072.99           28651.15           29590.37           28775.43
Discounted Revenue (TPC-H Q19)                                 8310.47            7767.28            9900.23           10129.90           10677.40
Potential Part Promotion (TPC-H Q20)                          12023.12            6472.71            9318.20            8081.92            8526.39
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           24081.16           19085.56           53810.93           40687.15           45517.53
Global Sales Opportunity Query (TPC-H Q22)                     7768.57            8525.75            6334.48            7268.50            6083.58

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0         1815.0        12.0     6485.0    8320.0
MonetDB-BHT-8-2-1           1.0         1815.0        12.0     6485.0    8320.0
MonetDB-BHT-8-3-1           1.0         1815.0        12.0     6485.0    8320.0
MonetDB-BHT-8-3-2           1.0         1815.0        12.0     6485.0    8320.0
MonetDB-BHT-8-3-3           1.0         1815.0        12.0     6485.0    8320.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          29.86
MonetDB-BHT-8-2-1          12.84
MonetDB-BHT-8-3-1          14.79
MonetDB-BHT-8-3-2          12.49
MonetDB-BHT-8-3-3          17.15

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           12283.39
MonetDB-BHT-8-2-1           29614.41
MonetDB-BHT-8-3-1           25664.08
MonetDB-BHT-8-3-2           30043.52
MonetDB-BHT-8-3-3           21778.90

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MonetDB-BHT-8-1 100 1              1               2014      1  100          3932.47
MonetDB-BHT-8-2 100 1              2                700      1  100         11314.29
MonetDB-BHT-8-3 100 1              3               1023      3  100         23225.81

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     4991.95    19.07         60.89               108.48
MonetDB-BHT-8-2     3873.07    15.15         95.47               179.62
MonetDB-BHT-8-3     8515.73    14.56        143.45               338.67

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       27.24     0.00          0.30                 0.32
MonetDB-BHT-8-2       27.24     0.01          0.53                 0.57
MonetDB-BHT-8-3       60.94     0.29          1.01                 1.05

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.

