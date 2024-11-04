# Benchmark: TPC-DS

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TPC-DS does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients for the loading test and the throughput test [2].

This example shows how to benchmark 99 reading queries Q1-Q99 derived from TPC-DS in MonetDB, PostgreSQL, MySQL and MariaDB.

> The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS Specification.

In particular we had to apply changes, because
* MySQL and MariaDB do not have a FULL OUTER JOIN
* MySQL and MariaDB do CASTing to INTEGER differently

See [query file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/tpcds/queries-tpcds.config) for all details.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

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
  -t 1200 \
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

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 13657s 
    Code: 1730390884
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
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
    disk:259224248
    datadisk:4310940
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:272072600
    datadisk:3147080
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:269644004
    datadisk:8487676
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:272072600
    datadisk:5363964
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
            MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q4               False              False             False                  True
TPC-DS Q16               True              False             False                 False
TPC-DS Q27               True              False             False                 False
TPC-DS Q35              False              False             False                  True
TPC-DS Q51               True              False              True                 False
TPC-DS Q54              False              False              True                 False
TPC-DS Q72               True              False             False                 False
TPC-DS Q74              False              False             False                  True
TPC-DS Q94               True              False             False                 False
TPC-DS Q95               True              False             False                 False
TPC-DS Q97               True              False              True                 False

### Warnings (result mismatch)
            MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q3               False               True              True                  True
TPC-DS Q4               False              False              True                 False
TPC-DS Q5               False               True              True                  True
TPC-DS Q6               False               True              True                  True
TPC-DS Q7               False               True              True                 False
TPC-DS Q9               False              False              True                 False
TPC-DS Q10              False              False              True                 False
TPC-DS Q11              False               True              True                 False
TPC-DS Q12              False              False              True                 False
TPC-DS Q13              False              False              True                 False
TPC-DS Q15              False               True              True                  True
TPC-DS Q16              False               True              True                  True
TPC-DS Q17              False              False              True                 False
TPC-DS Q18              False               True              True                  True
TPC-DS Q19              False               True              True                  True
TPC-DS Q20              False              False              True                 False
TPC-DS Q21              False               True              True                  True
TPC-DS Q22              False               True              True                  True
TPC-DS Q25              False              False              True                 False
TPC-DS Q26              False              False              True                 False
TPC-DS Q27              False               True              True                  True
TPC-DS Q28              False              False              True                 False
TPC-DS Q29              False              False              True                 False
TPC-DS Q30              False              False              True                 False
TPC-DS Q31              False              False              True                 False
TPC-DS Q32              False              False              True                 False
TPC-DS Q33              False              False              True                  True
TPC-DS Q35              False              False              True                 False
TPC-DS Q38              False               True              True                  True
TPC-DS Q40              False              False              True                 False
TPC-DS Q42              False               True              True                  True
TPC-DS Q44              False               True              True                  True
TPC-DS Q45              False               True              True                  True
TPC-DS Q47              False               True              True                 False
TPC-DS Q48              False               True              True                  True
TPC-DS Q49              False              False              True                 False
TPC-DS Q50              False              False              True                 False
TPC-DS Q51              False               True             False                  True
TPC-DS Q52              False               True              True                  True
TPC-DS Q53              False              False              True                 False
TPC-DS Q55              False               True              True                  True
TPC-DS Q56              False              False              True                  True
TPC-DS Q57              False              False              True                 False
TPC-DS Q60              False              False              True                 False
TPC-DS Q61              False               True             False                  True
TPC-DS Q62              False               True              True                  True
TPC-DS Q63              False              False              True                 False
TPC-DS Q64              False               True              True                  True
TPC-DS Q65              False              False              True                  True
TPC-DS Q66              False               True              True                  True
TPC-DS Q67              False              False              True                  True
TPC-DS Q69              False              False              True                 False
TPC-DS Q71              False               True              True                  True
TPC-DS Q72              False               True              True                  True
TPC-DS Q74              False              False              True                 False
TPC-DS Q75              False               True              True                  True
TPC-DS Q76              False              False              True                 False
TPC-DS Q77              False              False              True                 False
TPC-DS Q78              False               True              True                  True
TPC-DS Q79              False               True              True                  True
TPC-DS Q80              False               True              True                  True
TPC-DS Q81              False              False              True                 False
TPC-DS Q82              False              False              True                 False
TPC-DS Q83              False               True              True                  True
TPC-DS Q84              False               True              True                  True
TPC-DS Q87              False               True              True                  True
TPC-DS Q88              False              False              True                 False
TPC-DS Q89              False              False              True                 False
TPC-DS Q90              False              False              True                 False
TPC-DS Q91              False               True              True                  True
TPC-DS Q92              False              False              True                 False
TPC-DS Q93              False              False              True                  True
TPC-DS Q94              False               True              True                  True
TPC-DS Q95              False               True              True                  True
TPC-DS Q96              False               True              True                  True
TPC-DS Q97              False               True             False                  True
TPC-DS Q98              False               True              True                 False
TPC-DS Q99              False               True              True                  True

