# Benchmark: HammerDB's TPC-C

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

HammerDB's TPC-C implementation does not allow scaling data generation and ingestion, but scaling the benchmarking driver.
It uses very little resources, but stresses the DBMS a lot. Scale-out can simulate distributed clients [4].

About the benchmark [1]:
> The TPC-C specification on which TPROC-C is based implements a computer system to fulfil orders from customers to supply products from a company. The company sells 100,000 items and keeps its stock in warehouses. Each warehouse has 10 sales districts and each district serves 3000 customers. The customers call the company whose operators take the order, each order containing a number of items. Orders are usually satisfied from the local warehouse however a small number of items are not in stock at a particular point in time and are supplied by an alternative warehouse. It is important to note that the size of the company is not fixed and can add Warehouses and sales districts as the company grows. For this reason your test schema can be as small or large as you wish with a larger schema requiring a more powerful computer system to process the increased level of transactions. The TPROC-C schema is shown below, in particular note how the number of rows in all of the tables apart from the ITEM table which is fixed is dependent upon the number of warehouses you choose to create your schema.

<img src="https://www.hammerdb.com/docs/resources/ch3-2.png" alt="drawing" width="600"/>

About the metrics [2]:
> HammerDB workloads produce 2 statistics to compare systems called **TPM** and NOPM respectively. NOPM value is based on a metric captured from within the test schema itself. As such **NOPM (New Orders per minute)** as a performance metric independent of any particular database implementation is the recommended primary metric to use.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References
1. HammerDB Docs: https://www.hammerdb.com/docs/ch03s05.html
1. HammerDB Docs: https://www.hammerdb.com/docs/ch03s04.html
1. HammerDB Docs: https://www.hammerdb.com/docs/ch03.html
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Perform Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [hammerdb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/hammerdb.py).

Example:
```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_scale.log &
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using 16 (`-nlt`) threads
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-sd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```bash
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+---------------------+--------------+--------------+---------------+-------------+
| 1726578005          | sut          |   loaded [s] | use case      | loading     |
+=====================+==============+==============+===============+=============+
| PostgreSQL-BHT-16-1 | (1. Running) |            1 | hammerdb_tpcc | (1 Running) |
+---------------------+--------------+--------------+---------------+-------------+
```

The code `1726578005` is the unique identifier of the experiment.
You can find the number also in the output of `hammerdb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1726578005` (removes everything that is related to experiment `1726578005`).

## Evaluate Results

At the end of a benchmark you will see a summary like

doc_hammerdb_testcase_scale.log
```markdown
﻿## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1340s 
    Code: 1769095941
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [16] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98727
    datadisk:3282
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1769095941
PostgreSQL-BHT-16-1-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:99566
    datadisk:4121
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1769095941

### Execution
                       experiment_run  vusers  client  pod_count  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1      16       1          1         0.0  13344.0  30463.0         5       0
PostgreSQL-BHT-16-1-2               1      16       2          2         0.0  17921.0  41146.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-16-1 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       84.0        1.0   1.0                 685.714286
PostgreSQL-BHT-16-1-2       84.0        1.0   2.0                 685.714286

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```

We can see that scaled-out drivers (2 pods with 8 threads each) have similar results as a monolithic driver (1 pod with 16 threads) - but are a bit weaker.

To see the summary again you can simply call `bexperiments summary -e 1708411664` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server in the cluster by `bexperiments dashboard`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888

You can connect to an evaluation server locally by `bexperiments jupyter`.
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

### Dockerfiles

The Dockerfiles for the components can be found in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/hammerdb

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python hammerdb.py -h`

