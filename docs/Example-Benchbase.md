# Benchmark: Benchbase's TPC-C

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Benchbase's TPC-C [1] implementation [2,5] does not allow scaling data generation and ingestion, but scaling the benchmarking driver.
It uses quite some resources, so that for simulating a lot of users, scale-out of the driver is necessary [6].

> TPC-C involves a mix of five concurrent transactions of different types and complexity either executed on-line or queued for deferred execution. The database is comprised of nine types of tables with a wide range of record and population sizes. TPC-C is measured in transactions per minute (tpmC). While the benchmark portrays the activity of a wholesale supplier, TPC-C is not limited to the activity of any particular business segment, but, rather represents any industry that must manage, sell, or distribute a product or service.

In Benchbase's implementation, for each warehouse the number of assigned threads is computed [3].
Each thread receives a fixed warehouse and a fixed number of districts and starts a connection [4].
There still can be deadlocks, because *A supplying warehouse number (OL_SUPPLY_W_ID) is selected as the home warehouse 99% of the time and as a remote warehouse 1% of the time* [1], and a new order sets a lock at the stock table.


<img src="https://raw.githubusercontent.com/wiki/cmu-db/benchbase/img/tpcc.png" alt="drawing" width="600"/>

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. TPC-C Homepage: https://www.tpc.org/tpcc/
1. Benchbase Repository: https://github.com/cmu-db/benchbase/wiki/TPC-C
1. Benchbase threads per warehouse: https://github.com/cmu-db/benchbase/blob/main/src/main/java/com/oltpbenchmark/benchmarks/tpcc/TPCCBenchmark.java
1. Benchbase connect: https://github.com/cmu-db/benchbase/blob/main/src/main/java/com/oltpbenchmark/api/BenchmarkModule.java#L82
1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Perform Benchmark

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

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_scale.log
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-xsd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-xtb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexhoma status`

```bash
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+---------------------+--------------+--------------+----------------+-----------------------------+
| 1726658756          | sut          |   loaded [s] | use case       | benchmarker                 |
+=====================+==============+==============+================+=============================+
| PostgreSQL-1-1-1024 | (1. Running) |           62 | benchbase_tpcc | (2. Succeeded) (2. Running) |
+---------------------+--------------+--------------+----------------+-----------------------------+
```

The code `1726658756` is the unique identifier of the experiment.
You can find the number also in the output of `benchbase.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1726658756` (removes everything that is related to experiment `1726658756`).

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_scale_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_scale.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1209s 
* Code: 1787827390
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.13.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:440416
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1787827390
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:378203
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1787827390
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1787827390-78895f6857-kmpj5: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      382.00 |           1.00 |            0.00 |        174.00 |          207.00 |              1 |           1 |             |                |             0 | False         |              150.79 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 |           0 | 300.00 |          109 |                       14653.09 |                    14446.42 |         0.00 |                                                      27267.00 |                                              10737.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 |           0 | 300.00 |           15 |                        4365.37 |                     4319.92 |         0.00 |                                                      37582.00 |                                              18306.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 |           0 | 300.00 |           11 |                        4355.89 |                     4311.02 |         0.00 |                                                      37546.00 |                                              18358.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         160 |    16384 |               1 |           1 |           0 | 300.00 |          109 |                       14653.09 |                    14446.42 |         0.00 |                                                      27267.00 |                                              10737.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |         160 |    16384 |               1 |           2 |           0 | 300.00 |           26 |                        8721.25 |                     8630.94 |         0.00 |                                                      37582.00 |                                              18332.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

We can see that the overall throughput is close to the target and that scaled-out drivers (2 pods with 8 threads each) have similar results as a monolithic driver (1 pod with 16 threads).

To see the summary again you can simply call `bexhoma summary -e 1708411664` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server in the cluster by `bexhoma dashboard`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

## Adjust Parameters

The script supports
* exact repetitions for statistical confidence
* variations to scan a large parameters space
* combine results for easy evaluation

There are various ways to change parameters.

### Manifests

The YAML manifests for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s

### SQL Scrips

The SQL scripts for pre and post ingestion can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/benchbase

There are per DBMS
* `initschema`-files, that are invoked before loading of data
* `checkschema`-files, that are invoked after loading of data

You can find the output of the files in the result folder.



### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/benchbase

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python benchbase.py -h`

