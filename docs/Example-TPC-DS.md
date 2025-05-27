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
    Duration: 1162s 
    Code: 1748292351
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:310180844
    datadisk:165
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748292351
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:309033592
    datadisk:5600
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748292351
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:312649668
    datadisk:8290
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748292351
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:312635112
    datadisk:5805
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748292351

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
TPC-DS Q26                 False               True             False                  True
TPC-DS Q27                 False               True             False                  True
TPC-DS Q28                 False               True             False                  True
TPC-DS Q29                 False               True             False                  True
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
TPC-DS Q45                 False               True             False                  True
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
TPC-DS Q86                 False               True             False                  True
TPC-DS Q87                 False               True             False                  True
TPC-DS Q88                 False               True             False                 False
TPC-DS Q89                 False               True             False                 False
TPC-DS Q90                 False               True             False                 False
TPC-DS Q91                 False               True             False                 False
TPC-DS Q92                 False               True             False                 False
TPC-DS Q93                 False               True             False                 False
TPC-DS Q94                 False               True             False                 False
TPC-DS Q95                 False               True             False                 False
TPC-DS Q96                 False               True             False                 False
TPC-DS Q97                 False               True             False                 False
TPC-DS Q98                 False               True             False                 False
TPC-DS Q99                 False               True             False                 False

### Latency of Timer Execution [ms]
DBMS           MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q1                  18.90              41.01             78.23                320.85
TPC-DS Q2                   2.57             152.04              7.11                864.82
TPC-DS Q3                   1.01              22.22              3.19                499.23
TPC-DS Q4                   6.97            1198.62             23.02              15674.01
TPC-DS Q5                   2.33             254.59             12.39               1438.48
TPC-DS Q6                   1.16              86.78              2.93             219192.79
TPC-DS Q7                   0.92              59.19              2.93               1098.18
TPC-DS Q8                   2.14              42.42              4.95                150.14
TPC-DS Q9                   1.40              67.89              4.31               6408.73
TPC-DS Q10                  1.79             156.10              5.83               3022.64
TPC-DS Q11                  2.84             636.91             10.54              12083.55
TPC-DS Q12                  0.93             159.28             20.56                203.98
TPC-DS Q13                  1.29             100.93              4.18               1870.03
TPC-DS Q14a+b               8.15            2461.57             22.99               7781.78
TPC-DS Q15                  0.88              22.79              2.43                340.26
TPC-DS Q16                  1.19              43.56              3.08                719.30
TPC-DS Q17                  1.39             118.14              3.24               1033.52
TPC-DS Q18                  1.34             146.76              3.29               1225.23
TPC-DS Q19                  0.86             274.72              3.12                497.45
TPC-DS Q20                  0.95              35.80              3.13                300.16
TPC-DS Q21                  1.34             270.34              3.72                680.43
TPC-DS Q22                  0.90            1025.02              2.13               9864.75
TPC-DS Q23a+b               4.57            2631.44             12.46              10806.92
TPC-DS Q24a+b               3.03             223.28              8.64               1270.01
TPC-DS Q25                  1.24             104.69              2.87               1030.71
TPC-DS Q26                  0.93              24.36              2.29                714.30
TPC-DS Q27                  1.03             152.91              2.37                138.77
TPC-DS Q28                  2.82              62.46              3.96               4707.54
TPC-DS Q29                  1.70             101.30              2.93               1077.52
TPC-DS Q30                  1.70              66.53              3.38              28719.48
TPC-DS Q31                  2.21             144.30              5.81               6224.65
TPC-DS Q32                  1.38              23.84              1.66                232.04
TPC-DS Q33                  2.23              23.46              4.24               1203.66
TPC-DS Q34                  1.50              32.61              1.95                 58.57
TPC-DS Q35                  1.57              89.19              2.97               3374.74
TPC-DS Q36                  1.18             131.97              2.45               2119.36
TPC-DS Q37                  1.08             128.21              2.05                817.08
TPC-DS Q38                  1.09             198.48              2.58               3316.18
TPC-DS Q39a+b               3.11            1033.30              8.57               7454.21
TPC-DS Q40                  1.09              75.71              2.74                353.86
TPC-DS Q41                  1.11              13.80              2.60               3958.61
TPC-DS Q42                  0.80              19.90              2.19                265.33
TPC-DS Q43                  0.97              43.24              2.48                 59.16
TPC-DS Q44                  1.36              30.61              3.21                  2.68
TPC-DS Q45                  1.10              25.76              2.79                226.67
TPC-DS Q46                  1.06              49.17              3.13                 54.49
TPC-DS Q47                  2.36             259.73              6.56               4658.73
TPC-DS Q48                  0.99              99.52              3.02               1877.16
TPC-DS Q49                  2.02             117.67              5.48               2165.68
TPC-DS Q50                  1.03              91.64              2.80                727.11
TPC-DS Q51                  1.33             591.30              4.19               2953.97
TPC-DS Q52                  0.74              22.71              2.37                266.66
TPC-DS Q53                  0.93              27.63              2.43                339.52
TPC-DS Q54                  1.42              24.59              3.82                205.42
TPC-DS Q55                  0.76              16.50              1.95                267.58
TPC-DS Q56                  1.68              28.20              4.84                928.07
TPC-DS Q57                  1.93             102.75              5.03               2192.78
TPC-DS Q58                  1.73              58.71              8.54               1308.44
TPC-DS Q59                  1.61             116.82              4.60               1266.15
TPC-DS Q60                  1.77              24.95              4.53               1223.55
TPC-DS Q61                  1.38              32.64              2.59               3285.94
TPC-DS Q62                  1.13              26.71              3.20                295.93
TPC-DS Q63                  1.15              25.90              2.41                319.27
TPC-DS Q64                  4.03             383.41              7.02               2279.52
TPC-DS Q65                  1.20              94.91              2.27               1599.88
TPC-DS Q66                  2.53              97.65              5.63                608.27
TPC-DS Q67                  0.98             677.28              2.32               7045.12
TPC-DS Q68                  1.12              41.46              2.31                 56.81
TPC-DS Q69                  1.25              47.95              2.42                718.78
TPC-DS Q70                  1.24              70.52              2.36               1267.81
TPC-DS Q71                  1.09              32.83              2.47                924.69
TPC-DS Q72                  1.98             161.60              2.64               2999.07
TPC-DS Q73                  1.16              25.42              2.78                 58.31
TPC-DS Q74                  2.20             179.86              4.74               3745.40
TPC-DS Q75                  2.90             626.61              5.33               2497.34
TPC-DS Q76                  1.54              74.11              2.86                677.82
TPC-DS Q77                  2.68              54.07              5.95               5272.74
TPC-DS Q78                  1.99             777.68              4.22               4550.08
TPC-DS Q79                  1.39              43.04              2.80                457.35
TPC-DS Q80                  2.05             415.30              4.20               1485.00
TPC-DS Q81                  1.28              31.02              2.76             125082.90
TPC-DS Q82                  0.74             149.92              1.92                877.78
TPC-DS Q83                  1.46              16.55              3.12                301.16
TPC-DS Q84                  0.86              36.86              1.83                263.31
TPC-DS Q85                  1.27              35.06              2.56                909.04
TPC-DS Q86                  0.96              26.87              1.90                483.50
TPC-DS Q87                  1.10             248.62              2.24               3295.03
TPC-DS Q88                  2.73              89.58              7.45               6791.86
TPC-DS Q89                  1.15              35.32              3.16                316.26
TPC-DS Q90                  1.04              16.41              2.11               2135.82
TPC-DS Q91                  1.04              25.23              2.33                437.99
TPC-DS Q92                  0.91              12.99              2.41                206.34
TPC-DS Q93                  0.84              91.26              2.72                370.10
TPC-DS Q94                  0.95              16.52              2.20                467.56
TPC-DS Q95                  1.14             145.25              2.81               9692.89
TPC-DS Q96                  0.63              14.02              1.71                275.54
TPC-DS Q97                  1.09             232.02              2.93               1040.37
TPC-DS Q98                  0.86              40.01              2.03                506.25
TPC-DS Q99                  0.90              55.84              2.62                416.13

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1              1.0            3.0         4.0      169.0     188.0
MonetDB-BHT-8-1-1              1.0          108.0         9.0       98.0     225.0
MySQL-BHT-64-1-1               1.0           11.0         8.0      127.0     156.0
PostgreSQL-BHT-8-1-1           1.0          153.0         1.0      138.0     303.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              0.00
MonetDB-BHT-8-1-1              0.09
MySQL-BHT-64-1-1               0.00
PostgreSQL-BHT-8-1-1           1.06

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1            2484156.22
MonetDB-BHT-8-1-1              44504.06
MySQL-BHT-64-1-1              991792.76
PostgreSQL-BHT-8-1-1            3436.83

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
Traceback (most recent call last):
  File "/home/perdelt/repositories/Benchmark-Experiment-Host-Manager/tpcds.py", line 353, in <module>
    experiment.show_summary()
  File "/home/perdelt/repositories/Benchmark-Experiment-Host-Manager/bexhoma/experiments.py", line 1847, in show_summary
    df_time['benchmark_end'] = eva['times']['total'][c['name']]['time_end']
                               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
