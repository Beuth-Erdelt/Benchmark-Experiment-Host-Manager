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

```bash
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 24807s 
    Code: 1730998769
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 3600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 10Gi.
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
    disk:315628068
    datadisk:4318681
    volume_size:10G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:315907364
    datadisk:3149141
    volume_size:10G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:315906840
    datadisk:8487572
    volume_size:10G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:315907364
    datadisk:5845688
    volume_size:10G
    volume_used:5.6G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
            MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q4               False              False             False                  True
TPC-DS Q16               True              False             False                 False
TPC-DS Q35              False              False             False                  True
TPC-DS Q36              False               True             False                 False
TPC-DS Q86              False               True             False                 False
TPC-DS Q94               True              False             False                 False
TPC-DS Q95               True              False             False                 False
TPC-DS Q4
PostgreSQL-BHT-8-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
TPC-DS Q16
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=45) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q35
PostgreSQL-BHT-8-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
TPC-DS Q36
MonetDB-BHT-8-1-1: numRun 1: : 
TPC-DS Q86
MonetDB-BHT-8-1-1: numRun 1: : 
TPC-DS Q94
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=45) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q95
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=45) Query execution was interrupted (max_statement_time exceeded)

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
TPC-DS Q15              False              False              True                  True
TPC-DS Q16              False               True              True                  True
TPC-DS Q18              False               True              True                  True
TPC-DS Q19              False               True              True                  True
TPC-DS Q20              False              False              True                 False
TPC-DS Q21              False               True              True                  True
TPC-DS Q22              False               True              True                  True
TPC-DS Q25              False              False              True                 False
TPC-DS Q26              False              False              True                 False
TPC-DS Q27              False               True             False                  True
TPC-DS Q28              False              False              True                 False
TPC-DS Q29              False              False              True                 False
TPC-DS Q30              False              False              True                 False
TPC-DS Q31              False              False              True                 False
TPC-DS Q32              False              False              True                 False
TPC-DS Q33              False              False              True                 False
TPC-DS Q35              False              False              True                 False
TPC-DS Q36              False              False              True                  True
TPC-DS Q37              False              False              True                 False
TPC-DS Q38              False              False              True                 False
TPC-DS Q40              False              False              True                 False
TPC-DS Q41              False              False              True                 False
TPC-DS Q42              False              False              True                 False
TPC-DS Q44              False               True              True                  True
TPC-DS Q45              False              False              True                 False
TPC-DS Q47              False              False              True                 False
TPC-DS Q48              False              False              True                 False
TPC-DS Q49              False              False              True                 False
TPC-DS Q50              False              False              True                 False
TPC-DS Q51              False              False              True                 False
TPC-DS Q52              False               True              True                  True
TPC-DS Q53              False              False              True                 False
TPC-DS Q55              False               True              True                  True
TPC-DS Q57              False              False              True                 False
TPC-DS Q60              False              False              True                 False
TPC-DS Q62              False               True              True                  True
TPC-DS Q63              False              False              True                 False
TPC-DS Q64              False               True              True                  True
TPC-DS Q65              False              False              True                 False
TPC-DS Q66              False               True              True                  True
TPC-DS Q67              False              False              True                  True
TPC-DS Q69              False              False              True                 False
TPC-DS Q70              False               True              True                 False
TPC-DS Q71              False               True              True                  True
TPC-DS Q72              False              False              True                  True
TPC-DS Q74              False              False              True                 False
TPC-DS Q75              False               True              True                  True
TPC-DS Q76              False              False              True                 False
TPC-DS Q77              False              False              True                 False
TPC-DS Q78              False               True              True                  True
TPC-DS Q79              False              False              True                 False
TPC-DS Q80              False               True              True                  True
TPC-DS Q81              False              False              True                 False
TPC-DS Q82              False              False              True                 False
TPC-DS Q83              False               True              True                  True
TPC-DS Q84              False               True              True                  True
TPC-DS Q86              False              False              True                  True
TPC-DS Q87              False              False              True                 False
TPC-DS Q88              False              False              True                 False
TPC-DS Q90              False              False              True                 False
TPC-DS Q91              False               True              True                  True
TPC-DS Q92              False              False              True                 False
TPC-DS Q93              False              False              True                  True
TPC-DS Q94              False               True              True                  True
TPC-DS Q95              False               True              True                  True
TPC-DS Q96              False              False              True                 False
TPC-DS Q97              False               True              True                  True
TPC-DS Q98              False               True              True                 False
TPC-DS Q99              False              False              True                 False

### Latency of Timer Execution [ms]
DBMS           MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q1                 234.89             546.17             90.33                224.88
TPC-DS Q2               15733.01             225.20             15.09                941.55
TPC-DS Q3                 124.45             276.69              3.25                263.96
TPC-DS Q5               32044.60             910.59             15.13               1408.92
TPC-DS Q6                2952.45             135.14              3.28             166434.35
TPC-DS Q7               17655.72             874.35              3.82               1006.64
TPC-DS Q8               15684.37             195.32              4.62                609.42
TPC-DS Q9               13741.03              72.62              3.91               6251.91
TPC-DS Q10              21689.41            1745.88              4.98             284378.99
TPC-DS Q11              73544.50             626.28             10.64             432507.83
TPC-DS Q12                969.24              24.60              2.73                140.99
TPC-DS Q13               3394.49             167.73              4.24                578.62
TPC-DS Q14a+b          255379.21            2802.04             24.09              32314.36
TPC-DS Q15               9258.48              28.86              1.99                262.98
TPC-DS Q17               2964.39             173.35              2.98                326.26
TPC-DS Q18              11092.89             264.56              2.58                712.99
TPC-DS Q19                157.53              40.99              2.06                365.87
TPC-DS Q20               1710.96              27.25              2.07                205.40
TPC-DS Q21              80649.85             995.14              3.16                651.06
TPC-DS Q22                289.66            1891.36              1.73               9651.71
TPC-DS Q23a+b          305703.27            2712.64             11.46              13935.91
TPC-DS Q24a+b             202.78             533.10              8.21                605.77
TPC-DS Q25               2550.50             135.92              4.19                519.95
TPC-DS Q26               9085.62              63.30              2.14                590.01
TPC-DS Q27              16129.08             127.42              2.49                 60.84
TPC-DS Q28              10142.61              64.77              3.32               4582.77
TPC-DS Q29               2365.61             107.11              2.12                360.55
TPC-DS Q30               1087.73              26.70              3.48               2934.66
TPC-DS Q31              73575.99             165.00              7.25              12493.45
TPC-DS Q32                 17.29              17.28              1.83               1817.02
TPC-DS Q33              17871.82              65.93              4.54              68404.81
TPC-DS Q34               3471.98             110.17              2.31                 62.60
TPC-DS Q37              13917.62             200.02              1.88                894.17
TPC-DS Q38              26933.80             194.85              2.02               3003.07
TPC-DS Q39a+b          314649.13            1726.96              7.84               7257.92
TPC-DS Q40                742.29              43.50              2.22                321.60
TPC-DS Q41               1905.34               9.24              4.72               3126.81
TPC-DS Q42                241.66              19.98              1.84                354.27
TPC-DS Q43              11848.38              56.83              2.45                 57.91
TPC-DS Q44                  2.26              32.50              2.73                363.56
TPC-DS Q45               6531.64              27.03              2.13                205.81
TPC-DS Q46               6634.46              61.70              2.52                 59.59
TPC-DS Q47              63809.07             322.25              5.93               4130.72
TPC-DS Q48               4842.44              90.49              2.55                760.71
TPC-DS Q49                385.44             409.44              4.51               1282.20
TPC-DS Q50               2177.33             224.65              2.93                101.79
TPC-DS Q51              26141.03             573.01              3.88               2962.69
TPC-DS Q52                243.09              23.76              1.79                347.87
TPC-DS Q53                570.09              26.21              2.07                425.54
TPC-DS Q54              24100.34              26.06              3.16                146.66
TPC-DS Q55                 52.54              16.89              1.55                345.15
TPC-DS Q56                931.19              28.02              3.32               1685.83
TPC-DS Q57              33756.39             114.87              3.64               1844.09
TPC-DS Q58              23395.79              43.70              3.08                851.18
TPC-DS Q59              38293.21              95.51              3.03               1139.08
TPC-DS Q60               4482.14              24.32              3.28               8329.23
TPC-DS Q61               1607.11              81.09              2.30                310.62
TPC-DS Q62               7338.44              32.03              2.48                277.92
TPC-DS Q63                550.30              26.66              1.75                413.34
TPC-DS Q64               2147.96             416.90              6.44                831.68
TPC-DS Q65              22494.64              86.88              1.64               1536.94
TPC-DS Q66              14467.77             271.82              4.74                693.65
TPC-DS Q67              28196.42             675.60              1.66               3083.72
TPC-DS Q68               6239.14              38.24              1.64                 58.28
TPC-DS Q69              22372.43              39.85              1.84                477.95
TPC-DS Q70              33113.76             461.29              1.76               1191.98
TPC-DS Q71              19338.94              30.66              1.95               5149.30
TPC-DS Q72            1438669.73             433.61              1.88               3843.29
TPC-DS Q73               3512.66              25.28              1.69                 59.30
TPC-DS Q74              65301.95             184.69              3.54            1837094.25
TPC-DS Q75               5778.79             665.48              3.61               2482.34
TPC-DS Q76               1588.71              35.89              1.75                704.01
TPC-DS Q77              24184.88              73.77              4.26                920.29
TPC-DS Q78              45076.74             771.53              2.87               3191.72
TPC-DS Q79               9777.07              46.53              1.55                814.98
TPC-DS Q80               2253.20             460.16              3.36               4130.29
TPC-DS Q81               3332.93             112.75              2.22             125318.26
TPC-DS Q82              14135.94             191.22              1.51                957.50
TPC-DS Q83               3468.11              20.96              2.51                265.98
TPC-DS Q84                168.33             129.73              1.41                 92.87
TPC-DS Q85                342.85              38.11              2.02                178.26
TPC-DS Q87              26928.49             278.90              1.59               2932.82
TPC-DS Q88              42140.24             111.23              4.73               7550.98
TPC-DS Q89                 33.87              36.84              1.66                 61.55
TPC-DS Q90                401.79              14.24              1.66                257.42
TPC-DS Q91               1622.58             147.60              2.01                155.84
TPC-DS Q92                 18.97              14.44              1.64               6215.01
TPC-DS Q93                 98.23              99.19              1.56                136.40
TPC-DS Q96               2253.33              14.08              1.32                317.86
TPC-DS Q97              18796.60             228.94              2.00               1010.71
TPC-DS Q98               3441.29              40.94              1.67                311.42
TPC-DS Q99              16934.55              75.98              1.71                410.62

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1              0.0          635.0         4.0     8580.0    9228.0
MonetDB-BHT-8-1-1              1.0          108.0         6.0       43.0     167.0
MySQL-BHT-64-1-1               1.0           13.0         6.0      119.0     150.0
PostgreSQL-BHT-8-1-1           1.0          134.0         2.0       84.0     229.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              4.40
MonetDB-BHT-8-1-1              0.12
MySQL-BHT-64-1-1               0.00
PostgreSQL-BHT-8-1-1           1.10

### Power@Size
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1                819.98
MonetDB-BHT-8-1-1              32521.87
MySQL-BHT-64-1-1             1206858.79
PostgreSQL-BHT-8-1-1            3319.55

### Throughput@Size
                                                 time [s]  count  SF  Throughput@Size [~GB/h]
DBMS               SF num_experiment num_client                                              
MariaDB-BHT-8-1    1  1              1              14455      1   1                     5.48
MonetDB-BHT-8-1    1  1              1                 44      1   1                  1800.00
MySQL-BHT-64-1     1  1              1                  4      1   1                 19800.00
PostgreSQL-BHT-8-1 1  1              1              10327      1   1                     7.67

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

```bash
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 822s 
    Code: 1731082481
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
    disk:347859424
    datadisk:3147733
    volume_size:30G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:347859364
    datadisk:3276631
    volume_size:30G
    volume_used:3.2G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
            MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q36                 True                 True
