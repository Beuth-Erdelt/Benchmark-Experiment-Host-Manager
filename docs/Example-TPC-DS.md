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
nohup python tpcds.py -ms 1 -dt -tr \
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
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 1205s 
    Code: 1748357389
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
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
    disk:312594112
    datadisk:165
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748357389
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:312156252
    datadisk:5600
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748357389
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:315320580
    datadisk:8290
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748357389
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:306844676
    datadisk:5804
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748357389

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q3                  False               True             False                  True
TPC-DS Q4                  False               True             False                  True
TPC-DS Q5                  False               True             False                  True
TPC-DS Q6                  False               True             False                  True
TPC-DS Q7                  False               True             False                  True
TPC-DS Q9                  False               True             False                  True
TPC-DS Q10                 False               True             False                  True
TPC-DS Q11                 False               True             False                  True
TPC-DS Q12                 False               True             False                  True
TPC-DS Q13                 False               True             False                  True
TPC-DS Q14a+b              False               True             False                  True
TPC-DS Q15                 False               True             False                  True
TPC-DS Q17                 False               True             False                  True
TPC-DS Q18                 False               True             False                  True
TPC-DS Q19                 False               True             False                  True
TPC-DS Q20                 False               True             False                  True
TPC-DS Q21                 False               True             False                  True
TPC-DS Q22                 False               True             False                  True
TPC-DS Q25                 False               True             False                  True
TPC-DS Q26                 False               True             False                  True
TPC-DS Q27                 False               True             False                  True
TPC-DS Q28                 False               True             False                  True
TPC-DS Q30                 False               True             False                  True
TPC-DS Q31                 False               True             False                  True
TPC-DS Q32                 False               True             False                  True
TPC-DS Q33                 False               True             False                  True
TPC-DS Q35                 False               True             False                  True
TPC-DS Q36                 False               True             False                  True
TPC-DS Q37                 False               True             False                  True
TPC-DS Q38                 False               True             False                  True
TPC-DS Q39a+b              False               True              True                  True
TPC-DS Q40                 False               True             False                  True
TPC-DS Q41                 False               True             False                  True
TPC-DS Q42                 False               True             False                  True
TPC-DS Q44                 False               True             False                  True
TPC-DS Q45                 False               True             False                  True
TPC-DS Q46                 False               True             False                  True
TPC-DS Q47                 False               True             False                  True
TPC-DS Q48                 False               True             False                  True
TPC-DS Q49                 False               True             False                  True
TPC-DS Q50                 False               True             False                  True
TPC-DS Q51                 False               True             False                  True
TPC-DS Q52                 False               True             False                  True
TPC-DS Q53                 False               True             False                  True
TPC-DS Q55                 False               True             False                  True
TPC-DS Q56                 False               True             False                  True
TPC-DS Q57                 False               True             False                  True
TPC-DS Q60                 False               True             False                  True
TPC-DS Q62                 False               True             False                  True
TPC-DS Q63                 False               True             False                  True
TPC-DS Q64                 False               True             False                  True
TPC-DS Q65                 False               True             False                  True
TPC-DS Q66                 False               True             False                  True
TPC-DS Q67                 False               True             False                  True
TPC-DS Q69                 False               True             False                  True
TPC-DS Q70                 False               True             False                  True
TPC-DS Q71                 False               True             False                  True
TPC-DS Q72                 False               True             False                  True
TPC-DS Q74                 False               True             False                  True
TPC-DS Q75                 False               True             False                  True
TPC-DS Q76                 False               True             False                  True
TPC-DS Q77                 False               True             False                  True
TPC-DS Q78                 False               True             False                  True
TPC-DS Q79                 False               True             False                  True
TPC-DS Q80                 False               True             False                  True
TPC-DS Q81                 False               True             False                  True
TPC-DS Q82                 False               True             False                  True
TPC-DS Q83                 False               True             False                  True
TPC-DS Q84                 False               True             False                  True
TPC-DS Q85                 False               True             False                  True
TPC-DS Q86                 False               True             False                  True
TPC-DS Q87                 False               True             False                  True
TPC-DS Q88                 False               True             False                  True
TPC-DS Q89                 False               True             False                  True
TPC-DS Q90                 False               True             False                  True
TPC-DS Q91                 False               True             False                  True
TPC-DS Q92                 False               True             False                  True
TPC-DS Q93                 False               True             False                  True
TPC-DS Q94                 False               True             False                  True
TPC-DS Q95                 False               True             False                  True
TPC-DS Q96                 False               True             False                  True
TPC-DS Q97                 False               True             False                  True
TPC-DS Q98                 False               True             False                  True
TPC-DS Q99                 False               True             False                  True

### Latency of Timer Execution [ms]
DBMS           MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q1                  21.90              36.53            102.51                272.86
TPC-DS Q2                   3.00             185.99              9.64                885.29
TPC-DS Q3                   1.80             100.01              3.76                485.42
TPC-DS Q4                   7.81            1287.65             24.34              15763.61
TPC-DS Q5                   2.86             251.14              9.84               1454.51
TPC-DS Q6                   1.45              97.06              2.70             195769.23
TPC-DS Q7                   1.29              67.99              2.48               1091.75
TPC-DS Q8                   2.43              43.44              3.64                148.25
TPC-DS Q9                   1.84              70.30              3.03               6179.49
TPC-DS Q10                  2.45              57.16              3.74               3024.89
TPC-DS Q11                  3.62             655.54              7.99              11505.92
TPC-DS Q12                  1.42              23.81             17.05                207.75
TPC-DS Q13                  2.11             126.79              2.63               1910.02
TPC-DS Q14a+b               9.22            2611.46             17.26               7862.42
TPC-DS Q15                  1.54              34.25              1.79                328.44
TPC-DS Q16                  2.02              46.90              2.87                708.01
TPC-DS Q17                  2.52             185.90              2.93               1032.28
TPC-DS Q18                  2.20             126.81              2.53               1223.69
TPC-DS Q19                  2.16              40.75              1.90                460.09
TPC-DS Q20                  1.90              27.47              1.62                311.68
TPC-DS Q21                  2.09              68.15              2.82                707.06
TPC-DS Q22                  1.65            1097.26              1.79              10079.91
TPC-DS Q23a+b               6.39            2069.42              8.69              10923.88
TPC-DS Q24a+b               4.34             255.16              5.37               1246.86
TPC-DS Q25                  2.15             124.52              1.96               1032.74
TPC-DS Q26                  1.77              24.36              1.40                718.75
TPC-DS Q27                  2.69             120.97              1.84                140.53
TPC-DS Q28                  2.35              65.69              2.72               4795.53
TPC-DS Q29                  2.15             121.72              2.04               1076.78
TPC-DS Q30                  2.49              28.76              2.80              28499.49
TPC-DS Q31                  3.62             152.87              5.27               6106.62
TPC-DS Q32                  1.67              18.52              1.39                247.65
TPC-DS Q33                  2.24              25.79              3.70               1053.37
TPC-DS Q34                  2.78              27.39              1.73                 68.92
TPC-DS Q35                  2.58              95.34              2.49               3309.00
TPC-DS Q36                  2.03             144.05              1.69               2157.43
TPC-DS Q37                  1.62             118.44              1.22                839.86
TPC-DS Q38                  1.88             207.39              1.68               3365.95
TPC-DS Q39a+b               5.07            1172.42              5.97               7333.16
TPC-DS Q40                  1.77              77.97              1.52                341.32
TPC-DS Q41                  1.76               9.49              2.33               3071.48
TPC-DS Q42                  1.18              21.64              2.28                268.24
TPC-DS Q43                  1.36              48.71              2.33                 64.56
TPC-DS Q44                  1.65              91.54              3.15               1387.95
TPC-DS Q45                  1.35              28.30              2.45                209.28
TPC-DS Q46                  2.08              58.30              2.99                646.16
TPC-DS Q47                  2.98             240.60              6.33               4133.60
TPC-DS Q48                  1.67             101.66              3.17               1852.73
TPC-DS Q49                  2.95             122.17              4.90               2129.06
TPC-DS Q50                  1.83              99.98              2.68                692.06
TPC-DS Q51                  2.03             628.91              3.63               2855.69
TPC-DS Q52                  1.54              20.17              1.76                269.50
TPC-DS Q53                  1.71              28.23              2.59                311.39
TPC-DS Q54                  2.21              23.32              3.58                216.39
TPC-DS Q55                  1.52              19.24              2.16                270.98
TPC-DS Q56                  2.72              30.57              6.62               1163.22
TPC-DS Q57                  2.95              90.78              5.01               2023.48
TPC-DS Q58                  2.49              45.74              4.93               1355.18
TPC-DS Q59                  2.32             120.77              6.77               1237.94
TPC-DS Q60                  2.71              42.72              5.13               1141.79
TPC-DS Q61                  2.33              37.37              2.57               3358.25
TPC-DS Q62                  2.00              26.35              3.24                298.89
TPC-DS Q63                  2.45              32.50              2.37                324.38
TPC-DS Q64                  4.93             411.70              6.80               2262.71
TPC-DS Q65                  1.72             109.31              2.26               1615.30
TPC-DS Q66                  3.28             100.24              5.20                584.04
TPC-DS Q67                  1.76             696.21              2.39               7014.87
TPC-DS Q68                  1.49              45.51              2.59                 60.44
TPC-DS Q69                  2.40              46.04              2.70                734.99
TPC-DS Q70                  2.31              77.05              2.14               1220.64
TPC-DS Q71                  2.01              43.47              2.77                969.36
TPC-DS Q72                  2.12             174.16              2.59               2923.54
TPC-DS Q73                  1.86              25.95              2.65                 68.05
TPC-DS Q74                  3.05             219.26              4.07               4275.47
TPC-DS Q75                  3.29             656.24              5.79               2446.02
TPC-DS Q76                  1.87              84.61              2.69                680.76
TPC-DS Q77                  2.86              68.57              5.25               5262.14
TPC-DS Q78                  2.38             911.66              3.83               5055.72
TPC-DS Q79                  1.92              57.14              2.44                544.63
TPC-DS Q80                  2.92             457.37              3.54               1459.89
TPC-DS Q81                  2.09              42.69              2.34             120064.91
TPC-DS Q82                  1.54             162.37              1.84                928.82
TPC-DS Q83                  2.35              18.05              2.98                291.77
TPC-DS Q84                  1.58              39.50              1.74                264.04
TPC-DS Q85                  2.05              39.12              3.27               1339.50
TPC-DS Q86                  1.54              29.69              2.62                478.23
TPC-DS Q87                  2.51             290.15              2.63               3312.53
TPC-DS Q88                  3.56              97.49              5.84               6841.30
TPC-DS Q89                  1.88              39.51              2.45                316.61
TPC-DS Q90                  1.82              18.95              2.02               2166.51
TPC-DS Q91                  1.70              27.27              2.99                268.79
TPC-DS Q92                  1.41              14.80              1.84               1899.10
TPC-DS Q93                  1.49             101.10              3.36                373.82
TPC-DS Q94                  1.65              19.02              1.91                441.36
TPC-DS Q95                  1.94             152.56              1.98               9522.98
TPC-DS Q96                  1.21              14.32              1.34                277.50
TPC-DS Q97                  1.83             254.88              2.77               1022.39
TPC-DS Q98                  1.53              46.02              1.88                489.58
TPC-DS Q99                  1.52              59.78              1.60                418.97

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1              1.0            4.0         4.0      125.0     143.0
MonetDB-BHT-8-1-1              1.0          104.0         9.0       92.0     213.0
MySQL-BHT-64-1-1               1.0           11.0         8.0      122.0     149.0
PostgreSQL-BHT-8-1-1           1.0          145.0         1.0      142.0     297.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              0.00
MonetDB-BHT-8-1-1              0.09
MySQL-BHT-64-1-1               0.00
PostgreSQL-BHT-8-1-1           1.18

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1            1611522.34
MonetDB-BHT-8-1-1              43670.41
MySQL-BHT-64-1-1             1126744.64
PostgreSQL-BHT-8-1-1            3084.91

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
MariaDB-BHT-8-1    1  1              1                 11      1   1         32400.00
MonetDB-BHT-8-1    1  1              1                 38      1   1          9378.95
MySQL-BHT-64-1     1  1              1                  4      1   1         89100.00
PostgreSQL-BHT-8-1 1  1              1                569      1   1           626.36

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
  -sf 10 \
  -t 1200 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_monitoring.log &