### Latency of Timer Execution [ms]
DBMS           MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q1                  93.62              53.31             86.46                 48.16
TPC-DS Q2               15874.44             162.66             13.88                880.88
TPC-DS Q3                  90.69              25.10              3.28                239.09
TPC-DS Q5               31156.08             303.34             11.25               1369.51
TPC-DS Q6                2938.08              72.35              2.63             198592.92
TPC-DS Q7               17480.89              57.07              3.10                961.64
TPC-DS Q8                 379.16              38.10              3.20                498.10
TPC-DS Q9               13426.27              56.93              2.90               6251.33
TPC-DS Q10              21616.99              61.92              3.24               1973.41
TPC-DS Q11              73637.89             589.85              5.86             425524.32
TPC-DS Q12                997.62              20.33              1.80                129.91
TPC-DS Q13               3297.02             108.81              2.71                543.17
TPC-DS Q14a+b          256000.82            2153.81             17.57              36793.27
TPC-DS Q15               8727.57              31.46              1.50                241.33
TPC-DS Q17               2708.11             154.98              2.09                629.51
TPC-DS Q18               9615.23             139.64              1.91                662.08
TPC-DS Q19                 51.25              37.07              1.66                315.19
TPC-DS Q20               1737.43              28.36              1.50                179.67
TPC-DS Q21              78868.66              79.31              2.52                655.25
TPC-DS Q22                313.63            1113.05              1.25              10085.88
TPC-DS Q23a+b          308672.84            2814.62              7.46              13954.40
TPC-DS Q24a+b            7784.51             161.37              5.11                895.64
TPC-DS Q25               2420.90             105.43              1.72                635.74
TPC-DS Q26               8913.09              60.86              1.40               2247.90
TPC-DS Q28              10148.67              73.72              2.41               2156.65
TPC-DS Q29               2338.82              95.62              1.76                424.96
TPC-DS Q30               1189.47              28.51              2.56              27791.55
TPC-DS Q31              44120.71             157.34              5.17              18289.36
TPC-DS Q32                 31.09              23.71              1.61              36745.84
TPC-DS Q33              17629.99              23.54              3.29               1956.77
TPC-DS Q34               3377.11              29.79              1.67                 57.05
TPC-DS Q37              13635.77              65.83              1.33                761.84
TPC-DS Q38              26939.53             213.15              1.46               2719.32
TPC-DS Q39a+b          314001.80            1381.27              4.84               7467.58
TPC-DS Q40                732.05              55.97              1.64                305.58
TPC-DS Q41               1830.68               8.63              1.77               3690.84
TPC-DS Q42                239.26              18.98              1.20                323.05
TPC-DS Q43              11722.33              43.84              1.26                 56.34
TPC-DS Q44               4218.80              57.89              1.87               1421.14
TPC-DS Q45               6506.75              25.72              1.37                186.34
TPC-DS Q46               6188.09              38.62              1.55                 57.75
TPC-DS Q47              61018.14             233.42              3.86               3894.85
TPC-DS Q48               6424.61              92.59              1.40                719.91
TPC-DS Q49                355.28             118.93              2.99               1220.11
TPC-DS Q50               2182.99             108.75              1.71                114.96
TPC-DS Q52                234.68              20.55              1.14                311.10
TPC-DS Q53                622.93              27.34              1.57                404.54
TPC-DS Q55                238.61              15.47              0.99                312.81
TPC-DS Q56               2151.49              29.81              2.66             263283.76
TPC-DS Q57              31375.15             103.53              3.39               1933.91
TPC-DS Q58              22674.25              55.65              2.90                824.76
TPC-DS Q59              38605.98             102.15              2.51               1129.96
TPC-DS Q60               4424.49              24.36              2.58               8870.91
TPC-DS Q61               1624.88              32.15              1.75                305.36
TPC-DS Q62               7321.86              32.71              2.16                274.92
TPC-DS Q63                515.90              27.18              1.64                369.20
TPC-DS Q64               2101.21             286.95              6.64               1297.21
TPC-DS Q65              22528.18              96.03              1.80               1471.58
TPC-DS Q66              14167.07             123.20              4.42                637.49
TPC-DS Q67              27971.61             668.94              1.69               2897.00
TPC-DS Q68               6191.93              36.29              1.70                 56.17
TPC-DS Q69              22227.18              37.74              1.41                565.30
TPC-DS Q71              19305.23              29.87              1.46               5424.10
TPC-DS Q73               3345.58              23.51              1.46                 57.00
TPC-DS Q75               5576.00             667.35              3.14               2397.57
TPC-DS Q76               1531.84              35.88              1.60                686.03
TPC-DS Q77              24200.99              57.25              4.01                886.87
TPC-DS Q78              45025.15             772.71              2.53               4071.07
TPC-DS Q79               2546.83              35.25              1.83                755.86
TPC-DS Q80               2207.55             429.57              3.81               6700.83
TPC-DS Q81               2971.97              34.60              1.83             120537.16
TPC-DS Q82              13614.41              79.41              1.47                857.28
TPC-DS Q83               3419.13              19.09              2.63                274.90
TPC-DS Q84                165.04              31.06              4.84                 92.41
TPC-DS Q85                349.15              39.20              2.21                176.95
TPC-DS Q87              27065.55             263.45              1.67               2663.61
TPC-DS Q88              25044.69              94.80              4.66               7171.83
TPC-DS Q89                154.08              39.15              1.88                264.89
TPC-DS Q90                400.84              18.09              1.58                249.05
TPC-DS Q91               1613.68              24.12              1.93                 79.44
TPC-DS Q92                 19.39              17.29              1.44               4405.16
TPC-DS Q93                 99.48             101.48              1.48                136.08
TPC-DS Q96               2227.12              13.80              1.17                286.26
TPC-DS Q98               3439.88              39.91              1.54                298.20
TPC-DS Q99              16802.98              58.95              1.53                402.79

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1              1.0         1028.0         4.0     7044.0    8085.0
MonetDB-BHT-8-1-1              1.0          119.0         9.0       42.0     184.0
MySQL-BHT-64-1-1               1.0           12.0         8.0      242.0     275.0
PostgreSQL-BHT-8-1-1           1.0          136.0         1.0       52.0     200.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              3.90
MonetDB-BHT-8-1-1              0.08
MySQL-BHT-64-1-1               0.00
PostgreSQL-BHT-8-1-1           1.08

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1                926.35
MonetDB-BHT-8-1-1              51394.70
MySQL-BHT-64-1-1             1492286.07
PostgreSQL-BHT-8-1-1            3377.50

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
MariaDB-BHT-8-1    1  1              1               4439      1   1                    17.84
MonetDB-BHT-8-1    1  1              1                 33      1   1                  2400.00
MySQL-BHT-64-1     1  1              1                  3      1   1                 26400.00
PostgreSQL-BHT-8-1 1  1              1               3099      1   1                    25.56

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
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
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

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