```bash
usage: benchbase.py [-h] [-aws] [-dbms [{PostgreSQL,MySQL,MariaDB,YugabyteDB,CockroachDB,DatabaseService,Citus} ...]] [-db] [-sl] [-cx CONTEXT] [-e EXPERIMENT] [-m] [-mc] [-ms MAX_SUT] [-nc NUM_CONFIG]
                    [-ne NUM_QUERY_EXECUTORS] [-nw NUM_WORKER] [-nwr NUM_WORKER_REPLICAS] [-nws NUM_WORKER_SHARDS] [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS] [-nbp NUM_BENCHMARKING_PODS]
                    [-nbt NUM_BENCHMARKING_THREADS] [-xnbf NUM_BENCHMARKING_TARGET_FACTORS] [-sf SCALING_FACTOR] [-xsd SCALING_DURATION] [-xli SCALING_LOGGING] [-xkey] [-t TIMEOUT] [-rr REQUEST_RAM]
                    [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME]
                    [-rnl REQUEST_NODE_LOADING] [-rnb REQUEST_NODE_BENCHMARKING] [-tr] [-xbt {tpcc,twitter}] [-xtb TARGET_BASE]
                    {run,start,load}

Perform TPC-C inspired benchmarks based on Benchbase in a Kubernetes cluster. Optionally monitoring is actived. User can also choose some parameters like number of warehouses and request some resources.

positional arguments:
  {run,start,load}      start sut, also load data or also run the TPC-C queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms [{PostgreSQL,MySQL,MariaDB,YugabyteDB,CockroachDB,DatabaseService,Citus} ...], --dbms [{PostgreSQL,MySQL,MariaDB,YugabyteDB,CockroachDB,DatabaseService,Citus} ...]
                        DBMS to load the data
  -db, --debug          dump debug informations
  -sl, --skip-loading   do not ingest, start benchmarking immediately
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
  -e EXPERIMENT, --experiment EXPERIMENT
                        sets experiment code for continuing started experiment
  -m, --monitoring      activates monitoring for sut
  -mc, --monitoring-cluster
                        activates monitoring for all nodes of cluster
  -ms MAX_SUT, --max-sut MAX_SUT
                        maximum number of parallel DBMS configurations, default is no limit
  -nc NUM_CONFIG, --num-config NUM_CONFIG
                        number of runs per configuration
  -ne NUM_QUERY_EXECUTORS, --num-query-executors NUM_QUERY_EXECUTORS
                        comma separated list of number of parallel clients
  -nw NUM_WORKER, --num-worker NUM_WORKER
                        number of workers (for distributed dbms)
  -nwr NUM_WORKER_REPLICAS, --num-worker-replicas NUM_WORKER_REPLICAS
                        number of workers replications (for distributed dbms)
  -nws NUM_WORKER_SHARDS, --num-worker-shards NUM_WORKER_SHARDS
                        number of worker shards (for distributed dbms)
  -nlp NUM_LOADING_PODS, --num-loading-pods NUM_LOADING_PODS
                        total number of loaders per configuration
  -nlt NUM_LOADING_THREADS, --num-loading-threads NUM_LOADING_THREADS
                        total number of threads per loading process
  -nbp NUM_BENCHMARKING_PODS, --num-benchmarking-pods NUM_BENCHMARKING_PODS
                        comma separated list of number of benchmarkers per configuration
  -nbt NUM_BENCHMARKING_THREADS, --num-benchmarking-threads NUM_BENCHMARKING_THREADS
                        total number of threads per benchmarking process
  -xnbf NUM_BENCHMARKING_TARGET_FACTORS, --num-benchmarking-target-factors NUM_BENCHMARKING_TARGET_FACTORS
                        comma separated list of factors of 16384 ops as target - default range(1,9)
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF) = number of warehouses
  -xsd SCALING_DURATION, --scaling-duration SCALING_DURATION
                        scaling factor = duration in minutes
  -xli SCALING_LOGGING, --scaling-logging SCALING_LOGGING
                        logging status every x seconds
  -xkey, --extra-keying
                        activate keying and waiting time
  -t TIMEOUT, --timeout TIMEOUT
                        timeout for a run of a query
  -rr REQUEST_RAM, --request-ram REQUEST_RAM
                        request ram
  -rc REQUEST_CPU, --request-cpu REQUEST_CPU
                        request cpus
  -rct REQUEST_CPU_TYPE, --request-cpu-type REQUEST_CPU_TYPE
                        request node having node label cpu=
  -rg REQUEST_GPU, --request-gpu REQUEST_GPU
                        request number of gpus
  -rgt REQUEST_GPU_TYPE, --request-gpu-type REQUEST_GPU_TYPE
                        request node having node label gpu=
  -rst {None,,local-hdd,shared}, --request-storage-type {None,,local-hdd,shared}
                        request persistent storage of certain type
  -rss REQUEST_STORAGE_SIZE, --request-storage-size REQUEST_STORAGE_SIZE
                        request persistent storage of certain size
  -rnn REQUEST_NODE_NAME, --request-node-name REQUEST_NODE_NAME
                        request a specific node
  -rnl REQUEST_NODE_LOADING, --request-node-loading REQUEST_NODE_LOADING
                        request a specific node
  -rnb REQUEST_NODE_BENCHMARKING, --request-node-benchmarking REQUEST_NODE_BENCHMARKING
                        request a specific node
  -tr, --test-result    test if result fulfills some basic requirements
  -xbt {tpcc,twitter}, --benchmark {tpcc,twitter}
                        type of benchmark
  -xtb TARGET_BASE, --target-base TARGET_BASE
                        ops as target, base for factors - default 1024 = 2**10
```

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

