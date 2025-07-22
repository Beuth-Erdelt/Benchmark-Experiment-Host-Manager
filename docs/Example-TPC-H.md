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
nohup python tpch.py -ms 1 -dt -tr \
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

doc_tpch_testcase_compare.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 7762s 
    Code: 1752145620
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.9.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:425215960
    datadisk:2091
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1752145620
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:426024916
    datadisk:2883
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1752145620
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:430325360
    datadisk:7077
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1752145620
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:426092612
    datadisk:2949
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1752145620

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             26475.81            1090.35          29638.89               2506.47
Minimum Cost Supplier Query (TPC-H Q2)                         1448.71              28.11            355.73                444.65
Shipping Priority (TPC-H Q3)                                   5550.37             101.47           4409.17                732.31
Order Priority Checking Query (TPC-H Q4)                       1026.02              50.60           1559.06                346.06
Local Supplier Volume (TPC-H Q5)                               3242.78              73.23           4179.81                599.28
Forecasting Revenue Change (TPC-H Q6)                          3047.53              26.59           3969.57                471.55
Forecasting Revenue Change (TPC-H Q7)                          3787.50              76.71           6121.17                723.47
National Market Share (TPC-H Q8)                               6543.34             428.36           9618.80                392.40
Product Type Profit Measure (TPC-H Q9)                         5769.68              94.91           7233.99               1503.22
Forecasting Revenue Change (TPC-H Q10)                         2666.47             159.44           3043.14                657.90
Important Stock Identification (TPC-H Q11)                      458.17              20.13            521.41                170.74
Shipping Modes and Order Priority (TPC-H Q12)                 11782.71              55.79           6775.29                671.72
Customer Distribution (TPC-H Q13)                             10346.28             562.70          13592.95               2125.11
Forecasting Revenue Change (TPC-H Q14)                        29426.50              49.84           4921.25                519.32
Top Supplier Query (TPC-H Q15)                                 6859.21              39.93          43911.94                572.06
Parts/Supplier Relationship (TPC-H Q16)                         773.90              98.19           1102.20                476.86
Small-Quantity-Order Revenue (TPC-H Q17)                        164.45              58.73           1247.49               1569.61
Large Volume Customer (TPC-H Q18)                             10445.05             183.61           6024.96               5027.48
Discounted Revenue (TPC-H Q19)                                  268.55            6778.99            434.76                124.89
Potential Part Promotion (TPC-H Q20)                            520.98             126.65            812.50                283.78
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          195422.95            2447.84          18698.27                748.92
Global Sales Opportunity Query (TPC-H Q22)                      425.13              58.47            534.92                197.42

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1             17.0          237.0         1.0     2125.0    2384.0
MonetDB-BHT-8-1-1             17.0           22.0         8.0      101.0     153.0
MySQL-BHT-64-1-1              14.0          576.0         4.0     3684.0    4281.0
PostgreSQL-BHT-8-1-1          18.0           28.0         0.0      166.0     215.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              3.31
MonetDB-BHT-8-1-1              0.15
MySQL-BHT-64-1-1               3.48
PostgreSQL-BHT-8-1-1           0.66

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1               1119.93
MonetDB-BHT-8-1-1              28012.94
MySQL-BHT-64-1-1                1060.74
PostgreSQL-BHT-8-1-1            5762.59

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
MariaDB-BHT-8-1    1.0 1              1                330      1  1.0           240.00
MonetDB-BHT-8-1    1.0 1              1                 18      1  1.0          4400.00
MySQL-BHT-64-1     1.0 1              1                175      1  1.0           452.57
PostgreSQL-BHT-8-1 1.0 1              1                 26      1  1.0          3046.15

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
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
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
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
    Type: tpch
    Duration: 1637s 
    Code: 1748415248
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
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
    disk:329081380
    datadisk:27209
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748415248

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                17139.23
Minimum Cost Supplier Query (TPC-H Q2)                            4110.01
Shipping Priority (TPC-H Q3)                                      5458.75
Order Priority Checking Query (TPC-H Q4)                          8540.07
Local Supplier Volume (TPC-H Q5)                                  5237.90
Forecasting Revenue Change (TPC-H Q6)                             3104.04
Forecasting Revenue Change (TPC-H Q7)                             4716.80
National Market Share (TPC-H Q8)                                  4868.49
Product Type Profit Measure (TPC-H Q9)                            7419.58
Forecasting Revenue Change (TPC-H Q10)                            6891.22
Important Stock Identification (TPC-H Q11)                        2180.67
Shipping Modes and Order Priority (TPC-H Q12)                     5736.48
Customer Distribution (TPC-H Q13)                                19746.51
Forecasting Revenue Change (TPC-H Q14)                            4509.14
Top Supplier Query (TPC-H Q15)                                    4167.13
Parts/Supplier Relationship (TPC-H Q16)                           3452.79
Small-Quantity-Order Revenue (TPC-H Q17)                         19934.07
Large Volume Customer (TPC-H Q18)                                53555.52
Discounted Revenue (TPC-H Q19)                                    4514.44
Potential Part Promotion (TPC-H Q20)                              3112.82
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               5909.52
Global Sales Opportunity Query (TPC-H Q22)                        1077.97

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          384.0         1.0      687.0    1080.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1            6.0

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            6086.65

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-8-1 10 1              1                202      1  10          3920.79

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1     1465.39     3.33         16.85                30.91

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      153.35      0.4          0.04                10.53

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      1080.5     6.23         27.47                42.75

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       16.93        0          0.28                 0.28

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
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 594s 
    Code: 1748416988
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
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
    disk:304042092
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748416988
PostgreSQL-BHT-8-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:304042096
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748416988
PostgreSQL-BHT-8-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:304042096
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748416988

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-2-1  PostgreSQL-BHT-8-2-2
Pricing Summary Report (TPC-H Q1)                                 2497.40               2511.48               2495.05
Minimum Cost Supplier Query (TPC-H Q2)                             425.27                422.61                427.31
Shipping Priority (TPC-H Q3)                                       752.74                747.38                773.43
Order Priority Checking Query (TPC-H Q4)                          1245.43               1216.04               1273.53
Local Supplier Volume (TPC-H Q5)                                   647.59                640.98                661.82
Forecasting Revenue Change (TPC-H Q6)                              494.06                499.00                511.56
Forecasting Revenue Change (TPC-H Q7)                              773.62                753.51                763.88
National Market Share (TPC-H Q8)                                   617.91                613.36                633.55
Product Type Profit Measure (TPC-H Q9)                            1085.73               1039.60               1078.60
Forecasting Revenue Change (TPC-H Q10)                            1255.35               1236.60               1246.75
Important Stock Identification (TPC-H Q11)                         244.50                244.31                253.80
Shipping Modes and Order Priority (TPC-H Q12)                     1021.27               1025.54               1018.98
Customer Distribution (TPC-H Q13)                                 1886.70               1934.17               1902.37
Forecasting Revenue Change (TPC-H Q14)                             540.60                526.77                548.27
Top Supplier Query (TPC-H Q15)                                     550.23                557.28                552.17
Parts/Supplier Relationship (TPC-H Q16)                            560.00                576.71                553.01
Small-Quantity-Order Revenue (TPC-H Q17)                          2042.63               2059.54               2123.69
Large Volume Customer (TPC-H Q18)                                 8023.64               6910.84               7928.53
Discounted Revenue (TPC-H Q19)                                     699.08                694.65                685.55
Potential Part Promotion (TPC-H Q20)                               641.97                644.13                648.88
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                905.93                879.86                867.43
Global Sales Opportunity Query (TPC-H Q22)                         239.00                218.08                225.76

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0           27.0         1.0       87.0     123.0
PostgreSQL-BHT-8-2-1           1.0           27.0         1.0       87.0     123.0
PostgreSQL-BHT-8-2-2           1.0           27.0         1.0       87.0     123.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.88
PostgreSQL-BHT-8-2-1           0.87
PostgreSQL-BHT-8-2-2           0.88

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            4250.06
PostgreSQL-BHT-8-2-1            4317.15
PostgreSQL-BHT-8-2-2            4235.63

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-8-1 1  1              1                 32      1   1           2475.0
PostgreSQL-BHT-8-2 1  1              2                 32      2   1           4950.0

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

