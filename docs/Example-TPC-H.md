# Benchmark: TPC-H

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TPC-H does allow scaling data generation and ingestion, and scaling the benchmarking driver.
Scale-out can simulate distributed clients for the loading test and the throughput test [2].

This example shows how to benchmark 22 reading queries Q1-Q22 derived from TPC-H in PostgreSQL.

> The query file is derived from the TPC-H and as such is not comparable to published TPC-H results, as the query file results do not comply with the TPC-H Specification.

1. Official TPC-H benchmark - http://www.tpc.org/tpch
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

For a comparison of multiple DBMS (PostgreSQL, MonetDB, MySQL, MariaDB) see [TestCases.md](TestCases.md#tpc-h).

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

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example:
```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_tpch_postgresql.log
```

This
* starts a clean instance of PostgreSQL
  * fixed 64 Gi RAM (request `-rr` and limit `-lr`)
  * data directory inside a Docker container
* creates TPC-H schema in the database
* starts 8 loader pods (`-nlp`)
  * with a data generator (init) container each
    * generating a portion of TPC-H data of scaling factor 1 (`-sf`)
    * storing the data in a distributed filesystem (shared disk)
    * if data is already present: do nothing
  * with a loading container each
    * importing TPC-H data from the distributed filesystem
    * loading uses 8 threads (`-nlt`)
* creates constraints (`-xic`) and indexes (`-xii`) and updates table statistics (`-xis`) after ingestion
* runs 1 stream of TPC-H queries
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
You can find the number also in the output of `tpch.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1706255897` (removes everything that is related to experiment `1706255897`).

## Evaluate Results

At the end of a benchmark you will see a summary like

docs_tpch_postgresql.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 443s 
* Code: 1783869695
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.5.
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

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1097530
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783869695

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783869695-68b8767f69-pdkxq: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 | 1.00 |      148.00 |           1.00 |           12.00 |         10.00 |          119.00 |              8 |           0 |             |                |             0 | False         |               24.32 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         17 |            0.32 |            12367.76 |           4658.82 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         17 |            0.32 |            12367.76 |           4658.82 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1308.06 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 156.60 |
| Shipping Priority (TPC-H Q3)                        |                 432.16 |
| Order Priority Checking Query (TPC-H Q4)            |                 221.26 |
| Local Supplier Volume (TPC-H Q5)                    |                 279.37 |
| Forecasting Revenue Change (TPC-H Q6)               |                 216.85 |
| Volume Shipping Query (TPC-H Q7)                    |                 273.63 |
| National Market Share (TPC-H Q8)                    |                 152.20 |
| Product Type Profit Measure (TPC-H Q9)              |                 435.01 |
| Returned Item Reporting Query (TPC-H Q10)           |                 234.60 |
| Important Stock Identification (TPC-H Q11)          |                  71.60 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 336.26 |
| Customer Distribution (TPC-H Q13)                   |                 644.09 |
| Promotion Effect Query (TPC-H Q14)                  |                1471.75 |
| Top Supplier Query (TPC-H Q15)                      |                 255.78 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 213.31 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 547.34 |
| Large Volume Customer (TPC-H Q18)                   |                2101.58 |
| Discounted Revenue (TPC-H Q19)                      |                  46.26 |
| Potential Part Promotion (TPC-H Q20)                |                 114.40 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 389.45 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 108.49 |

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

This gives a survey about the errors and warnings (result set mismatch) and the latencies of execution per query.
Moreover the loading times (schema creation, ingestion and indexing), the geometric mean of query execution times and the TPC-H metrics power and throughput are reported.
Please note that the results are not suitable for being published as official TPC-H results.
In particular the refresh streams are missing.

To see the summary again you can simply call `bexhoma summary -e 1759316196` with the experiment code.

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

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch

### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/tpch

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python tpch.py -h`

```bash
usage: tpch.py [-h] [-aws] [-dbms {PostgreSQL,MonetDB,MySQL,MariaDB}] [-xlit LIMIT_IMPORT_TABLE] [-db] [-cx CONTEXT] [-e EXPERIMENT] [-m] [-mc] [-ms MAX_SUT] [-xdt] [-xqr NUM_RUN] [-nc NUM_CONFIG]
               [-ne NUM_QUERY_EXECUTORS] [-xnls NUM_LOADING_SPLIT] [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS] [-nbp NUM_BENCHMARKING_PODS] [-nbt NUM_BENCHMARKING_THREADS] [-sf SCALING_FACTOR]
               [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE]
               [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING] [-rnb REQUEST_NODE_BENCHMARKING] [-tr] [-xii] [-xic] [-xis] [-xrcp] [-xshq]
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
  -xlit LIMIT_IMPORT_TABLE, --limit-import-table LIMIT_IMPORT_TABLE
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
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 10 \
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
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_tpch_postgresql_monitoring.log
```

If monitoring is activated, the summary also contains a section like this:

docs_tpch_postgresql_monitoring.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 886s 
* Code: 1783870170
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 150Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1138192
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783870170

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783870170-cc86f8ff9-c4v7p: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |    SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 | 10.00 |      528.00 |           1.00 |           20.00 |         93.00 |          412.00 |              8 |           0 |             |                |             0 | False         |               68.18 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        122 |            3.39 |            11087.42 |           6491.80 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        122 |            3.39 |            11087.42 |           6491.80 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               15302.71 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                3035.40 |
| Shipping Priority (TPC-H Q3)                        |                4946.30 |
| Order Priority Checking Query (TPC-H Q4)            |                2483.36 |
| Local Supplier Volume (TPC-H Q5)                    |                3396.75 |
| Forecasting Revenue Change (TPC-H Q6)               |                3294.93 |
| Volume Shipping Query (TPC-H Q7)                    |                3815.30 |
| National Market Share (TPC-H Q8)                    |                1883.31 |
| Product Type Profit Measure (TPC-H Q9)              |                7890.71 |
| Returned Item Reporting Query (TPC-H Q10)           |                7920.39 |
| Important Stock Identification (TPC-H Q11)          |                 668.32 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                3241.00 |
| Customer Distribution (TPC-H Q13)                   |                6860.57 |
| Promotion Effect Query (TPC-H Q14)                  |                2390.25 |
| Top Supplier Query (TPC-H Q15)                      |                2775.06 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1557.75 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                5984.62 |
| Large Volume Customer (TPC-H Q18)                   |               24891.15 |
| Discounted Revenue (TPC-H Q19)                      |                 330.44 |
| Potential Part Promotion (TPC-H Q20)                |                3877.89 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                4457.73 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 477.25 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       537.62 |      3.24 |           6.21 |                 21.28 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       117.74 |      1.53 |           0.01 |                  1.14 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       228.42 |      2.91 |          21.06 |                 36.49 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        18.86 |      0.34 |           0.33 |                  0.33 |

### Tests
* TEST passed: No SUT container restarts
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
PostgreSQL is fast, so we cannot see a lot (metrics are fetched every 30 seconds).


## Perform Benchmark - Throughput Test

For performing the experiment we can run the [tpch file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/tpch.py).

Example:
```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_tpch_postgresql_throughput.log
```

This runs 3 streams (`-ne`), the first one as a single stream and the following 2 in parallel.

docs_tpch_postgresql_throughput.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 546s 
* Code: 1783871139
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.5.
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

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1103034
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783871139
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1103347
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783871139
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1103347
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783871139

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783871139-76d95dc457-gcsrv: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 | 1.00 |      176.00 |           1.00 |           21.00 |         27.00 |          124.00 |              8 |           0 |             |                |             0 | False         |               20.45 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         16 |            0.29 |            13506.12 |           4950.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         18 |            0.32 |            12358.12 |           4400.00 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |         17 |            0.32 |            12342.66 |           4658.82 |           0 | PostgreSQL-1-1-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         16 |            0.29 |            13506.12 |           4950.00 |           0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               44 |         18 |            0.32 |            12350.39 |           8800.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1277.87 |                1982.16 |                2302.71 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 162.16 |                 194.80 |                 169.19 |
| Shipping Priority (TPC-H Q3)                        |                 424.45 |                 394.49 |                 359.63 |
| Order Priority Checking Query (TPC-H Q4)            |                 116.79 |                 124.32 |                 132.68 |
| Local Supplier Volume (TPC-H Q5)                    |                 198.09 |                 189.83 |                 211.62 |
| Forecasting Revenue Change (TPC-H Q6)               |                 218.52 |                 229.21 |                 243.17 |
| Volume Shipping Query (TPC-H Q7)                    |                 253.87 |                 272.71 |                 270.00 |
| National Market Share (TPC-H Q8)                    |                 140.15 |                 138.29 |                 128.10 |
| Product Type Profit Measure (TPC-H Q9)              |                 431.93 |                 475.66 |                 450.92 |
| Returned Item Reporting Query (TPC-H Q10)           |                 221.00 |                 260.01 |                 240.78 |
| Important Stock Identification (TPC-H Q11)          |                  47.90 |                  59.02 |                  46.05 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 331.00 |                 345.57 |                 370.01 |
| Customer Distribution (TPC-H Q13)                   |                 934.89 |                 719.15 |                 677.60 |
| Promotion Effect Query (TPC-H Q14)                  |                1687.17 |                2204.03 |                2097.47 |
| Top Supplier Query (TPC-H Q15)                      |                 250.10 |                 320.28 |                 254.25 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 205.58 |                 233.70 |                 234.58 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 499.51 |                 835.00 |                 700.97 |
| Large Volume Customer (TPC-H Q18)                   |                2723.30 |                2191.22 |                2507.89 |
| Discounted Revenue (TPC-H Q19)                      |                  40.89 |                  36.85 |                  46.93 |
| Potential Part Promotion (TPC-H Q20)                |                  83.27 |                  90.10 |                  99.71 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 368.63 |                 382.35 |                 387.68 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  70.21 |                  76.09 |                 102.08 |

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

All executions use the same database, so loading times are the same.

Per default, all 3 streams use the same random parameters (like DELTA in Q1) and run in ordering Q1-Q22.
You can change this via
* `-xrcp`: Each stream has it's own random parameters
* `-xshq`: Use the ordering per stream as required by the TPC-H specification

## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_tpch_postgresql_storage.log
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

docs_tpch_postgresql_storage.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1023s 
* Code: 1783871723
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.5.
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

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1069508
  * volume_size:50G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783871723
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1080988
  * volume_size:50G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783871723

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783871723-5d4c57f957-r788l: 1 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 | 1.00 |      248.00 |           3.00 |           21.00 |         58.00 |          163.00 |              8 |           0 |             |                |             0 | False         |               14.52 |
| PostgreSQL-1-2 |                2 | 1.00 |      248.00 |           3.00 |           21.00 |         58.00 |          163.00 |              8 |           0 |             |                |             0 | False         |               14.52 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         15 |            0.31 |            12589.45 |           5280.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |         40 |            0.51 |             7651.88 |           1980.00 |           0 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         15 |            0.31 |            12589.45 |           5280.00 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |         40 |            0.51 |             7651.88 |           1980.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1284.51 |                9926.34 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 172.56 |                6891.48 |
| Shipping Priority (TPC-H Q3)                        |                 432.31 |                7236.54 |
| Order Priority Checking Query (TPC-H Q4)            |                 116.62 |                 140.47 |
| Local Supplier Volume (TPC-H Q5)                    |                 207.07 |                 202.59 |
| Forecasting Revenue Change (TPC-H Q6)               |                 222.94 |                 219.59 |
| Volume Shipping Query (TPC-H Q7)                    |                 354.77 |                 243.91 |
| National Market Share (TPC-H Q8)                    |                 230.29 |                2159.42 |
| Product Type Profit Measure (TPC-H Q9)              |                 601.69 |                 593.35 |
| Returned Item Reporting Query (TPC-H Q10)           |                 448.45 |                 378.43 |
| Important Stock Identification (TPC-H Q11)          |                  80.81 |                  51.59 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 345.34 |                 333.43 |
| Customer Distribution (TPC-H Q13)                   |                 713.92 |                 665.33 |
| Promotion Effect Query (TPC-H Q14)                  |                1363.85 |                1428.52 |
| Top Supplier Query (TPC-H Q15)                      |                 238.42 |                 243.87 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 192.83 |                 216.97 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 461.69 |                 595.25 |
| Large Volume Customer (TPC-H Q18)                   |                2734.39 |                2155.85 |
| Discounted Revenue (TPC-H Q19)                      |                  37.15 |                  40.48 |
| Potential Part Promotion (TPC-H Q20)                |                  77.96 |                  89.86 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 344.55 |                 571.86 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  61.05 |                  73.95 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST failed: No SUT container restarts
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```


The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.


## Fractional Scaling Factor

TPC-H supports scaling factors that are fractional.
Example: SF=0.1

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 0.1 \
  -nc 2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_fractional.log
```

results in

docs_tpch_postgresql_fractional.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=0.1
* Type: tpch
* Duration: 855s 
* Code: 1783872777
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=0.1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.5.
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

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1070482
  * volume_size:50G
  * volume_used:316M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783872777
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1070483
  * volume_size:50G
  * volume_used:316M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783872777

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1783872777-68d66954f7-m4zbn: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 | 0.10 |      152.00 |           1.00 |           23.00 |         12.00 |          112.00 |              8 |           0 |             |                |             0 | False         |                2.37 |
| PostgreSQL-1-2 |                2 | 0.10 |      152.00 |           1.00 |           23.00 |         12.00 |          112.00 |              8 |           0 |             |                |             0 | False         |                2.37 |

### Execution

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          7 |            0.04 |             9303.85 |           1131.43 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |         11 |            0.07 |             5173.52 |            720.00 |           0 | PostgreSQL-1-2-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |          7 |            0.04 |             9303.85 |           1131.43 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |         11 |            0.07 |             5173.52 |            720.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 154.39 |                3214.34 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  21.86 |                1243.38 |
| Shipping Priority (TPC-H Q3)                        |                  47.09 |                 932.93 |
| Order Priority Checking Query (TPC-H Q4)            |                  61.70 |                  69.35 |
| Local Supplier Volume (TPC-H Q5)                    |                  21.86 |                  22.29 |
| Forecasting Revenue Change (TPC-H Q6)               |                  22.22 |                  22.35 |
| Volume Shipping Query (TPC-H Q7)                    |                  30.19 |                  31.94 |
| National Market Share (TPC-H Q8)                    |                  27.70 |                 252.84 |
| Product Type Profit Measure (TPC-H Q9)              |                  65.02 |                  82.54 |
| Returned Item Reporting Query (TPC-H Q10)           |                  80.16 |                  73.52 |
| Important Stock Identification (TPC-H Q11)          |                   8.99 |                   8.96 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  55.84 |                  84.61 |
| Customer Distribution (TPC-H Q13)                   |                 135.99 |                 133.06 |
| Promotion Effect Query (TPC-H Q14)                  |                  58.79 |                  66.00 |
| Top Supplier Query (TPC-H Q15)                      |                  52.82 |                  59.99 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  87.10 |                  88.28 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  53.29 |                  70.04 |
| Large Volume Customer (TPC-H Q18)                   |                 179.50 |                 170.20 |
| Discounted Revenue (TPC-H Q19)                      |                   5.72 |                   4.83 |
| Potential Part Promotion (TPC-H Q20)                |                  10.08 |                   7.44 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                  35.81 |                  31.72 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  11.18 |                  11.35 |

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




## Refresh Stream

TPC-H specifies RF1/RF2 operations that insert new orders and delete retired orders to keep the database current during a throughput test.
`-xrs N` enables a parallel refresh stream that applies N RF1+RF2 pairs per benchmarking round, running in parallel with the query streams.
For a spec-compliant throughput test, set N equal to the number of parallel query streams.

Example: 3 parallel query streams with 3 RF1+RF2 pairs:

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -ne 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -xrs 3 \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_tpch_postgresql_refresh.log
```

Use `-xrso N` to skip the first N already-applied refresh sets and continue from where a previous run stopped.

docs_tpch_postgresql_refresh.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 403s 
* Code: 1782123923
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.18.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222681
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782123923
* PostgreSQL-1-1-1-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222681
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782123923
* PostgreSQL-1-1-1-1-3 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222681
  * datadisk:2757
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782123923

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      130.00 |           0.00 |           26.00 |          8.00 |           92.00 |              8 |           0 |             |                |             0 | False         |               27.69 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         12 |            0.31 |            11746.33 |           6600.00 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-1-1-2 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         11 |            0.28 |            12864.84 |           7200.00 |           0 | PostgreSQL-1-1-1-1-2 |
| PostgreSQL-1-1-1-1-3 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         11 |            0.27 |            13331.73 |           7200.00 |           0 | PostgreSQL-1-1-1-1-3 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |         12 |            0.29 |            12629.84 |          19800.00 |           0 |

### tpch_refresh

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| PostgreSQL-1-1-1-2-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-06-22 12:30:55 | 2026-06-22 12:30:57 |                    2 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-2 |   PostgreSQL-1-1-1-1-3 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1197.84 |                1176.55 |                1150.63 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 268.23 |                 217.91 |                 222.31 |
| Shipping Priority (TPC-H Q3)                        |                 334.51 |                 299.32 |                 299.50 |
| Order Priority Checking Query (TPC-H Q4)            |                 168.19 |                 142.73 |                 136.14 |
| Local Supplier Volume (TPC-H Q5)                    |                 319.30 |                 268.36 |                 273.07 |
| Forecasting Revenue Change (TPC-H Q6)               |                 203.53 |                 172.29 |                 175.51 |
| Volume Shipping Query (TPC-H Q7)                    |                 375.95 |                 362.46 |                 319.35 |
| National Market Share (TPC-H Q8)                    |                 177.14 |                 205.04 |                 154.65 |
| Product Type Profit Measure (TPC-H Q9)              |                 551.16 |                 561.68 |                 524.43 |
| Returned Item Reporting Query (TPC-H Q10)           |                 388.02 |                 375.05 |                 352.49 |
| Important Stock Identification (TPC-H Q11)          |                  95.98 |                  85.49 |                  83.83 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 314.60 |                 276.47 |                 263.54 |
| Customer Distribution (TPC-H Q13)                   |                1020.60 |                 756.30 |                 764.17 |
| Promotion Effect Query (TPC-H Q14)                  |                 214.08 |                 209.07 |                 213.99 |
| Top Supplier Query (TPC-H Q15)                      |                 239.29 |                 218.29 |                 205.38 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 298.77 |                 247.62 |                 238.91 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 885.59 |                 663.58 |                 669.75 |
| Large Volume Customer (TPC-H Q18)                   |                3087.54 |                3061.66 |                2869.76 |
| Discounted Revenue (TPC-H Q19)                      |                  52.03 |                  52.47 |                  53.29 |
| Potential Part Promotion (TPC-H Q20)                |                 152.57 |                 142.48 |                 139.41 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 280.37 |                 284.46 |                 287.71 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 104.57 |                  98.09 |                  93.23 |

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

The added `### tpch_refresh` section shows the wall-clock timing of the parallel refresh stream job: when it started, when it ended, and the total duration in seconds.





















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
Afterwards the script creates contraints (`-xic`) and indexes (`-xii`) and updates table statistics (`-xis`).
The database is located in another shared disk of storageClass shared (`-rst`) and of size 1000Gi (`-rss`).

The script also runs a power test (`-ne` set to 1) with timeout 1200s (`-t`) and data transfer activated (`-xdt`) once (`-nc` set to 1).
To avoid conflicts with other experiments we set a maximum of 1 DBMS per time (`-ms`).
Monitoring is activated (`-m`) for all components (`-mc`).
The components, that is the SUT (`-rnn`) and the loader (`-rnl`) and the benchmark driver (`-rnb`), are fixed to specific nodes in the cluster.

```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR

bexhoma tpch \
  -dbms MonetDB \
  -sf 100 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 3600 \
  -lr 256Gi \
  -rr 256Gi \
  -rss 1000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb_1.log
```

### Status Data Disk

You can watch the status of the data disk via `bexhoma data`.

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

You can watch the status of experiments via `bexhoma status`.

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

docs_tpch_monetdb_1.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 25192s 
* Code: 1784006384
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type cephcsi and size 1000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1198794
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784006384

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1784006384-5c45c8fbb4-v77jt: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |     SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 | 100.00 |    19615.00 |          11.00 |           20.00 |       2047.00 |        17533.00 |              8 |           0 |             | None           |             0 | False         |               18.35 |

### Execution

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               21 |       5373 |            8.28 |            47743.39 |           1407.04 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               21 |       5373 |            8.28 |            47743.39 |           1407.04 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MonetDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           309827.03 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              547.05 |
| Shipping Priority (TPC-H Q3)                        |             6249.89 |
| Local Supplier Volume (TPC-H Q5)                    |           879691.18 |
| Forecasting Revenue Change (TPC-H Q6)               |             1518.85 |
| Volume Shipping Query (TPC-H Q7)                    |             4982.96 |
| National Market Share (TPC-H Q8)                    |            75733.41 |
| Product Type Profit Measure (TPC-H Q9)              |             7399.30 |
| Returned Item Reporting Query (TPC-H Q10)           |            11360.79 |
| Important Stock Identification (TPC-H Q11)          |              713.93 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             1591.71 |
| Customer Distribution (TPC-H Q13)                   |            34001.50 |
| Promotion Effect Query (TPC-H Q14)                  |              833.30 |
| Top Supplier Query (TPC-H Q15)                      |             1995.43 |
| Parts/Supplier Relationship (TPC-H Q16)             |             4567.27 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |             3689.23 |
| Large Volume Customer (TPC-H Q18)                   |             9213.20 |
| Discounted Revenue (TPC-H Q19)                      |             1831.63 |
| Potential Part Promotion (TPC-H Q20)                |             3653.47 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           391298.27 |
| Global Sales Opportunity Query (TPC-H Q22)          |             2270.00 |

### Errors (failed queries)

|                   |   Pricing Summary Report (TPC-H Q1) |   Minimum Cost Supplier Query (TPC-H Q2) |   Shipping Priority (TPC-H Q3) |   Order Priority Checking Query (TPC-H Q4) |   Local Supplier Volume (TPC-H Q5) |   Forecasting Revenue Change (TPC-H Q6) |   Volume Shipping Query (TPC-H Q7) |   National Market Share (TPC-H Q8) |   Product Type Profit Measure (TPC-H Q9) |   Returned Item Reporting Query (TPC-H Q10) |   Important Stock Identification (TPC-H Q11) |   Shipping Modes and Order Priority (TPC-H Q12) |   Customer Distribution (TPC-H Q13) |   Promotion Effect Query (TPC-H Q14) |   Top Supplier Query (TPC-H Q15) |   Parts/Supplier Relationship (TPC-H Q16) |   Small-Quantity-Order Revenue (TPC-H Q17) |   Large Volume Customer (TPC-H Q18) |   Discounted Revenue (TPC-H Q19) |   Potential Part Promotion (TPC-H Q20) |   Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |   Global Sales Opportunity Query (TPC-H Q22) |
|:------------------|------------------------------------:|-----------------------------------------:|-------------------------------:|-------------------------------------------:|-----------------------------------:|----------------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------------:|--------------------------------------------:|---------------------------------------------:|------------------------------------------------:|------------------------------------:|-------------------------------------:|---------------------------------:|------------------------------------------:|-------------------------------------------:|------------------------------------:|---------------------------------:|---------------------------------------:|------------------------------------------------------:|---------------------------------------------:|
| MonetDB-1-1-1-1-1 |                                0.00 |                                     0.00 |                           0.00 |                                       1.00 |                               0.00 |                                    0.00 |                               0.00 |                               0.00 |                                     0.00 |                                        0.00 |                                         0.00 |                                            0.00 |                                0.00 |                                 0.00 |                             0.00 |                                      0.00 |                                       0.00 |                                0.00 |                             0.00 |                                   0.00 |                                                  0.00 |                                         0.00 |
* Order Priority Checking Query (TPC-H Q4)
  * MonetDB-1-1-1-1-1: numRun 1: : java.sql.SQLNonTransientConnectionException: connection timed out

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      8738.85 |      5.95 |         181.43 |                181.43 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      1589.01 |      1.07 |           0.03 |                 13.29 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      1607.63 |      5.98 |         234.98 |                234.98 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        34.36 |      0.26 |           0.36 |                  0.37 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

To see the summary again you can simply call `bexhoma summary -e 1708411664` with the experiment code.

### List local results

You can inspect a preview list of results via `bexhoma localresults`.

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
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"

bexhoma tpch \
  -dbms MonetDB \
  -sf 100 \
  -nc 2 \
  -ne 1,1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 3600 \
  -lr 256Gi \
  -rr 256Gi \
  -rss 1000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb_2.log
```

### Evaluate Results

docs_tpch_monetdb_2.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 6522s 
* Code: 1784031723
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type cephcsi and size 1000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199512
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784031723
* MonetDB-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199623
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784031723
* MonetDB-1-2-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199627
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784031723
* MonetDB-1-2-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199547
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784031723

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1784031723-8696dddc47-bx4kf: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 2 Client 2: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |     SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 | 100.00 |    19615.00 |          11.00 |           20.00 |       2047.00 |        17533.00 |              0 |           0 |             | None           |             0 | False         |               18.35 |
| MonetDB-1-2 |                2 | 100.00 |    19615.00 |          11.00 |           20.00 |       2047.00 |        17533.00 |              0 |           0 |             | None           |             0 | False         |               18.35 |

### Execution

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |       2555 |           29.30 |            12545.21 |           3099.80 |          -1 | MonetDB-1-1-1-1-1 |
| MonetDB-1-1-2-1-1 | MonetDB-1       | MonetDB-1-1-2 | MonetDB-1-1-2-1 |                1 |        2 |               1 |           1 | 100.00 |               22 |        404 |            4.55 |            87693.30 |          19603.96 |          -1 | MonetDB-1-1-2-1-1 |
| MonetDB-1-2-1-1-1 | MonetDB-1       | MonetDB-1-2-1 | MonetDB-1-2-1-1 |                2 |        1 |               1 |           1 | 100.00 |               22 |       2321 |           25.18 |            14662.83 |           3412.32 |          -1 | MonetDB-1-2-1-1-1 |
| MonetDB-1-2-2-1-1 | MonetDB-1       | MonetDB-1-2-2 | MonetDB-1-2-2-1 |                2 |        2 |               1 |           1 | 100.00 |               22 |        430 |            4.67 |            86100.83 |          18418.60 |          -1 | MonetDB-1-2-2-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |       2555 |           29.30 |            12545.21 |           3099.80 |          -1 |
| MonetDB-1-1-2 | MonetDB-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |        404 |            4.55 |            87693.30 |          19603.96 |          -1 |
| MonetDB-1-2-1 | MonetDB-1-2-1 |                2 |        1 |               1 |           1 | 100.00 |               22 |       2321 |           25.18 |            14662.83 |           3412.32 |          -1 |
| MonetDB-1-2-2 | MonetDB-1-2-2 |                2 |        2 |               1 |           1 | 100.00 |               22 |        430 |            4.67 |            86100.83 |          18418.60 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MonetDB-1-1-1-1-1 |   MonetDB-1-1-2-1-1 |   MonetDB-1-2-1-1-1 |   MonetDB-1-2-2-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           380507.57 |            90166.21 |           343853.46 |            94150.05 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            39231.68 |              503.30 |            38819.07 |              505.91 |
| Shipping Priority (TPC-H Q3)                        |           159098.82 |             5773.04 |           156006.22 |             4681.90 |
| Order Priority Checking Query (TPC-H Q4)            |           146030.20 |             7882.44 |           138574.18 |             8816.53 |
| Local Supplier Volume (TPC-H Q5)                    |            16031.75 |             3267.06 |            11083.36 |             6807.39 |
| Forecasting Revenue Change (TPC-H Q6)               |             1254.08 |             1332.36 |             1124.13 |             1059.84 |
| Volume Shipping Query (TPC-H Q7)                    |             5744.71 |             4260.30 |             5906.07 |             4019.69 |
| National Market Share (TPC-H Q8)                    |           192159.04 |            12041.34 |           180176.18 |            12662.47 |
| Product Type Profit Measure (TPC-H Q9)              |            40472.91 |             5168.41 |            34297.40 |             4148.17 |
| Returned Item Reporting Query (TPC-H Q10)           |            74701.23 |             8165.85 |            61954.80 |             8937.97 |
| Important Stock Identification (TPC-H Q11)          |            11122.38 |              469.77 |             8195.91 |              466.09 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             9910.23 |             1073.95 |             3073.33 |             1390.82 |
| Customer Distribution (TPC-H Q13)                   |           317306.27 |            24164.25 |           263381.00 |            26818.89 |
| Promotion Effect Query (TPC-H Q14)                  |              754.77 |              653.23 |              749.29 |              743.20 |
| Top Supplier Query (TPC-H Q15)                      |            12347.46 |             1537.04 |             7246.03 |             1668.07 |
| Parts/Supplier Relationship (TPC-H Q16)             |             3641.21 |             2854.27 |             4290.91 |             2646.84 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |           505277.90 |             1581.20 |           537225.61 |             2117.78 |
| Large Volume Customer (TPC-H Q18)                   |            44862.74 |             7737.06 |            48272.88 |             8162.54 |
| Discounted Revenue (TPC-H Q19)                      |             2725.01 |             3260.81 |             2298.18 |             1276.69 |
| Potential Part Promotion (TPC-H Q20)                |            11586.14 |             3290.00 |            10210.86 |             2633.67 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           546989.89 |           197237.61 |           429840.06 |           212197.41 |
| Global Sales Opportunity Query (TPC-H Q22)          |            10919.43 |             1769.46 |            11616.96 |             2474.70 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |       986.35 |      2.51 |         120.22 |                120.22 |
| MonetDB-1-1-2-1 |       857.75 |      7.19 |         181.10 |                181.10 |
| MonetDB-1-2-1-1 |      1871.10 |      5.75 |         136.40 |                136.40 |
| MonetDB-1-2-2-1 |       902.30 |      6.21 |         193.39 |                193.39 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        31.80 |      0.21 |           0.40 |                  0.42 |
| MonetDB-1-1-2-1 |        31.80 |      0.43 |           0.40 |                  0.42 |
| MonetDB-1-2-1-1 |        32.37 |      0.32 |           0.40 |                  0.42 |
| MonetDB-1-2-2-1 |        32.37 |      0.29 |           0.40 |                  0.42 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

### Perform Benchmark - Throughput Test

We now start a new instance of MonetDB and mount the existing database: we use the prepared database on the shared disk.
We then run two power tests, one after the other, and then a throughput test with 3 parallel driver (`-ne 1,1,3`). and shut down the DBMS.


```bash
mkdir -p ./logs/
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"

bexhoma tpch \
  -dbms MonetDB \
  -sf 100 \
  -nc 1 \
  -ne 1,1,3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 3600 \
  -lr 256Gi \
  -rr 256Gi \
  -rss 1000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_monetdb_3.log
```

### Evaluate Results

docs_tpch_monetdb_3.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 5775s 
* Code: 1784038339
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type cephcsi and size 1000Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 1, 3] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199550
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784038339
* MonetDB-1-1-2-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199462
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784038339
* MonetDB-1-1-3-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199464
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784038339
* MonetDB-1-1-3-1-2 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199464
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784038339
* MonetDB-1-1-3-1-3 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1199464
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1784038339

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1784038339-7cb6467b-8bnds: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpch (3 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 2: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 3: tpch (3 pods)

### Loading

#### Per Run

|             |   experiment_run |     SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-------:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 | 100.00 |    19615.00 |          11.00 |           20.00 |       2047.00 |        17533.00 |              0 |           0 |             | None           |             0 | False         |               18.35 |

### Execution

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |       2360 |           25.85 |            14292.09 |           3355.93 |          -1 | MonetDB-1-1-1-1-1 |
| MonetDB-1-1-2-1-1 | MonetDB-1       | MonetDB-1-1-2 | MonetDB-1-1-2-1 |                1 |        2 |               1 |           1 | 100.00 |               22 |        409 |            4.32 |            91829.06 |          19364.30 |          -1 | MonetDB-1-1-2-1-1 |
| MonetDB-1-1-3-1-1 | MonetDB-1       | MonetDB-1-1-3 | MonetDB-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |       2521 |           20.09 |            18687.70 |           3141.61 |          -1 | MonetDB-1-1-3-1-1 |
| MonetDB-1-1-3-1-2 | MonetDB-1       | MonetDB-1-1-3 | MonetDB-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |       2561 |           20.48 |            18347.50 |           3092.54 |          -1 | MonetDB-1-1-3-1-2 |
| MonetDB-1-1-3-1-3 | MonetDB-1       | MonetDB-1-1-3 | MonetDB-1-1-3-1 |                1 |        3 |               1 |           1 | 100.00 |               22 |       2583 |           23.95 |            15672.80 |           3066.20 |          -1 | MonetDB-1-1-3-1-3 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |       2360 |           25.85 |            14292.09 |           3355.93 |          -1 |
| MonetDB-1-1-2 | MonetDB-1-1-2 |                1 |        2 |               1 |           1 | 100.00 |               22 |        409 |            4.32 |            91829.06 |          19364.30 |          -1 |
| MonetDB-1-1-3 | MonetDB-1-1-3 |                1 |        3 |               1 |           3 | 100.00 |               66 |       2583 |           21.44 |            17515.66 |           9198.61 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MonetDB-1-1-1-1-1 |   MonetDB-1-1-2-1-1 |   MonetDB-1-1-3-1-1 |   MonetDB-1-1-3-1-2 |   MonetDB-1-1-3-1-3 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           345510.64 |            83581.58 |           432792.46 |           378821.83 |           365983.77 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            37824.54 |              505.99 |              470.61 |             3942.92 |            17136.05 |
| Shipping Priority (TPC-H Q3)                        |           145121.22 |             4339.19 |            44586.97 |            95130.53 |            94589.62 |
| Order Priority Checking Query (TPC-H Q4)            |           150159.15 |             7972.45 |            40322.32 |            39343.29 |            39730.09 |
| Local Supplier Volume (TPC-H Q5)                    |            13639.77 |             2576.59 |            13308.41 |            13211.69 |            13738.45 |
| Forecasting Revenue Change (TPC-H Q6)               |             1588.79 |             1405.06 |             5177.03 |             6929.45 |             5369.13 |
| Volume Shipping Query (TPC-H Q7)                    |             5796.60 |             4632.13 |             8293.63 |             7398.56 |             9809.22 |
| National Market Share (TPC-H Q8)                    |           205834.17 |            12995.63 |           202545.83 |           203563.03 |           202491.55 |
| Product Type Profit Measure (TPC-H Q9)              |            33555.04 |             3745.82 |            30535.53 |            28597.56 |            28434.93 |
| Returned Item Reporting Query (TPC-H Q10)           |            73743.04 |             7570.81 |            39307.30 |            39826.66 |            40103.74 |
| Important Stock Identification (TPC-H Q11)          |             7787.35 |              480.61 |             2673.13 |             2584.45 |             2508.71 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3202.88 |             1356.21 |             3709.38 |             3200.02 |             4097.94 |
| Customer Distribution (TPC-H Q13)                   |           283869.91 |            24407.00 |           225427.59 |           226670.62 |           221943.77 |
| Promotion Effect Query (TPC-H Q14)                  |              594.09 |              743.50 |              468.74 |              774.16 |              748.18 |
| Top Supplier Query (TPC-H Q15)                      |             6460.85 |             2143.70 |             3580.36 |             1818.34 |             6571.20 |
| Parts/Supplier Relationship (TPC-H Q16)             |             3662.20 |             2986.18 |             5686.28 |             5500.22 |             5497.51 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |           531005.84 |             1634.87 |           571005.52 |           571663.09 |           571519.36 |
| Large Volume Customer (TPC-H Q18)                   |            58555.41 |             7240.35 |            71217.61 |            73774.63 |            71086.52 |
| Discounted Revenue (TPC-H Q19)                      |             3125.98 |             1207.09 |             4145.76 |             1205.47 |             3916.92 |
| Potential Part Promotion (TPC-H Q20)                |            10407.51 |             3100.78 |            15472.85 |            15281.05 |            15004.89 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           407037.27 |           212794.11 |           771345.24 |           817269.84 |           840518.32 |
| Global Sales Opportunity Query (TPC-H Q22)          |             8983.04 |             1750.74 |             8420.04 |             3403.99 |             1809.50 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      1026.48 |      2.98 |         120.02 |                120.02 |
| MonetDB-1-1-2-1 |       822.70 |      4.64 |         192.97 |                192.97 |
| MonetDB-1-1-3-1 |      2823.36 |      5.78 |         253.95 |                255.99 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        31.55 |      0.34 |           0.38 |                  0.39 |
| MonetDB-1-1-2-1 |        31.55 |      0.36 |           0.38 |                  0.39 |
| MonetDB-1-1-3-1 |        71.71 |      0.76 |           0.39 |                  0.40 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.



