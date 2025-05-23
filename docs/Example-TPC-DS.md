# Benchmark: TPC-DS

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TPC-DS does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients for the loading test and the throughput test [2].

This example shows how to benchmark 99 reading queries Q1-Q99 derived from TPC-DS in MonetDB, PostgreSQL and MariaDB.

> The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS Specification.

In particular we had to apply changes to the queries, because
* MySQL and MariaDB do not have a FULL OUTER JOIN (Q51, Q97, ...)
* MySQL and MariaDB do CASTing to INTEGER differently
* column names may differ if AS is not used
* MariaDB does not know GROUPING
* the DBMS do not sort in the same way when NULL comes into play

See [query file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/tpcds/queries-tpcds.config) for all details.

The schema of
* MonetDB: sets primary keys and foreign key constraints after import and no other indexes
* MySQL: sets primary keys before import, all foreign key constraints and indexes on foreign keys of fact tables and customer table after import
* MariaDB: sets primary keys before import, all foreign key constraints and indexes on foreign keys of fact tables and customer table after import
* PostgreSQL: sets primary keys before import, all foreign key constraints and indexes on foreign keys of fact tables and customer table after import

**MySQL is excluded currently because the treatment of NULL during INSERT is complicated.**



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
nohup python tpcds.py -ms 3 -dt -tr \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_compare.log &
```

This
* starts a clean instance of PostgreSQL, MonetDB and MariaDB (at the same time, `-ms`)
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

doc_tpcds_testcase_compare.log
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

To see the summary again you can simply call `bexperiments summary -e 1730998769` with the experiment code.

For a more detailed query-wise evaluation you can call `dbmsbenchmarker read -r ~/benchmarks/1730998769 -e yes`.

To inspect result sets you can call `python evaluate.py -r ~/benchmarks/ -e 1730390884 -q 4 resultsets` (here: for query 4).

To compare result sets you can call `dbmsinspect -r ~/benchmarks -c 1730998769 -q 4` (here: for query 4).
This shows the differences in result sets only.


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
  -t 1200 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_monitoring.log &
```

If monitoring is activated, the summary also contains a section like this:

doc_tpcds_testcase_monitoring.log
```bash
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 815s 
    Code: 1731440648
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
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
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:365355764
    datadisk:13200736
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                  69.92
TPC-DS Q2                2267.27
TPC-DS Q3                  46.63
TPC-DS Q4                3928.99
TPC-DS Q5                 731.93
TPC-DS Q6                 225.43
TPC-DS Q7                 106.93
TPC-DS Q8                 112.86
TPC-DS Q9                 140.33
TPC-DS Q10                123.59
TPC-DS Q11               1955.41
TPC-DS Q12                 44.86
TPC-DS Q13                173.60
TPC-DS Q14a+b            6032.76
TPC-DS Q15                 42.55
TPC-DS Q16                280.60
TPC-DS Q17                567.48
TPC-DS Q18                267.12
TPC-DS Q19                 81.25
TPC-DS Q20                 50.34
TPC-DS Q21                105.59
TPC-DS Q22               2697.35
TPC-DS Q23a+b            9456.09
TPC-DS Q24a+b             907.48
TPC-DS Q25                322.06
TPC-DS Q26                 67.77
TPC-DS Q27                336.60
TPC-DS Q28                184.62
TPC-DS Q29                339.38
TPC-DS Q30                 33.78
TPC-DS Q31                432.64
TPC-DS Q32                 43.65
TPC-DS Q33                 50.09
TPC-DS Q34                 49.32
TPC-DS Q35                221.97
TPC-DS Q36                241.16
TPC-DS Q37                102.18
TPC-DS Q38                606.55
TPC-DS Q39a+b            3736.83
TPC-DS Q40                223.51
TPC-DS Q41                  9.93
TPC-DS Q42                 36.65
TPC-DS Q43                157.45
TPC-DS Q44                273.42
TPC-DS Q45                 40.13
TPC-DS Q46                 82.67
TPC-DS Q47                505.68
TPC-DS Q48                145.69
TPC-DS Q49                252.76
TPC-DS Q50                235.04
TPC-DS Q51               1847.90
TPC-DS Q52                 35.85
TPC-DS Q53                 56.81
TPC-DS Q54                 48.19
TPC-DS Q55                 31.65
TPC-DS Q56                 46.17
TPC-DS Q57                156.88
TPC-DS Q58                165.02
TPC-DS Q59                281.75
TPC-DS Q60                 50.14
TPC-DS Q61                 74.88
TPC-DS Q62                 47.11
TPC-DS Q63                 53.34
TPC-DS Q64               1206.93
TPC-DS Q65                455.95
TPC-DS Q66                254.53
TPC-DS Q67               2217.36
TPC-DS Q68                 82.16
TPC-DS Q69                 43.97
TPC-DS Q70                160.00
TPC-DS Q71                 63.60
TPC-DS Q72                254.20
TPC-DS Q73                 48.19
TPC-DS Q74                537.97
TPC-DS Q75               2261.56
TPC-DS Q76                168.90
TPC-DS Q77                173.78
TPC-DS Q78               3817.84
TPC-DS Q79                 89.28
TPC-DS Q80               1908.13
TPC-DS Q81                 55.64
TPC-DS Q82                364.76
TPC-DS Q83                 27.49
TPC-DS Q84                 86.08
TPC-DS Q85                 73.80
TPC-DS Q86                 70.74
TPC-DS Q87                829.58
TPC-DS Q88                207.62
TPC-DS Q89                 83.94
TPC-DS Q90                 23.09
TPC-DS Q91                 28.21
TPC-DS Q92                 27.08
TPC-DS Q93                536.56
TPC-DS Q94                 62.16
TPC-DS Q95                199.20
TPC-DS Q96                 31.04
TPC-DS Q97                850.49
TPC-DS Q98                 87.76
TPC-DS Q99                 98.91

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           0.0          270.0         9.0      207.0     493.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.19

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           60883.83

### Throughput@Size
                                              time [s]  count  SF  Throughput@Size [~GB/h]
DBMS            SF num_experiment num_client                                              
MonetDB-BHT-8-1 3  1              1                 82      1   3                  2897.56

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      711.83     2.71          2.54                 9.72

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       53.59     0.23          1.29                 2.72

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      395.22     2.89          8.05                16.87

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       15.61        0          0.24                 0.25

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
MonetDB is fast, so we cannot see a lot (metrics are fetched every 30 seconds).


## Perform Benchmark - Throughput Test

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

Example:
```bash
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_throughput.log &
```

This runs 3 streams (`-ne`), the first one as a single stream and the following 2 in parallel.

doc_tpcds_testcase_throughput.log
```bash
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 600s 
    Code: 1731441609
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
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
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:357892064
    datadisk:5737036
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:357973540
    datadisk:5818512
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-2 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:357973540
    datadisk:5818512
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-2-2
TPC-DS Q1                  42.76              39.85              54.82
TPC-DS Q2                 160.03             144.55             136.95
TPC-DS Q3                  25.01              19.39              27.44
TPC-DS Q4                1278.50            1274.18            1247.00
TPC-DS Q5                 256.02             240.49             250.72
TPC-DS Q6                  82.74              58.44              63.35
TPC-DS Q7                  60.59              50.88              48.48
TPC-DS Q8                  42.12              39.02              42.06
TPC-DS Q9                  72.98              47.71              48.04
TPC-DS Q10                 64.96              82.36              34.95
TPC-DS Q11                576.52             564.26             621.58
TPC-DS Q12                 20.57              19.23              18.97
TPC-DS Q13                108.43             101.86              90.00
TPC-DS Q14a+b            2179.64            2285.72            2100.95
TPC-DS Q15                 23.40              22.47              23.31
TPC-DS Q16                 36.49              34.14              37.14
TPC-DS Q17                114.34              98.90             125.67
TPC-DS Q18                112.08              57.72              53.31
TPC-DS Q19                 43.43              37.71              38.28
TPC-DS Q20                 26.40              24.75              26.71
TPC-DS Q21                 64.59              57.86              69.04
TPC-DS Q22               1024.77             973.15            1039.11
TPC-DS Q23a+b            2471.03            2835.27            2616.44
TPC-DS Q24a+b             177.35             173.43             169.47
TPC-DS Q25                115.60             112.72             100.49
TPC-DS Q26                 20.55              18.68              19.39
TPC-DS Q27                132.58             101.47              98.33
TPC-DS Q28                 61.85              63.16              66.19
TPC-DS Q29                 98.48              84.76              85.80
TPC-DS Q30                 21.35              19.13              21.11
TPC-DS Q31                142.60             124.05             133.51
TPC-DS Q32                 17.38              18.35              16.99
TPC-DS Q33                 28.32              48.51              24.67
TPC-DS Q34                 25.16              24.49              26.96
TPC-DS Q35                 81.90              74.92              84.24
TPC-DS Q36                 73.85              73.39              89.84
TPC-DS Q37                119.51              44.48              62.42
TPC-DS Q38                206.11             192.83             184.52
TPC-DS Q39a+b            1560.19            1431.08            1417.28
TPC-DS Q40                 73.27              92.07              91.97
TPC-DS Q41                  8.18               8.37               9.05
TPC-DS Q42                 18.56              19.59              20.19
TPC-DS Q43                 61.18              61.60              61.10
TPC-DS Q44                 33.11              34.38              32.69
TPC-DS Q45                 27.19              26.02              25.75
TPC-DS Q46                 41.99              38.50              37.53
TPC-DS Q47                207.82             220.54             225.33
TPC-DS Q48                 93.82              91.37              92.92
TPC-DS Q49                100.54              86.89              96.05
TPC-DS Q50                 93.53              94.98              95.66
TPC-DS Q51                607.96             554.41             613.88
TPC-DS Q52                 24.18              19.32              20.35
TPC-DS Q53                 31.06              68.29              27.99
TPC-DS Q54                 32.90              22.43              27.77
TPC-DS Q55                 16.66              16.73              18.64
TPC-DS Q56                 24.62              22.05              21.93
TPC-DS Q57                 94.97              77.89              81.13
TPC-DS Q58                 50.73              40.66              49.96
TPC-DS Q59                100.97              94.47              99.69
TPC-DS Q60                 23.73              30.91              23.30
TPC-DS Q61                 36.71              31.89              39.74
TPC-DS Q62                 27.95              23.03              24.38
TPC-DS Q63                 27.14              24.75              25.04
TPC-DS Q64                364.77             210.17             216.78
TPC-DS Q65                 91.43              84.43              86.79
TPC-DS Q66                101.67              98.59              93.10
TPC-DS Q67                680.65             673.14             644.91
TPC-DS Q68                 38.61              43.35              38.61
TPC-DS Q69                 23.97              23.74              27.95
TPC-DS Q70                 75.92              69.10              70.94
TPC-DS Q71                 34.98              30.12              36.60
TPC-DS Q72                165.90             140.47             150.97
TPC-DS Q73                 29.88              25.42              26.07
TPC-DS Q74                606.10             586.68             624.53
TPC-DS Q75                668.21             649.32             642.13
TPC-DS Q76                 44.56              43.87              45.47
TPC-DS Q77                 62.77              55.95              53.79
TPC-DS Q78                847.53             752.27             779.49
TPC-DS Q79                 39.99              37.35              39.81
TPC-DS Q80                421.99             459.42             505.40
TPC-DS Q81                 30.52              30.23              30.91
TPC-DS Q82                128.72              57.96              47.84
TPC-DS Q83                 14.59              13.68              15.58
TPC-DS Q84                 30.19              36.04              22.00
TPC-DS Q85                 43.21              34.97              35.57
TPC-DS Q86                 25.47              26.91              27.37
TPC-DS Q87                249.99             264.31             246.14
TPC-DS Q88                 88.54              91.55              88.12
TPC-DS Q89                 35.55              45.89              36.82
TPC-DS Q90                 23.13              13.15              19.69
TPC-DS Q91                 25.58              30.56              24.75
TPC-DS Q92                 13.99              14.30              15.21
TPC-DS Q93                 89.16              98.85              90.00
TPC-DS Q94                 18.25              16.10              18.67
TPC-DS Q95                145.06              94.63             115.50
TPC-DS Q96                 14.56              14.47              14.26
TPC-DS Q97                219.87             206.63             207.40
TPC-DS Q98                151.67              39.72              42.51
TPC-DS Q99                 54.07              51.19              55.81

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          103.0         9.0       73.0     192.0
MonetDB-BHT-8-2-1           1.0          103.0         9.0       73.0     192.0
MonetDB-BHT-8-2-2           1.0          103.0         9.0       73.0     192.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.08
MonetDB-BHT-8-2-1           0.08
MonetDB-BHT-8-2-2           0.08

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           48148.77
MonetDB-BHT-8-2-1           52598.23
MonetDB-BHT-8-2-2           52186.57

