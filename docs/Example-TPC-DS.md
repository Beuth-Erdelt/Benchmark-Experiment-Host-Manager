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
    Duration: 19347s 
    Code: 1764326998
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.16.
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
    disk:426278
    datadisk:4559
    cpu_list:0-63
    args:['--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1764326998
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:427321
    datadisk:5602
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1764326998
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:454586
    datadisk:32866
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1764326998
PostgreSQL-BHT-8-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:427523
    datadisk:5803
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1764326998

### Errors (failed queries)
            MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q72               True              False             False                 False
TPC-DS Q94               True              False             False                 False
TPC-DS Q95               True              False             False                 False
TPC-DS Q72
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=246) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q94
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=246) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q95
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=246) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)
               MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q3                  False              False              True                 False
TPC-DS Q4                  False              False              True                 False
TPC-DS Q5                  False              False              True                 False
TPC-DS Q6                  False              False              True                 False
TPC-DS Q7                  False              False              True                 False
TPC-DS Q9                  False              False              True                 False
TPC-DS Q10                 False              False              True                 False
TPC-DS Q11                 False               True              True                 False
TPC-DS Q12                 False              False              True                 False
TPC-DS Q13                 False              False              True                 False
TPC-DS Q14a+b              False              False              True                 False
TPC-DS Q15                 False              False              True                 False
TPC-DS Q18                 False              False              True                 False
TPC-DS Q19                 False              False              True                 False
TPC-DS Q20                 False              False              True                  True
TPC-DS Q21                 False              False              True                 False
TPC-DS Q22                 False              False              True                 False
TPC-DS Q24a+b              False              False              True                 False
TPC-DS Q26                 False              False              True                 False
TPC-DS Q27                 False               True             False                  True
TPC-DS Q28                 False              False              True                 False
TPC-DS Q30                 False              False              True                 False
TPC-DS Q31                 False              False              True                 False
TPC-DS Q32                 False              False              True                 False
TPC-DS Q33                 False              False              True                 False
TPC-DS Q35                 False              False              True                 False
TPC-DS Q36                 False               True             False                  True
TPC-DS Q38                 False              False              True                 False
TPC-DS Q39a+b              False               True              True                  True
TPC-DS Q40                 False              False              True                 False
TPC-DS Q42                 False              False              True                 False
TPC-DS Q44                 False               True              True                 False
TPC-DS Q45                 False              False              True                 False
TPC-DS Q47                 False              False              True                 False
TPC-DS Q48                 False              False              True                 False
TPC-DS Q49                 False              False              True                 False
TPC-DS Q50                 False              False              True                 False
TPC-DS Q51                 False              False              True                 False
TPC-DS Q52                 False              False              True                 False
TPC-DS Q53                 False              False              True                 False
TPC-DS Q55                 False              False              True                 False
TPC-DS Q56                 False              False              True                 False
TPC-DS Q57                 False              False              True                 False
TPC-DS Q60                 False              False              True                 False
TPC-DS Q62                 False              False              True                 False
TPC-DS Q63                 False              False              True                 False
TPC-DS Q64                 False              False              True                 False
TPC-DS Q65                 False              False              True                 False
TPC-DS Q66                 False              False              True                 False
TPC-DS Q67                 False               True              True                  True
TPC-DS Q69                 False              False              True                 False
TPC-DS Q70                 False               True              True                 False
TPC-DS Q71                 False              False              True                 False
TPC-DS Q72                 False               True              True                  True
TPC-DS Q74                 False              False              True                 False
TPC-DS Q75                 False              False              True                 False
TPC-DS Q76                 False              False              True                 False
TPC-DS Q77                 False              False              True                 False
TPC-DS Q78                 False               True              True                  True
TPC-DS Q79                 False              False              True                 False
TPC-DS Q80                 False               True              True                  True
TPC-DS Q81                 False              False              True                 False
TPC-DS Q83                 False              False              True                 False
TPC-DS Q86                 False               True              True                  True
TPC-DS Q87                 False              False              True                 False
TPC-DS Q88                 False              False              True                 False
TPC-DS Q90                 False              False              True                 False
TPC-DS Q91                 False              False              True                 False
TPC-DS Q92                 False              False              True                 False
TPC-DS Q93                 False              False              True                 False
TPC-DS Q94                 False               True              True                  True
TPC-DS Q95                 False               True              True                  True
TPC-DS Q96                 False              False              True                 False
TPC-DS Q97                 False              False              True                 False
TPC-DS Q98                 False               True              True                 False
TPC-DS Q99                 False              False              True                 False

