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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 478s 
* Code: 1794590048
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1139703
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794590048

### Ingestion
* PostgreSQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794590048-5fb97d7f9d-gdzcr: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       81.00 |           4.00 |           35.00 |          9.00 |           20.00 |              8 |         0 |             |                |             0 | False         |               44.44 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         15 |            0.29 |            13462.62 |           5280.00 |           0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         15 |            0.29 |            13462.62 |           5280.00 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1255.22 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 227.03 |
| Shipping Priority (TPC-H Q3)                        |                 478.72 |
| Order Priority Checking Query (TPC-H Q4)            |                 141.59 |
| Local Supplier Volume (TPC-H Q5)                    |                 204.32 |
| Forecasting Revenue Change (TPC-H Q6)               |                 211.00 |
| Volume Shipping Query (TPC-H Q7)                    |                 231.69 |
| National Market Share (TPC-H Q8)                    |                 119.64 |
| Product Type Profit Measure (TPC-H Q9)              |                 408.56 |
| Returned Item Reporting Query (TPC-H Q10)           |                 219.67 |
| Important Stock Identification (TPC-H Q11)          |                  60.51 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 346.05 |
| Customer Distribution (TPC-H Q13)                   |                 664.20 |
| Promotion Effect Query (TPC-H Q14)                  |                1377.08 |
| Top Supplier Query (TPC-H Q15)                      |                 239.80 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 151.43 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 579.20 |
| Large Volume Customer (TPC-H Q18)                   |                2471.23 |
| Discounted Revenue (TPC-H Q19)                      |                  41.86 |
| Potential Part Promotion (TPC-H Q20)                |                 114.87 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 367.55 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  68.57 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

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
usage: tpch.py [-h] [-aws] [-db] [-sl] [-ss] [-ar] [-cx CONTEXT]
               [-e EXPERIMENT] [-m] [-ma] [-mc] [-mm MONITORING_METRICS]
               [-ms MAX_SUT] [-mse MAX_SUT_EXPERIMENT]
               [-et EXPERIMENT_TIMEOUT] [-lt LOADING_TIMEOUT] [-nc NUM_CONFIG]
               [-ne NUM_QUERY_EXECUTORS] [-nw NUM_WORKER]
               [-nwr NUM_WORKER_REPLICAS] [-nws NUM_WORKER_SHARDS]
               [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS]
               [-nbp NUM_BENCHMARKING_PODS] [-nbt NUM_BENCHMARKING_THREADS]
               [-sf SCALING_FACTOR] [-t TIMEOUT] [-lr LIMIT_RAM]
               [-lc LIMIT_CPU] [-rr REQUEST_RAM] [-rc REQUEST_CPU]
               [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU]
               [-rgt REQUEST_GPU_TYPE] [-rst REQUEST_STORAGE_TYPE]
               [-rss REQUEST_STORAGE_SIZE] [-rsr] [-rsrp]
               [-rnn [REQUEST_NODE_NAME]] [-rnl [REQUEST_NODE_LOADING]]
               [-rnb [REQUEST_NODE_BENCHMARKING]]
               [-rnp [REQUEST_NODE_POOLING]] [-mtn MULTI_TENANT_NUM]
               [-mtb MULTI_TENANT_BY] [-mtv] [-tr] [-rp] [--set SETS]
               [-dbms [{PostgreSQL,MonetDB,MySQL,MariaDB,DatabaseService,Citus,CedarDB,PgDuckDB} ...]]
               [-xlit LIMIT_IMPORT_TABLE] [-xdt] [-xqr NUM_RUN]
               [-xnls NUM_LOADING_SPLIT] [-xii] [-xic] [-xis] [-xcol]
               [-xdim {replicated,distributed}] [-xrcp]
               [-xshq] [-xrs NUM_REFRESH_STREAMS]
               [-xrso NUM_REFRESH_STREAM_OFFSET] [-xaq ACTIVE_QUERIES] [-xdfe]
               [-xve] [-xse]
               {profiling,run,start,load,empty,summary}

Run TPC-H benchmark queries against a DBMS in Kubernetes. Data is generated on
a shared distributed filesystem and loaded in parallel. Supports optional
index, constraint, and statistics creation; multi-stream query ordering.

positional arguments:
  {profiling,run,start,load,empty,summary}
                        experiment phase: profile import, run queries, start
                        SUT only, load data, empty tables, or summarize
                        results

