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
  -rss 50Gi \
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

You can watch the status while benchmark is running via `bexhoma status`

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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 684s 
* Code: 1785193272
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:815944
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785193272

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785193272-656f8cb747-drf4v: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      232.00 |           1.00 |            1.00 |         47.00 |          173.00 |              8 |           0 |             | None           |             0 | False         |               15.52 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        173 |            0.31 |            11830.77 |           2060.12 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        173 |            0.31 |            11830.77 |           2060.12 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 109.95 |
| TPC-DS Q2     |                 182.18 |
| TPC-DS Q3     |                 133.08 |
| TPC-DS Q4     |                6471.18 |
| TPC-DS Q5     |                 356.01 |
| TPC-DS Q6     |               52188.59 |
| TPC-DS Q7     |                 477.19 |
| TPC-DS Q8     |                  65.57 |
| TPC-DS Q9     |                1809.40 |
| TPC-DS Q10    |                 889.22 |
| TPC-DS Q11    |                4086.16 |
| TPC-DS Q12    |                  56.30 |
| TPC-DS Q13    |                 500.07 |
| TPC-DS Q14a+b |                1901.05 |
| TPC-DS Q15    |                 104.96 |
| TPC-DS Q16    |                 165.03 |
| TPC-DS Q17    |                 277.10 |
| TPC-DS Q18    |                 335.71 |
| TPC-DS Q19    |                 128.04 |
| TPC-DS Q20    |                  84.34 |
| TPC-DS Q21    |                 162.67 |
| TPC-DS Q22    |                2681.91 |
| TPC-DS Q23a+b |                4308.65 |
| TPC-DS Q24a+b |                 658.89 |
| TPC-DS Q25    |                 266.19 |
| TPC-DS Q26    |                 201.77 |
| TPC-DS Q27    |                  19.00 |
| TPC-DS Q28    |                 568.06 |
| TPC-DS Q29    |                 277.87 |
| TPC-DS Q30    |                7886.31 |
| TPC-DS Q31    |                1315.02 |
| TPC-DS Q32    |                  87.19 |
| TPC-DS Q33    |                 322.58 |
| TPC-DS Q34    |                  21.35 |
| TPC-DS Q35    |                 942.11 |
| TPC-DS Q36    |                  20.96 |
| TPC-DS Q37    |                 415.40 |
| TPC-DS Q38    |                1262.30 |
| TPC-DS Q39a+b |                1921.96 |
| TPC-DS Q40    |                 119.69 |
| TPC-DS Q41    |                 759.77 |
| TPC-DS Q42    |                  66.16 |
| TPC-DS Q43    |                 125.14 |
| TPC-DS Q44    |                 363.81 |
| TPC-DS Q45    |                  94.80 |
| TPC-DS Q46    |                  44.87 |
| TPC-DS Q47    |                1926.97 |
| TPC-DS Q48    |                 592.35 |
| TPC-DS Q49    |                 333.06 |
| TPC-DS Q50    |                 409.95 |
| TPC-DS Q51    |                 656.55 |
| TPC-DS Q52    |                  59.41 |
| TPC-DS Q53    |                  77.59 |
| TPC-DS Q54    |                  61.26 |
| TPC-DS Q55    |                  55.35 |
| TPC-DS Q56    |                 375.43 |
| TPC-DS Q57    |                 903.13 |
| TPC-DS Q58    |                 313.30 |
| TPC-DS Q59    |                 378.35 |
| TPC-DS Q60    |                 338.52 |
| TPC-DS Q61    |                 103.74 |
| TPC-DS Q62    |                  75.59 |
| TPC-DS Q63    |                  76.23 |
| TPC-DS Q64    |                 481.26 |
| TPC-DS Q65    |                 391.07 |
| TPC-DS Q66    |                 163.58 |
| TPC-DS Q67    |                2368.04 |
| TPC-DS Q68    |                  32.44 |
| TPC-DS Q69    |                 443.68 |
| TPC-DS Q70    |                 689.59 |
| TPC-DS Q71    |                 274.80 |
| TPC-DS Q72    |                 788.24 |
| TPC-DS Q73    |                  22.42 |
| TPC-DS Q74    |                 928.96 |
| TPC-DS Q75    |                 605.82 |
| TPC-DS Q76    |                  95.81 |
| TPC-DS Q77    |                 240.99 |
| TPC-DS Q78    |                1018.57 |
| TPC-DS Q79    |                 150.29 |
| TPC-DS Q80    |                 352.79 |
| TPC-DS Q81    |               32398.12 |
| TPC-DS Q82    |                 628.66 |
| TPC-DS Q83    |                  75.01 |
| TPC-DS Q84    |                  64.31 |
| TPC-DS Q85    |                 237.35 |
| TPC-DS Q86    |                 176.67 |
| TPC-DS Q87    |                1023.54 |
| TPC-DS Q88    |                2791.43 |
| TPC-DS Q89    |                  76.27 |
| TPC-DS Q90    |                  92.53 |
| TPC-DS Q91    |                  73.33 |
| TPC-DS Q92    |                  40.05 |
| TPC-DS Q93    |                 160.78 |
| TPC-DS Q94    |                 121.51 |
| TPC-DS Q95    |                2509.91 |
| TPC-DS Q96    |                  70.46 |
| TPC-DS Q97    |                 275.70 |
| TPC-DS Q98    |                 335.42 |
| TPC-DS Q99    |                 158.49 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