### Latency of Timer Execution [ms]
DBMS           MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
TPC-DS Q1                  36.80              43.11             73.34                235.24
TPC-DS Q2               17588.33             153.12              8.30                855.34
TPC-DS Q3                  41.08              21.46              3.17                462.49
TPC-DS Q4               40281.63            1175.52             17.61              19390.56
TPC-DS Q5               29774.60             236.44              8.33               1341.11
TPC-DS Q6                2769.43              64.01              2.95             172618.06
TPC-DS Q7               12628.04              54.76              2.48               1020.07
TPC-DS Q8                1033.34              42.72              3.47                140.34
TPC-DS Q9               12700.37              51.75              3.43               5746.28
TPC-DS Q10               2011.63              34.28              4.46               2735.61
TPC-DS Q11              25222.75             604.72              6.57              12017.74
TPC-DS Q12                926.62              26.25             14.95                184.73
TPC-DS Q13               2977.28              92.97              3.31               1787.29
TPC-DS Q14a+b          156910.82            2001.73             16.72               6122.35
TPC-DS Q15                896.52              28.46              2.67                328.80
TPC-DS Q16              37827.85              35.16              2.77                535.00
TPC-DS Q17               7436.96             128.23              2.74                887.64
TPC-DS Q18               6970.41             146.71              2.51               1189.26
TPC-DS Q19                824.33              41.44              1.65                463.76
TPC-DS Q20               1745.32              25.82              1.42                292.19
TPC-DS Q21              88974.46              79.19              2.60                658.57
TPC-DS Q22             176840.88            1113.24              1.83               9762.14
TPC-DS Q23a+b          195152.75            2823.61              8.28              12481.06
TPC-DS Q24a+b            6991.31             251.14              6.20               1844.49
TPC-DS Q25               1475.36             129.77              2.02                868.81
TPC-DS Q26               7646.60              24.17              2.24                713.35
TPC-DS Q27               4968.65             150.47              2.57                 50.82
TPC-DS Q28               9243.49              64.13              3.42               4330.62
TPC-DS Q29                240.96             130.84              2.48                955.88
TPC-DS Q30                303.05              21.84              3.18              29898.41
TPC-DS Q31               4207.17             165.93              6.47               5073.78
TPC-DS Q32                 22.83              20.08              2.22                285.19
TPC-DS Q33                546.82              24.87              4.18               1089.99
TPC-DS Q34              12371.95              29.40              1.96                 56.99
TPC-DS Q35               3429.21              87.82              2.99               3045.28
TPC-DS Q36               5461.30              66.91              2.62                 51.27
TPC-DS Q37              13602.58              70.57              2.25                668.25
TPC-DS Q38              26137.20             218.10              2.43               3216.43
TPC-DS Q39a+b            4537.91            1470.64              6.16               6106.69
TPC-DS Q40                732.16              76.03              1.91                310.14
TPC-DS Q41               1629.13               9.44              5.59               2842.39
TPC-DS Q42                692.39              19.25              2.43                237.24
TPC-DS Q43               3476.53              43.38              2.40                 56.57
TPC-DS Q44               4081.01              77.76              2.04               1127.82
TPC-DS Q45                428.81              26.19              1.81                221.24
TPC-DS Q46              14033.26              45.17              1.94                 76.96
TPC-DS Q47              42406.81             258.63              3.79               4824.81
TPC-DS Q48               3467.92              95.81              1.87               1808.02
TPC-DS Q49               1097.82             100.91              3.60               1996.78
TPC-DS Q50                159.43             100.01              2.10               1140.36
TPC-DS Q51              26861.49             491.46              2.53               2612.23
TPC-DS Q52                797.29              23.91              1.44                235.48
TPC-DS Q53                589.20              26.19              1.72                293.06
TPC-DS Q54               2819.18              27.00              4.49                182.34
TPC-DS Q55                718.32              15.35              1.55                238.21
TPC-DS Q56                674.54              29.09              3.75               1018.05
TPC-DS Q57              23196.99             117.53              5.47               2295.15
TPC-DS Q58              23357.49              59.39              9.21               1232.57
TPC-DS Q59              36330.22             118.47              4.49               1146.19
TPC-DS Q60               1380.17              21.94              4.15               1000.75
TPC-DS Q61               1228.10              31.90              1.91               4064.54
TPC-DS Q62               6260.09              26.21              3.34                286.38
TPC-DS Q63                611.95              26.37              2.48                287.73
TPC-DS Q64               2045.48             360.94              6.46               1730.21
TPC-DS Q65              22901.59              95.97              2.31               1441.78
TPC-DS Q66               4143.02              94.90              4.91                590.46
TPC-DS Q67              25711.18             445.45              2.60               6675.24
TPC-DS Q68              12231.50              37.68              2.14                 78.03
TPC-DS Q69               1372.16              35.06              2.80                631.03
TPC-DS Q70              32895.85              92.63              2.30               1122.47
TPC-DS Q71               1271.68              29.95              2.16                978.87
TPC-DS Q73              11195.77              23.14              2.80                 56.45
TPC-DS Q74              19097.68             623.13              4.29               2711.07
TPC-DS Q75              17733.91             711.98              4.02               2199.20
TPC-DS Q76               1544.01              46.90              2.15                577.61
TPC-DS Q77              23362.23              55.85              4.40               4215.28
TPC-DS Q78              19942.37             773.83              3.41               3481.06
TPC-DS Q79              12618.43              48.63              2.41                451.04
TPC-DS Q80               2199.45             474.07              3.24               1204.90
TPC-DS Q81                770.93              29.66              2.63             122458.31
TPC-DS Q82              13461.63              61.62              2.15                627.85
TPC-DS Q83               2959.17              19.19              2.70                267.79
TPC-DS Q84                469.63              35.94              1.22                256.73
TPC-DS Q85                425.58              37.74              1.95                846.31
TPC-DS Q86               3454.71              27.89              1.39                553.10
TPC-DS Q87              26331.19             296.46              2.28               3292.46
TPC-DS Q88              86967.21              68.40              4.96               6151.85
TPC-DS Q89               4787.68              34.14              2.17                 58.38
TPC-DS Q90                374.63              16.86              1.28               1918.59
TPC-DS Q91                 64.29              26.02              1.78                451.51
TPC-DS Q92                 13.61              14.91              1.85                137.13
TPC-DS Q93                137.45             129.15              1.94                521.84
TPC-DS Q96               9744.53              11.46              1.27                250.37
TPC-DS Q97              19219.35             235.67              5.16                986.33
TPC-DS Q98               3406.38              40.54              2.41                486.96
TPC-DS Q99              18958.58              55.61              2.13                383.63

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1              1.0          631.0         7.0    11727.0   12374.0
MonetDB-BHT-8-1-1              1.0           97.0         9.0      251.0     367.0
MySQL-BHT-64-1-1               1.0            9.0         7.0      181.0     208.0
PostgreSQL-BHT-8-1-1           0.0          137.0         1.0      337.0     484.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              3.68
MonetDB-BHT-8-1-1              0.08
MySQL-BHT-64-1-1               0.00
PostgreSQL-BHT-8-1-1           0.97

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1                980.15
MonetDB-BHT-8-1-1              48664.29
MySQL-BHT-64-1-1             1156008.07
PostgreSQL-BHT-8-1-1            3757.32

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
MariaDB-BHT-8-1    1.0 1              1               5131      1  1.0            67.36
MonetDB-BHT-8-1    1.0 1              1                 31      1  1.0         11148.39
MySQL-BHT-64-1     1.0 1              1                 10      1  1.0         34560.00
PostgreSQL-BHT-8-1 1.0 1              1                532      1  1.0           649.62

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MariaDB-BHT-8-1-1        MariaDB-BHT-8-1  1.0     8               1           1       1764340668     1764345799
MonetDB-BHT-8-1-1        MonetDB-BHT-8-1  1.0     8               1           1       1764328567     1764328598
MySQL-BHT-64-1-1          MySQL-BHT-64-1  1.0     8               1           1       1764346274     1764346284
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  1.0     8               1           1       1764327525     1764328057

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
    Duration: 764s 
    Code: 1764346504
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.16.
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
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:434611
    datadisk:12891
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1764346504

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                  58.38
TPC-DS Q2                 518.37
TPC-DS Q3                  44.88
TPC-DS Q4                3999.70
TPC-DS Q5                 651.97
TPC-DS Q6                 219.02
TPC-DS Q7                  84.42
TPC-DS Q8                  95.72
TPC-DS Q9                 125.66
TPC-DS Q10                 94.52
TPC-DS Q11               1949.05
TPC-DS Q12                 36.78
TPC-DS Q13                160.14
TPC-DS Q14a+b            6650.44
TPC-DS Q15                 47.22
TPC-DS Q16                298.26
TPC-DS Q17                380.11
TPC-DS Q18                247.53
TPC-DS Q19                 79.01
TPC-DS Q20                 54.48
TPC-DS Q21                102.85
TPC-DS Q22               2974.30
TPC-DS Q23a+b            9444.67
TPC-DS Q24a+b             925.89
TPC-DS Q25                438.94
TPC-DS Q26                 67.85
TPC-DS Q27                358.86
TPC-DS Q28                167.72
TPC-DS Q29                378.76
TPC-DS Q30                 31.81
TPC-DS Q31                504.43
TPC-DS Q32                 36.35
TPC-DS Q33                 46.87
TPC-DS Q34                 41.27
TPC-DS Q35                194.63
TPC-DS Q36                424.67
TPC-DS Q37                229.88
TPC-DS Q38                632.30
TPC-DS Q39a+b            3731.51
TPC-DS Q40                208.92
TPC-DS Q41                  9.15
TPC-DS Q42                 35.39
TPC-DS Q43                101.56
TPC-DS Q44                211.67
TPC-DS Q45                 41.21
TPC-DS Q46                 82.89
TPC-DS Q47                660.57
TPC-DS Q48                132.69
TPC-DS Q49                258.74
TPC-DS Q50                217.66
TPC-DS Q51               1474.10
TPC-DS Q52                 40.56
TPC-DS Q53                 53.35
TPC-DS Q54                 39.26
TPC-DS Q55                 31.25
TPC-DS Q56                 76.71
TPC-DS Q57                180.70
TPC-DS Q58                164.51
TPC-DS Q59                289.76
TPC-DS Q60                 52.41
TPC-DS Q61                 73.00
TPC-DS Q62                 49.24
TPC-DS Q63                 49.43
TPC-DS Q64               1253.06
TPC-DS Q65                432.21
TPC-DS Q66                271.92
TPC-DS Q67               1479.15
TPC-DS Q68                 78.49
TPC-DS Q69                 37.15
TPC-DS Q70                273.88
TPC-DS Q71                 64.54
TPC-DS Q72                277.42
TPC-DS Q73                 46.11
TPC-DS Q74                570.71
TPC-DS Q75               2241.43
TPC-DS Q76                182.24
TPC-DS Q77                170.45
TPC-DS Q78               3006.89
TPC-DS Q79                111.97
TPC-DS Q80               2244.42
TPC-DS Q81                 56.20
TPC-DS Q82                429.92
TPC-DS Q83                 31.30
TPC-DS Q84                101.00
TPC-DS Q85                 80.68
TPC-DS Q86                 66.84
TPC-DS Q87                926.64
TPC-DS Q88                177.80
TPC-DS Q89                 80.39
TPC-DS Q90                 19.26
TPC-DS Q91                 26.91
TPC-DS Q92                 22.68
TPC-DS Q93                453.31
TPC-DS Q94                 63.81
TPC-DS Q95                217.77
TPC-DS Q96                 21.78
TPC-DS Q97                900.70
TPC-DS Q98                 91.31
TPC-DS Q99                 99.57

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          238.0         8.0      495.0     749.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.18

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           62179.63

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MonetDB-BHT-8-1 3.0 1              1                 70      1  3.0         15274.29

