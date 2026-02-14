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
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_compare.log &
```

This
* starts a clean instance of PostgreSQL, MonetDB, MySQL and MariaDB (one after the other, `-ms`)
  * fixed 64 Gi RAM (request `-rr` and limit `-rl`)
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
    Duration: 37012s 
    Code: 1766194209
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.19.
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
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:439579
    cpu_list:0-63
    args:['--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766194209
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:440499
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766194209
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:473290
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766194209
PostgreSQL-BHT-8-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:440827
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766194209

### Errors (failed queries)
            MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q72               True              False             False                 False
TPC-DS Q94               True              False             False                 False
TPC-DS Q95               True              False             False                 False
TPC-DS Q72
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=290) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q94
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=290) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q95
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=290) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)
               MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q27                 False               True             False                  True
TPC-DS Q36                 False               True              True                  True
TPC-DS Q39a+b              False               True              True                  True
TPC-DS Q47                 False               True             False                 False
TPC-DS Q56                 False              False             False                  True
TPC-DS Q70                 False               True             False                 False
TPC-DS Q72                 False               True              True                  True
TPC-DS Q78                 False               True             False                  True
TPC-DS Q80                 False               True             False                  True
TPC-DS Q86                 False               True              True                  True
TPC-DS Q94                 False               True              True                  True
TPC-DS Q95                 False               True              True                  True
TPC-DS Q98                 False               True             False                 False

### Latency of Timer Execution [ms]
DBMS           MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q1                  62.13              41.28            102.37                348.68
TPC-DS Q2               19059.70             806.15          20714.88               1538.91
TPC-DS Q3                  21.88             230.43             30.39               2149.37
TPC-DS Q4               43945.23           10682.39         112260.82              24458.31
TPC-DS Q5               32034.99             574.00          51805.08               1590.58
TPC-DS Q6                2995.91             620.02         310761.47             252152.15
TPC-DS Q7               13451.01             204.39           2869.87               1070.70
TPC-DS Q8                1166.92              73.84           1592.79                153.84
TPC-DS Q9               14216.15             177.76          16447.85               6060.82
TPC-DS Q10               1576.46             189.65            218.71               2877.92
TPC-DS Q11              25447.55            2394.10          70049.24              11342.99
TPC-DS Q12                959.66              81.00           1447.50                205.57
TPC-DS Q13               2977.47             303.07           4507.51               1874.23
TPC-DS Q14a+b          172136.41            7421.52         203617.96               6325.45
TPC-DS Q15                564.13             102.12            783.54                343.74
TPC-DS Q16              47316.78              73.22            365.89                555.93
TPC-DS Q17               7763.42             333.97           2241.26                968.30
TPC-DS Q18               8962.54             228.68           3496.61               1267.54
TPC-DS Q19                863.12              86.77           1277.34                488.92
TPC-DS Q20               1784.88              45.17           2488.88                307.48
TPC-DS Q21             100498.52             136.18         133260.96                679.72
TPC-DS Q22             286224.44            4186.79          22417.43               9887.60
TPC-DS Q23a+b          193389.26            9042.85         159280.91              10569.00
TPC-DS Q24a+b             295.17            1443.65           5387.76               2004.74
TPC-DS Q25               1467.30             354.25            534.28                891.74
TPC-DS Q26               4783.78              44.09          23909.73               2460.82
TPC-DS Q27               5071.20             373.61           2222.40                349.00
TPC-DS Q28               9144.11             205.14          12538.55               7966.25
TPC-DS Q29                255.07             307.57            306.80               8975.75
TPC-DS Q30                309.51             178.45           1714.05              32141.87
TPC-DS Q31               4472.77             393.12          51615.83               9146.51
TPC-DS Q32                 14.73              86.21            425.20                433.37
TPC-DS Q33                782.46              80.33           1054.26               2553.87
TPC-DS Q34              12902.74             104.81           4428.33                345.04
TPC-DS Q35               4550.25             611.92          64570.57               4772.00
TPC-DS Q36               9705.24             507.57          12674.68               1392.08
TPC-DS Q37              13783.58             294.18             37.36               1155.11
TPC-DS Q38              27362.41            1018.63          37682.10               3561.84
TPC-DS Q39a+b            4605.46            3547.54           8513.49               6219.03
TPC-DS Q40               1035.87             258.13            792.87                339.47
TPC-DS Q41               1382.08              15.38           5332.26               2821.16
TPC-DS Q42                768.97              73.45             89.23                246.29
TPC-DS Q43               3772.76             107.27              2.54                 58.76
TPC-DS Q44                 63.83              98.25              2.85                  2.82
TPC-DS Q45                500.27              47.30            510.35                234.45
TPC-DS Q46              13775.60             137.40           3255.03                 79.58
TPC-DS Q47              41688.97             840.77          32464.01               4927.87
TPC-DS Q48               3677.79             109.67           4913.58               2946.50
TPC-DS Q49               1017.94             226.61           1667.41               4335.79
TPC-DS Q50                156.88             257.79            115.09               2438.48
TPC-DS Q51              26857.20            1835.85          28193.26               3190.20
TPC-DS Q52                793.16             140.68             97.01                538.42
TPC-DS Q53                523.68              91.26           1105.05                566.41
TPC-DS Q54               2896.32              89.67          12705.91                530.06
TPC-DS Q55                795.58              38.76             89.61                550.67
TPC-DS Q56                781.09              53.17           1004.97               1679.33
TPC-DS Q57              22981.57             198.30          16006.57               2855.14
TPC-DS Q58              23813.50             111.85          30684.30               1815.43
TPC-DS Q59              36612.90             369.09          29492.39               1565.49
TPC-DS Q60               1056.88              54.37           1932.63               1412.03
TPC-DS Q61               1288.60             160.63              3.40               3882.83
TPC-DS Q62               6403.63             162.35          13408.14                566.69
TPC-DS Q63                613.32             142.64           1127.88                516.06
TPC-DS Q64               2157.80            1116.91           1748.00               2549.54
TPC-DS Q65              23506.92             262.08          34615.90               2150.58
TPC-DS Q66               4362.06             385.55           9631.70                834.08
TPC-DS Q67              25645.95            4162.06          36930.84               7215.49
TPC-DS Q68              12574.77              84.86           1266.92                 76.79
TPC-DS Q69               1178.34             100.42           1914.21                649.84
TPC-DS Q70              34103.11             494.25          59563.17               1127.27
TPC-DS Q71               1757.12             139.63           1948.15                948.72
TPC-DS Q73              11690.39              57.34           4186.37                 57.63
TPC-DS Q74              22172.30            1641.66          22677.65               3099.87
TPC-DS Q75              19040.72            1240.38           8336.19               2596.06
TPC-DS Q76               2633.86              67.47           1718.58                911.09
TPC-DS Q77              24580.17             112.78          44606.00               6236.71
TPC-DS Q78              20138.29            2055.85          49707.94               8767.92
TPC-DS Q79              12842.84             100.26          19645.35               1026.41
TPC-DS Q80               2255.92            8016.31          38595.06               2639.23
TPC-DS Q81                810.46              44.29           6966.24             137329.68
TPC-DS Q82              13976.93             248.61             29.68               2456.36
TPC-DS Q83               3024.25              23.15           3850.75               1756.32
TPC-DS Q84                351.95              22.95            251.75                133.31
TPC-DS Q85                468.12             248.79            460.04               1904.66
TPC-DS Q86               3571.49              71.36           5354.34                920.82
TPC-DS Q87              27818.49             423.40          37665.38               8959.90
TPC-DS Q88              61431.56             159.29           6785.32              10932.56
TPC-DS Q89               7687.86             101.44            189.79                463.66
TPC-DS Q90                569.56              30.03           1463.02               2751.10
TPC-DS Q91                 92.29              73.08             58.84                708.08
TPC-DS Q92                 26.84              39.72            370.12                599.34
TPC-DS Q93                191.72             940.07            138.56               1250.83
TPC-DS Q96               3132.97              24.07            474.50                261.83
TPC-DS Q97              19673.59            1011.28          26851.19                985.36
TPC-DS Q98               3496.97              74.49           5050.29                506.24
TPC-DS Q99              20182.43             139.79          54475.29                403.64

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1              1.0          720.0         9.0    14426.0   15165.0
MonetDB-BHT-8-1-1              1.0          117.0        13.0      342.0     482.0
MySQL-BHT-64-1-1               1.0          428.0        12.0    12183.0   12633.0
PostgreSQL-BHT-8-1-1           1.0          174.0         2.0      464.0     649.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              3.57
MonetDB-BHT-8-1-1              0.23
MySQL-BHT-64-1-1               2.98
PostgreSQL-BHT-8-1-1           1.42

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1               1011.66
MonetDB-BHT-8-1-1              16122.64
MySQL-BHT-64-1-1                1213.43
PostgreSQL-BHT-8-1-1            2558.24

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
MariaDB-BHT-8-1    1.0 1              1               5269      1  1.0            65.59
MonetDB-BHT-8-1    1.0 1              1                 92      1  1.0          3756.52
MySQL-BHT-64-1     1.0 1              1               2107      1  1.0           164.02
PostgreSQL-BHT-8-1 1.0 1              1                701      1  1.0           493.01

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MariaDB-BHT-8-1-1        MariaDB-BHT-8-1  1.0     8               1           1       1766211065     1766216334
MonetDB-BHT-8-1-1        MonetDB-BHT-8-1  1.0     8               1           1       1766196216     1766196308
MySQL-BHT-64-1-1          MySQL-BHT-64-1  1.0     8               1           1       1766229027     1766231134
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  1.0     8               1           1       1766194899     1766195600

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
  -rr 64Gi -lr 64Gi \
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
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 910s 
    Code: 1766153904
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.19.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:447271
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766153904

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                  69.48
TPC-DS Q2                 717.34
TPC-DS Q3                  52.33
TPC-DS Q4                4368.62
TPC-DS Q5                 366.81
TPC-DS Q6                 248.73
TPC-DS Q7                  91.15
TPC-DS Q8                 104.38
TPC-DS Q9                 149.15
TPC-DS Q10                 67.71
TPC-DS Q11               1942.81
TPC-DS Q12                 35.42
TPC-DS Q13                133.48
TPC-DS Q14a+b            7474.38
TPC-DS Q15                 50.43
TPC-DS Q16                334.24
TPC-DS Q17                465.34
TPC-DS Q18                245.27
TPC-DS Q19                 83.66
TPC-DS Q20                 57.26
TPC-DS Q21                 96.64
TPC-DS Q22               2756.94
TPC-DS Q23a+b            9905.13
TPC-DS Q24a+b            1100.17
TPC-DS Q25                376.62
TPC-DS Q26                118.49
TPC-DS Q27                359.52
TPC-DS Q28                182.23
TPC-DS Q29                384.15
TPC-DS Q30                 37.46
TPC-DS Q31                511.78
TPC-DS Q32                 42.04
TPC-DS Q33                 52.52
TPC-DS Q34                 66.76
TPC-DS Q35                207.45
TPC-DS Q36                247.12
TPC-DS Q37                 91.05
TPC-DS Q38                628.88
TPC-DS Q39a+b            3976.87
TPC-DS Q40                244.95
TPC-DS Q41                  7.28
TPC-DS Q42                 34.47
TPC-DS Q43                103.17
TPC-DS Q44                112.97
TPC-DS Q45                 23.42
TPC-DS Q46                 93.31
TPC-DS Q47                619.78
TPC-DS Q48                100.23
TPC-DS Q49                342.69
TPC-DS Q50                237.35
TPC-DS Q51               1504.39
TPC-DS Q52                 41.45
TPC-DS Q53                 50.69
TPC-DS Q54                 56.21
TPC-DS Q55                 29.00
TPC-DS Q56                 44.44
TPC-DS Q57                144.02
TPC-DS Q58                166.86
TPC-DS Q59                280.99
TPC-DS Q60                 47.52
TPC-DS Q61                 75.39
TPC-DS Q62                 49.76
TPC-DS Q63                 43.41
TPC-DS Q64               1269.91
TPC-DS Q65                461.86
TPC-DS Q66                301.35
TPC-DS Q67               1430.15
TPC-DS Q68                 90.48
TPC-DS Q69                 87.49
TPC-DS Q70                264.88
TPC-DS Q71                 65.39
TPC-DS Q72                250.19
TPC-DS Q73                 43.87
TPC-DS Q74                538.62
TPC-DS Q75               2036.27
TPC-DS Q76                167.30
TPC-DS Q77                170.97
TPC-DS Q78               3113.85
TPC-DS Q79                 78.07
TPC-DS Q80               2314.78
TPC-DS Q81                 51.34
TPC-DS Q82                393.72
TPC-DS Q83                 28.22
TPC-DS Q84                126.83
TPC-DS Q85                 58.86
TPC-DS Q86                 75.89
TPC-DS Q87                794.70
TPC-DS Q88                183.59
TPC-DS Q89                 83.62
TPC-DS Q90                 19.12
TPC-DS Q91                 25.37
TPC-DS Q92                 20.15
TPC-DS Q93                508.70
TPC-DS Q94                 64.34
TPC-DS Q95               1294.89
TPC-DS Q96                 23.36
TPC-DS Q97                995.32
TPC-DS Q98                 81.44
TPC-DS Q99                 94.73

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          266.0        16.0      597.0     887.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.18

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           61654.51

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MonetDB-BHT-8-1 3.0 1              1                 71      1  3.0         15059.15

### Workflow
                         orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  3.0     8               1           1       1766154664     1766154735

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       35.18     0.18          0.01                 2.65

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      295.03     4.97          7.76                15.68

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       13.22        0          0.31                 0.31

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
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
    Duration: 696s 
    Code: 1766154959
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.19.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:440494
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766154959
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:440578
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766154959
MonetDB-BHT-8-2-2 uses docker image monetdb/monetdb:Dec2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:440578
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766154959

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-2-2
TPC-DS Q39a+b              False               True               True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-2-2
TPC-DS Q1                  44.99              42.25              42.66
TPC-DS Q2                 240.88             115.08             117.05
TPC-DS Q3                  21.76              18.28              24.32
TPC-DS Q4                1237.50            1289.42            1240.63
TPC-DS Q5                 105.42              85.66              82.75
TPC-DS Q6                  99.42              73.21              73.35
TPC-DS Q7                  52.30              47.11              54.57
TPC-DS Q8                  39.16              48.23              42.54
TPC-DS Q9                  63.81              53.28              55.75
TPC-DS Q10                 34.57              28.32              33.26
TPC-DS Q11                603.49             571.32             608.82
TPC-DS Q12                 19.34              16.85              18.08
TPC-DS Q13                 58.06              49.98              52.01
TPC-DS Q14a+b            2616.83            2552.61            2397.98
TPC-DS Q15                 23.33              23.44              19.74
TPC-DS Q16                 36.46              32.02              35.75
TPC-DS Q17                136.48             111.97             106.42
TPC-DS Q18                135.37              60.40              50.95
TPC-DS Q19                 40.18              37.56              37.75
TPC-DS Q20                 24.77              22.35              27.34
TPC-DS Q21                 72.10             104.54              63.88
TPC-DS Q22               1091.80            1015.77             989.57
TPC-DS Q23a+b            2073.21            1992.07            2037.60
TPC-DS Q24a+b             186.89             184.56             184.66
TPC-DS Q25                118.89             105.12             141.37
TPC-DS Q26                 29.83              19.89              19.81
TPC-DS Q27                152.67              99.19             107.49
TPC-DS Q28                 65.59              64.78              64.83
TPC-DS Q29                116.84             104.56             114.36
TPC-DS Q30                 24.84              16.96              18.65
TPC-DS Q31                172.92             133.64             143.18
TPC-DS Q32                 19.88              16.38              16.63
TPC-DS Q33                 21.79              20.03              23.91
TPC-DS Q34                 27.71              29.23              33.13
TPC-DS Q35                 88.00              69.42              75.00
TPC-DS Q36                 79.75              64.97              67.85
TPC-DS Q37                 80.23              42.27              44.79
TPC-DS Q38                218.42             190.04             202.21
TPC-DS Q39a+b            1407.00            1274.54            1298.48
TPC-DS Q40                 79.96             103.86             103.93
TPC-DS Q41                  5.98               6.43               8.14
TPC-DS Q42                 17.33              19.16              18.45
TPC-DS Q43                 41.82              45.58              44.36
TPC-DS Q44                 71.70              68.91              65.34
TPC-DS Q45                 13.72              13.18              13.14
TPC-DS Q46                 43.88              41.46              35.59
TPC-DS Q47                191.85             200.64             199.09
TPC-DS Q48                 40.37              38.15              44.53
TPC-DS Q49                102.54              92.89              82.19
TPC-DS Q50                103.14              97.73              95.01
TPC-DS Q51                480.50             439.12             514.34
TPC-DS Q52                 24.19              19.65              18.01
TPC-DS Q53                 25.77              23.81              24.00
TPC-DS Q54                 25.01              25.45              27.49
TPC-DS Q55                 14.07              14.89              14.44
TPC-DS Q56                 31.81              22.49              21.37
TPC-DS Q57                 94.44              94.97              92.47
TPC-DS Q58                 57.89              43.68              44.32
TPC-DS Q59                107.87             102.73              97.85
TPC-DS Q60                 23.35              22.36              22.99
TPC-DS Q61                 32.13              33.65              35.87
TPC-DS Q62                 23.77              23.36              22.97
TPC-DS Q63                 24.65              22.79              22.98
TPC-DS Q64                385.47             241.45             239.47
TPC-DS Q65                 98.62              86.10              89.73
TPC-DS Q66                 94.84             103.78             104.55
TPC-DS Q67                424.79             450.09             442.12
TPC-DS Q68                 44.19              38.84              37.14
TPC-DS Q69                 34.87              31.00              31.74
TPC-DS Q70                111.56              86.33              89.01
TPC-DS Q71                 30.51              29.61              29.14
TPC-DS Q72                171.85             147.64             163.48
TPC-DS Q73                 23.75              21.85              21.96
TPC-DS Q74                190.59             176.71             174.96
TPC-DS Q75                540.61             486.87             530.24
TPC-DS Q76                 49.83              54.69              47.39
TPC-DS Q77                 79.06              54.41              50.78
TPC-DS Q78                834.20             814.23             805.08
TPC-DS Q79                 42.70              42.30              41.20
TPC-DS Q80                455.17             407.86             455.30
TPC-DS Q81                 27.86              26.48              27.02
TPC-DS Q82                170.12              67.29              65.51
TPC-DS Q83                 14.46              12.73              13.10
TPC-DS Q84                 48.22              16.09              14.34
TPC-DS Q85                 78.01              82.79             102.52
TPC-DS Q86                 26.43              27.68              26.12
TPC-DS Q87                242.02             240.27             250.39
TPC-DS Q88                 68.97              67.56              80.41
TPC-DS Q89                 34.80              35.86              35.54
TPC-DS Q90                 12.44               9.28              12.73
TPC-DS Q91                 22.35              20.91              21.84
TPC-DS Q92                 10.71              12.27              11.33
TPC-DS Q93                 87.45              86.86              96.61
TPC-DS Q94                 15.83              16.26              16.08
TPC-DS Q95                246.72             174.33             181.29
TPC-DS Q96                 11.51              12.57              10.77
TPC-DS Q97                223.69             205.75             226.46
TPC-DS Q98                 37.36              38.82              36.67
TPC-DS Q99                 63.07              52.63              51.39

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          112.0        20.0      304.0     446.0
MonetDB-BHT-8-2-1           1.0          112.0        20.0      304.0     446.0
MonetDB-BHT-8-2-2           1.0          112.0        20.0      304.0     446.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.08
MonetDB-BHT-8-2-1           0.07
MonetDB-BHT-8-2-2           0.07

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           50573.62
MonetDB-BHT-8-2-1           57018.33
MonetDB-BHT-8-2-2           55951.94

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MonetDB-BHT-8-1 1.0 1              1                 29      1  1.0         12289.66
MonetDB-BHT-8-2 1.0 1              2                 29      2  1.0         24579.31

### Workflow
                         orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  1.0     8               1           1       1766155443     1766155472
MonetDB-BHT-8-2-1  MonetDB-BHT-8-2  1.0     8               1           2       1766155568     1766155596
MonetDB-BHT-8-2-2  MonetDB-BHT-8-2  1.0     8               1           2       1766155567     1766155594

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
    Duration: 1027s 
    Code: 1766250237
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.19.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:435027
    volume_size:50G
    volume_used:5.1G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766250237
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:435027
    volume_size:50G
    volume_used:5.5G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766250237

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q39a+b                False                 True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q1                    62.92               589.42
TPC-DS Q2                   421.94              1354.76
TPC-DS Q3                    44.48              1054.97
TPC-DS Q4                  1674.40              5793.75
TPC-DS Q5                   148.79              2152.54
TPC-DS Q6                   148.01               572.69
TPC-DS Q7                    90.37              2309.16
TPC-DS Q8                    82.45               827.19
TPC-DS Q9                    94.30              1001.77
TPC-DS Q10                   87.25              7759.25
TPC-DS Q11                  777.88               955.92
TPC-DS Q12                   29.80               193.31
TPC-DS Q13                   83.99               482.19
TPC-DS Q14a+b              2933.48              6312.00
TPC-DS Q15                   26.47                61.42
TPC-DS Q16                   42.52              1330.05
TPC-DS Q17                  153.11               391.04
TPC-DS Q18                  259.77               245.34
TPC-DS Q19                   39.07               161.04
TPC-DS Q20                   25.43                32.28
TPC-DS Q21                  100.46              3097.32
TPC-DS Q22                 1079.34              1369.04
TPC-DS Q23a+b              2846.00              4908.12
TPC-DS Q24a+b               269.53               518.92
TPC-DS Q25                  109.60                98.72
TPC-DS Q26                   26.68                31.09
TPC-DS Q27                  168.26               220.81
TPC-DS Q28                   66.40                73.69
TPC-DS Q29                   95.92               108.97
TPC-DS Q30                   16.01                82.54
TPC-DS Q31                  176.58               165.04
TPC-DS Q32                   15.90                25.52
TPC-DS Q33                   22.30                81.45
TPC-DS Q34                   36.92                97.77
TPC-DS Q35                   83.79                99.89
TPC-DS Q36                   75.03                77.75
TPC-DS Q37                  264.05                73.60
TPC-DS Q38                  189.76               215.09
TPC-DS Q39a+b              1423.95              1818.78
TPC-DS Q40                   76.39               183.27
TPC-DS Q41                    6.39                11.11
TPC-DS Q42                   18.37                40.48
TPC-DS Q43                   62.93               130.35
TPC-DS Q44                   46.28               225.17
TPC-DS Q45                   33.26                98.15
TPC-DS Q46                  374.38               180.58
TPC-DS Q47                 1751.25               799.71
TPC-DS Q48                  315.75                57.88
TPC-DS Q49                  418.79               812.04
TPC-DS Q50                  466.78               409.41
TPC-DS Q51                 2782.51               602.11
TPC-DS Q52                   40.96                30.53
TPC-DS Q53                   40.69                41.51
TPC-DS Q54                   34.84                51.32
TPC-DS Q55                   22.23                24.24
TPC-DS Q56                   34.39                56.86
TPC-DS Q57                   85.06               152.06
TPC-DS Q58                   56.89                54.07
TPC-DS Q59                   99.58               111.86
TPC-DS Q60                   32.32                22.86
TPC-DS Q61                   64.36               123.90
TPC-DS Q62                  104.84                44.39
TPC-DS Q63                   58.53                33.74
TPC-DS Q64                 1387.80               730.66
TPC-DS Q65                 1853.18               126.21
TPC-DS Q66                   97.08               121.43
TPC-DS Q67                  516.20               459.42
TPC-DS Q68                   49.08                45.91
TPC-DS Q69                   35.08                48.39
TPC-DS Q70                  107.51               357.02
TPC-DS Q71                   30.31                41.18
TPC-DS Q72                  224.75              1047.58
TPC-DS Q73                   23.92                24.69
TPC-DS Q74                  212.43               196.79
TPC-DS Q75                  506.58               538.51
TPC-DS Q76                   88.98               957.15
TPC-DS Q77                   84.29                90.77
TPC-DS Q78                  824.74               905.09
TPC-DS Q79                   49.12                42.74
TPC-DS Q80                  500.16               436.55
TPC-DS Q81                   30.50               205.93
TPC-DS Q82                  626.41               193.04
TPC-DS Q83                   27.73                21.21
TPC-DS Q84                   72.84                83.97
TPC-DS Q85                   89.42               117.41
TPC-DS Q86                   27.78                27.25
TPC-DS Q87                  246.27               256.74
TPC-DS Q88                   88.29               134.03
TPC-DS Q89                   46.52                36.17
TPC-DS Q90                   16.86                12.76
TPC-DS Q91                   30.55               101.00
TPC-DS Q92                   11.78                11.06
TPC-DS Q93                  105.03               125.76
TPC-DS Q94                   20.07                36.88
TPC-DS Q95                  249.58               285.32
TPC-DS Q96                   14.46                10.11
TPC-DS Q97                  230.77               292.52
TPC-DS Q98                   45.55                38.35
TPC-DS Q99                   70.96                58.93

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0          107.0        11.0      332.0     458.0
MonetDB-BHT-8-2-1-1           1.0          107.0        11.0      332.0     458.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.11
MonetDB-BHT-8-2-1-1           0.18

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           34992.41
MonetDB-BHT-8-2-1-1           20892.23

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                 time [s]  count   SF  Throughput@Size
DBMS              SF  num_experiment num_client                                       
MonetDB-BHT-8-1-1 1.0 1              1                 43      1  1.0          8288.37
MonetDB-BHT-8-2-1 1.0 2              1                135      1  1.0          2640.00

### Workflow
                             orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-1  1.0     8               1           1       1766250770     1766250813
MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-1  1.0     8               2           1       1766251077     1766251212

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
  -rr 64Gi -lr 64Gi \
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
    Duration: 1026s 
    Code: 1766251365
    We compute for all columns: Minimum, maximum, average, count, count distinct, count NULL and non NULL entries and coefficient of variation.
    This experiment compares imported TPC-DS data sets in different DBMS.
    TPC-DS (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.19.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
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
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:435027
    volume_size:50G
    volume_used:40G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766251365
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:435027
    volume_size:50G
    volume_used:40G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766251365

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                                    MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1
statistics_tab about call_center.cc_call_center_sk - all                            50.86              29.17
statistics_tab about call_center.cc_call_center_id - all                            74.08               9.10
statistics_tab about call_center.cc_rec_start_date - all                            18.55               7.25
statistics_tab about call_center.cc_rec_end_date - all                              16.52               9.28
statistics_tab about call_center.cc_closed_date_sk - all                            16.22               4.57
statistics_tab about call_center.cc_open_date_sk - all                              50.42               4.31
statistics_tab about call_center.cc_name - all                                      15.73               7.43
statistics_tab about call_center.cc_class - all                                     27.02               6.61
statistics_tab about call_center.cc_employees - all                                  5.22               4.44
statistics_tab about call_center.cc_sq_ft - all                                     15.47               4.19
statistics_tab about call_center.cc_hours - all                                     53.21               6.69
statistics_tab about call_center.cc_manager - all                                   42.84               6.29
statistics_tab about call_center.cc_mkt_id - all                                     6.21               4.15
statistics_tab about call_center.cc_mkt_class - all                                 41.68               7.92
statistics_tab about call_center.cc_mkt_desc - all                                  38.31               7.75
statistics_tab about call_center.cc_market_manager - all                             9.42               7.47
statistics_tab about call_center.cc_division - all                                  13.84               5.31
statistics_tab about call_center.cc_division_name - all                             14.13               6.86
statistics_tab about call_center.cc_company - all                                    5.22               5.31
statistics_tab about call_center.cc_company_name - all                              17.57               7.22
statistics_tab about call_center.cc_street_number - all                             66.24               6.51
statistics_tab about call_center.cc_street_name - all                              115.94               6.20
statistics_tab about call_center.cc_street_type - all                               18.91               6.73
statistics_tab about call_center.cc_suite_number - all                              19.73               6.37
statistics_tab about call_center.cc_city - all                                      26.73               6.38
statistics_tab about call_center.cc_county - all                                    21.41               5.88
statistics_tab about call_center.cc_state - all                                     31.05               6.44
statistics_tab about call_center.cc_zip - all                                       20.05               5.93
statistics_tab about call_center.cc_country - all                                   25.92               5.63
statistics_tab about call_center.cc_gmt_offset - all                               118.37               3.88
statistics_tab about call_center.cc_tax_percentage - all                            19.98               3.98
statistics_tab about catalog_page.cp_catalog_page_sk - all                           6.18               4.88
statistics_tab about catalog_page.cp_catalog_page_id - all                          22.96               8.26
statistics_tab about catalog_page.cp_start_date_sk - all                             6.35               5.63
statistics_tab about catalog_page.cp_end_date_sk - all                               6.24               5.21
statistics_tab about catalog_page.cp_department - all                               38.02               7.09
statistics_tab about catalog_page.cp_catalog_number - all                           28.83               4.59
statistics_tab about catalog_page.cp_catalog_page_number - all                      32.99               4.26
statistics_tab about catalog_page.cp_description - all                              39.69              13.64
statistics_tab about catalog_page.cp_type - all                                     20.54               6.78
statistics_tab about catalog_returns.cr_returned_date_sk - all                     179.86              73.11
statistics_tab about catalog_returns.cr_returned_time_sk - all                     160.60             119.07
statistics_tab about catalog_returns.cr_item_sk - all                              134.35             119.31
statistics_tab about catalog_returns.cr_refunded_customer_sk - all                 175.47             134.57
statistics_tab about catalog_returns.cr_refunded_cdemo_sk - all                    400.32             195.61
statistics_tab about catalog_returns.cr_refunded_hdemo_sk - all                    168.20              77.37
statistics_tab about catalog_returns.cr_refunded_addr_sk - all                     196.34             231.66
statistics_tab about catalog_returns.cr_returning_customer_sk - all                197.96             147.43
statistics_tab about catalog_returns.cr_returning_cdemo_sk - all                   323.37             393.88
statistics_tab about catalog_returns.cr_returning_hdemo_sk - all                   161.14              73.77
statistics_tab about catalog_returns.cr_returning_addr_sk - all                    208.87             110.73
statistics_tab about catalog_returns.cr_call_center_sk - all                       127.38              80.21
statistics_tab about catalog_returns.cr_catalog_page_sk - all                      124.55              58.77
statistics_tab about catalog_returns.cr_ship_mode_sk - all                         129.60              69.69
statistics_tab about catalog_returns.cr_warehouse_sk - all                         134.86              72.13
statistics_tab about catalog_returns.cr_reason_sk - all                            127.02              83.55
statistics_tab about catalog_returns.cr_order_number - all                         233.78              94.98
statistics_tab about catalog_returns.cr_return_quantity - all                      422.16              66.66
statistics_tab about catalog_returns.cr_return_amount - all                        173.27             110.57
statistics_tab about catalog_returns.cr_return_tax - all                           142.70              93.31
statistics_tab about catalog_returns.cr_return_amt_inc_tax - all                   167.67             135.21
statistics_tab about catalog_returns.cr_fee - all                                  130.63              60.72
statistics_tab about catalog_returns.cr_return_ship_cost - all                     200.31             163.80
statistics_tab about catalog_returns.cr_refunded_cash - all                        185.59             113.95
statistics_tab about catalog_returns.cr_reversed_charge - all                      108.75              85.15
statistics_tab about catalog_returns.cr_store_credit - all                         256.71             202.10
statistics_tab about catalog_returns.cr_net_loss - all                             207.86             117.44
statistics_tab about catalog_sales.cs_sold_date_sk - all                          1250.85             733.78
statistics_tab about catalog_sales.cs_sold_time_sk - all                          1396.62            1051.67
statistics_tab about catalog_sales.cs_ship_date_sk - all                          1345.30             756.81
statistics_tab about catalog_sales.cs_bill_customer_sk - all                      1654.81            1027.67
statistics_tab about catalog_sales.cs_bill_cdemo_sk - all                         1643.08            1033.49
statistics_tab about catalog_sales.cs_bill_hdemo_sk - all                         1407.68             670.44
statistics_tab about catalog_sales.cs_bill_addr_sk - all                          1992.25             973.86
statistics_tab about catalog_sales.cs_ship_customer_sk - all                      1502.68            1135.70
statistics_tab about catalog_sales.cs_ship_cdemo_sk - all                         1510.57            1022.55
statistics_tab about catalog_sales.cs_ship_hdemo_sk - all                         1476.57             654.33
statistics_tab about catalog_sales.cs_ship_addr_sk - all                          1662.86            1081.44
statistics_tab about catalog_sales.cs_call_center_sk - all                        1452.93             674.22
statistics_tab about catalog_sales.cs_catalog_page_sk - all                       1586.02             717.21
statistics_tab about catalog_sales.cs_ship_mode_sk - all                          1364.97             808.82
statistics_tab about catalog_sales.cs_warehouse_sk - all                          1684.94             779.95
statistics_tab about catalog_sales.cs_item_sk - all                               1347.51             756.84
statistics_tab about catalog_sales.cs_promo_sk - all                              1563.38             691.62
statistics_tab about catalog_sales.cs_order_number - all                          1425.81             783.13
statistics_tab about catalog_sales.cs_quantity - all                              1484.31             658.49
statistics_tab about catalog_sales.cs_wholesale_cost - all                        1560.92             643.05
statistics_tab about catalog_sales.cs_list_price - all                            1730.93             683.90
statistics_tab about catalog_sales.cs_sales_price - all                           1301.37             669.20
statistics_tab about catalog_sales.cs_ext_discount_amt - all                      2409.07            1657.48
statistics_tab about catalog_sales.cs_ext_sales_price - all                       2531.98            1724.70
statistics_tab about catalog_sales.cs_ext_wholesale_cost - all                    2427.02            1441.84
statistics_tab about catalog_sales.cs_ext_list_price - all                        3061.97            1985.99
statistics_tab about catalog_sales.cs_ext_tax - all                               1717.03            1192.01
statistics_tab about catalog_sales.cs_coupon_amt - all                            1621.63            4571.67
statistics_tab about catalog_sales.cs_ext_ship_cost - all                         2458.36            7063.84
statistics_tab about catalog_sales.cs_net_paid - all                              2376.78            3254.91
statistics_tab about catalog_sales.cs_net_paid_inc_tax - all                      2683.10            3675.46
statistics_tab about catalog_sales.cs_net_paid_inc_ship - all                     2860.43            3309.64
statistics_tab about catalog_sales.cs_net_paid_inc_ship_tax - all                 2474.84            2471.54
statistics_tab about catalog_sales.cs_net_profit - all                            3899.14            2768.29
statistics_tab about customer.c_customer_sk - all                                  151.71              45.62
statistics_tab about customer.c_customer_id - all                                  669.24             289.47
statistics_tab about customer.c_current_cdemo_sk - all                             258.39              61.22
statistics_tab about customer.c_current_hdemo_sk - all                              85.92              49.41
statistics_tab about customer.c_current_addr_sk - all                              336.59              31.46
statistics_tab about customer.c_first_shipto_date_sk - all                         185.01              82.31
statistics_tab about customer.c_first_sales_date_sk - all                          208.99              31.60
statistics_tab about customer.c_salutation - all                                   137.15              14.99
statistics_tab about customer.c_first_name - all                                   307.47              68.86
statistics_tab about customer.c_last_name - all                                    201.95             127.44
statistics_tab about customer.c_preferred_cust_flag - all                           68.53              18.60
statistics_tab about customer.c_birth_day - all                                    103.69              36.81
statistics_tab about customer.c_birth_month - all                                   91.21              40.20
statistics_tab about customer.c_birth_year - all                                    93.60              46.42
statistics_tab about customer.c_birth_country - all                                 65.22              12.48
statistics_tab about customer.c_login - all                                         29.36              11.52
statistics_tab about customer.c_email_address - all                                425.52             407.68
statistics_tab about customer.c_last_review_date - all                             237.03              16.52
statistics_tab about customer_address.ca_address_sk - all                          231.24              13.18
statistics_tab about customer_address.ca_address_id - all                          757.34             155.51
statistics_tab about customer_address.ca_street_number - all                        82.78              14.70
statistics_tab about customer_address.ca_street_name - all                         288.19              49.54
statistics_tab about customer_address.ca_street_type - all                         187.91              12.37
statistics_tab about customer_address.ca_suite_number - all                        256.90              20.09
statistics_tab about customer_address.ca_city - all                                162.78              13.39
statistics_tab about customer_address.ca_county - all                              282.11              13.21
statistics_tab about customer_address.ca_state - all                                78.46              13.05
statistics_tab about customer_address.ca_zip - all                                 176.61              62.44
statistics_tab about customer_address.ca_country - all                             100.76              11.47
statistics_tab about customer_address.ca_gmt_offset - all                           93.17              17.51
statistics_tab about customer_address.ca_location_type - all                       223.96              12.16
statistics_tab about customer_demographics.cd_demo_sk - all                        761.10             185.87
statistics_tab about customer_demographics.cd_gender - all                         649.18              22.91
statistics_tab about customer_demographics.cd_marital_status - all                 155.53              26.12
statistics_tab about customer_demographics.cd_education_status - all                83.64              29.29
statistics_tab about customer_demographics.cd_purchase_estimate - all              237.58             101.29
statistics_tab about customer_demographics.cd_credit_rating - all                  136.06              22.36
statistics_tab about customer_demographics.cd_dep_count - all                      258.65             120.23
statistics_tab about customer_demographics.cd_dep_employed_count - all             184.26              95.10
statistics_tab about customer_demographics.cd_dep_college_count - all              197.33              89.92
statistics_tab about date_dim.d_date_sk - all                                       31.59               7.38
statistics_tab about date_dim.d_date_id - all                                      164.22              29.75
statistics_tab about date_dim.d_date - all                                          44.08              11.57
statistics_tab about date_dim.d_month_seq - all                                     17.58               5.73
statistics_tab about date_dim.d_week_seq - all                                      64.94               5.54
statistics_tab about date_dim.d_quarter_seq - all                                   33.71               6.68
statistics_tab about date_dim.d_year - all                                          50.68               6.36
statistics_tab about date_dim.d_dow - all                                           33.52               6.08
statistics_tab about date_dim.d_moy - all                                           30.25               5.46
statistics_tab about date_dim.d_dom - all                                           29.28               7.33
statistics_tab about date_dim.d_qoy - all                                           41.70               5.49
statistics_tab about date_dim.d_fy_year - all                                       47.33               6.26
statistics_tab about date_dim.d_fy_quarter_seq - all                                16.64               7.11
statistics_tab about date_dim.d_fy_week_seq - all                                   67.05               5.78
statistics_tab about date_dim.d_day_name - all                                     160.19               6.74
statistics_tab about date_dim.d_quarter_name - all                                  93.18               6.67
statistics_tab about date_dim.d_holiday - all                                       44.83               8.03
statistics_tab about date_dim.d_weekend - all                                      217.83               7.66
statistics_tab about date_dim.d_following_holiday - all                            161.51               8.32
statistics_tab about date_dim.d_first_dom - all                                     47.28               7.58
statistics_tab about date_dim.d_last_dom - all                                      29.42               7.86
statistics_tab about date_dim.d_same_day_ly - all                                   55.53               7.46
statistics_tab about date_dim.d_same_day_lq - all                                   62.93               8.95
statistics_tab about date_dim.d_current_day - all                                   46.02               8.03
statistics_tab about date_dim.d_current_week - all                                  52.11               9.13
statistics_tab about date_dim.d_current_month - all                                 47.27               8.02
statistics_tab about date_dim.d_current_quarter - all                               98.85               7.12
statistics_tab about date_dim.d_current_year - all                                 120.26               7.61
statistics_tab about dbgen_version.dv_version - all                                 82.95               6.09
statistics_tab about dbgen_version.dv_create_date - all                             39.79               6.78
statistics_tab about dbgen_version.dv_create_time - all                             35.94               5.76
statistics_tab about dbgen_version.dv_cmdline_args - all                            29.44               6.36
statistics_tab about household_demographics.hd_demo_sk - all                        23.81               4.40
statistics_tab about household_demographics.hd_income_band_sk - all                 95.94               4.85
statistics_tab about household_demographics.hd_buy_potential - all                  44.90               7.81
statistics_tab about household_demographics.hd_dep_count - all                     134.99               4.85
statistics_tab about household_demographics.hd_vehicle_count - all                  25.50               3.89
statistics_tab about income_band.ib_income_band_sk - all                            40.13               3.55
statistics_tab about income_band.ib_lower_bound - all                               19.96               4.46
statistics_tab about income_band.ib_upper_bound - all                               44.03               4.72
statistics_tab about inventory.inv_date_sk - all                                 16644.60            9044.67
statistics_tab about inventory.inv_item_sk - all                                 16005.35            7518.33
statistics_tab about inventory.inv_warehouse_sk - all                            14788.76            7000.83
statistics_tab about inventory.inv_quantity_on_hand - all                        17227.92            8625.47
statistics_tab about item.i_item_sk - all                                           63.09              10.30
statistics_tab about item.i_item_id - all                                           69.39              33.45
statistics_tab about item.i_rec_start_date - all                                    40.76               9.89
statistics_tab about item.i_rec_end_date - all                                      38.72               9.16
statistics_tab about item.i_item_desc - all                                        281.36              81.06
statistics_tab about item.i_current_price - all                                     38.22               9.21
statistics_tab about item.i_wholesale_cost - all                                    36.40               9.13
statistics_tab about item.i_brand_id - all                                          71.56               9.81
statistics_tab about item.i_brand - all                                             47.52               9.56
statistics_tab about item.i_class_id - all                                          69.50               7.52
statistics_tab about item.i_class - all                                             54.74               8.19
statistics_tab about item.i_category_id - all                                       37.49               8.43
statistics_tab about item.i_category - all                                          27.08               9.27
statistics_tab about item.i_manufact_id - all                                       37.69               9.29
statistics_tab about item.i_manufact - all                                          66.93              10.67
statistics_tab about item.i_size - all                                              29.74               9.99
statistics_tab about item.i_formulation - all                                      112.99              44.10
statistics_tab about item.i_color - all                                             73.80               8.56
statistics_tab about item.i_units - all                                            341.78               8.03
statistics_tab about item.i_container - all                                         40.88               7.28
statistics_tab about item.i_manager_id - all                                        61.58              10.67
statistics_tab about item.i_product_name - all                                     143.27              43.89
statistics_tab about promotion.p_promo_sk - all                                     37.77               3.55
statistics_tab about promotion.p_promo_id - all                                     82.01               7.06
statistics_tab about promotion.p_start_date_sk - all                                18.26               3.69
statistics_tab about promotion.p_end_date_sk - all                                 100.88               3.48
statistics_tab about promotion.p_item_sk - all                                      20.53               3.86
statistics_tab about promotion.p_cost - all                                          6.67               3.84
statistics_tab about promotion.p_response_target - all                              20.17               3.97
statistics_tab about promotion.p_promo_name - all                                   26.42               5.94
statistics_tab about promotion.p_channel_dmail - all                                91.67               6.44
statistics_tab about promotion.p_channel_email - all                                81.41              17.61
statistics_tab about promotion.p_channel_catalog - all                              43.39               7.28
statistics_tab about promotion.p_channel_tv - all                                   22.08               6.53
statistics_tab about promotion.p_channel_radio - all                                67.59               5.87
statistics_tab about promotion.p_channel_press - all                                19.06               5.93
statistics_tab about promotion.p_channel_event - all                                93.42               6.05
statistics_tab about promotion.p_channel_demo - all                                 17.77               5.89
statistics_tab about promotion.p_channel_details - all                              33.75               6.60
statistics_tab about promotion.p_purpose - all                                      39.27               6.95
statistics_tab about promotion.p_discount_active - all                              75.77              11.49
statistics_tab about reason.r_reason_sk - all                                      114.47               3.81
statistics_tab about reason.r_reason_id - all                                       52.46               6.24
statistics_tab about reason.r_reason_desc - all                                     41.28               5.65
statistics_tab about ship_mode.sm_ship_mode_sk - all                                18.45               3.72
statistics_tab about ship_mode.sm_ship_mode_id - all                                23.97               7.08
statistics_tab about ship_mode.sm_type - all                                        50.66               6.37
statistics_tab about ship_mode.sm_code - all                                        47.75               6.68
statistics_tab about ship_mode.sm_carrier - all                                     28.36               7.25
statistics_tab about ship_mode.sm_contract - all                                    70.83               6.24
statistics_tab about store.s_store_sk - all                                          5.29               4.07
statistics_tab about store.s_store_id - all                                         37.88               6.44
statistics_tab about store.s_rec_start_date - all                                   15.96               5.90
statistics_tab about store.s_rec_end_date - all                                     16.27               6.61
statistics_tab about store.s_closed_date_sk - all                                    5.26               4.58
statistics_tab about store.s_store_name - all                                       22.69              10.14
statistics_tab about store.s_number_employees - all                                 42.87               3.91
statistics_tab about store.s_floor_space - all                                      15.24               4.24
statistics_tab about store.s_hours - all                                            24.22               7.36
statistics_tab about store.s_manager - all                                          31.87               6.79
statistics_tab about store.s_market_id - all                                        11.29               4.42
statistics_tab about store.s_geography_class - all                                  15.85               6.33
statistics_tab about store.s_market_desc - all                                      22.38               7.06
statistics_tab about store.s_market_manager - all                                   40.52               6.11
statistics_tab about store.s_division_id - all                                      48.47               3.36
statistics_tab about store.s_division_name - all                                    11.05               6.40
statistics_tab about store.s_company_id - all                                        5.67               3.97
statistics_tab about store.s_company_name - all                                     72.97               6.00
statistics_tab about store.s_street_number - all                                    21.28               7.36
statistics_tab about store.s_street_name - all                                      16.99               7.09
statistics_tab about store.s_street_type - all                                     150.59               6.45
statistics_tab about store.s_suite_number - all                                     49.03               7.03
statistics_tab about store.s_city - all                                             23.89               6.31
statistics_tab about store.s_county - all                                           95.61               6.93
statistics_tab about store.s_state - all                                            61.88               6.41
statistics_tab about store.s_zip - all                                               9.49               6.51
statistics_tab about store.s_country - all                                          27.48               5.92
statistics_tab about store.s_gmt_offset - all                                        5.06               3.99
statistics_tab about store.s_tax_precentage - all                                    5.29               4.16
statistics_tab about store_returns.sr_returned_date_sk - all                       301.83             141.37
statistics_tab about store_returns.sr_return_time_sk - all                         468.61             163.64
statistics_tab about store_returns.sr_item_sk - all                                320.65             203.34
statistics_tab about store_returns.sr_customer_sk - all                            399.56             310.99
statistics_tab about store_returns.sr_cdemo_sk - all                               580.19             636.71
statistics_tab about store_returns.sr_hdemo_sk - all                               288.52             167.22
statistics_tab about store_returns.sr_addr_sk - all                                350.60             226.75
statistics_tab about store_returns.sr_store_sk - all                               297.20             150.55
statistics_tab about store_returns.sr_reason_sk - all                              280.56             124.78
statistics_tab about store_returns.sr_ticket_number - all                          291.80             264.03
statistics_tab about store_returns.sr_return_quantity - all                        271.67             211.67
statistics_tab about store_returns.sr_return_amt - all                             416.30             235.05
statistics_tab about store_returns.sr_return_tax - all                             333.24             169.23
statistics_tab about store_returns.sr_return_amt_inc_tax - all                     511.10             350.01
statistics_tab about store_returns.sr_fee - all                                    304.32             137.39
statistics_tab about store_returns.sr_return_ship_cost - all                       412.61             271.94
statistics_tab about store_returns.sr_refunded_cash - all                          537.48             210.93
statistics_tab about store_returns.sr_reversed_charge - all                        426.90             173.32
statistics_tab about store_returns.sr_store_credit - all                           324.64             165.53
statistics_tab about store_returns.sr_net_loss - all                               304.59             222.30
statistics_tab about store_sales.ss_sold_date_sk - all                            2872.85            1303.93
statistics_tab about store_sales.ss_sold_time_sk - all                            4588.20            2748.49
statistics_tab about store_sales.ss_item_sk - all                                 2981.31            1397.33
statistics_tab about store_sales.ss_customer_sk - all                             3687.24            2142.08
statistics_tab about store_sales.ss_cdemo_sk - all                                3618.75            1964.85
statistics_tab about store_sales.ss_hdemo_sk - all                                2847.17            1260.32
statistics_tab about store_sales.ss_addr_sk - all                                 3464.90            1753.54
statistics_tab about store_sales.ss_store_sk - all                                2691.85            1335.31
statistics_tab about store_sales.ss_promo_sk - all                                2962.09            1467.99
statistics_tab about store_sales.ss_ticket_number - all                           2929.86            1350.53
statistics_tab about store_sales.ss_quantity - all                                2889.57            1354.46
statistics_tab about store_sales.ss_wholesale_cost - all                          3063.50            1622.44
statistics_tab about store_sales.ss_list_price - all                              3059.04            1376.33
statistics_tab about store_sales.ss_sales_price - all                             3345.88            1573.13
statistics_tab about store_sales.ss_ext_discount_amt - all                        3841.80            2474.25
statistics_tab about store_sales.ss_ext_sales_price - all                         5813.68            3359.76
statistics_tab about store_sales.ss_ext_wholesale_cost - all                      6147.53            3958.78
statistics_tab about store_sales.ss_ext_list_price - all                          6500.38            3588.84
statistics_tab about store_sales.ss_ext_tax - all                                 3477.69            1521.12
statistics_tab about store_sales.ss_coupon_amt - all                              3632.33            1813.39
statistics_tab about store_sales.ss_net_paid - all                                5950.79            2933.72
statistics_tab about store_sales.ss_net_paid_inc_tax - all                        4783.15            3182.09
statistics_tab about store_sales.ss_net_profit - all                              6655.40            6461.79
statistics_tab about time_dim.t_time_sk - all                                      153.82               6.74
statistics_tab about time_dim.t_time_id - all                                      116.33              48.13
statistics_tab about time_dim.t_time - all                                          25.58              16.20
statistics_tab about time_dim.t_hour - all                                           8.32              17.72
statistics_tab about time_dim.t_minute - all                                        31.29              41.36
statistics_tab about time_dim.t_second - all                                        12.66              10.84
statistics_tab about time_dim.t_am_pm - all                                        107.30              20.67
statistics_tab about time_dim.t_shift - all                                        105.55              16.50
statistics_tab about time_dim.t_sub_shift - all                                     69.11              14.86
statistics_tab about time_dim.t_meal_time - all                                     43.91              25.18
statistics_tab about warehouse.w_warehouse_sk - all                                 20.13               9.18
statistics_tab about warehouse.w_warehouse_id - all                                 38.45              35.83
statistics_tab about warehouse.w_warehouse_name - all                               32.90              32.48
statistics_tab about warehouse.w_warehouse_sq_ft - all                              22.66              42.05
statistics_tab about warehouse.w_street_number - all                                91.79              22.96
statistics_tab about warehouse.w_street_name - all                                  18.73              17.89
statistics_tab about warehouse.w_street_type - all                                  25.78              21.33
statistics_tab about warehouse.w_suite_number - all                                 26.17              26.76
statistics_tab about warehouse.w_city - all                                         37.76              28.23
statistics_tab about warehouse.w_county - all                                       36.76              20.90
statistics_tab about warehouse.w_state - all                                        33.83              19.37
statistics_tab about warehouse.w_zip - all                                           8.91              19.90
statistics_tab about warehouse.w_country - all                                       8.96              17.46
statistics_tab about warehouse.w_gmt_offset - all                                   39.94               8.16
statistics_tab about web_page.wp_web_page_sk - all                                  14.48               7.62
statistics_tab about web_page.wp_web_page_id - all                                 103.83              20.07
statistics_tab about web_page.wp_rec_start_date - all                               35.16              20.10
statistics_tab about web_page.wp_rec_end_date - all                                 20.82              43.75
statistics_tab about web_page.wp_creation_date_sk - all                            130.07               8.25
statistics_tab about web_page.wp_access_date_sk - all                                5.82              10.37
statistics_tab about web_page.wp_autogen_flag - all                                 39.97              15.91
statistics_tab about web_page.wp_customer_sk - all                                   7.54              15.75
statistics_tab about web_page.wp_url - all                                          24.44              42.38
statistics_tab about web_page.wp_type - all                                         21.00              34.58
statistics_tab about web_page.wp_char_count - all                                   22.76              10.68
statistics_tab about web_page.wp_link_count - all                                   27.32              12.32
statistics_tab about web_page.wp_image_count - all                                  17.45              10.42
statistics_tab about web_page.wp_max_ad_count - all                                 16.63               7.31
statistics_tab about web_returns.wr_returned_date_sk - all                         104.98             197.80
statistics_tab about web_returns.wr_returned_time_sk - all                          53.97             761.71
statistics_tab about web_returns.wr_item_sk - all                                  100.08             172.81
statistics_tab about web_returns.wr_refunded_customer_sk - all                     108.75             286.65
statistics_tab about web_returns.wr_refunded_cdemo_sk - all                        151.06             401.55
statistics_tab about web_returns.wr_refunded_hdemo_sk - all                         47.62              99.20
statistics_tab about web_returns.wr_refunded_addr_sk - all                         102.69             210.71
statistics_tab about web_returns.wr_returning_customer_sk - all                    140.53            1613.54
statistics_tab about web_returns.wr_returning_cdemo_sk - all                       193.18             289.64
statistics_tab about web_returns.wr_returning_hdemo_sk - all                        60.97              55.82
statistics_tab about web_returns.wr_returning_addr_sk - all                        101.46             493.88
statistics_tab about web_returns.wr_web_page_sk - all                              131.40              93.64
statistics_tab about web_returns.wr_reason_sk - all                                 86.12              98.17
statistics_tab about web_returns.wr_order_number - all                             103.52              56.22
statistics_tab about web_returns.wr_return_quantity - all                          167.41              74.28
statistics_tab about web_returns.wr_return_amt - all                               990.23             340.10
statistics_tab about web_returns.wr_return_tax - all                               301.35             209.99
statistics_tab about web_returns.wr_return_amt_inc_tax - all                       251.88             171.76
statistics_tab about web_returns.wr_fee - all                                      201.94              68.88
statistics_tab about web_returns.wr_return_ship_cost - all                         425.94             137.31
statistics_tab about web_returns.wr_refunded_cash - all                            691.92             255.51
statistics_tab about web_returns.wr_reversed_charge - all                          117.46             108.80
statistics_tab about web_returns.wr_account_credit - all                           119.77             283.39
statistics_tab about web_returns.wr_net_loss - all                                 150.44             107.82
statistics_tab about web_sales.ws_sold_date_sk - all                               870.13             682.99
statistics_tab about web_sales.ws_sold_time_sk - all                              1550.84             493.22
statistics_tab about web_sales.ws_ship_date_sk - all                               944.93             425.80
statistics_tab about web_sales.ws_item_sk - all                                   1263.39             678.09
statistics_tab about web_sales.ws_bill_customer_sk - all                          1231.59             537.62
statistics_tab about web_sales.ws_bill_cdemo_sk - all                             1739.71             650.60
statistics_tab about web_sales.ws_bill_hdemo_sk - all                             2098.77             598.09
statistics_tab about web_sales.ws_bill_addr_sk - all                              1299.60             526.05
statistics_tab about web_sales.ws_ship_customer_sk - all                          1355.70            1095.03
statistics_tab about web_sales.ws_ship_cdemo_sk - all                             1278.13             694.81
statistics_tab about web_sales.ws_ship_hdemo_sk - all                             1016.88             626.99
statistics_tab about web_sales.ws_ship_addr_sk - all                              1140.64             914.88
statistics_tab about web_sales.ws_web_page_sk - all                               1401.75             454.09
statistics_tab about web_sales.ws_web_site_sk - all                                877.34             548.07
statistics_tab about web_sales.ws_ship_mode_sk - all                              1200.61             576.12
statistics_tab about web_sales.ws_warehouse_sk - all                               916.10             422.92
statistics_tab about web_sales.ws_promo_sk - all                                   877.23             404.51
statistics_tab about web_sales.ws_order_number - all                               699.37             367.51
statistics_tab about web_sales.ws_quantity - all                                   825.34             437.68
statistics_tab about web_sales.ws_wholesale_cost - all                             918.43             395.83
statistics_tab about web_sales.ws_list_price - all                                1429.16             538.43
statistics_tab about web_sales.ws_sales_price - all                                821.51             417.84
statistics_tab about web_sales.ws_ext_discount_amt - all                          1604.58             952.62
statistics_tab about web_sales.ws_ext_sales_price - all                           1570.52            1097.33
statistics_tab about web_sales.ws_ext_wholesale_cost - all                        1936.56            2629.18
statistics_tab about web_sales.ws_ext_list_price - all                            2072.71            3010.45
statistics_tab about web_sales.ws_ext_tax - all                                   3424.75             626.84
statistics_tab about web_sales.ws_coupon_amt - all                                1187.25            1243.99
statistics_tab about web_sales.ws_ext_ship_cost - all                             2022.44            1165.85
statistics_tab about web_sales.ws_net_paid - all                                  1736.41            5093.56
statistics_tab about web_sales.ws_net_paid_inc_tax - all                          2356.72            1389.55
statistics_tab about web_sales.ws_net_paid_inc_ship - all                         1364.52             954.03
statistics_tab about web_sales.ws_net_paid_inc_ship_tax - all                     2097.88            1054.93
statistics_tab about web_sales.ws_net_profit - all                                2446.98            1203.30
statistics_tab about web_site.web_site_sk - all                                      5.52               4.24
statistics_tab about web_site.web_site_id - all                                     55.06               6.86
statistics_tab about web_site.web_rec_start_date - all                              25.52               6.03
statistics_tab about web_site.web_rec_end_date - all                                14.85               5.71
statistics_tab about web_site.web_name - all                                        92.48              10.42
statistics_tab about web_site.web_open_date_sk - all                                16.53               6.34
statistics_tab about web_site.web_close_date_sk - all                               16.87               9.09
statistics_tab about web_site.web_class - all                                       27.48               8.10
statistics_tab about web_site.web_manager - all                                     40.46               6.06
statistics_tab about web_site.web_mkt_id - all                                      17.91               2.81
statistics_tab about web_site.web_mkt_class - all                                    9.75               5.54
statistics_tab about web_site.web_mkt_desc - all                                    38.97               6.64
statistics_tab about web_site.web_market_manager - all                              10.60               6.27
statistics_tab about web_site.web_company_id - all                                  41.64               3.43
statistics_tab about web_site.web_company_name - all                                13.18               6.53
statistics_tab about web_site.web_street_number - all                               31.47               6.17
statistics_tab about web_site.web_street_name - all                                 17.30               7.44
statistics_tab about web_site.web_street_type - all                                 37.39               6.11
statistics_tab about web_site.web_suite_number - all                                44.15               6.05
statistics_tab about web_site.web_city - all                                        10.97               5.92
statistics_tab about web_site.web_county - all                                      17.01               6.26
statistics_tab about web_site.web_state - all                                       64.40               7.00
statistics_tab about web_site.web_zip - all                                         47.89               6.57
statistics_tab about web_site.web_country - all                                     28.98               6.03
statistics_tab about web_site.web_gmt_offset - all                                  19.06               4.05
statistics_tab about web_site.web_tax_percentage - all                              14.20               3.01

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           0.0          360.0         8.0     1177.0    1553.0
MonetDB-BHT-8-2-1           0.0          360.0         8.0     1177.0    1553.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.13
MonetDB-BHT-8-2-1           0.05

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1          276127.11
MonetDB-BHT-8-2-1          781590.35

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                time [s]  count    SF  Throughput@Size
DBMS            SF   num_experiment num_client                                        
MonetDB-BHT-8-1 10.0 1              1                350      1  10.0         44125.71
MonetDB-BHT-8-2 10.0 1              2                210      1  10.0         73542.86

### Workflow
                         orig_name    SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  10.0     8               1           1       1766251580     1766251930
MonetDB-BHT-8-2-1  MonetDB-BHT-8-2  10.0     8               1           2       1766252121     1766252331

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      436.64     1.65          1.81                11.53
MonetDB-BHT-8-2      476.76     2.60         10.37                14.02

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1        21.1     0.30          0.28                 0.28
MonetDB-BHT-8-2        21.1     0.29          0.31                 0.32

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
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
  -rr 256Gi -lr 256Gi \
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
    Duration: 13455s 
    Code: 1764348964
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 7200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.16.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
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
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:421721
    datadisk:315651
    volume_size:1000G
    volume_used:309G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764348964

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                2754.47
TPC-DS Q2               22800.43
TPC-DS Q3                1938.88
TPC-DS Q4              202685.95
TPC-DS Q5               32206.24
TPC-DS Q6               11647.25
TPC-DS Q7                2951.38
TPC-DS Q8                5624.54
TPC-DS Q9                5215.94
TPC-DS Q10               4636.40
TPC-DS Q11              80198.26
TPC-DS Q12                811.42
TPC-DS Q13               2883.80
TPC-DS Q14a+b          300217.02
TPC-DS Q15               1244.64
TPC-DS Q16               4185.35
TPC-DS Q17              53278.58
TPC-DS Q18              10278.59
TPC-DS Q19               2473.37
TPC-DS Q20               1231.04
TPC-DS Q21               2551.33
TPC-DS Q22              74645.20
TPC-DS Q23a+b         3198633.76
TPC-DS Q24a+b         1071831.37
TPC-DS Q25              35333.38
TPC-DS Q26               4481.13
TPC-DS Q27              42544.16
TPC-DS Q28               5484.10
TPC-DS Q29              22908.07
TPC-DS Q30               5246.11
TPC-DS Q31              31456.33
TPC-DS Q32               1548.44
TPC-DS Q33              10898.97
TPC-DS Q34               2727.10
TPC-DS Q35              26023.74
TPC-DS Q36              17205.19
TPC-DS Q37              31470.79
TPC-DS Q38              46617.65
TPC-DS Q39a+b           58032.77
TPC-DS Q40              18279.20
TPC-DS Q41                653.23
TPC-DS Q42               1858.54
TPC-DS Q43               1327.14
TPC-DS Q44             110119.10
TPC-DS Q45               1147.98
TPC-DS Q46               3480.13
TPC-DS Q47               6064.92
TPC-DS Q48               4407.22
TPC-DS Q49              26807.41
TPC-DS Q50               3230.66
TPC-DS Q51              34328.80
TPC-DS Q52               1848.04
TPC-DS Q53               1774.23
TPC-DS Q54               4600.29
TPC-DS Q55               1201.49
TPC-DS Q56               2112.08
TPC-DS Q57               1512.48
TPC-DS Q58               5266.74
TPC-DS Q59              12435.56
TPC-DS Q60               2312.90
TPC-DS Q61               2940.84
TPC-DS Q62               2791.62
TPC-DS Q63               1788.18
TPC-DS Q64              77781.13
TPC-DS Q65              26012.53
TPC-DS Q66               9415.78
TPC-DS Q67              80246.95
TPC-DS Q68               2330.18
TPC-DS Q69               1734.96
TPC-DS Q70              21182.03
TPC-DS Q71               5329.63
TPC-DS Q72              21211.32
TPC-DS Q73               2027.50
TPC-DS Q74              88103.12
TPC-DS Q75             108845.77
TPC-DS Q76              61635.63
TPC-DS Q77               9760.18
TPC-DS Q78             175194.73
TPC-DS Q79               6491.46
TPC-DS Q80             113201.11
TPC-DS Q81               1641.52
TPC-DS Q82              23417.73
TPC-DS Q83               1665.61
TPC-DS Q84                870.94
TPC-DS Q85               1592.40
TPC-DS Q86               3262.04
TPC-DS Q87              43520.90
TPC-DS Q88               5373.00
TPC-DS Q89               2339.37
TPC-DS Q90               1164.47
TPC-DS Q91                610.75
TPC-DS Q92               1670.50
TPC-DS Q93              22496.68
TPC-DS Q94               3441.55
TPC-DS Q95              16699.92
TPC-DS Q96               1867.98
TPC-DS Q97              44659.65
TPC-DS Q98               2405.56
TPC-DS Q99               3992.94

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0         1423.0        10.0     6504.0    7947.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           8.63

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           42144.68

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                 time [s]  count     SF  Throughput@Size
DBMS            SF    num_experiment num_client                                         
MonetDB-BHT-8-1 100.0 1              1               6746      1  100.0          5283.13

### Workflow
                         orig_name     SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  100.0     8               1           1       1764355587     1764362333

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     1148.99     1.14          0.03                 12.0

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    50482.51    46.07        250.93                256.0

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       65.83     0.26           0.4                 0.41

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
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
  -rr 256Gi -lr 256Gi \
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
    Duration: 34802s 
    Code: 1764362708
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 7200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.16.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
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
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:421721
    datadisk:322121
    volume_size:1000G
    volume_used:315G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764362708
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:421723
    datadisk:317014
    volume_size:1000G
    volume_used:310G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764362708
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:421724
    datadisk:317014
    volume_size:1000G
    volume_used:310G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764362708
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:421725
    datadisk:317014
    volume_size:1000G
    volume_used:310G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764362708

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q39a+b                 True                False                 True                 True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q1                 12001.22              3977.45             14159.88              4499.08
TPC-DS Q2                 42156.83             14415.25             51051.61             16386.14
TPC-DS Q3                 98469.62              2700.40            112315.76              2907.41
TPC-DS Q4                322185.28            184036.82            344662.45            199732.34
TPC-DS Q5                205194.77             25827.87            223425.60             23915.46
TPC-DS Q6                 12387.54             12766.28             10973.96             10164.85
TPC-DS Q7                 88888.04              2888.06             99442.09             10059.18
TPC-DS Q8                 33588.06              7744.76             34443.83              4538.67
TPC-DS Q9                  4259.45              3828.03              5406.04              4233.24
TPC-DS Q10               347635.79              2863.60            390974.89              3216.62
TPC-DS Q11                80179.93             81743.88             96366.30             86622.72
TPC-DS Q12                 1680.90               753.66              2328.92               916.28
TPC-DS Q13                 3238.57              2974.58              3426.90              3077.35
TPC-DS Q14a+b            342576.81            354371.53            328023.90            436556.76
TPC-DS Q15                 1722.34              2137.38              3337.28              2110.85
TPC-DS Q16                21527.96              2025.14             27724.19              2134.15
TPC-DS Q17                41042.47             37962.93             50567.04             60036.85
TPC-DS Q18                25308.91             11391.09             29919.26             13142.58
TPC-DS Q19                 2028.65              2739.78              3323.57              2625.70
TPC-DS Q20                 1302.46              1684.15              1701.01              1193.30
TPC-DS Q21                88169.15              3027.40            102371.69              2998.94
TPC-DS Q22               109668.42             99449.72            117784.10             83478.18
TPC-DS Q23a+b           3560207.86           3530487.14           2784528.05           4216243.65
TPC-DS Q24a+b           1704172.70           1645391.17           1980345.55           2044643.56
TPC-DS Q25                32292.04             32700.89             36272.44             32564.32
TPC-DS Q26                 3624.77              3266.54              3967.43              3538.09
TPC-DS Q27                42795.75             43742.62             44170.08             40710.51
TPC-DS Q28                 4723.47              4923.52              5431.19              5568.78
TPC-DS Q29                20792.53             14702.69             17513.41             17981.73
TPC-DS Q30                 3164.08              3446.47              5749.94              3915.27
TPC-DS Q31                35489.78             30711.09             31659.85             30791.29
TPC-DS Q32                 1498.80              1170.54              1342.25              1294.04
TPC-DS Q33                12383.22             11620.99             11442.59             11714.73
TPC-DS Q34                 3884.74              3527.34              5305.39              3273.89
TPC-DS Q35                11589.27              9437.75             13821.93             11700.27
TPC-DS Q36                20067.29             19537.39             21613.50             19477.88
TPC-DS Q37                26998.31             27597.66             29678.81             23784.42
TPC-DS Q38                62358.76             52326.80             61861.46             55202.37
TPC-DS Q39a+b             58713.40             54543.37             56621.94             55810.86
TPC-DS Q40                 8003.25              6612.42             10655.74              6611.11
TPC-DS Q41                 1682.43               601.28               964.62               721.87
TPC-DS Q42                 2247.36              2079.91              3858.08              2082.35
TPC-DS Q43                 1714.41              1369.48              2203.69              1397.57
TPC-DS Q44               113264.43            118240.77            119616.88            131007.56
TPC-DS Q45                 2226.81              1540.36              1898.67              2093.98
TPC-DS Q46                 8705.10              6039.25              5455.88              6952.88
TPC-DS Q47                11016.37              7367.71             14610.38             10844.10
TPC-DS Q48                 2916.11              2029.13              3704.09              2260.96
TPC-DS Q49                44602.78             24214.47             49309.31             22916.37
TPC-DS Q50                 3424.80              3686.05              4182.93              4827.19
TPC-DS Q51                41565.98             36859.58             38166.66             44038.79
TPC-DS Q52                 2228.38              2250.76              2384.00              2455.39
TPC-DS Q53                 2119.07              1654.85              2300.00              2331.90
TPC-DS Q54                 5696.70              4618.05              5321.35              4601.48
TPC-DS Q55                 1438.14               218.93              1483.23               218.79
TPC-DS Q56                 2442.64              2332.98              2889.77              2571.86
TPC-DS Q57                 1662.42              1528.92              2170.89              2111.57
TPC-DS Q58                 5785.08              5503.17              5617.24              6012.37
TPC-DS Q59                16101.45             11750.36             16047.87             15599.17
TPC-DS Q60                 2005.68              1684.04              3033.89              1916.34
TPC-DS Q61                 3384.08              2444.24              3085.37              2471.34
TPC-DS Q62                 3561.19              3211.39              3536.47              3554.86
TPC-DS Q63                 2166.37              1555.67              2265.98               779.82
TPC-DS Q64                52447.91             47505.10             53013.53             51595.66
TPC-DS Q65                33868.26             24085.37             29855.84             28959.95
TPC-DS Q66                12510.29             11556.16             13018.98             11117.41
TPC-DS Q67                97373.01            101092.95             85242.99             89722.62
TPC-DS Q68                 2614.41              2869.02              3009.53              2494.21
TPC-DS Q69                 5236.35              4821.23              4706.07              5925.50
TPC-DS Q70                25924.86             24603.08             27377.44             29730.98
TPC-DS Q71                 5201.13              5028.43              5772.71              7043.70
TPC-DS Q72                24061.77             20116.92             24508.32             24635.26
TPC-DS Q73                 2532.58              1356.61              2779.60              4084.36
TPC-DS Q74                44965.51             36070.46             28707.96             33148.83
TPC-DS Q75               125163.49            129358.41            113862.28            134708.36
TPC-DS Q76                76942.48             88719.12             80685.99             78265.37
TPC-DS Q77                11239.84             11554.86             11190.36             12161.69
TPC-DS Q78               199009.63            194646.13            187545.02            204997.42
TPC-DS Q79                10063.98              6096.18              7844.88              7370.29
TPC-DS Q80               109154.02            117114.37            100825.42            102568.43
TPC-DS Q81                 4422.02              3427.16              4283.13              2664.39
TPC-DS Q82                27358.33             31105.60             29352.16             27425.32
TPC-DS Q83                 1855.52              2162.24              1992.14              1754.73
TPC-DS Q84                 1116.21              1184.70              1682.04              1216.72
TPC-DS Q85                 1903.18              2064.08              2715.93              1643.89
TPC-DS Q86                 3559.16              3687.79              4123.14              3584.41
TPC-DS Q87                56229.70             50644.45             64397.42             55033.68
TPC-DS Q88                 5236.16              6208.88              6270.29              6257.61
TPC-DS Q89                 3162.36              3149.54              3707.42              3149.47
TPC-DS Q90                 1036.98              1238.40              1075.42              1041.07
TPC-DS Q91                  609.63               981.14               530.70               561.07
TPC-DS Q92                 2246.03              1855.40              2152.80              2327.10
TPC-DS Q93                31769.33             34631.79             44376.14             36255.86
TPC-DS Q94                 4293.85              5380.05              4632.94              3963.17
TPC-DS Q95                16763.14             18651.32             19928.13             19886.46
TPC-DS Q96                 1737.46              2163.46              2250.28              2081.64
TPC-DS Q97                59545.77             48263.43             51364.59             49274.26
TPC-DS Q98                 6230.33             14252.22              3071.11              3216.91
TPC-DS Q99                 4501.87              5664.47              4779.95              4191.70

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0         1423.0        10.0     6504.0    7947.0
MonetDB-BHT-8-1-2-1           1.0         1423.0        10.0     6504.0    7947.0
MonetDB-BHT-8-2-1-1           1.0         1423.0        10.0     6504.0    7947.0
MonetDB-BHT-8-2-2-1           1.0         1423.0        10.0     6504.0    7947.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1          12.44
MonetDB-BHT-8-1-2-1           8.88
MonetDB-BHT-8-2-1-1          13.37
MonetDB-BHT-8-2-2-1           9.24

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           29197.13
MonetDB-BHT-8-1-2-1           40873.10
MonetDB-BHT-8-2-1-1           27206.42
MonetDB-BHT-8-2-2-1           39334.35

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                   time [s]  count     SF  Throughput@Size
DBMS              SF    num_experiment num_client                                         
MonetDB-BHT-8-1-1 100.0 1              1               8910      1  100.0          4000.00
MonetDB-BHT-8-1-2 100.0 1              2               7710      1  100.0          4622.57
MonetDB-BHT-8-2-1 100.0 2              1               8561      1  100.0          4163.07
MonetDB-BHT-8-2-2 100.0 2              2               8934      1  100.0          3989.25

### Workflow
                             orig_name     SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-1  100.0     8               1           1       1764362824     1764371734
MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-1-2  100.0     8               1           2       1764371843     1764379553
MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-1  100.0     8               2           1       1764379819     1764388380
MonetDB-BHT-8-2-2-1  MonetDB-BHT-8-2-2  100.0     8               2           2       1764388481     1764397415

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1    71358.47    43.88        251.70                256.0
MonetDB-BHT-8-1-2    61131.63    49.23        252.10                256.0
MonetDB-BHT-8-2-1   133099.15    43.39        251.51                256.0
MonetDB-BHT-8-2-2    85888.50    42.57        252.59                256.0

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       52.76     0.23          0.40                 0.41
MonetDB-BHT-8-1-2       52.76     0.27          0.38                 0.39
MonetDB-BHT-8-2-1       51.89     0.22          0.39                 0.40
MonetDB-BHT-8-2-2       51.09     0.14          0.39                 0.40

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
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
  -rr 256Gi -lr 256Gi \
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