options:
  -h, --help            show this help message and exit
  -aws, --aws           pin components to AWS EKS node groups
  -db, --debug          enable debug logging
  -sl, --skip-loading   skip data loading and start benchmarking immediately
  -ss, --skip-shutdown  keep SUT pods running after the experiment finishes
  -ar, --activate-reset
                        activate configured reset scripts (e.g.
                        CHECKPOINT/VACUUM) when set on a benchmarker entry;
                        off by default
  -cx, --context CONTEXT
                        kubectl context to use (default: current context)
  -e, --experiment EXPERIMENT
                        resume an existing experiment by its code
  -m, --monitoring      enable Prometheus monitoring for the SUT
  -ma, --monitoring-app
                        enable application-level metrics collection
  -mc, --monitoring-cluster
                        enable node-level monitoring for the entire cluster
  -mm, --monitoring-metrics MONITORING_METRICS
                        switch single cluster-wide hardware metrics of
                        cluster.config on or off for this experiment,
                        overriding their 'active' flag, e.g.
                        total_gpu_util=on,total_network_rx=off; needs -m or
                        -mc
  -ms, --max-sut MAX_SUT
                        maximum number of DBMS configurations to run in
                        parallel cluster-wide (default: no limit)
  -mse, --max-sut-experiment MAX_SUT_EXPERIMENT
                        maximum number of DBMS configurations in this
                        experiment to run in parallel (default: no limit)
  -et, --experiment-timeout EXPERIMENT_TIMEOUT
                        maximum wall-clock duration of the experiment in
                        minutes; when exceeded, the experiment is stopped and
                        all its components are removed from the cluster
                        (default: no limit)
  -lt, --loading-timeout LOADING_TIMEOUT
                        maximum loading duration per configuration in minutes;
                        captures diagnostics and removes the experiment when
                        exceeded (default: no limit)
  -nc, --num-config NUM_CONFIG
                        number of experiment repetitions per configuration
  -ne, --num-query-executors NUM_QUERY_EXECUTORS
                        comma-separated list of parallel client counts to
                        sweep
  -nw, --num-worker NUM_WORKER
                        number of worker nodes for distributed DBMS
  -nwr, --num-worker-replicas NUM_WORKER_REPLICAS
                        number of replicas per worker node
  -nws, --num-worker-shards NUM_WORKER_SHARDS
                        number of shards per worker node
  -nlp, --num-loading-pods NUM_LOADING_PODS
                        comma-separated list of total loader pod counts
  -nlt, --num-loading-threads NUM_LOADING_THREADS
                        comma-separated list of total loader threads (split
                        across pods)
  -nbp, --num-benchmarking-pods NUM_BENCHMARKING_PODS
                        comma-separated list of benchmarker pod counts
  -nbt, --num-benchmarking-threads NUM_BENCHMARKING_THREADS
                        total benchmarking threads, split evenly across pods
  -sf, --scaling-factor SCALING_FACTOR
                        scaling factor controlling dataset size
  -t, --timeout TIMEOUT
                        per-query timeout in seconds
  -lr, --limit-ram LIMIT_RAM
                        RAM limit for the SUT and worker pods (e.g. 64Gi; 0 =
                        no limit); comma-separated to sweep several settings
                        (e.g. 32Gi,64Gi), one configuration per entry
  -lc, --limit-cpu LIMIT_CPU
                        CPU limit for the SUT and worker pods (e.g. 4; 0 = no
                        limit); comma-separated to sweep, must then match the
                        length of any other swept resource list
  -rr, --request-ram REQUEST_RAM
                        RAM request for the SUT and worker pods (e.g. 16Gi);
                        comma-separated to sweep several settings (e.g.
                        32Gi,64Gi), one configuration per entry
  -rc, --request-cpu REQUEST_CPU
                        CPU request for the SUT and worker pods (e.g. 4);
                        comma-separated to sweep, must then match the length
                        of any other swept resource list
  -rct, --request-cpu-type REQUEST_CPU_TYPE
                        require SUT node to carry label cpu=<value>
  -rg, --request-gpu REQUEST_GPU
                        number of GPUs to request for the SUT pod
  -rgt, --request-gpu-type REQUEST_GPU_TYPE
                        require SUT node to carry label gpu=<value>
  -rst, --request-storage-type REQUEST_STORAGE_TYPE
                        storage class for the SUT persistent volume ('' or
                        unset = ephemeral, 'ramdisk' = in-memory; other values
                        must be declared for the active cluster context, see
                        cluster config 'storage_classes'); comma-separated to
                        sweep the class, one configuration per entry and
                        paired by position with -rc/-lc/-rr/-lr, an empty
                        entry meaning ephemeral
  -rss, --request-storage-size REQUEST_STORAGE_SIZE
                        size of the SUT persistent volume (e.g. 10Gi)
  -rsr, --request-storage-remove
                        delete any existing PVC for the SUT before starting
  -rsrp, --request-storage-remove-per-repetition
                        delete the PVC of the SUT before every repetition
                        (-nc), so each repetition loads into a fresh volume;
                        implies -rsr
  -rnn, --request-node-name [REQUEST_NODE_NAME]
                        pin the SUT pod to this Kubernetes node
  -rnl, --request-node-loading [REQUEST_NODE_LOADING]
                        pin loader pods to this Kubernetes node
  -rnb, --request-node-benchmarking [REQUEST_NODE_BENCHMARKING]
                        pin benchmarker pods to this Kubernetes node
  -rnp, --request-node-pooling [REQUEST_NODE_POOLING]
                        pin pooling pods to this Kubernetes node
  -mtn, --multi-tenant-num MULTI_TENANT_NUM
                        number of tenants for multi-tenant experiments
  -mtb, --multi-tenant-by MULTI_TENANT_BY
                        tenancy granularity: schema, database, or container
  -mtv, --multi-tenant-volume
                        allocate a separate persistent volume per tenant
  -tr, --test-result    validate that results meet basic correctness
                        requirements
  -rp, --report         also write a tiered Markdown summary report
                        (report/index.md + detail files) to the result folder
  --set SETS            override a deployment parameter, e.g.
                        deployment[bexhoma-deployment-postgres].container[dbms].
                        max_worker_processes=128
  -dbms, --dbms [{PostgreSQL,MonetDB,MySQL,MariaDB,DatabaseService,Citus,CedarDB,PgDuckDB} ...]
                        one or more DBMS engines to test
  -xlit, --xlimit-import-table LIMIT_IMPORT_TABLE
                        import only this table (useful for partial re-loads)
  -xdt, --xdata-transfer
                        also measure data transfer volume per query
  -xqr, --xnum-query-runs NUM_RUN
                        number of times to repeat each query
  -xnls, --xnum-loading-split NUM_LOADING_SPLIT
                        number of parallel loader batches (total loaders ÷
                        this = batch size)
  -xii, --xinit-indexes
                        create indexes on all tables after loading
  -xic, --xinit-constraints
                        add primary-key and foreign-key constraints after
                        loading
  -xis, --xinit-statistics
                        run ANALYZE / UPDATE STATISTICS after loading
  -xcol, --xinit-columns
                        use columnar storage (Citus only)
  -xdim, --xdimensions {replicated,distributed}
                        ClickHouseCluster: replicated = a full copy of part,
                        partsupp, supplier and customer on every node, joins
                        with orders/lineitem run locally per shard;
                        distributed = these four spread over the shards like
                        orders and lineitem, joined across nodes per query;
                        nation and region are a full copy in both. Citus
                        always uses reference tables (distributed is
                        refused), single-node DBMS ignore it
  -xrcp, --xrecreate-parameter
                        regenerate random query parameters for each stream
  -xshq, --xshuffle-queries
                        shuffle query execution order independently per stream
  -xrs, --xnum-refresh-streams NUM_REFRESH_STREAMS
                        enable a TPC-H RF1/RF2 refresh stream running in
                        parallel with the query streams; value is the number
                        of RF1+RF2 pairs applied per benchmarking round (set
                        equal to the number of parallel query streams for a
                        spec-compliant throughput test; 0 = disabled)
  -xrso, --xrefresh-stream-offset NUM_REFRESH_STREAM_OFFSET
                        start the refresh stream at set OFFSET+1, so that sets
                        1..OFFSET are skipped (use to continue from a previous
                        run without re-applying already-applied sets)
  -xaq, --xactive-queries ACTIVE_QUERIES
                        comma-separated 1-based query numbers to run, e.g.
                        3,5,6,7 (all other queries are set inactive in the
                        query config uploaded to the cluster; unset = run all
                        queries as defined in the query config file)
  -xdfe, --xduckdb-force-execution
                        run queries on PostgreSQL tables in pg_duckdb's DuckDB
                        engine (PgDuckDB only); off by default, so they run in
                        PostgreSQL's own executor
  -xve, --xverbose-explain
                        run and print configured EXPLAIN statements after each
                        benchmark query (requires an 'explain' key in the DBMS
                        connection's JDBC config)
  -xse, --xstore-explain
                        run configured EXPLAIN statements after the first run
                        of each benchmark query and store the result in the
                        protocol (requires an 'explain' key in the DBMS
                        connection's JDBC config)
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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_monitoring_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 836s 
* Code: 1795120829
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 150Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:834187
  * datadisk:27210
  * volume_size:1.8T
  * volume_used:815G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795120829

### Ingestion
* PostgreSQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795120829-84d6ccc85-q9x6x: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   10 |      360.00 |           3.00 |           19.00 |         85.00 |          249.00 |              8 |         0 |             |                |             0 | False         |              100.00 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 10.00 |               22 |                  22 |        113 |            3.17 |            11623.87 |           7008.85 |           0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |                  22 |        113 |            3.17 |            11623.87 |           7008.85 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |               11097.48 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                2317.63 |
| Shipping Priority (TPC-H Q3)                        |                3929.73 |
| Order Priority Checking Query (TPC-H Q4)            |                2023.46 |
| Local Supplier Volume (TPC-H Q5)                    |                3226.83 |
| Forecasting Revenue Change (TPC-H Q6)               |                2766.73 |
| Volume Shipping Query (TPC-H Q7)                    |                3898.31 |
| National Market Share (TPC-H Q8)                    |                1805.72 |
| Product Type Profit Measure (TPC-H Q9)              |                9111.85 |
| Returned Item Reporting Query (TPC-H Q10)           |                7434.85 |
| Important Stock Identification (TPC-H Q11)          |                 719.72 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                3615.17 |
| Customer Distribution (TPC-H Q13)                   |                8015.30 |
| Promotion Effect Query (TPC-H Q14)                  |                2412.61 |
| Top Supplier Query (TPC-H Q15)                      |                2566.36 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1462.76 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                6267.14 |
| Large Volume Customer (TPC-H Q18)                   |               24639.59 |
| Discounted Revenue (TPC-H Q19)                      |                 348.85 |
| Potential Part Promotion (TPC-H Q20)                |                3703.40 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                3956.05 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 487.17 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       506.53 |      2.79 |           6.11 |                 21.60 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       122.04 |      1.67 |           0.00 |                  1.13 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       200.62 |      2.88 |          19.71 |                 35.64 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |        17.94 |      0.34 |           0.33 |                  0.33 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_throughput_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_throughput.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 501s 
* Code: 1794591453
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1154569
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794591453
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1155485
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794591453
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1155485
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794591453

### Ingestion
* PostgreSQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794591453-7c8cbf99d-vtm7d: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       48.00 |           4.00 |            5.00 |          9.00 |           24.00 |              8 |         0 |             |                |             0 | False         |               75.00 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         16 |            0.30 |            12831.93 |           4950.00 |           0 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         24 |            0.34 |            11184.82 |           3300.00 |           0 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 | 1.00 |               22 |                  22 |         24 |            0.34 |            11398.59 |           3300.00 |           0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         16 |            0.30 |            12831.93 |           4950.00 |           0 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               44 |                  44 |         24 |            0.34 |            11291.20 |           6600.00 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1629.52 |                1786.66 |                1754.68 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 207.30 |                 211.91 |                 224.56 |
| Shipping Priority (TPC-H Q3)                        |                 459.12 |                 419.63 |                 396.50 |
| Order Priority Checking Query (TPC-H Q4)            |                 137.49 |                 117.63 |                 143.03 |
| Local Supplier Volume (TPC-H Q5)                    |                 219.67 |                 237.17 |                 325.99 |
| Forecasting Revenue Change (TPC-H Q6)               |                 259.01 |                 242.48 |                 403.38 |
| Volume Shipping Query (TPC-H Q7)                    |                 257.80 |                 443.02 |                 301.99 |
| National Market Share (TPC-H Q8)                    |                 132.36 |                 193.00 |                 154.48 |
| Product Type Profit Measure (TPC-H Q9)              |                 444.50 |                 473.78 |                 485.90 |
| Returned Item Reporting Query (TPC-H Q10)           |                 250.82 |                 286.11 |                 260.80 |
| Important Stock Identification (TPC-H Q11)          |                  75.71 |                  80.51 |                  72.90 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 436.15 |                 375.31 |                 551.22 |
| Customer Distribution (TPC-H Q13)                   |                 728.21 |                 988.86 |                1244.74 |
| Promotion Effect Query (TPC-H Q14)                  |                 272.67 |                 444.81 |                 318.76 |
| Top Supplier Query (TPC-H Q15)                      |                 296.01 |                 352.62 |                 281.19 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 181.50 |                 227.12 |                 190.77 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 853.61 |                 646.11 |                 901.43 |
| Large Volume Customer (TPC-H Q18)                   |                2546.97 |                2987.43 |                2478.55 |
| Discounted Revenue (TPC-H Q19)                      |                  44.45 |                  49.06 |                  45.84 |
| Potential Part Promotion (TPC-H Q20)                |                 129.48 |                 110.06 |                 116.14 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 432.20 |                 493.55 |                 620.38 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  81.67 |                 216.25 |                  88.72 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_storage_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_storage.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 687s 
* Code: 1795120859
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.0.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:834716
  * datadisk:2757
  * volume_size:49G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795120859
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:834187
  * datadisk:2757
  * volume_size:49G
  * volume_used:2.7G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795120859

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: index_method=btree, btree_dedup=on, statistics_target=100, extended_statistics=off
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* PostgreSQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795120859-6789b67dd7-qx2mv: 0
* bexhoma-sut-postgresql-1-1795120859-54cb467774-nmz4f: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       77.00 |           2.00 |           41.00 |          7.00 |           18.00 |              8 |         0 |             |                |             0 | False         |               46.75 | False               |
| PostgreSQL-1-2 |                2 |    1 |       77.00 |           2.00 |           41.00 |          7.00 |           18.00 |              8 |         0 |             |                |             0 | False         |               46.75 | True                |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         14 |            0.28 |            13788.83 |           5657.14 |           0 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         21 |            0.39 |            10055.39 |           3771.43 |           0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         14 |            0.28 |            13788.83 |           5657.14 |           0 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         21 |            0.39 |            10055.39 |           3771.43 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1242.03 |                1626.73 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 166.66 |                1143.86 |
| Shipping Priority (TPC-H Q3)                        |                 385.31 |                5746.54 |
| Order Priority Checking Query (TPC-H Q4)            |                 111.79 |                 114.81 |
| Local Supplier Volume (TPC-H Q5)                    |                 207.08 |                 166.76 |
| Forecasting Revenue Change (TPC-H Q6)               |                 220.47 |                 202.82 |
| Volume Shipping Query (TPC-H Q7)                    |                 264.12 |                 216.32 |
| National Market Share (TPC-H Q8)                    |                 135.74 |                1018.67 |
| Product Type Profit Measure (TPC-H Q9)              |                 395.61 |                 702.84 |
| Returned Item Reporting Query (TPC-H Q10)           |                 245.87 |                 201.88 |
| Important Stock Identification (TPC-H Q11)          |                  56.06 |                  50.34 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 342.13 |                 320.80 |
| Customer Distribution (TPC-H Q13)                   |                 681.90 |                 626.22 |
| Promotion Effect Query (TPC-H Q14)                  |                1558.25 |                1243.97 |
| Top Supplier Query (TPC-H Q15)                      |                 258.10 |                 229.45 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 153.83 |                 147.86 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 519.15 |                 493.10 |
| Large Volume Customer (TPC-H Q18)                   |                2093.45 |                2039.33 |
| Discounted Revenue (TPC-H Q19)                      |                  44.59 |                 125.52 |
| Potential Part Promotion (TPC-H Q20)                |                 101.75 |                  90.73 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 369.90 |                 344.00 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  70.45 |                  70.29 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>


The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
`-rsr` removes the volume only before the first repetition (`-nc`); the second repetition finds it loaded, skips loading and copies the loading times (`loading_inherited` in the connections).
Use `-rsrp` instead to remove the volume before every repetition, so each repetition loads into a fresh volume and measures its own loading.
See [Concepts](Concepts.html) for details.
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

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_fractional_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_fractional.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=0.1
* Type: tpch
* Duration: 630s 
* Code: 1794593199
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=0.1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1125193
  * datadisk:316
  * volume_size:49G
  * volume_used:316M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794593199
* postgresql-1-2-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1123982
  * datadisk:316
  * volume_size:49G
  * volume_used:316M
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794593199

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: PostgreSQL-1-2

### Data Parameters of Reused Volumes
* PostgreSQL-1: DDL values of the volume: index_method=btree, btree_dedup=on, statistics_target=100, extended_statistics=off
* PostgreSQL-1: loading values of the volume: script=Schema, indexing=Index_and_Constraints_and_Statistics

### Ingestion
* PostgreSQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794593199-5655c6c874-8z5xq: 0
* bexhoma-sut-postgresql-1-1794593199-7cd686499c-9spp7: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 | 0.10 |       42.00 |           6.00 |           18.00 |          2.00 |           11.00 |              8 |         0 |             |                |             0 | False         |                8.57 | False               |
| PostgreSQL-1-2 |                2 | 0.10 |       42.00 |           6.00 |           18.00 |          2.00 |           11.00 |              8 |         0 |             |                |             0 | False         |                8.57 | True                |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 0.10 |               22 |                  22 |          7 |            0.04 |            10288.64 |           1131.43 |           0 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |       1 | 0.10 |               22 |                  22 |          6 |            0.05 |             7682.37 |           1320.00 |           0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 0.10 |               22 |                  22 |          7 |            0.04 |            10288.64 |           1131.43 |           0 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |        1 |               1 |           1 | 0.10 |               22 |                  22 |          6 |            0.05 |             7682.37 |           1320.00 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-2-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-2-1-1-1 |
|:----------------------------------------------------|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                 303.37 |                 372.20 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                  20.85 |                 280.44 |
| Shipping Priority (TPC-H Q3)                        |                  54.70 |                 115.34 |
| Order Priority Checking Query (TPC-H Q4)            |                  83.69 |                  65.54 |
| Local Supplier Volume (TPC-H Q5)                    |                  32.45 |                  25.47 |
| Forecasting Revenue Change (TPC-H Q6)               |                  27.18 |                  25.04 |
| Volume Shipping Query (TPC-H Q7)                    |                  37.72 |                  37.78 |
| National Market Share (TPC-H Q8)                    |                  34.19 |                  42.89 |
| Product Type Profit Measure (TPC-H Q9)              |                  86.03 |                 116.07 |
| Returned Item Reporting Query (TPC-H Q10)           |                  53.24 |                  47.56 |
| Important Stock Identification (TPC-H Q11)          |                   7.31 |                   6.91 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                  36.38 |                  53.12 |
| Customer Distribution (TPC-H Q13)                   |                  47.41 |                  45.32 |
| Promotion Effect Query (TPC-H Q14)                  |                  29.83 |                  27.34 |
| Top Supplier Query (TPC-H Q15)                      |                  25.18 |                  26.57 |
| Parts/Supplier Relationship (TPC-H Q16)             |                  29.21 |                  29.48 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                  52.02 |                  47.66 |
| Large Volume Customer (TPC-H Q18)                   |                 180.13 |                 244.14 |
| Discounted Revenue (TPC-H Q19)                      |                   6.03 |                   9.34 |
| Potential Part Promotion (TPC-H Q20)                |                   9.67 |                  26.26 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                  36.02 |                  38.56 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  11.28 |                  32.46 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>




## Reset Scripts

With `-ar`, a reset script runs before each benchmarking round (statistics, persist, counters; e.g. `VACUUM ANALYZE`, `CHECKPOINT` and a statistics reset for PostgreSQL), so every stream starts from a comparable state.
With a refresh stream (`-xrs`), it runs once per round, before both streams start.
See [Reset scripts](DBMS.md#reset-scripts--ar) for what each DBMS does.


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

The refresh stream has a loader image per SQL dialect and runs for these DBMS, with examples on their pages:
[MySQL](Example-MySQL.md#refresh-stream), [MariaDB](Example-MariaDB.md#refresh-stream), [MonetDB](Example-MonetDB.md#refresh-stream), [MariaDB ColumnStore](Example-MariaDBCS.md#refresh-stream), [PgDuckDB](Example-PgDuckDB.md#refresh-stream), [ClickHouse](Example-ClickHouse.md#refresh-stream), [Citus](Example-Citus.md#tpc-h-refresh-stream), [DatabaseService](Example-CloudDatabase.md#refresh-stream).
Which job a DBMS uses is its `refresh_template` in `cluster.config` (see [DBMS](DBMS.md#benchmarks-of-a-dbms)); CedarDB, Citus and DatabaseService use the one of PostgreSQL.

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_refresh_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_refresh.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 370s 
* Code: 1795120889
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * A TPC-H refresh stream (RF1+RF2) runs in parallel, with 3 pair(s) applied per round.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.0.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [3] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:830673
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:812G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795120889
* postgresql-1-1-1-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:830673
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:812G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795120889
* postgresql-1-1-1-1-3 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:830673
  * datadisk:2757
  * volume_size:1.8T
  * volume_used:812G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795120889

### Ingestion
* PostgreSQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1795120889-847c8f575-8cklm: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (3 pods), tpch_refresh (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |    1 |       64.00 |           2.00 |           29.00 |         10.00 |           19.00 |              8 |         0 |             |                |             0 | False         |               56.25 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         14 |            0.28 |            12801.54 |           5657.14 |           0 |
| postgresql-1-1-1-1-2 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       2 | 1.00 |               22 |                  22 |         12 |            0.27 |            13169.28 |           6600.00 |           0 |
| postgresql-1-1-1-1-3 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       3 | 1.00 |               22 |                  22 |         11 |            0.25 |            14136.77 |           7200.00 |           0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           3 | 1.00 |               66 |                  66 |         14 |            0.27 |            13357.49 |          16971.43 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| postgresql-1-1-1 |      3 | 3/3                                 | 3/3                                      | 3/3                            | 3/3                                        | 3/3                                | 3/3                                     | 3/3                                | 3/3                                | 3/3                                      | 3/3                                         | 3/3                                          | 3/3                                             | 3/3                                 | 3/3                                  | 3/3                              | 3/3                                       | 3/3                                        | 3/3                                 | 3/3                              | 3/3                                    | 3/3                                                   | 3/3                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### tpch_refresh

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count | benchmark_begin     | benchmark_end       |   benchmark_duration |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|:--------------------|:--------------------|---------------------:|
| postgresql-1-1-1-2-1 | postgresql-1-1-1 | postgresql-1-1-1-2 |                1 |        1 |               2 |           1 | 2026-11-19 21:46:48 | 2026-11-19 21:46:50 |                    2 |

### Latency of Timer Execution [ms]
| Queries                                             |   postgresql-1-1-1-1-1 |   postgresql-1-1-1-1-2 |   postgresql-1-1-1-1-3 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                3512.22 |                1506.82 |                1425.12 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 216.40 |                 173.09 |                 178.49 |
| Shipping Priority (TPC-H Q3)                        |                 811.38 |                 415.04 |                 410.32 |
| Order Priority Checking Query (TPC-H Q4)            |                 132.03 |                 128.06 |                 135.49 |
| Local Supplier Volume (TPC-H Q5)                    |                 204.39 |                 227.95 |                 225.83 |
| Forecasting Revenue Change (TPC-H Q6)               |                 225.05 |                 227.90 |                 227.84 |
| Volume Shipping Query (TPC-H Q7)                    |                 298.51 |                 281.00 |                 294.29 |
| National Market Share (TPC-H Q8)                    |                 135.30 |                 161.53 |                 162.04 |
| Product Type Profit Measure (TPC-H Q9)              |                 462.02 |                 435.39 |                 419.70 |
| Returned Item Reporting Query (TPC-H Q10)           |                 223.04 |                 232.22 |                 238.01 |
| Important Stock Identification (TPC-H Q11)          |                  68.29 |                  64.72 |                  64.72 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 353.03 |                 351.31 |                 348.44 |
| Customer Distribution (TPC-H Q13)                   |                 591.00 |                 610.38 |                 591.68 |
| Promotion Effect Query (TPC-H Q14)                  |                 248.22 |                 552.01 |                 247.80 |
| Top Supplier Query (TPC-H Q15)                      |                 258.98 |                 561.46 |                 262.87 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 258.67 |                 160.62 |                 161.28 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 506.73 |                 518.63 |                 498.55 |
| Large Volume Customer (TPC-H Q18)                   |                2636.41 |                2295.41 |                2102.00 |
| Discounted Revenue (TPC-H Q19)                      |                  58.62 |                  40.94 |                  44.48 |
| Potential Part Promotion (TPC-H Q20)                |                 101.88 |                 103.82 |                 103.14 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 377.65 |                 372.16 |                 373.82 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  68.01 |                  94.37 |                  97.69 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

The added `### tpch_refresh` section shows the wall-clock timing of the parallel refresh stream job: when it started, when it ended, and the total duration in seconds.

### Refresh Stream on two DBMS

With several DBMS in one experiment, each DBMS gets its own refresh stream, running against its own SUT beside its own query streams.
All of them use the same refresh job template, so the DBMS must declare the same `refresh_template`; bexhoma refuses the run otherwise.
PostgreSQL and PgDuckDB both use the job of PostgreSQL:

```bash
bexhoma tpch \
  -dbms PostgreSQL PgDuckDB \
  -xdfe \
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
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_refresh_two_dbms.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_refresh_two_dbms_summary.md" target="_blank" rel="noopener">docs_tpch_refresh_two_dbms.log</a></summary>

```markdown
(not run yet)
```

</details>


## Run a Subset of Queries

Not every iteration needs the full 22-query stream. `-xaq` restricts a run to the given 1-based query numbers; every other query is set inactive for this experiment's uploaded query config only — the query config files in [experiments/tpch/](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch) are never modified, so a later run without `-xaq` sees the full query set again.

Looking back at the [SF=10 monitoring example](#monitoring) above, Q1, Q18, Q14 and Q9 dominate total runtime (34.5s, 24.0s, 17.0s and 10.3s respectively), while every other query finishes in under 8.5s. When iterating on a tuning change (e.g. `shared_buffers` or `work_mem`), re-running just these four queries gives a fast read on whether the change helped, without waiting on the full stream.

Example:
```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xaq 1,9,14,18 \
  -xdt \
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
  run &>$LOG_DIR/docs_tpch_postgresql_subset.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_postgresql_subset_summary.md" target="_blank" rel="noopener">docs_tpch_postgresql_subset.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 725s 
* Code: 1794594284
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * Query selection is limited to Q1, Q9, Q14, Q18.
  * All instances use the same query parameters.
  * Timeout per query is 1800.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 150Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'random_page_cost', 'target': 'container'}, '1.1'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_io_concurrency', 'target': 'container'}, '200'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'io_method', 'target': 'container'}, 'io_uring'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers_per_gather', 'target': 'container'}, '2'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_parallel_workers', 'target': 'container'}, '4'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_worker_processes', 'target': 'container'}, '6'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'shared_buffers', 'target': 'container'}, '20GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'effective_cache_size', 'target': 'container'}, '48GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'work_mem', 'target': 'container'}, '1GB'), ({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'maintenance_work_mem', 'target': 'container'}, '2GB')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1156368
  * datadisk:27209
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=6', '-c', 'max_parallel_workers=4', '-c', 'max_parallel_workers_per_gather=2', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=20GB', '-c', 'effective_cache_size=48GB', '-c', 'work_mem=1GB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000', '-c', 'random_page_cost=1.1', '-c', 'effective_io_concurrency=200', '-c', 'io_method=io_uring']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794594284

