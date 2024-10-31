# Benchmark: TPC-DS

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TPC-DS does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients for the loading test and the throughput test [2].

This example shows how to benchmark 99 reading queries Q1-Q99 derived from TPC-DS in MonetDB and PostgreSQL.

> The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS Specification.

1. Official TPC-DS benchmark - http://www.tpc.org/tpcds
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Perform Benchmark - Power Test

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

Example:
```bash
nohup python tpcds.py -ms 4 -dt -tr \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_compare.log &
```

This
* starts a clean instance of PostgreSQL, MonetDB, MySQL and MariaDB (at the same time, `-ms`)
  * data directory inside a Docker container
  * with a maximum of 1 DBMS per time (`-ms`)
* creates TPC-DS schema in each database
* starts 8 loader pods per DBMS (`-nlp`)
  * with a data generator (init) container each
    * each generating a portion of TPC-DS data of scaling factor 1 (`-sf`)
    * storing the data in a distributed filesystem (shared disk)
    * if data is already present: do nothing
  * with a loading container each
    * importing TPC-DS data from the distributed filesystem
    * MySQL: only one pod active and it loads with 8 threads (`-nlt`)
* creates contraints (`-ic`) and indexes (`-ii`) and updates table statistics (`-is`) in each DBMS after ingestion
* runs 1 stream of TPC-DS queries per DBMS
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
You can find the number also in the output of `tpcds.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1706255897` (removes everything that is related to experiment `1706255897`).

## Evaluate Results

At the end of a benchmark you will see a summary like

```bash
## Show Summary
```

This gives a survey about the errors and warnings (result set mismatch) and the latencies of execution per query.
Moreover the loading times (schema creation, ingestion and indexing), the geometric mean of query execution times and the TPC-DS metrics power and throughput are reported.
Please note that the results are not suitable for being published as official TPC-DS results.
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

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpcds

### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/tpcds

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python tpcds.py -h`

```bash
usage: tpcds.py [-h] [-aws] [-dbms {PostgreSQL,MonetDB,MySQL,MariaDB}] [-lit LIMIT_IMPORT_TABLE] [-db] [-sl] [-cx CONTEXT] [-e EXPERIMENT] [-m] [-mc] [-ms MAX_SUT] [-dt] [-nr NUM_RUN] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nls NUM_LOADING_SPLIT]
                [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS] [-nbp NUM_BENCHMARKING_PODS] [-nbt NUM_BENCHMARKING_THREADS] [-sf SCALING_FACTOR] [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE]
                [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING] [-rnb REQUEST_NODE_BENCHMARKING] [-tr] [-ii] [-ic] [-is] [-rcp] [-shq]
                {profiling,run,start,load,empty,summary}

Performs a TPC-DS experiment. Data is generated and imported into a DBMS from a distributed filesystem (shared disk).