### Workflow
                         orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  3.0     8               1           1       1764347142     1764347212

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       27.55     0.18          0.01                 2.21

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      336.01     4.83          7.66                16.77

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       12.48        0          0.25                 0.25

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
    Duration: 538s 
    Code: 1764347404
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.16.
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
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:427319
    datadisk:5599
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1764347404
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:427377
    datadisk:5657
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1764347404
MonetDB-BHT-8-2-2 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:427377
    datadisk:5657
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1764347404

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-2-2
TPC-DS Q39a+b              False               True               True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-2-2
TPC-DS Q1                  36.61              39.70              34.84
TPC-DS Q2                 174.57             177.10             140.32
TPC-DS Q3                  24.36              23.31              60.98
TPC-DS Q4                1252.88            1279.92            1252.54
TPC-DS Q5                 264.33             267.02             271.44
TPC-DS Q6                  78.19              71.77              63.73
TPC-DS Q7                  48.10              53.14              60.23
TPC-DS Q8                  45.36              40.38              41.85
TPC-DS Q9                  52.69              55.13             116.47
TPC-DS Q10                 62.33              37.02              35.97
TPC-DS Q11                709.26             611.58             607.37
TPC-DS Q12                 21.60              19.97              22.22
TPC-DS Q13                110.48              98.84             114.30
TPC-DS Q14a+b            2315.15            2413.78            2473.02
TPC-DS Q15                 27.19              29.46              23.52
TPC-DS Q16                 35.35              35.81              32.22
TPC-DS Q17                132.17             130.50             105.14
TPC-DS Q18                121.94              60.34              55.98
TPC-DS Q19                 37.96              38.65              38.19
TPC-DS Q20                 25.23              23.16              25.22
TPC-DS Q21                 65.62              62.14              65.31
TPC-DS Q22               1111.44            1104.78            1139.10
TPC-DS Q23a+b            1905.39            2010.35            2307.70
TPC-DS Q24a+b             170.49             171.59             168.67
TPC-DS Q25                108.71              98.10              92.73
TPC-DS Q26                 26.83              19.63              20.54
TPC-DS Q27                103.15             126.56             122.41
TPC-DS Q28                 65.11              64.15              63.17
TPC-DS Q29                109.54             102.20             113.56
TPC-DS Q30                 21.85              20.01              19.16
TPC-DS Q31                165.50             135.30             134.08
TPC-DS Q32                 16.73              18.19              16.47
TPC-DS Q33                 22.55              27.44              21.93
TPC-DS Q34                 24.27              25.47              23.25
TPC-DS Q35                 81.26              71.90              71.34
TPC-DS Q36                 83.17              71.40              76.46
TPC-DS Q37                122.99              51.52              51.83
TPC-DS Q38                210.65             204.86             194.85
TPC-DS Q39a+b            1373.91            1370.93            1334.98
TPC-DS Q40                 75.09             112.41             110.33
TPC-DS Q41                  9.19               8.06               7.78
TPC-DS Q42                 18.17              18.94              18.31
TPC-DS Q43                 63.06              62.66              63.18
TPC-DS Q44                 36.45              33.09              36.97
TPC-DS Q45                 25.80              27.66              24.44
TPC-DS Q46                 44.90              47.87              44.92
TPC-DS Q47                248.34             265.71             248.25
TPC-DS Q48                 96.79             110.87              94.90
TPC-DS Q49                 96.85             104.29             102.00
TPC-DS Q50                 93.26              99.71             111.06
TPC-DS Q51                476.07             499.40             490.02
TPC-DS Q52                 21.60              25.90              19.13
TPC-DS Q53                 26.29              25.77              24.53
TPC-DS Q54                 23.09              22.84              30.30
TPC-DS Q55                 14.48              15.65              15.55
TPC-DS Q56                 25.93              20.89              26.26
TPC-DS Q57                108.08             115.55             113.07
TPC-DS Q58                 51.28             101.50              45.77
TPC-DS Q59                118.94             106.80             117.32
TPC-DS Q60                 25.93              28.26              37.66
TPC-DS Q61                 33.63              34.11              32.58
TPC-DS Q62                 23.61              22.81              25.49
TPC-DS Q63                 27.62              26.30              26.23
TPC-DS Q64                371.34             223.54             208.01
TPC-DS Q65                 95.57              88.11              91.80
TPC-DS Q66                 98.29              89.45              91.11
TPC-DS Q67                416.33             421.57             428.77
TPC-DS Q68                 39.47              38.98              38.36
TPC-DS Q69                 33.93              32.72              34.29
TPC-DS Q70                103.00             100.06              86.97
TPC-DS Q71                 30.97              30.76              30.22
TPC-DS Q72                160.95             136.18             148.29
TPC-DS Q73                 24.94              31.71              25.65
TPC-DS Q74                186.46             176.89             191.58
TPC-DS Q75                684.87             692.60             681.44
TPC-DS Q76                 48.32              52.53              47.48
TPC-DS Q77                 68.38              63.20              75.39
TPC-DS Q78                857.88             928.14             932.96
TPC-DS Q79                 40.91              39.45              42.93
TPC-DS Q80                512.17             503.22             476.91
TPC-DS Q81                 33.21              27.33              30.92
TPC-DS Q82                 61.72              43.87              63.82
TPC-DS Q83                 14.88              13.40              13.97
TPC-DS Q84                 38.97              15.20              14.39
TPC-DS Q85                 33.76              34.43              37.31
TPC-DS Q86                 26.73              26.15              25.47
TPC-DS Q87                279.84             288.42             272.61
TPC-DS Q88                 70.42              64.74              71.53
TPC-DS Q89                 39.47              38.27              37.65
TPC-DS Q90                 17.18               9.89              15.41
TPC-DS Q91                 26.22              32.35              25.45
TPC-DS Q92                 12.31              11.35              11.57
TPC-DS Q93                 99.52             133.79              98.15
TPC-DS Q94                 16.92              16.39              15.60
TPC-DS Q95                107.56             124.83             139.07
TPC-DS Q96                 14.99              11.33              11.00
TPC-DS Q97                221.46             231.34             249.60
TPC-DS Q98                 46.84              40.81              40.09
TPC-DS Q99                 56.48              54.49              52.49

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0           91.0         9.0      207.0     316.0
MonetDB-BHT-8-2-1           1.0           91.0         9.0      207.0     316.0
MonetDB-BHT-8-2-2           1.0           91.0         9.0      207.0     316.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.08
MonetDB-BHT-8-2-1           0.07
MonetDB-BHT-8-2-2           0.07

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           50112.52
MonetDB-BHT-8-2-1           52331.93
MonetDB-BHT-8-2-2           51929.54

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MonetDB-BHT-8-1 1.0 1              1                 33      1  1.0          10800.0
MonetDB-BHT-8-2 1.0 1              2                 30      2  1.0          23760.0

### Workflow
                         orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  1.0     8               1           1       1764347755     1764347788