Example:

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_monitoring.log
```

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_monitoring_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_monitoring.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1183s 
* Code: 1787828607
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.13.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:364384
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1787828607
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:479803
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1787828607
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1787828607-78b95c468c-8k5q4: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      315.00 |           1.00 |            0.00 |        136.00 |          178.00 |              1 |           1 |             |                |             0 | False         |              182.86 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 |           0 | 300.00 |          128 |                       12064.81 |                    11889.49 |         0.00 |                                                      31718.00 |                                              13221.00 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 |           0 | 300.00 |            4 |                        1107.30 |                     1095.08 |         0.00 |                                                     373936.00 |                                              72059.00 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 |           0 | 300.00 |            4 |                        1112.65 |                     1100.06 |         0.00 |                                                     369253.00 |                                              71833.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         160 |    16384 |               1 |           1 |           0 | 300.00 |          128 |                       12064.81 |                    11889.49 |         0.00 |                                                      31718.00 |                                              13221.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |         160 |    16384 |               1 |           2 |           0 | 300.00 |            8 |                        2219.95 |                     2195.14 |         0.00 |                                                     373936.00 |                                              71946.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       135.22 |      2.60 |           2.05 |                  3.69 |
| postgresql-1-1-2-1 |       135.22 |      2.60 |           2.05 |                  3.69 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1740.25 |     14.98 |           0.25 |                  0.25 |
| postgresql-1-1-2-1 |      1740.25 |     14.98 |           0.25 |                  0.25 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      4088.36 |     18.09 |           7.80 |                 12.95 |
| postgresql-1-1-2-1 |      1003.13 |      6.12 |           8.28 |                 14.07 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      4443.54 |     20.29 |           1.34 |                  1.34 |
| postgresql-1-1-2-1 |      4443.54 |      8.17 |           1.34 |                  1.34 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.

In this example, metrics are very instable. Metrics are fetched every 30 seconds.
This is too coarse for such a quick example.


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nc 2 \
  -nbp 1 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_storage.log
```