This example shows how to run Q1-Q99 derived from TPC-DS in MonetDB at SF=100.
It covers the power and the throughput test.
The refresh stream is not included.

> The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS specification.

Official TPC-DS benchmark - http://www.tpc.org/tpcds

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**



## Generate and Load Data

At first we generate TPC-DS data at SF=100 (`-sf`) with 8 parallel generators (`-nlp`).
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


## Status Database and Benchmark

You can watch the status of experiments via `bexperiments status`.

In the following example output we see all components of bexhoma are up and running.
The cluster stores a MonetDB database corresponding to TPC-DS of SF=100.
The disk is of storageClass shared and of size 300Gi and 156G of that space is used.
It took about 4000s to build this database.
Currently no DBMS is running.

```
Dashboard: Running
Message Queue: Running
Data directory: Running
Result directory: Running
Cluster Prometheus: Running
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                 | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+=========================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-monetdb-tpcds-100       | monetdb         | tpcds-100    | True         |              4019 | MonetDB    | shared               | 300Gi     | Bound    | 300G   | 156G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

## Summary of Results

At the end of a benchmark you will see a summary like

```bash
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 9730s 
    Code: 1730405979
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
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
    disk:254913816
    datadisk:153205046
    volume_size:300G
    volume_used:147G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                8487.85