```bash
usage: hammerdb.py [-h] [-aws] [-dbms [{PostgreSQL,MySQL,MariaDB,Citus} ...]] [-db] [-sl] [-cx CONTEXT] [-e EXPERIMENT] [-m] [-mc] [-ms MAX_SUT] [-dt] [-nr NUM_RUN] [-nc NUM_CONFIG]
                   [-ne NUM_QUERY_EXECUTORS] [-nw NUM_WORKER] [-nwr NUM_WORKER_REPLICAS] [-nws NUM_WORKER_SHARDS] [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS] [-nbp NUM_BENCHMARKING_PODS]
                   [-nbt NUM_BENCHMARKING_THREADS] [-nrt NUM_RAMPUP_TIME] [-sf SCALING_FACTOR] [-sd SCALING_DURATION] [-xlat] [-xkey] [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU]
                   [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING]
                   [-rnb REQUEST_NODE_BENCHMARKING] [-tr]
                   {run,start,load,summary}

Perform TPC-C inspired benchmarks in a Kubernetes cluster. Optionally monitoring is actived. User can also choose some parameters like number of warehouses and request some resources.

positional arguments:
  {run,start,load,summary}
                        start sut, also load data or also run the TPC-C queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms [{PostgreSQL,MySQL,MariaDB,Citus} ...], --dbms [{PostgreSQL,MySQL,MariaDB,Citus} ...]
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
  -dt, --datatransfer   activates datatransfer
  -nr NUM_RUN, --num-run NUM_RUN
                        number of runs per query
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
  -nrt NUM_RAMPUP_TIME, --num-rampup-time NUM_RAMPUP_TIME
                        Rampup time in minutes
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF) = number of warehouses
  -sd SCALING_DURATION, --scaling-duration SCALING_DURATION
                        scaling factor = duration in minutes
  -xlat, --extra-latency
                        also log latencies
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
```

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).
We in the following also activate measurement of latencies with `-xlat`.

Example:
```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -xlat \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_monitoring.log &
```

If monitoring is activated, the summary also contains a section like

doc_hammerdb_testcase_monitoring.log
```markdown
﻿## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1339s 
    Code: 1769097321
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [16] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98727
    datadisk:3282
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1769097321
PostgreSQL-BHT-16-1-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:99587
    datadisk:4142
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1769097321

### Execution
                       experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1      16       1          1     34.01     66.31         0.0  13242.0  30632.0         5       0
PostgreSQL-BHT-16-1-2               1      16       2          2     33.81     58.54         0.0  20703.5  47538.5         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       84.0        1.0   1.0                 685.714286
PostgreSQL-BHT-16-1-2       84.0        1.0   2.0                 685.714286

### Monitoring

### Loading phase: SUT deployment
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      113.98     1.52          7.77                 8.43
PostgreSQL-BHT-16-1-2      113.98     1.52          7.77                 8.43

### Loading phase: component loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      201.08        0          0.15                 0.15
PostgreSQL-BHT-16-1-2      201.08        0          0.15                 0.15

### Execution phase: SUT deployment
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      278.05     1.52           8.2                 9.04
PostgreSQL-BHT-16-1-2      373.24     0.89           8.6                 9.66

### Execution phase: component benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       50.21     0.12          0.14                 0.15
PostgreSQL-BHT-16-1-2       50.21     0.28          0.14                 0.15

### Tests
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.

In this example, metrics are very instable. Metrics are fetched every 30 seconds.
This is too coarse for such a quick example.


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms PostgreSQL \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_storage.log &
```

The following status shows we have two volumes of type `shared`.
Every experiment running HammerDB's TPC-C of SF=16 (warehouses) will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of PostgreSQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```bash
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                  | configuration   | experiment    | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-hammerdb-16   | postgresql      | hammerdb-16   | True         |               101 | PostgreSQL | shared               | 30Gi      | Bound    | 30G    | 4.8G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-hammerdb-128  | postgresql      | hammerdb-128  | True         |               369 | PostgreSQL | shared               | 50Gi      | Bound    | 50G    | 43G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