The following status shows we have two volumes of type `shared`.
Every PostgreSQL experiment running Benchbase's TPC-C of SF=16 (warehouses) will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of PostgreSQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```bash
+----------------------------------------------+-----------------+-------------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                      | configuration   | experiment        | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+==============================================+=================+===================+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-postgresql-benchbase-tpcc-16 | postgresql      | benchbase-tpcc-16 | True         |               184 | PostgreSQL      | shared               | 50Gi      | Bound    | 50G    | 4.8G   |
+----------------------------------------------+-----------------+-------------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_storage_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_storage.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2072s 
* Code: 1787829826
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.13.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:364053
  * volume_size:50G
  * volume_used:4.3G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1787829826
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:366886
  * volume_size:50G
  * volume_used:4.5G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1787829826
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1787829826-7dfc8bdd66-hptjz: 0 0
* bexhoma-sut-postgresql-1-1787829826-d4b8b785-2wh4z: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |     1576.00 |           2.00 |            0.00 |        746.00 |          828.00 |              1 |           1 |             |                |             0 | False         |               36.55 |
| PostgreSQL-1-2 |                2 |   16 |     1576.00 |           2.00 |            0.00 |        746.00 |          828.00 |              1 |           1 |             |                |             0 | False         |               36.55 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 |           0 | 300.00 |            1 |                         576.05 |                      572.24 |         0.00 |                                                    1288914.00 |                                             276997.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |         160 |    16384 |        1 |               1 |       1 |           0 | 300.00 |            1 |                         409.07 |                      406.60 |         0.00 |                                                    1792752.00 |                                             390564.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |         160 |    16384 |               1 |           1 |           0 | 300.00 |            1 |                         576.05 |                      572.24 |         0.00 |                                                    1288914.00 |                                             276997.00 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |         160 |    16384 |               1 |           1 |           0 | 300.00 |            1 |                         409.07 |                      406.60 |         0.00 |                                                    1792752.00 |                                             390564.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.
Also note the size increases from first to second run (benchmark writes data).

## Reset Scripts

For repeated benchmarking rounds against the same TPC-C database, bloat and stale planner statistics can drift the result away from the first round.
Bexhoma can run a pre-benchmark reset script (`CHECKPOINT` + `VACUUM ANALYZE` on all 9 TPC-C tables for PostgreSQL) before each round to start every round from a comparable state.
The feature is off by default; pass `-ar` to activate it.

Example (`-nc 2` repeats the experiment twice, so the reset script runs before each repeat):
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 2 \
  -nbp 1 \
  -nbt 40 \
  -ar \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_reset.log
```

The reset script's own stdout/stderr is saved next to the other per-DBMS SQL script logs in the result folder, one pair of files per repeat, e.g. `bexhoma-reset_1_1_1-postgresql-1-reset-benchbase.sql.log` / `.error`.

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_reset_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_reset.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=4
* Type: benchbase
* Duration: 1067s 
* Code: 1787831906
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 4. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 2 minutes. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Experiment uses bexhoma version 0.10.13.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [40] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:363458
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1787831906
    * TENANT_VOL:False
* postgresql-1-2-1-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:366787
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1787831906
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1787831906-7b7ff6f56-m42pk: 0 0
* bexhoma-sut-postgresql-1-1787831906-fb66c48fc-s7c5q: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    4 |      176.00 |           1.00 |            0.00 |         30.00 |          145.00 |              1 |           1 |             |                |             0 | False         |               81.82 |
| PostgreSQL-1-2 |                2 |    4 |       88.00 |           1.00 |            0.00 |         27.00 |           60.00 |              1 |           1 |             |                |             0 | False         |              163.64 |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |          40 |     1024 |        1 |               1 |       1 |           0 | 120.00 |            3 |                        1023.98 |                     1016.50 |         0.00 |                                                      12274.00 |                                               5842.00 |
| postgresql-1-2-1-1-1 | postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |          40 |     1024 |        1 |               1 |       1 |           0 | 120.00 |            0 |                        1023.97 |                     1016.21 |         0.00 |                                                      11833.00 |                                               4688.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |          40 |     1024 |               1 |           1 |           0 | 120.00 |            3 |                        1023.98 |                     1016.50 |         0.00 |                                                      12274.00 |                                               5842.00 |
| postgresql-1-2-1 | postgresql-1-2-1 |                2 |          40 |     1024 |               1 |           1 |           0 | 120.00 |            0 |                        1023.97 |                     1016.21 |         0.00 |                                                      11833.00 |                                               4688.00 |

#### Reset

| phase            | job                |   experiment_run |   client |   benchmark_run |   time_reset |
|:-----------------|:-------------------|-----------------:|---------:|----------------:|-------------:|
| postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |         2.00 |
| postgresql-1-2-1 | postgresql-1-2-1-1 |                2 |        1 |               1 |         1.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

The `#### Reset` section appears once per experiment repeat (`-nc 2`), right after `#### Per Phase`.
At SF=4 the 9 TPC-C tables are small, so `CHECKPOINT` + `VACUUM ANALYZE` finish in about 2 seconds here; at larger scaling factors this cost grows with table size and is worth comparing against the benchmarking duration itself.