TPC-DS Q2              151923.88
TPC-DS Q3                 905.48
TPC-DS Q4              254499.90
TPC-DS Q5               62567.55
TPC-DS Q6               11580.69
TPC-DS Q7                1386.00
TPC-DS Q8                4412.06
TPC-DS Q9                1997.43
TPC-DS Q10               2133.16
TPC-DS Q11              82401.02
TPC-DS Q12                898.62
TPC-DS Q13               2191.91
TPC-DS Q14a+b          324098.77
TPC-DS Q15               1846.92
TPC-DS Q16               7825.79
TPC-DS Q17              54326.28
TPC-DS Q18               9313.78
TPC-DS Q19               3102.17
TPC-DS Q20                668.31
TPC-DS Q21                924.07
TPC-DS Q22              67826.67
TPC-DS Q23a+b         3093870.15
TPC-DS Q24a+b           10940.12
TPC-DS Q25              17420.76
TPC-DS Q26                973.29
TPC-DS Q27              13031.49
TPC-DS Q28               7427.71
TPC-DS Q29              14588.75
TPC-DS Q30                792.23
TPC-DS Q31              19072.92
TPC-DS Q32                641.79
TPC-DS Q33               6272.47
TPC-DS Q34               1787.43
TPC-DS Q35               7229.82
TPC-DS Q37               7075.80
TPC-DS Q38              27739.19
TPC-DS Q39a+b           72942.27
TPC-DS Q40               3317.84
TPC-DS Q41                176.37
TPC-DS Q42               2202.22
TPC-DS Q43                667.64
TPC-DS Q44               1391.02
TPC-DS Q45                737.27
TPC-DS Q46               1637.75
TPC-DS Q47               6753.22
TPC-DS Q48               2715.50
TPC-DS Q49              10936.67
TPC-DS Q50               1829.45
TPC-DS Q51              46890.66
TPC-DS Q52               2276.80
TPC-DS Q53               2243.95
TPC-DS Q54               4364.62
TPC-DS Q55                377.10
TPC-DS Q56               1807.07
TPC-DS Q57               1117.86
TPC-DS Q58               4742.87
TPC-DS Q59              11487.65
TPC-DS Q60               1415.10
TPC-DS Q61                717.52
TPC-DS Q62                755.90
TPC-DS Q63                955.24
TPC-DS Q64              46849.52
TPC-DS Q65              23937.75
TPC-DS Q66               4750.16
TPC-DS Q67             105741.06
TPC-DS Q68               5980.62
TPC-DS Q69               2460.54
TPC-DS Q71               1322.11
TPC-DS Q72              25515.56
TPC-DS Q73                325.28
TPC-DS Q74              24674.21
TPC-DS Q75             123299.04
TPC-DS Q76              14956.14
TPC-DS Q77               7376.96
TPC-DS Q78             176943.68
TPC-DS Q79               5530.19
TPC-DS Q80             124497.51
TPC-DS Q81                784.88
TPC-DS Q82              57358.76
TPC-DS Q83                952.67
TPC-DS Q84                293.56
TPC-DS Q85               1128.16
TPC-DS Q87              53821.10
TPC-DS Q88               5310.08
TPC-DS Q89               1958.66
TPC-DS Q90                308.85
TPC-DS Q91                 80.71
TPC-DS Q92               1433.28
TPC-DS Q93              18714.89
TPC-DS Q94               1680.08
TPC-DS Q95              18150.04
TPC-DS Q96                356.39
TPC-DS Q97              41533.27
TPC-DS Q98               2601.72
TPC-DS Q99               1411.17

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           0.0         1435.0         7.0     2616.0    4066.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           5.36

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1            68546.5

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               5413      1  100                  1463.14

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    20953.14    16.82         22.09               126.44

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      2329.5     1.03          41.0                 84.3

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    20866.68    24.86         148.0               315.74

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       50.35     0.09          0.36                 0.37

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

### Evaluate Results