### Ingestion
* PostgreSQL-1: 50 of 50 units ok

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1794594284-58bcff54bb-q98t4: 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PostgreSQL-1-1 |                1 |   10 |      359.00 |           4.00 |           23.00 |         76.00 |          252.00 |              8 |         0 |             |                |             0 | False         |              100.28 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 10.00 |                4 |                   4 |         49 |            8.87 |             4060.63 |           2938.78 |           0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |                4 |                   4 |         49 |            8.87 |             4060.63 |           2938.78 |           0 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Product Type Profit Measure (TPC-H Q9)   | Promotion Effect Query (TPC-H Q14)   | Large Volume Customer (TPC-H Q18)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------------|:------------------------------------|:-----------|
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                                  | 1/1                                 | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                |   postgresql-1-1-1-1-1 |
|:---------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)      |               11274.15 |
| Product Type Profit Measure (TPC-H Q9) |                9945.89 |
| Promotion Effect Query (TPC-H Q14)     |                2323.31 |
| Large Volume Customer (TPC-H Q18)      |               23713.74 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

In the resulting summary, `### Latency of Timer Execution` lists only Q1, Q9, Q14 and Q18; `num_of_queries` in `### Execution` drops to 4 accordingly, and `Power@Size` / `Geo Times` are computed over that reduced set only — so they are not comparable to a full-stream run.





















## MonetDB at SF 100

An example of MonetDB at SF=100, power and throughput test, is on [Example: Benchmark MonetDB](Example-MonetDB.md#tpc-h-at-sf-100).