</details>

This gives a survey about the errors and warnings (result set mismatch) and the latencies of execution per query.
Moreover the loading times (schema creation, ingestion and indexing), the geometric mean of query execution times and the TPC-DS metrics power and throughput are reported.
Please note that the results are not suitable for being published as official TPC-DS results.
In particular the refresh streams are missing.

To see the summary again you can simply call `bexhoma summary -e 1750150367` with the experiment code.

For a more detailed query-wise evaluation you can call `dbmsbenchmarker read -r ~/benchmarks/1750150367 -e yes`.

To inspect result sets you can call `python evaluate.py -r ~/benchmarks/ -e 1750150367 -q 4 resultsets` (here: for query 4).

To compare result sets you can call `dbmsinspect -r ~/benchmarks -c 1750150367 -q 4` (here: for query 4).
This shows the differences in result sets only.


### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in more detail.
Detailed evaluations can be done using DBMSBenchmarker
* [Dashboard](https://dbmsbenchmarker.readthedocs.io/en/latest/Dashboard.html)
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server in the cluster by `bexhoma dashboard`.
This forwards ports, so you have
* a DBMSBenchmarker dashboard in browser at http://localhost:8050
* a Jupyter notebook server at http://localhost:8888 containing the example notebooks

You can connect to a local evaluation server by `bexhoma localdashboard`.
This forwards ports, so you have
* a DBMSBenchmarker dashboard in browser at http://localhost:8050

You can connect to a local jupyter server by `bexhoma jupyter`.
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
  -dbms PostgreSQL \
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
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_monitoring.log
```

If monitoring is activated, the summary also contains a section like this:

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_monitoring_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1372s 
* Code: 1785194031
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824131
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785194031

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785194031-65d5f7bcb7-sqhfz: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      427.00 |           0.00 |            1.00 |        133.00 |          284.00 |              8 |           0 |             | None           |             0 | False         |               25.29 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |        734 |            0.65 |            16838.29 |           1456.68 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |        734 |            0.65 |            16838.29 |           1456.68 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 195.35 |
| TPC-DS Q2     |                 467.28 |
| TPC-DS Q3     |                 400.11 |
| TPC-DS Q4     |               18040.64 |
| TPC-DS Q5     |                 761.92 |
| TPC-DS Q6     |              206976.58 |
| TPC-DS Q7     |                 989.82 |
| TPC-DS Q8     |                 101.67 |
| TPC-DS Q9     |                2337.01 |
| TPC-DS Q10    |                1116.31 |
| TPC-DS Q11    |               10068.44 |
| TPC-DS Q12    |                 144.69 |
| TPC-DS Q13    |                1270.97 |
| TPC-DS Q14a+b |                6535.59 |
| TPC-DS Q15    |                 282.16 |
| TPC-DS Q16    |                 399.91 |
| TPC-DS Q17    |                 656.58 |
| TPC-DS Q18    |                 585.07 |
| TPC-DS Q19    |                 402.52 |
| TPC-DS Q20    |                 251.33 |
| TPC-DS Q21    |                 310.85 |
| TPC-DS Q22    |                7219.18 |
| TPC-DS Q23a+b |               11006.14 |
| TPC-DS Q24a+b |                1254.05 |
| TPC-DS Q25    |                 626.01 |
| TPC-DS Q26    |                 435.74 |
| TPC-DS Q27    |                1153.78 |
| TPC-DS Q28    |                1846.05 |
| TPC-DS Q29    |                 730.88 |
| TPC-DS Q30    |               67156.80 |
| TPC-DS Q31    |                3833.71 |
| TPC-DS Q32    |                 149.93 |
| TPC-DS Q33    |                 763.77 |
| TPC-DS Q34    |                  35.09 |
| TPC-DS Q35    |                1213.32 |
| TPC-DS Q36    |                  36.54 |
| TPC-DS Q37    |                 333.39 |
| TPC-DS Q38    |                2848.07 |
| TPC-DS Q39a+b |                4748.58 |
| TPC-DS Q40    |                 425.59 |
| TPC-DS Q41    |                2672.53 |
| TPC-DS Q42    |                 161.92 |
| TPC-DS Q43    |                  52.63 |
| TPC-DS Q44    |                   1.84 |
| TPC-DS Q45    |                 168.58 |
| TPC-DS Q46    |                  53.39 |
| TPC-DS Q47    |                2184.92 |
| TPC-DS Q48    |                1043.56 |
| TPC-DS Q49    |                 644.92 |
| TPC-DS Q50    |                1149.79 |
| TPC-DS Q51    |                2086.48 |
| TPC-DS Q52    |                 154.05 |
| TPC-DS Q53    |                 186.12 |
| TPC-DS Q54    |                  64.13 |
| TPC-DS Q55    |                 150.59 |
| TPC-DS Q56    |                 727.62 |
| TPC-DS Q57    |                1960.78 |
| TPC-DS Q58    |                 727.06 |
| TPC-DS Q59    |                 710.90 |
| TPC-DS Q60    |                 878.03 |
| TPC-DS Q61    |                 104.92 |
| TPC-DS Q62    |                 173.42 |
| TPC-DS Q63    |                 190.57 |
| TPC-DS Q64    |                 850.32 |
| TPC-DS Q65    |                1112.75 |
| TPC-DS Q66    |                 545.22 |
| TPC-DS Q67    |                7656.39 |
| TPC-DS Q68    |                  69.99 |
| TPC-DS Q69    |                 373.90 |
| TPC-DS Q70    |                 701.40 |
| TPC-DS Q71    |                 679.06 |
| TPC-DS Q72    |                2323.13 |
| TPC-DS Q73    |                  37.58 |
| TPC-DS Q74    |                1989.23 |
| TPC-DS Q75    |                3282.63 |
| TPC-DS Q76    |                 357.60 |
| TPC-DS Q77    |                 430.96 |
| TPC-DS Q78    |                4011.82 |
| TPC-DS Q79    |                 262.61 |
| TPC-DS Q80    |                 875.13 |
| TPC-DS Q81    |              292877.99 |
| TPC-DS Q82    |                 447.08 |
| TPC-DS Q83    |                 136.95 |
| TPC-DS Q84    |                  23.43 |
| TPC-DS Q85    |                 279.84 |
| TPC-DS Q86    |                 470.08 |
| TPC-DS Q87    |                2212.85 |
| TPC-DS Q88    |                2446.88 |
| TPC-DS Q89    |                 204.56 |
| TPC-DS Q90    |                 284.55 |
| TPC-DS Q91    |                 145.01 |
| TPC-DS Q92    |                 168.23 |
| TPC-DS Q93    |                 581.52 |
| TPC-DS Q94    |                 309.36 |
| TPC-DS Q95    |                7145.29 |
| TPC-DS Q96    |                 317.96 |
| TPC-DS Q97    |                 719.43 |
| TPC-DS Q98    |                 389.86 |
| TPC-DS Q99    |                 297.96 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       235.12 |      2.11 |           6.32 |                 13.00 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.11 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        23.75 |      0.25 |           0.01 |                  2.21 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       893.62 |      2.54 |           6.97 |                 13.65 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        21.39 |      0.55 |           0.34 |                  0.35 |

### Tests
* TEST passed: No SUT container restarts
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

</details>

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.
MonetDB is fast, so we cannot see a lot (metrics are fetched every 30 seconds).


## Perform Benchmark - Throughput Test

For performing the experiment we can run the [tpcds file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpcds.py).

Example:
```bash
bexhoma tpcds \
  -dbms PostgreSQL \
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_throughput.log
```

This runs 3 streams (`-ne`), the first one as a single stream and the following 2 in parallel.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_throughput_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_throughput.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 885s 
* Code: 1785195502
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:816851
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785195502
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:817022
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785195502
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:817022
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785195502

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785195502-864dd966b8-4fqrv: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      230.00 |           1.00 |            0.00 |         47.00 |          174.00 |              8 |           0 |             | None           |             0 | False         |               15.65 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        161 |            0.29 |            12740.32 |           2213.66 |          -1 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |        164 |            0.30 |            12297.11 |           2173.17 |          -1 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               99 |        161 |            0.31 |            12127.19 |           2213.66 |          -1 | PostgreSQL-1-1-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        161 |            0.29 |            12740.32 |           2213.66 |          -1 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              198 |        164 |            0.30 |            12211.86 |           4346.34 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |
|:--------------|-----------------------:|-----------------------:|-----------------------:|
| TPC-DS Q1     |                 106.18 |                 107.42 |                 103.17 |
| TPC-DS Q2     |                 184.50 |                 182.91 |                 182.88 |
| TPC-DS Q3     |                 139.18 |                 132.11 |                 134.50 |
| TPC-DS Q4     |                6705.71 |                6624.58 |                6521.45 |
| TPC-DS Q5     |                 374.29 |                 371.06 |                 366.61 |
| TPC-DS Q6     |               51964.98 |               54028.23 |               52468.61 |
| TPC-DS Q7     |                 287.65 |                 285.44 |                 301.32 |
| TPC-DS Q8     |                  94.12 |                  91.97 |                  87.91 |
| TPC-DS Q9     |                1720.50 |                1697.48 |                1693.86 |
| TPC-DS Q10    |                 860.98 |                 864.21 |                 857.61 |
| TPC-DS Q11    |                3900.98 |                4756.54 |                4206.76 |
| TPC-DS Q12    |                  55.57 |                  56.82 |                  58.07 |
| TPC-DS Q13    |                 471.63 |                 474.69 |                 490.93 |
| TPC-DS Q14a+b |                2356.39 |                1592.23 |                1657.78 |
| TPC-DS Q15    |                  98.82 |                 100.20 |                  98.97 |
| TPC-DS Q16    |                 153.21 |                 149.33 |                 166.58 |
| TPC-DS Q17    |                 256.80 |                 493.12 |                 267.67 |
| TPC-DS Q18    |                 307.60 |                 397.33 |                 340.31 |
| TPC-DS Q19    |                 136.99 |                 140.54 |                 132.91 |
| TPC-DS Q20    |                  83.11 |                  85.24 |                  86.68 |
| TPC-DS Q21    |                 180.67 |                 171.44 |                 167.90 |
| TPC-DS Q22    |                2618.08 |                2627.61 |                2853.36 |
| TPC-DS Q23a+b |                4000.45 |                5248.84 |                4625.11 |
| TPC-DS Q24a+b |                 485.37 |                 474.16 |                 524.08 |
| TPC-DS Q25    |                 250.69 |                 250.10 |                 259.74 |
| TPC-DS Q26    |                 205.62 |                 184.50 |                 211.95 |
| TPC-DS Q27    |                  20.26 |                  16.61 |                  18.69 |
| TPC-DS Q28    |                 563.38 |                 549.98 |                 574.49 |
| TPC-DS Q29    |                 271.92 |                 263.55 |                 283.31 |
| TPC-DS Q30    |                7574.89 |                8709.46 |                7664.16 |
| TPC-DS Q31    |                1284.96 |                1258.18 |                1541.14 |
| TPC-DS Q32    |                 116.25 |                 111.57 |                 173.54 |
| TPC-DS Q33    |                 326.44 |                 316.42 |                 431.05 |
| TPC-DS Q34    |                  20.14 |                  20.56 |                  21.73 |
| TPC-DS Q35    |                 953.13 |                 960.19 |                 961.27 |
| TPC-DS Q36    |                  16.67 |                  20.83 |                  19.84 |
| TPC-DS Q37    |                 190.20 |                 383.73 |                 189.42 |
| TPC-DS Q38    |                1022.46 |                1375.93 |                1030.78 |
| TPC-DS Q39a+b |                1822.88 |                1838.23 |                2155.70 |
| TPC-DS Q40    |                 108.57 |                 107.57 |                 153.13 |
| TPC-DS Q41    |                 721.27 |                 775.94 |                 762.86 |
| TPC-DS Q42    |                  65.00 |                  63.05 |                  67.97 |
| TPC-DS Q43    |                  21.63 |                  20.76 |                  20.21 |
| TPC-DS Q44    |                 363.74 |                 356.02 |                 411.50 |
| TPC-DS Q45    |                  71.04 |                  71.55 |                  73.99 |
| TPC-DS Q46    |                  25.61 |                  27.40 |                  27.87 |
| TPC-DS Q47    |                1532.01 |                1797.48 |                1170.42 |
| TPC-DS Q48    |                 488.99 |                 479.31 |                 468.33 |
| TPC-DS Q49    |                 334.71 |                 328.72 |                 326.59 |
| TPC-DS Q50    |                 323.77 |                 309.97 |                 375.24 |
| TPC-DS Q51    |                 691.33 |                 646.80 |                 766.26 |
| TPC-DS Q52    |                  66.84 |                  62.71 |                 121.89 |
| TPC-DS Q53    |                  78.92 |                  73.44 |                 163.76 |
| TPC-DS Q54    |                  63.27 |                  62.51 |                 105.44 |
| TPC-DS Q55    |                  63.56 |                  61.18 |                 120.23 |
| TPC-DS Q56    |                 308.41 |                 298.90 |                 428.22 |
| TPC-DS Q57    |                 589.85 |                 649.97 |                 586.46 |
| TPC-DS Q58    |                 319.35 |                 303.87 |                 323.93 |
| TPC-DS Q59    |                 290.96 |                 288.42 |                 282.94 |
| TPC-DS Q60    |                 319.56 |                 307.62 |                 305.75 |
| TPC-DS Q61    |                 102.03 |                  97.53 |                 100.13 |
| TPC-DS Q62    |                  76.15 |                  73.38 |                  77.35 |
| TPC-DS Q63    |                  81.45 |                 123.29 |                  78.20 |
| TPC-DS Q64    |                 442.34 |                1094.73 |                 440.12 |
| TPC-DS Q65    |                 626.57 |                 586.61 |                 408.72 |
| TPC-DS Q66    |                 351.38 |                 172.55 |                 163.65 |
| TPC-DS Q67    |                2436.39 |                2311.29 |                2720.61 |
| TPC-DS Q68    |                  31.67 |                  29.93 |                  41.06 |
| TPC-DS Q69    |                 206.84 |                 200.94 |                 419.69 |
| TPC-DS Q70    |                 279.56 |                 282.03 |                 319.49 |
| TPC-DS Q71    |                 261.06 |                 258.98 |                 254.93 |
| TPC-DS Q72    |                 734.15 |                 743.40 |                 739.32 |
| TPC-DS Q73    |                  22.05 |                  22.01 |                  20.53 |
| TPC-DS Q74    |                 841.81 |                1185.84 |                 781.92 |
| TPC-DS Q75    |                 570.92 |                1415.90 |                 555.30 |
| TPC-DS Q76    |                 189.39 |                 186.56 |                 170.35 |
| TPC-DS Q77    |                 238.20 |                 250.86 |                 234.44 |
| TPC-DS Q78    |                1692.42 |                1409.04 |                1229.87 |
| TPC-DS Q79    |                 113.02 |                 111.79 |                 104.38 |
| TPC-DS Q80    |                 362.75 |                 352.65 |                 760.09 |
| TPC-DS Q81    |               32340.66 |               32888.77 |               34285.62 |
| TPC-DS Q82    |                 242.82 |                 234.56 |                 239.81 |
| TPC-DS Q83    |                  70.44 |                  69.56 |                  68.32 |
| TPC-DS Q84    |                  65.79 |                  69.72 |                  64.37 |
| TPC-DS Q85    |                 238.82 |                 257.74 |                 238.14 |
| TPC-DS Q86    |                 147.66 |                 165.17 |                 150.87 |
| TPC-DS Q87    |                1021.58 |                1045.36 |                1032.90 |
| TPC-DS Q88    |                1909.65 |                2299.74 |                1972.22 |
| TPC-DS Q89    |                 116.30 |                 118.70 |                 114.81 |
| TPC-DS Q90    |                 100.08 |                  88.12 |                  91.91 |
| TPC-DS Q91    |                  75.79 |                  73.01 |                  74.38 |
| TPC-DS Q92    |                  62.16 |                  62.31 |                  64.06 |
| TPC-DS Q93    |                 163.50 |                 159.26 |                 152.83 |
| TPC-DS Q94    |                 124.60 |                 140.77 |                 137.53 |
| TPC-DS Q95    |                2460.48 |                2452.51 |                2629.43 |
| TPC-DS Q96    |                  71.91 |                  72.11 |                  68.50 |
| TPC-DS Q97    |                 277.37 |                 281.39 |                 280.80 |
| TPC-DS Q98    |                 131.31 |                 134.46 |                 140.95 |
| TPC-DS Q99    |                 107.82 |                 107.61 |                 110.10 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                      |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:---------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| PostgreSQL-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| PostgreSQL-1-1-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
```

</details>

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
  -dbms PostgreSQL \
  -sf 1 \
  -nc 2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_storage_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1435s 
* Code: 1785196488
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.8.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:811054
  * volume_size:50G
  * volume_used:5.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785196488
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:811055
  * volume_size:50G
  * volume_used:5.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1785196488

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1785196488-55778c77c5-vsv7g: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      477.00 |           2.00 |            1.00 |        167.00 |          298.00 |              8 |           0 |             | None           |             0 | False         |                7.55 |
| PostgreSQL-1-2 |                2 |    1 |      477.00 |           2.00 |            1.00 |        167.00 |          298.00 |              8 |           0 |             | None           |             0 | False         |                7.55 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        175 |            0.30 |            12344.86 |           2036.57 |          -1 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |        220 |            0.39 |             9492.14 |           1620.00 |          -1 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |        175 |            0.30 |            12344.86 |           2036.57 |          -1 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               99 |        220 |            0.39 |             9492.14 |           1620.00 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:--------------|-----------------------:|-----------------------:|
| TPC-DS Q1     |                  93.62 |                7561.26 |
| TPC-DS Q2     |                 176.60 |               12176.55 |
| TPC-DS Q3     |                 140.86 |               18132.04 |
| TPC-DS Q4     |                6308.65 |                8457.55 |
| TPC-DS Q5     |                 359.16 |                2555.33 |
| TPC-DS Q6     |               52932.48 |               54066.11 |
| TPC-DS Q7     |                 299.28 |                4661.85 |
| TPC-DS Q8     |                  51.55 |                 126.47 |
| TPC-DS Q9     |                1700.51 |                2094.08 |
| TPC-DS Q10    |                1662.46 |                2359.01 |
| TPC-DS Q11    |                3953.10 |                4518.14 |
| TPC-DS Q12    |                  53.45 |                  53.82 |
| TPC-DS Q13    |                 469.79 |                 648.91 |
| TPC-DS Q14a+b |                2295.82 |                1531.42 |
| TPC-DS Q15    |                  90.79 |                  90.67 |
| TPC-DS Q16    |                 150.73 |                 416.35 |
| TPC-DS Q17    |                 331.39 |                 282.00 |
| TPC-DS Q18    |                 345.40 |                 319.80 |
| TPC-DS Q19    |                 116.30 |                 117.80 |
| TPC-DS Q20    |                  77.79 |                  77.96 |
| TPC-DS Q21    |                 171.23 |               11606.43 |
| TPC-DS Q22    |                3165.07 |                2916.53 |
| TPC-DS Q23a+b |                4038.67 |                4266.69 |
| TPC-DS Q24a+b |                1493.98 |                 513.82 |
| TPC-DS Q25    |                 265.06 |                 240.51 |
| TPC-DS Q26    |                 202.54 |                 278.22 |
| TPC-DS Q27    |                  21.56 |                  15.95 |
| TPC-DS Q28    |                 561.13 |                 538.30 |
| TPC-DS Q29    |                 270.70 |                 260.74 |
| TPC-DS Q30    |                7835.26 |                7312.17 |
| TPC-DS Q31    |                1430.45 |                1274.53 |
| TPC-DS Q32    |                 194.84 |                 111.94 |
| TPC-DS Q33    |                 820.47 |                 317.82 |
| TPC-DS Q34    |                  23.53 |                  21.06 |
| TPC-DS Q35    |                 941.87 |                 926.92 |
| TPC-DS Q36    |                  16.59 |                  18.93 |
| TPC-DS Q37    |                 238.19 |                 218.00 |
| TPC-DS Q38    |                1016.05 |                1301.66 |
| TPC-DS Q39a+b |                2907.38 |                2061.48 |
| TPC-DS Q40    |                 110.64 |                 121.28 |
| TPC-DS Q41    |                 744.11 |                 810.65 |
| TPC-DS Q42    |                  69.96 |                  64.41 |
| TPC-DS Q43    |                 131.12 |                 123.96 |
| TPC-DS Q44    |                   2.23 |                  85.34 |
| TPC-DS Q45    |                  71.44 |                  74.21 |
| TPC-DS Q46    |                  23.10 |                  23.48 |
| TPC-DS Q47    |                1542.97 |                1315.29 |
| TPC-DS Q48    |                 815.99 |                 457.40 |
| TPC-DS Q49    |                 322.84 |                 332.10 |
| TPC-DS Q50    |                 396.56 |                 322.69 |
| TPC-DS Q51    |                 656.40 |                 830.38 |
| TPC-DS Q52    |                  61.31 |                  81.60 |
| TPC-DS Q53    |                  80.14 |                  77.32 |
| TPC-DS Q54    |                  63.28 |                  62.77 |
| TPC-DS Q55    |                  63.89 |                  57.85 |
| TPC-DS Q56    |                 314.85 |                 303.16 |
| TPC-DS Q57    |                 676.63 |                 630.92 |
| TPC-DS Q58    |                 305.71 |                 294.49 |
| TPC-DS Q59    |                 284.25 |                 286.14 |
| TPC-DS Q60    |                 264.61 |                 262.78 |
| TPC-DS Q61    |                 103.09 |                  97.95 |
| TPC-DS Q62    |                  79.79 |                 179.77 |
| TPC-DS Q63    |                  80.08 |                  74.67 |
| TPC-DS Q64    |                 824.75 |                 485.94 |
| TPC-DS Q65    |                 697.74 |                 407.01 |
| TPC-DS Q66    |                 242.45 |                 700.54 |
| TPC-DS Q67    |                2236.41 |                2588.14 |
| TPC-DS Q68    |                  32.11 |                  31.49 |
| TPC-DS Q69    |                  92.07 |                 193.79 |
| TPC-DS Q70    |                 297.27 |                 280.90 |
| TPC-DS Q71    |                 262.73 |                 273.08 |
| TPC-DS Q72    |                 784.64 |                 758.44 |
| TPC-DS Q73    |                  20.73 |                  20.25 |
| TPC-DS Q74    |                 782.85 |                 746.32 |
| TPC-DS Q75    |                 600.35 |                 981.11 |
| TPC-DS Q76    |                 359.79 |                 268.34 |
| TPC-DS Q77    |                 446.30 |                 424.11 |
| TPC-DS Q78    |                1306.57 |                1018.02 |
| TPC-DS Q79    |                 120.42 |                 115.80 |
| TPC-DS Q80    |                 359.06 |                 359.20 |
| TPC-DS Q81    |               34502.58 |               32038.58 |
| TPC-DS Q82    |                 231.56 |                 229.51 |
| TPC-DS Q83    |                  69.69 |                  72.60 |
| TPC-DS Q84    |                  62.95 |                  68.36 |
| TPC-DS Q85    |                 236.34 |                 352.86 |
| TPC-DS Q86    |                 172.09 |                 204.17 |
| TPC-DS Q87    |                1025.10 |                1149.33 |
| TPC-DS Q88    |                2486.25 |                1923.72 |
| TPC-DS Q89    |                  90.20 |                  88.08 |
| TPC-DS Q90    |                  97.96 |                  87.19 |
| TPC-DS Q91    |                 115.56 |                 112.80 |
| TPC-DS Q92    |                  48.27 |                  45.55 |
| TPC-DS Q93    |                 150.79 |                 133.05 |
| TPC-DS Q94    |                 119.90 |                 204.58 |
| TPC-DS Q95    |                2696.18 |                2816.05 |
| TPC-DS Q96    |                  67.86 |                  91.84 |
| TPC-DS Q97    |                 321.84 |                 310.37 |
| TPC-DS Q98    |                 206.42 |                 157.19 |
| TPC-DS Q99    |                 267.80 |                 105.67 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                      |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:---------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| PostgreSQL-1-2-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
```

</details>


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

Here, we run it at TPC-DS SF=10 in PostgreSQL:


```bash
bexhoma tpcds \
  -dbms PostgreSQL \
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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_postgresql_profiling_summary.md" target="_blank" rel="noopener">docs_tpcds_postgresql_profiling.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Data Profiling SF=10
* Type: tpcds
* Duration: 1511s 
* Code: 1783024751
* We compute for all columns: Minimum, maximum, average, count, count distinct, count NULL and non NULL entries and coefficient of variation.
* This experiment compares imported TPC-DS data sets in different DBMS.
  * TPC-DS (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:676748
  * volume_size:50G
  * volume_used:50G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783024751
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:676753
  * volume_size:50G
  * volume_used:50G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783024751

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783024751-f9968dd55-kw6cv: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |    SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 | 10.00 |     1997.00 |           1.00 |            1.00 |        919.00 |         1069.00 |              8 |           0 |             | None           |             0 | False         |               18.03 |

### Execution

#### Per Connection


#### Per Phase



### Latency of Timer Execution [ms]

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1652.96 |      2.19 |          12.84 |                 37.64 |
| PostgreSQL-1-1-2-1 |      1652.96 |      2.19 |          12.84 |                 37.64 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       139.44 |      0.66 |           0.01 |                  2.82 |
| PostgreSQL-1-1-2-1 |       139.44 |      0.66 |           0.01 |                  2.82 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.26 |           3.74 |                 30.20 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.28 |           8.16 |                 40.21 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST failed: Geo Times [s] contains 0 or NaN
* TEST failed: Power@Size [~Q/h] contains 0 or NaN
* TEST failed: Throughput@Size contains 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

</details>













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

You can watch the status of experiments via `bexhoma status`.

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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_1_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_1.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-DS Queries SF=30
* Type: tpcds
* Duration: 2587s 
* Code: 1785198017
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=30) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 14400.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Database is persisted to disk of type shared and size 2000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 4 CPU and 1024Gi RAM. RAM limit is 1024Gi.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:808966
  * volume_size:2.0T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:1024Gi
  * limits_memory:1024Gi
  * eval_parameters
    * code:1785198017

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1785198017-584964766c-ghvn9: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |   30 |     1680.00 |          19.00 |            1.00 |        611.00 |         1031.00 |              8 |           0 |             | None           |             0 | False         |               64.29 |

### Execution

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |       1271 |            0.75 |           149185.98 |           8412.27 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 30.00 |               99 |       1271 |            0.75 |           149185.98 |           8412.27 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MonetDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |              288.11 |
| TPC-DS Q2     |             1979.46 |
| TPC-DS Q3     |              711.46 |
| TPC-DS Q4     |            15593.91 |
| TPC-DS Q5     |             1686.43 |
| TPC-DS Q6     |              517.96 |
| TPC-DS Q7     |              352.82 |
| TPC-DS Q8     |              294.70 |
| TPC-DS Q9     |              813.54 |
| TPC-DS Q10    |              155.84 |
| TPC-DS Q11    |             6191.11 |
| TPC-DS Q12    |              151.86 |
| TPC-DS Q13    |              506.86 |
| TPC-DS Q14a+b |            29041.90 |
| TPC-DS Q15    |              183.92 |
| TPC-DS Q16    |            42886.51 |
| TPC-DS Q17    |             2144.94 |
| TPC-DS Q18    |              919.24 |
| TPC-DS Q19    |              166.74 |
| TPC-DS Q20    |              130.16 |
| TPC-DS Q21    |              141.98 |
| TPC-DS Q22    |             1120.45 |
| TPC-DS Q23a+b |            49711.06 |
| TPC-DS Q24a+b |            25162.45 |
| TPC-DS Q25    |             2616.15 |
| TPC-DS Q26    |              244.52 |
| TPC-DS Q27    |             1278.48 |
| TPC-DS Q28    |              866.44 |
| TPC-DS Q29    |             1519.46 |
| TPC-DS Q30    |               87.40 |
| TPC-DS Q31    |             1926.08 |
| TPC-DS Q32    |              232.75 |
| TPC-DS Q33    |               99.64 |
| TPC-DS Q34    |              203.92 |
| TPC-DS Q35    |              976.48 |
| TPC-DS Q36    |             1143.53 |
| TPC-DS Q37    |              511.73 |
| TPC-DS Q38    |             2628.07 |
| TPC-DS Q39a+b |             1491.78 |
| TPC-DS Q40    |             1022.23 |
| TPC-DS Q41    |                8.27 |
| TPC-DS Q42    |              119.79 |
| TPC-DS Q43    |              288.39 |
| TPC-DS Q44    |              216.70 |
| TPC-DS Q45    |              147.13 |
| TPC-DS Q46    |              233.33 |
| TPC-DS Q47    |              835.90 |
| TPC-DS Q48    |              239.30 |
| TPC-DS Q49    |             1254.03 |
| TPC-DS Q50    |              561.76 |
| TPC-DS Q51    |             2483.18 |
| TPC-DS Q52    |              111.26 |
| TPC-DS Q53    |              101.63 |
| TPC-DS Q54    |              107.02 |
| TPC-DS Q55    |               85.25 |
| TPC-DS Q56    |              111.35 |
| TPC-DS Q57    |              135.91 |
| TPC-DS Q58    |             5326.37 |
| TPC-DS Q59    |             1141.37 |
| TPC-DS Q60    |              184.73 |
| TPC-DS Q61    |              365.66 |
| TPC-DS Q62    |              314.11 |
| TPC-DS Q63    |              113.65 |
| TPC-DS Q64    |             3907.05 |
| TPC-DS Q65    |             1034.50 |
| TPC-DS Q66    |             1770.44 |
| TPC-DS Q67    |             4552.48 |
| TPC-DS Q68    |              405.16 |
| TPC-DS Q69    |              315.45 |
| TPC-DS Q70    |             2349.17 |
| TPC-DS Q71    |              191.91 |
| TPC-DS Q72    |             1143.62 |
| TPC-DS Q73    |               83.45 |
| TPC-DS Q74    |             1749.93 |
| TPC-DS Q75    |             5312.18 |
| TPC-DS Q76    |             1340.61 |
| TPC-DS Q77    |              781.62 |
| TPC-DS Q78    |            12347.74 |
| TPC-DS Q79    |              234.85 |
| TPC-DS Q80    |             7332.41 |
| TPC-DS Q81    |              143.10 |
| TPC-DS Q82    |             1484.97 |
| TPC-DS Q83    |              261.03 |
| TPC-DS Q84    |               36.93 |
| TPC-DS Q85    |              882.09 |
| TPC-DS Q86    |              411.31 |
| TPC-DS Q87    |             2703.99 |
| TPC-DS Q88    |              565.03 |
| TPC-DS Q89    |              145.29 |
| TPC-DS Q90    |               98.36 |
| TPC-DS Q91    |               52.83 |
| TPC-DS Q92    |              194.85 |
| TPC-DS Q93    |             1930.47 |
| TPC-DS Q94    |            34490.63 |
| TPC-DS Q95    |           928120.49 |
| TPC-DS Q96    |             9390.99 |
| TPC-DS Q97    |             1187.65 |
| TPC-DS Q98    |              717.79 |
| TPC-DS Q99    |             1856.50 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      2853.66 |      7.28 |          50.31 |                 51.03 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         1.27 |      0.00 |           0.01 |                  0.01 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       441.11 |      1.09 |           0.03 |                  9.94 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |     41885.59 |    210.86 |         998.57 |               1024.00 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        25.16 |      0.40 |           0.38 |                  0.38 |

### Tests
* TEST passed: No SUT container restarts
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

</details>

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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_2_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_2.log</a></summary>

```markdown
## Show Summary

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

</details>

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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_monetdb_3_summary.md" target="_blank" rel="noopener">docs_tpcds_monetdb_3.log</a></summary>

```markdown
## Show Summary

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

</details>