```bash
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 19958s 
    Code: 1730416121
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
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
    disk:254914096
    datadisk:162394763
    volume_size:300G
    volume_used:155G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254914264
    datadisk:153668365
    volume_size:300G
    volume_used:148G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254914436
    datadisk:153668366
    volume_size:300G
    volume_used:147G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254914776
    datadisk:153672271
    volume_size:300G
    volume_used:147G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q1                 19634.32              3122.48             19436.17              3067.77
TPC-DS Q2                203325.35             14007.45            203746.66             13230.24
TPC-DS Q3                 42866.25              3590.16             83101.51              4970.89
TPC-DS Q4                351160.24            162193.86            336107.34            157447.65
TPC-DS Q5                111842.01             33588.12            109826.20             32163.15
TPC-DS Q6                 12580.57              8472.36             12072.81              6515.58
TPC-DS Q7                 62299.71              4233.76             57319.94              4562.61
TPC-DS Q8                 41138.62             18385.78             40353.33              3746.55
TPC-DS Q9                 16824.15              2477.14             17811.25              1965.28
TPC-DS Q10                12983.84              4847.01             12142.04              3328.94
TPC-DS Q11                81974.02             73203.30             82967.20             75322.31
TPC-DS Q12                 2530.17               655.40              2427.39               590.44
TPC-DS Q13                 8388.22              5683.23              6831.16              1630.58
TPC-DS Q14a+b            364469.25            292715.04            359320.98            277743.88
TPC-DS Q15                10906.39              1102.28              9145.17              1661.15
TPC-DS Q16                17371.39              1201.63             18045.84               867.85
TPC-DS Q17                96499.49             50229.22             68194.40             31630.77
TPC-DS Q18                23316.20             15131.60             22643.95              7867.51
TPC-DS Q19                 7375.96              3431.83              4319.63              2443.85
TPC-DS Q20                 1534.48              1285.41              1508.07               671.08
TPC-DS Q21                77273.33              4877.92             78439.06              1659.85
TPC-DS Q22                80231.34             81616.97             80584.07             62257.66
TPC-DS Q23a+b           2363955.25           2546196.19           2009135.96           2467336.99
TPC-DS Q24a+b              7277.87              6196.78              7424.56              4302.74
TPC-DS Q25                17897.78             12511.37             21556.02             11737.61
TPC-DS Q26                 3391.19              2241.43              3583.52               743.99
TPC-DS Q27                16325.47             16761.93             17749.81             13833.43
TPC-DS Q28                17884.44              7488.03             17044.73              3828.79
TPC-DS Q29                12863.84             13971.04             14284.25             11146.77
TPC-DS Q30                 2622.27               846.71              2743.32               788.93
TPC-DS Q31                25771.04             21209.35             25968.10             17670.33
TPC-DS Q32                 2074.52               536.15               662.60               458.80
TPC-DS Q33                 9341.15              2754.79              6585.91               791.51
TPC-DS Q34                 4441.03               514.59              2194.20               527.21
TPC-DS Q35                15834.44              7799.78              7568.51              7801.56
TPC-DS Q37                18570.40             12124.86             11430.45             11064.35
TPC-DS Q38                32065.89             28259.69             29258.44             26496.64
TPC-DS Q39a+b             73579.50             70647.27             94667.31             76026.37
TPC-DS Q40                 4597.86              4594.75              5530.00              5196.02
TPC-DS Q41                  448.58               283.19                15.37               421.49
TPC-DS Q42                 2064.88              1976.44              2728.51               540.56
TPC-DS Q43                 1081.72               762.04               680.54               517.63
TPC-DS Q44                 1542.07              1007.91              1480.60               488.47
TPC-DS Q45                  740.19               732.37               882.79               344.26
TPC-DS Q46                 1177.84              1294.10              1320.88               943.59
TPC-DS Q47                 4801.63              5027.35              4990.49              5241.73
TPC-DS Q48                 1903.71               574.40              1291.03              2191.27
TPC-DS Q49                36974.38              8943.77             40370.28              7981.21
TPC-DS Q50                 4752.58              2447.35              2291.48              1740.01
TPC-DS Q51                46696.55             46669.23             47074.00             45961.28
TPC-DS Q52                 1172.62              1941.49              2183.50               997.02
TPC-DS Q53                 1589.66              1318.91              1553.08              1277.11
TPC-DS Q54                 6817.38              4386.03              6993.93              4270.68
TPC-DS Q55                  123.31              2135.59               130.30              1262.42
TPC-DS Q56                 1904.15              1613.02              8961.03               860.15
TPC-DS Q57                 1515.68              1855.97              1358.42              1113.87
TPC-DS Q58                 6909.53              4905.17              5231.72              4582.71
TPC-DS Q59                12154.06             10544.35             11618.51              9880.81
TPC-DS Q60                14109.51              1550.67              1617.88              1154.82
TPC-DS Q61                 3203.04               257.58               309.73               262.95
TPC-DS Q62                 2715.01              1500.46              2981.73               667.20
TPC-DS Q63                  753.74               541.99               563.20               563.46
TPC-DS Q64                44234.90             36459.31             41767.23             29958.83
TPC-DS Q65                23852.91             23393.82             22279.18             20001.86
TPC-DS Q66                20584.84              3422.25             15632.43              3422.89
TPC-DS Q67               110918.54            107300.89            104690.22             96695.21
TPC-DS Q68                19362.20              5366.98             19872.21              1570.54
TPC-DS Q69                10279.11              2756.73              3491.61              2260.46
TPC-DS Q71                 3672.33              3214.36              1426.14              1113.17
TPC-DS Q72                42312.41             69357.12             71569.69             68066.25
TPC-DS Q73                  402.37               469.98               371.33               507.37
TPC-DS Q74                24415.12             23262.79             23686.89             22434.35
TPC-DS Q75               160428.38            106527.82            159908.28            110214.71
TPC-DS Q76                14068.51             15951.35             13780.44              3094.74
TPC-DS Q77                 7324.85              7021.75              8500.17              6007.80
TPC-DS Q78               177657.12            148683.47            179526.55            150401.61
TPC-DS Q79                 4862.83              3166.87              9947.58              5968.67
TPC-DS Q80               119687.95            106530.46            117314.53            103188.99
TPC-DS Q81                 2938.77              1552.18              2297.99              1382.26
TPC-DS Q82                56103.50              9110.52              9209.18              7388.19
TPC-DS Q83                 3457.54               275.00              1871.91               602.78
TPC-DS Q84                  677.06                74.98              1032.02                87.39
TPC-DS Q85                 2280.84              2250.75              4468.39              1164.20
TPC-DS Q87                53159.93             38057.72             40239.67             37729.02
TPC-DS Q88                 3545.43              1541.43              3600.89              1149.82
TPC-DS Q89                 1536.65              1024.86              2177.86               457.19
TPC-DS Q90                 1393.46               434.04              1214.47               442.72
TPC-DS Q91                  798.80               194.61              1284.15               929.59
TPC-DS Q92                 1960.35               582.73              1484.61               247.44
TPC-DS Q93                19608.29             17941.48             19647.83             18086.87
TPC-DS Q94                 2124.08              2243.51              2378.01               884.08
TPC-DS Q95                18482.05             14451.44             14282.81             14404.21
TPC-DS Q96                  117.64               117.55               127.07               118.30
TPC-DS Q97                42127.45             39990.41             41251.34             41905.87
TPC-DS Q98                 2342.82              1291.38              3667.14              1525.29
TPC-DS Q99                 3023.86              2592.55              1945.46              1399.32

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           0.0         1435.0         7.0     2616.0    4066.0
MonetDB-BHT-8-1-2-1           0.0         1435.0         7.0     2616.0    4066.0
MonetDB-BHT-8-2-1-1           0.0         1435.0         7.0     2616.0    4066.0
MonetDB-BHT-8-2-2-1           0.0         1435.0         7.0     2616.0    4066.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           9.60
MonetDB-BHT-8-1-2-1           4.98
MonetDB-BHT-8-2-1-1           8.38
MonetDB-BHT-8-2-2-1           3.95

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           38096.87
MonetDB-BHT-8-1-2-1           73599.96
MonetDB-BHT-8-2-1-1           43875.11
MonetDB-BHT-8-2-2-1           93292.19

### Throughput@Size
                                                 time [s]  count   SF  Throughput@Size [~GB/h]
DBMS              SF  num_experiment num_client                                               
MonetDB-BHT-8-1-1 100 1              1               5510      1  100                  1437.39
MonetDB-BHT-8-1-2 100 1              2               4507      1  100                  1757.27
MonetDB-BHT-8-2-1 100 2              1               5073      1  100                  1561.21
MonetDB-BHT-8-2-2 100 2              2               4269      1  100                  1855.24

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1    18753.02    18.18        133.01               202.86
MonetDB-BHT-8-1-2    19617.62    20.95        138.81               248.40
MonetDB-BHT-8-2-1    38492.62    36.87        212.83               285.18
MonetDB-BHT-8-2-2    18755.20    18.47        170.38               259.19

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       76.84     0.23          0.42                 0.44
MonetDB-BHT-8-1-2       76.84     0.21          0.66                 0.70
MonetDB-BHT-8-2-1       78.23     0.10          0.43                 0.46
MonetDB-BHT-8-2-2       78.23     0.06          0.66                 0.70

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
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

### Evaluate Results

```
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 18519s 
    Code: 1730436947
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
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
    Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254914948
    datadisk:153672273
    volume_size:300G
    volume_used:147G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254915288
    datadisk:153672274
    volume_size:300G
    volume_used:147G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254915628
    datadisk:153672274
    volume_size:300G
    volume_used:147G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254915628
    datadisk:153672274
    volume_size:300G
    volume_used:147G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-3 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254915628
    datadisk:153672274
    volume_size:300G
    volume_used:147G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
               MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