positional arguments:
  {profiling,run,start,load,empty,summary}
                        profile the import or run the TPC-DS queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms {PostgreSQL,MonetDB,MySQL,MariaDB}, --dbms {PostgreSQL,MonetDB,MySQL,MariaDB}
                        DBMS
  -lit LIMIT_IMPORT_TABLE, --limit-import-table LIMIT_IMPORT_TABLE
                        limit import to one table, name of this table
  -db, --debug          dump debug informations
  -sl, --skip-loading   do not ingest, start benchmarking immediately
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
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_monitoring.log &
```

If monitoring is activated, the summary also contains a section like
```bash
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 726s 
    Code: 1730389898
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
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
    disk:260978700
    datadisk:6065900
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                  62.97
TPC-DS Q2                 534.62
TPC-DS Q3                  44.31
TPC-DS Q4                3845.58
TPC-DS Q5                 764.13
TPC-DS Q6                 244.52
TPC-DS Q7                 100.44
TPC-DS Q8                 180.42
TPC-DS Q9                 140.16
TPC-DS Q10                149.38
TPC-DS Q11               1797.21
TPC-DS Q12                 49.17
TPC-DS Q13                170.82
TPC-DS Q14a+b            6787.00
TPC-DS Q15                 49.01
TPC-DS Q16                317.06
TPC-DS Q17                434.33
TPC-DS Q18                305.86
TPC-DS Q19                 91.21
TPC-DS Q20                 60.16
TPC-DS Q21                136.73
TPC-DS Q22               2989.99
TPC-DS Q23a+b            8791.66
TPC-DS Q24a+b             356.62
TPC-DS Q25                334.82
TPC-DS Q26                 70.04
TPC-DS Q27                357.87
TPC-DS Q28                173.86
TPC-DS Q29                332.73
TPC-DS Q30                 29.23
TPC-DS Q31                539.12
TPC-DS Q32                 39.95
TPC-DS Q33                 47.61
TPC-DS Q34                 55.19
TPC-DS Q35                192.41
TPC-DS Q37                 77.10
TPC-DS Q38                633.56
TPC-DS Q39a+b            3954.81
TPC-DS Q40                 91.26
TPC-DS Q41                 13.00
TPC-DS Q42                 35.87
TPC-DS Q43                135.63
TPC-DS Q44                106.18
TPC-DS Q45                 36.34
TPC-DS Q46                 70.02
TPC-DS Q47                623.51
TPC-DS Q48                133.55
TPC-DS Q49                274.97
TPC-DS Q50                210.24
TPC-DS Q51               1795.68
TPC-DS Q52                 36.86
TPC-DS Q53                 53.48
TPC-DS Q54                125.95
TPC-DS Q55                 28.33
TPC-DS Q56                 54.86
TPC-DS Q57                179.49
TPC-DS Q58                140.61
TPC-DS Q59                256.00
TPC-DS Q60                 56.49
TPC-DS Q61                 61.78
TPC-DS Q62                 52.96
TPC-DS Q63                 54.18
TPC-DS Q64               1100.35
TPC-DS Q65                391.17
TPC-DS Q66                271.59
TPC-DS Q67               2353.67
TPC-DS Q68                 79.73
TPC-DS Q69                112.86
TPC-DS Q71                 63.78
TPC-DS Q72                288.28
TPC-DS Q73                 50.75
TPC-DS Q74                537.08
TPC-DS Q75               2449.19
TPC-DS Q76                 71.73
TPC-DS Q77                173.96
TPC-DS Q78               3092.98
TPC-DS Q79                 88.23
TPC-DS Q80               2664.39
TPC-DS Q81                 53.47
TPC-DS Q82                375.68
TPC-DS Q83                 30.70
TPC-DS Q84                 16.77
TPC-DS Q85                 78.00
TPC-DS Q87                782.68
TPC-DS Q88                184.58
TPC-DS Q89                 82.09
TPC-DS Q90                 21.34
TPC-DS Q91                 26.00
TPC-DS Q92                 26.51
TPC-DS Q93                405.65
TPC-DS Q94                 65.22
TPC-DS Q95                176.05
TPC-DS Q96                 25.71
TPC-DS Q97                816.58
TPC-DS Q98                 86.52
TPC-DS Q99                100.61

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          289.0         8.0      108.0     414.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.18

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           63256.32

### Throughput@Size
                                              time [s]  count  SF  Throughput@Size [~GB/h]
DBMS            SF num_experiment num_client                                              
MonetDB-BHT-8-1 3  1              1                 70      1   3                  3394.29

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      709.64     2.26          2.18                 8.71

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       52.21     0.28          1.04                 2.26

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      353.58        0          4.68                10.47

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       13.68        0          0.24                 0.26

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
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

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

Example:
```bash
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -nc 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_throughput.log &
```

This runs 3 streams (`-ne`), the first one as a single stream and the following 2 in parallel.

