# Example: HammerDB

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

About the benchmark [1]:
> The TPC-C specification on which TPROC-C is based implements a computer system to fulfil orders from customers to supply products from a company. The company sells 100,000 items and keeps its stock in warehouses. Each warehouse has 10 sales districts and each district serves 3000 customers. The customers call the company whose operators take the order, each order containing a number of items. Orders are usually satisfied from the local warehouse however a small number of items are not in stock at a particular point in time and are supplied by an alternative warehouse. It is important to note that the size of the company is not fixed and can add Warehouses and sales districts as the company grows. For this reason your test schema can be as small or large as you wish with a larger schema requiring a more powerful computer system to process the increased level of transactions. The TPROC-C schema is shown below, in particular note how the number of rows in all of the tables apart from the ITEM table which is fixed is dependent upon the number of warehouses you choose to create your schema.

<img src="https://www.hammerdb.com/docs/resources/ch3-2.png" alt="drawing" width="600"/>

About the metrics [2]:
> HammerDB workloads produce 2 statistics to compare systems called **TPM** and NOPM respectively. NOPM value is based on a metric captured from within the test schema itself. As such **NOPM (New Orders per minute)** as a performance metric independent of any particular database implementation is the recommended primary metric to use.

References
1. https://www.hammerdb.com/docs/ch03s05.html
1. https://www.hammerdb.com/docs/ch03s04.html
1. https://www.hammerdb.com/docs/ch03.html

## Perform Benchmark

For performing the experiment we can run the [hammerdb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/hammerdb.py).

Example:
```
python hammerdb.py -ms 1 \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 8 \
  run
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
    * `-nbp`: first stream 1 pos, second stream 2 pods (8 threads each)
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```
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

```bash
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
TPC-C data is generated and loaded using several threads.
Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
Benchmark is limited to DBMS P, o, s, t, g, r, e, S, Q, L.
Import is handled by 1 processes (pods).
Loading is tested with [16] threads, split into [1] pods.
Benchmarking is tested with [16] threads, split into [1, 2] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:313545868
    datadisk:3376692
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-16-1-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-117-generic
    node:cl-worker12
    disk:314521268
    datadisk:4352092
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1      16       1          1  13012.0  40471.0         5       0
PostgreSQL-BHT-16-1-2               1      16       2          2  11434.5  35596.5         5       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-16-1 - Pods [[2, 1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       84.0        1.0   1.0                 685.714286
PostgreSQL-BHT-16-1-2       84.0        1.0   2.0                 685.714286
TEST passed: NOPM contains no 0 or NaN
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
usage: hammerdb.py [-h] [-aws] [-dbms {PostgreSQL,MonetDB,SingleStore,CockroachDB,MySQL,MariaDB,YugabyteDB,Kinetica}] [-db] [-cx CONTEXT] [-e EXPERIMENT] [-m] [-mc] [-ms MAX_SUT] [-dt] [-nr NUM_RUN]
                   [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS] [-nbp NUM_BENCHMARKING_PODS] [-nbt NUM_BENCHMARKING_THREADS] [-nrt NUM_RAMPUP_TIME]
                   [-sf SCALING_FACTOR] [-sd SCALING_DURATION] [-t TIMEOUT] [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE]
                   [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME] [-rnl REQUEST_NODE_LOADING] [-rnb REQUEST_NODE_BENCHMARKING] [-tr]
                   {run,start,load,summary}

Perform TPC-C inspired benchmarks in a Kubernetes cluster. Optionally monitoring is actived. User can also choose some parameters like number of warehouses and request some resources.

positional arguments:
  {run,start,load,summary}
                        start sut, also load data or also run the TPC-C queries

options:
  -h, --help            show this help message and exit
  -aws, --aws           fix components to node groups at AWS
  -dbms {PostgreSQL,MonetDB,SingleStore,CockroachDB,MySQL,MariaDB,YugabyteDB,Kinetica}
                        DBMS to load the data
  -db, --debug          dump debug informations
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

If monitoring is activated, the summary also contains a section like

```bash
## Show Summary

### Workload
    HammerDB Workload SF=16 (warehouses for TPC-C)
    This includes no queries. HammerDB runs the benchmark
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
TPC-C data is generated and loaded using several threads.
Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
System metrics are monitored by a cluster-wide installation.
Benchmark is limited to DBMS P, o, s, t, g, r, e, S, Q, L.
Import is handled by 1 processes (pods).
Loading is fixed to cl-worker19.
Benchmarking is fixed to cl-worker19.
SUT is fixed to cl-worker11.
Loading is tested with [16] threads, split into [1] pods.
Benchmarking is tested with [16] threads, split into [1, 2] pods.
Benchmarking is run as [1] times the number of benchmarking pods.
Experiment is run once.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250283616
    datadisk:3377276
    requests_cpu:4
    requests_memory:16Gi
PostgreSQL-BHT-16-1-2 uses docker image postgres:16.1
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:251219648
    datadisk:4313308
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  vusers  client  pod_count     NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1      16       1          1  12447.0  38156.0         5       0
PostgreSQL-BHT-16-1-2               1      16       2          2  10576.5  32801.0         5       0

Warehouses: 16

### Workflow
DBMS PostgreSQL-BHT-16-1 - Pods [[2, 1]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       84.0        1.0   1.0                 685.714286
PostgreSQL-BHT-16-1-2       84.0        1.0   2.0                 685.714286

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       93.49     1.81          3.72                 4.38
PostgreSQL-BHT-16-1-2       93.49     1.81          3.72                 4.38

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      209.57        0          0.14                 0.14
PostgreSQL-BHT-16-1-2      209.57        0          0.14                 0.14

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1    26425.11    62.79          5.45                 6.22
PostgreSQL-BHT-16-1-2    26610.13    62.59          5.61                 6.59

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       46.97     0.14          0.06                 0.06
PostgreSQL-BHT-16-1-2       46.97     0.10          0.12                 0.12
TEST passed: NOPM contains no 0 or NaN
```

This gives a survey about CPU (in CPU seconds) and RAM usage (in Gb) during loading and execution of the benchmark.

In this example, metrics are very instable. Metrics are fetched every 30 seconds.
This is too coarse for such a quick example.


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```
python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -dbms PostgreSQL \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run
```

The following status shows we have two volumes of type `shared`.
Every experiment running HammerDB's TPC-C of SF=16 (warehouses) will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of PostgreSQL mounts the volume and generates the data.
All other instances just use the database without generating and loading data.

```
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                  | configuration   | experiment    | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-hammerdb-16   | postgresql      | hammerdb-16   | True         |               101 | PostgreSQL | shared               | 30Gi      | Bound    | 30G    | 4.8G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-hammerdb-128  | postgresql      | hammerdb-128  | True         |               369 | PostgreSQL | shared               | 50Gi      | Bound    | 50G    | 43G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```