KeyError: 'time_end'
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
```bash
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 817s 
    Code: 1748293672
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
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
    disk:311417752
    datadisk:12891
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748293672

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                  73.19
TPC-DS Q2                 559.30
TPC-DS Q3                  43.08
TPC-DS Q4                3892.92
TPC-DS Q5                 635.07
TPC-DS Q6                 163.41
TPC-DS Q7                  91.91
TPC-DS Q8                 106.77
TPC-DS Q9                 136.61
TPC-DS Q10                133.09
TPC-DS Q11               1960.68
TPC-DS Q12                 39.70
TPC-DS Q13                175.00
TPC-DS Q14a+b            6554.92
TPC-DS Q15                 51.57
TPC-DS Q16                273.42
TPC-DS Q17                407.71
TPC-DS Q18                253.09
TPC-DS Q19                 88.69
TPC-DS Q20                 54.95
TPC-DS Q21                103.08
TPC-DS Q22               2846.45
TPC-DS Q23a+b            6554.82
TPC-DS Q24a+b             905.17
TPC-DS Q25                375.80
TPC-DS Q26                 68.36
TPC-DS Q27                335.96
TPC-DS Q28                175.81
TPC-DS Q29                384.49
TPC-DS Q30                 35.26
TPC-DS Q31                512.82
TPC-DS Q32                 38.41
TPC-DS Q33                 54.45
TPC-DS Q34                 50.51
TPC-DS Q35                227.54
TPC-DS Q36                253.98
TPC-DS Q37                232.11
TPC-DS Q38                679.68
TPC-DS Q39a+b            3030.21
TPC-DS Q40                222.91
TPC-DS Q41                  9.88
TPC-DS Q42                 49.14
TPC-DS Q43                 94.40
TPC-DS Q44                 84.20
TPC-DS Q45                 49.62
TPC-DS Q46                 89.24
TPC-DS Q47                622.86
TPC-DS Q48                146.49
TPC-DS Q49                243.69
TPC-DS Q50                242.27
TPC-DS Q51               1907.59
TPC-DS Q52                 37.75
TPC-DS Q53                 51.30
TPC-DS Q54                 56.13
TPC-DS Q55                 31.13
TPC-DS Q56                 56.85
TPC-DS Q57                154.40
TPC-DS Q58                134.11
TPC-DS Q59                316.89
TPC-DS Q60                 55.01
TPC-DS Q61                 80.64
TPC-DS Q62                 49.53
TPC-DS Q63                 55.80
TPC-DS Q64               1125.45
TPC-DS Q65                387.26
TPC-DS Q66                277.43
TPC-DS Q67               2203.88
TPC-DS Q68                 86.68
TPC-DS Q69                 44.35
TPC-DS Q70                169.20
TPC-DS Q71                 63.76
TPC-DS Q72                264.27
TPC-DS Q73                 50.11
TPC-DS Q74               1842.58
TPC-DS Q75               2296.02
TPC-DS Q76                 69.41
TPC-DS Q77                173.46
TPC-DS Q78               3356.02
TPC-DS Q79                 80.69
TPC-DS Q80               2299.65
TPC-DS Q81                 53.50
TPC-DS Q82                359.57
TPC-DS Q83                 27.90
TPC-DS Q84                 20.76
TPC-DS Q85                 72.20
TPC-DS Q86                 70.27
TPC-DS Q87                799.99
TPC-DS Q88                201.89
TPC-DS Q89                 73.63
TPC-DS Q90                 24.84
TPC-DS Q91                 25.40
TPC-DS Q92                 25.75
TPC-DS Q93                348.22
TPC-DS Q94                 60.50
TPC-DS Q95                212.18
TPC-DS Q96                 27.40
TPC-DS Q97                894.57
TPC-DS Q98                 87.66
TPC-DS Q99                 94.31

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          290.0         9.0      192.0     501.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.18

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           63139.23

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MonetDB-BHT-8-1 3  1              1                 76      1   3         14068.42

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      721.88     2.22          3.31                10.94

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       56.38     0.25          1.12                 2.28

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      216.13     4.55          7.26                16.63

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       20.22        0          0.26                 0.27

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
```bash
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 600s 
    Code: 1748294632
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.5.
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
    disk:303952520
    datadisk:5601
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748294632
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:304034260
    datadisk:5681
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748294632
MonetDB-BHT-8-2-2 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:304034260
    datadisk:5681
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748294632

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-2-2
TPC-DS Q39a+b              False               True               True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-2-2
TPC-DS Q1                  49.09              46.93              40.81
TPC-DS Q2                 167.78             187.02             170.66
TPC-DS Q3                  22.90              31.04              32.03
TPC-DS Q4                1199.91            1300.36            1248.91
TPC-DS Q5                 235.54             250.01             236.18
TPC-DS Q6                  70.27              61.24              64.11
TPC-DS Q7                  49.62              46.89              57.51
TPC-DS Q8                  40.54              43.81              40.19
TPC-DS Q9                  53.37              52.76              51.68
TPC-DS Q10                 39.72              46.99              52.26
TPC-DS Q11                584.45             561.83             590.17
TPC-DS Q12                 20.21              20.61              30.79
TPC-DS Q13                100.93             110.32              89.28
TPC-DS Q14a+b            2123.34            2263.32            2325.81
TPC-DS Q15                 21.67              22.17              28.77
TPC-DS Q16                 36.26              34.60              37.47
TPC-DS Q17                103.72             103.88             117.06
TPC-DS Q18                116.50              66.64              78.35
TPC-DS Q19                 43.46              37.22              35.95
TPC-DS Q20                 33.94              27.33              31.38
TPC-DS Q21                 69.44              67.30              61.91
TPC-DS Q22               1073.43            1024.23            1062.44
TPC-DS Q23a+b            2039.89            2158.43            2242.29
TPC-DS Q24a+b             186.98             186.46             179.71
TPC-DS Q25                136.09             111.94             114.00
TPC-DS Q26                 22.32              23.24              24.13
TPC-DS Q27                148.09             104.64             109.31
TPC-DS Q28                 70.81              74.43              77.77
TPC-DS Q29                 87.38              88.25              91.86
TPC-DS Q30                 22.51              23.22              23.02
TPC-DS Q31                170.70             145.37             154.42
TPC-DS Q32                 22.75              19.40              19.08
TPC-DS Q33                 31.04              22.30              23.06
TPC-DS Q34                 26.69              35.36              34.58
TPC-DS Q35                 97.84              72.64              93.62
TPC-DS Q36                 77.75              59.29              88.50
TPC-DS Q37                 81.08              63.37              48.45
TPC-DS Q38                213.03             197.22             185.03
TPC-DS Q39a+b            1053.98             961.82            1026.58
TPC-DS Q40                 74.87             100.37              98.94
TPC-DS Q41                 10.09              10.51               8.77
TPC-DS Q42                 20.46              24.44              19.81
TPC-DS Q43                 43.66              50.24              45.37
TPC-DS Q44                 85.02              75.08              79.00
TPC-DS Q45                 27.02              26.95              31.35
TPC-DS Q46                 40.66              47.89              43.06
TPC-DS Q47                258.90             275.40             256.80
TPC-DS Q48                107.37             109.21             105.95
TPC-DS Q49                108.05             107.45             103.73
TPC-DS Q50                102.72             110.67              92.19
TPC-DS Q51                618.44             615.81             597.22
TPC-DS Q52                 22.00              20.31              19.52
TPC-DS Q53                 26.99              25.48              26.39
TPC-DS Q54                 27.51              23.75              24.31
TPC-DS Q55                 17.07              16.57              18.35
TPC-DS Q56                 27.84              28.08              21.65
TPC-DS Q57                103.45              98.10              96.47
TPC-DS Q58                 61.88              46.42              46.29
TPC-DS Q59                116.23              99.29             111.47
TPC-DS Q60                 23.27              22.36              23.56
TPC-DS Q61                 35.38              32.36              32.04
TPC-DS Q62                 23.49              23.58              23.69
TPC-DS Q63                 26.06              27.27              25.21
TPC-DS Q64                390.02             270.22             241.70
TPC-DS Q65                 89.97              81.81              96.47
TPC-DS Q66                 92.58              98.38             101.99
TPC-DS Q67                632.48             670.40             650.69
TPC-DS Q68                 37.85              40.37              41.70
TPC-DS Q69                 23.34              24.64              22.66
TPC-DS Q70                 70.72              76.14              73.48
TPC-DS Q71                 30.92              31.44              30.45
TPC-DS Q72                155.87             154.72             149.37
TPC-DS Q73                 25.71              25.61              26.21
TPC-DS Q74                183.08             203.63             197.01
TPC-DS Q75                716.96             679.86             636.26
TPC-DS Q76                 36.77              35.00              46.35
TPC-DS Q77                 64.28              66.53              60.93
TPC-DS Q78                802.19             833.13             836.99
TPC-DS Q79                 53.63              46.41              46.43
TPC-DS Q80                477.96             451.68             443.75
TPC-DS Q81                 23.20              23.01              21.15
TPC-DS Q82                168.76              76.97              56.75
TPC-DS Q83                 15.07              13.83              13.00
TPC-DS Q84                 30.73              15.36              19.83
TPC-DS Q85                 37.39              36.15              34.15
TPC-DS Q86                 30.78              24.82              26.35
TPC-DS Q87                266.17             261.83             283.34
TPC-DS Q88                 88.01              93.54              92.72
TPC-DS Q89                 35.43              35.10              35.39
TPC-DS Q90                 16.83              29.27              12.79
TPC-DS Q91                 28.80              25.34              24.54
TPC-DS Q92                 14.95              13.93              13.04
TPC-DS Q93                 94.08              93.54             123.03
TPC-DS Q94                 18.44              17.88              16.63
TPC-DS Q95                133.13             151.89             130.49
TPC-DS Q96                 14.78              14.38              14.42
TPC-DS Q97                215.17             225.60             209.41
TPC-DS Q98                 39.51              40.97              41.85
TPC-DS Q99                 65.60              53.86              54.21

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          108.0         8.0       70.0     194.0
MonetDB-BHT-8-2-1           1.0          108.0         8.0       70.0     194.0
MonetDB-BHT-8-2-2           1.0          108.0         8.0       70.0     194.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.08
MonetDB-BHT-8-2-1           0.08
MonetDB-BHT-8-2-2           0.08

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           49186.37
MonetDB-BHT-8-2-1           51142.42
MonetDB-BHT-8-2-2           51319.60

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MonetDB-BHT-8-1 1  1              1                 32      1   1          11137.5
MonetDB-BHT-8-2 1  1              2                 36      2   1          19800.0

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
    Duration: 875s 
    Code: 1748295382
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.5.
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
    disk:298217920
    datadisk:5599
    volume_size:10G
    volume_used:5.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748295382
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:298217856
    datadisk:5680
    volume_size:10G
    volume_used:5.6G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748295382

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q39a+b                False                 True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q1                    39.70               789.01
TPC-DS Q2                   159.29               914.43
TPC-DS Q3                    32.44              1090.26
TPC-DS Q4                  1197.60              3732.65
TPC-DS Q5                   240.91              1540.81
TPC-DS Q6                    69.30               664.23
TPC-DS Q7                    58.22              1590.08
TPC-DS Q8                    90.32               568.77
TPC-DS Q9                    61.65               425.51
TPC-DS Q10                   52.17              7134.99
TPC-DS Q11                  543.38               607.54
TPC-DS Q12                   24.83               464.93
TPC-DS Q13                  101.86               279.29
TPC-DS Q14a+b              2724.12              2975.03
TPC-DS Q15                   28.05                25.28
TPC-DS Q16                   44.79              1086.10
TPC-DS Q17                  130.71               253.99
TPC-DS Q18                  435.29               798.57
TPC-DS Q19                   38.35               138.64
TPC-DS Q20                   28.77                32.17
TPC-DS Q21                  106.42              3716.57
TPC-DS Q22                 1062.25              1550.63
TPC-DS Q23a+b              2647.35              2692.20
TPC-DS Q24a+b               223.03               495.46
TPC-DS Q25                  108.86               105.08
TPC-DS Q26                   25.06                23.21
TPC-DS Q27                  148.14               106.31
TPC-DS Q28                   64.07                69.05
TPC-DS Q29                  114.73                96.24
TPC-DS Q30                   32.27               136.77
TPC-DS Q31                  160.69               136.95
TPC-DS Q32                   28.27                17.95
TPC-DS Q33                   23.61                77.31
TPC-DS Q34                   38.67               295.50
TPC-DS Q35                  100.90                94.75
TPC-DS Q36                  120.22                79.30
TPC-DS Q37                   74.52                54.27
TPC-DS Q38                  200.20               204.36
TPC-DS Q39a+b              1376.71              1552.82
TPC-DS Q40                   86.17                58.13
TPC-DS Q41                    9.77                 8.73
TPC-DS Q42                   19.75                18.39
TPC-DS Q43                   43.64                86.74
TPC-DS Q44                   32.07                90.07
TPC-DS Q45                   27.42                27.65
TPC-DS Q46                   39.25               471.09
TPC-DS Q47                  257.02               298.88
TPC-DS Q48                   98.91                92.61
TPC-DS Q49                  104.17               728.84
TPC-DS Q50                  102.33               565.56
TPC-DS Q51                  605.62               614.93
TPC-DS Q52                   25.34                22.41
TPC-DS Q53                   25.74                27.76
TPC-DS Q54                   36.22               639.48
TPC-DS Q55                   18.54                17.32
TPC-DS Q56                   32.02                68.08
TPC-DS Q57                   94.95               161.61
TPC-DS Q58                   50.20                57.22
TPC-DS Q59                   95.93               215.52
TPC-DS Q60                   32.01                24.57
TPC-DS Q61                   32.51               154.10
TPC-DS Q62                   32.55               124.73
TPC-DS Q63                   31.83                29.70
TPC-DS Q64                  403.09              1125.19
TPC-DS Q65                   92.21               156.12
TPC-DS Q66                  120.44               141.73
TPC-DS Q67                  701.99               681.73
TPC-DS Q68                   41.31                40.50
TPC-DS Q69                   26.86                24.35
TPC-DS Q70                   73.90               544.70
TPC-DS Q71                   30.80                33.84
TPC-DS Q72                  379.99               972.60
TPC-DS Q73                   29.26                26.25
TPC-DS Q74                  208.21               188.89
TPC-DS Q75                  931.26               740.54
TPC-DS Q76                   35.64               259.07
TPC-DS Q77                   75.95                63.31
TPC-DS Q78                  849.19               826.89
TPC-DS Q79                   53.79                52.92
TPC-DS Q80                  417.80               426.14
TPC-DS Q81                   28.78               220.16
TPC-DS Q82                  232.96               303.61
TPC-DS Q83                   62.66               108.60
TPC-DS Q84                   45.42               297.33
TPC-DS Q85                   44.75                70.29
TPC-DS Q86                   31.90                27.24
TPC-DS Q87                  265.49               278.05
TPC-DS Q88                  117.31               169.59
TPC-DS Q89                   40.84                38.85
TPC-DS Q90                   17.77                13.50
TPC-DS Q91                   29.70               233.45
TPC-DS Q92                   15.61                13.87
TPC-DS Q93                   96.33               100.55
TPC-DS Q94                   24.43                19.75
TPC-DS Q95                  149.71               155.45
TPC-DS Q96                   14.72                13.93
TPC-DS Q97                  226.66               241.90
TPC-DS Q98                   43.46                41.53
TPC-DS Q99                   63.01                65.35

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0          123.0        10.0       85.0     226.0
MonetDB-BHT-8-2-1-1           1.0          123.0        10.0       85.0     226.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.09
MonetDB-BHT-8-2-1-1           0.18

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           43874.30
MonetDB-BHT-8-2-1-1           21461.19

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                time [s]  count  SF  Throughput@Size
DBMS              SF num_experiment num_client                                      
MonetDB-BHT-8-1-1 1  1              1                 38      1   1          9378.95
MonetDB-BHT-8-2-1 1  2              1                131      1   1          2720.61

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
```bash
## Show Summary

### Workload
TPC-DS Data Profiling SF=10
    Type: tpcds
    Duration: 898s 
    Code: 1748325602
    We compute for all columns: Minimum, maximum, average, count, count distinct, count NULL and non NULL entries and coefficient of variation.
    This experiment compares imported TPC-DS data sets in different DBMS.
    TPC-DS (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.5.
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
    disk:298915504
    datadisk:40080
    volume_size:50G
    volume_used:40G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748325602
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Aug2024
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:298915508
    datadisk:40080
    volume_size:50G
    volume_used:40G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748325602

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                                    MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1
statistics_tab about call_center.cc_call_center_sk - all                            63.45              25.27
statistics_tab about call_center.cc_call_center_id - all                            84.51               5.89
statistics_tab about call_center.cc_rec_start_date - all                            18.83               6.21
statistics_tab about call_center.cc_rec_end_date - all                              25.63               5.11
statistics_tab about call_center.cc_closed_date_sk - all                            27.05               3.54
statistics_tab about call_center.cc_open_date_sk - all                              44.72               3.23
statistics_tab about call_center.cc_name - all                                      38.16               5.19
statistics_tab about call_center.cc_class - all                                     74.30               4.81
statistics_tab about call_center.cc_employees - all                                 35.57               2.88
statistics_tab about call_center.cc_sq_ft - all                                     22.64               3.18
statistics_tab about call_center.cc_hours - all                                     23.91               5.81
statistics_tab about call_center.cc_manager - all                                   36.58               5.19
statistics_tab about call_center.cc_mkt_id - all                                    15.84               3.26
statistics_tab about call_center.cc_mkt_class - all                                 64.77               4.93
statistics_tab about call_center.cc_mkt_desc - all                                 100.42               4.79
statistics_tab about call_center.cc_market_manager - all                            39.44               5.00
statistics_tab about call_center.cc_division - all                                  66.75               2.80
statistics_tab about call_center.cc_division_name - all                             38.27               4.92
statistics_tab about call_center.cc_company - all                                   31.23               2.94
statistics_tab about call_center.cc_company_name - all                              61.64               4.85
statistics_tab about call_center.cc_street_number - all                             27.50               4.66
statistics_tab about call_center.cc_street_name - all                               69.65               4.92
statistics_tab about call_center.cc_street_type - all                               47.05               4.99
statistics_tab about call_center.cc_suite_number - all                              83.42               4.60
statistics_tab about call_center.cc_city - all                                     289.15               5.44
statistics_tab about call_center.cc_county - all                                    54.53               4.98
statistics_tab about call_center.cc_state - all                                     32.53               4.96
statistics_tab about call_center.cc_zip - all                                       35.32               5.77
statistics_tab about call_center.cc_country - all                                   64.46               5.11
statistics_tab about call_center.cc_gmt_offset - all                                38.39               4.29
statistics_tab about call_center.cc_tax_percentage - all                            49.08               3.71
statistics_tab about catalog_page.cp_catalog_page_sk - all                         126.32               3.96
statistics_tab about catalog_page.cp_catalog_page_id - all                         206.39               6.74
statistics_tab about catalog_page.cp_start_date_sk - all                            42.09               4.68
statistics_tab about catalog_page.cp_end_date_sk - all                              20.13               4.16
statistics_tab about catalog_page.cp_department - all                              352.86               6.73
statistics_tab about catalog_page.cp_catalog_number - all                           29.82               4.09
statistics_tab about catalog_page.cp_catalog_page_number - all                      16.69               3.95
statistics_tab about catalog_page.cp_description - all                             128.38               9.64
statistics_tab about catalog_page.cp_type - all                                     70.98               6.41
statistics_tab about catalog_returns.cr_returned_date_sk - all                     124.90              65.63
statistics_tab about catalog_returns.cr_returned_time_sk - all                     385.33              98.92
statistics_tab about catalog_returns.cr_item_sk - all                              164.45              96.04
statistics_tab about catalog_returns.cr_refunded_customer_sk - all                 301.67             115.56
statistics_tab about catalog_returns.cr_refunded_cdemo_sk - all                    424.39             164.18
statistics_tab about catalog_returns.cr_refunded_hdemo_sk - all                    158.20              65.39
statistics_tab about catalog_returns.cr_refunded_addr_sk - all                     207.93              97.54
statistics_tab about catalog_returns.cr_returning_customer_sk - all                272.27             132.38
statistics_tab about catalog_returns.cr_returning_cdemo_sk - all                   351.84             200.58
statistics_tab about catalog_returns.cr_returning_hdemo_sk - all                   175.43              65.33
statistics_tab about catalog_returns.cr_returning_addr_sk - all                    214.02              98.64
statistics_tab about catalog_returns.cr_call_center_sk - all                       406.25              57.35
statistics_tab about catalog_returns.cr_catalog_page_sk - all                      202.16              61.07
statistics_tab about catalog_returns.cr_ship_mode_sk - all                         136.87              61.21
statistics_tab about catalog_returns.cr_warehouse_sk - all                         111.80              58.20
statistics_tab about catalog_returns.cr_reason_sk - all                            303.06              63.85
statistics_tab about catalog_returns.cr_order_number - all                         162.12              76.49
statistics_tab about catalog_returns.cr_return_quantity - all                      165.45              60.58
statistics_tab about catalog_returns.cr_return_amount - all                        191.44             113.02
statistics_tab about catalog_returns.cr_return_tax - all                           171.35              75.20
statistics_tab about catalog_returns.cr_return_amt_inc_tax - all                   422.03             114.37
statistics_tab about catalog_returns.cr_fee - all                                  310.33              59.44
statistics_tab about catalog_returns.cr_return_ship_cost - all                     238.35              96.79
statistics_tab about catalog_returns.cr_refunded_cash - all                        203.15             103.51
statistics_tab about catalog_returns.cr_reversed_charge - all                      154.53              85.29
statistics_tab about catalog_returns.cr_store_credit - all                         195.30              99.03
statistics_tab about catalog_returns.cr_net_loss - all                             216.56             100.31
statistics_tab about catalog_sales.cs_sold_date_sk - all                          1668.59             642.14
statistics_tab about catalog_sales.cs_sold_time_sk - all                          1930.41             731.75
statistics_tab about catalog_sales.cs_ship_date_sk - all                          3251.02             612.76
statistics_tab about catalog_sales.cs_bill_customer_sk - all                      2085.67             860.86
statistics_tab about catalog_sales.cs_bill_cdemo_sk - all                         2070.20             916.40
statistics_tab about catalog_sales.cs_bill_hdemo_sk - all                         2106.43             596.68
statistics_tab about catalog_sales.cs_bill_addr_sk - all                          2078.11             784.80
statistics_tab about catalog_sales.cs_ship_customer_sk - all                      1860.06             833.04
statistics_tab about catalog_sales.cs_ship_cdemo_sk - all                         2123.86             875.46
statistics_tab about catalog_sales.cs_ship_hdemo_sk - all                         2024.71             584.70
statistics_tab about catalog_sales.cs_ship_addr_sk - all                          2117.58             794.25
statistics_tab about catalog_sales.cs_call_center_sk - all                        1937.58             579.03
statistics_tab about catalog_sales.cs_catalog_page_sk - all                       2208.67             582.62
statistics_tab about catalog_sales.cs_ship_mode_sk - all                          1687.75             619.28
statistics_tab about catalog_sales.cs_warehouse_sk - all                          1574.43             614.76
statistics_tab about catalog_sales.cs_item_sk - all                               2105.89             796.93
statistics_tab about catalog_sales.cs_promo_sk - all                              1864.29             619.70
statistics_tab about catalog_sales.cs_order_number - all                          1903.47             855.18
statistics_tab about catalog_sales.cs_quantity - all                              1813.11             611.83
statistics_tab about catalog_sales.cs_wholesale_cost - all                        1670.30             642.59
statistics_tab about catalog_sales.cs_list_price - all                            2225.29             691.94
statistics_tab about catalog_sales.cs_sales_price - all                           2228.71             674.38
statistics_tab about catalog_sales.cs_ext_discount_amt - all                      3346.39            1781.84
statistics_tab about catalog_sales.cs_ext_sales_price - all                       2978.69            1910.28
statistics_tab about catalog_sales.cs_ext_wholesale_cost - all                    2662.74            1596.99
statistics_tab about catalog_sales.cs_ext_list_price - all                        3381.99            2420.14
statistics_tab about catalog_sales.cs_ext_tax - all                               1544.32             833.61
statistics_tab about catalog_sales.cs_coupon_amt - all                            2137.34             948.71
statistics_tab about catalog_sales.cs_ext_ship_cost - all                         2289.57            1396.40
statistics_tab about catalog_sales.cs_net_paid - all                              3133.21            1904.50
statistics_tab about catalog_sales.cs_net_paid_inc_tax - all                      3304.83            2127.88
statistics_tab about catalog_sales.cs_net_paid_inc_ship - all                     3090.33            1874.56
statistics_tab about catalog_sales.cs_net_paid_inc_ship_tax - all                 3674.22            2087.77
statistics_tab about catalog_sales.cs_net_profit - all                            3765.78            2691.74
statistics_tab about customer.c_customer_sk - all                                   68.41              12.16
statistics_tab about customer.c_customer_id - all                                  341.02             182.75
statistics_tab about customer.c_current_cdemo_sk - all                             104.71              59.19
statistics_tab about customer.c_current_hdemo_sk - all                              69.89              26.02
statistics_tab about customer.c_current_addr_sk - all                              231.34              61.20
statistics_tab about customer.c_first_shipto_date_sk - all                          70.45              26.56
statistics_tab about customer.c_first_sales_date_sk - all                           84.17              27.02
statistics_tab about customer.c_salutation - all                                   226.92              10.00
statistics_tab about customer.c_first_name - all                                   221.26              57.54
statistics_tab about customer.c_last_name - all                                    173.39              66.15
statistics_tab about customer.c_preferred_cust_flag - all                          214.51              10.39
statistics_tab about customer.c_birth_day - all                                     67.58              22.02
statistics_tab about customer.c_birth_month - all                                   62.38              27.32
statistics_tab about customer.c_birth_year - all                                    99.17              24.83
statistics_tab about customer.c_birth_country - all                                 59.67              10.86
statistics_tab about customer.c_login - all                                        213.79               8.75
statistics_tab about customer.c_email_address - all                                672.27             196.38
statistics_tab about customer.c_last_review_date - all                              61.76              10.65
statistics_tab about customer_address.ca_address_sk - all                           57.66               9.72
statistics_tab about customer_address.ca_address_id - all                          292.06              70.08
statistics_tab about customer_address.ca_street_number - all                        50.97               8.82
statistics_tab about customer_address.ca_street_name - all                          92.29              35.15
statistics_tab about customer_address.ca_street_type - all                         205.68               8.98
statistics_tab about customer_address.ca_suite_number - all                        214.38               9.13
statistics_tab about customer_address.ca_city - all                                410.92               8.37
statistics_tab about customer_address.ca_county - all                              141.12               8.87
statistics_tab about customer_address.ca_state - all                                58.54              17.62
statistics_tab about customer_address.ca_zip - all                                 139.77              30.76
statistics_tab about customer_address.ca_country - all                             148.43               7.79
statistics_tab about customer_address.ca_gmt_offset - all                           64.09              12.32
statistics_tab about customer_address.ca_location_type - all                        76.13               7.42
statistics_tab about customer_demographics.cd_demo_sk - all                        277.19              11.98
statistics_tab about customer_demographics.cd_gender - all                          98.39              19.73
statistics_tab about customer_demographics.cd_marital_status - all                 231.72              20.67
statistics_tab about customer_demographics.cd_education_status - all               163.28              20.97
statistics_tab about customer_demographics.cd_purchase_estimate - all              225.80             106.84
statistics_tab about customer_demographics.cd_credit_rating - all                  279.53              20.83
statistics_tab about customer_demographics.cd_dep_count - all                      428.70              75.76
statistics_tab about customer_demographics.cd_dep_employed_count - all             292.96             100.21
statistics_tab about customer_demographics.cd_dep_college_count - all              131.49              91.33
statistics_tab about date_dim.d_date_sk - all                                       44.62               5.83
statistics_tab about date_dim.d_date_id - all                                      154.23              17.83
statistics_tab about date_dim.d_date - all                                          55.10               7.14
statistics_tab about date_dim.d_month_seq - all                                     94.46               5.39
statistics_tab about date_dim.d_week_seq - all                                     129.24               7.21
statistics_tab about date_dim.d_quarter_seq - all                                  104.26               5.54
statistics_tab about date_dim.d_year - all                                          27.26               6.67
statistics_tab about date_dim.d_dow - all                                           33.60               5.37
statistics_tab about date_dim.d_moy - all                                           34.23               6.38
statistics_tab about date_dim.d_dom - all                                          100.23               6.56
statistics_tab about date_dim.d_qoy - all                                           63.10               5.97
statistics_tab about date_dim.d_fy_year - all                                       24.89               5.85
statistics_tab about date_dim.d_fy_quarter_seq - all                               106.10               5.93
statistics_tab about date_dim.d_fy_week_seq - all                                   39.31               5.10
statistics_tab about date_dim.d_day_name - all                                      63.38               6.16
statistics_tab about date_dim.d_quarter_name - all                                  92.13               6.17
statistics_tab about date_dim.d_holiday - all                                      121.36               6.76
statistics_tab about date_dim.d_weekend - all                                       56.56               6.45
statistics_tab about date_dim.d_following_holiday - all                            120.75               6.19
statistics_tab about date_dim.d_first_dom - all                                     40.14               5.86
statistics_tab about date_dim.d_last_dom - all                                      33.52               6.37
statistics_tab about date_dim.d_same_day_ly - all                                  107.27               6.13
statistics_tab about date_dim.d_same_day_lq - all                                   56.23               6.23
statistics_tab about date_dim.d_current_day - all                                   75.05               6.52
statistics_tab about date_dim.d_current_week - all                                 128.60               5.87
statistics_tab about date_dim.d_current_month - all                                 79.32               6.65
statistics_tab about date_dim.d_current_quarter - all                               49.82              10.80
statistics_tab about date_dim.d_current_year - all                                  98.37               6.25
statistics_tab about dbgen_version.dv_version - all                                 64.34               4.75
statistics_tab about dbgen_version.dv_create_date - all                             25.94               5.10
statistics_tab about dbgen_version.dv_create_time - all                             40.23               5.42
statistics_tab about dbgen_version.dv_cmdline_args - all                           101.68               5.61
statistics_tab about household_demographics.hd_demo_sk - all                        72.97               3.84
statistics_tab about household_demographics.hd_income_band_sk - all                 18.39               3.49
statistics_tab about household_demographics.hd_buy_potential - all                 334.42               5.05
statistics_tab about household_demographics.hd_dep_count - all                      21.85               3.23
statistics_tab about household_demographics.hd_vehicle_count - all                  16.88               3.57
statistics_tab about income_band.ib_income_band_sk - all                           232.71               3.51
statistics_tab about income_band.ib_lower_bound - all                               86.36               3.28
statistics_tab about income_band.ib_upper_bound - all                               41.94               3.11
statistics_tab about inventory.inv_date_sk - all                                 15528.54            5356.14
statistics_tab about inventory.inv_item_sk - all                                 17476.30            5438.38
statistics_tab about inventory.inv_warehouse_sk - all                            15354.57            5304.41
statistics_tab about inventory.inv_quantity_on_hand - all                        18162.04            5613.06
statistics_tab about item.i_item_sk - all                                          192.84               6.06
statistics_tab about item.i_item_id - all                                           95.74              21.39
statistics_tab about item.i_rec_start_date - all                                    47.23               8.08
statistics_tab about item.i_rec_end_date - all                                     113.28               8.62
statistics_tab about item.i_item_desc - all                                        296.48              63.99
statistics_tab about item.i_current_price - all                                     32.23               7.20
statistics_tab about item.i_wholesale_cost - all                                    24.20               7.17
statistics_tab about item.i_brand_id - all                                          76.37               8.23
statistics_tab about item.i_brand - all                                            146.87               6.62
statistics_tab about item.i_class_id - all                                          20.18               7.20
statistics_tab about item.i_class - all                                             98.00               6.90
statistics_tab about item.i_category_id - all                                       54.16               6.72
statistics_tab about item.i_category - all                                          74.97              16.53
statistics_tab about item.i_manufact_id - all                                       47.63               7.32
statistics_tab about item.i_manufact - all                                          77.76               6.86
statistics_tab about item.i_size - all                                             129.64               7.01
statistics_tab about item.i_formulation - all                                      116.94              29.37
statistics_tab about item.i_color - all                                             43.04               6.91
statistics_tab about item.i_units - all                                             76.20               6.24
statistics_tab about item.i_container - all                                        181.78               5.86
statistics_tab about item.i_manager_id - all                                        52.67               7.06
statistics_tab about item.i_product_name - all                                     135.83              34.88
statistics_tab about promotion.p_promo_sk - all                                     27.19               2.89
statistics_tab about promotion.p_promo_id - all                                    124.35               4.89
statistics_tab about promotion.p_start_date_sk - all                                56.70               2.87
statistics_tab about promotion.p_end_date_sk - all                                  31.38               3.05
statistics_tab about promotion.p_item_sk - all                                      20.13               2.84
statistics_tab about promotion.p_cost - all                                         33.69               4.21
statistics_tab about promotion.p_response_target - all                              17.26               3.54
statistics_tab about promotion.p_promo_name - all                                  166.10               5.02
statistics_tab about promotion.p_channel_dmail - all                                64.70               5.34
statistics_tab about promotion.p_channel_email - all                               243.86               5.06
statistics_tab about promotion.p_channel_catalog - all                              67.45               4.66
statistics_tab about promotion.p_channel_tv - all                                   79.62               5.33
statistics_tab about promotion.p_channel_radio - all                                70.52               5.10
statistics_tab about promotion.p_channel_press - all                                79.46               5.56
statistics_tab about promotion.p_channel_event - all                                61.34               5.48
statistics_tab about promotion.p_channel_demo - all                                253.92               5.52
statistics_tab about promotion.p_channel_details - all                             168.26               5.33
statistics_tab about promotion.p_purpose - all                                      67.12               6.72
statistics_tab about promotion.p_discount_active - all                              34.18               5.76
statistics_tab about reason.r_reason_sk - all                                       35.20               3.10
statistics_tab about reason.r_reason_id - all                                      203.78               5.06
statistics_tab about reason.r_reason_desc - all                                     56.53               6.52
statistics_tab about ship_mode.sm_ship_mode_sk - all                                50.04               4.23
statistics_tab about ship_mode.sm_ship_mode_id - all                                99.13               5.60
statistics_tab about ship_mode.sm_type - all                                        90.33               5.07
statistics_tab about ship_mode.sm_code - all                                        56.34               5.55
statistics_tab about ship_mode.sm_carrier - all                                     54.86               5.68
statistics_tab about ship_mode.sm_contract - all                                    84.66               4.98
statistics_tab about store.s_store_sk - all                                         25.21               3.47
statistics_tab about store.s_store_id - all                                        155.48               5.51
statistics_tab about store.s_rec_start_date - all                                    8.09               4.66
statistics_tab about store.s_rec_end_date - all                                     13.96               4.50
statistics_tab about store.s_closed_date_sk - all                                   16.63               3.12
statistics_tab about store.s_store_name - all                                      371.80               8.62
statistics_tab about store.s_number_employees - all                                  5.99               3.78
statistics_tab about store.s_floor_space - all                                      40.66               3.46
statistics_tab about store.s_hours - all                                            48.28               5.19
statistics_tab about store.s_manager - all                                          28.93               5.70
statistics_tab about store.s_market_id - all                                        39.67               2.88
statistics_tab about store.s_geography_class - all                                  75.77               4.89
statistics_tab about store.s_market_desc - all                                      52.44               5.10
statistics_tab about store.s_market_manager - all                                   34.77               4.41
statistics_tab about store.s_division_id - all                                     123.95               3.10
statistics_tab about store.s_division_name - all                                   254.96               5.63
statistics_tab about store.s_company_id - all                                       84.10               3.77
statistics_tab about store.s_company_name - all                                     43.16               5.86
statistics_tab about store.s_street_number - all                                    52.78               5.15
statistics_tab about store.s_street_name - all                                      26.97               5.01
statistics_tab about store.s_street_type - all                                      78.54               6.04
statistics_tab about store.s_suite_number - all                                     34.87               7.16
statistics_tab about store.s_city - all                                             45.09               4.88
statistics_tab about store.s_county - all                                          125.72               4.91
statistics_tab about store.s_state - all                                            60.93               4.66
statistics_tab about store.s_zip - all                                             145.24               4.88
statistics_tab about store.s_country - all                                          48.11               5.07
statistics_tab about store.s_gmt_offset - all                                       31.70               3.72
statistics_tab about store.s_tax_precentage - all                                   41.50               3.16
statistics_tab about store_returns.sr_returned_date_sk - all                       331.03             148.99
statistics_tab about store_returns.sr_return_time_sk - all                         986.80             137.97
statistics_tab about store_returns.sr_item_sk - all                                587.34             172.83
statistics_tab about store_returns.sr_customer_sk - all                            483.55             283.34
statistics_tab about store_returns.sr_cdemo_sk - all                               650.14             455.19
statistics_tab about store_returns.sr_hdemo_sk - all                               311.31             124.14
statistics_tab about store_returns.sr_addr_sk - all                                430.19             199.80
statistics_tab about store_returns.sr_store_sk - all                               404.37             123.52
statistics_tab about store_returns.sr_reason_sk - all                              417.75             107.71
statistics_tab about store_returns.sr_ticket_number - all                          412.74             153.91
statistics_tab about store_returns.sr_return_quantity - all                        311.18             114.44
statistics_tab about store_returns.sr_return_amt - all                             449.92             231.31
statistics_tab about store_returns.sr_return_tax - all                             372.45             139.92
statistics_tab about store_returns.sr_return_amt_inc_tax - all                     533.15             222.43
statistics_tab about store_returns.sr_fee - all                                    597.26             122.94
statistics_tab about store_returns.sr_return_ship_cost - all                       556.51             188.34
statistics_tab about store_returns.sr_refunded_cash - all                          512.77             206.26
statistics_tab about store_returns.sr_reversed_charge - all                        688.53             173.08
statistics_tab about store_returns.sr_store_credit - all                           483.34             177.14
statistics_tab about store_returns.sr_net_loss - all                               711.24             214.42
statistics_tab about store_sales.ss_sold_date_sk - all                            3225.17            1149.75
statistics_tab about store_sales.ss_sold_time_sk - all                            3430.67            1267.56
statistics_tab about store_sales.ss_item_sk - all                                 3364.10            1406.77
statistics_tab about store_sales.ss_customer_sk - all                             4220.98            1780.94
statistics_tab about store_sales.ss_cdemo_sk - all                                3893.32            1754.21
statistics_tab about store_sales.ss_hdemo_sk - all                                3257.67            1178.38
statistics_tab about store_sales.ss_addr_sk - all                                 4242.48            1562.23
statistics_tab about store_sales.ss_store_sk - all                                3585.38            1152.45
statistics_tab about store_sales.ss_promo_sk - all                                3182.10            1223.27
statistics_tab about store_sales.ss_ticket_number - all                           3399.91            1344.79
statistics_tab about store_sales.ss_quantity - all                                3726.29            1214.92
statistics_tab about store_sales.ss_wholesale_cost - all                          3547.23            1256.89
statistics_tab about store_sales.ss_list_price - all                              3720.34            1329.70
statistics_tab about store_sales.ss_sales_price - all                             3696.62            1309.91
statistics_tab about store_sales.ss_ext_discount_amt - all                        4040.04            1830.24
statistics_tab about store_sales.ss_ext_sales_price - all                         5645.82            3420.94
statistics_tab about store_sales.ss_ext_wholesale_cost - all                      5553.22            3043.89
statistics_tab about store_sales.ss_ext_list_price - all                          7711.16            4019.82
statistics_tab about store_sales.ss_ext_tax - all                                 3734.90            1537.74
statistics_tab about store_sales.ss_coupon_amt - all                              4700.96            1839.49
statistics_tab about store_sales.ss_net_paid - all                                5785.81            3178.05
statistics_tab about store_sales.ss_net_paid_inc_tax - all                        5955.50            3671.30
statistics_tab about store_sales.ss_net_profit - all                              7709.77            5682.20
statistics_tab about time_dim.t_time_sk - all                                       39.48               8.08
statistics_tab about time_dim.t_time_id - all                                      107.61              30.62
statistics_tab about time_dim.t_time - all                                          45.85               7.56
statistics_tab about time_dim.t_hour - all                                          99.39               6.96
statistics_tab about time_dim.t_minute - all                                        98.20               6.58
statistics_tab about time_dim.t_second - all                                       173.51               6.32
statistics_tab about time_dim.t_am_pm - all                                        122.71               5.91
statistics_tab about time_dim.t_shift - all                                        296.84               6.96
statistics_tab about time_dim.t_sub_shift - all                                     45.61               7.01
statistics_tab about time_dim.t_meal_time - all                                    200.92               7.20
statistics_tab about warehouse.w_warehouse_sk - all                                 17.03               3.66
statistics_tab about warehouse.w_warehouse_id - all                                108.09               4.66
statistics_tab about warehouse.w_warehouse_name - all                              124.95               5.45
statistics_tab about warehouse.w_warehouse_sq_ft - all                              61.57               3.34
statistics_tab about warehouse.w_street_number - all                               191.26               5.34
statistics_tab about warehouse.w_street_name - all                                  50.93              10.35
statistics_tab about warehouse.w_street_type - all                                  33.07               5.01
statistics_tab about warehouse.w_suite_number - all                                 40.79               4.94
statistics_tab about warehouse.w_city - all                                         89.33               5.49
statistics_tab about warehouse.w_county - all                                       75.80               4.56
statistics_tab about warehouse.w_state - all                                        36.11               4.97
statistics_tab about warehouse.w_zip - all                                         106.94               4.98
statistics_tab about warehouse.w_country - all                                      26.58               4.90
statistics_tab about warehouse.w_gmt_offset - all                                  114.36               3.26
statistics_tab about web_page.wp_web_page_sk - all                                  30.85               3.03
statistics_tab about web_page.wp_web_page_id - all                                  63.85               5.03
statistics_tab about web_page.wp_rec_start_date - all                               22.26               4.67
statistics_tab about web_page.wp_rec_end_date - all                                  7.66               5.73
statistics_tab about web_page.wp_creation_date_sk - all                             37.41               3.09
statistics_tab about web_page.wp_access_date_sk - all                                5.90               2.92
statistics_tab about web_page.wp_autogen_flag - all                                 85.52               4.68
statistics_tab about web_page.wp_customer_sk - all                                  19.95               3.72
statistics_tab about web_page.wp_url - all                                         128.26               5.24
statistics_tab about web_page.wp_type - all                                         42.35               5.13
statistics_tab about web_page.wp_char_count - all                                   69.63               3.13
statistics_tab about web_page.wp_link_count - all                                    6.85               2.84
statistics_tab about web_page.wp_image_count - all                                  36.87               2.90
statistics_tab about web_page.wp_max_ad_count - all                                 17.97               3.04
statistics_tab about web_returns.wr_returned_date_sk - all                         114.73              37.13
statistics_tab about web_returns.wr_returned_time_sk - all                         108.51              40.42
statistics_tab about web_returns.wr_item_sk - all                                   89.56              45.69
statistics_tab about web_returns.wr_refunded_customer_sk - all                     110.38              55.95
statistics_tab about web_returns.wr_refunded_cdemo_sk - all                        194.95              82.33
statistics_tab about web_returns.wr_refunded_hdemo_sk - all                         90.42              33.64
statistics_tab about web_returns.wr_refunded_addr_sk - all                         130.03              54.25
statistics_tab about web_returns.wr_returning_customer_sk - all                    128.02              56.80
statistics_tab about web_returns.wr_returning_cdemo_sk - all                       172.61              87.45
statistics_tab about web_returns.wr_returning_hdemo_sk - all                        94.42              32.94
statistics_tab about web_returns.wr_returning_addr_sk - all                        128.19              49.13
statistics_tab about web_returns.wr_web_page_sk - all                              168.47              29.60
statistics_tab about web_returns.wr_reason_sk - all                                124.92              43.24
statistics_tab about web_returns.wr_order_number - all                              99.99              27.81
statistics_tab about web_returns.wr_return_quantity - all                          101.39              31.54
statistics_tab about web_returns.wr_return_amt - all                               153.23              58.45
statistics_tab about web_returns.wr_return_tax - all                               137.93              38.22
statistics_tab about web_returns.wr_return_amt_inc_tax - all                       164.10              65.48
statistics_tab about web_returns.wr_fee - all                                      288.41              32.15
statistics_tab about web_returns.wr_return_ship_cost - all                         213.61              56.35
statistics_tab about web_returns.wr_refunded_cash - all                            113.58              51.39
statistics_tab about web_returns.wr_reversed_charge - all                          141.07              50.31
statistics_tab about web_returns.wr_account_credit - all                           128.79              47.68
statistics_tab about web_returns.wr_net_loss - all                                 123.13              51.10
statistics_tab about web_sales.ws_sold_date_sk - all                              1456.93             298.05
statistics_tab about web_sales.ws_sold_time_sk - all                               709.41             349.01
statistics_tab about web_sales.ws_ship_date_sk - all                              1152.64             286.21
statistics_tab about web_sales.ws_item_sk - all                                    737.99             351.47
statistics_tab about web_sales.ws_bill_customer_sk - all                           813.63             404.03
statistics_tab about web_sales.ws_bill_cdemo_sk - all                             1333.50             423.31
statistics_tab about web_sales.ws_bill_hdemo_sk - all                             1071.19             330.57
statistics_tab about web_sales.ws_bill_addr_sk - all                              1251.45             384.43
statistics_tab about web_sales.ws_ship_customer_sk - all                          1188.26             404.85
statistics_tab about web_sales.ws_ship_cdemo_sk - all                              854.55             468.25
statistics_tab about web_sales.ws_ship_hdemo_sk - all                              719.75             314.61
statistics_tab about web_sales.ws_ship_addr_sk - all                              1139.33             378.91
statistics_tab about web_sales.ws_web_page_sk - all                               1111.52             312.94
statistics_tab about web_sales.ws_web_site_sk - all                                922.97             289.11
statistics_tab about web_sales.ws_ship_mode_sk - all                              1008.08             310.80
statistics_tab about web_sales.ws_warehouse_sk - all                               954.37             332.11
statistics_tab about web_sales.ws_promo_sk - all                                   647.76             308.42
statistics_tab about web_sales.ws_order_number - all                               583.41             253.24
statistics_tab about web_sales.ws_quantity - all                                  1120.19             308.31
statistics_tab about web_sales.ws_wholesale_cost - all                             694.44             302.59
statistics_tab about web_sales.ws_list_price - all                                 752.48             337.20
statistics_tab about web_sales.ws_sales_price - all                                886.38             314.08
statistics_tab about web_sales.ws_ext_discount_amt - all                          1706.22             850.21
statistics_tab about web_sales.ws_ext_sales_price - all                           1556.26             860.59
statistics_tab about web_sales.ws_ext_wholesale_cost - all                        1361.97             765.00
statistics_tab about web_sales.ws_ext_list_price - all                            1711.67            1307.70
statistics_tab about web_sales.ws_ext_tax - all                                   1051.68             391.78
statistics_tab about web_sales.ws_coupon_amt - all                                1021.52             387.81
statistics_tab about web_sales.ws_ext_ship_cost - all                             1632.42             634.26
statistics_tab about web_sales.ws_net_paid - all                                  1463.10             804.00
statistics_tab about web_sales.ws_net_paid_inc_tax - all                          1911.86             916.61
statistics_tab about web_sales.ws_net_paid_inc_ship - all                         1365.19            1020.93
statistics_tab about web_sales.ws_net_paid_inc_ship_tax - all                     1328.35            1017.54
statistics_tab about web_sales.ws_net_profit - all                                1691.80            1304.24
statistics_tab about web_site.web_site_sk - all                                    130.03               3.53
statistics_tab about web_site.web_site_id - all                                     53.09               5.16
statistics_tab about web_site.web_rec_start_date - all                              38.36               4.68
statistics_tab about web_site.web_rec_end_date - all                                32.44               5.44
statistics_tab about web_site.web_name - all                                        53.18               4.94
statistics_tab about web_site.web_open_date_sk - all                                16.59               3.19
statistics_tab about web_site.web_close_date_sk - all                              106.66               3.03
statistics_tab about web_site.web_class - all                                       43.66               4.86
statistics_tab about web_site.web_manager - all                                    115.10               5.81
statistics_tab about web_site.web_mkt_id - all                                      12.39               2.82
statistics_tab about web_site.web_mkt_class - all                                  147.50               5.58
statistics_tab about web_site.web_mkt_desc - all                                    79.36               5.08
statistics_tab about web_site.web_market_manager - all                              74.65               5.72
statistics_tab about web_site.web_company_id - all                                  68.89               3.53
statistics_tab about web_site.web_company_name - all                               330.56               4.96
statistics_tab about web_site.web_street_number - all                              206.24               5.31
statistics_tab about web_site.web_street_name - all                                 49.25               5.41
statistics_tab about web_site.web_street_type - all                                 22.74               5.66
statistics_tab about web_site.web_suite_number - all                                71.81               5.23
statistics_tab about web_site.web_city - all                                       112.83               5.09
statistics_tab about web_site.web_county - all                                     123.62               5.00
statistics_tab about web_site.web_state - all                                       95.76               4.71
statistics_tab about web_site.web_zip - all                                         90.14               7.48
statistics_tab about web_site.web_country - all                                     42.84               5.13
statistics_tab about web_site.web_gmt_offset - all                                  23.93               2.94
statistics_tab about web_site.web_tax_percentage - all                              26.92               3.24

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          339.0         9.0      695.0    1051.0
MonetDB-BHT-8-2-1           1.0          339.0         9.0      695.0    1051.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.18
MonetDB-BHT-8-2-1           0.03

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1          201828.09
MonetDB-BHT-8-2-1         1189101.13

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MonetDB-BHT-8-1 10 1              1                400      1  10         38610.00
MonetDB-BHT-8-2 10 1              2                188      1  10         82148.94

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      407.56     1.52          2.30                12.58
MonetDB-BHT-8-2      406.16     1.47         10.79                14.73

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       27.12     0.07          0.26                 0.28
MonetDB-BHT-8-2       27.12     0.09          0.51                 0.54

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
  -rst shared -rss 1000Gi \
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
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_monetdb_3.log &
```

### Evaluate Results

doc_tpcds_monetdb_3.log
```bash
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