TPC-DS Q23a+b              False              False               True               True              False

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
TPC-DS Q1               18538.90            2564.99            2220.44            3423.14            2127.86
TPC-DS Q2              206626.52           12952.16           25054.57           25312.30           25206.61
TPC-DS Q3               83923.47            5101.27            6885.62            5025.47            6869.26
TPC-DS Q4              341735.64          166898.11          174661.85          174263.79          184724.37
TPC-DS Q5              113147.73           34085.45           39026.79           43528.86           28225.25
TPC-DS Q6               11724.19            7468.09           16794.39           15240.69           16148.02
TPC-DS Q7               59291.34            5462.72            4644.01            2257.73            6190.63
TPC-DS Q8               38243.78            4784.95            4633.57            4655.19            4339.35
TPC-DS Q9               30894.64            3800.46            6835.66            6615.47            5347.63
TPC-DS Q10              11754.60            8930.01            2025.92            2264.03            3514.53
TPC-DS Q11              77910.52           82305.28           95381.96           97042.97           95182.40
TPC-DS Q12               2640.05            1125.40             568.27            1341.16             747.19
TPC-DS Q13               5295.13            3076.21            2117.58             381.46            2119.44
TPC-DS Q14a+b          347309.77          336362.91          334259.51          338778.72          346726.64
TPC-DS Q15              10819.29            3361.51             700.35             696.32             585.21
TPC-DS Q16              17402.31             880.24            1675.65            1804.18             770.67
TPC-DS Q17             105361.40           54613.78           30239.78           30107.69           33232.12
TPC-DS Q18              22399.99           10421.44            8207.63            7890.14            7610.50
TPC-DS Q19               7081.09            4718.60             535.36             267.54             259.49
TPC-DS Q20                660.08             467.20             526.03             462.43             544.21
TPC-DS Q21              75792.44            4850.98            2013.01             504.70             492.74
TPC-DS Q22              77925.58           81645.32           77118.38           84165.47           65111.29
TPC-DS Q24a+b            7943.15           11060.33            3718.91           14801.84            3176.85
TPC-DS Q25              42011.09           36420.81           19102.83           25421.29           19955.39
TPC-DS Q26               2507.95             816.84            2036.94            9321.68            2119.76
TPC-DS Q27              25541.98           24850.50           12828.37           24919.88           44332.58
TPC-DS Q28              21794.64            6997.52            3551.57            5919.81            7250.54
TPC-DS Q29              22337.55           14252.95           14942.36           13221.91           12618.90
TPC-DS Q30               2876.82            1917.35            2225.91            3044.77            2291.65
TPC-DS Q31              24420.65           22387.04           16419.53           15985.83           17144.23
TPC-DS Q32               1000.83            1102.64             801.99             435.47             556.06
TPC-DS Q33              13598.80           13705.28           26606.43            1157.75             853.98
TPC-DS Q34               3244.01             786.51             509.80            1655.66             769.00
TPC-DS Q35               7866.53            7540.92            7546.51            8840.01            7531.34
TPC-DS Q37              20779.53            4183.23            3998.35            5910.21            1475.68
TPC-DS Q38              29732.39           29028.00           29397.20           28329.74           27820.09
TPC-DS Q39a+b           98426.42           69300.28           73493.82           69373.18           68516.18
TPC-DS Q40               4582.57            4241.85            4623.61            3369.54            3497.11
TPC-DS Q41                244.48             170.95              43.77              37.72             325.69
TPC-DS Q42               2089.23            1495.20             343.33             186.09            1212.33
TPC-DS Q43                695.88             594.78             327.10             588.17             581.39
TPC-DS Q44               1415.14             446.89            1043.17             316.15             392.22
TPC-DS Q45               1752.86            1192.34             289.06             371.29             571.94
TPC-DS Q46               2261.84            1112.34            1498.11             504.37             487.35
TPC-DS Q47               6231.53            6253.64            7008.00            6436.11            5933.75
TPC-DS Q48               2417.78             630.50            1647.52            7323.05            3036.16
TPC-DS Q49              36103.78           10268.64           13246.03            8002.66            8280.82
TPC-DS Q50               2230.24            1672.75            1642.27            2049.90            1219.12
TPC-DS Q51              46839.43           47730.19           50289.85           49995.35           47831.40
TPC-DS Q52               1341.16            1283.00             250.51             163.38            1218.38
TPC-DS Q53               1229.44            1510.02             610.87             598.65             995.26
TPC-DS Q54               4160.67            5075.40            4342.14            2551.51            5214.75
TPC-DS Q55                137.30            2420.09             154.20             134.00             148.02
TPC-DS Q56               8529.82            7424.54             768.85             767.73            1385.61
TPC-DS Q57               1259.90            1175.05            1205.79            1612.11            1065.38
TPC-DS Q58               4821.48            4722.62            4917.19            4549.98            4765.35
TPC-DS Q59              12296.12           10286.31            8886.33            8761.30            6460.04
TPC-DS Q60               1530.88            1168.67            1071.28            1117.83            1079.16
TPC-DS Q61               1478.40            1859.86             311.65             765.74             349.23
TPC-DS Q62               2796.75             686.21             677.18            1946.50            1157.81
TPC-DS Q63                964.44             542.66             574.59             545.92             546.87
TPC-DS Q64              41146.04           44234.90           36084.76           15953.11           14065.01
TPC-DS Q65              21350.44           21049.03           20773.70           22756.05           18895.48
TPC-DS Q66              17058.07            4993.49            2829.59           10934.63            2803.38
TPC-DS Q67             108175.28          110521.62          120647.71          100644.12           99478.02
TPC-DS Q68               4859.84            3099.50            1971.40             257.48            1620.49
TPC-DS Q69                649.49            1019.74             949.95             999.80             710.93
TPC-DS Q71               1745.50            1485.03            3398.25            1073.85            1093.97
TPC-DS Q72              79121.96           78854.07           97114.36           64622.83           58027.22
TPC-DS Q73                281.33             662.41             324.96            5645.14             279.98
TPC-DS Q74              98710.09           96902.52           88934.52           85181.47           81699.48
TPC-DS Q75             159039.22          119952.73          132048.62          144545.27          115533.12
TPC-DS Q76              12350.49           12267.55            6091.41            1580.38            3162.96
TPC-DS Q77               7155.27            5473.63            6906.14            9835.00            5571.81
TPC-DS Q78             167043.52          155490.67          170988.15          162612.76          145893.56
TPC-DS Q79               3207.19            5585.74            5481.68            3956.64            2552.96
TPC-DS Q80             126991.90          131982.26          121104.21           93930.91           88835.91
TPC-DS Q81               2867.30            1713.44            2357.92            2311.51            2305.91
TPC-DS Q82              26836.80           22369.88           27270.93            1680.02            2847.54
TPC-DS Q83               1924.84             588.11            2778.61             600.79             510.15
TPC-DS Q84                569.03             240.97            1103.53              80.13              75.24
TPC-DS Q85               3017.01            2195.59            2135.49             382.32            1487.40
TPC-DS Q87              53571.97           53618.47           37358.23           37637.21           38414.79
TPC-DS Q88               3867.43            1097.83            4118.08             859.60            1172.68
TPC-DS Q89               2186.33            2626.02            2312.28             519.48            1007.99
TPC-DS Q90               1027.49             270.62            4491.05             279.03             193.60
TPC-DS Q91                721.70             201.46             918.71              78.81             318.97
TPC-DS Q92               1463.35            1612.42             626.89             256.65             238.47
TPC-DS Q93              20177.40           18137.07           21952.74           19281.39           17681.13
TPC-DS Q94               2287.83            2072.25            2677.01            1682.66            1409.30
TPC-DS Q95              15071.98           15504.95           15740.51           16015.02           16564.77
TPC-DS Q96                118.74             101.77             110.34             113.45             111.59
TPC-DS Q97              47587.94           38059.75           41848.00           44470.64           39341.23
TPC-DS Q98               2571.03            2458.00            1003.90            1016.74            1236.83
TPC-DS Q99               1724.46            1429.16            2850.31            1422.36            1417.27

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           0.0         1435.0         7.0     2616.0    4066.0
MonetDB-BHT-8-2-1           0.0         1435.0         7.0     2616.0    4066.0
MonetDB-BHT-8-3-1           0.0         1435.0         7.0     2616.0    4066.0
MonetDB-BHT-8-3-2           0.0         1435.0         7.0     2616.0    4066.0
MonetDB-BHT-8-3-3           0.0         1435.0         7.0     2616.0    4066.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           8.34
MonetDB-BHT-8-2-1           5.12
MonetDB-BHT-8-3-1           4.50
MonetDB-BHT-8-3-2           3.59
MonetDB-BHT-8-3-3           3.58

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           43888.65
MonetDB-BHT-8-2-1           71758.86
MonetDB-BHT-8-3-1           81691.72
MonetDB-BHT-8-3-2          103239.56
MonetDB-BHT-8-3-3          103178.60

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               6549      1  100                  1209.34
MonetDB-BHT-8-2 100 1              2               5734      1  100                  1381.23
MonetDB-BHT-8-3 100 1              3               5888      3  100                  4035.33

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    21590.57    24.13        218.26               282.27
MonetDB-BHT-8-2    20699.48    16.15        184.44               291.25
MonetDB-BHT-8-3    49373.64    44.21        406.72               481.28

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       48.00     0.06          0.37                 0.38
MonetDB-BHT-8-2       48.00     0.04          0.61                 0.63
MonetDB-BHT-8-3       80.71     0.09          1.04                 1.07

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST failed: SQL errors
TEST passed: No SQL warnings
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