```bash
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
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 853s 
    Code: 1748417679
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
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
    disk:301219704
    datadisk:2757
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748417679
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301219688
    datadisk:2757
    volume_size:30G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748417679

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-2-1-1
Pricing Summary Report (TPC-H Q1)                                   2588.36                17033.92
Minimum Cost Supplier Query (TPC-H Q2)                               423.41                 6390.27
Shipping Priority (TPC-H Q3)                                         747.56                 6980.26
Order Priority Checking Query (TPC-H Q4)                            1248.18                 1264.69
Local Supplier Volume (TPC-H Q5)                                     648.03                  669.12
Forecasting Revenue Change (TPC-H Q6)                                500.03                  516.54
Forecasting Revenue Change (TPC-H Q7)                                763.18                  981.14
National Market Share (TPC-H Q8)                                     598.95                  687.29
Product Type Profit Measure (TPC-H Q9)                              1078.06                 1872.35
Forecasting Revenue Change (TPC-H Q10)                              1230.80                 1264.56
Important Stock Identification (TPC-H Q11)                           250.98                  251.83
Shipping Modes and Order Priority (TPC-H Q12)                       1012.02                 1011.29
Customer Distribution (TPC-H Q13)                                   1940.91                 1874.39
Forecasting Revenue Change (TPC-H Q14)                               532.92                  556.13
Top Supplier Query (TPC-H Q15)                                       549.82                  593.43
Parts/Supplier Relationship (TPC-H Q16)                              547.15                  565.34
Small-Quantity-Order Revenue (TPC-H Q17)                            1983.55                 2084.26
Large Volume Customer (TPC-H Q18)                                   6969.96                 6427.64
Discounted Revenue (TPC-H Q19)                                       689.88                  707.44
Potential Part Promotion (TPC-H Q20)                                 666.25                  774.95
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  889.95                 2054.75
Global Sales Opportunity Query (TPC-H Q22)                           242.59                  366.08

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0           41.0         1.0       84.0     135.0
PostgreSQL-BHT-8-2-1-1           1.0           41.0         1.0       84.0     135.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           0.87
PostgreSQL-BHT-8-2-1-1           1.34

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            4283.85
PostgreSQL-BHT-8-2-1-1            2795.51

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                   time [s]  count  SF  Throughput@Size
DBMS                 SF num_experiment num_client                                      
PostgreSQL-BHT-8-1-1 1  1              1                 31      1   1          2554.84
PostgreSQL-BHT-8-2-1 1  2              1                 60      1   1          1320.00

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
  -t 3600 -dt \
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

```bash
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
```markdown
## Show Summary

### Workload
TPC-H Queries SF=100
    Type: tpch
    Duration: 9645s 
    Code: 1748418609
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 1000Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301220308
    datadisk:213089
    volume_size:1000G
    volume_used:209G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748418609

### Errors (failed queries)
                                MonetDB-BHT-8-1-1
Discounted Revenue (TPC-H Q19)               True
Discounted Revenue (TPC-H Q19)
MonetDB-BHT-8-1-1: numRun 1: : java.sql.SQLException: Query aborted due to timeout

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                            251831.87
Minimum Cost Supplier Query (TPC-H Q2)                         1950.89
Shipping Priority (TPC-H Q3)                                  14166.02
Order Priority Checking Query (TPC-H Q4)                      15180.64
Local Supplier Volume (TPC-H Q5)                              10880.50
Forecasting Revenue Change (TPC-H Q6)                          7369.26
Forecasting Revenue Change (TPC-H Q7)                         11308.37
National Market Share (TPC-H Q8)                              64562.58
Product Type Profit Measure (TPC-H Q9)                        16805.17
Forecasting Revenue Change (TPC-H Q10)                        27650.78
Important Stock Identification (TPC-H Q11)                     1264.27
Shipping Modes and Order Priority (TPC-H Q12)                  5209.90
Customer Distribution (TPC-H Q13)                            122043.14
Forecasting Revenue Change (TPC-H Q14)                         7956.57
Top Supplier Query (TPC-H Q15)                                10030.79
Parts/Supplier Relationship (TPC-H Q16)                       12361.31
Small-Quantity-Order Revenue (TPC-H Q17)                      17835.86
Large Volume Customer (TPC-H Q18)                             20898.84
Potential Part Promotion (TPC-H Q20)                          67758.20
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           20541.82
Global Sales Opportunity Query (TPC-H Q22)                     7484.85

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0         1780.0         8.0     5625.0    7421.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          16.31

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           23353.41

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MonetDB-BHT-8-1 100 1              1               1963      1  100          3851.25

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    19779.65    12.19        114.37               203.68

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     2698.77     1.39         52.92               106.26

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     9636.82    39.74        135.56               471.53

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       29.24     0.14          0.31                 0.31

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

To see the summary again you can simply call `bexperiments summary -e 1708411664` with the experiment code.

### List local results

You can inspect a preview list of results via `bexperiments localresults`.

```bash
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
  -t 3600 -dt \
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_monetdb_2.log &
```

### Evaluate Results

doc_tpch_monetdb_2.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=100
    Type: tpch
    Duration: 5428s 
    Code: 1748428572
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 1000Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301220304
    datadisk:218011
    volume_size:1000G
    volume_used:213G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748428572
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301220504
    datadisk:214824
    volume_size:1000G
    volume_used:215G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748428572
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301220512
    datadisk:214824
    volume_size:1000G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748428572
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301220708
    datadisk:214824
    volume_size:1000G
    volume_used:215G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748428572

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
Pricing Summary Report (TPC-H Q1)                              611158.42            286151.76            620589.30            277486.39
Minimum Cost Supplier Query (TPC-H Q2)                          32720.03              1606.76             29610.08              1588.07
Shipping Priority (TPC-H Q3)                                    93613.18             11292.88             90184.18             13476.13
Order Priority Checking Query (TPC-H Q4)                       315089.74             11338.63            308214.83             11637.19
Local Supplier Volume (TPC-H Q5)                                12225.49             10299.41             14428.27             10367.83
Forecasting Revenue Change (TPC-H Q6)                            6984.67              6150.07              6966.54              6639.70
Forecasting Revenue Change (TPC-H Q7)                           10969.41              6246.78              9363.37              8787.82
National Market Share (TPC-H Q8)                               100155.29             34344.52             96210.85             30202.08
Product Type Profit Measure (TPC-H Q9)                          29798.06             17461.28             30413.67             17241.85
Forecasting Revenue Change (TPC-H Q10)                          63417.51             27387.35             62596.46             27098.13
Important Stock Identification (TPC-H Q11)                       5952.21              1294.63              5787.10              1244.56
Shipping Modes and Order Priority (TPC-H Q12)                    6135.55              5458.46              5466.83              4705.70
Customer Distribution (TPC-H Q13)                              288610.23            108725.76            289230.28            111199.29
Forecasting Revenue Change (TPC-H Q14)                           7200.07              7006.30              7754.60              8422.72
Top Supplier Query (TPC-H Q15)                                   9944.06              5558.80              6645.42             10622.85
Parts/Supplier Relationship (TPC-H Q16)                         14585.55             11986.39             13856.28             13092.09
Small-Quantity-Order Revenue (TPC-H Q17)                        53268.49             15339.79             48007.70             15055.13
Large Volume Customer (TPC-H Q18)                               39332.84             21194.79             39509.69             20210.96
Discounted Revenue (TPC-H Q19)                                   7337.70              6533.91              6530.23              7175.17
Potential Part Promotion (TPC-H Q20)                             9232.29              4777.49              9315.73              4893.31
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)             20137.53             17464.32             19692.88             17691.07
Global Sales Opportunity Query (TPC-H Q22)                       6544.29              7029.48              6432.72              7630.63

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0         1780.0         8.0     5625.0    7421.0
MonetDB-BHT-8-1-2-1           1.0         1780.0         8.0     5625.0    7421.0
MonetDB-BHT-8-2-1-1           1.0         1780.0         8.0     5625.0    7421.0
MonetDB-BHT-8-2-2-1           1.0         1780.0         8.0     5625.0    7421.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1          27.15
MonetDB-BHT-8-1-2-1          12.08
MonetDB-BHT-8-2-1-1          25.98
MonetDB-BHT-8-2-2-1          12.85

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           13554.19
MonetDB-BHT-8-1-2-1           31641.68
MonetDB-BHT-8-2-1-1           14145.92
MonetDB-BHT-8-2-2-1           29780.14

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count   SF  Throughput@Size
DBMS              SF  num_experiment num_client                                       
MonetDB-BHT-8-1-1 100 1              1               1771      1  100          4472.05
MonetDB-BHT-8-1-2 100 1              2                643      1  100         12317.26
MonetDB-BHT-8-2-1 100 2              1               1750      1  100          4525.71
MonetDB-BHT-8-2-2 100 2              2                644      1  100         12298.14

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1     7808.89    21.56         56.20               105.83
MonetDB-BHT-8-1-2     6435.11    25.92         89.37               178.50
MonetDB-BHT-8-2-1    14247.00    16.57         90.29               115.62
MonetDB-BHT-8-2-2     6471.31    29.86         87.50               175.82

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       29.08     0.14          0.31                 0.33
MonetDB-BHT-8-1-2       29.08     0.19          0.55                 0.58
MonetDB-BHT-8-2-1       26.05     0.01          0.32                 0.34
MonetDB-BHT-8-2-2       25.52     0.02          0.56                 0.59

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
  -t 3600 -dt \
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_monetdb_3.log &
```