```bash
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 542s 
    Code: 1730317653
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:258056336
    datadisk:3146824
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:258107624
    datadisk:3198112
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:258107624
    datadisk:3198112
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-2-2
TPC-DS Q1                  52.98              42.35              40.88
TPC-DS Q2                 190.06             139.34             138.69
TPC-DS Q3                  23.93              48.12              17.95
TPC-DS Q4                1175.21            1140.20            1188.24
TPC-DS Q5                 276.22             232.87             264.24
TPC-DS Q6                  72.40              61.95              71.45
TPC-DS Q7                  61.08              46.80              51.83
TPC-DS Q8                  34.93              33.47              40.64
TPC-DS Q9                  57.54              57.35              56.31
TPC-DS Q10                 60.09              30.39              42.65
TPC-DS Q11                610.81             552.57             595.01
TPC-DS Q12                 21.66              18.52              19.45
TPC-DS Q13                103.69              92.67              88.23
TPC-DS Q14a+b            2372.95            2081.48            2055.55
TPC-DS Q15                 32.83              21.10              22.20
TPC-DS Q16                 52.66              33.67              34.08
TPC-DS Q17                162.18             100.17             106.85
TPC-DS Q18                141.12              98.36              98.21
TPC-DS Q19                 36.94              36.81              37.06
TPC-DS Q20                 27.46              25.26              25.30
TPC-DS Q21                 76.70              52.65              61.83
TPC-DS Q22               1047.68            1029.34             983.00
TPC-DS Q23a+b            2521.53            2530.04            2555.41
TPC-DS Q24a+b             141.40             136.92             138.26
TPC-DS Q25                105.49              96.44              95.33
TPC-DS Q26                 59.91              57.38              60.22
TPC-DS Q27                146.26             117.09             104.31
TPC-DS Q28                 72.42              66.55              76.98
TPC-DS Q29                104.95             102.30              92.19
TPC-DS Q30                 26.63              20.24              21.31
TPC-DS Q31                175.30             129.30             144.72
TPC-DS Q32                 17.12              17.81              17.13
TPC-DS Q33                 23.13              25.71              24.92
TPC-DS Q34                 26.40              23.09              24.18
TPC-DS Q35                 71.55              68.59              71.29
TPC-DS Q37                 64.60              44.50              62.91
TPC-DS Q38                216.91             173.32             185.62
TPC-DS Q39a+b            1226.89            1071.67            1005.83
TPC-DS Q40                 61.56              37.21              42.41
TPC-DS Q41                  8.13               8.31               8.87
TPC-DS Q42                 22.86              18.59              24.70
TPC-DS Q43                 58.19              68.64              59.22
TPC-DS Q44                 30.47              31.20              31.79
TPC-DS Q45                 23.19              22.96              26.50
TPC-DS Q46                 43.35              35.89              38.12
TPC-DS Q47                286.02             264.16             236.53
TPC-DS Q48                103.14              85.05              92.22
TPC-DS Q49                127.83              86.84              96.73
TPC-DS Q50                100.18              95.28             101.64
TPC-DS Q51                639.18             631.49             601.57
TPC-DS Q52                 19.63              22.54              19.85
TPC-DS Q53                 26.74              26.36              27.12
TPC-DS Q54                 53.71              22.20              25.44
TPC-DS Q55                 15.52              17.08              16.03
TPC-DS Q56                 28.20              24.24              24.52
TPC-DS Q57                 95.36              98.06              96.13
TPC-DS Q58                 50.01              54.38              44.99
TPC-DS Q59                 99.74              97.03              94.58
TPC-DS Q60                 27.31              31.31              63.72
TPC-DS Q61                 31.10              34.30              32.59
TPC-DS Q62                 31.76              23.92              36.64
TPC-DS Q63                 26.42              26.93              28.43
TPC-DS Q64                253.44             265.37             257.72
TPC-DS Q65                 92.16              94.19              99.27
TPC-DS Q66                120.74             114.30             124.59
TPC-DS Q67                690.45             685.76             649.91
TPC-DS Q68                 50.67              35.02              36.50
TPC-DS Q69                 40.58              40.51              36.91
TPC-DS Q71                 33.21              32.97              27.77
TPC-DS Q72                160.02             142.97             148.49
TPC-DS Q73                 23.47              24.01              24.50
TPC-DS Q74                602.89             578.14             585.55
TPC-DS Q75                671.14             646.76             679.46
TPC-DS Q76                 35.84              38.33              35.80
TPC-DS Q77                 69.53              61.24              48.26
TPC-DS Q78                849.84             770.34             807.75
TPC-DS Q79                 40.95              48.63              40.12
TPC-DS Q80                599.98             476.06             473.29
TPC-DS Q81                 30.89              29.07              40.99
TPC-DS Q82                150.65              49.78              50.42
TPC-DS Q83                 16.66              16.59              24.88
TPC-DS Q84                 14.38              14.18              16.13
TPC-DS Q85                 36.15              69.79              35.17
TPC-DS Q87                244.91             246.37             257.06
TPC-DS Q88                 89.78              83.52              90.83
TPC-DS Q89                 39.14              48.36              41.03
TPC-DS Q90                 18.09              12.22              15.77
TPC-DS Q91                 23.62              25.50              24.50
TPC-DS Q92                 16.18              14.60              16.56
TPC-DS Q93                 82.97              87.75              91.61
TPC-DS Q94                 17.78              17.50              16.94
TPC-DS Q95                121.50             132.12             129.57
TPC-DS Q96                 16.20              13.04              17.24
TPC-DS Q97                213.12             224.09             223.01
TPC-DS Q98                 40.63              45.60              39.48
TPC-DS Q99                 61.33              52.73              59.19

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          113.0         9.0       41.0     171.0
MonetDB-BHT-8-2-1           1.0          113.0         9.0       41.0     171.0
MonetDB-BHT-8-2-2           1.0          113.0         9.0       41.0     171.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.08
MonetDB-BHT-8-2-1           0.08
MonetDB-BHT-8-2-2           0.08

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           47181.62
MonetDB-BHT-8-2-1           52119.86
MonetDB-BHT-8-2-2           50777.18

### Throughput@Size
                                              time [s]  count  SF  Throughput@Size [~GB/h]
DBMS            SF num_experiment num_client                                              
MonetDB-BHT-8-1 1  1              1                 30      1   1                  2640.00
MonetDB-BHT-8-2 1  1              2                 31      2   1                  5109.68

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 2]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 2]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```