### Throughput@Size
                                              time [s]  count  SF  Throughput@Size [~GB/h]
DBMS            SF num_experiment num_client                                              
MonetDB-BHT-8-1 1  1              1                 41      1   1                  1931.71
MonetDB-BHT-8-2 1  1              2                 42      2   1                  3771.43

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
  -t 1200 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 10Gi \
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
| bexhoma-storage-monetdb-tpcds-1         | monetdb         | tpcds-1      | True         |               151 | MonetDB    | shared               | 30Gi      | Bound    | 10G    | 2.0G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpcds-3         | monetdb         | tpcds-3      | True         |               393 | MonetDB    | shared               | 100Gi     | Bound    | 100G   | 5.4G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpcds-100       | monetdb         | tpcds-100    | True         |              4019 | MonetDB    | shared               | 300Gi     | Bound    | 300G   | 156G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+

+---------------+--------------+--------------+---------------+
| 1707740320    | sut          |   loaded [s] | benchmarker   |
+===============+==============+==============+===============+
| MonetDB-BHT-8 | (1. Running) |       185.41 | (1. Running)  |
+---------------+--------------+--------------+---------------+
```

The result looks something like

doc_tpcds_testcase_storage.log
```bash
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 871s 
    Code: 1731442419
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
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
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352155192
    datadisk:5729478
    volume_size:30G
    volume_used:4.7G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352155124
    datadisk:5811019
    volume_size:30G
    volume_used:5.6G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q1                   127.88              2946.87
TPC-DS Q2                   176.99               458.44
TPC-DS Q3                    38.43              1222.77
TPC-DS Q4                  1239.66              3117.34
TPC-DS Q5                   281.69              1170.22
TPC-DS Q6                    82.89               375.91
TPC-DS Q7                   129.98              2127.72
TPC-DS Q8                    49.60               607.43
TPC-DS Q9                    70.18                81.81
TPC-DS Q10                  140.89              4987.28
TPC-DS Q11                  673.28               640.01
TPC-DS Q12                   22.71               323.02
TPC-DS Q13                  109.77               344.94
TPC-DS Q14a+b              2283.67              2734.75
TPC-DS Q15                   21.78                22.82
TPC-DS Q16                   53.82              1408.81
TPC-DS Q17                  111.73               166.23
TPC-DS Q18                  181.94               421.87
TPC-DS Q19                   37.86               165.16
TPC-DS Q20                   23.63                28.58
TPC-DS Q21                  101.49              3155.03
TPC-DS Q22                 1039.17              2043.95
TPC-DS Q23a+b              2476.93              2790.04
TPC-DS Q24a+b               183.81               408.54
TPC-DS Q25                  123.78               108.64
TPC-DS Q26                   27.28               580.47
TPC-DS Q27                  121.74               146.69
TPC-DS Q28                   69.77                63.69
TPC-DS Q29                   97.23               114.31
TPC-DS Q30                   28.94               248.53
TPC-DS Q31                  194.25               272.54
TPC-DS Q32                   20.07                19.16
TPC-DS Q33                   25.71               197.31
TPC-DS Q34                   47.14               520.25
TPC-DS Q35                   95.92              1914.37
TPC-DS Q36                  112.05               103.56
TPC-DS Q37                  169.43               160.53
TPC-DS Q38                  210.32               194.20
TPC-DS Q39a+b              1448.24              1530.53
TPC-DS Q40                   89.28               161.32
TPC-DS Q41                   75.48                 8.51
TPC-DS Q42                   64.92                22.76
TPC-DS Q43                   51.10                48.60
TPC-DS Q44                  105.93               533.25
TPC-DS Q45                   30.11                29.02
TPC-DS Q46                  101.04               157.47
TPC-DS Q47                  302.50               236.87
TPC-DS Q48                  108.13               120.98
TPC-DS Q49                  137.67               474.16
TPC-DS Q50                  448.56               228.91
TPC-DS Q51                  639.00               596.68
TPC-DS Q52                   22.09                20.73
TPC-DS Q53                   26.82                27.08
TPC-DS Q54                   22.56                24.07
TPC-DS Q55                   17.69                16.61
TPC-DS Q56                   27.11               106.15
TPC-DS Q57                  104.50               132.26
TPC-DS Q58                   47.75                52.94
TPC-DS Q59                  110.85               129.75
TPC-DS Q60                   31.22                26.10
TPC-DS Q61                   92.51                48.48
TPC-DS Q62                   44.37              1646.72
TPC-DS Q63                   30.94                28.92
TPC-DS Q64                  563.64               881.72
TPC-DS Q65                  103.82                93.21
TPC-DS Q66                  125.30               698.35
TPC-DS Q67                  640.19               663.11
TPC-DS Q68                   38.73                36.24
TPC-DS Q69                   51.43               108.91
TPC-DS Q70                  539.50               246.73
TPC-DS Q71                   29.31                77.67
TPC-DS Q72                  937.38               922.06
TPC-DS Q73                   29.81                26.93
TPC-DS Q74                  596.64               593.48
TPC-DS Q75                  694.32               656.11
TPC-DS Q76                   79.73               576.46
TPC-DS Q77                   60.13                93.19
TPC-DS Q78                  850.47               878.12
TPC-DS Q79                   49.85                92.98
TPC-DS Q80                  446.50               751.46
TPC-DS Q81                   75.51               107.10
TPC-DS Q82                  458.65               344.17
TPC-DS Q83                   54.78               121.99
TPC-DS Q84                   16.63                28.89
TPC-DS Q85                   71.51               228.22
TPC-DS Q86                   34.93                32.01
TPC-DS Q87                  262.10               276.17
TPC-DS Q88                  116.91               333.94
TPC-DS Q89                   36.50                37.79
TPC-DS Q90                   18.47                14.18
TPC-DS Q91                  105.03               101.94
TPC-DS Q92                   12.90                11.25
TPC-DS Q93                  104.56               205.66
TPC-DS Q94                  144.15               773.81
TPC-DS Q95                  125.26               133.15
TPC-DS Q96                   14.77                13.59
TPC-DS Q97                  209.55               235.88
TPC-DS Q98                   40.29                60.52
TPC-DS Q99                  265.88                64.68

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0          139.0         6.0       78.0     230.0
MonetDB-BHT-8-2-1-1           1.0          139.0         6.0       78.0     230.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.11
MonetDB-BHT-8-2-1-1           0.20

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           35524.47
MonetDB-BHT-8-2-1-1           18657.53