### Evaluate Results

doc_tpch_monetdb_3.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=100
    Type: tpch
    Duration: 3735s 
    Code: 1748434214
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 3600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 1000Gi.
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
    disk:301220720
    datadisk:214824
    volume_size:1000G
    volume_used:210G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748434214
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301220740
    datadisk:214824
    volume_size:1000G
    volume_used:215G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748434214
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301220924
    datadisk:214824
    volume_size:1000G
    volume_used:215G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748434214
MonetDB-BHT-8-3-2 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301220924
    datadisk:214824
    volume_size:1000G
    volume_used:215G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748434214
MonetDB-BHT-8-3-3 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301220924
    datadisk:214824
    volume_size:1000G
    volume_used:215G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748434214

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
Pricing Summary Report (TPC-H Q1)                            608844.40          282261.72          512298.36          506249.69          519867.78
Minimum Cost Supplier Query (TPC-H Q2)                        29290.57            2926.62            4023.94           10621.37            7820.99
Shipping Priority (TPC-H Q3)                                  91344.59           17204.56           19286.05           19024.42           10758.94
Order Priority Checking Query (TPC-H Q4)                     305787.58           13031.13           23955.84           23516.28           22083.62
Local Supplier Volume (TPC-H Q5)                              14534.71           10078.91           13671.73           14706.04           13262.09
Forecasting Revenue Change (TPC-H Q6)                          7037.13            4732.99            6315.53            5966.08            6258.37
Forecasting Revenue Change (TPC-H Q7)                          9614.17            4291.50            9228.77           12430.23           10666.34
National Market Share (TPC-H Q8)                              94883.28           29652.77           47208.95           44226.71           46867.46
Product Type Profit Measure (TPC-H Q9)                        30483.78           17978.80           23406.14           23185.70           23486.88
Forecasting Revenue Change (TPC-H Q10)                        63242.44           27257.22           25494.39           27371.91           26465.30
Important Stock Identification (TPC-H Q11)                     5953.83            1262.94            3630.09            1825.74            1500.48
Shipping Modes and Order Priority (TPC-H Q12)                  5613.47            4944.56            8349.25            7642.35            8515.75
Customer Distribution (TPC-H Q13)                            308354.55          105699.44          109535.62          110815.17          112989.95
Forecasting Revenue Change (TPC-H Q14)                         8171.53            6894.32           10409.51            9122.42            7646.31
Top Supplier Query (TPC-H Q15)                                10480.21            6224.29           11390.89           10586.51           10576.28
Parts/Supplier Relationship (TPC-H Q16)                       14018.48           13674.34           13930.51           12454.11           11733.53
Small-Quantity-Order Revenue (TPC-H Q17)                      50353.85           15639.09           13195.09           15458.95           15809.57
Large Volume Customer (TPC-H Q18)                             40185.74           22456.12           25767.86           26680.95           27467.79
Discounted Revenue (TPC-H Q19)                                 8073.13            6854.46            7916.83            7415.78            6546.55
Potential Part Promotion (TPC-H Q20)                           9829.05            6490.36            6551.82            6489.62            6529.78
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           19769.84           16923.06           47978.09           41733.64           39603.43
Global Sales Opportunity Query (TPC-H Q22)                     6382.48            7243.76            6764.96            6351.40            6942.87

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0         1780.0         8.0     5625.0    7421.0
MonetDB-BHT-8-2-1           1.0         1780.0         8.0     5625.0    7421.0
MonetDB-BHT-8-3-1           1.0         1780.0         8.0     5625.0    7421.0
MonetDB-BHT-8-3-2           1.0         1780.0         8.0     5625.0    7421.0
MonetDB-BHT-8-3-3           1.0         1780.0         8.0     5625.0    7421.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          27.11
MonetDB-BHT-8-2-1          12.51
MonetDB-BHT-8-3-1          17.04
MonetDB-BHT-8-3-2          17.44
MonetDB-BHT-8-3-3          16.35

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           13528.13
MonetDB-BHT-8-2-1           30412.81
MonetDB-BHT-8-3-1           21722.15
MonetDB-BHT-8-3-2           21652.10
MonetDB-BHT-8-3-3           23095.41

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MonetDB-BHT-8-1 100 1              1               1766      1  100          4484.71
MonetDB-BHT-8-2 100 1              2                641      1  100         12355.69
MonetDB-BHT-8-3 100 1              3                968      3  100         24545.45

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     6788.75    19.81         53.28               106.00
MonetDB-BHT-8-2     5619.66    22.30         85.64               178.55
MonetDB-BHT-8-3    12307.41    27.54        137.00               328.86

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       26.82     0.06          0.31                 0.33
MonetDB-BHT-8-2       26.82     0.02          0.54                 0.57
MonetDB-BHT-8-3       56.88     0.46          1.00                 1.04

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