doc_hammerdb_testcase_storage.log
```markdown
﻿## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1689s 
    Code: 1769098732
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95452
    datadisk:3286
    volume_size:30G
    volume_used:3.3G
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1769098732
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95452
    datadisk:3784
    volume_size:30G
    volume_used:3.7G
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1769098732

### Execution
                        experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency    NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1-1               1      16       1          1    252.31    426.13         0.0  5993.0  13841.0         5       0
PostgreSQL-BHT-8-1-2-1               2      16       1          1    316.71    531.02         0.0  7069.0  16319.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1], [1]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1-1      195.0        1.0   1.0                 295.384615
PostgreSQL-BHT-8-1-2-1      195.0        1.0   1.0                 295.384615

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```

The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.
Also note the size descreases from first to second run (PostgreSQL does some cleaning?).

## Keying and Thinking Time

We can activate waiting times before and after execution of transactions with `-xkey` to follow TPC-C specifications more closely.
Also also make sure, the number of driver threads (`-nbt`) is 10 times the number of warehouses (`-sf`).

We at first remove persistent storage
```bash
kubectl delete pvc bexhoma-storage-postgresql-hammerdb-16
```

The keying and thinking times can be activated via `-xkey`:

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 160 \
  -sd 30 \
  -xlat \
  -xkey \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2,5,10 \
  -nbt 1600 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_keytime.log &
```

## Evaluate Results

doc_hammerdb_testcase_keytime.log
```markdown
﻿## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 6760s 
    Code: 1769100503
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 20 minutes. Benchmarking has keying and thinking times activated. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95452
    datadisk:3287
    volume_size:30G
    volume_used:3.3G
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1769100503
PostgreSQL-BHT-8-1-1-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95452
    datadisk:3357
    volume_size:30G
    volume_used:3.3G
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1769100503
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95452
    datadisk:3427
    volume_size:30G
    volume_used:3.4G
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1769100503
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95452
    datadisk:3447
    volume_size:30G
    volume_used:3.4G
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1769100503

### Execution
                        experiment_run  vusers  client  pod_count  efficiency   NOPM    TPM  duration  errors
PostgreSQL-BHT-8-1-1-1               1     160       1          1       97.20  200.0  464.0        20       0
PostgreSQL-BHT-8-1-1-2               1     160       2          2       97.20  200.0  466.0        20       0
PostgreSQL-BHT-8-1-2-1               2     160       1          1       97.69  201.0  460.0        20       0
PostgreSQL-BHT-8-1-2-2               2     160       2          2       98.42  202.5  466.0        20       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[2, 1], [2, 1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1, 2], [1, 2]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1-1      195.0        1.0   1.0                 295.384615
PostgreSQL-BHT-8-1-1-2      195.0        1.0   2.0                 295.384615
PostgreSQL-BHT-8-1-2-1      195.0        1.0   1.0                 295.384615
PostgreSQL-BHT-8-1-2-2      195.0        1.0   2.0                 295.384615

### Monitoring

### Loading phase: SUT deployment
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       93.45     0.59          7.59                 9.04
PostgreSQL-BHT-8-1-1-2       93.45     0.59          7.59                 9.04

### Loading phase: component loader
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       248.1     2.98          0.08                 0.09
PostgreSQL-BHT-8-1-1-2       248.1     2.98          0.08                 0.09

### Execution phase: SUT deployment
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       31.12     0.31          8.86                10.42
PostgreSQL-BHT-8-1-1-2       30.61     0.05          9.02                10.57
PostgreSQL-BHT-8-1-2-1      200.66     0.07          7.91                 9.56
PostgreSQL-BHT-8-1-2-2       39.44     0.07          8.05                 9.98

### Execution phase: component benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       23.80     0.06          0.58                 0.58
PostgreSQL-BHT-8-1-1-2       23.41     0.02          0.58                 0.58
PostgreSQL-BHT-8-1-2-1       26.34     0.07          0.58                 0.58
PostgreSQL-BHT-8-1-2-2       23.93     0.12          0.58                 0.58

### Tests
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```

Now also efficiency is computed via `100. * NOPM / 12.86 / sf`, when number of client threads is 10 times the number of warehouses:
* 100 makes it a percentage value
* NOPM is the number of new orders per minute
* sf is the number of warehouses
* 12.86 is the theoretical limit in the TPC-C speficications

Note that these are statistical values.