### Throughput@Size
                                                time [s]  count  SF  Throughput@Size [~GB/h]
DBMS              SF num_experiment num_client                                              
MonetDB-BHT-8-1-1 1  1              1                 56      1   1                  1414.29
MonetDB-BHT-8-2-1 1  2              1                134      1   1                   591.04

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









## Profiling Benchmark

We have included a custom data profiling benchmark as in [1].
> We differentiate between metric attributes (INTEGER, DOUBLE, DECIMAL) and nominal attributes (others). We seek to obtain basic statistics about the attributes and we use COUNT, COUNT NULL (missing values), COUNT DISTINCT and the distribution: MIN, MAX, truncated AVG of values (metric) or of frequencies (nominal). We query for these 6 statistics per attribute and this yields 429 profiling queries. 

In [1] the benchmark is used to assess node stability and to compare performance of DBMS and cloud providers.

[1] [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
> Erdelt P.K. (2022)
> Orchestrating DBMS Benchmarking in the Cloud with Kubernetes.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2021.
> Lecture Notes in Computer Science, vol 13169. Springer, Cham.
> https://doi.org/10.1007/978-3-030-94437-7_6

Here, we run it at TPC-DS SF=10 in MonetDB:


```bash
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 10 \
  -ii -ic -is \
  -ne 1,1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 50Gi \
  profiling </dev/null &>$LOG_DIR/doc_tpcds_testcase_profiling.log &
```

### Evaluate Results

doc_tpcds_testcase_profiling.log
```bash
## Show Summary

### Workload
TPC-DS Data Profiling SF=10
    Type: tpcds
    Duration: 763s 
    Code: 1745497803
    We compute for all columns: Minimum, maximum, average, count, count distinct, count NULL and non NULL entries and coefficient of variation.
    This experiment compares imported TPC-DS data sets in different DBMS.
    TPC-DS (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.4.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:218884212
    datadisk:40080
    volume_size:50G
    volume_used:40G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1745497803
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:218884224
    datadisk:40080
    volume_size:50G
    volume_used:40G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1745497803

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                                    MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1
statistics_tab about call_center.cc_call_center_sk - all                            47.63              24.83
statistics_tab about call_center.cc_call_center_id - all                            52.27               5.01
statistics_tab about call_center.cc_rec_start_date - all                            10.24               5.22
statistics_tab about call_center.cc_rec_end_date - all                              19.61               4.95
statistics_tab about call_center.cc_closed_date_sk - all                            26.12               3.48
statistics_tab about call_center.cc_open_date_sk - all                              18.58               4.02
statistics_tab about call_center.cc_name - all                                      40.58               5.48
statistics_tab about call_center.cc_class - all                                     38.37               4.69
statistics_tab about call_center.cc_employees - all                                  6.60               3.05
statistics_tab about call_center.cc_sq_ft - all                                      6.50               3.46
statistics_tab about call_center.cc_hours - all                                     26.13               5.08
statistics_tab about call_center.cc_manager - all                                   95.48               5.18
statistics_tab about call_center.cc_mkt_id - all                                    15.72               3.27
statistics_tab about call_center.cc_mkt_class - all                                 11.18               5.23
statistics_tab about call_center.cc_mkt_desc - all                                  40.41               5.23
statistics_tab about call_center.cc_market_manager - all                            31.24               4.97
statistics_tab about call_center.cc_division - all                                  24.04               2.82
statistics_tab about call_center.cc_division_name - all                             36.20               4.76
statistics_tab about call_center.cc_company - all                                   12.21               3.25
statistics_tab about call_center.cc_company_name - all                              20.04               5.38
statistics_tab about call_center.cc_street_number - all                             29.89               4.92
statistics_tab about call_center.cc_street_name - all                               22.45               5.02
statistics_tab about call_center.cc_street_type - all                               21.93               4.94
statistics_tab about call_center.cc_suite_number - all                              27.78               7.55
statistics_tab about call_center.cc_city - all                                      25.58               5.02
statistics_tab about call_center.cc_county - all                                    33.76               4.17
statistics_tab about call_center.cc_state - all                                     26.70               6.02
statistics_tab about call_center.cc_zip - all                                       19.34               4.84
statistics_tab about call_center.cc_country - all                                  155.23               4.66
statistics_tab about call_center.cc_gmt_offset - all                                20.09               2.79
statistics_tab about call_center.cc_tax_percentage - all                             6.29               3.26
statistics_tab about catalog_page.cp_catalog_page_sk - all                         129.40               3.02
statistics_tab about catalog_page.cp_catalog_page_id - all                          50.13               6.40
statistics_tab about catalog_page.cp_start_date_sk - all                            18.45               3.68
statistics_tab about catalog_page.cp_end_date_sk - all                              21.48               3.25
statistics_tab about catalog_page.cp_department - all                               50.68               4.65
statistics_tab about catalog_page.cp_catalog_number - all                            7.44               3.16
statistics_tab about catalog_page.cp_catalog_page_number - all                      22.42               3.58
statistics_tab about catalog_page.cp_description - all                              86.87               8.93
statistics_tab about catalog_page.cp_type - all                                     11.20               4.77
statistics_tab about catalog_returns.cr_returned_date_sk - all                     134.94              64.64
statistics_tab about catalog_returns.cr_returned_time_sk - all                     168.53              84.32
statistics_tab about catalog_returns.cr_item_sk - all                              174.25              84.50
statistics_tab about catalog_returns.cr_refunded_customer_sk - all                 312.40             111.84
statistics_tab about catalog_returns.cr_refunded_cdemo_sk - all                    223.49             167.28
statistics_tab about catalog_returns.cr_refunded_hdemo_sk - all                    210.27              63.49
statistics_tab about catalog_returns.cr_refunded_addr_sk - all                     208.56             106.44
statistics_tab about catalog_returns.cr_returning_customer_sk - all                212.29             127.26
statistics_tab about catalog_returns.cr_returning_cdemo_sk - all                   320.13             185.59
statistics_tab about catalog_returns.cr_returning_hdemo_sk - all                   129.83              61.60
statistics_tab about catalog_returns.cr_returning_addr_sk - all                    201.62             100.20
statistics_tab about catalog_returns.cr_call_center_sk - all                       574.24              60.65
statistics_tab about catalog_returns.cr_catalog_page_sk - all                      204.67              57.14
statistics_tab about catalog_returns.cr_ship_mode_sk - all                          94.40              56.13
statistics_tab about catalog_returns.cr_warehouse_sk - all                         188.22              53.77
statistics_tab about catalog_returns.cr_reason_sk - all                            188.39              64.56
statistics_tab about catalog_returns.cr_order_number - all                         165.68              93.07
statistics_tab about catalog_returns.cr_return_quantity - all                      111.77              60.11
statistics_tab about catalog_returns.cr_return_amount - all                        188.96             120.95
statistics_tab about catalog_returns.cr_return_tax - all                           189.19              69.27
statistics_tab about catalog_returns.cr_return_amt_inc_tax - all                   308.53             124.47
statistics_tab about catalog_returns.cr_fee - all                                  190.89              57.99
statistics_tab about catalog_returns.cr_return_ship_cost - all                     280.09             101.62
statistics_tab about catalog_returns.cr_refunded_cash - all                        188.78              99.95
statistics_tab about catalog_returns.cr_reversed_charge - all                      164.56              84.21
statistics_tab about catalog_returns.cr_store_credit - all                         129.98              89.92
statistics_tab about catalog_returns.cr_net_loss - all                             181.71              97.14
statistics_tab about catalog_sales.cs_sold_date_sk - all                          1505.20             577.34
statistics_tab about catalog_sales.cs_sold_time_sk - all                          1441.49             700.04
statistics_tab about catalog_sales.cs_ship_date_sk - all                          2300.68             599.49
statistics_tab about catalog_sales.cs_bill_customer_sk - all                      1590.79             889.47
statistics_tab about catalog_sales.cs_bill_cdemo_sk - all                         1810.83             886.50
statistics_tab about catalog_sales.cs_bill_hdemo_sk - all                         1326.84             603.77
statistics_tab about catalog_sales.cs_bill_addr_sk - all                          1689.55             817.76
statistics_tab about catalog_sales.cs_ship_customer_sk - all                      1650.89             880.17
statistics_tab about catalog_sales.cs_ship_cdemo_sk - all                         1726.83             887.29
statistics_tab about catalog_sales.cs_ship_hdemo_sk - all                         1565.99             605.26
statistics_tab about catalog_sales.cs_ship_addr_sk - all                          1860.20             826.41
statistics_tab about catalog_sales.cs_call_center_sk - all                        1650.72             582.33
statistics_tab about catalog_sales.cs_catalog_page_sk - all                       1721.86             578.45
statistics_tab about catalog_sales.cs_ship_mode_sk - all                          1304.08             607.44
statistics_tab about catalog_sales.cs_warehouse_sk - all                          1253.97             612.32
statistics_tab about catalog_sales.cs_item_sk - all                               1483.43             738.76
statistics_tab about catalog_sales.cs_promo_sk - all                              1423.84             613.65
statistics_tab about catalog_sales.cs_order_number - all                          1496.67             691.41
statistics_tab about catalog_sales.cs_quantity - all                              1229.25             614.54
statistics_tab about catalog_sales.cs_wholesale_cost - all                        1302.69             640.06
statistics_tab about catalog_sales.cs_list_price - all                            1515.21             685.16
statistics_tab about catalog_sales.cs_sales_price - all                           1478.83             681.13
statistics_tab about catalog_sales.cs_ext_discount_amt - all                      2936.22            2005.93
statistics_tab about catalog_sales.cs_ext_sales_price - all                       2669.45            1790.24
statistics_tab about catalog_sales.cs_ext_wholesale_cost - all                    2428.26            1563.71
statistics_tab about catalog_sales.cs_ext_list_price - all                        3219.84            2510.34
statistics_tab about catalog_sales.cs_ext_tax - all                               1689.64             760.85
statistics_tab about catalog_sales.cs_coupon_amt - all                            1602.07            1000.03
statistics_tab about catalog_sales.cs_ext_ship_cost - all                         2164.15            1443.36
statistics_tab about catalog_sales.cs_net_paid - all                              3033.59            1870.80
statistics_tab about catalog_sales.cs_net_paid_inc_tax - all                      2838.79            2034.02
statistics_tab about catalog_sales.cs_net_paid_inc_ship - all                     3153.74            1899.78
statistics_tab about catalog_sales.cs_net_paid_inc_ship_tax - all                 2973.05            2041.60
statistics_tab about catalog_sales.cs_net_profit - all                            3373.47            3734.79
statistics_tab about customer.c_customer_sk - all                                   49.14               8.79
statistics_tab about customer.c_customer_id - all                                  331.32             169.47
statistics_tab about customer.c_current_cdemo_sk - all                             114.68              52.19
statistics_tab about customer.c_current_hdemo_sk - all                             110.94              22.75
statistics_tab about customer.c_current_addr_sk - all                               88.81              33.37
statistics_tab about customer.c_first_shipto_date_sk - all                          68.64              28.16
statistics_tab about customer.c_first_sales_date_sk - all                           42.76              31.71
statistics_tab about customer.c_salutation - all                                    86.05               9.45
statistics_tab about customer.c_first_name - all                                   111.94              59.07
statistics_tab about customer.c_last_name - all                                    156.94              59.34
statistics_tab about customer.c_preferred_cust_flag - all                           91.51               9.85
statistics_tab about customer.c_birth_day - all                                     48.35              22.59
statistics_tab about customer.c_birth_month - all                                   72.97              22.69
statistics_tab about customer.c_birth_year - all                                    85.09              27.47
statistics_tab about customer.c_birth_country - all                                 57.37              10.22
statistics_tab about customer.c_login - all                                         32.24               8.51
statistics_tab about customer.c_email_address - all                                473.52             188.81
statistics_tab about customer.c_last_review_date - all                              65.37              10.40
statistics_tab about customer_address.ca_address_sk - all                           46.01               8.99
statistics_tab about customer_address.ca_address_id - all                          163.67              70.93
statistics_tab about customer_address.ca_street_number - all                        18.36               8.48
statistics_tab about customer_address.ca_street_name - all                          83.38              38.49
statistics_tab about customer_address.ca_street_type - all                          96.97               8.12
statistics_tab about customer_address.ca_suite_number - all                        276.95               7.99
statistics_tab about customer_address.ca_city - all                                150.48               8.39
statistics_tab about customer_address.ca_county - all                              147.99               7.92
statistics_tab about customer_address.ca_state - all                                86.89               7.57
statistics_tab about customer_address.ca_zip - all                                  92.78              29.28
statistics_tab about customer_address.ca_country - all                              63.17               8.30
statistics_tab about customer_address.ca_gmt_offset - all                           66.00              14.06
statistics_tab about customer_address.ca_location_type - all                       169.22               7.96
statistics_tab about customer_demographics.cd_demo_sk - all                        118.56              13.27
statistics_tab about customer_demographics.cd_gender - all                          55.35              21.29
statistics_tab about customer_demographics.cd_marital_status - all                  79.99              18.77
statistics_tab about customer_demographics.cd_education_status - all                69.74              19.45
statistics_tab about customer_demographics.cd_purchase_estimate - all              156.79              66.90
statistics_tab about customer_demographics.cd_credit_rating - all                   79.24              19.78
statistics_tab about customer_demographics.cd_dep_count - all                      144.92              70.70
statistics_tab about customer_demographics.cd_dep_employed_count - all             144.74              76.94
statistics_tab about customer_demographics.cd_dep_college_count - all              186.07              70.21
statistics_tab about date_dim.d_date_sk - all                                       29.57               6.04
statistics_tab about date_dim.d_date_id - all                                       64.45              20.84
statistics_tab about date_dim.d_date - all                                          44.83               6.79
statistics_tab about date_dim.d_month_seq - all                                     22.34               5.88
statistics_tab about date_dim.d_week_seq - all                                      11.86               5.05
statistics_tab about date_dim.d_quarter_seq - all                                   27.47               5.05
statistics_tab about date_dim.d_year - all                                          21.92               4.95
statistics_tab about date_dim.d_dow - all                                           41.08               4.90
statistics_tab about date_dim.d_moy - all                                           66.39               5.75
statistics_tab about date_dim.d_dom - all                                           20.45               5.39
statistics_tab about date_dim.d_qoy - all                                           11.12               5.09
statistics_tab about date_dim.d_fy_year - all                                       10.26               4.81
statistics_tab about date_dim.d_fy_quarter_seq - all                                28.37               6.22
statistics_tab about date_dim.d_fy_week_seq - all                                   51.58               5.00
statistics_tab about date_dim.d_day_name - all                                      52.89               6.05
statistics_tab about date_dim.d_quarter_name - all                                  13.32               6.37
statistics_tab about date_dim.d_holiday - all                                       44.52               5.79
statistics_tab about date_dim.d_weekend - all                                       26.96               5.77
statistics_tab about date_dim.d_following_holiday - all                            189.17               6.24
statistics_tab about date_dim.d_first_dom - all                                     11.33               6.29
statistics_tab about date_dim.d_last_dom - all                                      94.03               6.29
statistics_tab about date_dim.d_same_day_ly - all                                   16.90               5.54
statistics_tab about date_dim.d_same_day_lq - all                                   10.39               5.54
statistics_tab about date_dim.d_current_day - all                                   11.91               6.62
statistics_tab about date_dim.d_current_week - all                                  22.46               5.88
statistics_tab about date_dim.d_current_month - all                                156.91               5.54
statistics_tab about date_dim.d_current_quarter - all                               35.87              12.12
statistics_tab about date_dim.d_current_year - all                                  11.94               6.93
statistics_tab about dbgen_version.dv_version - all                                 71.59               4.82
statistics_tab about dbgen_version.dv_create_date - all                             34.58               4.40
statistics_tab about dbgen_version.dv_create_time - all                             27.74               4.46
statistics_tab about dbgen_version.dv_cmdline_args - all                            10.09               4.73
statistics_tab about household_demographics.hd_demo_sk - all                         8.95               2.82
statistics_tab about household_demographics.hd_income_band_sk - all                 18.22               2.98
statistics_tab about household_demographics.hd_buy_potential - all                  70.08               4.81
statistics_tab about household_demographics.hd_dep_count - all                      14.92               2.66
statistics_tab about household_demographics.hd_vehicle_count - all                  12.11               3.17
statistics_tab about income_band.ib_income_band_sk - all                            26.28               2.76
statistics_tab about income_band.ib_lower_bound - all                               91.45               3.10
statistics_tab about income_band.ib_upper_bound - all                                5.72               2.74
statistics_tab about inventory.inv_date_sk - all                                 13127.06            5224.90
statistics_tab about inventory.inv_item_sk - all                                 14170.30            5599.72
statistics_tab about inventory.inv_warehouse_sk - all                            14345.21            5133.95
statistics_tab about inventory.inv_quantity_on_hand - all                        14383.04            5458.93
statistics_tab about item.i_item_sk - all                                           37.23               6.20
statistics_tab about item.i_item_id - all                                           33.50              20.77
statistics_tab about item.i_rec_start_date - all                                    12.72               9.38
statistics_tab about item.i_rec_end_date - all                                      33.62               8.85
statistics_tab about item.i_item_desc - all                                        288.90              69.91
statistics_tab about item.i_current_price - all                                     23.65               8.30
statistics_tab about item.i_wholesale_cost - all                                    12.18               7.94
statistics_tab about item.i_brand_id - all                                          32.81               8.21
statistics_tab about item.i_brand - all                                            154.90               7.18
statistics_tab about item.i_class_id - all                                          11.85               8.06
statistics_tab about item.i_class - all                                             12.48               7.02
statistics_tab about item.i_category_id - all                                       29.45               8.26
statistics_tab about item.i_category - all                                          46.23               6.37
statistics_tab about item.i_manufact_id - all                                       11.64               6.56
statistics_tab about item.i_manufact - all                                          15.09               7.35
statistics_tab about item.i_size - all                                              29.48               6.84
statistics_tab about item.i_formulation - all                                       69.49              27.06
statistics_tab about item.i_color - all                                             24.84               6.67
statistics_tab about item.i_units - all                                             31.96               6.37
statistics_tab about item.i_container - all                                        128.36               6.88
statistics_tab about item.i_manager_id - all                                        28.00              42.62
statistics_tab about item.i_product_name - all                                     136.59              71.66
statistics_tab about promotion.p_promo_sk - all                                     90.07               3.31
statistics_tab about promotion.p_promo_id - all                                     10.15               5.02
statistics_tab about promotion.p_start_date_sk - all                                34.49               3.45
statistics_tab about promotion.p_end_date_sk - all                                  12.19               3.09
statistics_tab about promotion.p_item_sk - all                                       5.57               3.93
statistics_tab about promotion.p_cost - all                                          5.49               3.08
statistics_tab about promotion.p_response_target - all                               5.53               3.36
statistics_tab about promotion.p_promo_name - all                                  102.12               5.62
statistics_tab about promotion.p_channel_dmail - all                                22.33               5.22
statistics_tab about promotion.p_channel_email - all                                50.19               4.82
statistics_tab about promotion.p_channel_catalog - all                              11.63               4.63
statistics_tab about promotion.p_channel_tv - all                                   25.87               5.30
statistics_tab about promotion.p_channel_radio - all                                59.18               5.28
statistics_tab about promotion.p_channel_press - all                                35.13               8.90
statistics_tab about promotion.p_channel_event - all                                37.39               4.61
statistics_tab about promotion.p_channel_demo - all                                 64.52               4.63
statistics_tab about promotion.p_channel_details - all                              28.23               4.56
statistics_tab about promotion.p_purpose - all                                      47.44               6.55
statistics_tab about promotion.p_discount_active - all                              15.33               4.58
statistics_tab about reason.r_reason_sk - all                                       20.96               3.15
statistics_tab about reason.r_reason_id - all                                       26.16               4.76
statistics_tab about reason.r_reason_desc - all                                     43.48               4.77
statistics_tab about ship_mode.sm_ship_mode_sk - all                                21.25               2.83
statistics_tab about ship_mode.sm_ship_mode_id - all                                40.35               4.45
statistics_tab about ship_mode.sm_type - all                                        28.25               4.77
statistics_tab about ship_mode.sm_code - all                                        26.90               4.62
statistics_tab about ship_mode.sm_carrier - all                                     25.61               4.98
statistics_tab about ship_mode.sm_contract - all                                    32.27               4.70
statistics_tab about store.s_store_sk - all                                          5.94               3.16
statistics_tab about store.s_store_id - all                                        203.52               5.22
statistics_tab about store.s_rec_start_date - all                                    7.80               4.39
statistics_tab about store.s_rec_end_date - all                                      7.73               4.35
statistics_tab about store.s_closed_date_sk - all                                    5.66               2.73
statistics_tab about store.s_store_name - all                                       91.91               4.82
statistics_tab about store.s_number_employees - all                                  6.35               2.91
statistics_tab about store.s_floor_space - all                                       6.23               2.90
statistics_tab about store.s_hours - all                                            72.53               6.90
statistics_tab about store.s_manager - all                                          11.44               4.83
statistics_tab about store.s_market_id - all                                        52.66               2.59
statistics_tab about store.s_geography_class - all                                  10.11               4.47
statistics_tab about store.s_market_desc - all                                      10.31               4.62
statistics_tab about store.s_market_manager - all                                   37.60               4.73
statistics_tab about store.s_division_id - all                                     187.23               2.67
statistics_tab about store.s_division_name - all                                    17.83               4.56
statistics_tab about store.s_company_id - all                                        6.01               2.70
statistics_tab about store.s_company_name - all                                     10.36               4.49
statistics_tab about store.s_street_number - all                                    33.77               4.49
statistics_tab about store.s_street_name - all                                      33.34               4.88
statistics_tab about store.s_street_type - all                                      16.98               4.56
statistics_tab about store.s_suite_number - all                                     10.62               4.69
statistics_tab about store.s_city - all                                             36.71               4.68
statistics_tab about store.s_county - all                                           33.63               4.76
statistics_tab about store.s_state - all                                            13.88               4.41
statistics_tab about store.s_zip - all                                              23.40               4.31
statistics_tab about store.s_country - all                                          10.39               4.39
statistics_tab about store.s_gmt_offset - all                                       24.10               2.70
statistics_tab about store.s_tax_precentage - all                                    6.05               2.64
statistics_tab about store_returns.sr_returned_date_sk - all                       355.85             123.92
statistics_tab about store_returns.sr_return_time_sk - all                         656.84             138.45
statistics_tab about store_returns.sr_item_sk - all                                458.09             158.98
statistics_tab about store_returns.sr_customer_sk - all                            450.31             257.68
statistics_tab about store_returns.sr_cdemo_sk - all                               735.14             533.44
statistics_tab about store_returns.sr_hdemo_sk - all                               331.28             114.86
statistics_tab about store_returns.sr_addr_sk - all                                318.37             202.13
statistics_tab about store_returns.sr_store_sk - all                               291.98             108.39
statistics_tab about store_returns.sr_reason_sk - all                              456.11             111.83
statistics_tab about store_returns.sr_ticket_number - all                          282.73             164.25
statistics_tab about store_returns.sr_return_quantity - all                        259.42             141.97
statistics_tab about store_returns.sr_return_amt - all                             466.67             245.88
statistics_tab about store_returns.sr_return_tax - all                             272.79             134.23
statistics_tab about store_returns.sr_return_amt_inc_tax - all                     374.31             239.38
statistics_tab about store_returns.sr_fee - all                                    260.30             130.81
statistics_tab about store_returns.sr_return_ship_cost - all                       368.60             182.21
statistics_tab about store_returns.sr_refunded_cash - all                          417.66             201.49
statistics_tab about store_returns.sr_reversed_charge - all                        304.32             181.29
statistics_tab about store_returns.sr_store_credit - all                           323.00             169.41
statistics_tab about store_returns.sr_net_loss - all                               443.03             215.79
statistics_tab about store_sales.ss_sold_date_sk - all                            2797.29            1142.29
statistics_tab about store_sales.ss_sold_time_sk - all                            2879.22            1304.33
statistics_tab about store_sales.ss_item_sk - all                                 3283.02            1389.47
statistics_tab about store_sales.ss_customer_sk - all                             3418.22            1660.86
statistics_tab about store_sales.ss_cdemo_sk - all                                3024.28            1682.47
statistics_tab about store_sales.ss_hdemo_sk - all                                2907.36            1171.26
statistics_tab about store_sales.ss_addr_sk - all                                 3017.83            1581.61
statistics_tab about store_sales.ss_store_sk - all                                2684.17            1153.38
statistics_tab about store_sales.ss_promo_sk - all                                2939.35            1275.74
statistics_tab about store_sales.ss_ticket_number - all                           3280.78            1344.90
statistics_tab about store_sales.ss_quantity - all                                2723.69            1217.24
statistics_tab about store_sales.ss_wholesale_cost - all                          2954.86            1266.23
statistics_tab about store_sales.ss_list_price - all                              3210.15            1333.69
statistics_tab about store_sales.ss_sales_price - all                             2968.55            1294.32
statistics_tab about store_sales.ss_ext_discount_amt - all                        3512.83            1837.83
statistics_tab about store_sales.ss_ext_sales_price - all                         4299.06            3522.88
statistics_tab about store_sales.ss_ext_wholesale_cost - all                      4680.98            3070.14
statistics_tab about store_sales.ss_ext_list_price - all                          5985.31            4123.39
statistics_tab about store_sales.ss_ext_tax - all                                 3119.77            1552.07
statistics_tab about store_sales.ss_coupon_amt - all                              3464.24            1884.92
statistics_tab about store_sales.ss_net_paid - all                                4605.40            3356.75
statistics_tab about store_sales.ss_net_paid_inc_tax - all                        5396.76            3640.68
statistics_tab about store_sales.ss_net_profit - all                              7500.73            6000.52
statistics_tab about time_dim.t_time_sk - all                                       10.34               6.93
statistics_tab about time_dim.t_time_id - all                                      111.52              27.13
statistics_tab about time_dim.t_time - all                                          50.05               6.57
statistics_tab about time_dim.t_hour - all                                          31.15               5.90
statistics_tab about time_dim.t_minute - all                                        37.22               5.44
statistics_tab about time_dim.t_second - all                                         9.80               6.51
statistics_tab about time_dim.t_am_pm - all                                        120.18               5.65
statistics_tab about time_dim.t_shift - all                                         25.95               5.49
statistics_tab about time_dim.t_sub_shift - all                                     23.99               6.41
statistics_tab about time_dim.t_meal_time - all                                     29.67               6.10
statistics_tab about warehouse.w_warehouse_sk - all                                  5.29               2.43
statistics_tab about warehouse.w_warehouse_id - all                                 88.94               4.15
statistics_tab about warehouse.w_warehouse_name - all                               21.49               4.34
statistics_tab about warehouse.w_warehouse_sq_ft - all                               5.92               2.63
statistics_tab about warehouse.w_street_number - all                                38.30               4.10
statistics_tab about warehouse.w_street_name - all                                  39.23               4.36
statistics_tab about warehouse.w_street_type - all                                  92.10               4.18
statistics_tab about warehouse.w_suite_number - all                                  9.62               4.13
statistics_tab about warehouse.w_city - all                                          9.68               4.00
statistics_tab about warehouse.w_county - all                                       30.71               4.33
statistics_tab about warehouse.w_state - all                                         9.76               4.38
statistics_tab about warehouse.w_zip - all                                          20.53               4.27
statistics_tab about warehouse.w_country - all                                      28.25               4.18
statistics_tab about warehouse.w_gmt_offset - all                                   22.38               2.55
statistics_tab about web_page.wp_web_page_sk - all                                  19.56               2.67
statistics_tab about web_page.wp_web_page_id - all                                  34.68               4.14
statistics_tab about web_page.wp_rec_start_date - all                                7.39               4.16
statistics_tab about web_page.wp_rec_end_date - all                                 10.78               4.01
statistics_tab about web_page.wp_creation_date_sk - all                              6.42               2.71
statistics_tab about web_page.wp_access_date_sk - all                               12.32               3.56
statistics_tab about web_page.wp_autogen_flag - all                                 68.37               4.53
statistics_tab about web_page.wp_customer_sk - all                                  33.36               2.72
statistics_tab about web_page.wp_url - all                                          24.98               4.37
statistics_tab about web_page.wp_type - all                                         42.04               4.47
statistics_tab about web_page.wp_char_count - all                                   17.58               2.72
statistics_tab about web_page.wp_link_count - all                                    7.61               3.06
statistics_tab about web_page.wp_image_count - all                                  16.36               2.88
statistics_tab about web_page.wp_max_ad_count - all                                  5.68               2.96
statistics_tab about web_returns.wr_returned_date_sk - all                          91.61              37.80
statistics_tab about web_returns.wr_returned_time_sk - all                         116.35              42.39
statistics_tab about web_returns.wr_item_sk - all                                  152.26              48.74
statistics_tab about web_returns.wr_refunded_customer_sk - all                     106.38              65.88
statistics_tab about web_returns.wr_refunded_cdemo_sk - all                        170.08             129.46
statistics_tab about web_returns.wr_refunded_hdemo_sk - all                         90.69              33.99
statistics_tab about web_returns.wr_refunded_addr_sk - all                         122.64              61.01
statistics_tab about web_returns.wr_returning_customer_sk - all                    138.29              61.41
statistics_tab about web_returns.wr_returning_cdemo_sk - all                       103.68              76.40
statistics_tab about web_returns.wr_returning_hdemo_sk - all                        74.31              31.83
statistics_tab about web_returns.wr_returning_addr_sk - all                        131.09              49.55
statistics_tab about web_returns.wr_web_page_sk - all                              137.18              32.95
statistics_tab about web_returns.wr_reason_sk - all                                 49.43              28.41
statistics_tab about web_returns.wr_order_number - all                              95.74              27.54
statistics_tab about web_returns.wr_return_quantity - all                           47.95              29.17
statistics_tab about web_returns.wr_return_amt - all                               136.57              58.04
statistics_tab about web_returns.wr_return_tax - all                               114.92              38.73
statistics_tab about web_returns.wr_return_amt_inc_tax - all                       156.38              65.95
statistics_tab about web_returns.wr_fee - all                                      109.19              31.69
statistics_tab about web_returns.wr_return_ship_cost - all                         116.10              54.21
statistics_tab about web_returns.wr_refunded_cash - all                            129.47              56.60
statistics_tab about web_returns.wr_reversed_charge - all                          125.58              46.02
statistics_tab about web_returns.wr_account_credit - all                            53.82              49.88
statistics_tab about web_returns.wr_net_loss - all                                 104.93              53.62
statistics_tab about web_sales.ws_sold_date_sk - all                               970.11             304.70
statistics_tab about web_sales.ws_sold_time_sk - all                               632.79             335.88
statistics_tab about web_sales.ws_ship_date_sk - all                               715.78             302.36
statistics_tab about web_sales.ws_item_sk - all                                    733.33             372.56
statistics_tab about web_sales.ws_bill_customer_sk - all                           794.39             407.48
statistics_tab about web_sales.ws_bill_cdemo_sk - all                              977.44             410.07
statistics_tab about web_sales.ws_bill_hdemo_sk - all                              758.85             291.34
statistics_tab about web_sales.ws_bill_addr_sk - all                               732.34             368.09
statistics_tab about web_sales.ws_ship_customer_sk - all                           757.72             421.50
statistics_tab about web_sales.ws_ship_cdemo_sk - all                              731.64             412.17
statistics_tab about web_sales.ws_ship_hdemo_sk - all                              652.35             278.01
statistics_tab about web_sales.ws_ship_addr_sk - all                               982.78             399.66
statistics_tab about web_sales.ws_web_page_sk - all                                774.22             312.59
statistics_tab about web_sales.ws_web_site_sk - all                                814.56             324.00
statistics_tab about web_sales.ws_ship_mode_sk - all                               868.82             298.84
statistics_tab about web_sales.ws_warehouse_sk - all                               879.79             321.69
statistics_tab about web_sales.ws_promo_sk - all                                   614.46             283.95
statistics_tab about web_sales.ws_order_number - all                               458.91             252.17
statistics_tab about web_sales.ws_quantity - all                                   871.57             337.28
statistics_tab about web_sales.ws_wholesale_cost - all                             756.37             273.64
statistics_tab about web_sales.ws_list_price - all                                 629.10             343.38
statistics_tab about web_sales.ws_sales_price - all                                612.55             302.05
statistics_tab about web_sales.ws_ext_discount_amt - all                          1234.75             935.18
statistics_tab about web_sales.ws_ext_sales_price - all                           1369.45             770.37
statistics_tab about web_sales.ws_ext_wholesale_cost - all                        1333.00             757.63
statistics_tab about web_sales.ws_ext_list_price - all                            1425.32            1086.45
statistics_tab about web_sales.ws_ext_tax - all                                    723.98             399.79
statistics_tab about web_sales.ws_coupon_amt - all                                 819.73             429.50
statistics_tab about web_sales.ws_ext_ship_cost - all                             1138.71             656.40
statistics_tab about web_sales.ws_net_paid - all                                  1364.71             849.48
statistics_tab about web_sales.ws_net_paid_inc_tax - all                          1391.74             863.56
statistics_tab about web_sales.ws_net_paid_inc_ship - all                         1428.22            1036.74
statistics_tab about web_sales.ws_net_paid_inc_ship_tax - all                     1193.93             945.00
statistics_tab about web_sales.ws_net_profit - all                                1572.04            1159.02
statistics_tab about web_site.web_site_sk - all                                     30.68               4.04
statistics_tab about web_site.web_site_id - all                                    101.58               5.13
statistics_tab about web_site.web_rec_start_date - all                              19.59               5.06
statistics_tab about web_site.web_rec_end_date - all                                22.76               4.88
statistics_tab about web_site.web_name - all                                        45.65               4.54
statistics_tab about web_site.web_open_date_sk - all                                15.66               3.05
statistics_tab about web_site.web_close_date_sk - all                               37.07               3.69
statistics_tab about web_site.web_class - all                                       58.92              22.39
statistics_tab about web_site.web_manager - all                                     44.06               6.48
statistics_tab about web_site.web_mkt_id - all                                       6.81               3.28
statistics_tab about web_site.web_mkt_class - all                                   63.42               4.93
statistics_tab about web_site.web_mkt_desc - all                                    28.06               5.67
statistics_tab about web_site.web_market_manager - all                              24.77               5.68
statistics_tab about web_site.web_company_id - all                                  13.48               3.21
statistics_tab about web_site.web_company_name - all                                81.17               5.10
statistics_tab about web_site.web_street_number - all                               22.85               5.16
statistics_tab about web_site.web_street_name - all                                 28.70               4.76
statistics_tab about web_site.web_street_type - all                                 10.42               4.87
statistics_tab about web_site.web_suite_number - all                                10.10               5.31
statistics_tab about web_site.web_city - all                                        21.85               5.40
statistics_tab about web_site.web_county - all                                      12.77               5.41
statistics_tab about web_site.web_state - all                                       25.79               5.30
statistics_tab about web_site.web_zip - all                                         38.35               7.34
statistics_tab about web_site.web_country - all                                     16.39               6.39
statistics_tab about web_site.web_gmt_offset - all                                  32.99               2.86
statistics_tab about web_site.web_tax_percentage - all                               6.11               3.32

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          339.0         9.0      695.0    1051.0
MonetDB-BHT-8-2-1           1.0          339.0         9.0      695.0    1051.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.10
MonetDB-BHT-8-2-1           0.03

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1          354429.69
MonetDB-BHT-8-2-1         1236591.34

### Throughput@Size
                                              time [s]  count  SF  Throughput@Size [~GB/h]
DBMS            SF num_experiment num_client                                              
MonetDB-BHT-8-1 10 1              1                301      1  10                  2631.23
MonetDB-BHT-8-2 10 1              2                157      1  10                  5044.59

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      385.43     1.81          1.89                 11.8
MonetDB-BHT-8-2      361.42     2.54          9.10                 13.1

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       25.63     0.07          0.25                 0.27
MonetDB-BHT-8-2       25.63     0.00          0.50                 0.54

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






## Example: MonetDB TPC-DS@100

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



### Generate and Load Data

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
  -t 7200 -dt \
  -rst shared -rss 300Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_monetdb_1.log &
```


### Status Database and Benchmark

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

### Summary of Results

At the end of a benchmark you will see a summary like

doc_tpcds_monetdb_1.log
```bash
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 13117s 
    Code: 1731443469
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 7200.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 500Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352155532
    datadisk:323280316
    volume_size:500G
    volume_used:309G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                3977.58
TPC-DS Q2               17384.02
TPC-DS Q3                5168.18
TPC-DS Q4              184584.63
TPC-DS Q5               51097.76
TPC-DS Q6               12621.57
TPC-DS Q7                8077.35
TPC-DS Q8               46097.48
TPC-DS Q9                7052.68
TPC-DS Q10              24790.37
TPC-DS Q11              82027.21
TPC-DS Q12               2124.69
TPC-DS Q13               9384.45
TPC-DS Q14a+b          363748.34
TPC-DS Q15               2160.49
TPC-DS Q16               7483.69
TPC-DS Q17             111541.94
TPC-DS Q18              24667.27
TPC-DS Q19               7784.94
TPC-DS Q20               1137.78
TPC-DS Q21               4425.45
TPC-DS Q22              98260.60
TPC-DS Q23a+b         2196591.57
TPC-DS Q24a+b          451613.98
TPC-DS Q25              28300.73
TPC-DS Q26               2363.96
TPC-DS Q27              37048.68
TPC-DS Q28               6486.65
TPC-DS Q29              17075.58
TPC-DS Q30               4569.33
TPC-DS Q31              26897.11
TPC-DS Q32               1494.90
TPC-DS Q33               9898.11
TPC-DS Q34               2324.71
TPC-DS Q35              12144.28
TPC-DS Q36              12921.38
TPC-DS Q37              14521.68
TPC-DS Q38              64601.86
TPC-DS Q39a+b           81761.26
TPC-DS Q40              13298.16
TPC-DS Q41                 28.28
TPC-DS Q42               3286.65
TPC-DS Q43               1283.46
TPC-DS Q44                192.90
TPC-DS Q45               1996.05
TPC-DS Q46               3975.10
TPC-DS Q47               8047.82
TPC-DS Q48               3077.32
TPC-DS Q49              19676.25
TPC-DS Q50               5506.01
TPC-DS Q51              47738.73
TPC-DS Q52               4660.72
TPC-DS Q53               2581.62
TPC-DS Q54              12764.94
TPC-DS Q55               2163.44
TPC-DS Q56              11108.39
TPC-DS Q57               1983.69
TPC-DS Q58              12059.22
TPC-DS Q59              13378.30
TPC-DS Q60               2777.83
TPC-DS Q61               5049.56
TPC-DS Q62               2461.30
TPC-DS Q63               2120.53
TPC-DS Q64              71980.05
TPC-DS Q65              24200.06
TPC-DS Q66              15389.70
TPC-DS Q67             120844.40
TPC-DS Q68               4832.98
TPC-DS Q69               7260.66
TPC-DS Q70               6350.04
TPC-DS Q71               3727.16
TPC-DS Q72              22622.18
TPC-DS Q73               4333.65
TPC-DS Q74              25569.79
TPC-DS Q75             141933.40
TPC-DS Q76              61149.38
TPC-DS Q77              28583.39
TPC-DS Q78             203927.50
TPC-DS Q79              12952.43
TPC-DS Q80             150508.84
TPC-DS Q81               2888.61
TPC-DS Q82              60326.83
TPC-DS Q83               4198.52
TPC-DS Q84               1978.71
TPC-DS Q85               5263.93
TPC-DS Q86               9732.69
TPC-DS Q87              57722.86
TPC-DS Q88               7182.01
TPC-DS Q89               4266.72
TPC-DS Q90               1668.58
TPC-DS Q91               1259.29
TPC-DS Q92               1693.92
TPC-DS Q93              26996.48
TPC-DS Q94               9621.58
TPC-DS Q95              16178.75
TPC-DS Q96               2167.87
TPC-DS Q97              44732.91
TPC-DS Q98               3540.66
TPC-DS Q99               3674.52

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0         1572.0         5.0     5760.0    7346.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          10.66

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           34173.49

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               5452      1  100                  1452.68

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     22216.3    17.05         23.06                77.22

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      1934.2     1.43         46.97                95.38

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    36588.49    58.65        408.05               479.37

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       51.25     0.18          0.34                 0.35

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

### Perform Benchmark - Power Test

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
  -t 7200 -dt \
  -rst shared -rss 300Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_monetdb_2.log &
```

### Evaluate Results

doc_tpcds_monetdb_2.log
```bash
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 27392s 
    Code: 1731457093
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 7200.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 500Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352155636
    datadisk:329919870
    volume_size:500G
    volume_used:315G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352155976
    datadisk:324691593
    volume_size:500G
    volume_used:316G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352156316
    datadisk:324691595
    volume_size:500G
    volume_used:310G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:352156656
    datadisk:324691596
    volume_size:500G
    volume_used:310G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q1                 10042.83              3142.23             10066.88              3106.77
TPC-DS Q2                 38941.88             15221.96             37757.17             14824.72
TPC-DS Q3                 86152.05             49772.01             91159.66             44731.60
TPC-DS Q4                280885.78            164190.88            286666.18            172818.27
TPC-DS Q5                187593.44             36049.82            205495.44             35878.49
TPC-DS Q6                 11155.97              9205.10             11981.31             10068.37
TPC-DS Q7                 91499.99              6222.42             99746.70              7403.79
TPC-DS Q8                 28529.43             27814.84             30964.75             27327.52
TPC-DS Q9                 20413.45              7078.24             20975.67              7141.95
TPC-DS Q10               310701.94              4726.84            317842.08              4764.86
TPC-DS Q11                80958.04             80707.20             83997.91             80224.78
TPC-DS Q12                 1557.36              1468.54              1854.46              1524.94
TPC-DS Q13                 3279.95              6345.54              9428.36              5342.05
TPC-DS Q14a+b            328629.87            289573.01            346603.23            317076.54
TPC-DS Q15                 1198.75              1141.26              2572.32              1671.84
TPC-DS Q16                20492.62              2500.10             20345.71              2391.60
TPC-DS Q17                55439.96             46887.60             63496.67             85714.70
TPC-DS Q18                25551.22             21728.05             23217.82             23278.58
TPC-DS Q19                 3303.20              2273.43              3011.99              4223.77
TPC-DS Q20                 1119.25               542.63              1222.06              1013.35
TPC-DS Q21                84854.21              5123.28             88569.15              4834.70
TPC-DS Q22                99613.49             88131.05            100370.52             92833.07
TPC-DS Q23a+b           3092717.58           2995302.50           3650757.98           3336709.77
TPC-DS Q24a+b            264477.61            264066.18            263438.51            255409.33
TPC-DS Q25                21620.90             22624.07             22503.89             21699.67
TPC-DS Q26                 2617.10              1905.62              2771.65              3101.46
TPC-DS Q27                19320.31             20145.53             20491.50             35080.52
TPC-DS Q28                 4987.18              5176.54              5159.88              5262.15
TPC-DS Q29                37262.69             35118.51             24962.49             29726.66
TPC-DS Q30                 3157.56              2617.68              2993.22              2370.24
TPC-DS Q31                26124.20             26269.90             22075.62             21878.51
TPC-DS Q32                 1867.46              1130.99              1335.18              1545.65
TPC-DS Q33                13231.11              5728.70              1567.42              7221.50
TPC-DS Q34                 4082.24              2374.89              2345.54              3247.86
TPC-DS Q35                16233.54             15759.48              8075.05             15905.18
TPC-DS Q36                32499.33             33827.07             17889.56             11981.64
TPC-DS Q37                24663.16              9341.11             11582.14             23849.47
TPC-DS Q38                63332.96             60565.18             62859.91             47671.33
TPC-DS Q39a+b            128982.49             77365.62             74252.36            128500.54
TPC-DS Q40                 6020.77              5255.56              5361.19              6193.66
TPC-DS Q41                  374.92               375.43               349.16               262.82
TPC-DS Q42                 4786.15              3433.94              4058.70              3454.72
TPC-DS Q43                 2729.13              2672.01              2810.49              2288.61
TPC-DS Q44                46051.42             43953.90             48506.05             42922.52
TPC-DS Q45                 3204.80              1752.25              1981.56              1970.14
TPC-DS Q46                 6603.64              5962.95              6941.91              5491.72
TPC-DS Q47                 7303.30              7476.95             10587.58              7134.99
TPC-DS Q48                 3969.03              3613.91              4569.20              3772.23
TPC-DS Q49                43389.10             25201.64             46138.10             27188.42
TPC-DS Q50                 7831.25              4968.77              8852.95              8686.45
TPC-DS Q51                49185.36             51153.55             48884.66             48338.78
TPC-DS Q52                 4685.09              3957.21              4809.77              3715.90
TPC-DS Q53                 3237.10              2755.29              3419.08              2818.72
TPC-DS Q54                12911.58               843.33             12218.18             11616.70
TPC-DS Q55                 1187.22               137.84              1213.45               931.26
TPC-DS Q56                28470.57             16073.42             17949.09             21736.21
TPC-DS Q57                 2477.18              1638.65              2209.00              2313.56
TPC-DS Q58                11721.32              5405.34              6271.57             10224.70
TPC-DS Q59                12982.20             11904.19             13186.38             12071.46
TPC-DS Q60                 3105.21              4547.07              3686.25              2595.11
TPC-DS Q61                  294.78               283.63               483.92               345.34
TPC-DS Q62                 2795.81              2316.54              2714.24              2693.73
TPC-DS Q63                 2037.15              2337.53              3433.96              1627.89
TPC-DS Q64                75201.74             67313.12             71450.21             58697.14
TPC-DS Q65                22822.27             22580.22             23365.80             25123.18
TPC-DS Q66                23858.73             17720.11             19497.85             18461.09
TPC-DS Q67               123815.67            128032.23            125112.47            127174.29
TPC-DS Q68                 7787.53              4242.00              3767.74              7801.41
TPC-DS Q69                13047.73              6999.57             13120.27             12667.00
TPC-DS Q70                 6620.94              4934.47              6482.53              4258.97
TPC-DS Q71                 5560.56              5344.54              5528.70              4871.44
TPC-DS Q72                21778.54             18940.42             20479.85             21657.24
TPC-DS Q73                 4930.95              3681.16              2275.21              4476.78
TPC-DS Q74                32767.41             31481.66             28188.10             27366.61
TPC-DS Q75               159530.36            129357.12            147711.82            165584.57
TPC-DS Q76                71612.24             71624.21             69445.23             69871.08
TPC-DS Q77                27300.99             26833.67             26490.84             24393.92
TPC-DS Q78               200308.90            194687.76            199010.08            178800.85
TPC-DS Q79                11819.46             11353.41             10708.80             11273.51
TPC-DS Q80               115257.62            119283.36            115940.39             97591.82
TPC-DS Q81                 3566.42              3234.76              3467.94              3075.99
TPC-DS Q82                53321.08             50213.70             50808.41             54344.65
TPC-DS Q83                 3140.56              2721.72              2725.85              2993.31
TPC-DS Q84                 1378.39               756.11               940.35              1172.78
TPC-DS Q85                 3649.66              2783.87              3486.61              3024.29
TPC-DS Q86                 9469.77              9615.71              9611.84              9518.13
TPC-DS Q87                70336.52             70123.90             57991.45             58439.67
TPC-DS Q88                 9570.35              6034.67              7032.46              8503.33
TPC-DS Q89                 4844.72              4033.63              3798.53              4468.22
TPC-DS Q90                 1376.42               963.74              1166.89              1156.22
TPC-DS Q91                 1174.76               915.00              1287.03              1070.36
TPC-DS Q92                 1997.35              1762.89              2255.26              2414.42
TPC-DS Q93                21644.82             20215.81             22430.29             18995.41
TPC-DS Q94                 4569.07              4076.63              4078.65              3907.82
TPC-DS Q95                15080.58             15031.61             15250.04             16359.60
TPC-DS Q96                 7146.36              4265.69              3901.74              4987.36
TPC-DS Q97                47546.39             42913.71             47851.72             45226.89
TPC-DS Q98                 7070.69              5057.15              4754.93              4437.88
TPC-DS Q99                 3728.52              2602.84              2969.50              3426.07

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0         1572.0         5.0     5760.0    7346.0
MonetDB-BHT-8-1-2-1           1.0         1572.0         5.0     5760.0    7346.0
MonetDB-BHT-8-2-1-1           1.0         1572.0         5.0     5760.0    7346.0
MonetDB-BHT-8-2-2-1           1.0         1572.0         5.0     5760.0    7346.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1          13.79
MonetDB-BHT-8-1-2-1           9.36
MonetDB-BHT-8-2-1-1          12.72
MonetDB-BHT-8-2-2-1          10.61

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           26319.01
MonetDB-BHT-8-1-2-1           38884.44
MonetDB-BHT-8-2-1-1           28565.42
MonetDB-BHT-8-2-2-1           34315.93

### Throughput@Size
                                                 time [s]  count   SF  Throughput@Size [~GB/h]
DBMS              SF  num_experiment num_client                                               
MonetDB-BHT-8-1-1 100 1              1               7065      1  100                  1121.02
MonetDB-BHT-8-1-2 100 1              2               5843      1  100                  1355.47
MonetDB-BHT-8-2-1 100 2              1               7521      1  100                  1053.05
MonetDB-BHT-8-2-2 100 2              2               6302      1  100                  1256.74

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1    31061.13    54.22        296.38               317.47
MonetDB-BHT-8-1-2    30906.08    57.92        305.11               331.89
MonetDB-BHT-8-2-1    62141.22    19.61        293.91               313.24
MonetDB-BHT-8-2-2    31748.58    43.41        299.14               302.68

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       61.75     0.10          0.40                 0.41
MonetDB-BHT-8-1-2       61.75     0.24          0.64                 0.67
MonetDB-BHT-8-2-1       62.25     0.21          0.63                 0.67
MonetDB-BHT-8-2-2       62.42     0.22          0.65                 0.68

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

### Perform Benchmark - Throughput Test

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
  -t 7200 -dt \
  -rst shared -rss 300Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_monetdb_3.log &
```

### Evaluate Results

doc_tpcds_monetdb_3.log
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