```

If monitoring is activated, the summary also contains a section like this:

doc_tpcds_testcase_monitoring.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 888s 
    Code: 1748358770
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
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
    disk:314090284
    datadisk:12892
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748358770

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                  80.50
TPC-DS Q2                 529.56
TPC-DS Q3                  62.08
TPC-DS Q4                4502.64
TPC-DS Q5                 956.12
TPC-DS Q6                 289.11
TPC-DS Q7                 112.88
TPC-DS Q8                 142.04
TPC-DS Q9                 173.16
TPC-DS Q10                116.82
TPC-DS Q11               2077.35
TPC-DS Q12                 45.35
TPC-DS Q13                228.51
TPC-DS Q14a+b            7106.75
TPC-DS Q15                 75.40
TPC-DS Q16                335.89
TPC-DS Q17                711.30
TPC-DS Q18                324.69
TPC-DS Q19                 95.47
TPC-DS Q20                 60.81
TPC-DS Q21                107.80
TPC-DS Q22               3400.54
TPC-DS Q23a+b            7581.13
TPC-DS Q24a+b            1165.39
TPC-DS Q25                577.06
TPC-DS Q26                 92.65
TPC-DS Q27                474.24
TPC-DS Q28                204.69
TPC-DS Q29                553.92
TPC-DS Q30                 45.89
TPC-DS Q31                620.44
TPC-DS Q32                 49.87
TPC-DS Q33                 56.59
TPC-DS Q34                 67.81
TPC-DS Q35                258.44
TPC-DS Q36                313.73
TPC-DS Q37                261.93
TPC-DS Q38                784.55
TPC-DS Q39a+b            3494.23
TPC-DS Q40                310.12
TPC-DS Q41                 11.37
TPC-DS Q42                 52.24
TPC-DS Q43                179.59
TPC-DS Q44                137.19
TPC-DS Q45                 47.86
TPC-DS Q46                125.35
TPC-DS Q47                633.76
TPC-DS Q48                203.14
TPC-DS Q49                305.92
TPC-DS Q50                259.73
TPC-DS Q51               2250.12
TPC-DS Q52                 46.94
TPC-DS Q53                 70.32
TPC-DS Q54                 61.75
TPC-DS Q55                 40.77
TPC-DS Q56                 79.15
TPC-DS Q57                250.45
TPC-DS Q58                129.78
TPC-DS Q59                450.25
TPC-DS Q60                 69.90
TPC-DS Q61                 91.11
TPC-DS Q62                 63.01
TPC-DS Q63                 61.48
TPC-DS Q64               1443.05
TPC-DS Q65                504.92
TPC-DS Q66                298.74
TPC-DS Q67               2888.01
TPC-DS Q68                109.31
TPC-DS Q69                 54.79
TPC-DS Q70                234.20
TPC-DS Q71                 78.56
TPC-DS Q72                360.59
TPC-DS Q73                 68.75
TPC-DS Q74                655.56
TPC-DS Q75               2762.70
TPC-DS Q76                212.11
TPC-DS Q77                201.36
TPC-DS Q78               4093.02
TPC-DS Q79                139.37
TPC-DS Q80               2676.81
TPC-DS Q81                 63.59
TPC-DS Q82                108.71
TPC-DS Q83                 39.57
TPC-DS Q84                127.33
TPC-DS Q85                123.37
TPC-DS Q86                 86.23
TPC-DS Q87               1113.49
TPC-DS Q88                263.51
TPC-DS Q89                 81.08
TPC-DS Q90                 30.35
TPC-DS Q91                 32.19
TPC-DS Q92                 30.71
TPC-DS Q93                508.38
TPC-DS Q94                 90.07
TPC-DS Q95                274.36
TPC-DS Q96                 31.60
TPC-DS Q97               1143.17
TPC-DS Q98                108.30
TPC-DS Q99                123.28

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          294.0         9.0      230.0     541.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.23

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           50246.87

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MonetDB-BHT-8-1 3  1              1                 83      1   3         12881.93

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      748.32     2.09           4.5                14.27

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       56.37     0.22          1.12                 2.28

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      314.58     0.42          7.98                17.07

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       21.61     0.14          0.26                 0.27

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
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 590s 
    Code: 1748359790
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:306624692
    datadisk:5602
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748359790
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:306682912
    datadisk:5659
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748359790
MonetDB-BHT-8-2-2 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:306682912
    datadisk:5659
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748359790

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-2-2
TPC-DS Q39a+b              False               True               True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-2-2
TPC-DS Q1                  49.47             146.64              42.82
TPC-DS Q2                 179.67             131.43             136.87
TPC-DS Q3                  25.90              26.27              22.43
TPC-DS Q4                1260.68            1279.07            1282.52
TPC-DS Q5                 258.63             246.35             250.21
TPC-DS Q6                  84.78              64.09              67.03
TPC-DS Q7                  54.70              47.83              54.17
TPC-DS Q8                  42.96              61.98              43.50
TPC-DS Q9                  55.35              51.28              50.14
TPC-DS Q10                 47.82              31.71              40.65
TPC-DS Q11                627.49             557.56             667.35
TPC-DS Q12                 26.98              20.80              22.27
TPC-DS Q13                138.62              89.35              96.32
TPC-DS Q14a+b            2316.95            2091.20            2165.90
TPC-DS Q15                 26.73              21.71              21.76
TPC-DS Q16                 41.74              39.95              41.12
TPC-DS Q17                181.85             112.75             128.66
TPC-DS Q18                143.66              63.22              57.49
TPC-DS Q19                 42.70              45.36              43.43
TPC-DS Q20                 28.48              27.32              52.50
TPC-DS Q21                 74.60              71.05              69.72
TPC-DS Q22               1089.04            1070.70            1121.73
TPC-DS Q23a+b            2813.97            3026.25            2838.14
TPC-DS Q24a+b             332.62             325.38             278.95
TPC-DS Q25                128.49             102.76             154.32
TPC-DS Q26                 24.93              19.79              47.02
TPC-DS Q27                103.70              92.99             103.33
TPC-DS Q28                 68.68              68.11              63.90
TPC-DS Q29                113.48              93.08              98.16
TPC-DS Q30                 17.92              15.27              17.26
TPC-DS Q31                156.87             141.32             131.59
TPC-DS Q32                 18.42              16.01              23.10
TPC-DS Q33                 25.62              21.22              22.78
TPC-DS Q34                 28.14              26.21              25.56
TPC-DS Q35                 84.36              71.35              85.58
TPC-DS Q36                102.35              85.81              69.41
TPC-DS Q37                116.30              59.13              57.00
TPC-DS Q38                203.38             178.73             204.25
TPC-DS Q39a+b            1495.53            1308.62            1321.85
TPC-DS Q40                 81.38              99.07             112.94
TPC-DS Q41                  9.73               9.13               9.18
TPC-DS Q42                 20.61              19.40              22.95
TPC-DS Q43                 44.93              44.05              47.08
TPC-DS Q44                 33.68              32.33              32.51
TPC-DS Q45                 26.75              29.58              27.32
TPC-DS Q46                 39.38              38.03              51.67
TPC-DS Q47                225.77             238.90             222.09
TPC-DS Q48                102.84              98.84             104.74
TPC-DS Q49                 89.05              93.31              94.26
TPC-DS Q50                 99.44              91.01             103.66
TPC-DS Q51                625.38             574.59             585.06
TPC-DS Q52                 21.68              21.63              19.99
TPC-DS Q53                 33.55              28.91              31.43
TPC-DS Q54                 26.73              24.65              23.24
TPC-DS Q55                 18.78              17.29              17.13
TPC-DS Q56                 26.33              20.73              28.48
TPC-DS Q57                106.67             103.46             100.40
TPC-DS Q58                 59.30              55.54              56.56
TPC-DS Q59                111.02             103.78             100.05
TPC-DS Q60                 25.29              23.13              24.70
TPC-DS Q61                 33.53              32.39              32.91
TPC-DS Q62                 27.52              25.71              81.48
TPC-DS Q63                 26.71              43.77              26.92
TPC-DS Q64                462.21             238.43             222.09
TPC-DS Q65                 94.91              94.92              96.87
TPC-DS Q66                101.15              95.67             102.42
TPC-DS Q67                684.23             677.40             783.58
TPC-DS Q68                 37.68              50.72              38.74
TPC-DS Q69                 43.97              42.58              43.06
TPC-DS Q70                 72.70              83.18              75.69
TPC-DS Q71                 30.97              31.48              31.77
TPC-DS Q72                172.74             148.42             158.88
TPC-DS Q73                 29.96              26.04              24.36
TPC-DS Q74                199.55             187.50             183.47
TPC-DS Q75                699.16             685.26             645.00
TPC-DS Q76                 48.71              44.51              48.86
TPC-DS Q77                 57.52              57.44              58.54
TPC-DS Q78                855.71             835.73             788.17
TPC-DS Q79                 52.62              58.47              47.24
TPC-DS Q80                445.35             419.79             458.99
TPC-DS Q81                 32.32              31.02              31.69
TPC-DS Q82                 71.38              49.88              49.51
TPC-DS Q83                 17.25              14.74              14.38
TPC-DS Q84                 30.78              25.49              15.20
TPC-DS Q85                 39.26              61.23              35.01
TPC-DS Q86                 28.78              25.05              28.48
TPC-DS Q87                280.56             274.57             276.74
TPC-DS Q88                 96.65              96.59              95.74
TPC-DS Q89                 39.84              47.25              37.54
TPC-DS Q90                 24.57              12.71              17.86
TPC-DS Q91                 26.65              24.07              25.76
TPC-DS Q92                 14.04              15.45              15.68
TPC-DS Q93                 96.41              85.74             106.48
TPC-DS Q94                 19.12              20.18              16.79
TPC-DS Q95                118.50             108.23              91.16
TPC-DS Q96                 16.65              15.39              14.65
TPC-DS Q97                258.45             235.23             252.12
TPC-DS Q98                 46.04              47.98              44.72
TPC-DS Q99                 69.42              61.81              53.20

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          109.0         9.0       70.0     197.0
MonetDB-BHT-8-2-1           1.0          109.0         9.0       70.0     197.0
MonetDB-BHT-8-2-2           1.0          109.0         9.0       70.0     197.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.08
MonetDB-BHT-8-2-1           0.08
MonetDB-BHT-8-2-2           0.08

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           46864.96
MonetDB-BHT-8-2-1           50566.29
MonetDB-BHT-8-2-2           49690.12

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MonetDB-BHT-8-1 1  1              1                 40      1   1          8910.00
MonetDB-BHT-8-2 1  1              2                 39      2   1         18276.92

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 2]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 2]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST failed: SQL warnings (result mismatch)
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

```bash
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
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 918s 
    Code: 1748360541
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 10Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:300889240
    datadisk:5597
    volume_size:10G
    volume_used:5.3G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748360541
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:300889176
    datadisk:5654
    volume_size:10G
    volume_used:5.6G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748360541

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q39a+b                False                 True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q1                    46.63               966.94
TPC-DS Q2                   198.61               775.30
TPC-DS Q3                    34.85              1263.19
TPC-DS Q4                  1308.21              3415.42
TPC-DS Q5                   286.99              1196.30
TPC-DS Q6                    88.46               502.87
TPC-DS Q7                    74.27              1963.28
TPC-DS Q8                    72.96               309.12
TPC-DS Q9                    73.15                94.52
TPC-DS Q10                   84.37              8510.05
TPC-DS Q11                  628.53               670.48
TPC-DS Q12                   26.05               302.00
TPC-DS Q13                  117.00               399.34
TPC-DS Q14a+b              2094.44              3165.19
TPC-DS Q15                   25.09                29.51
TPC-DS Q16                   42.41              1157.15
TPC-DS Q17                  147.93               332.66
TPC-DS Q18                  151.43               219.73
TPC-DS Q19                   42.02               228.92
TPC-DS Q20                   33.35                26.97
TPC-DS Q21                  107.32              3838.91
TPC-DS Q22                 1146.76              1243.02
TPC-DS Q23a+b              3065.63              2886.36
TPC-DS Q24a+b               303.07               647.71
TPC-DS Q25                  133.20               116.78
TPC-DS Q26                   26.45                21.17
TPC-DS Q27                  149.90               116.36
TPC-DS Q28                   93.41                71.78
TPC-DS Q29                  123.43               117.32
TPC-DS Q30                   26.51               142.49
TPC-DS Q31                  183.40               177.86
TPC-DS Q32                   20.00                17.78
TPC-DS Q33                   25.11                62.84
TPC-DS Q34                   34.69               233.45
TPC-DS Q35                   89.82                89.99
TPC-DS Q36                   82.53               102.35
TPC-DS Q37                   86.66                75.10
TPC-DS Q38                  223.83               196.33
TPC-DS Q39a+b              1152.03              1222.93
TPC-DS Q40                   86.75                55.12
TPC-DS Q41                   10.60                 8.67
TPC-DS Q42                   21.53                23.32
TPC-DS Q43                   50.69                57.31
TPC-DS Q44                  104.47              1061.03
TPC-DS Q45                   27.46                28.39
TPC-DS Q46                   47.90               477.64
TPC-DS Q47                  279.14               298.96
TPC-DS Q48                  105.67               119.09
TPC-DS Q49                  135.79               436.65
TPC-DS Q50                  112.51               400.99
TPC-DS Q51                  639.02               603.91
TPC-DS Q52                   25.70                19.89
TPC-DS Q53                   31.56                29.31
TPC-DS Q54                   25.30                23.19
TPC-DS Q55                   17.48                16.97
TPC-DS Q56                   34.64               100.97
TPC-DS Q57                   89.87               120.32
TPC-DS Q58                   51.42                54.81
TPC-DS Q59                  125.16               130.58
TPC-DS Q60                   25.00                22.33
TPC-DS Q61                   39.35                70.82
TPC-DS Q62                   63.72               173.57
TPC-DS Q63                   26.47                28.22
TPC-DS Q64                  541.82               736.03
TPC-DS Q65                  109.39               122.59
TPC-DS Q66                   96.42               435.99
TPC-DS Q67                  720.97               673.69
TPC-DS Q68                   40.25                38.64
TPC-DS Q69                   41.72                41.69
TPC-DS Q70                   71.99               758.83
TPC-DS Q71                   33.25                40.70
TPC-DS Q72                  194.98              1469.10
TPC-DS Q73                   28.32                25.96
TPC-DS Q74                  575.94               610.16
TPC-DS Q75                  713.80               719.91
TPC-DS Q76                   87.42               660.74
TPC-DS Q77                   62.50               108.95
TPC-DS Q78                  890.58               847.03
TPC-DS Q79                   61.98               115.44
TPC-DS Q80                  561.80               482.35
TPC-DS Q81                   43.01               333.21
TPC-DS Q82                   67.43               112.57
TPC-DS Q83                   23.49                29.68
TPC-DS Q84                   79.32                68.00
TPC-DS Q85                   45.43                76.65
TPC-DS Q86                   32.17                35.38
TPC-DS Q87                  313.64               272.58
TPC-DS Q88                  111.34               107.51
TPC-DS Q89                   39.95                36.17
TPC-DS Q90                   20.18                14.02
TPC-DS Q91                   30.03               345.52
TPC-DS Q92                   19.67                13.57
TPC-DS Q93                  120.02               103.43
TPC-DS Q94                   24.57                21.47
TPC-DS Q95                  147.74               135.94
TPC-DS Q96                   14.94                14.62
TPC-DS Q97                  288.17               264.40
TPC-DS Q98                   44.26                40.71
TPC-DS Q99                   69.96                62.27

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0          131.0        11.0      101.0     251.0
MonetDB-BHT-8-2-1-1           1.0          131.0        11.0      101.0     251.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.09
MonetDB-BHT-8-2-1-1           0.18

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           41359.09
MonetDB-BHT-8-2-1-1           21997.80

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                time [s]  count  SF  Throughput@Size
DBMS              SF num_experiment num_client                                      
MonetDB-BHT-8-1-1 1  1              1                 38      1   1          9378.95
MonetDB-BHT-8-2-1 1  2              1                130      1   1          2741.54

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1], [1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1], [1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST failed: SQL warnings (result mismatch)
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
```markdown
## Show Summary

### Workload
TPC-DS Data Profiling SF=10
    Type: tpcds
    Duration: 808s 
    Code: 1748410145
    We compute for all columns: Minimum, maximum, average, count, count distinct, count NULL and non NULL entries and coefficient of variation.
    This experiment compares imported TPC-DS data sets in different DBMS.
    TPC-DS (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301206216
    datadisk:40080
    volume_size:50G
    volume_used:40G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748410145
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301206220
    datadisk:40080
    volume_size:50G
    volume_used:40G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748410145

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                                    MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1
statistics_tab about call_center.cc_call_center_sk - all                           112.70              39.00
statistics_tab about call_center.cc_call_center_id - all                            87.18               5.92
statistics_tab about call_center.cc_rec_start_date - all                            11.38               5.37
statistics_tab about call_center.cc_rec_end_date - all                              40.11               5.51
statistics_tab about call_center.cc_closed_date_sk - all                            22.57               3.09
statistics_tab about call_center.cc_open_date_sk - all                              37.15               3.38
statistics_tab about call_center.cc_name - all                                      69.24               5.08
statistics_tab about call_center.cc_class - all                                     64.64               5.96
statistics_tab about call_center.cc_employees - all                                 63.17               3.71
statistics_tab about call_center.cc_sq_ft - all                                     15.07               3.11
statistics_tab about call_center.cc_hours - all                                     66.14               5.53
statistics_tab about call_center.cc_manager - all                                   30.50               5.25
statistics_tab about call_center.cc_mkt_id - all                                    16.62               3.32
statistics_tab about call_center.cc_mkt_class - all                                 50.87               5.68
statistics_tab about call_center.cc_mkt_desc - all                                  55.90               5.18
statistics_tab about call_center.cc_market_manager - all                            49.94               5.23
statistics_tab about call_center.cc_division - all                                  29.09               3.96
statistics_tab about call_center.cc_division_name - all                             33.94               6.73
statistics_tab about call_center.cc_company - all                                   54.65               3.97
statistics_tab about call_center.cc_company_name - all                              67.04               5.51
statistics_tab about call_center.cc_street_number - all                             69.50               5.11
statistics_tab about call_center.cc_street_name - all                               60.74               5.21
statistics_tab about call_center.cc_street_type - all                               22.82               5.29
statistics_tab about call_center.cc_suite_number - all                              38.82               5.58
statistics_tab about call_center.cc_city - all                                      59.42               5.14
statistics_tab about call_center.cc_county - all                                    32.95               4.72
statistics_tab about call_center.cc_state - all                                    130.31               5.96
statistics_tab about call_center.cc_zip - all                                       44.41               5.96
statistics_tab about call_center.cc_country - all                                   14.84               5.47
statistics_tab about call_center.cc_gmt_offset - all                                20.89               3.59
statistics_tab about call_center.cc_tax_percentage - all                            12.22               3.68
statistics_tab about catalog_page.cp_catalog_page_sk - all                          69.92               3.86
statistics_tab about catalog_page.cp_catalog_page_id - all                          50.14               6.97
statistics_tab about catalog_page.cp_start_date_sk - all                            19.56               4.04
statistics_tab about catalog_page.cp_end_date_sk - all                              32.72               5.42
statistics_tab about catalog_page.cp_department - all                              101.78               5.00
statistics_tab about catalog_page.cp_catalog_number - all                           25.46               4.68
statistics_tab about catalog_page.cp_catalog_page_number - all                      19.20               7.55
statistics_tab about catalog_page.cp_description - all                              71.44              10.62
statistics_tab about catalog_page.cp_type - all                                     54.11               5.26
statistics_tab about catalog_returns.cr_returned_date_sk - all                     201.54              56.80
statistics_tab about catalog_returns.cr_returned_time_sk - all                     200.31              85.91
statistics_tab about catalog_returns.cr_item_sk - all                              158.74              84.99
statistics_tab about catalog_returns.cr_refunded_customer_sk - all                 429.20             113.40
statistics_tab about catalog_returns.cr_refunded_cdemo_sk - all                    297.17             160.13
statistics_tab about catalog_returns.cr_refunded_hdemo_sk - all                    175.92              62.03
statistics_tab about catalog_returns.cr_refunded_addr_sk - all                     336.87              96.25
statistics_tab about catalog_returns.cr_returning_customer_sk - all                417.48             128.77
statistics_tab about catalog_returns.cr_returning_cdemo_sk - all                   532.36             197.41
statistics_tab about catalog_returns.cr_returning_hdemo_sk - all                   141.05              63.36
statistics_tab about catalog_returns.cr_returning_addr_sk - all                    189.64             100.19
statistics_tab about catalog_returns.cr_call_center_sk - all                       292.42              53.92
statistics_tab about catalog_returns.cr_catalog_page_sk - all                      223.55              61.17
statistics_tab about catalog_returns.cr_ship_mode_sk - all                         123.21              65.94
statistics_tab about catalog_returns.cr_warehouse_sk - all                         159.13              57.03
statistics_tab about catalog_returns.cr_reason_sk - all                            147.99              54.46
statistics_tab about catalog_returns.cr_order_number - all                         174.68              66.69
statistics_tab about catalog_returns.cr_return_quantity - all                      119.45              54.12
statistics_tab about catalog_returns.cr_return_amount - all                        200.14             125.80
statistics_tab about catalog_returns.cr_return_tax - all                           221.94              76.27
statistics_tab about catalog_returns.cr_return_amt_inc_tax - all                   289.58             125.32
statistics_tab about catalog_returns.cr_fee - all                                  218.76              60.12
statistics_tab about catalog_returns.cr_return_ship_cost - all                     168.08             100.62
statistics_tab about catalog_returns.cr_refunded_cash - all                        186.72             104.37
statistics_tab about catalog_returns.cr_reversed_charge - all                      181.28              97.89
statistics_tab about catalog_returns.cr_store_credit - all                         167.25              84.75
statistics_tab about catalog_returns.cr_net_loss - all                             242.76              98.53
statistics_tab about catalog_sales.cs_sold_date_sk - all                          1689.32             585.53
statistics_tab about catalog_sales.cs_sold_time_sk - all                          1929.51             706.82
statistics_tab about catalog_sales.cs_ship_date_sk - all                          1634.84             603.12
statistics_tab about catalog_sales.cs_bill_customer_sk - all                      1778.08             908.19
statistics_tab about catalog_sales.cs_bill_cdemo_sk - all                         2636.00             867.18
statistics_tab about catalog_sales.cs_bill_hdemo_sk - all                         1623.83             588.63
statistics_tab about catalog_sales.cs_bill_addr_sk - all                          1710.00             758.88
statistics_tab about catalog_sales.cs_ship_customer_sk - all                      2037.14             898.24
statistics_tab about catalog_sales.cs_ship_cdemo_sk - all                         1854.23             918.19
statistics_tab about catalog_sales.cs_ship_hdemo_sk - all                         2526.76             592.18
statistics_tab about catalog_sales.cs_ship_addr_sk - all                          1809.28             824.02
statistics_tab about catalog_sales.cs_call_center_sk - all                        1530.30             567.71
statistics_tab about catalog_sales.cs_catalog_page_sk - all                       1948.03             580.13
statistics_tab about catalog_sales.cs_ship_mode_sk - all                          1516.66             605.35
statistics_tab about catalog_sales.cs_warehouse_sk - all                          1390.40             611.83
statistics_tab about catalog_sales.cs_item_sk - all                               2163.23             719.95
statistics_tab about catalog_sales.cs_promo_sk - all                              1859.47             608.82
statistics_tab about catalog_sales.cs_order_number - all                          1701.32             681.87
statistics_tab about catalog_sales.cs_quantity - all                              1372.68             621.68
statistics_tab about catalog_sales.cs_wholesale_cost - all                        1474.59             637.83
statistics_tab about catalog_sales.cs_list_price - all                            1682.04             695.76
statistics_tab about catalog_sales.cs_sales_price - all                           1696.15             678.78
statistics_tab about catalog_sales.cs_ext_discount_amt - all                      2900.87            1766.89
statistics_tab about catalog_sales.cs_ext_sales_price - all                       2677.49            1621.36
statistics_tab about catalog_sales.cs_ext_wholesale_cost - all                    2696.78            1543.04
statistics_tab about catalog_sales.cs_ext_list_price - all                        3455.93            2436.23
statistics_tab about catalog_sales.cs_ext_tax - all                               1916.85             844.14
statistics_tab about catalog_sales.cs_coupon_amt - all                            1775.94             964.74
statistics_tab about catalog_sales.cs_ext_ship_cost - all                         2258.33            1322.84
statistics_tab about catalog_sales.cs_net_paid - all                              2751.30            1763.91
statistics_tab about catalog_sales.cs_net_paid_inc_tax - all                      2763.24            2035.56
statistics_tab about catalog_sales.cs_net_paid_inc_ship - all                     3019.47            1986.82
statistics_tab about catalog_sales.cs_net_paid_inc_ship_tax - all                 3490.73            2087.81
statistics_tab about catalog_sales.cs_net_profit - all                            4486.38            3154.13
statistics_tab about customer.c_customer_sk - all                                  109.40              13.48
statistics_tab about customer.c_customer_id - all                                  355.48             193.44
statistics_tab about customer.c_current_cdemo_sk - all                              96.12              57.61
statistics_tab about customer.c_current_hdemo_sk - all                              75.45              22.70
statistics_tab about customer.c_current_addr_sk - all                              108.57              65.09
statistics_tab about customer.c_first_shipto_date_sk - all                         163.26              28.81
statistics_tab about customer.c_first_sales_date_sk - all                           64.52              29.82
statistics_tab about customer.c_salutation - all                                    54.18              10.06
statistics_tab about customer.c_first_name - all                                   138.50              55.37
statistics_tab about customer.c_last_name - all                                    181.26              68.58
statistics_tab about customer.c_preferred_cust_flag - all                           82.61              10.83
statistics_tab about customer.c_birth_day - all                                     75.22              26.10
statistics_tab about customer.c_birth_month - all                                  145.44              21.09
statistics_tab about customer.c_birth_year - all                                    91.84              24.44
statistics_tab about customer.c_birth_country - all                                 56.79              11.87
statistics_tab about customer.c_login - all                                         52.73               8.86
statistics_tab about customer.c_email_address - all                                541.08             189.63
statistics_tab about customer.c_last_review_date - all                              88.88              12.33
statistics_tab about customer_address.ca_address_sk - all                           98.05              11.00
statistics_tab about customer_address.ca_address_id - all                          181.41              86.11
statistics_tab about customer_address.ca_street_number - all                        48.76               9.89
statistics_tab about customer_address.ca_street_name - all                         128.24              39.80
statistics_tab about customer_address.ca_street_type - all                         134.16               8.87
statistics_tab about customer_address.ca_suite_number - all                         80.21               8.30
statistics_tab about customer_address.ca_city - all                                112.29               9.14
statistics_tab about customer_address.ca_county - all                               64.33              11.95
statistics_tab about customer_address.ca_state - all                                58.11               9.54
statistics_tab about customer_address.ca_zip - all                                 258.88              37.47
statistics_tab about customer_address.ca_country - all                             393.03               9.19
statistics_tab about customer_address.ca_gmt_offset - all                           56.14              17.51
statistics_tab about customer_address.ca_location_type - all                        64.25               8.70
statistics_tab about customer_demographics.cd_demo_sk - all                         98.36              13.59
statistics_tab about customer_demographics.cd_gender - all                          54.20              23.48
statistics_tab about customer_demographics.cd_marital_status - all                  80.69              21.76
statistics_tab about customer_demographics.cd_education_status - all                94.63              22.46
statistics_tab about customer_demographics.cd_purchase_estimate - all              183.38              96.37
statistics_tab about customer_demographics.cd_credit_rating - all                  104.02              22.32
statistics_tab about customer_demographics.cd_dep_count - all                      170.93              98.97
statistics_tab about customer_demographics.cd_dep_employed_count - all             169.73              75.06
statistics_tab about customer_demographics.cd_dep_college_count - all              142.20             111.54
statistics_tab about date_dim.d_date_sk - all                                       36.97               7.64
statistics_tab about date_dim.d_date_id - all                                       65.24              18.94
statistics_tab about date_dim.d_date - all                                          27.50               7.12
statistics_tab about date_dim.d_month_seq - all                                     29.78               8.14
statistics_tab about date_dim.d_week_seq - all                                     201.19               6.49
statistics_tab about date_dim.d_quarter_seq - all                                   74.55               7.70
statistics_tab about date_dim.d_year - all                                          31.19               5.95
statistics_tab about date_dim.d_dow - all                                           37.93               6.71
statistics_tab about date_dim.d_moy - all                                           33.57               6.02
statistics_tab about date_dim.d_dom - all                                           61.61               6.37
statistics_tab about date_dim.d_qoy - all                                           96.43               5.89
statistics_tab about date_dim.d_fy_year - all                                       59.16               8.84
statistics_tab about date_dim.d_fy_quarter_seq - all                               108.25               8.19
statistics_tab about date_dim.d_fy_week_seq - all                                   39.32               8.15
statistics_tab about date_dim.d_day_name - all                                      43.59               7.01
statistics_tab about date_dim.d_quarter_name - all                                 120.73               8.48
statistics_tab about date_dim.d_holiday - all                                       62.11               7.85
statistics_tab about date_dim.d_weekend - all                                      108.72               6.55
statistics_tab about date_dim.d_following_holiday - all                            110.39               6.28
statistics_tab about date_dim.d_first_dom - all                                     35.18               7.51
statistics_tab about date_dim.d_last_dom - all                                      29.99               6.67
statistics_tab about date_dim.d_same_day_ly - all                                   28.17               7.20
statistics_tab about date_dim.d_same_day_lq - all                                   32.74               7.28
statistics_tab about date_dim.d_current_day - all                                  130.26               6.10
statistics_tab about date_dim.d_current_week - all                                  82.78              10.87
statistics_tab about date_dim.d_current_month - all                                 79.16               6.79
statistics_tab about date_dim.d_current_quarter - all                               28.43               6.31
statistics_tab about date_dim.d_current_year - all                                  72.74               8.60
statistics_tab about dbgen_version.dv_version - all                                 49.79               5.45
statistics_tab about dbgen_version.dv_create_date - all                             23.81               4.89
statistics_tab about dbgen_version.dv_create_time - all                             31.53               4.84
statistics_tab about dbgen_version.dv_cmdline_args - all                            57.33               4.91
statistics_tab about household_demographics.hd_demo_sk - all                        33.85               3.09
statistics_tab about household_demographics.hd_income_band_sk - all                 37.94               7.18
statistics_tab about household_demographics.hd_buy_potential - all                 130.84               5.16
statistics_tab about household_demographics.hd_dep_count - all                      15.97               3.88
statistics_tab about household_demographics.hd_vehicle_count - all                  16.24               3.25
statistics_tab about income_band.ib_income_band_sk - all                            78.19               2.83
statistics_tab about income_band.ib_lower_bound - all                               33.33               3.72
statistics_tab about income_band.ib_upper_bound - all                               19.87               3.16
statistics_tab about inventory.inv_date_sk - all                                 13808.15            5260.30
statistics_tab about inventory.inv_item_sk - all                                 15485.13            5511.30
statistics_tab about inventory.inv_warehouse_sk - all                            15042.62            5093.93
statistics_tab about inventory.inv_quantity_on_hand - all                        15668.53            5504.64
statistics_tab about item.i_item_sk - all                                           30.33               8.98
statistics_tab about item.i_item_id - all                                           57.49              22.90
statistics_tab about item.i_rec_start_date - all                                    26.83               8.96
statistics_tab about item.i_rec_end_date - all                                      38.29               8.75
statistics_tab about item.i_item_desc - all                                        304.93              66.18
statistics_tab about item.i_current_price - all                                     22.88               8.74
statistics_tab about item.i_wholesale_cost - all                                   126.54              10.37
statistics_tab about item.i_brand_id - all                                          30.15               9.23
statistics_tab about item.i_brand - all                                             93.96               7.12
statistics_tab about item.i_class_id - all                                          46.67               8.47
statistics_tab about item.i_class - all                                            183.66               8.01
statistics_tab about item.i_category_id - all                                      136.53               7.65
statistics_tab about item.i_category - all                                          48.66               6.86
statistics_tab about item.i_manufact_id - all                                       63.28               7.23
statistics_tab about item.i_manufact - all                                          75.69               6.56
statistics_tab about item.i_size - all                                             126.14               6.95
statistics_tab about item.i_formulation - all                                      178.59              27.96
statistics_tab about item.i_color - all                                             98.20               7.61
statistics_tab about item.i_units - all                                            137.63               7.37
statistics_tab about item.i_container - all                                         93.62               6.54
statistics_tab about item.i_manager_id - all                                        57.31               7.03
statistics_tab about item.i_product_name - all                                     174.46              38.03
statistics_tab about promotion.p_promo_sk - all                                     35.70               3.05
statistics_tab about promotion.p_promo_id - all                                     68.56               5.00
statistics_tab about promotion.p_start_date_sk - all                                56.63               3.30
statistics_tab about promotion.p_end_date_sk - all                                  21.32               2.72
statistics_tab about promotion.p_item_sk - all                                      34.33               2.77
statistics_tab about promotion.p_cost - all                                         16.27               2.94
statistics_tab about promotion.p_response_target - all                              19.98               3.28
statistics_tab about promotion.p_promo_name - all                                   78.58               4.30
statistics_tab about promotion.p_channel_dmail - all                                44.40               4.50
statistics_tab about promotion.p_channel_email - all                                48.74               4.45
statistics_tab about promotion.p_channel_catalog - all                              61.23               4.35
statistics_tab about promotion.p_channel_tv - all                                   37.29               4.72
statistics_tab about promotion.p_channel_radio - all                                43.40               4.71
statistics_tab about promotion.p_channel_press - all                               455.12               5.04
statistics_tab about promotion.p_channel_event - all                                50.52               4.75
statistics_tab about promotion.p_channel_demo - all                                 75.41               4.72
statistics_tab about promotion.p_channel_details - all                             132.03               4.79
statistics_tab about promotion.p_purpose - all                                      43.29               8.93
statistics_tab about promotion.p_discount_active - all                              38.39               5.58
statistics_tab about reason.r_reason_sk - all                                       40.98               2.93
statistics_tab about reason.r_reason_id - all                                       43.73               4.65
statistics_tab about reason.r_reason_desc - all                                    146.69               4.93
statistics_tab about ship_mode.sm_ship_mode_sk - all                                17.64               3.59
statistics_tab about ship_mode.sm_ship_mode_id - all                                37.63               4.84
statistics_tab about ship_mode.sm_type - all                                        88.90               4.89
statistics_tab about ship_mode.sm_code - all                                        46.23               4.41
statistics_tab about ship_mode.sm_carrier - all                                     34.63               5.24
statistics_tab about ship_mode.sm_contract - all                                    99.41               5.80
statistics_tab about store.s_store_sk - all                                          6.80               3.03
statistics_tab about store.s_store_id - all                                        129.79               5.14
statistics_tab about store.s_rec_start_date - all                                    8.15               4.64
statistics_tab about store.s_rec_end_date - all                                     19.83              11.09
statistics_tab about store.s_closed_date_sk - all                                   17.05               3.22
statistics_tab about store.s_store_name - all                                       99.34               4.62
statistics_tab about store.s_number_employees - all                                 21.22               3.28
statistics_tab about store.s_floor_space - all                                      43.25               3.22
statistics_tab about store.s_hours - all                                            90.67               4.98
statistics_tab about store.s_manager - all                                          18.17               5.05
statistics_tab about store.s_market_id - all                                        54.55               3.25
statistics_tab about store.s_geography_class - all                                  18.84               4.89
statistics_tab about store.s_market_desc - all                                      19.93               4.89
statistics_tab about store.s_market_manager - all                                  146.37               5.33
statistics_tab about store.s_division_id - all                                      78.30               2.76
statistics_tab about store.s_division_name - all                                    19.90               4.33
statistics_tab about store.s_company_id - all                                       27.72               2.66
statistics_tab about store.s_company_name - all                                     57.86               4.72
statistics_tab about store.s_street_number - all                                   215.64               4.57
statistics_tab about store.s_street_name - all                                     113.59               4.86
statistics_tab about store.s_street_type - all                                      49.51               5.58
statistics_tab about store.s_suite_number - all                                     99.15               5.78
statistics_tab about store.s_city - all                                             31.92               4.75
statistics_tab about store.s_county - all                                           82.47               4.60
statistics_tab about store.s_state - all                                            59.79               5.26
statistics_tab about store.s_zip - all                                              39.19               4.68
statistics_tab about store.s_country - all                                          64.20               4.70
statistics_tab about store.s_gmt_offset - all                                       21.23               3.59
statistics_tab about store.s_tax_precentage - all                                    7.65               3.11
statistics_tab about store_returns.sr_returned_date_sk - all                       418.47             129.66
statistics_tab about store_returns.sr_return_time_sk - all                         449.66             129.36
statistics_tab about store_returns.sr_item_sk - all                                477.84             164.00
statistics_tab about store_returns.sr_customer_sk - all                            470.14             261.65
statistics_tab about store_returns.sr_cdemo_sk - all                               645.72             523.39
statistics_tab about store_returns.sr_hdemo_sk - all                               474.45             121.21
statistics_tab about store_returns.sr_addr_sk - all                                362.35             209.89
statistics_tab about store_returns.sr_store_sk - all                               288.16             127.75
statistics_tab about store_returns.sr_reason_sk - all                              697.13             127.28
statistics_tab about store_returns.sr_ticket_number - all                          351.02             157.98
statistics_tab about store_returns.sr_return_quantity - all                        337.69             107.53
statistics_tab about store_returns.sr_return_amt - all                             448.60             241.34
statistics_tab about store_returns.sr_return_tax - all                             296.48             147.03
statistics_tab about store_returns.sr_return_amt_inc_tax - all                     507.68             244.66
statistics_tab about store_returns.sr_fee - all                                    320.13             119.90
statistics_tab about store_returns.sr_return_ship_cost - all                       431.69             199.74
statistics_tab about store_returns.sr_refunded_cash - all                          640.23             202.22
statistics_tab about store_returns.sr_reversed_charge - all                        574.90             171.20
statistics_tab about store_returns.sr_store_credit - all                           740.70             189.04
statistics_tab about store_returns.sr_net_loss - all                               684.20             201.10
statistics_tab about store_sales.ss_sold_date_sk - all                            3177.84            1179.41
statistics_tab about store_sales.ss_sold_time_sk - all                            3154.27            1278.18
statistics_tab about store_sales.ss_item_sk - all                                 2985.53            1412.26
statistics_tab about store_sales.ss_customer_sk - all                             3535.18            1696.84
statistics_tab about store_sales.ss_cdemo_sk - all                                3596.40            1677.64
statistics_tab about store_sales.ss_hdemo_sk - all                                3049.08            1190.35
statistics_tab about store_sales.ss_addr_sk - all                                 3502.70            1572.23
statistics_tab about store_sales.ss_store_sk - all                                3029.17            1170.05
statistics_tab about store_sales.ss_promo_sk - all                                3062.83            1230.85
statistics_tab about store_sales.ss_ticket_number - all                           2855.82            1547.16
statistics_tab about store_sales.ss_quantity - all                                3574.35            1230.64
statistics_tab about store_sales.ss_wholesale_cost - all                          3197.94            1272.84
statistics_tab about store_sales.ss_list_price - all                              3626.31            1312.80
statistics_tab about store_sales.ss_sales_price - all                             3452.03            1298.02
statistics_tab about store_sales.ss_ext_discount_amt - all                        4060.61            1889.29
statistics_tab about store_sales.ss_ext_sales_price - all                         5706.67            3151.15
statistics_tab about store_sales.ss_ext_wholesale_cost - all                      4957.82            3168.46
statistics_tab about store_sales.ss_ext_list_price - all                          6246.81            4141.11
statistics_tab about store_sales.ss_ext_tax - all                                 3619.66            1557.08
statistics_tab about store_sales.ss_coupon_amt - all                              4060.60            1864.47
statistics_tab about store_sales.ss_net_paid - all                                5435.06            3106.79
statistics_tab about store_sales.ss_net_paid_inc_tax - all                        5616.72            3642.88
statistics_tab about store_sales.ss_net_profit - all                              7491.44            5555.77
statistics_tab about time_dim.t_time_sk - all                                       43.64               6.84
statistics_tab about time_dim.t_time_id - all                                      164.52              21.03
statistics_tab about time_dim.t_time - all                                          20.94               5.97
statistics_tab about time_dim.t_hour - all                                          47.93               5.81
statistics_tab about time_dim.t_minute - all                                       168.15               6.61
statistics_tab about time_dim.t_second - all                                        38.26               6.03
statistics_tab about time_dim.t_am_pm - all                                         36.33               5.94
statistics_tab about time_dim.t_shift - all                                         52.37               6.49
statistics_tab about time_dim.t_sub_shift - all                                     74.60               5.86
statistics_tab about time_dim.t_meal_time - all                                     51.54               6.56
statistics_tab about warehouse.w_warehouse_sk - all                                 25.02               3.22
statistics_tab about warehouse.w_warehouse_id - all                                 97.41               4.90
statistics_tab about warehouse.w_warehouse_name - all                               41.67               4.72
statistics_tab about warehouse.w_warehouse_sq_ft - all                              27.86               3.59
statistics_tab about warehouse.w_street_number - all                                50.74               4.72
statistics_tab about warehouse.w_street_name - all                                 110.31               4.57
statistics_tab about warehouse.w_street_type - all                                  66.25               4.77
statistics_tab about warehouse.w_suite_number - all                                115.85               4.65
statistics_tab about warehouse.w_city - all                                         38.88               4.50
statistics_tab about warehouse.w_county - all                                       54.55               4.40
statistics_tab about warehouse.w_state - all                                        38.48               4.41
statistics_tab about warehouse.w_zip - all                                          55.41               4.24
statistics_tab about warehouse.w_country - all                                      38.01               5.59
statistics_tab about warehouse.w_gmt_offset - all                                  231.57               3.75
statistics_tab about web_page.wp_web_page_sk - all                                  25.45               3.37
statistics_tab about web_page.wp_web_page_id - all                                  71.44               4.80
statistics_tab about web_page.wp_rec_start_date - all                               22.24               4.99
statistics_tab about web_page.wp_rec_end_date - all                                  7.24               4.53
statistics_tab about web_page.wp_creation_date_sk - all                             20.53               2.69
statistics_tab about web_page.wp_access_date_sk - all                               27.36               2.85
statistics_tab about web_page.wp_autogen_flag - all                                 97.38               5.49
statistics_tab about web_page.wp_customer_sk - all                                  14.48               3.36
statistics_tab about web_page.wp_url - all                                          36.22               4.57
statistics_tab about web_page.wp_type - all                                         42.30               4.84
statistics_tab about web_page.wp_char_count - all                                   41.38               3.61
statistics_tab about web_page.wp_link_count - all                                    5.37               3.32
statistics_tab about web_page.wp_image_count - all                                  33.57               3.85
statistics_tab about web_page.wp_max_ad_count - all                                 17.95               3.46
statistics_tab about web_returns.wr_returned_date_sk - all                          99.92              36.84
statistics_tab about web_returns.wr_returned_time_sk - all                         189.51              43.76
statistics_tab about web_returns.wr_item_sk - all                                  126.91              64.33
statistics_tab about web_returns.wr_refunded_customer_sk - all                     136.26              58.18
statistics_tab about web_returns.wr_refunded_cdemo_sk - all                        155.84              97.83
statistics_tab about web_returns.wr_refunded_hdemo_sk - all                        149.35              34.41
statistics_tab about web_returns.wr_refunded_addr_sk - all                         127.02              53.56
statistics_tab about web_returns.wr_returning_customer_sk - all                    138.48              58.66
statistics_tab about web_returns.wr_returning_cdemo_sk - all                       177.23              83.55
statistics_tab about web_returns.wr_returning_hdemo_sk - all                        93.71              33.69
statistics_tab about web_returns.wr_returning_addr_sk - all                        173.55              54.42
statistics_tab about web_returns.wr_web_page_sk - all                              130.20              29.49
statistics_tab about web_returns.wr_reason_sk - all                                166.83              34.74
statistics_tab about web_returns.wr_order_number - all                              91.27              32.02
statistics_tab about web_returns.wr_return_quantity - all                           71.77              32.01
statistics_tab about web_returns.wr_return_amt - all                               118.73              68.21
statistics_tab about web_returns.wr_return_tax - all                               105.33              38.68
statistics_tab about web_returns.wr_return_amt_inc_tax - all                       115.60              59.86
statistics_tab about web_returns.wr_fee - all                                      149.37              35.84
statistics_tab about web_returns.wr_return_ship_cost - all                         329.61              46.87
statistics_tab about web_returns.wr_refunded_cash - all                            232.70              48.08
statistics_tab about web_returns.wr_reversed_charge - all                          120.31              48.02
statistics_tab about web_returns.wr_account_credit - all                            97.77              43.32
statistics_tab about web_returns.wr_net_loss - all                                  89.44              54.33
statistics_tab about web_sales.ws_sold_date_sk - all                              1001.37             298.83
statistics_tab about web_sales.ws_sold_time_sk - all                               726.74             353.40
statistics_tab about web_sales.ws_ship_date_sk - all                              1017.33             295.65
statistics_tab about web_sales.ws_item_sk - all                                    779.32             351.41
statistics_tab about web_sales.ws_bill_customer_sk - all                           803.89             371.85
statistics_tab about web_sales.ws_bill_cdemo_sk - all                             1116.73             404.51
statistics_tab about web_sales.ws_bill_hdemo_sk - all                              670.22             286.75
statistics_tab about web_sales.ws_bill_addr_sk - all                              1257.05             378.09
statistics_tab about web_sales.ws_ship_customer_sk - all                           995.86             370.55
statistics_tab about web_sales.ws_ship_cdemo_sk - all                              992.36             354.94
statistics_tab about web_sales.ws_ship_hdemo_sk - all                              929.24             275.56
statistics_tab about web_sales.ws_ship_addr_sk - all                              1124.67             375.10
statistics_tab about web_sales.ws_web_page_sk - all                               1130.42             304.53
statistics_tab about web_sales.ws_web_site_sk - all                                844.84             315.87
statistics_tab about web_sales.ws_ship_mode_sk - all                               986.76             266.43
statistics_tab about web_sales.ws_warehouse_sk - all                               875.03             318.06
statistics_tab about web_sales.ws_promo_sk - all                                   696.20             293.21
statistics_tab about web_sales.ws_order_number - all                               849.97             266.64
statistics_tab about web_sales.ws_quantity - all                                   674.28             304.47
statistics_tab about web_sales.ws_wholesale_cost - all                             858.94             309.14
statistics_tab about web_sales.ws_list_price - all                                 804.16             334.18
statistics_tab about web_sales.ws_sales_price - all                                876.06             349.08
statistics_tab about web_sales.ws_ext_discount_amt - all                          1530.84             835.69
statistics_tab about web_sales.ws_ext_sales_price - all                           1667.39             785.00
statistics_tab about web_sales.ws_ext_wholesale_cost - all                        1286.63             739.82
statistics_tab about web_sales.ws_ext_list_price - all                            1618.70            1252.48
statistics_tab about web_sales.ws_ext_tax - all                                    807.52             398.71
statistics_tab about web_sales.ws_coupon_amt - all                                 845.90             452.73
statistics_tab about web_sales.ws_ext_ship_cost - all                             1422.11             629.83
statistics_tab about web_sales.ws_net_paid - all                                  1277.82             819.60
statistics_tab about web_sales.ws_net_paid_inc_tax - all                          1376.43             872.82
statistics_tab about web_sales.ws_net_paid_inc_ship - all                         1270.72             995.02
statistics_tab about web_sales.ws_net_paid_inc_ship_tax - all                     1459.21             945.69
statistics_tab about web_sales.ws_net_profit - all                                1676.48            1173.58
statistics_tab about web_site.web_site_sk - all                                     12.09               3.70
statistics_tab about web_site.web_site_id - all                                     88.01               5.33
statistics_tab about web_site.web_rec_start_date - all                              47.05               4.90
statistics_tab about web_site.web_rec_end_date - all                                20.72               4.81
statistics_tab about web_site.web_name - all                                        62.16               4.98
statistics_tab about web_site.web_open_date_sk - all                                27.00               3.29
statistics_tab about web_site.web_close_date_sk - all                               33.25               4.47
statistics_tab about web_site.web_class - all                                       47.17               5.88
statistics_tab about web_site.web_manager - all                                     32.39               5.86
statistics_tab about web_site.web_mkt_id - all                                      13.01               3.23
statistics_tab about web_site.web_mkt_class - all                                   32.04               5.40
statistics_tab about web_site.web_mkt_desc - all                                    97.94              10.76
statistics_tab about web_site.web_market_manager - all                              21.04               5.90
statistics_tab about web_site.web_company_id - all                                  88.38               3.24
statistics_tab about web_site.web_company_name - all                                80.27               5.28
statistics_tab about web_site.web_street_number - all                               60.58               4.96
statistics_tab about web_site.web_street_name - all                                 53.42               5.12
statistics_tab about web_site.web_street_type - all                                113.08               5.16
statistics_tab about web_site.web_suite_number - all                                56.28               4.89
statistics_tab about web_site.web_city - all                                        48.24               5.44
statistics_tab about web_site.web_county - all                                      60.63               5.38
statistics_tab about web_site.web_state - all                                      468.43               5.18
statistics_tab about web_site.web_zip - all                                         53.20               5.29
statistics_tab about web_site.web_country - all                                    124.32               6.18
statistics_tab about web_site.web_gmt_offset - all                                  22.55               3.43
statistics_tab about web_site.web_tax_percentage - all                              11.82               3.34

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          339.0         9.0      695.0    1051.0
MonetDB-BHT-8-2-1           1.0          339.0         9.0      695.0    1051.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.15
MonetDB-BHT-8-2-1           0.03

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1          236821.96
MonetDB-BHT-8-2-1         1177926.60

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MonetDB-BHT-8-1 10 1              1                343      1  10         45026.24
MonetDB-BHT-8-2 10 1              2                176      1  10         87750.00

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      397.09     1.41          2.11                12.28
MonetDB-BHT-8-2      332.08     3.02          9.16                14.51

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       24.49     0.02          0.25                 0.26
MonetDB-BHT-8-2       24.49     0.07          0.50                 0.54

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



## Fractional Scaling Factor

TPC-DS supports scaling factors that are fractional.
Example: SF=0.1

```bash
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 0.1 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 5Gi -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_fractional.log &
```

results in

doc_tpcds_testcase_fractional.log
```markdown
## Show Summary
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
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_monetdb_1.log &
```


### Status Database and Benchmark

You can watch the status of experiments via `bexperiments status`.

In the following example output we see all components of bexhoma are up and running.
The cluster stores a MonetDB database corresponding to TPC-DS of SF=100.
The disk is of storageClass shared and of size 1000Gi and 156G of that space is used.
It took about 4000s to build this database.
Currently no DBMS is running.

```bash
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
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 12332s 
    Code: 1748361591
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 7200.
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
    disk:300889676
    datadisk:315690
    volume_size:1000G
    volume_used:309G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748361591

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                2637.88
TPC-DS Q2               16764.28
TPC-DS Q3                1918.33
TPC-DS Q4              165305.06
TPC-DS Q5               23933.02
TPC-DS Q6               11482.90
TPC-DS Q7                2830.86
TPC-DS Q8                5504.10
TPC-DS Q9                5874.06
TPC-DS Q10               2100.43
TPC-DS Q11              82490.57
TPC-DS Q12                719.09
TPC-DS Q13               2874.62
TPC-DS Q14a+b          274520.90
TPC-DS Q15               1200.84
TPC-DS Q16               1769.05
TPC-DS Q17              38280.43
TPC-DS Q18               8892.97
TPC-DS Q19               2175.67
TPC-DS Q20               1207.08
TPC-DS Q21               2371.85
TPC-DS Q22              64545.85
TPC-DS Q23a+b         1420883.33
TPC-DS Q24a+b         1090365.04
TPC-DS Q25             144393.47
TPC-DS Q26               4972.95
TPC-DS Q27              41497.92
TPC-DS Q28               4921.31
TPC-DS Q29              16622.60
TPC-DS Q30               4905.84
TPC-DS Q31              30967.47
TPC-DS Q32               1767.50
TPC-DS Q33              13230.04
TPC-DS Q34               4432.81
TPC-DS Q35              23996.74
TPC-DS Q36              17233.46
TPC-DS Q37              38518.46
TPC-DS Q38              64598.41
TPC-DS Q39a+b           82144.36
TPC-DS Q40              19052.14
TPC-DS Q41                674.80
TPC-DS Q42               1984.63
TPC-DS Q43               1403.81
TPC-DS Q44                132.62
TPC-DS Q45               1569.16
TPC-DS Q46               3184.14
TPC-DS Q47               7547.96
TPC-DS Q48               3235.58
TPC-DS Q49              46504.22
TPC-DS Q50               3513.86
TPC-DS Q51              48649.29
TPC-DS Q52               2109.35
TPC-DS Q53               1787.58
TPC-DS Q54               4786.27
TPC-DS Q55                210.19
TPC-DS Q56               2722.33
TPC-DS Q57               1938.84
TPC-DS Q58              12032.30
TPC-DS Q59              13143.44
TPC-DS Q60               3724.71
TPC-DS Q61                182.96
TPC-DS Q62               3202.51
TPC-DS Q63               1751.03
TPC-DS Q64              76310.83
TPC-DS Q65              26397.61
TPC-DS Q66              12444.26
TPC-DS Q67             105200.44
TPC-DS Q68               2544.14
TPC-DS Q69               4422.59
TPC-DS Q70               5459.43
TPC-DS Q71               3842.16
TPC-DS Q72              19984.29
TPC-DS Q73               2089.12
TPC-DS Q74              24865.37
TPC-DS Q75             127216.13
TPC-DS Q76              82956.82
TPC-DS Q77              34580.05
TPC-DS Q78             198436.54
TPC-DS Q79               4928.64
TPC-DS Q80             144077.02
TPC-DS Q81               2910.95
TPC-DS Q82              25892.81
TPC-DS Q83               3508.32
TPC-DS Q84                599.91
TPC-DS Q85               1600.58
TPC-DS Q86               3346.72
TPC-DS Q87              65159.52
TPC-DS Q88               6268.49
TPC-DS Q89               3189.81
TPC-DS Q90               1192.39
TPC-DS Q91               1262.45
TPC-DS Q92               1160.22
TPC-DS Q93              24331.82
TPC-DS Q94               3965.59
TPC-DS Q95              17793.74
TPC-DS Q96               1693.31
TPC-DS Q97              42108.78
TPC-DS Q98               2518.05
TPC-DS Q99               3900.43

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0         1782.0        12.0     5226.0    7028.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           8.09

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           45069.94

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MonetDB-BHT-8-1 100 1              1               5042      1  100          7068.62

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    23227.41    16.19        118.33               299.77

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     2401.94     1.19         46.84                95.91

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    41174.98     44.4         441.7               486.48

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       47.96     0.18          0.35                 0.36

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
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_monetdb_2.log &
```

### Evaluate Results

doc_tpcds_monetdb_2.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 20864s 
    Code: 1748374315
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 7200.
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
    disk:300889844
    datadisk:322157
    volume_size:1000G
    volume_used:315G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748374315
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:300890260
    datadisk:317050
    volume_size:1000G
    volume_used:316G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748374315
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:300890492
    datadisk:317050
    volume_size:1000G
    volume_used:310G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748374315
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:300890920
    datadisk:317050
    volume_size:1000G
    volume_used:316G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748374315

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q39a+b                 True                False                 True                 True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q1                 10904.81              1352.03              9901.93              1348.35
TPC-DS Q2                 51489.32             14557.18             46446.74             13278.68
TPC-DS Q3                120653.04              6777.71            114318.50              7929.78
TPC-DS Q4                311777.32            167573.60            306934.30            161539.60
TPC-DS Q5                225504.20             24223.44            232864.89             25229.96
TPC-DS Q6                 10889.72              8368.32             13320.43              8260.00
TPC-DS Q7                115641.50              2029.28            114523.74              1964.57
TPC-DS Q8                 35707.40              3827.72             37130.19              3723.03
TPC-DS Q9                 24372.10              3906.10             20527.53              5348.19
TPC-DS Q10               374243.44              2838.67            371704.39              2228.05
TPC-DS Q11                93190.84             78779.70             82520.08             74712.26
TPC-DS Q12                 1705.40               695.00              1773.42               662.24
TPC-DS Q13                 2561.94              2743.26              2713.58              3170.96
TPC-DS Q14a+b            359374.60            308801.62            319509.01            311527.06
TPC-DS Q15                 1873.77              1718.39              1638.29              1676.62
TPC-DS Q16                25209.54              1279.67             23601.25              1324.00
TPC-DS Q17                45375.49             36448.08             43223.89             33698.96
TPC-DS Q18                25321.64              8928.83             26768.06              8223.27
TPC-DS Q19                 2375.33              2313.53              2716.17              2605.62
TPC-DS Q20                 1286.75               729.90              1207.05               744.14
TPC-DS Q21               101462.80              2161.39            101032.31              2218.40
TPC-DS Q22               108842.70             67772.51            101136.33             65702.80
TPC-DS Q23a+b           2091759.26           2022871.68           2315934.41           1909392.23
TPC-DS Q24a+b            306361.68            398768.27            261103.37            262275.87
TPC-DS Q25                26568.13             20393.10             20786.73             12043.68
TPC-DS Q26                 1560.41              1383.51              1796.41              1237.06
TPC-DS Q27                13793.56             13035.05             14251.62             13603.37
TPC-DS Q28                 4343.33              3234.34              5333.42              5362.64
TPC-DS Q29                15774.73             16851.59             13889.33             13087.10
TPC-DS Q30                  958.14              1181.86               907.45               362.97
TPC-DS Q31                25284.10             36529.71             24821.07             19929.00
TPC-DS Q32                  813.29               860.83               814.24               814.61
TPC-DS Q33                 1768.43              1783.52              2469.47              1518.13
TPC-DS Q34                 3507.67              1618.43              2603.10              1363.38
TPC-DS Q35                 9201.65              9645.38              8044.87              8883.01
TPC-DS Q36                11029.02             11051.45             11332.44             12576.23
TPC-DS Q37                21802.03              3422.73             24983.11              4071.75
TPC-DS Q38                31111.62             30073.89             30151.31             30279.28
TPC-DS Q39a+b             77397.97             76773.33             77824.80             71404.67
TPC-DS Q40                 4136.33              4478.14              3634.45              3294.53
TPC-DS Q41                   20.13                39.53                41.69                33.92
TPC-DS Q42                 1999.16              1989.36              2238.03              2201.05
TPC-DS Q43                 1394.18              1370.88              1339.87              1330.72
TPC-DS Q44                  125.90                71.59               117.12                69.17
TPC-DS Q45                  654.97               642.61               771.86               733.16
TPC-DS Q46                 2839.05              2751.05              3079.43              2612.81
TPC-DS Q47                 7520.64              7302.91              7255.58              6387.04
TPC-DS Q48                 1638.89             21557.14              1447.42             10663.95
TPC-DS Q49                31126.79             10747.06             30730.99              9581.53
TPC-DS Q50                 3379.85              2793.56              3686.27              2039.17
TPC-DS Q51                47360.46             48835.04             45475.11             47215.94
TPC-DS Q52                 1988.19              2003.49              2246.14              2214.85
TPC-DS Q53                 1713.94              1693.28              1760.14              1747.88
TPC-DS Q54                  428.14              2832.40               444.04             11366.42
TPC-DS Q55                  161.26               157.76               158.74               156.02
TPC-DS Q56                 1769.63              1652.07              2002.50              1716.37
TPC-DS Q57                 1815.17              2898.21              1614.87              1346.02
TPC-DS Q58                 5420.43              5247.72              5048.72              5701.47
TPC-DS Q59                13996.60             12810.58             11845.29             11496.10
TPC-DS Q60                 2235.12              3034.58              1754.40              1231.60
TPC-DS Q61                 1695.06              2116.67              1909.84              1709.60
TPC-DS Q62                 2741.80              4040.34              2676.77              1447.72
TPC-DS Q63                 2319.98              2201.95              1594.96              1493.53
TPC-DS Q64                43543.28             29724.27             38257.13             25264.07
TPC-DS Q65                23533.95             26963.64             22266.78             21110.60
TPC-DS Q66                 9113.54              4512.01              8639.02              4279.82
TPC-DS Q67               110468.74            106361.54            102108.11            102762.08
TPC-DS Q68                 2281.20              2334.19              2750.34              2756.76
TPC-DS Q69                 3392.75              3477.12              3343.56              5048.33
TPC-DS Q70                 4828.28              4656.49              4985.86              3946.66
TPC-DS Q71                 1717.05              2323.08              1476.57              1573.63
TPC-DS Q72                15425.84              8440.21             14190.01             10957.44
TPC-DS Q73                 1994.49              1133.51              2258.62              2239.25
TPC-DS Q74                25175.00             24230.50             24659.84             23145.59
TPC-DS Q75               109733.72            129790.39            114130.04            116399.20
TPC-DS Q76                66961.70            110892.62             68739.89             13516.90
TPC-DS Q77                 9478.52             13589.86              9044.33              6182.89
TPC-DS Q78               176578.51            176591.73            160347.11            174063.35
TPC-DS Q79                 7333.02             15247.42              6771.19              9364.31
TPC-DS Q80               112814.47            108045.40             95400.05            104351.20
TPC-DS Q81                 2391.58              2028.63              2028.15              2595.69
TPC-DS Q82                15446.04             21499.45             23742.17             17634.71
TPC-DS Q83                 1944.60               522.80              1958.27               329.47
TPC-DS Q84                  712.75               224.24               465.95               152.64
TPC-DS Q85                 1637.07              1467.32              1667.91               741.50
TPC-DS Q86                 3207.51              3226.77              3081.94              3095.99
TPC-DS Q87                43042.21             40343.56             41008.98             40362.45
TPC-DS Q88                 5804.04             20951.42              5937.42             18973.08
TPC-DS Q89                 2805.83              3533.73              3223.14              3920.89
TPC-DS Q90                  540.35              2677.86               679.32               453.96
TPC-DS Q91                  794.40               274.70               893.82               138.28
TPC-DS Q92                  560.85               582.67               572.07               611.29
TPC-DS Q93                22710.15             22534.21             18529.48             17593.24
TPC-DS Q94                 4060.43              3612.02              3599.67              1805.88
TPC-DS Q95                17132.26             17532.72             16924.43             17340.93
TPC-DS Q96                 1815.50              1737.36              1914.22              1918.25
TPC-DS Q97                46241.42             45808.23             47074.06             47514.31
TPC-DS Q98                 2508.92              2472.47              2597.59              2699.35
TPC-DS Q99                 2781.97              2775.45              2867.33              1999.41

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0         1782.0        12.0     5226.0    7028.0
MonetDB-BHT-8-1-2-1           1.0         1782.0        12.0     5226.0    7028.0
MonetDB-BHT-8-2-1-1           1.0         1782.0        12.0     5226.0    7028.0
MonetDB-BHT-8-2-2-1           1.0         1782.0        12.0     5226.0    7028.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           8.26
MonetDB-BHT-8-1-2-1           5.99
MonetDB-BHT-8-2-1-1           8.17
MonetDB-BHT-8-2-2-1           5.20

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           44447.76
MonetDB-BHT-8-1-2-1           61041.84
MonetDB-BHT-8-2-1-1           44872.33
MonetDB-BHT-8-2-2-1           70523.98

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count   SF  Throughput@Size
DBMS              SF  num_experiment num_client                                       
MonetDB-BHT-8-1-1 100 1              1               5786      1  100          6159.70
MonetDB-BHT-8-1-2 100 1              2               4544      1  100          7843.31
MonetDB-BHT-8-2-1 100 2              1               5834      1  100          6109.02
MonetDB-BHT-8-2-2 100 2              2               4082      1  100          8731.01

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1    29618.87    24.02        287.72               352.21
MonetDB-BHT-8-1-2    28483.56    30.07        374.37               414.51
MonetDB-BHT-8-2-1    58470.69    32.85        317.91               382.31
MonetDB-BHT-8-2-2    31838.36    58.96        377.89               411.75

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       49.92     0.03          0.36                 0.38
MonetDB-BHT-8-1-2       49.92     0.11          0.60                 0.64
MonetDB-BHT-8-2-1       47.25     0.18          0.61                 0.65
MonetDB-BHT-8-2-2       48.66     0.27          0.61                 0.65

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST failed: SQL warnings (result mismatch)
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
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_monetdb_3.log &
```

### Evaluate Results

doc_tpcds_monetdb_3.log
```markdown
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

