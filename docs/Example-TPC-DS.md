# Benchmark: TPC-DS

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TPC-DS does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients for the loading test and the throughput test [2].

This example shows how to benchmark 99 reading queries Q1-Q99 derived from TPC-DS in PostgreSQL.

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

For a comparison of multiple DBMS (PostgreSQL, MonetDB, MySQL, MariaDB) see [TestCases.md](TestCases.md#tpc-ds).

1. Official TPC-DS benchmark - http://www.tpc.org/tpcds
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Perform Benchmark - Power Test

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

Example:
```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql.log
```

This
* starts a clean instance of PostgreSQL
  * fixed 64 Gi RAM (request `-rr` and limit `-lr`)
  * data directory inside a Docker container
* creates TPC-DS schema in the database
* starts 8 loader pods (`-nlp`)
  * with a data generator (init) container each
    * generating a portion of TPC-DS data of scaling factor 1 (`-sf`)
    * storing the data in a distributed filesystem (shared disk)
    * if data is already present: do nothing
  * with a loading container each
    * importing TPC-DS data from the distributed filesystem
    * loading uses 8 threads (`-nlt`)
* creates constraints (`-xic`) and indexes (`-xii`) and updates table statistics (`-xis`) after ingestion
* runs 1 stream of TPC-DS queries
  * data transfer is also measured (`-xdt`)
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

docs_tpcds_postgresql.log
```markdown
﻿## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 709s 
* Code: 1782066626
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222221
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782066626

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      246.00 |           1.00 |            1.00 |         56.00 |          177.00 |              8 |           0 |             | None           |             0 | False         |               14.63 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        215 |            0.41 |             9022.65 |           1657.67 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        215 |            0.41 |             9022.65 |           1657.67 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 137.92 |
| TPC-DS Q2     |                 323.34 |
| TPC-DS Q3     |                 223.21 |
| TPC-DS Q4     |               12569.39 |
| TPC-DS Q5     |                 589.96 |
| TPC-DS Q6     |               68802.30 |
| TPC-DS Q7     |                 361.33 |
| TPC-DS Q8     |                  74.10 |
| TPC-DS Q9     |                2613.06 |
| TPC-DS Q10    |                1303.97 |
| TPC-DS Q11    |                6453.03 |
| TPC-DS Q12    |                  79.18 |
| TPC-DS Q13    |                 828.35 |
| TPC-DS Q14a+b |                2448.08 |
| TPC-DS Q15    |                 124.29 |
| TPC-DS Q16    |                 189.29 |
| TPC-DS Q17    |                 303.34 |
| TPC-DS Q18    |                 379.35 |
| TPC-DS Q19    |                 158.96 |
| TPC-DS Q20    |                 110.73 |
| TPC-DS Q21    |                 225.06 |
| TPC-DS Q22    |                3140.25 |
| TPC-DS Q23a+b |                5332.70 |
| TPC-DS Q24a+b |                 914.64 |
| TPC-DS Q25    |                 351.26 |
| TPC-DS Q26    |                 269.28 |
| TPC-DS Q27    |                  33.86 |
| TPC-DS Q28    |                 823.70 |
| TPC-DS Q29    |                 371.84 |
| TPC-DS Q30    |                8555.63 |
| TPC-DS Q31    |                1540.38 |
| TPC-DS Q32    |                 136.67 |
| TPC-DS Q33    |                 437.99 |
| TPC-DS Q34    |                  43.53 |
| TPC-DS Q35    |                1675.24 |
| TPC-DS Q36    |                  37.28 |
| TPC-DS Q37    |                 527.03 |
| TPC-DS Q38    |                1708.67 |
| TPC-DS Q39a+b |                2702.48 |
| TPC-DS Q40    |                 119.76 |
| TPC-DS Q41    |                 985.82 |
| TPC-DS Q42    |                  95.58 |
| TPC-DS Q43    |                  33.36 |
| TPC-DS Q44    |                 483.61 |
| TPC-DS Q45    |                 103.09 |
| TPC-DS Q46    |                  49.11 |
| TPC-DS Q47    |                1707.06 |
| TPC-DS Q48    |                 671.40 |
| TPC-DS Q49    |                 491.40 |
| TPC-DS Q50    |                 509.69 |
| TPC-DS Q51    |                 831.34 |
| TPC-DS Q52    |                  98.64 |
| TPC-DS Q53    |                 120.65 |
| TPC-DS Q54    |                 300.62 |
| TPC-DS Q55    |                  93.59 |
| TPC-DS Q56    |                 437.00 |
| TPC-DS Q57    |                 808.18 |
| TPC-DS Q58    |                 498.78 |
| TPC-DS Q59    |                 429.05 |
| TPC-DS Q60    |                 397.35 |
| TPC-DS Q61    |                 147.66 |
| TPC-DS Q62    |                 139.81 |
| TPC-DS Q63    |                 118.65 |
| TPC-DS Q64    |                 807.32 |
| TPC-DS Q65    |                 606.55 |
| TPC-DS Q66    |                 244.09 |
| TPC-DS Q67    |                2951.08 |
| TPC-DS Q68    |                  48.16 |
| TPC-DS Q69    |                 127.60 |
| TPC-DS Q70    |                 380.18 |
| TPC-DS Q71    |                 305.68 |
| TPC-DS Q72    |                 906.85 |
| TPC-DS Q73    |                  33.97 |
| TPC-DS Q74    |                1389.26 |
| TPC-DS Q75    |                 999.60 |
| TPC-DS Q76    |                 165.17 |
| TPC-DS Q77    |                 414.44 |
| TPC-DS Q78    |                2298.00 |
| TPC-DS Q79    |                 258.29 |
| TPC-DS Q80    |                 573.87 |
| TPC-DS Q81    |               39195.32 |
| TPC-DS Q82    |                 358.69 |
| TPC-DS Q83    |                 100.76 |
| TPC-DS Q84    |                  36.53 |
| TPC-DS Q85    |                 352.59 |
| TPC-DS Q86    |                 206.82 |
| TPC-DS Q87    |                1445.54 |
| TPC-DS Q88    |                3027.72 |
| TPC-DS Q89    |                 138.10 |
| TPC-DS Q90    |                 134.10 |
| TPC-DS Q91    |                 110.48 |
| TPC-DS Q92    |                  83.81 |
| TPC-DS Q93    |                 219.53 |
| TPC-DS Q94    |                 197.74 |
| TPC-DS Q95    |                3176.24 |
| TPC-DS Q96    |                 103.56 |
| TPC-DS Q97    |                 411.08 |
| TPC-DS Q98    |                 189.24 |
| TPC-DS Q99    |                 181.16 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

This gives a survey about the errors and warnings (result set mismatch) and the latencies of execution per query.
Moreover the loading times (schema creation, ingestion and indexing), the geometric mean of query execution times and the TPC-DS metrics power and throughput are reported.
Please note that the results are not suitable for being published as official TPC-DS results.
In particular the refresh streams are missing.

To see the summary again you can simply call `bexperiments summary -e 1750150367` with the experiment code.

For a more detailed query-wise evaluation you can call `dbmsbenchmarker read -r ~/benchmarks/1750150367 -e yes`.

To inspect result sets you can call `python evaluate.py -r ~/benchmarks/ -e 1750150367 -q 4 resultsets` (here: for query 4).

To compare result sets you can call `dbmsinspect -r ~/benchmarks -c 1750150367 -q 4` (here: for query 4).
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
usage: tpcds.py [-h] [-aws] [-dbms {PostgreSQL,MonetDB,MySQL,MariaDB}] [-xlit LIMIT_IMPORT_TABLE] [-db] [-sl] [-cx CONTEXT] [-e EXPERIMENT] [-m] [-mc] [-ms MAX_SUT] [-xdt] [-xqr NUM_RUN] [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-xnls NUM_LOADING_SPLIT]
                [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS] [-nbp NUM_BENCHMARKING_PODS] [-nbt NUM_BENCHMARKING_THREADS] [-sf SCALING_FACTOR] [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE]
                [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING] [-rnb REQUEST_NODE_BENCHMARKING] [-tr] [-xii] [-xic] [-xis] [-xrcp] [-xshq]
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
  -xlit LIMIT_IMPORT_TABLE, --limit-import-table LIMIT_IMPORT_TABLE
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
  -xdt, --datatransfer   activates transfer of data per query (not only execution)
  -xqr NUM_RUN, --num-run NUM_RUN
                        number of runs per query
  -nc NUM_CONFIG, --num-config NUM_CONFIG
                        number of runs per configuration
  -ne NUM_QUERY_EXECUTORS, --num-query-executors NUM_QUERY_EXECUTORS
                        comma separated list of number of parallel clients
  -xnls NUM_LOADING_SPLIT, --num-loading-split NUM_LOADING_SPLIT
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
  -xii, --init-indexes   adds indexes to tables after ingestion
  -xic, --init-constraints
                        adds constraints to tables after ingestion
  -xis, --init-statistics
                        recomputes statistics of tables after ingestion
  -xrcp, --recreate-parameter
                        recreate parameter for randomized queries
  -xshq, --shuffle-queries
                        have different orderings per stream
```

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

Example:
```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_monitoring.log
```

If monitoring is activated, the summary also contains a section like this:

docs_tpcds_postgresql_monitoring.log
```markdown
﻿## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 739s 
* Code: 1782067395
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:247216
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782067395

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |    3 |      854.00 |           1.00 |            1.00 |        375.00 |          471.00 |              8 |           0 |             | None           |             0 | False         |               12.65 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         58 |            0.16 |            71524.20 |          18434.48 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |         58 |            0.16 |            71524.20 |          18434.48 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               85.28 |
| TPC-DS Q2     |              240.54 |
| TPC-DS Q3     |               49.83 |
| TPC-DS Q4     |             1900.02 |
| TPC-DS Q5     |              182.26 |
| TPC-DS Q6     |               76.98 |
| TPC-DS Q7     |               78.91 |
| TPC-DS Q8     |               37.30 |
| TPC-DS Q9     |              153.13 |
| TPC-DS Q10    |               63.95 |
| TPC-DS Q11    |              924.75 |
| TPC-DS Q12    |               39.20 |
| TPC-DS Q13    |              149.57 |
| TPC-DS Q14a+b |             8211.41 |
| TPC-DS Q15    |               64.70 |
| TPC-DS Q16    |              242.18 |
| TPC-DS Q17    |              351.47 |
| TPC-DS Q18    |              164.76 |
| TPC-DS Q19    |              107.81 |
| TPC-DS Q20    |               51.52 |
| TPC-DS Q21    |              140.59 |
| TPC-DS Q22    |             2142.98 |
| TPC-DS Q23a+b |             3577.64 |
| TPC-DS Q24a+b |              325.85 |
| TPC-DS Q25    |              212.43 |
| TPC-DS Q26    |               48.23 |
| TPC-DS Q27    |              178.75 |
| TPC-DS Q28    |              135.45 |
| TPC-DS Q29    |              201.98 |
| TPC-DS Q30    |               23.58 |
| TPC-DS Q31    |              327.26 |
| TPC-DS Q32    |               39.63 |
| TPC-DS Q33    |               48.61 |
| TPC-DS Q34    |               66.98 |
| TPC-DS Q35    |              194.14 |
| TPC-DS Q36    |              281.83 |
| TPC-DS Q37    |               62.67 |
| TPC-DS Q38    |              329.34 |
| TPC-DS Q39a+b |             2763.47 |
| TPC-DS Q40    |              155.25 |
| TPC-DS Q41    |                9.57 |
| TPC-DS Q42    |               70.34 |
| TPC-DS Q43    |              172.05 |
| TPC-DS Q44    |              131.21 |
| TPC-DS Q45    |               30.57 |
| TPC-DS Q46    |              121.86 |
| TPC-DS Q47    |              489.21 |
| TPC-DS Q48    |              112.75 |
| TPC-DS Q49    |              285.22 |
| TPC-DS Q50    |              305.51 |
| TPC-DS Q51    |             1043.73 |
| TPC-DS Q52    |               62.76 |
| TPC-DS Q53    |               58.56 |
| TPC-DS Q54    |               66.01 |
| TPC-DS Q55    |               48.83 |
| TPC-DS Q56    |               57.09 |
| TPC-DS Q57    |              175.96 |
| TPC-DS Q58    |              186.18 |
| TPC-DS Q59    |              278.75 |
| TPC-DS Q60    |               60.43 |
| TPC-DS Q61    |              119.25 |
| TPC-DS Q62    |               60.83 |
| TPC-DS Q63    |               56.42 |
| TPC-DS Q64    |              930.71 |
| TPC-DS Q65    |              321.53 |
| TPC-DS Q66    |              293.49 |
| TPC-DS Q67    |              853.66 |
| TPC-DS Q68    |              115.30 |
| TPC-DS Q69    |               89.29 |
| TPC-DS Q70    |              249.40 |
| TPC-DS Q71    |               85.23 |
| TPC-DS Q72    |              327.34 |
| TPC-DS Q73    |               51.38 |
| TPC-DS Q74    |              345.36 |
| TPC-DS Q75    |             1001.13 |
| TPC-DS Q76    |               96.87 |
| TPC-DS Q77    |              165.51 |
| TPC-DS Q78    |             2378.38 |
| TPC-DS Q79    |              119.04 |
| TPC-DS Q80    |             1163.60 |
| TPC-DS Q81    |               69.97 |
| TPC-DS Q82    |               86.09 |
| TPC-DS Q83    |               20.22 |
| TPC-DS Q84    |               23.32 |
| TPC-DS Q85    |              277.86 |
| TPC-DS Q86    |               69.18 |
| TPC-DS Q87    |              471.57 |
| TPC-DS Q88    |              161.67 |
| TPC-DS Q89    |               90.51 |
| TPC-DS Q90    |               22.85 |
| TPC-DS Q91    |               30.50 |
| TPC-DS Q92    |               26.11 |
| TPC-DS Q93    |              258.79 |
| TPC-DS Q94    |               83.38 |
| TPC-DS Q95    |              743.06 |
| TPC-DS Q96    |               29.35 |
| TPC-DS Q97    |              508.77 |
| TPC-DS Q98    |              104.50 |
| TPC-DS Q99    |               93.12 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      1012.01 |      3.74 |           6.20 |                  7.72 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        36.40 |      0.13 |           0.01 |                  2.65 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       166.05 |      3.92 |          12.12 |                 13.65 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        18.68 |      0.48 |           0.32 |                  0.32 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.
MonetDB is fast, so we cannot see a lot (metrics are fetched every 30 seconds).


## Perform Benchmark - Throughput Test

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

Example:
```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_throughput.log
```

This runs 3 streams (`-ne`), the first one as a single stream and the following 2 in parallel.

docs_tpcds_postgresql_throughput.log
```markdown
﻿## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 589s 
* Code: 1782068232
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:241985
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782068232
* MonetDB-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:242009
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782068232
* MonetDB-1-1-2-1-2 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:242009
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782068232

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |    1 |      370.00 |           1.00 |            1.00 |        129.00 |          232.00 |              8 |           0 |             | None           |             0 | False         |                9.73 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |         25 |            0.07 |            53559.51 |          14256.00 |          -1 | MonetDB-1-1-1-1-1 |
| MonetDB-1-1-2-1-1 | MonetDB-1       | MonetDB-1-1-2 | MonetDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |         28 |            0.07 |            53933.61 |          12728.57 |          -1 | MonetDB-1-1-2-1-1 |
| MonetDB-1-1-2-1-2 | MonetDB-1       | MonetDB-1-1-2 | MonetDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |         28 |            0.07 |            53324.59 |          12728.57 |          -1 | MonetDB-1-1-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |         25 |            0.07 |            53559.51 |          14256.00 |          -1 |
| MonetDB-1-1-2 | MonetDB-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |         28 |            0.07 |            53628.24 |          25457.14 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |   MonetDB-1-1-2-1-1 |   MonetDB-1-1-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |               56.24 |               58.60 |               57.80 |
| TPC-DS Q2     |              111.55 |               77.16 |               80.34 |
| TPC-DS Q3     |               23.87 |               20.84 |               33.27 |
| TPC-DS Q4     |              658.56 |              577.52 |              664.99 |
| TPC-DS Q5     |               74.23 |               69.82 |               68.90 |
| TPC-DS Q6     |               53.02 |               43.11 |               46.59 |
| TPC-DS Q7     |               49.94 |               42.53 |               42.43 |
| TPC-DS Q8     |               26.57 |               24.35 |               24.80 |
| TPC-DS Q9     |               73.82 |               51.58 |               53.29 |
| TPC-DS Q10    |               64.12 |               51.80 |               53.80 |
| TPC-DS Q11    |              400.34 |              327.96 |              317.14 |
| TPC-DS Q12    |               23.42 |               16.00 |               16.88 |
| TPC-DS Q13    |               51.82 |               42.26 |               51.95 |
| TPC-DS Q14a+b |             2089.30 |             2441.96 |             2034.95 |
| TPC-DS Q15    |               31.49 |               32.98 |               33.23 |
| TPC-DS Q16    |               38.56 |               37.86 |               53.13 |
| TPC-DS Q17    |               97.09 |               92.95 |               95.19 |
| TPC-DS Q18    |               64.92 |               53.10 |               59.67 |
| TPC-DS Q19    |               46.82 |               50.12 |               47.28 |
| TPC-DS Q20    |               30.55 |               25.21 |               33.91 |
| TPC-DS Q21    |              137.82 |              134.72 |              132.84 |
| TPC-DS Q22    |              692.86 |              658.12 |              697.29 |
| TPC-DS Q23a+b |             1660.81 |             1562.43 |             1759.93 |
| TPC-DS Q24a+b |              141.36 |              181.83 |              144.98 |
| TPC-DS Q25    |              124.74 |              102.54 |              106.75 |
| TPC-DS Q26    |               26.13 |               25.02 |               22.82 |
| TPC-DS Q27    |               79.10 |               64.87 |               59.27 |
| TPC-DS Q28    |               54.10 |               58.37 |               69.73 |
| TPC-DS Q29    |              106.58 |              104.87 |               97.65 |
| TPC-DS Q30    |               25.62 |               30.73 |               28.58 |
| TPC-DS Q31    |              127.92 |              107.56 |              115.44 |
| TPC-DS Q32    |               20.02 |               27.14 |               25.61 |
| TPC-DS Q33    |               26.88 |               25.76 |               25.31 |
| TPC-DS Q34    |               28.88 |               32.98 |               32.07 |
| TPC-DS Q35    |               83.24 |               97.76 |               71.49 |
| TPC-DS Q36    |               81.49 |               68.74 |               60.41 |
| TPC-DS Q37    |               71.12 |               91.76 |               88.13 |
| TPC-DS Q38    |              112.08 |              108.58 |              132.05 |
| TPC-DS Q39a+b |             1098.51 |             1273.88 |             1179.47 |
| TPC-DS Q40    |               53.91 |               71.50 |               65.77 |
| TPC-DS Q41    |                7.18 |                9.44 |                9.30 |
| TPC-DS Q42    |               21.09 |               27.63 |               24.01 |
| TPC-DS Q43    |               50.28 |               65.15 |               63.75 |
| TPC-DS Q44    |               30.84 |               41.00 |               46.67 |
| TPC-DS Q45    |               16.08 |               15.00 |               19.82 |
| TPC-DS Q46    |               45.00 |               45.48 |               46.22 |
| TPC-DS Q47    |              193.02 |              213.59 |              206.49 |
| TPC-DS Q48    |               41.97 |               45.04 |               45.07 |
| TPC-DS Q49    |               80.32 |               90.93 |               77.92 |
| TPC-DS Q50    |               96.73 |              116.99 |              110.77 |
| TPC-DS Q51    |              311.39 |              340.51 |              336.57 |
| TPC-DS Q52    |               18.61 |               25.75 |               27.23 |
| TPC-DS Q53    |               30.22 |               34.04 |               32.24 |
| TPC-DS Q54    |               46.74 |               39.96 |               43.54 |
| TPC-DS Q55    |               24.22 |               19.73 |               23.57 |
| TPC-DS Q56    |               20.76 |               23.71 |               26.64 |
| TPC-DS Q57    |              102.46 |              112.01 |              107.60 |
| TPC-DS Q58    |               58.13 |               48.80 |               65.23 |
| TPC-DS Q59    |               85.15 |               90.21 |              102.22 |
| TPC-DS Q60    |               23.01 |               27.07 |               26.43 |
| TPC-DS Q61    |               34.93 |               42.84 |               37.08 |
| TPC-DS Q62    |               29.03 |               32.84 |               31.69 |
| TPC-DS Q63    |               22.84 |               33.66 |               29.63 |
| TPC-DS Q64    |              212.62 |              291.82 |              298.47 |
| TPC-DS Q65    |               87.23 |               93.33 |               92.44 |
| TPC-DS Q66    |              125.64 |              139.12 |              121.14 |
| TPC-DS Q67    |              268.29 |              269.61 |              295.90 |
| TPC-DS Q68    |               41.44 |               43.56 |               45.02 |
| TPC-DS Q69    |               33.03 |               39.96 |               27.12 |
| TPC-DS Q70    |              111.86 |               86.59 |               78.45 |
| TPC-DS Q71    |               34.73 |               33.01 |               40.73 |
| TPC-DS Q72    |              244.16 |              244.82 |              247.19 |
| TPC-DS Q73    |               26.70 |               29.60 |               27.94 |
| TPC-DS Q74    |              108.99 |              105.35 |              118.54 |
| TPC-DS Q75    |              335.40 |              365.72 |              299.85 |
| TPC-DS Q76    |               61.20 |               41.65 |               44.01 |
| TPC-DS Q77    |               55.46 |               61.06 |               60.12 |
| TPC-DS Q78    |              523.19 |              525.96 |              536.87 |
| TPC-DS Q79    |               49.86 |               49.67 |               50.51 |
| TPC-DS Q80    |              373.86 |              368.25 |              392.28 |
| TPC-DS Q81    |               36.14 |               38.30 |               31.82 |
| TPC-DS Q82    |               86.47 |               78.46 |               84.01 |
| TPC-DS Q83    |               13.73 |               15.67 |               12.53 |
| TPC-DS Q84    |               22.97 |               21.06 |               25.97 |
| TPC-DS Q85    |              199.91 |              182.04 |              188.45 |
| TPC-DS Q86    |               40.28 |               39.57 |               47.34 |
| TPC-DS Q87    |              211.03 |              163.34 |              170.87 |
| TPC-DS Q88    |               57.37 |               61.40 |               55.46 |
| TPC-DS Q89    |               41.19 |               36.54 |               45.41 |
| TPC-DS Q90    |               17.54 |               13.20 |               13.36 |
| TPC-DS Q91    |               38.53 |               31.13 |               31.57 |
| TPC-DS Q92    |               15.12 |               13.95 |               15.01 |
| TPC-DS Q93    |               88.05 |               82.99 |               78.90 |
| TPC-DS Q94    |               32.71 |               23.26 |               24.43 |
| TPC-DS Q95    |              205.81 |              126.77 |              143.80 |
| TPC-DS Q96    |               16.00 |               17.28 |               15.39 |
| TPC-DS Q97    |              170.96 |              185.90 |              171.14 |
| TPC-DS Q98    |               48.92 |               50.35 |               42.70 |
| TPC-DS Q99    |               56.31 |               51.75 |               49.79 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MonetDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MonetDB-1-1-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
```

All executions use the same database, so loading times are the same.

Per default, all 3 streams use the same random parameters (like YEAR in Q1) and run in ordering Q1-Q99.
You can change this via
* `-xrcp`: Each stream has it's own random parameters
* `-xshq`: Use the ordering per stream as required by the TPC-DS specification

## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 1 \
  -nc 2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_storage.log
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

docs_tpcds_postgresql_storage.log
```markdown
﻿## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1053s 
* Code: 1782055410
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 10Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:216187
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782055410
* MonetDB-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:216142
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782055410

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |    1 |      493.00 |          19.00 |            1.00 |        177.00 |          290.00 |              8 |           0 |             | None           |             0 | False         |                7.30 |
| MonetDB-1-2 |                2 |    1 |      493.00 |          19.00 |            1.00 |        177.00 |          290.00 |              8 |           0 |             | None           |             0 | False         |                7.30 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |         24 |            0.08 |            49982.02 |          14850.00 |          -1 | MonetDB-1-1-1-1-1 |
| MonetDB-1-2-1-1-1 | MonetDB-1       | MonetDB-1-2-1 | MonetDB-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |        236 |            0.21 |            18447.18 |           1510.17 |          -1 | MonetDB-1-2-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |         24 |            0.08 |            49982.02 |          14850.00 |          -1 |
| MonetDB-1-2-1 | MonetDB-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |        236 |            0.21 |            18447.18 |           1510.17 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |   MonetDB-1-2-1-1-1 |
|:--------------|--------------------:|--------------------:|
| TPC-DS Q1     |               50.62 |             1208.67 |
| TPC-DS Q2     |              101.96 |             2076.77 |
| TPC-DS Q3     |               24.32 |             3562.78 |
| TPC-DS Q4     |              627.70 |             8773.46 |
| TPC-DS Q5     |               80.50 |             3608.42 |
| TPC-DS Q6     |               59.73 |              593.32 |
| TPC-DS Q7     |               55.93 |             6828.25 |
| TPC-DS Q8     |               26.73 |             1595.61 |
| TPC-DS Q9     |               62.41 |             2770.97 |
| TPC-DS Q10    |               55.69 |            38806.31 |
| TPC-DS Q11    |              362.92 |              518.17 |
| TPC-DS Q12    |               17.34 |              832.75 |
| TPC-DS Q13    |               45.29 |              382.18 |
| TPC-DS Q14a+b |             1653.49 |             1815.43 |
| TPC-DS Q15    |               29.99 |               38.25 |
| TPC-DS Q16    |               42.29 |             3705.95 |
| TPC-DS Q17    |               94.46 |              940.74 |
| TPC-DS Q18    |               72.27 |              945.13 |
| TPC-DS Q19    |               50.41 |              106.01 |
| TPC-DS Q20    |               35.72 |               34.73 |
| TPC-DS Q21    |               96.54 |            23859.18 |
| TPC-DS Q22    |              665.77 |             7862.92 |
| TPC-DS Q23a+b |             1482.78 |             1862.37 |
| TPC-DS Q24a+b |              268.70 |              454.48 |
| TPC-DS Q25    |               98.13 |              101.23 |
| TPC-DS Q26    |               19.75 |               21.63 |
| TPC-DS Q27    |               59.84 |               64.05 |
| TPC-DS Q28    |               47.39 |               48.63 |
| TPC-DS Q29    |              101.80 |               96.53 |
| TPC-DS Q30    |               22.59 |              461.93 |
| TPC-DS Q31    |              132.57 |              139.84 |
| TPC-DS Q32    |               24.88 |               18.53 |
| TPC-DS Q33    |               29.04 |              104.97 |
| TPC-DS Q34    |               38.45 |               30.12 |
| TPC-DS Q35    |               88.44 |               73.61 |
| TPC-DS Q36    |               93.74 |               80.50 |
| TPC-DS Q37    |               66.88 |               83.82 |
| TPC-DS Q38    |              124.70 |              131.05 |
| TPC-DS Q39a+b |              982.71 |             1322.16 |
| TPC-DS Q40    |               63.52 |               63.46 |
| TPC-DS Q41    |                8.68 |               10.14 |
| TPC-DS Q42    |               26.26 |               31.27 |
| TPC-DS Q43    |               60.92 |               63.02 |
| TPC-DS Q44    |               33.99 |               41.59 |
| TPC-DS Q45    |               17.87 |               19.39 |
| TPC-DS Q46    |               45.53 |              681.58 |
| TPC-DS Q47    |              201.25 |              280.26 |
| TPC-DS Q48    |               44.10 |               48.28 |
| TPC-DS Q49    |               99.54 |             1815.87 |
| TPC-DS Q50    |              128.09 |              306.83 |
| TPC-DS Q51    |              309.63 |              321.07 |
| TPC-DS Q52    |               22.92 |               26.84 |
| TPC-DS Q53    |               26.54 |               33.04 |
| TPC-DS Q54    |               24.39 |               32.96 |
| TPC-DS Q55    |               18.53 |               24.88 |
| TPC-DS Q56    |               20.05 |               52.39 |
| TPC-DS Q57    |              102.21 |              157.46 |
| TPC-DS Q58    |               68.03 |               70.29 |
| TPC-DS Q59    |              112.53 |              117.73 |
| TPC-DS Q60    |               30.54 |               32.05 |
| TPC-DS Q61    |               48.39 |              105.16 |
| TPC-DS Q62    |               43.16 |              162.43 |
| TPC-DS Q63    |               37.89 |               26.37 |
| TPC-DS Q64    |              287.40 |             1122.17 |
| TPC-DS Q65    |               94.69 |               89.02 |
| TPC-DS Q66    |              136.54 |              145.66 |
| TPC-DS Q67    |              269.83 |              258.47 |
| TPC-DS Q68    |               64.62 |               34.39 |
| TPC-DS Q69    |               57.71 |              669.98 |
| TPC-DS Q70    |               90.07 |              717.94 |
| TPC-DS Q71    |               45.99 |               27.60 |
| TPC-DS Q72    |              258.69 |              818.21 |
| TPC-DS Q73    |               34.89 |               25.99 |
| TPC-DS Q74    |              118.15 |              105.79 |
| TPC-DS Q75    |              342.39 |              248.41 |
| TPC-DS Q76    |               60.40 |             4064.06 |
| TPC-DS Q77    |               52.66 |              274.41 |
| TPC-DS Q78    |              522.97 |              531.30 |
| TPC-DS Q79    |               67.65 |               70.29 |
| TPC-DS Q80    |              382.65 |              401.02 |
| TPC-DS Q81    |               45.98 |              547.09 |
| TPC-DS Q82    |              113.74 |               99.71 |
| TPC-DS Q83    |               16.06 |               14.18 |
| TPC-DS Q84    |               26.74 |             1745.35 |
| TPC-DS Q85    |              188.25 |              212.39 |
| TPC-DS Q86    |               38.94 |               42.36 |
| TPC-DS Q87    |              203.71 |              173.07 |
| TPC-DS Q88    |               64.12 |              110.06 |
| TPC-DS Q89    |               48.66 |               52.79 |
| TPC-DS Q90    |               27.66 |               19.45 |
| TPC-DS Q91    |               38.88 |               54.65 |
| TPC-DS Q92    |               16.96 |               18.06 |
| TPC-DS Q93    |               92.68 |              115.84 |
| TPC-DS Q94    |               81.28 |               28.00 |
| TPC-DS Q95    |              187.31 |              176.49 |
| TPC-DS Q96    |               19.65 |               26.27 |
| TPC-DS Q97    |              173.70 |              165.69 |
| TPC-DS Q98    |               48.96 |               85.75 |
| TPC-DS Q99    |               68.23 |               61.80 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MonetDB-1-2-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
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
bexhoma tpcds \
  -dbms MonetDB \
  -sf 10 \
  -ne 1,1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  profiling &>$LOG_DIR/docs_tpcds_postgresql_profiling.log
```

### Evaluate Results

docs_tpcds_postgresql_profiling.log
```markdown
﻿## Show Summary

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













## Example: MonetDB TPC-DS@30

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

This example shows how to run Q1-Q99 derived from TPC-DS in MonetDB at SF=30.
It covers the power and the throughput test.
The refresh stream is not included.

> The query file is derived from the TPC-DS and as such is not comparable to published TPC-DS results, as the query file results do not comply with the TPC-DS specification.

Official TPC-DS benchmark - http://www.tpc.org/tpcds

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**



### Generate and Load Data

At first we generate TPC-DS data at SF=30 (`-sf`) with 8 parallel generators (`-nlp`).
The generated data is stored at the shared disk `data`.
Moreover the data is loaded into an instance of MonetDB using again 8 parallel loaders.
Afterwards the script creates contraints (`-xic`) and indexes (`-xii`) and updates table statistics (`-xis`).
The database is located in another shared disk of storageClass shared (`-rst`) and of size 2000Gi (`-rss`).
Storage is cleaned if it has existed (`-rsr`).

The script also runs a power test (`-ne` set to 1) with timeout 14400s (`-t`) and data transfer activated (`-xdt`) once (`-nc` set to 1).
To avoid conflicts with other experiments we set a maximum of 1 DBMS per time (`-ms`).
Monitoring is activated (`-m`) for all components (`-mc`).
A node is requested that has 1024Gi RAM (`-rr`=request, `-lr`=limit).

```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR

bexhoma tpcds \
  -dbms MonetDB \
  -sf 30 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -lr 1024Gi \
  -rr 1024Gi \
  -rsr \
  -rss 2000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_1.log
```


### Status Database and Benchmark

You can watch the status of experiments via `bexperiments status`.

In the following example output we see all components of bexhoma are up and running.
The cluster stores a MonetDB database corresponding to TPC-DS of SF=30.
The disk is of storageClass shared and of size 2000Gi and 156G of that space is used.
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
| bexhoma-storage-monetdb-tpcds-30        | monetdb         | tpcds-30     | True         |              4019 | MonetDB    | shared               | 300Gi     | Bound    | 1000G  | 156G   |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

### Summary of Results

At the end of a benchmark you will see a summary like

docs_tpcds_monetdb_1.log
```markdown
﻿## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 4729s 
* Code: 1782070019
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type shared and size 1000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:986808
  * volume_size:1000G
  * volume_used:52G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:1024Gi
  * limits_memory:1024Gi
  * eval_parameters
    * code:1782070019

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |   30 |     2044.00 |          14.00 |            1.00 |        574.00 |         1368.00 |              8 |           0 |             | None           |             0 | False         |               52.84 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |        662 |            0.71 |           157930.98 |          16151.06 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |        662 |            0.71 |           157930.98 |          16151.06 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |              273.87 |
| TPC-DS Q2     |             1828.73 |
| TPC-DS Q3     |              753.23 |
| TPC-DS Q4     |            15931.35 |
| TPC-DS Q5     |             1371.27 |
| TPC-DS Q6     |              524.98 |
| TPC-DS Q7     |              311.60 |
| TPC-DS Q8     |              305.48 |
| TPC-DS Q9     |              627.78 |
| TPC-DS Q10    |              116.57 |
| TPC-DS Q11    |             7453.98 |
| TPC-DS Q12    |              128.81 |
| TPC-DS Q13    |              469.30 |
| TPC-DS Q14a+b |            41778.98 |
| TPC-DS Q15    |              178.18 |
| TPC-DS Q16    |            42006.56 |
| TPC-DS Q17    |             3010.00 |
| TPC-DS Q18    |              885.27 |
| TPC-DS Q19    |              368.37 |
| TPC-DS Q20    |              110.14 |
| TPC-DS Q21    |              148.43 |
| TPC-DS Q22    |             1205.13 |
| TPC-DS Q23a+b |            50767.16 |
| TPC-DS Q24a+b |            28562.96 |
| TPC-DS Q25    |             1453.51 |
| TPC-DS Q26    |              249.57 |
| TPC-DS Q27    |             2145.72 |
| TPC-DS Q28    |              977.90 |
| TPC-DS Q29    |             2404.93 |
| TPC-DS Q30    |               92.77 |
| TPC-DS Q31    |             1983.54 |
| TPC-DS Q32    |              149.58 |
| TPC-DS Q33    |              103.21 |
| TPC-DS Q34    |              220.93 |
| TPC-DS Q35    |             1498.60 |
| TPC-DS Q36    |             1483.10 |
| TPC-DS Q37    |              457.57 |
| TPC-DS Q38    |             2398.96 |
| TPC-DS Q39a+b |             1467.18 |
| TPC-DS Q40    |             1035.11 |
| TPC-DS Q41    |                5.29 |
| TPC-DS Q42    |              103.08 |
| TPC-DS Q43    |              219.34 |
| TPC-DS Q44    |              220.30 |
| TPC-DS Q45    |              150.45 |
| TPC-DS Q46    |              244.66 |
| TPC-DS Q47    |              968.44 |
| TPC-DS Q48    |              235.06 |
| TPC-DS Q49    |             1307.86 |
| TPC-DS Q50    |              601.30 |
| TPC-DS Q51    |             2238.90 |
| TPC-DS Q52    |               88.25 |
| TPC-DS Q53    |               73.84 |
| TPC-DS Q54    |               96.33 |
| TPC-DS Q55    |               86.10 |
| TPC-DS Q56    |               88.47 |
| TPC-DS Q57    |              153.25 |
| TPC-DS Q58    |             6793.41 |
| TPC-DS Q59    |             1048.57 |
| TPC-DS Q60    |              176.82 |
| TPC-DS Q61    |              294.53 |
| TPC-DS Q62    |              332.93 |
| TPC-DS Q63    |               77.77 |
| TPC-DS Q64    |             4044.19 |
| TPC-DS Q65    |              987.95 |
| TPC-DS Q66    |             2004.89 |
| TPC-DS Q67    |             6044.39 |
| TPC-DS Q68    |              540.62 |
| TPC-DS Q69    |               67.55 |
| TPC-DS Q70    |             2589.25 |
| TPC-DS Q71    |              242.11 |
| TPC-DS Q72    |             1184.34 |
| TPC-DS Q73    |               93.21 |
| TPC-DS Q74    |             6663.86 |
| TPC-DS Q75    |             5948.79 |
| TPC-DS Q76    |             1472.45 |
| TPC-DS Q77    |              810.35 |
| TPC-DS Q78    |            13295.24 |
| TPC-DS Q79    |              202.92 |
| TPC-DS Q80    |             8460.92 |
| TPC-DS Q81    |              134.47 |
| TPC-DS Q82    |             1641.35 |
| TPC-DS Q83    |              463.27 |
| TPC-DS Q84    |               32.81 |
| TPC-DS Q85    |              923.57 |
| TPC-DS Q86    |              354.97 |
| TPC-DS Q87    |             2933.00 |
| TPC-DS Q88    |              679.16 |
| TPC-DS Q89    |              129.89 |
| TPC-DS Q90    |              135.25 |
| TPC-DS Q91    |               30.45 |
| TPC-DS Q92    |              176.36 |
| TPC-DS Q93    |             2034.99 |
| TPC-DS Q94    |            35747.45 |
| TPC-DS Q95    |           306471.19 |
| TPC-DS Q96    |              290.38 |
| TPC-DS Q97    |             3312.19 |
| TPC-DS Q98    |              188.73 |
| TPC-DS Q99    |              298.54 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      2540.34 |      5.99 |          51.04 |                 51.75 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.85 |      0.00 |           0.01 |                  0.01 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       332.23 |      0.75 |           0.03 |                  9.94 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |     12084.91 |    125.31 |         878.15 |                878.17 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        25.28 |      0.17 |           0.39 |                  0.40 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

### Perform Benchmark - Power Test

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other (`-ne 1,1`), and shut down the DBMS.
This is repeated 2 times (`-nc`).

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 30 \
  -nc 2 \
  -ne 1,1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -lr 1024Gi \
  -rr 1024Gi \
  -rss 2000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_2.log
```

### Evaluate Results

docs_tpcds_monetdb_2.log
```markdown
﻿## Show Summary

### Workload
TPC-DS Queries SF=30
    Type: tpcds
    Duration: 2276s 
    Code: 1772479408
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=30) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 14400.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Database is persisted to disk of type shared and size 1000Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191991
    volume_size:1000G
    volume_used:75G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772479408
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191993
    volume_size:1000G
    volume_used:75G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772479408
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191985
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772479408
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191988
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772479408

### Errors (failed queries)
            MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q90                 True                 True                 True                 True
TPC-DS Q90
MonetDB-BHT-8-1-2-1: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-2-2-1: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-1-1-1: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-2-1-1: numRun 1: : java.sql.SQLException: division by zero.

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q39a+b                 True                False                 True                 True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1
TPC-DS Q1                  2826.56                62.55              2512.90                65.91
TPC-DS Q2                  8435.85               217.23              7983.39               205.07
TPC-DS Q3                 19638.00               308.97             17956.18               318.85
TPC-DS Q4                 48656.34              4318.13             47250.61              4069.01
TPC-DS Q5                 61212.16              1307.72             62282.62              1303.80
TPC-DS Q6                  1191.94               545.45              1251.95               356.28
TPC-DS Q7                 34696.43               129.74             33854.55               152.15
TPC-DS Q8                   419.65                13.26               199.14                11.30
TPC-DS Q9                  1017.37               733.66               949.91               645.32
TPC-DS Q10               115826.34                50.80            115181.32                52.48
TPC-DS Q11                 2369.69              1800.28              2334.08              1581.88
TPC-DS Q12                  284.16               129.29               353.36               131.39
TPC-DS Q13                  393.37               255.94               381.72               265.08
TPC-DS Q14a+b                61.98                38.42                53.15                26.46
TPC-DS Q15                  126.07               138.27               115.81               133.59
TPC-DS Q16                50886.81             39387.54             50040.85             39240.87
TPC-DS Q17                12354.78              2230.10             12322.87              2291.14
TPC-DS Q18                 3756.94               512.79              4039.04               566.11
TPC-DS Q19                  359.42               175.92               277.55               173.71
TPC-DS Q20                  122.11                98.86               135.08               128.17
TPC-DS Q21                 7585.90               108.21              7721.92               119.27
TPC-DS Q22                 2596.31               244.49              2431.62               344.44
TPC-DS Q23a+b               935.17               629.97              1031.56               644.73
TPC-DS Q24a+b              3390.77              3167.91              3801.41              3172.05
TPC-DS Q25                  838.72               660.20               746.02               669.47
TPC-DS Q26                  140.51               136.72               146.48               165.09
TPC-DS Q27                 6635.07               867.54              7005.99               861.01
TPC-DS Q28                 1834.76              1026.56              1796.13              1069.73
TPC-DS Q29                  731.26               683.28               816.55               675.38
TPC-DS Q30                  219.34                18.40               174.29                32.38
TPC-DS Q31                 2665.72              1214.38              2557.54              1163.32
TPC-DS Q32                  153.25               137.98               138.89               130.84
TPC-DS Q33                  329.03                78.56               144.57                80.47
TPC-DS Q34                 2003.90               335.00              1667.71               337.43
TPC-DS Q35                   33.18                28.02                35.80                27.13
TPC-DS Q36                  784.55               753.23               730.25               729.42
TPC-DS Q37                  461.13               511.49               435.50               344.97
TPC-DS Q38                    5.61                 6.06                 5.37                 5.29
TPC-DS Q39a+b                12.90                10.01                 9.03                 8.97
TPC-DS Q40                 1696.95               498.46              2194.12               547.27
TPC-DS Q41                    6.09                 5.64                 6.07                 5.23
TPC-DS Q42                   91.93                69.45                92.81                74.36
TPC-DS Q43                  266.83               231.77               302.81               257.88
TPC-DS Q44                  245.38               246.25               270.45               227.70
TPC-DS Q45                  193.67               136.94               170.82               144.34
TPC-DS Q46                  302.86               193.60               269.31               192.79
TPC-DS Q47                  232.44               142.66               242.17               139.36
TPC-DS Q48                  164.19               167.37               168.61               167.43
TPC-DS Q49                 7430.78               949.56              7459.57              1012.68
TPC-DS Q50                  781.49               619.02               865.88               629.30
TPC-DS Q51                   94.30               116.72               103.25                90.37
TPC-DS Q52                   64.41                61.23                64.51                63.13
TPC-DS Q53                  123.76                85.27                98.40                89.21
TPC-DS Q54                 2030.80               151.17              2157.87               148.46
TPC-DS Q55                   71.84                64.50                70.98                50.32
TPC-DS Q56                 1598.46              1633.47              1668.59              1641.33
TPC-DS Q57                  218.59               117.96               209.82               116.57
TPC-DS Q58                 1374.24               427.65              1533.40               454.38
TPC-DS Q59                  914.30               812.16               927.35               822.67
TPC-DS Q60                 3039.10              3060.70              3033.69              3070.00
TPC-DS Q61                  241.43               177.60               235.55               190.22
TPC-DS Q62                  378.38               252.87               339.74               254.04
TPC-DS Q63                  151.45               102.17               118.79               108.03
TPC-DS Q64                10251.22              2252.86             10200.66              2163.83
TPC-DS Q65                  194.27               205.60               184.99               209.12
TPC-DS Q66                 1642.17              1417.15              1769.73              1415.39
TPC-DS Q67                   16.96                17.03                16.83                16.22
TPC-DS Q68                  256.01               325.09               263.94               277.61
TPC-DS Q69                   35.85                34.39                37.04                35.10
TPC-DS Q70                  381.16                11.87               435.16                11.61
TPC-DS Q71                  176.05               126.83               189.09               128.07
TPC-DS Q72                 1587.83               629.29              1446.11               646.11
TPC-DS Q73                   94.93                86.82                79.04                79.75
TPC-DS Q74                  552.13               499.24               535.68               458.69
TPC-DS Q75                 5659.66              3224.52              5847.85              3236.84
TPC-DS Q76                21541.68              6118.99             21848.77              5005.27
TPC-DS Q77                  724.31               502.99               851.97               571.36
TPC-DS Q78                 6986.43              2815.09              7061.53              3056.98
TPC-DS Q79                  177.69               150.95               149.61               150.41
TPC-DS Q80                 6015.40              5942.31              6175.09              5950.51
TPC-DS Q81                  211.11                24.02               123.87                22.17
TPC-DS Q82                  484.13               401.15               467.56               501.44
TPC-DS Q83                   20.68                23.56                21.20                20.59
TPC-DS Q84                  114.92                37.32                62.61                24.08
TPC-DS Q85                  424.98               375.37               430.98               397.02
TPC-DS Q86                  166.25               250.17               157.58               239.26
TPC-DS Q87                   16.24                 8.34                 7.67                 6.71
TPC-DS Q88                  731.94               657.34               707.60               665.00
TPC-DS Q89                  179.08               188.31               173.58               153.14
TPC-DS Q91                  247.89                29.74               201.08                26.64
TPC-DS Q92                  123.74               136.88               135.54               136.20
TPC-DS Q93                 1919.05              1879.40              1910.63              1891.93
TPC-DS Q94                35739.82             35444.00             35666.21             32985.20
TPC-DS Q95                36990.16             34054.68             33622.06             36310.39
TPC-DS Q96                   35.80                36.00                36.09                34.71
TPC-DS Q97                   62.38                50.63                65.17                44.29
TPC-DS Q98                  131.69               128.08               125.96               101.95
TPC-DS Q99                  267.73               267.17               280.21               268.54

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-1-2-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-2-1-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-2-2-1           1.0          257.0        11.0     1070.0    1376.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.61
MonetDB-BHT-8-1-2-1           0.25
MonetDB-BHT-8-2-1-1           0.58
MonetDB-BHT-8-2-2-1           0.25

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1          176269.76
MonetDB-BHT-8-1-2-1          425439.59
MonetDB-BHT-8-2-1-1          185272.31
MonetDB-BHT-8-2-2-1          433826.07

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count    SF  Throughput@Size
DBMS              SF   num_experiment num_client                                        
MonetDB-BHT-8-1-1 30.0 1              1                566      1  30.0         18699.65
MonetDB-BHT-8-1-2 30.0 1              2                177      1  30.0         59796.61
MonetDB-BHT-8-2-1 30.0 2              1                561      1  30.0         18866.31
MonetDB-BHT-8-2-2 30.0 2              2                178      1  30.0         59460.67

### Workflow
                             orig_name    SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-1  30.0     8               1           1       1772479577     1772480143
MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-1-2  30.0     8               1           2       1772480273     1772480450
MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-1  30.0     8               2           1       1772480734     1772481295
MonetDB-BHT-8-2-2-1  MonetDB-BHT-8-2-2  30.0     8               2           2       1772481429     1772481607

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1], [1, 1]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1     2985.66    16.74         42.76                42.83
MonetDB-BHT-8-1-2     2504.62    18.74         49.43                49.52
MonetDB-BHT-8-2-1    12931.64    15.30         46.08                46.16
MonetDB-BHT-8-2-2     2366.11    20.23         46.50                46.58

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       13.59     0.20          0.32                 0.33
MonetDB-BHT-8-1-2       13.59     0.01          0.32                 0.33
MonetDB-BHT-8-2-1       15.11     0.02          0.30                 0.31
MonetDB-BHT-8-2-2       15.11     0.18          0.30                 0.31

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```

### Perform Benchmark - Throughput Test

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other, and then a throughput test with 3 parallel driver (`-ne 1,1,3`). and shut down the DBMS.


```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 30 \
  -nc 1 \
  -ne 1,1,3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -lr 1024Gi \
  -rr 1024Gi \
  -rss 2000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_3.log
```

### Evaluate Results

docs_tpcds_monetdb_3.log
```markdown
﻿## Show Summary

### Workload
TPC-DS Queries SF=30
    Type: tpcds
    Duration: 1771s 
    Code: 1772481803
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=30) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 14400.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Database is persisted to disk of type shared and size 1000Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191989
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772481803
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191974
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772481803
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191977
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772481803
MonetDB-BHT-8-3-2 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191977
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772481803
MonetDB-BHT-8-3-3 uses docker image monetdb/monetdb:Dec2025
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1191977
    volume_size:1000G
    volume_used:74G
    cpu_list:0-223
    requests_cpu:4
    requests_memory:1024Gi
    limits_memory:1024Gi
    eval_parameters
        code:1772481803

### Errors (failed queries)
            MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
TPC-DS Q90               True               True               True               True               True
TPC-DS Q90
MonetDB-BHT-8-3-2: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-3-3: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-1-1: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-2-1: numRun 1: : java.sql.SQLException: division by zero.
MonetDB-BHT-8-3-1: numRun 1: : java.sql.SQLException: division by zero.

### Warnings (result mismatch)
               MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
TPC-DS Q39a+b               True               True               True              False               True

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3
TPC-DS Q1                2803.58              69.71              73.52              53.87              57.44
TPC-DS Q2                8636.28             217.20             483.02             227.28             380.94
TPC-DS Q3               19256.43             359.37             102.71             567.71             532.36
TPC-DS Q4               47404.68            4054.92            6772.10            7032.01            7949.06
TPC-DS Q5               63149.32            2945.17            1588.82            1526.41            1487.74
TPC-DS Q6                1134.22             567.84             871.56             768.15             246.80
TPC-DS Q7               33931.77             127.99             159.69             212.03             159.79
TPC-DS Q8                 302.24              12.71              16.17              13.35              13.43
TPC-DS Q9                6324.16             686.99            1364.37            1530.11            1122.17
TPC-DS Q10             114502.85              47.49              33.14              40.01             121.52
TPC-DS Q11               2380.92            1644.09            2159.83            2667.66            2052.77
TPC-DS Q12                275.96             106.42             239.59             227.31             238.17
TPC-DS Q13                388.99             258.05             435.11             288.15             212.08
TPC-DS Q14a+b              75.95              27.79              25.32              25.43              28.13
TPC-DS Q15                117.27             129.62             138.21             133.06             120.35
TPC-DS Q16              49963.68           37998.73          112920.96           37736.07           65578.99
TPC-DS Q17              12802.24            2308.06            4348.07            2677.53            4326.35
TPC-DS Q18               4766.91             525.50             935.86            2412.95           16190.55
TPC-DS Q19                306.45             173.01             434.99            7789.65           25793.19
TPC-DS Q20                 97.40             125.16             139.32           14255.65             432.73
TPC-DS Q21               7677.42             115.28             274.69            3808.50             136.01
TPC-DS Q22               2931.76             277.51             270.36            1040.16             452.07
TPC-DS Q23a+b             885.41             847.03             621.95           41871.17            1384.82
TPC-DS Q24a+b            3350.83            3174.31            3831.31            4005.44            4162.98
TPC-DS Q25                817.57             826.34             851.26            1044.04             801.04
TPC-DS Q26                150.48             139.26             158.75             357.60             464.47
TPC-DS Q27               6555.77             810.79             782.19             977.48            1066.21
TPC-DS Q28               1734.06            1044.71             686.95            1240.80            1339.89
TPC-DS Q29                747.44             756.86            1132.73            1366.01            1192.19
TPC-DS Q30                191.30              25.81              33.17              82.61              11.07
TPC-DS Q31               2563.32            1246.91            5385.29            1812.21            1066.69
TPC-DS Q32                153.86             154.81             137.56             167.41             158.73
TPC-DS Q33                 98.75              81.36              68.85             115.08              78.96
TPC-DS Q34               1818.60             328.39             236.52             472.46             133.31
TPC-DS Q35                 32.59              29.95              30.48              38.18              24.89
TPC-DS Q36                841.94             565.84             574.60             766.96             565.11
TPC-DS Q37                482.81             342.44             592.50             492.02             534.97
TPC-DS Q38                  6.32               6.28               5.41               4.89               6.82
TPC-DS Q39a+b              10.05               8.25               7.14              11.79              11.59
TPC-DS Q40               2360.66             541.37             785.37             533.41             761.12
TPC-DS Q41                  5.80               5.89              37.51               6.48              11.55
TPC-DS Q42                 65.77              64.91              70.27              74.08             153.14
TPC-DS Q43                280.81             225.06             267.67             296.65             401.79
TPC-DS Q44              32553.06            5740.13             478.14            5390.60            4231.37
TPC-DS Q45                145.31             142.65             146.96             145.81             176.72
TPC-DS Q46                864.18             204.38             210.67             219.54             175.63
TPC-DS Q47                184.57             137.03             165.87             147.89             197.19
TPC-DS Q48                183.77             161.29             174.82             207.64             276.78
TPC-DS Q49               8313.61            1093.56             903.92            1055.62            1131.00
TPC-DS Q50                864.38             717.24             733.83             604.91             813.81
TPC-DS Q51                 91.12              95.57             109.52             137.41             234.60
TPC-DS Q52                 64.85              63.04             196.57             572.37             100.53
TPC-DS Q53                273.91              90.94             306.55              86.12              98.07
TPC-DS Q54                 98.67              98.26             302.96             124.66             125.56
TPC-DS Q55                 70.61              48.51             184.94              87.97              72.03
TPC-DS Q56               2037.01            2227.03            2069.12            2244.94            2396.48
TPC-DS Q57                226.64             144.32             145.91             164.27             374.95
TPC-DS Q58               1799.45             439.38             440.71             614.94             747.81
TPC-DS Q59                991.79             768.36             964.88             895.87             728.67
TPC-DS Q60               3212.06            3104.75            4233.68            3529.38            3355.82
TPC-DS Q61                472.16             178.71             182.90             423.99             251.76
TPC-DS Q62                361.57             248.52            1303.95             242.52             253.02
TPC-DS Q63                125.88             103.57            2509.54             146.43              91.01
TPC-DS Q64              10774.75            2188.13            2379.56            3400.74            3473.68
TPC-DS Q65                201.24             202.42             188.75             201.48             163.07
TPC-DS Q66               1821.07            1386.27            1579.40            2479.53            4026.82
TPC-DS Q67                 19.43              17.27              16.10            1680.60              76.35
TPC-DS Q68                286.35             252.43             242.65             179.01             221.11
TPC-DS Q69                 39.58              34.79              32.38              49.93              30.61
TPC-DS Q70                540.12              12.50               6.93              14.34               8.28
TPC-DS Q71                168.06             135.65              94.49             107.96             132.17
TPC-DS Q72               1688.20             631.94             532.54             897.29             680.48
TPC-DS Q73                108.79              97.90             105.01             158.49             236.45
TPC-DS Q74                689.27             476.11             381.40             940.41             803.10
TPC-DS Q75               6573.59            3550.55            5712.90            3882.19            4518.24
TPC-DS Q76              20834.45            5040.30             269.67            5219.21            5008.92
TPC-DS Q77                740.88             710.68             545.66             788.12             656.38
TPC-DS Q78               7206.13            2682.08            5491.52            5602.49            5649.14
TPC-DS Q79                139.08             148.61             154.51             160.40             237.46
TPC-DS Q80               6120.70            5939.55            7249.11            8925.97            9619.09
TPC-DS Q81                182.25              28.04              17.52              21.52              17.28
TPC-DS Q82                453.41             429.05             730.50             361.56             378.46
TPC-DS Q83                 27.07              20.55              49.51              23.09              18.27
TPC-DS Q84                 53.71              33.24              27.15              77.00              26.38
TPC-DS Q85                420.64             371.79             373.49             597.47             738.88
TPC-DS Q86                185.09             202.03             178.51             441.08             253.73
TPC-DS Q87                  6.67               6.64               4.94              11.68               8.14
TPC-DS Q88                756.03             654.05             734.00             979.32            1116.13
TPC-DS Q89                189.44             149.20             151.75             179.42             223.14
TPC-DS Q91                171.14              31.49             478.53              86.20              79.90
TPC-DS Q92                125.06             137.27             121.95             134.68             212.19
TPC-DS Q93               1869.49            1905.25            4202.07            3808.53            3754.87
TPC-DS Q94              35218.64           33696.25          129556.76           35459.53          163957.84
TPC-DS Q95              38308.70           37077.34           61195.83           49604.13           56100.01
TPC-DS Q96                 41.19              34.42              27.86           13180.38              58.11
TPC-DS Q97                 69.07              47.53              51.63           21225.57              69.97
TPC-DS Q98                134.70              99.39             120.01           28621.51              96.24
TPC-DS Q99                277.76             295.99             266.47           15876.60             255.60

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-2-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-3-1           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-3-2           1.0          257.0        11.0     1070.0    1376.0
MonetDB-BHT-8-3-3           1.0          257.0        11.0     1070.0    1376.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.64
MonetDB-BHT-8-2-1           0.26
MonetDB-BHT-8-3-1           0.33
MonetDB-BHT-8-3-2           0.53
MonetDB-BHT-8-3-3           0.37

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1          168770.19
MonetDB-BHT-8-2-1          411294.30
MonetDB-BHT-8-3-1          332405.14
MonetDB-BHT-8-3-2          204235.70
MonetDB-BHT-8-3-3          290573.47

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                time [s]  count    SF  Throughput@Size
DBMS            SF   num_experiment num_client                                        
MonetDB-BHT-8-1 30.0 1              1                605      1  30.0         17494.21
MonetDB-BHT-8-2 30.0 1              2                189      1  30.0         56000.00
MonetDB-BHT-8-3 30.0 1              3                436      3  30.0         72825.69

### Workflow
                         orig_name    SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MonetDB-BHT-8-1-1  MonetDB-BHT-8-1  30.0     8               1           1       1772481970     1772482575
MonetDB-BHT-8-2-1  MonetDB-BHT-8-2  30.0     8               1           2       1772482728     1772482917
MonetDB-BHT-8-3-1  MonetDB-BHT-8-3  30.0     8               1           3       1772483055     1772483456
MonetDB-BHT-8-3-2  MonetDB-BHT-8-3  30.0     8               1           3       1772483055     1772483429
MonetDB-BHT-8-3-3  MonetDB-BHT-8-3  30.0     8               1           3       1772483055     1772483491

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 3]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1     9057.51    72.35        177.71               177.80
MonetDB-BHT-8-2     2853.24    22.14         47.24                47.32
MonetDB-BHT-8-3    15960.43    72.12        263.95               264.03

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       11.90     0.16          0.30                  0.3
MonetDB-BHT-8-2       11.90     0.01          0.30                  0.3
MonetDB-BHT-8-3       31.49     0.57          0.29                  0.3

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```