MonetDB-BHT-8-2-1  MonetDB-BHT-8-2  1.0     8               1           2       1764347847     1764347877
MonetDB-BHT-8-2-2  MonetDB-BHT-8-2  1.0     8               1           2       1764347847     1764347877

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
    Duration: 774s 
    Code: 1764348094
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.16.
    Experiment is limited to DBMS ['MonetDB'].
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
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:421721
    datadisk:5598
    volume_size:10G
    volume_used:5.2G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1764348094
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:421721
    datadisk:5677
    volume_size:10G
    volume_used:5.6G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1764348094

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q39a+b                False                 True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-2-1-1
TPC-DS Q1                    44.79               409.05
TPC-DS Q2                   168.70               605.58
TPC-DS Q3                    36.42               762.32
TPC-DS Q4                  1246.79              2897.77
TPC-DS Q5                   254.37              1403.22
TPC-DS Q6                    72.03               530.68
TPC-DS Q7                    62.87              1718.39
TPC-DS Q8                    48.82               309.25
TPC-DS Q9                    68.94               247.69
TPC-DS Q10                   65.47              6218.97
TPC-DS Q11                  585.53               642.25
TPC-DS Q12                   28.48               371.86
TPC-DS Q13                  102.79               240.84
TPC-DS Q14a+b              2471.93              2655.83
TPC-DS Q15                   25.62                31.43
TPC-DS Q16                   40.42               796.48
TPC-DS Q17                  192.92               307.50
TPC-DS Q18                  160.29               434.90
TPC-DS Q19                   41.46               106.19
TPC-DS Q20                   26.36                26.42
TPC-DS Q21                   99.78              3216.02
TPC-DS Q22                 1166.49              1231.95
TPC-DS Q23a+b              2178.62              2475.68
TPC-DS Q24a+b               182.77               301.73
TPC-DS Q25                   88.72               110.88
TPC-DS Q26                   21.89                21.52
TPC-DS Q27                  150.37               128.68
TPC-DS Q28                   66.45                67.99
TPC-DS Q29                  123.43               120.71
TPC-DS Q30                   28.27               175.92
TPC-DS Q31                  195.37               172.30
TPC-DS Q32                   19.54                24.05
TPC-DS Q33                   23.16                54.28
TPC-DS Q34                   32.54               143.47
TPC-DS Q35                   76.19                81.28
TPC-DS Q36                   84.95                88.01
TPC-DS Q37                  146.25                77.64
TPC-DS Q38                  218.21               220.68
TPC-DS Q39a+b              1172.87              1183.25
TPC-DS Q40                   78.31                54.97
TPC-DS Q41                    8.30                 8.39
TPC-DS Q42                   18.12                24.01
TPC-DS Q43                   42.65               172.18
TPC-DS Q44                   38.71                96.93
TPC-DS Q45                   25.65                66.99
TPC-DS Q46                   46.78               102.66
TPC-DS Q47                  248.63               333.18
TPC-DS Q48                  102.89                97.53
TPC-DS Q49                  109.75               421.68
TPC-DS Q50                   94.14               232.37
TPC-DS Q51                  506.76               526.11
TPC-DS Q52                   20.34                20.88
TPC-DS Q53                   26.85                31.89
TPC-DS Q54                   28.10                25.39
TPC-DS Q55                   15.26                14.27
TPC-DS Q56                   32.12                42.32
TPC-DS Q57                  101.02               130.97
TPC-DS Q58                   46.70                52.31
TPC-DS Q59                  114.69               121.32
TPC-DS Q60                   24.29               120.09
TPC-DS Q61                   33.19               104.73
TPC-DS Q62                   43.97                87.92
TPC-DS Q63                   25.26                24.05
TPC-DS Q64                  438.90               652.54
TPC-DS Q65                   95.46               132.23
TPC-DS Q66                   93.75               125.10
TPC-DS Q67                  407.10               437.63
TPC-DS Q68                   39.50                39.28
TPC-DS Q69                   36.18                61.01
TPC-DS Q70                  101.43               694.28
TPC-DS Q71                   37.68                35.32
TPC-DS Q72                  262.43              1100.42
TPC-DS Q73                   23.27                23.78
TPC-DS Q74                  183.51               184.33
TPC-DS Q75                  684.84               732.47
TPC-DS Q76                   34.09               190.13
TPC-DS Q77                   84.45                93.43
TPC-DS Q78                  801.33               903.54
TPC-DS Q79                   43.42                73.37
TPC-DS Q80                  449.13               503.04
TPC-DS Q81                   32.76               342.61
TPC-DS Q82                  189.54               422.67
TPC-DS Q83                   31.71                21.97
TPC-DS Q84                   44.81                69.56
TPC-DS Q85                   34.55                57.53
TPC-DS Q86                   26.23                30.93
TPC-DS Q87                  262.85               268.29
TPC-DS Q88                   98.90               192.08
TPC-DS Q89                   36.08                33.72
TPC-DS Q90                   16.21                12.66
TPC-DS Q91                   24.35               110.80
TPC-DS Q92                   11.05                10.66
TPC-DS Q93                   94.85               107.92
TPC-DS Q94                   20.49                19.60
TPC-DS Q95                  135.77               107.90
TPC-DS Q96                   11.43                11.37
TPC-DS Q97                  224.47               231.92
TPC-DS Q98                   40.74                41.14
TPC-DS Q99                   57.76                63.36

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0           93.0        11.0      221.0     334.0
MonetDB-BHT-8-2-1-1           1.0           93.0        11.0      221.0     334.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.08
MonetDB-BHT-8-2-1-1           0.15

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           46817.41
MonetDB-BHT-8-2-1-1           24744.43

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                 time [s]  count   SF  Throughput@Size
DBMS              SF  num_experiment num_client                                       
MonetDB-BHT-8-1-1 1.0 1              1                 28      1  1.0         12728.57
MonetDB-BHT-8-2-1 1.0 2              1                114      1  1.0          3126.32

### Workflow
                             orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-1  1.0     8               1           1       1764348447     1764348475
MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-1  1.0     8               2           1       1764348702     1764348816

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
    Duration: 1853s 
    Code: 1764433708
    We compute for all columns: Minimum, maximum, average, count, count distinct, count NULL and non NULL entries and coefficient of variation.
    This experiment compares imported TPC-DS data sets in different DBMS.
    TPC-DS (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.16.
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
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:421727
    datadisk:40681
    volume_size:50G
    volume_used:40G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1764433708
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:421727
    datadisk:40681
    volume_size:50G
    volume_used:40G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1764433708

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                                    MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1
statistics_tab about call_center.cc_call_center_sk - all                            39.33              26.57
statistics_tab about call_center.cc_call_center_id - all                            15.78               7.20
statistics_tab about call_center.cc_rec_start_date - all                            13.71               7.01
statistics_tab about call_center.cc_rec_end_date - all                              14.06               6.12
statistics_tab about call_center.cc_closed_date_sk - all                            11.34               4.12
statistics_tab about call_center.cc_open_date_sk - all                              12.85               4.28
statistics_tab about call_center.cc_name - all                                      22.74               6.25
statistics_tab about call_center.cc_class - all                                     17.38               5.93
statistics_tab about call_center.cc_employees - all                                  6.73               4.55
statistics_tab about call_center.cc_sq_ft - all                                      7.33               3.93
statistics_tab about call_center.cc_hours - all                                     11.15               6.15
statistics_tab about call_center.cc_manager - all                                   10.38               6.40
statistics_tab about call_center.cc_mkt_id - all                                     6.58               4.64
statistics_tab about call_center.cc_mkt_class - all                                  8.26               6.32
statistics_tab about call_center.cc_mkt_desc - all                                   9.73               6.50
statistics_tab about call_center.cc_market_manager - all                            10.89               6.70
statistics_tab about call_center.cc_division - all                                   5.46               3.93
statistics_tab about call_center.cc_division_name - all                              7.65               6.66
statistics_tab about call_center.cc_company - all                                    5.23               4.08
statistics_tab about call_center.cc_company_name - all                               8.05               5.67
statistics_tab about call_center.cc_street_number - all                              9.41               5.44
statistics_tab about call_center.cc_street_name - all                               10.34               6.42
statistics_tab about call_center.cc_street_type - all                                9.77               5.92
statistics_tab about call_center.cc_suite_number - all                              11.29               5.68
statistics_tab about call_center.cc_city - all                                       9.97               5.88
statistics_tab about call_center.cc_county - all                                     9.66               5.65
statistics_tab about call_center.cc_state - all                                      9.77               5.71
statistics_tab about call_center.cc_zip - all                                        9.25               6.03
statistics_tab about call_center.cc_country - all                                   10.75               5.52
statistics_tab about call_center.cc_gmt_offset - all                                 7.24               3.64
statistics_tab about call_center.cc_tax_percentage - all                             5.83               3.49
statistics_tab about catalog_page.cp_catalog_page_sk - all                          12.32               4.90
statistics_tab about catalog_page.cp_catalog_page_id - all                          13.44               6.36
statistics_tab about catalog_page.cp_start_date_sk - all                             7.24               5.31
statistics_tab about catalog_page.cp_end_date_sk - all                               8.86               4.89
statistics_tab about catalog_page.cp_department - all                               11.96               6.76
statistics_tab about catalog_page.cp_catalog_number - all                            8.58               4.03
statistics_tab about catalog_page.cp_catalog_page_number - all                       5.47               3.89
statistics_tab about catalog_page.cp_description - all                              15.82              12.75
statistics_tab about catalog_page.cp_type - all                                      9.23               6.01
statistics_tab about catalog_returns.cr_returned_date_sk - all                      73.00              89.53
statistics_tab about catalog_returns.cr_returned_time_sk - all                     116.28             100.00
statistics_tab about catalog_returns.cr_item_sk - all                              126.18              90.59
statistics_tab about catalog_returns.cr_refunded_customer_sk - all                 302.49             127.57
statistics_tab about catalog_returns.cr_refunded_cdemo_sk - all                    251.46             178.65
statistics_tab about catalog_returns.cr_refunded_hdemo_sk - all                     71.99              59.71
statistics_tab about catalog_returns.cr_refunded_addr_sk - all                     196.59             104.08
statistics_tab about catalog_returns.cr_returning_customer_sk - all                390.15             136.93
statistics_tab about catalog_returns.cr_returning_cdemo_sk - all                   354.02             193.05
statistics_tab about catalog_returns.cr_returning_hdemo_sk - all                    90.71              74.09
statistics_tab about catalog_returns.cr_returning_addr_sk - all                    234.82             104.55
statistics_tab about catalog_returns.cr_call_center_sk - all                        76.65              59.04
statistics_tab about catalog_returns.cr_catalog_page_sk - all                       74.44              74.74
statistics_tab about catalog_returns.cr_ship_mode_sk - all                         114.03              59.77
statistics_tab about catalog_returns.cr_warehouse_sk - all                          90.78              73.97
statistics_tab about catalog_returns.cr_reason_sk - all                             91.97              60.06
statistics_tab about catalog_returns.cr_order_number - all                          99.05              99.29
statistics_tab about catalog_returns.cr_return_quantity - all                       66.25              56.51
statistics_tab about catalog_returns.cr_return_amount - all                        187.56             130.77
statistics_tab about catalog_returns.cr_return_tax - all                            98.43              71.87
statistics_tab about catalog_returns.cr_return_amt_inc_tax - all                   273.05             124.01
statistics_tab about catalog_returns.cr_fee - all                                   82.41              68.91
statistics_tab about catalog_returns.cr_return_ship_cost - all                     137.17             103.41
statistics_tab about catalog_returns.cr_refunded_cash - all                        164.44             117.67
statistics_tab about catalog_returns.cr_reversed_charge - all                      126.69              96.82
statistics_tab about catalog_returns.cr_store_credit - all                         127.08              98.49
statistics_tab about catalog_returns.cr_net_loss - all                             186.71             118.49
statistics_tab about catalog_sales.cs_sold_date_sk - all                           794.60             590.89
statistics_tab about catalog_sales.cs_sold_time_sk - all                           945.92             720.15
statistics_tab about catalog_sales.cs_ship_date_sk - all                           670.74             593.12
statistics_tab about catalog_sales.cs_bill_customer_sk - all                       916.56             891.25
statistics_tab about catalog_sales.cs_bill_cdemo_sk - all                          988.28             903.15
statistics_tab about catalog_sales.cs_bill_hdemo_sk - all                          606.83             641.18
statistics_tab about catalog_sales.cs_bill_addr_sk - all                           933.11             801.12
statistics_tab about catalog_sales.cs_ship_customer_sk - all                      1011.49             905.33
statistics_tab about catalog_sales.cs_ship_cdemo_sk - all                          912.05            1386.55
statistics_tab about catalog_sales.cs_ship_hdemo_sk - all                          600.15            1477.64
statistics_tab about catalog_sales.cs_ship_addr_sk - all                          1066.90            2145.76
statistics_tab about catalog_sales.cs_call_center_sk - all                         599.68             842.30
statistics_tab about catalog_sales.cs_catalog_page_sk - all                        659.19            1078.99
statistics_tab about catalog_sales.cs_ship_mode_sk - all                           650.58             792.13
statistics_tab about catalog_sales.cs_warehouse_sk - all                           742.02             885.91
statistics_tab about catalog_sales.cs_item_sk - all                                769.02             798.38
statistics_tab about catalog_sales.cs_promo_sk - all                               639.35             867.01
statistics_tab about catalog_sales.cs_order_number - all                           723.60             760.53
statistics_tab about catalog_sales.cs_quantity - all                               679.71             816.45
statistics_tab about catalog_sales.cs_wholesale_cost - all                         672.24             850.60
statistics_tab about catalog_sales.cs_list_price - all                             707.79             888.74
statistics_tab about catalog_sales.cs_sales_price - all                            693.38            3913.24
statistics_tab about catalog_sales.cs_ext_discount_amt - all                      2310.31            6847.33
statistics_tab about catalog_sales.cs_ext_sales_price - all                       2069.47            2021.03
statistics_tab about catalog_sales.cs_ext_wholesale_cost - all                    1593.47            2573.04
statistics_tab about catalog_sales.cs_ext_list_price - all                        2620.24            4138.32
statistics_tab about catalog_sales.cs_ext_tax - all                                928.54             959.68
statistics_tab about catalog_sales.cs_coupon_amt - all                             972.56            1308.37
statistics_tab about catalog_sales.cs_ext_ship_cost - all                         1380.62            6298.36
statistics_tab about catalog_sales.cs_net_paid - all                              1720.02            3984.40
statistics_tab about catalog_sales.cs_net_paid_inc_tax - all                      2053.45            3722.93
statistics_tab about catalog_sales.cs_net_paid_inc_ship - all                     2153.66            2831.32
statistics_tab about catalog_sales.cs_net_paid_inc_ship_tax - all                 2371.48            5173.38
statistics_tab about catalog_sales.cs_net_profit - all                            2737.03            3880.86
statistics_tab about customer.c_customer_sk - all                                    8.95              15.17
statistics_tab about customer.c_customer_id - all                                  139.03             250.70
statistics_tab about customer.c_current_cdemo_sk - all                              52.50              97.75
statistics_tab about customer.c_current_hdemo_sk - all                              27.88              34.00
statistics_tab about customer.c_current_addr_sk - all                               49.04              50.52
statistics_tab about customer.c_first_shipto_date_sk - all                          33.99              39.32
statistics_tab about customer.c_first_sales_date_sk - all                           28.65              46.49
statistics_tab about customer.c_salutation - all                                     9.98              16.79
statistics_tab about customer.c_first_name - all                                    55.17              64.53
statistics_tab about customer.c_last_name - all                                     62.23              91.53
statistics_tab about customer.c_preferred_cust_flag - all                            8.51              15.34
statistics_tab about customer.c_birth_day - all                                     22.55              33.42
statistics_tab about customer.c_birth_month - all                                   22.08              34.05
statistics_tab about customer.c_birth_year - all                                    26.21              35.71
statistics_tab about customer.c_birth_country - all                                  9.29              16.35
statistics_tab about customer.c_login - all                                          7.87              13.51
statistics_tab about customer.c_email_address - all                                192.66             291.92
statistics_tab about customer.c_last_review_date - all                              10.50              17.34
statistics_tab about customer_address.ca_address_sk - all                            9.64              17.02
statistics_tab about customer_address.ca_address_id - all                           65.88              82.20
statistics_tab about customer_address.ca_street_number - all                         7.83              13.81
statistics_tab about customer_address.ca_street_name - all                          40.07              45.68
statistics_tab about customer_address.ca_street_type - all                           8.25              13.26
statistics_tab about customer_address.ca_suite_number - all                          7.10              13.16
statistics_tab about customer_address.ca_city - all                                  7.40              16.06
statistics_tab about customer_address.ca_county - all                                8.07              17.07
statistics_tab about customer_address.ca_state - all                                 7.62              14.26
statistics_tab about customer_address.ca_zip - all                                  29.43              41.52
statistics_tab about customer_address.ca_country - all                               6.44              12.20
statistics_tab about customer_address.ca_gmt_offset - all                           12.50              17.63
statistics_tab about customer_address.ca_location_type - all                        15.40              14.06
statistics_tab about customer_demographics.cd_demo_sk - all                         16.23              22.91
statistics_tab about customer_demographics.cd_gender - all                          21.87              25.55
statistics_tab about customer_demographics.cd_marital_status - all                  22.38              24.18
statistics_tab about customer_demographics.cd_education_status - all                17.60              27.23
statistics_tab about customer_demographics.cd_purchase_estimate - all               97.68              97.12
statistics_tab about customer_demographics.cd_credit_rating - all                   20.15              28.17
statistics_tab about customer_demographics.cd_dep_count - all                       81.37              85.23
statistics_tab about customer_demographics.cd_dep_employed_count - all              86.47              88.06
statistics_tab about customer_demographics.cd_dep_college_count - all               75.45              85.15
statistics_tab about date_dim.d_date_sk - all                                        7.90              10.62
statistics_tab about date_dim.d_date_id - all                                        7.67              11.73
statistics_tab about date_dim.d_date - all                                           7.70              14.49
statistics_tab about date_dim.d_month_seq - all                                      5.75               8.84
statistics_tab about date_dim.d_week_seq - all                                       5.57               9.59
statistics_tab about date_dim.d_quarter_seq - all                                    7.02               7.13
statistics_tab about date_dim.d_year - all                                           5.67               8.56
statistics_tab about date_dim.d_dow - all                                            5.83               7.71
statistics_tab about date_dim.d_moy - all                                            5.51               7.43
statistics_tab about date_dim.d_dom - all                                            8.51               8.46
statistics_tab about date_dim.d_qoy - all                                            5.41               8.11
statistics_tab about date_dim.d_fy_year - all                                        5.99               7.81
statistics_tab about date_dim.d_fy_quarter_seq - all                                 5.40               7.54
statistics_tab about date_dim.d_fy_week_seq - all                                    6.73               7.55
statistics_tab about date_dim.d_day_name - all                                       6.79               9.07
statistics_tab about date_dim.d_quarter_name - all                                   7.25               9.20
statistics_tab about date_dim.d_holiday - all                                        6.07               8.74
statistics_tab about date_dim.d_weekend - all                                        6.43               9.80
statistics_tab about date_dim.d_following_holiday - all                              4.75               8.53
statistics_tab about date_dim.d_first_dom - all                                      6.10               8.15
statistics_tab about date_dim.d_last_dom - all                                       7.67               8.94
statistics_tab about date_dim.d_same_day_ly - all                                    5.94               8.01
statistics_tab about date_dim.d_same_day_lq - all                                    6.35               9.17
statistics_tab about date_dim.d_current_day - all                                    4.79               9.10
statistics_tab about date_dim.d_current_week - all                                   4.94               8.20
statistics_tab about date_dim.d_current_month - all                                  5.03               8.48
statistics_tab about date_dim.d_current_quarter - all                                4.81               8.65
statistics_tab about date_dim.d_current_year - all                                   5.08               8.57
statistics_tab about dbgen_version.dv_version - all                                  4.00               9.20
statistics_tab about dbgen_version.dv_create_date - all                              5.12               8.73
statistics_tab about dbgen_version.dv_create_time - all                              5.08               8.45
statistics_tab about dbgen_version.dv_cmdline_args - all                             5.29               8.92
statistics_tab about household_demographics.hd_demo_sk - all                         3.18               6.21
statistics_tab about household_demographics.hd_income_band_sk - all                  3.52               6.71
statistics_tab about household_demographics.hd_buy_potential - all                   4.86               9.91
statistics_tab about household_demographics.hd_dep_count - all                       2.98               8.73
statistics_tab about household_demographics.hd_vehicle_count - all                   2.66               6.26
statistics_tab about income_band.ib_income_band_sk - all                             2.50               5.37
statistics_tab about income_band.ib_lower_bound - all                                2.41               6.23
statistics_tab about income_band.ib_upper_bound - all                                2.54               5.51
statistics_tab about inventory.inv_date_sk - all                                  8389.75            7674.50
statistics_tab about inventory.inv_item_sk - all                                  7976.66            7971.91
statistics_tab about inventory.inv_warehouse_sk - all                             8174.07            7131.78
statistics_tab about inventory.inv_quantity_on_hand - all                        15342.03           10230.56
statistics_tab about item.i_item_sk - all                                           21.27               9.78
statistics_tab about item.i_item_id - all                                           48.58              28.11
statistics_tab about item.i_rec_start_date - all                                    20.88              13.00
statistics_tab about item.i_rec_end_date - all                                      16.44              12.31
statistics_tab about item.i_item_desc - all                                        147.97              97.98
statistics_tab about item.i_current_price - all                                     20.83              10.36
statistics_tab about item.i_wholesale_cost - all                                    19.00              10.43
statistics_tab about item.i_brand_id - all                                          23.42              12.85
statistics_tab about item.i_brand - all                                             20.69              10.39
statistics_tab about item.i_class_id - all                                          18.62              10.69
statistics_tab about item.i_class - all                                             16.14              10.70
statistics_tab about item.i_category_id - all                                       16.36              11.18
statistics_tab about item.i_category - all                                          16.04              10.63
statistics_tab about item.i_manufact_id - all                                       15.41              10.81
statistics_tab about item.i_manufact - all                                          14.30              10.55
statistics_tab about item.i_size - all                                              15.96              11.22
statistics_tab about item.i_formulation - all                                       53.80              35.39
statistics_tab about item.i_color - all                                             19.05              11.84
statistics_tab about item.i_units - all                                             21.18              10.74
statistics_tab about item.i_container - all                                         21.63              10.38
statistics_tab about item.i_manager_id - all                                        18.92              10.90
statistics_tab about item.i_product_name - all                                     161.76              49.93
statistics_tab about promotion.p_promo_sk - all                                     12.67               6.06
statistics_tab about promotion.p_promo_id - all                                     15.14               8.91
statistics_tab about promotion.p_start_date_sk - all                                10.18               6.65
statistics_tab about promotion.p_end_date_sk - all                                   8.94               6.43
statistics_tab about promotion.p_item_sk - all                                       7.09               6.68
statistics_tab about promotion.p_cost - all                                          8.99               7.26
statistics_tab about promotion.p_response_target - all                               8.88               7.41
statistics_tab about promotion.p_promo_name - all                                   11.16              10.59
statistics_tab about promotion.p_channel_dmail - all                                10.38               9.25
statistics_tab about promotion.p_channel_email - all                                11.13               9.36
statistics_tab about promotion.p_channel_catalog - all                              12.91               8.51
statistics_tab about promotion.p_channel_tv - all                                   14.08               9.33
statistics_tab about promotion.p_channel_radio - all                                11.84               8.84
statistics_tab about promotion.p_channel_press - all                                13.56               8.54
statistics_tab about promotion.p_channel_event - all                                14.84               8.70
statistics_tab about promotion.p_channel_demo - all                                 10.04               8.57
statistics_tab about promotion.p_channel_details - all                              10.77               8.80
statistics_tab about promotion.p_purpose - all                                       9.94               9.95
statistics_tab about promotion.p_discount_active - all                               9.48               9.97
statistics_tab about reason.r_reason_sk - all                                       13.85               7.76
statistics_tab about reason.r_reason_id - all                                       20.25               9.67
statistics_tab about reason.r_reason_desc - all                                     19.73              10.35
statistics_tab about ship_mode.sm_ship_mode_sk - all                                12.98               7.35
statistics_tab about ship_mode.sm_ship_mode_id - all                                12.71               9.49
statistics_tab about ship_mode.sm_type - all                                        12.68               9.60
statistics_tab about ship_mode.sm_code - all                                        13.33               9.13
statistics_tab about ship_mode.sm_carrier - all                                     14.18              10.23
statistics_tab about ship_mode.sm_contract - all                                    13.08               8.31
statistics_tab about store.s_store_sk - all                                          8.79               5.72
statistics_tab about store.s_store_id - all                                          9.58               9.61
statistics_tab about store.s_rec_start_date - all                                   12.06               9.51
statistics_tab about store.s_rec_end_date - all                                     14.09               9.75
statistics_tab about store.s_closed_date_sk - all                                    8.45               6.75
statistics_tab about store.s_store_name - all                                       13.82               9.62
statistics_tab about store.s_number_employees - all                                 10.69               7.32
statistics_tab about store.s_floor_space - all                                       7.65               7.77
statistics_tab about store.s_hours - all                                            10.44               9.94
statistics_tab about store.s_manager - all                                           9.57              10.63
statistics_tab about store.s_market_id - all                                         8.89               7.40
statistics_tab about store.s_geography_class - all                                  12.08               9.67
statistics_tab about store.s_market_desc - all                                      10.36               9.92
statistics_tab about store.s_market_manager - all                                    9.08               9.86
statistics_tab about store.s_division_id - all                                       7.97               7.09
statistics_tab about store.s_division_name - all                                    10.13               9.96
statistics_tab about store.s_company_id - all                                        8.41               7.43
statistics_tab about store.s_company_name - all                                     11.95              10.30
statistics_tab about store.s_street_number - all                                    10.34              12.97
statistics_tab about store.s_street_name - all                                       9.84              10.19
statistics_tab about store.s_street_type - all                                       9.29              11.02
statistics_tab about store.s_suite_number - all                                     10.38              11.17
statistics_tab about store.s_city - all                                             10.47              10.86
statistics_tab about store.s_county - all                                            9.77              10.69
statistics_tab about store.s_state - all                                            11.30              10.55
statistics_tab about store.s_zip - all                                               9.92              10.78
statistics_tab about store.s_country - all                                          11.11              10.02
statistics_tab about store.s_gmt_offset - all                                       10.44               7.03
statistics_tab about store.s_tax_precentage - all                                    7.03               6.65
statistics_tab about store_returns.sr_returned_date_sk - all                       221.94             170.60
statistics_tab about store_returns.sr_return_time_sk - all                         175.28             176.52
statistics_tab about store_returns.sr_item_sk - all                                292.41             214.39
statistics_tab about store_returns.sr_customer_sk - all                            381.19             404.67
statistics_tab about store_returns.sr_cdemo_sk - all                               597.38             697.31
statistics_tab about store_returns.sr_hdemo_sk - all                               193.71             167.67
statistics_tab about store_returns.sr_addr_sk - all                                333.81             327.89
statistics_tab about store_returns.sr_store_sk - all                               155.02             138.90
statistics_tab about store_returns.sr_reason_sk - all                              168.55             129.96
statistics_tab about store_returns.sr_ticket_number - all                          203.52             235.73
statistics_tab about store_returns.sr_return_quantity - all                        166.63             133.30
statistics_tab about store_returns.sr_return_amt - all                             303.45             462.28
statistics_tab about store_returns.sr_return_tax - all                             176.21             172.00
statistics_tab about store_returns.sr_return_amt_inc_tax - all                     633.60             324.76
statistics_tab about store_returns.sr_fee - all                                    195.71             141.18
statistics_tab about store_returns.sr_return_ship_cost - all                       290.25             291.14
statistics_tab about store_returns.sr_refunded_cash - all                          223.84             280.94
statistics_tab about store_returns.sr_reversed_charge - all                        189.52             214.79
statistics_tab about store_returns.sr_store_credit - all                           200.53             199.70
statistics_tab about store_returns.sr_net_loss - all                               268.20             278.44
statistics_tab about store_sales.ss_sold_date_sk - all                            1275.80            1314.01
statistics_tab about store_sales.ss_sold_time_sk - all                            1574.77            1708.36
statistics_tab about store_sales.ss_item_sk - all                                 2851.94            1587.37
statistics_tab about store_sales.ss_customer_sk - all                             2108.79            2000.61
statistics_tab about store_sales.ss_cdemo_sk - all                                1872.59            1968.67
statistics_tab about store_sales.ss_hdemo_sk - all                                1336.15            1449.87
statistics_tab about store_sales.ss_addr_sk - all                                 1972.91            1908.05
statistics_tab about store_sales.ss_store_sk - all                                1309.92            1300.76
statistics_tab about store_sales.ss_promo_sk - all                                1349.74            1437.32
statistics_tab about store_sales.ss_ticket_number - all                           1588.57            1503.78
statistics_tab about store_sales.ss_quantity - all                                1407.97            1701.33
statistics_tab about store_sales.ss_wholesale_cost - all                          1423.91            1417.82
statistics_tab about store_sales.ss_list_price - all                              1556.86            1469.84
statistics_tab about store_sales.ss_sales_price - all                             1654.46            1444.99
statistics_tab about store_sales.ss_ext_discount_amt - all                        2276.27            2333.78
statistics_tab about store_sales.ss_ext_sales_price - all                         4441.18            4308.21
statistics_tab about store_sales.ss_ext_wholesale_cost - all                      4589.05            4907.78
statistics_tab about store_sales.ss_ext_list_price - all                          5905.38            5746.14
statistics_tab about store_sales.ss_ext_tax - all                                 2173.78            1806.47
statistics_tab about store_sales.ss_coupon_amt - all                              2251.31            2457.38
statistics_tab about store_sales.ss_net_paid - all                                4594.97            3805.22
statistics_tab about store_sales.ss_net_paid_inc_tax - all                        4523.33            4125.82
statistics_tab about store_sales.ss_net_profit - all                              7191.67            8733.77
statistics_tab about time_dim.t_time_sk - all                                       11.65              10.31
statistics_tab about time_dim.t_time_id - all                                       12.48              12.20
statistics_tab about time_dim.t_time - all                                           9.37               9.01
statistics_tab about time_dim.t_hour - all                                           9.70               9.42
statistics_tab about time_dim.t_minute - all                                         9.06               8.61
statistics_tab about time_dim.t_second - all                                         9.09               7.80
statistics_tab about time_dim.t_am_pm - all                                         10.45               9.32
statistics_tab about time_dim.t_shift - all                                         12.98              10.68
statistics_tab about time_dim.t_sub_shift - all                                     12.41               9.12
statistics_tab about time_dim.t_meal_time - all                                     14.86              10.16
statistics_tab about warehouse.w_warehouse_sk - all                                  7.10               5.10
statistics_tab about warehouse.w_warehouse_id - all                                 10.25               6.94
statistics_tab about warehouse.w_warehouse_name - all                               11.07               7.39
statistics_tab about warehouse.w_warehouse_sq_ft - all                               7.55               4.98
statistics_tab about warehouse.w_street_number - all                                10.02               7.29
statistics_tab about warehouse.w_street_name - all                                  10.42               6.95
statistics_tab about warehouse.w_street_type - all                                  10.12               7.07
statistics_tab about warehouse.w_suite_number - all                                 10.44               7.63
statistics_tab about warehouse.w_city - all                                          9.96               7.56
statistics_tab about warehouse.w_county - all                                       10.65               7.13
statistics_tab about warehouse.w_state - all                                         7.99               7.04
statistics_tab about warehouse.w_zip - all                                           8.67               7.22
statistics_tab about warehouse.w_country - all                                       7.17               7.59
statistics_tab about warehouse.w_gmt_offset - all                                    4.54               5.72
statistics_tab about web_page.wp_web_page_sk - all                                   4.73               5.32
statistics_tab about web_page.wp_web_page_id - all                                   6.90               7.45
statistics_tab about web_page.wp_rec_start_date - all                                7.84               7.55
statistics_tab about web_page.wp_rec_end_date - all                                  7.11               7.07
statistics_tab about web_page.wp_creation_date_sk - all                              5.00               5.18
statistics_tab about web_page.wp_access_date_sk - all                                4.90               5.18
statistics_tab about web_page.wp_autogen_flag - all                                  7.48               6.72
statistics_tab about web_page.wp_customer_sk - all                                   5.25               4.86
statistics_tab about web_page.wp_url - all                                           7.09               8.85
statistics_tab about web_page.wp_type - all                                          8.22               7.98
statistics_tab about web_page.wp_char_count - all                                    5.83               5.95
statistics_tab about web_page.wp_link_count - all                                    6.03               5.65
statistics_tab about web_page.wp_image_count - all                                   4.95               5.69
statistics_tab about web_page.wp_max_ad_count - all                                  4.33               5.20
statistics_tab about web_returns.wr_returned_date_sk - all                          44.84              49.48
statistics_tab about web_returns.wr_returned_time_sk - all                          49.92              64.68
statistics_tab about web_returns.wr_item_sk - all                                   53.00              51.21
statistics_tab about web_returns.wr_refunded_customer_sk - all                      86.66             105.58
statistics_tab about web_returns.wr_refunded_cdemo_sk - all                        162.63              83.83
statistics_tab about web_returns.wr_refunded_hdemo_sk - all                         39.82              39.72
statistics_tab about web_returns.wr_refunded_addr_sk - all                          56.71              64.26
statistics_tab about web_returns.wr_returning_customer_sk - all                     78.97             100.99
statistics_tab about web_returns.wr_returning_cdemo_sk - all                       121.36             164.80
statistics_tab about web_returns.wr_returning_hdemo_sk - all                        44.40              47.77
statistics_tab about web_returns.wr_returning_addr_sk - all                         88.83              69.76
statistics_tab about web_returns.wr_web_page_sk - all                               41.54              36.15
statistics_tab about web_returns.wr_reason_sk - all                                 46.65              38.21
statistics_tab about web_returns.wr_order_number - all                              45.51              52.49
statistics_tab about web_returns.wr_return_quantity - all                           33.51              35.78
statistics_tab about web_returns.wr_return_amt - all                                91.28              95.36
statistics_tab about web_returns.wr_return_tax - all                                63.11              39.95
statistics_tab about web_returns.wr_return_amt_inc_tax - all                        80.09              93.62
statistics_tab about web_returns.wr_fee - all                                       41.40              39.97
statistics_tab about web_returns.wr_return_ship_cost - all                          75.56              74.78
statistics_tab about web_returns.wr_refunded_cash - all                             65.76              78.90
statistics_tab about web_returns.wr_reversed_charge - all                           51.01              50.65
statistics_tab about web_returns.wr_account_credit - all                            58.51              60.91
statistics_tab about web_returns.wr_net_loss - all                                  76.42              66.68
statistics_tab about web_sales.ws_sold_date_sk - all                               345.32             319.72
statistics_tab about web_sales.ws_sold_time_sk - all                               414.28             467.57
statistics_tab about web_sales.ws_ship_date_sk - all                               329.22             311.97
statistics_tab about web_sales.ws_item_sk - all                                    427.18             405.48
statistics_tab about web_sales.ws_bill_customer_sk - all                           541.67             410.20
statistics_tab about web_sales.ws_bill_cdemo_sk - all                              542.24             380.42
statistics_tab about web_sales.ws_bill_hdemo_sk - all                              345.37             324.19
statistics_tab about web_sales.ws_bill_addr_sk - all                               409.88             508.00
statistics_tab about web_sales.ws_ship_customer_sk - all                           469.84             475.88
statistics_tab about web_sales.ws_ship_cdemo_sk - all                              420.73             481.71
statistics_tab about web_sales.ws_ship_hdemo_sk - all                              330.87             338.34
statistics_tab about web_sales.ws_ship_addr_sk - all                               453.07             376.72
statistics_tab about web_sales.ws_web_page_sk - all                                340.00             346.17
statistics_tab about web_sales.ws_web_site_sk - all                                329.84             331.59
statistics_tab about web_sales.ws_ship_mode_sk - all                               297.49             325.19
statistics_tab about web_sales.ws_warehouse_sk - all                               361.66             323.05
statistics_tab about web_sales.ws_promo_sk - all                                   325.50             342.75
statistics_tab about web_sales.ws_order_number - all                               251.30             290.92
statistics_tab about web_sales.ws_quantity - all                                   325.50             368.17
statistics_tab about web_sales.ws_wholesale_cost - all                             388.35             374.82
statistics_tab about web_sales.ws_list_price - all                                 363.43             386.59
statistics_tab about web_sales.ws_sales_price - all                                371.06             378.39
statistics_tab about web_sales.ws_ext_discount_amt - all                           922.20            1240.19
statistics_tab about web_sales.ws_ext_sales_price - all                           1157.08            1360.66
statistics_tab about web_sales.ws_ext_wholesale_cost - all                         756.89            1107.38
statistics_tab about web_sales.ws_ext_list_price - all                            1589.28            2249.21
statistics_tab about web_sales.ws_ext_tax - all                                    443.88             515.63
statistics_tab about web_sales.ws_coupon_amt - all                                 452.73             536.02
statistics_tab about web_sales.ws_ext_ship_cost - all                              688.08             754.97
statistics_tab about web_sales.ws_net_paid - all                                   932.33            1214.39
statistics_tab about web_sales.ws_net_paid_inc_tax - all                           961.52            1335.91
statistics_tab about web_sales.ws_net_paid_inc_ship - all                         1363.99            1093.89
statistics_tab about web_sales.ws_net_paid_inc_ship_tax - all                     1291.55            1545.16
statistics_tab about web_sales.ws_net_profit - all                                2151.42            1677.42
statistics_tab about web_site.web_site_sk - all                                      6.86               6.52
statistics_tab about web_site.web_site_id - all                                     11.92               9.12
statistics_tab about web_site.web_rec_start_date - all                              10.92               8.33
statistics_tab about web_site.web_rec_end_date - all                                11.05               7.13
statistics_tab about web_site.web_name - all                                         7.81               8.36
statistics_tab about web_site.web_open_date_sk - all                                 6.36               5.43
statistics_tab about web_site.web_close_date_sk - all                                5.49               4.92
statistics_tab about web_site.web_class - all                                        9.46               8.43
statistics_tab about web_site.web_manager - all                                     10.06               7.69
statistics_tab about web_site.web_mkt_id - all                                       5.25               6.71
statistics_tab about web_site.web_mkt_class - all                                    8.25               8.34
statistics_tab about web_site.web_mkt_desc - all                                     9.35               8.49
statistics_tab about web_site.web_market_manager - all                               8.52               8.84
statistics_tab about web_site.web_company_id - all                                   5.94               5.57
statistics_tab about web_site.web_company_name - all                                 7.82               8.08
statistics_tab about web_site.web_street_number - all                                8.56               8.74
statistics_tab about web_site.web_street_name - all                                 17.02               8.17
statistics_tab about web_site.web_street_type - all                                  7.47               7.82
statistics_tab about web_site.web_suite_number - all                                 7.87               8.21
statistics_tab about web_site.web_city - all                                         9.01               7.79
statistics_tab about web_site.web_county - all                                       9.68               8.84
statistics_tab about web_site.web_state - all                                        8.77               8.61
statistics_tab about web_site.web_zip - all                                          7.46               9.01
statistics_tab about web_site.web_country - all                                      7.08               8.76
statistics_tab about web_site.web_gmt_offset - all                                   5.38               6.33
statistics_tab about web_site.web_tax_percentage - all                               6.14               5.78

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           0.0          360.0         8.0     1177.0    1553.0
MonetDB-BHT-8-2-1           0.0          360.0         8.0     1177.0    1553.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.04
MonetDB-BHT-8-2-1           0.04

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1          808893.57
MonetDB-BHT-8-2-1          843736.40

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                time [s]  count    SF  Throughput@Size
DBMS            SF   num_experiment num_client                                        
MonetDB-BHT-8-1 10.0 1              1                196      1  10.0         78795.92
MonetDB-BHT-8-2 10.0 1              2                219      1  10.0         70520.55

### Workflow
                         orig_name    SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  10.0     8               1           1       1764435012     1764435208
MonetDB-BHT-8-2-1  MonetDB-BHT-8-2  10.0     8               1           2       1764435287     1764435506

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1]]

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      128.46     0.88          0.01                 2.82
MonetDB-BHT-8-2      128.46     0.88          0.01                 2.82

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      368.45     2.62         17.17                47.81
MonetDB-BHT-8-2      445.59     2.91         17.53                45.64

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       19.26     0.24          0.25                 0.25
MonetDB-BHT-8-2       19.26     0.10          0.25                 0.26

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

