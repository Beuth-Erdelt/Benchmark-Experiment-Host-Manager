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
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_compare.log &
```

This
* starts a clean instance of PostgreSQL, MonetDB, MySQL and MariaDB (one after the other, `-ms`)
  * fixed 64 Gi RAM (request `-rr` and limit `-rl`)
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
    Duration: 7813s 
    Code: 1766231382
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
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
    disk:437111
    cpu_list:0-63
    args:['--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766231382
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:437963
    cpu_list:0-63
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766231382
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008486400
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:470775
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766231382
PostgreSQL-BHT-8-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:437782
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766231382

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1  MonetDB-BHT-8-1-1  MySQL-BHT-64-1-1  PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             25801.04            1210.83          30153.67               2622.38
Minimum Cost Supplier Query (TPC-H Q2)                         1366.41              33.92            363.49                466.68
Shipping Priority (TPC-H Q3)                                   7925.11             174.80           4494.12                902.45
Order Priority Checking Query (TPC-H Q4)                       3374.20             165.98           1656.18                392.31
Local Supplier Volume (TPC-H Q5)                               7443.77             101.20           4142.92                797.35
Forecasting Revenue Change (TPC-H Q6)                          4749.10              39.80           4294.22                625.62
Forecasting Revenue Change (TPC-H Q7)                          6502.67             180.81           5842.28                900.11
National Market Share (TPC-H Q8)                              12880.07             700.23           9425.13                502.65
Product Type Profit Measure (TPC-H Q9)                        11944.80             133.60           6837.69               1177.04
Forecasting Revenue Change (TPC-H Q10)                         3365.03             224.30           4055.67               1083.85
Important Stock Identification (TPC-H Q11)                      369.58              40.68            448.91                172.17
Shipping Modes and Order Priority (TPC-H Q12)                 10896.50              90.20           6615.59                972.20
Customer Distribution (TPC-H Q13)                             14728.79             724.81          13439.29               2256.01
Forecasting Revenue Change (TPC-H Q14)                        30369.09              67.83           5217.79                968.63
Top Supplier Query (TPC-H Q15)                                 6414.62              56.79          47100.59                736.65
Parts/Supplier Relationship (TPC-H Q16)                         667.55             121.70           1076.59                642.23
Small-Quantity-Order Revenue (TPC-H Q17)                        153.21              97.14           1343.36               2244.13
Large Volume Customer (TPC-H Q18)                             10053.47             340.72           6156.23               7018.70
Discounted Revenue (TPC-H Q19)                                  260.11             143.24            424.28                127.15
Potential Part Promotion (TPC-H Q20)                            524.54              97.81            865.60                300.44
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          245802.21            3995.89          19010.21                796.87
Global Sales Opportunity Query (TPC-H Q22)                      447.66              76.58            503.85                218.34

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1             28.0          384.0         3.0     2370.0    2788.0
MonetDB-BHT-8-1-1             27.0           24.0        17.0      180.0     253.0
MySQL-BHT-64-1-1              22.0          292.0         5.0     2977.0    3300.0
PostgreSQL-BHT-8-1-1          18.0           42.0         2.0      193.0     259.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
MariaDB-BHT-8-1-1              4.13
MonetDB-BHT-8-1-1              0.18
MySQL-BHT-64-1-1               3.54
PostgreSQL-BHT-8-1-1           0.79

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
MariaDB-BHT-8-1-1                894.74
MonetDB-BHT-8-1-1              22458.62
MySQL-BHT-64-1-1                1043.37
PostgreSQL-BHT-8-1-1            4748.66

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
MariaDB-BHT-8-1    1.0 1              1                411      1  1.0           192.70
MonetDB-BHT-8-1    1.0 1              1                 13      1  1.0          6092.31
MySQL-BHT-64-1     1.0 1              1                180      1  1.0           440.00
PostgreSQL-BHT-8-1 1.0 1              1                 33      1  1.0          2400.00

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MariaDB-BHT-8-1-1        MariaDB-BHT-8-1  1.0     8               1           1       1766235026     1766235437
MonetDB-BHT-8-1-1        MonetDB-BHT-8-1  1.0     8               1           1       1766232310     1766232323
MySQL-BHT-64-1-1          MySQL-BHT-64-1  1.0     8               1           1       1766238954     1766239134
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  1.0     8               1           1       1766231805     1766231838

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
  -rr 64Gi -lr 64Gi \
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
    Duration: 1824s 
    Code: 1766137093
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.19.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:462228
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1766137093

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                15949.47
Minimum Cost Supplier Query (TPC-H Q2)                            5714.23
Shipping Priority (TPC-H Q3)                                      5347.69
Order Priority Checking Query (TPC-H Q4)                          2263.14
Local Supplier Volume (TPC-H Q5)                                  5389.56
Forecasting Revenue Change (TPC-H Q6)                             3219.39
Forecasting Revenue Change (TPC-H Q7)                             5106.66
National Market Share (TPC-H Q8)                                  4017.21
Product Type Profit Measure (TPC-H Q9)                           12731.60
Forecasting Revenue Change (TPC-H Q10)                            4956.50
Important Stock Identification (TPC-H Q11)                        1624.97
Shipping Modes and Order Priority (TPC-H Q12)                     4285.67
Customer Distribution (TPC-H Q13)                                20994.08
Forecasting Revenue Change (TPC-H Q14)                            5559.70
Top Supplier Query (TPC-H Q15)                                    3770.76
Parts/Supplier Relationship (TPC-H Q16)                           3521.06
Small-Quantity-Order Revenue (TPC-H Q17)                         19713.81
Large Volume Customer (TPC-H Q18)                                38023.69
Discounted Revenue (TPC-H Q19)                                     616.70
Potential Part Promotion (TPC-H Q20)                              7193.82
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               5327.75
Global Sales Opportunity Query (TPC-H Q22)                        1051.43

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1          21.0          531.0         1.0     1364.0    1923.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           5.26

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            6962.86

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                   time [s]  count    SF  Throughput@Size
DBMS               SF   num_experiment num_client                                        
PostgreSQL-BHT-8-1 10.0 1              1                183      1  10.0          4327.87

### Workflow
                               orig_name    SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  10.0     8               1           1       1766138659     1766138842

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      117.34     0.47          0.01                  1.3

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       599.0     4.29         27.43                42.71

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        17.3     0.23          0.35                 0.35

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
    Duration: 666s 
    Code: 1766128526
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.19.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:437775
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766128526
PostgreSQL-BHT-8-2-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:437775
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766128526
PostgreSQL-BHT-8-2-2 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:437775
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766128526

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-2-1  PostgreSQL-BHT-8-2-2
Pricing Summary Report (TPC-H Q1)                                 2424.11               2815.97               2749.06
Minimum Cost Supplier Query (TPC-H Q2)                             448.94                552.38                510.30
Shipping Priority (TPC-H Q3)                                       727.00               1025.86                824.63
Order Priority Checking Query (TPC-H Q4)                           355.46                505.06                435.54
Local Supplier Volume (TPC-H Q5)                                   686.60                844.11                747.23
Forecasting Revenue Change (TPC-H Q6)                              471.50                621.36                592.07
Forecasting Revenue Change (TPC-H Q7)                              759.00                956.53                922.68
National Market Share (TPC-H Q8)                                   419.45                645.83                502.83
Product Type Profit Measure (TPC-H Q9)                            1487.61               1867.20               1944.09
Forecasting Revenue Change (TPC-H Q10)                            1178.45               1410.65               1386.52
Important Stock Identification (TPC-H Q11)                         182.43                249.98                224.79
Shipping Modes and Order Priority (TPC-H Q12)                      683.20                877.40                916.91
Customer Distribution (TPC-H Q13)                                 2081.67               2816.47               2291.90
Forecasting Revenue Change (TPC-H Q14)                             854.24                987.07                976.41
Top Supplier Query (TPC-H Q15)                                     522.77                707.89                743.47
Parts/Supplier Relationship (TPC-H Q16)                            571.80                637.07                676.49
Small-Quantity-Order Revenue (TPC-H Q17)                          2147.63               2415.30               2337.38
Large Volume Customer (TPC-H Q18)                                 5476.44               5753.87               7135.67
Discounted Revenue (TPC-H Q19)                                     120.64                122.43                118.99
Potential Part Promotion (TPC-H Q20)                               292.46                289.25                290.87
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                775.51                762.18                765.43
Global Sales Opportunity Query (TPC-H Q22)                         225.48                217.42                215.26

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1          27.0           47.0         2.0      226.0     308.0
PostgreSQL-BHT-8-2-1          27.0           47.0         2.0      226.0     308.0
PostgreSQL-BHT-8-2-2          27.0           47.0         2.0      226.0     308.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           0.71
PostgreSQL-BHT-8-2-1           0.85
PostgreSQL-BHT-8-2-2           0.82

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            5254.00
PostgreSQL-BHT-8-2-1            4351.66
PostgreSQL-BHT-8-2-2            4537.39

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1 1.0 1              1                 29      1  1.0          2731.03
PostgreSQL-BHT-8-2 1.0 1              2                 32      2  1.0          4950.00

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  1.0     8               1           1       1766128983     1766129012
PostgreSQL-BHT-8-2-1  PostgreSQL-BHT-8-2  1.0     8               1           2       1766129096     1766129128
PostgreSQL-BHT-8-2-2  PostgreSQL-BHT-8-2  1.0     8               1           2       1766129096     1766129128

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
    Duration: 917s 
    Code: 1766129231
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.19.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:435020
    volume_size:30G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766129231
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:435020
    volume_size:30G
    volume_used:2.7G
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766129231

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-2-1-1
Pricing Summary Report (TPC-H Q1)                                   2425.30                17549.82
Minimum Cost Supplier Query (TPC-H Q2)                               446.27                 5109.61
Shipping Priority (TPC-H Q3)                                         727.58                 7567.22
Order Priority Checking Query (TPC-H Q4)                             356.53                  383.60
Local Supplier Volume (TPC-H Q5)                                     650.61                  740.23
Forecasting Revenue Change (TPC-H Q6)                                476.77                  471.31
Forecasting Revenue Change (TPC-H Q7)                                749.83                  753.62
National Market Share (TPC-H Q8)                                     427.31                 1578.68
Product Type Profit Measure (TPC-H Q9)                              1098.29                 1147.91
Forecasting Revenue Change (TPC-H Q10)                              1338.92                 1171.35
Important Stock Identification (TPC-H Q11)                           170.74                  156.54
Shipping Modes and Order Priority (TPC-H Q12)                        693.97                  720.46
Customer Distribution (TPC-H Q13)                                   2158.90                 2350.44
Forecasting Revenue Change (TPC-H Q14)                               522.19                  516.76
Top Supplier Query (TPC-H Q15)                                       516.55                  505.84
Parts/Supplier Relationship (TPC-H Q16)                              598.33                  585.78
Small-Quantity-Order Revenue (TPC-H Q17)                            2209.16                 2154.79
Large Volume Customer (TPC-H Q18)                                   6418.01                 5726.80
Discounted Revenue (TPC-H Q19)                                       140.57                  135.97
Potential Part Promotion (TPC-H Q20)                                 298.11                  317.22
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  840.33                  774.80
Global Sales Opportunity Query (TPC-H Q22)                           253.37                  219.39

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1          26.0           36.0         3.0      223.0     293.0
PostgreSQL-BHT-8-2-1-1          26.0           36.0         3.0      223.0     293.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           0.72
PostgreSQL-BHT-8-2-1-1           1.01

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            5285.35
PostgreSQL-BHT-8-2-1-1            3704.30

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1-1 1.0 1              1                 28      1  1.0          2828.57
PostgreSQL-BHT-8-2-1 1.0 2              1                 56      1  1.0          1414.29

### Workflow
                                   orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-1  1.0     8               1           1       1766129699     1766129727
PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-1  1.0     8               2           1       1766130027     1766130083

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


## Fractional Scaling Factor

TPC-H supports scaling factors that are fractional.
Example: SF=0.1

```bash
nohup python tpch.py -ms 1 -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 0.1 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 5Gi -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_fractional.log &
```

results in

doc_tpch_testcase_fractional.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=0.1
    Type: tpch
    Duration: 907s 
    Code: 1766139002
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=0.1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.19.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 5Gi. Persistent storage is removed at experiment start.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:435020
    volume_size:5.0G
    volume_used:312M
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766139002
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:435020
    volume_size:5.0G
    volume_used:312M
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766139002

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-2-1-1
Pricing Summary Report (TPC-H Q1)                                    425.07                 2807.33
Minimum Cost Supplier Query (TPC-H Q2)                                60.90                 1119.80
Shipping Priority (TPC-H Q3)                                         160.96                 1215.43
Order Priority Checking Query (TPC-H Q4)                             240.48                  245.98
Local Supplier Volume (TPC-H Q5)                                      83.62                   79.66
Forecasting Revenue Change (TPC-H Q6)                                 87.05                   84.67
Forecasting Revenue Change (TPC-H Q7)                                113.80                  112.01
National Market Share (TPC-H Q8)                                     109.37                  275.47
Product Type Profit Measure (TPC-H Q9)                               213.32                  210.92
Forecasting Revenue Change (TPC-H Q10)                               137.85                  133.27
Important Stock Identification (TPC-H Q11)                            15.27                   16.55
Shipping Modes and Order Priority (TPC-H Q12)                        123.24                  133.82
Customer Distribution (TPC-H Q13)                                    221.55                  175.75
Forecasting Revenue Change (TPC-H Q14)                                98.15                   92.95
Top Supplier Query (TPC-H Q15)                                        97.81                   95.95
Parts/Supplier Relationship (TPC-H Q16)                              128.76                  115.74
Small-Quantity-Order Revenue (TPC-H Q17)                             203.55                  182.98
Large Volume Customer (TPC-H Q18)                                    497.12                  491.97
Discounted Revenue (TPC-H Q19)                                        16.76                   17.37
Potential Part Promotion (TPC-H Q20)                                  27.47                   30.52
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  124.79                  123.58
Global Sales Opportunity Query (TPC-H Q22)                            33.26                   34.21

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1          19.0            5.0         2.0      149.0     181.0
PostgreSQL-BHT-8-2-1-1          19.0            5.0         2.0      149.0     181.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           0.11
PostgreSQL-BHT-8-2-1-1           0.15

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            3443.40
PostgreSQL-BHT-8-2-1-1            2457.16

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1-1 0.1 1              1                  4      1  0.1           1980.0
PostgreSQL-BHT-8-2-1 0.1 2              1                 10      1  0.1            792.0

### Workflow
                                   orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-1  0.1     8               1           1       1766139498     1766139502
PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-1  0.1     8               2           1       1766139826     1766139836

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
    Duration: 11744s 
    Code: 1764069062
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 3600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.15.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 1000Gi. Persistent storage is removed at experiment start.
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
    disk:420885
    datadisk:213090
    volume_size:1000G
    volume_used:209G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764069062

### Errors (failed queries)
                                MonetDB-BHT-8-1-1
Discounted Revenue (TPC-H Q19)               True
Discounted Revenue (TPC-H Q19)
MonetDB-BHT-8-1-1: numRun 1: : java.sql.SQLException: Query aborted due to timeout

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                            248845.50
Minimum Cost Supplier Query (TPC-H Q2)                         2414.29
Shipping Priority (TPC-H Q3)                                  13550.74
Order Priority Checking Query (TPC-H Q4)                      14804.17
Local Supplier Volume (TPC-H Q5)                              10460.44
Forecasting Revenue Change (TPC-H Q6)                          7633.96
Forecasting Revenue Change (TPC-H Q7)                         10390.25
National Market Share (TPC-H Q8)                              71922.34
Product Type Profit Measure (TPC-H Q9)                        17534.50
Forecasting Revenue Change (TPC-H Q10)                        29790.61
Important Stock Identification (TPC-H Q11)                     1312.80
Shipping Modes and Order Priority (TPC-H Q12)                  4890.64
Customer Distribution (TPC-H Q13)                            119351.04
Forecasting Revenue Change (TPC-H Q14)                         8212.25
Top Supplier Query (TPC-H Q15)                                 9945.37
Parts/Supplier Relationship (TPC-H Q16)                       12487.65
Small-Quantity-Order Revenue (TPC-H Q17)                      15866.47
Large Volume Customer (TPC-H Q18)                             19466.52
Potential Part Promotion (TPC-H Q20)                          65424.08
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           26578.08
Global Sales Opportunity Query (TPC-H Q22)                    14033.20

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1          17.0         1654.0        11.0     7193.0    8879.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          16.92

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           22356.26

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                 time [s]  count     SF  Throughput@Size
DBMS            SF    num_experiment num_client                                         
MonetDB-BHT-8-1 100.0 1              1               4380      1  100.0          1726.03

### Workflow
                         orig_name     SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  100.0     8               1           1       1764076366     1764080746

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     1283.86     1.15          0.04                13.29

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    17938.22    37.21        137.34                256.0

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       30.18     0.13          0.32                 0.33

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
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
    Duration: 5296s 
    Code: 1764081005
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 3600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.15.
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
    disk:420885
    datadisk:218011
    volume_size:1000G
    volume_used:213G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764081005
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:420885
    datadisk:214825
    volume_size:1000G
    volume_used:215G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764081005
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:420885
    datadisk:214825
    volume_size:1000G
    volume_used:210G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764081005
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:420884
    datadisk:214825
    volume_size:1000G
    volume_used:215G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764081005

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
Pricing Summary Report (TPC-H Q1)                              564910.54            263481.03            589081.92            264379.57
Minimum Cost Supplier Query (TPC-H Q2)                          34413.05              4921.86             30088.80              9888.09
Shipping Priority (TPC-H Q3)                                    88154.82             13410.10             88526.51             12597.86
Order Priority Checking Query (TPC-H Q4)                       293573.48             13356.59            306226.47             15242.48
Local Supplier Volume (TPC-H Q5)                                12827.12             10208.18             13972.07             10198.56
Forecasting Revenue Change (TPC-H Q6)                            6719.28              6380.97              6347.75              5003.06
Forecasting Revenue Change (TPC-H Q7)                            8885.74              5554.95              8113.32              3468.27
National Market Share (TPC-H Q8)                                98153.80             37336.12            111622.19             30907.54
Product Type Profit Measure (TPC-H Q9)                          28676.99             16764.13             30067.54             16593.83
Forecasting Revenue Change (TPC-H Q10)                          66017.03             27345.10             66667.78             27267.16
Important Stock Identification (TPC-H Q11)                       7096.50              1387.89              6100.56              1233.97
Shipping Modes and Order Priority (TPC-H Q12)                    4808.32              4766.30              4605.43              4683.93
Customer Distribution (TPC-H Q13)                              281615.20            106839.44            292939.89            101862.48
Forecasting Revenue Change (TPC-H Q14)                           8308.94              7919.26              8513.54              8169.44
Top Supplier Query (TPC-H Q15)                                  10251.22              6067.61              5633.20              9679.96
Parts/Supplier Relationship (TPC-H Q16)                         12823.52             11596.93             12634.11             11730.34
Small-Quantity-Order Revenue (TPC-H Q17)                        52635.23             15074.87             53038.41             16263.07
Large Volume Customer (TPC-H Q18)                               36915.61             21109.61             38444.27             20198.17
Discounted Revenue (TPC-H Q19)                                   7046.59              6395.70              6900.75             30245.41
Potential Part Promotion (TPC-H Q20)                             7598.14              4288.36              9251.04              5597.55
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)             22746.50             18965.79             25265.60             18080.00
Global Sales Opportunity Query (TPC-H Q22)                       6561.36              6238.40              6411.75              6503.64

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1          17.0         1654.0        11.0     7193.0    8879.0
MonetDB-BHT-8-1-2-1          17.0         1654.0        11.0     7193.0    8879.0
MonetDB-BHT-8-2-1-1          17.0         1654.0        11.0     7193.0    8879.0
MonetDB-BHT-8-2-2-1          17.0         1654.0        11.0     7193.0    8879.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1          26.28
MonetDB-BHT-8-1-2-1          12.65
MonetDB-BHT-8-2-1-1          25.90
MonetDB-BHT-8-2-2-1          13.92

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           13936.88
MonetDB-BHT-8-1-2-1           29920.99
MonetDB-BHT-8-2-1-1           14167.23
MonetDB-BHT-8-2-2-1           27288.61

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                   time [s]  count     SF  Throughput@Size
DBMS              SF    num_experiment num_client                                         
MonetDB-BHT-8-1-1 100.0 1              1               1686      1  100.0          4697.51
MonetDB-BHT-8-1-2 100.0 1              2                627      1  100.0         12631.58
MonetDB-BHT-8-2-1 100.0 2              1               1745      1  100.0          4538.68
MonetDB-BHT-8-2-2 100.0 2              2                649      1  100.0         12203.39

### Workflow
                             orig_name     SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-1  100.0     8               1           1       1764081115     1764082801
MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-1-2  100.0     8               1           2       1764082870     1764083497
MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-1  100.0     8               2           1       1764083747     1764085492
MonetDB-BHT-8-2-2-1  MonetDB-BHT-8-2-2  100.0     8               2           2       1764085576     1764086225

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1     7704.62    26.52         60.11               107.97
MonetDB-BHT-8-1-2     5180.21    27.04         98.66               182.17
MonetDB-BHT-8-2-1    14562.91    26.48         96.41               115.32
MonetDB-BHT-8-2-2     6534.63    28.65         95.92               180.29

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       23.82     0.08          0.31                 0.32
MonetDB-BHT-8-1-2       23.82     0.12          0.31                 0.32
MonetDB-BHT-8-2-1       27.09     0.10          0.32                 0.33
MonetDB-BHT-8-2-2       26.36     0.19          0.32                 0.33

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
    Duration: 3721s 
    Code: 1764245999
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 3600.
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
    Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:420892
    datadisk:214825
    volume_size:1000G
    volume_used:210G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764245999
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:420892
    datadisk:214825
    volume_size:1000G
    volume_used:215G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764245999
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:420892
    datadisk:214825
    volume_size:1000G
    volume_used:210G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764245999
MonetDB-BHT-8-3-2 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:420892
    datadisk:214825
    volume_size:1000G
    volume_used:210G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764245999
MonetDB-BHT-8-3-3 uses docker image monetdb/monetdb:Mar2025
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:420892
    datadisk:214825
    volume_size:1000G
    volume_used:210G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:256Gi
    limits_memory:256Gi
    eval_parameters
        code:1764245999

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
Pricing Summary Report (TPC-H Q1)                            572039.47          255207.17          509168.41          505326.23          498909.74
Minimum Cost Supplier Query (TPC-H Q2)                        30268.95           11094.24           16501.43           20397.91           26218.52
Shipping Priority (TPC-H Q3)                                  84225.45           13685.24           31426.72           32663.00           30795.34
Order Priority Checking Query (TPC-H Q4)                     282408.27           13806.58           23831.19           24449.57           24483.18
Local Supplier Volume (TPC-H Q5)                              14416.21           10700.94           15652.76           13695.28           15520.60
Forecasting Revenue Change (TPC-H Q6)                          6850.36            6998.22            8067.89            8122.54            8087.37
Forecasting Revenue Change (TPC-H Q7)                          8223.70            5977.03           14384.42           13058.83           12794.40
National Market Share (TPC-H Q8)                              90389.99           36421.67           47260.15           48558.01           47703.13
Product Type Profit Measure (TPC-H Q9)                        28767.57           14662.66           27779.30           26462.56           27835.34
Forecasting Revenue Change (TPC-H Q10)                        62386.19           22628.32           34007.12           33367.77           35317.27
Important Stock Identification (TPC-H Q11)                     5910.12            1187.33            1171.19            3143.58             932.31
Shipping Modes and Order Priority (TPC-H Q12)                  5890.49            4720.47            8391.76            8608.96            8400.16
Customer Distribution (TPC-H Q13)                            264559.04          100853.60          111680.99          123142.51          127995.02
Forecasting Revenue Change (TPC-H Q14)                         9211.93            7381.95            8327.66             645.15             989.07
Top Supplier Query (TPC-H Q15)                                10053.06            6443.23            8473.57            5289.03            5336.34
Parts/Supplier Relationship (TPC-H Q16)                       12904.93           12095.87           12718.55           12329.56           11997.62
Small-Quantity-Order Revenue (TPC-H Q17)                      51153.18           14088.99           95864.52           96131.02           91302.47
Large Volume Customer (TPC-H Q18)                             43891.23           21421.92           37014.57           36678.93           35789.28
Discounted Revenue (TPC-H Q19)                                 7001.95            7749.74           10696.45           11005.48           11320.08
Potential Part Promotion (TPC-H Q20)                           8786.27            5292.32            6816.10            6878.47            6841.78
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           21009.96           19239.45           50461.66           55552.98           51126.66
Global Sales Opportunity Query (TPC-H Q22)                     7607.57            7373.05            8056.91            6422.94            8612.33

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1          17.0         1654.0        11.0     7193.0    8879.0
MonetDB-BHT-8-2-1          17.0         1654.0        11.0     7193.0    8879.0
MonetDB-BHT-8-3-1          17.0         1654.0        11.0     7193.0    8879.0
MonetDB-BHT-8-3-2          17.0         1654.0        11.0     7193.0    8879.0
MonetDB-BHT-8-3-3          17.0         1654.0        11.0     7193.0    8879.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          26.46
MonetDB-BHT-8-2-1          13.31
MonetDB-BHT-8-3-1          21.37
MonetDB-BHT-8-3-2          19.03
MonetDB-BHT-8-3-3          19.36

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           13859.65
MonetDB-BHT-8-2-1           28541.64
MonetDB-BHT-8-3-1           17811.43
MonetDB-BHT-8-3-2           19545.84
MonetDB-BHT-8-3-3           19782.48

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                 time [s]  count     SF  Throughput@Size
DBMS            SF    num_experiment num_client                                         
MonetDB-BHT-8-1 100.0 1              1               1653      1  100.0          4791.29
MonetDB-BHT-8-2 100.0 1              2                617      1  100.0         12836.30
MonetDB-BHT-8-3 100.0 1              3               1110      3  100.0         21405.41

### Workflow
                         orig_name     SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  100.0     8               1           1       1764246113     1764247766
MonetDB-BHT-8-2-1  MonetDB-BHT-8-2  100.0     8               1           2       1764247839     1764248456
MonetDB-BHT-8-3-1  MonetDB-BHT-8-3  100.0     8               1           3       1764248544     1764249650
MonetDB-BHT-8-3-2  MonetDB-BHT-8-3  100.0     8               1           3       1764248544     1764249654
MonetDB-BHT-8-3-3  MonetDB-BHT-8-3  100.0     8               1           3       1764248544     1764249651

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     6449.32    23.90         51.69               104.45
MonetDB-BHT-8-2     4940.70    25.88         85.20               177.94
MonetDB-BHT-8-3    13964.50    42.01        130.70               256.00

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       28.66     0.12          0.32                 0.33
MonetDB-BHT-8-2       28.66     0.11          0.32                 0.33
MonetDB-BHT-8-3       60.66     0.41          0.33                 0.34

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

The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.