## Keying and Thinking Time

We can activate waiting times before and after execution of transactions with `-xkey` to follow TPC-C specifications more closely.
Also also make sure, the number of driver threads (`-nbt`) is 10 times the number of warehouses (`-sf`).
Since `-nbt` can exceed the DBMS's connection limit at the largest pod count in the `-nbp` sweep, raise
`max_connections` accordingly with `--set`.

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 160 \
  -xsd 30 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1 \
  -nbp 1,2,5,10 \
  -nbt 1600 \
  -xkey \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rss 100Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=2000 \
  run &>$LOG_DIR/docs_benchbase_postgresql_keytime.log
```

## Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_postgresql_keytime_summary.md" target="_blank" rel="noopener">docs_benchbase_postgresql_keytime.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=160
* Type: benchbase
* Duration: 12976s 
* Code: 1787832981
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 160. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 30 minutes.
  * Experiment uses bexhoma version 0.10.13.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1600] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-postgres', 'config': '', 'container': 'dbms', 'param': 'max_connections'}, '2000')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* postgresql-1-1-1-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:373255
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1787832981
    * TENANT_VOL:False
* postgresql-1-1-2-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:378333
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1787832981
    * TENANT_VOL:False
* postgresql-1-1-3-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:383492
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1787832981
    * TENANT_VOL:False
* postgresql-1-1-4-1 uses docker image postgres:18.3
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:389435
  * volume_size:100G
  * volume_used:43G
  * cpu_list:0-223
  * args:['-c', 'max_connections=2000', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1787832981
    * TENANT_VOL:False

### SUT Container Restarts
* bexhoma-sut-postgresql-1-1787832981-cb75b5795-rwh9t: 0 0

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (10 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (10 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |  160 |     8665.00 |           1.00 |            0.00 |       4096.00 |         4568.00 |              1 |           1 |             |                |             0 | False         |               66.47 |

### Benchmarking

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1-1-1  | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1600 |     1024 |        1 |               1 |       1 |           0 | 1800.00 |            0 |                          75.90 |                       75.57 |        99.17 |                                                     548400.00 |                                             133666.00 |
| postgresql-1-1-2-1-1  | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |         800 |      512 |        2 |               1 |       1 |           0 | 1800.00 |            0 |                          37.88 |                       37.72 |        49.50 |                                                     638914.00 |                                             163413.00 |
| postgresql-1-1-2-1-2  | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |         800 |      512 |        2 |               1 |       2 |           0 | 1800.00 |            0 |                          37.97 |                       37.79 |        49.59 |                                                     626171.00 |                                             161275.00 |
| postgresql-1-1-3-1-1  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       1 |           0 | 1800.00 |            0 |                          15.23 |                       15.16 |        19.90 |                                                     637663.00 |                                             163128.00 |
| postgresql-1-1-3-1-2  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       2 |           0 | 1800.00 |            0 |                          15.36 |                       15.30 |        20.08 |                                                     608247.00 |                                             160115.00 |
| postgresql-1-1-3-1-3  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       3 |           0 | 1800.00 |            0 |                          15.22 |                       15.15 |        19.88 |                                                     620403.00 |                                             158827.00 |
| postgresql-1-1-3-1-4  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       4 |           0 | 1800.00 |            0 |                          15.02 |                       14.95 |        19.61 |                                                     648646.00 |                                             163488.00 |
| postgresql-1-1-3-1-5  | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |         320 |      204 |        3 |               1 |       5 |           0 | 1800.00 |            0 |                          15.20 |                       15.13 |        19.86 |                                                     627734.00 |                                             161776.00 |
| postgresql-1-1-4-1-1  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       1 |           0 | 1800.00 |            0 |                           7.50 |                        7.46 |         9.79 |                                                     707969.00 |                                             185400.00 |
| postgresql-1-1-4-1-2  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       2 |           0 | 1800.00 |            0 |                           7.60 |                        7.57 |         9.93 |                                                     710168.00 |                                             186289.00 |
| postgresql-1-1-4-1-3  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       3 |           0 | 1800.00 |            0 |                           7.55 |                        7.51 |         9.86 |                                                     725065.00 |                                             187981.00 |
| postgresql-1-1-4-1-4  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       4 |           0 | 1800.00 |            0 |                           7.55 |                        7.51 |         9.86 |                                                     707896.00 |                                             183602.00 |
| postgresql-1-1-4-1-5  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       5 |           0 | 1800.00 |            0 |                           7.53 |                        7.49 |         9.83 |                                                     690508.00 |                                             183456.00 |
| postgresql-1-1-4-1-6  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       6 |           0 | 1800.00 |            0 |                           7.57 |                        7.54 |         9.89 |                                                     713480.00 |                                             185164.00 |
| postgresql-1-1-4-1-7  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       7 |           0 | 1800.00 |            0 |                           7.55 |                        7.50 |         9.85 |                                                     711451.00 |                                             185728.00 |
| postgresql-1-1-4-1-8  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       8 |           0 | 1800.00 |            0 |                           7.57 |                        7.54 |         9.90 |                                                     719171.00 |                                             188075.00 |
| postgresql-1-1-4-1-9  | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |       9 |           0 | 1800.00 |            0 |                           7.51 |                        7.47 |         9.81 |                                                     707870.00 |                                             184112.00 |
| postgresql-1-1-4-1-10 | postgresql-1-1-4 | postgresql-1-1-4-1 |                1 |         160 |      102 |        4 |               1 |      10 |           0 | 1800.00 |            0 |                           7.51 |                        7.48 |         9.81 |                                                     693735.00 |                                             183244.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1600 |     1024 |               1 |           1 |           0 | 1800.00 |            0 |                          75.90 |                       75.57 |        99.17 |                                                     548400.00 |                                             133666.00 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        1600 |     1024 |               1 |           2 |           0 | 1800.00 |            0 |                          75.85 |                       75.52 |        99.09 |                                                     638914.00 |                                             162344.00 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        1600 |     1020 |               1 |           5 |           0 | 1800.00 |            0 |                          76.03 |                       75.70 |        99.33 |                                                     648646.00 |                                             161466.80 |
| postgresql-1-1-4 | postgresql-1-1-4 |                1 |        1600 |     1020 |               1 |          10 |           0 | 1800.00 |            0 |                          75.43 |                       75.09 |        98.53 |                                                     725065.00 |                                             185305.10 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |      1371.68 |      0.57 |          16.60 |                 32.54 |
| postgresql-1-1-2-1 |      1371.68 |      0.57 |          16.60 |                 32.54 |
| postgresql-1-1-3-1 |      1371.68 |      0.57 |          16.60 |                 32.54 |
| postgresql-1-1-4-1 |      1371.68 |      0.57 |          16.60 |                 32.54 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |     21174.08 |     15.88 |           0.29 |                  0.29 |
| postgresql-1-1-2-1 |     21174.08 |     15.88 |           0.29 |                  0.29 |
| postgresql-1-1-3-1 |     21174.08 |     15.88 |           0.29 |                  0.29 |
| postgresql-1-1-4-1 |     21174.08 |     15.88 |           0.29 |                  0.29 |

### Benchmarking phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       396.80 |      4.12 |          26.06 |                 42.33 |
| postgresql-1-1-2-1 |       269.93 |      0.31 |          26.11 |                 42.59 |
| postgresql-1-1-3-1 |       278.01 |      0.40 |          26.80 |                 43.47 |
| postgresql-1-1-4-1 |       288.97 |      0.50 |          27.41 |                 44.27 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| postgresql-1-1-1-1 |       387.23 |      2.10 |           4.18 |                  4.18 |
| postgresql-1-1-2-1 |       387.23 |      2.84 |           4.02 |                  4.02 |
| postgresql-1-1-3-1 |       568.38 |      5.33 |           2.48 |                  2.48 |
| postgresql-1-1-4-1 |       775.40 |      9.39 |           1.17 |                  1.17 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

</details>

Now also efficiency is computed via `0.45 * 60. * 100. * Goodput (requests/second) / 12.86 / sf`, when number of client threads is 10 times the number of warehouses:
* 45% is the average portion of new orders in the set of transactions
* 60 transforms to per-minute
* 100 makes it a percentage value
* Goodput (requests/second) is the number of successful transactions per second
* sf is the number of warehouses
* 12.86 is the theoretical limit in the TPC-C speficications

Note that these are statistical values.