TPC-DS Q86                 True                 True
TPC-DS Q36
MonetDB-BHT-8-1-1-1: numRun 1: : 
MonetDB-BHT-8-2-1-1: numRun 1: : 
TPC-DS Q86
MonetDB-BHT-8-1-1-1: numRun 1: : 
MonetDB-BHT-8-2-1-1: numRun 1: : 

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q1                   168.84               565.43
TPC-DS Q2                   287.59               679.23
TPC-DS Q3                   282.97               467.61
TPC-DS Q4                  2518.67              2728.85
TPC-DS Q5                   649.96              3015.32
TPC-DS Q6                   184.92               462.35
TPC-DS Q7                  1183.94              1298.37
TPC-DS Q8                   152.81               328.03
TPC-DS Q9                   186.18               164.67
TPC-DS Q10                 2791.51              2760.26
TPC-DS Q11                  619.74               609.30
TPC-DS Q12                   70.78               166.07
TPC-DS Q13                  182.39               177.18
TPC-DS Q14a+b              2240.61              2248.29
TPC-DS Q15                   24.24                27.30
TPC-DS Q16                  646.58               682.15
TPC-DS Q17                  182.57               603.97
TPC-DS Q18                  346.90               176.36
TPC-DS Q19                   47.03                90.23
TPC-DS Q20                   27.07                27.68
TPC-DS Q21                 1258.18              1627.85
TPC-DS Q22                 1849.55              1936.32
TPC-DS Q23a+b              2122.79              2256.81
TPC-DS Q24a+b               635.78               409.56
TPC-DS Q25                  108.43               118.79
TPC-DS Q26                   50.48               416.18
TPC-DS Q27                  144.51               146.58
TPC-DS Q28                   64.86                63.41
TPC-DS Q29                  116.74               109.34
TPC-DS Q30                   30.11               187.22
TPC-DS Q31                  158.54               607.93
TPC-DS Q32                   17.13                25.19
TPC-DS Q33                  174.20                36.88
TPC-DS Q34                  106.55               342.44
TPC-DS Q35                   74.08               925.96
TPC-DS Q37                  144.53               174.75
TPC-DS Q38                  209.40               192.61
TPC-DS Q39a+b              1396.28              1867.91
TPC-DS Q40                   56.06                60.85
TPC-DS Q41                   10.52                 9.08
TPC-DS Q42                   20.76                25.77
TPC-DS Q43                   67.03                54.90
TPC-DS Q44                   90.88                80.48
TPC-DS Q45                   25.99                28.12
TPC-DS Q46                  116.69               107.87
TPC-DS Q47                  238.03               294.97
TPC-DS Q48                  106.16               105.47
TPC-DS Q49                  131.09              1351.96
TPC-DS Q50                  129.38               188.98
TPC-DS Q51                  582.73               601.34
TPC-DS Q52                   20.19                21.67
TPC-DS Q53                   27.26                27.55
TPC-DS Q54                   22.55                22.65
TPC-DS Q55                   16.53                16.23
TPC-DS Q56                   27.58                44.58
TPC-DS Q57                  124.34                87.33
TPC-DS Q58                   48.19                57.48
TPC-DS Q59                  108.11               122.73
TPC-DS Q60                   65.98                23.54
TPC-DS Q61                   66.39               122.68
TPC-DS Q62                   81.81               537.52
TPC-DS Q63                   27.85                27.02
TPC-DS Q64                  682.90               786.95
TPC-DS Q65                   80.21               113.05
TPC-DS Q66                  247.82               444.34
TPC-DS Q67                  649.55               667.30
TPC-DS Q68                   37.20                40.16
TPC-DS Q69                   27.27                28.58
TPC-DS Q70                  162.72               366.32
TPC-DS Q71                   30.91                37.48
TPC-DS Q72                 1086.50               529.90
TPC-DS Q73                   25.54                26.12
TPC-DS Q74                  176.75               178.95
TPC-DS Q75                  638.06               661.88
TPC-DS Q76                   35.94                37.20
TPC-DS Q77                   67.06                93.31
TPC-DS Q78                  762.11               875.07
TPC-DS Q79                  132.88                71.34
TPC-DS Q80                  431.28               420.46
TPC-DS Q81                  202.50                57.89
TPC-DS Q82                  182.42               177.76
TPC-DS Q83                   55.39               241.31
TPC-DS Q84                   86.85                97.76
TPC-DS Q85                   87.58               101.64
TPC-DS Q87                  271.64               268.04
TPC-DS Q88                  112.71               357.29
TPC-DS Q89                   37.67                37.54
TPC-DS Q90                   12.45                16.90
TPC-DS Q91                  120.52                37.53
TPC-DS Q92                   13.58                14.60
TPC-DS Q93                   95.07                90.28
TPC-DS Q94                   19.48               306.54
TPC-DS Q95                  130.32               134.48
TPC-DS Q96                   18.17                13.98
TPC-DS Q97                  252.89               237.52
TPC-DS Q98                   40.00                40.22
TPC-DS Q99                  349.07               306.37

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0          102.0         6.0       47.0     163.0
MonetDB-BHT-8-2-1-1           1.0          102.0         6.0       47.0     163.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.13
MonetDB-BHT-8-2-1-1           0.17

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           28980.04
MonetDB-BHT-8-2-1-1           22306.10

### Throughput@Size
                                                time [s]  count  SF  Throughput@Size [~GB/h]
DBMS              SF num_experiment num_client                                              
MonetDB-BHT-8-1-1 1  1              1                 45      1   1                  1760.00
MonetDB-BHT-8-2-1 1  2              1                107      1   1                   740.19

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1], [1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1], [1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST failed: SQL errors
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