All executions use the same database, so loading times are the same.

Per default, all 3 streams use the same random parameters (like YEAR in Q1) and run in ordering Q1-Q99.
You can change this via
* `-rcp`: Each stream has it's own random parameters
* `-shq`: Use the ordering per stream as required by the TPC-DS specification

## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_storage.log &
```
The following status shows we have a volumes of type `shared`.
Every experiment running TPC-DS of SF=1 at MonetDB will take the database from this volume and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of MonetDB mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                 | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+=========================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-monetdb-tpcds-1         | monetdb         | tpcds-1      | True         |               151 | MonetDB    | shared               | 30Gi      | Bound    | 30G    | 2.0G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpcds-3         | monetdb         | tpcds-3      | True         |               393 | MonetDB    | shared               | 100Gi     | Bound    | 100G   | 5.4G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpcds-100       | monetdb         | tpcds-100    | True         |              4019 | MonetDB    | shared               | 300Gi     | Bound    | 300G   | 156G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+

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
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 733s 
    Code: 1730318343
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Benchmark is limited to DBMS ['MonetDB'].
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
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254909672
    datadisk:3147808
    volume_size:30G
    volume_used:2.2G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254909612
    datadisk:3175842
    volume_size:30G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q1                    47.78               804.64
TPC-DS Q2                   176.11              1808.03
TPC-DS Q3                    24.95               728.48
TPC-DS Q4                  1151.49              3334.71
TPC-DS Q5                   245.56              1288.57
TPC-DS Q6                    82.69               304.22
TPC-DS Q7                    60.65              1039.59
TPC-DS Q8                    39.61               177.67
TPC-DS Q9                    59.75               424.99
TPC-DS Q10                   85.94              1292.05
TPC-DS Q11                  580.94               614.35
TPC-DS Q12                   23.01               152.45
TPC-DS Q13                   93.65               179.10
TPC-DS Q14a+b              2322.47              2572.74
TPC-DS Q15                   29.40               161.59
TPC-DS Q16                   52.14               333.63
TPC-DS Q17                  145.47               443.85
TPC-DS Q18                  117.39               495.14
TPC-DS Q19                   38.25               110.05
TPC-DS Q20                   28.03                27.20
TPC-DS Q21                   70.50              2366.47
TPC-DS Q22                 1123.02              1169.92
TPC-DS Q23a+b              1963.65              1971.61
TPC-DS Q24a+b               144.61               298.94
TPC-DS Q25                  133.66               100.05
TPC-DS Q26                   69.29                24.05
TPC-DS Q27                  118.69               121.15
TPC-DS Q28                   68.29               217.77
TPC-DS Q29                   85.45                84.76
TPC-DS Q30                   19.98               129.67
TPC-DS Q31                  165.31               148.71
TPC-DS Q32                   17.55                23.70
TPC-DS Q33                   24.19                77.99
TPC-DS Q34                   26.63               147.63
TPC-DS Q35                   66.32                64.52
TPC-DS Q37                   62.20                70.20
TPC-DS Q38                  194.88               192.19
TPC-DS Q39a+b              1154.50              1121.81
TPC-DS Q40                   54.73                74.71
TPC-DS Q41                    8.51                 8.23
TPC-DS Q42                   22.38                23.45
TPC-DS Q43                   45.63                48.67
TPC-DS Q44                   65.40                67.36
TPC-DS Q45                   26.12                79.11
TPC-DS Q46                   38.19                70.33
TPC-DS Q47                  213.00               255.35
TPC-DS Q48                   94.54                88.56
TPC-DS Q49                  124.85               256.06
TPC-DS Q50                  102.91               299.47
TPC-DS Q51                  609.65               595.76
TPC-DS Q52                   19.56                18.57
TPC-DS Q53                   28.81                26.18
TPC-DS Q54                   67.32                66.22
TPC-DS Q55                   15.89                15.18
TPC-DS Q56                   28.47                21.27
TPC-DS Q57                   89.33               127.61
TPC-DS Q58                   55.47                60.62
TPC-DS Q59                  104.04               101.17
TPC-DS Q60                   23.49                22.94
TPC-DS Q61                   32.23               118.65
TPC-DS Q62                   32.36                66.71
TPC-DS Q63                   26.20                29.63
TPC-DS Q64                  263.89               709.22
TPC-DS Q65                   85.92               118.04
TPC-DS Q66                  114.45               214.35
TPC-DS Q67                  769.34               681.86
TPC-DS Q68                   50.03               237.85
TPC-DS Q69                   42.90                39.65
TPC-DS Q71                   31.25                30.64
TPC-DS Q72                  154.49               223.55
TPC-DS Q73                   24.49                24.09
TPC-DS Q74                  191.39               183.01
TPC-DS Q75                  681.59              1605.93
TPC-DS Q76                   34.45                36.41
TPC-DS Q77                   56.80                58.22
TPC-DS Q78                  806.57               791.53
TPC-DS Q79                   41.24               101.68
TPC-DS Q80                  476.77               419.02
TPC-DS Q81                   27.82               114.48
TPC-DS Q82                   54.60                62.58
TPC-DS Q83                   17.71                22.44
TPC-DS Q84                   34.60                64.68
TPC-DS Q85                   36.41               105.51
TPC-DS Q87                  245.82               272.06
TPC-DS Q88                   87.82                88.24
TPC-DS Q89                   42.74                39.45
TPC-DS Q90                   13.10                17.20
TPC-DS Q91                   23.90                74.34
TPC-DS Q92                   15.01                14.33
TPC-DS Q93                   85.81                84.17
TPC-DS Q94                   18.27                17.01
TPC-DS Q95                  120.79               149.38
TPC-DS Q96                   14.24                13.25
TPC-DS Q97                  207.16               936.20
TPC-DS Q98                   49.49                48.36
TPC-DS Q99                   62.02                62.00

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0           99.0         4.0       39.0     151.0
MonetDB-BHT-8-2-1-1           1.0           99.0         4.0       39.0     151.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.08
MonetDB-BHT-8-2-1-1           0.15

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           48527.46
MonetDB-BHT-8-2-1-1           26455.04

### Throughput@Size
                                                time [s]  count  SF  Throughput@Size [~GB/h]
DBMS              SF num_experiment num_client                                              
MonetDB-BHT-8-1-1 1  1              1                 29      1   1                  2731.03
MonetDB-BHT-8-2-1 1  2              1                 77      1   1                  1028.57

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1], [1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1], [1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```


The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.

# Example: MonetDB TPC-DS@100

## First Test Run

This also sets up the database:

```bash
nohup python tpcds.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 1200 -dt \
  -rst shared -rss 300Gi \
  run &>$LOG_DIR/doc_tpcds_monetdb_1.log &
```

## Perform Benchmark - Power Test

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other (`-ne 1,1`), and shut down the DBMS.
This is repeated 2 times (`-nc`).

```bash
nohup python tpcds.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 2 -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 1200 -dt \
  -rst shared -rss 300Gi \
  run &>$LOG_DIR/doc_tpcds_monetdb_2.log &
```

## Perform Benchmark - Throughput Test

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other, and then a throughput test with 3 parallel driver (`-ne 1,1,3`). and shut down the DBMS.


```bash
nohup python tpcds.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1,1,3 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 1200 -dt \
  -rst shared -rss 300Gi \
  run &>$LOG_DIR/doc_tpcds_monetdb_3.log &
```

