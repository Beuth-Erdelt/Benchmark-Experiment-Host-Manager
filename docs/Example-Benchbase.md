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

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

Example:
```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_scale.log &
```

This
* starts a clean instance of PostgreSQL (`-dbms`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-sd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-tb`) ops
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

doc_benchbase_testcase_scale.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 84194s 
    Code: 1752161627
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.9.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:427291092
    datadisk:3844
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1752161627
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:432783456
    datadisk:9168
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1752161627

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1        160   16384       1      1  300.0          55                    5450.58658                5356.306581         0.0                                                      51965.0                                              29332.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1        160   16384          1  300.0          55                       5450.59                    5356.31         0.0                                                      51965.0                                              29332.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      181.0        1.0   1.0         318.232044
PostgreSQL-1-1-1024-2      181.0        1.0   2.0         318.232044

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST failed: Workflow not as planned
```

We can see that the overall throughput is close to the target and that scaled-out drivers (2 pods with 8 threads each) have similar results as a monolithic driver (1 pod with 16 threads).

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
                    [-nbt NUM_BENCHMARKING_THREADS] [-nbf NUM_BENCHMARKING_TARGET_FACTORS] [-sf SCALING_FACTOR] [-sd SCALING_DURATION] [-slg SCALING_LOGGING] [-xkey] [-t TIMEOUT] [-rr REQUEST_RAM]
                    [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE] [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE] [-rst {None,,local-hdd,shared}] [-rss REQUEST_STORAGE_SIZE] [-rnn REQUEST_NODE_NAME]
                    [-rnl REQUEST_NODE_LOADING] [-rnb REQUEST_NODE_BENCHMARKING] [-tr] [-b {tpcc,twitter}] [-tb TARGET_BASE]
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
  -nbf NUM_BENCHMARKING_TARGET_FACTORS, --num-benchmarking-target-factors NUM_BENCHMARKING_TARGET_FACTORS
                        comma separated list of factors of 16384 ops as target - default range(1,9)
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor (SF) = number of warehouses
  -sd SCALING_DURATION, --scaling-duration SCALING_DURATION
                        scaling factor = duration in minutes
  -slg SCALING_LOGGING, --scaling-logging SCALING_LOGGING
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
  -b {tpcc,twitter}, --benchmark {tpcc,twitter}
                        type of benchmark
  -tb TARGET_BASE, --target-base TARGET_BASE
                        ops as target, base for factors - default 1024 = 2**10
```

## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

Example:

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_monitoring.log &
```

The result looks something like

doc_benchbase_testcase_monitoring.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1202s 
    Code: 1752245831
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.9.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:427529448
    datadisk:3748
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1752245831
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:429232076
    datadisk:5216
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1752245831

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1        160   16384       1      1  300.0          47                   4685.744987                4601.795017         0.0                                                      69080.0                                              34135.0
PostgreSQL-1-1-1024-2-1               1         80    8192       2      1  300.0          15                   2788.018949                2743.498966         0.0                                                      71700.0                                              28677.0
PostgreSQL-1-1-1024-2-2               1         80    8192       2      2  300.0          20                   2804.526101                2759.306110         0.0                                                      71163.0                                              28513.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1        160   16384          1  300.0          47                       4685.74                    4601.80         0.0                                                      69080.0                                              34135.0
PostgreSQL-1-1-1024-2               1        160   16384          2  300.0          35                       5592.55                    5502.81         0.0                                                      71700.0                                              28595.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      201.0        1.0   1.0         286.567164
PostgreSQL-1-1-1024-2      201.0        1.0   2.0         286.567164

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      758.37     5.94           4.4                  9.1
PostgreSQL-1-1-1024-2      758.37     5.94           4.4                  9.1

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1554.83     5.61          1.29                 1.29
PostgreSQL-1-1-1024-2     1554.83     5.61          1.29                 1.29

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     6009.50    18.27          7.43                15.18
PostgreSQL-1-1-1024-2     7112.55    26.46          9.44                21.25

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1775.92     7.77          4.08                 4.08
PostgreSQL-1-1-1024-2     1775.92     6.79          7.15                 7.15

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
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
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -nc 2 \
  -rst shared -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_storage.log &
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

doc_benchbase_testcase_storage.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 7459s 
    Code: 1752247121
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.9.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:423905112
    datadisk:3796
    volume_size:30G
    volume_used:3.8G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1752247121
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:423906220
    datadisk:5301
    volume_size:30G
    volume_used:5.2G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1752247121

### Execution

#### Per Pod
                           experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                       
PostgreSQL-1-1-1024-1-1-1               1        160   16384       1      1  300.0          56                   5419.465718                5323.799068         0.0                                                      59017.0                                              29499.0
PostgreSQL-1-1-1024-2-1-1               2        160   16384       1      1  300.0          64                   4853.976110                4765.459453         0.0                                                      61479.0                                              32952.0

#### Aggregated Parallel
                         experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1        160   16384          1  300.0          56                       5419.47                    5323.80         0.0                                                      59017.0                                              29499.0
PostgreSQL-1-1-1024-2-1               2        160   16384          1  300.0          64                       4853.98                    4765.46         0.0                                                      61479.0                                              32952.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1-1      204.0        1.0   1.0         282.352941
PostgreSQL-1-1-1024-2-1      204.0        1.0   1.0         282.352941

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

The loading times for both instances of loading are the same, since both relate to the same process of ingesting into the database.
Note the added section about `volume_size` and `volume_used` in the connections section.
Also note the size increases from first to second run (benchmark writes data).

## Keying and Thinking Time

We can activate waiting times before and after execution of transactions with `-xkey` to follow TPC-C specifications more closely.
Also also make sure, the number of driver threads (`-nbt`) is 10 times the number of warehouses (`-sf`).

We at first remove persistent storage
```bash
kubectl delete pvc bexhoma-storage-postgresql-benchbase-160
```

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 160 \
  -sd 30 \
  -xkey \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1,2,5,10 \
  -nbt 1600 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_keytime.log &
```

## Evaluate Results

doc_benchbase_testcase_keytime.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=160
    Type: benchbase
    Duration: 8999s 
    Code: 1752254654
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 160. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 30 minutes.
    Experiment uses bexhoma version 0.8.9.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [1600] threads, split into [1, 2, 5, 10] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:423260432
    datadisk:22137
    volume_size:100G
    volume_used:22G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1752254654
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:423917924
    datadisk:18393
    volume_size:100G
    volume_used:22G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1752254654
PostgreSQL-1-1-1024-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:423922112
    datadisk:18393
    volume_size:100G
    volume_used:22G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1752254654
PostgreSQL-1-1-1024-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:423922232
    datadisk:18393
    volume_size:100G
    volume_used:22G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1752254654

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                       
PostgreSQL-1-1-1024-1-1                1       1600    1024       1      1  1800.0           0                      0.000000                   0.000000    0.000000                                                         -1.0                                                 -1.0
PostgreSQL-1-1-1024-2-2                1        800     512       2      1  1800.0           0                      0.000000                   0.000000    0.000000                                                         -1.0                                                 -1.0
PostgreSQL-1-1-1024-2-1                1        800     512       2      2  1800.0           0                      0.000000                   0.000000    0.000000                                                         -1.0                                                 -1.0
PostgreSQL-1-1-1024-3-1                1          0     204       3      1  1800.0           0                      0.000000                   0.000000    0.000000                                                          0.0                                                  0.0
PostgreSQL-1-1-1024-3-2                1          0     204       3      2  1800.0           0                      0.000000                   0.000000    0.000000                                                          0.0                                                  0.0
PostgreSQL-1-1-1024-3-5                1          0     204       3      3  1800.0           0                      0.000000                   0.000000    0.000000                                                          0.0                                                  0.0
PostgreSQL-1-1-1024-3-4                1          0     204       3      4  1800.0           0                      0.000000                   0.000000    0.000000                                                          0.0                                                  0.0
PostgreSQL-1-1-1024-3-3                1          0     204       3      5  1800.0           0                      0.000000                   0.000000    0.000000                                                          0.0                                                  0.0
PostgreSQL-1-1-1024-4-10               1        160     102       4      1  1800.0           0                      0.000000                   0.000000    0.000000                                                         -1.0                                                 -1.0
PostgreSQL-1-1-1024-4-8                1        160     102       4      2  1800.0           0                      0.000000                   0.000000    0.000000                                                         -1.0                                                 -1.0
PostgreSQL-1-1-1024-4-6                1        160     102       4      3  1800.0           0                      7.641070                   7.609959    9.985852                                                      29210.0                                              12310.0
PostgreSQL-1-1-1024-4-7                1        160     102       4      4  1800.0           0                      7.606111                   7.567222    9.929772                                                      29353.0                                              12336.0
PostgreSQL-1-1-1024-4-2                1        160     102       4      5  1800.0           0                      7.665514                   7.631070   10.013554                                                      29428.0                                              12479.0
PostgreSQL-1-1-1024-4-9                1        160     102       4      6  1800.0           0                      0.000000                   0.000000    0.000000                                                         -1.0                                                 -1.0
PostgreSQL-1-1-1024-4-4                1        160     102       4      7  1800.0           0                      0.000000                   0.000000    0.000000                                                         -1.0                                                 -1.0
PostgreSQL-1-1-1024-4-3                1        160     102       4      8  1800.0           0                      7.748854                   7.711632   10.119269                                                      29406.0                                              12373.0
PostgreSQL-1-1-1024-4-1                1        160     102       4      9  1800.0           0                      7.553848                   7.514959    9.861192                                                      29503.0                                              12423.0
PostgreSQL-1-1-1024-4-5                1        160     102       4     10  1800.0           0                      7.621626                   7.584960    9.953048                                                      29744.0                                              12439.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1       1600    1024          1  1800.0           0                          0.00                       0.00        0.00                                                         -1.0                                                 -1.0
PostgreSQL-1-1-1024-2               1       1600    1024          2  1800.0           0                          0.00                       0.00        0.00                                                         -1.0                                                 -1.0
PostgreSQL-1-1-1024-3               1          0    1020          5  1800.0           0                          0.00                       0.00        0.00                                                          0.0                                                  0.0
PostgreSQL-1-1-1024-4               1       1600    1020         10  1800.0           0                         45.84                      45.62       59.86                                                      29744.0                                               7435.6

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[10, 2, 5, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 5, 10]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1     1531.0        1.0   1.0          376.22469
PostgreSQL-1-1-1024-2     1531.0        1.0   2.0          376.22469
PostgreSQL-1-1-1024-3     1531.0        1.0   5.0          376.22469
PostgreSQL-1-1-1024-4     1531.0        1.0  10.0          376.22469

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     7141.16     6.14         18.73                48.95
PostgreSQL-1-1-1024-2     7141.16     6.14         18.73                48.95
PostgreSQL-1-1-1024-3     7141.16     6.14         18.73                48.95
PostgreSQL-1-1-1024-4     7141.16     6.14         18.73                48.95

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1    15140.06    11.78          1.35                 1.35
PostgreSQL-1-1-1024-2    15140.06    11.78          1.35                 1.35
PostgreSQL-1-1-1024-3    15140.06    11.78          1.35                 1.35
PostgreSQL-1-1-1024-4    15140.06    11.78          1.35                 1.35

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       64.11     0.03         21.13                48.95
PostgreSQL-1-1-1024-2       19.17     0.08         21.18                39.14
PostgreSQL-1-1-1024-3        0.00     0.00         18.71                36.66
PostgreSQL-1-1-1024-4      722.19     0.81         26.89                45.04

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       66.84     0.03          0.26                 0.26
PostgreSQL-1-1-1024-2       66.84     0.03          0.65                 0.65
PostgreSQL-1-1-1024-3        0.00     0.00          0.40                 0.40
PostgreSQL-1-1-1024-4      610.28     2.64          7.47                 7.47

### Tests
TEST failed: Throughput (requests/second) contains 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

Now also efficiency is computed via `0.45 * 60. * 100. * Goodput (requests/second) / 12.86 / sf`, when number of client threads is 10 times the number of warehouses:
* 45% is the average portion of new orders in the set of transactions
* 60 transforms to per-minute
* 100 makes it a percentage value
* Goodput (requests/second) is the number of successful transactions per second
* sf is the number of warehouses
* 12.86 is the theoretical limit in the TPC-C speficications

Note that these are statistical values.