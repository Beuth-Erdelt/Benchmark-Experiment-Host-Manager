# Example: Benchmark Citus

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Citus is a PostgreSQL extension, that introduces sharding [1].
A cluster has an instance of PostgreSQL with Citus as a coordinator (here called master, managed by a Kubernetes deployment).
More instances can register at the master as worker nodes (here managed by Kubernetes stateful sets).
Bexhoma also deploys a service for communication external to Citus (from within the cluster) and a headless service for communication between the pods of the Citus cluster.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Citus: https://www.citusdata.com/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. Benchbase Repository: https://github.com/cmu-db/benchbase/wiki/TPC-C
1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9


## Perform YCSB Benchmark - Ingestion of Data Included

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  --workload a \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_citus_1.log &
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of Citus (`-dbms`) with 3 workers (`-nw`), no replication (one instance `-nwr`) and 32 shards (`-nws`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=10, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [4]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 10.000.000 operations (`-sfo`)
      * workload A = 50% read / 50% write (`--workload`)
      * target throughput is `s` * 16384
      * threads = 64/`m` (`-nbt`)
    * with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* monitors (`-m`) all components (`-mc`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexperiments status`

```
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+------------------+--------------+------------+-------------+
| 1741884177       | sut          | use case   | worker      |
+==================+==============+============+=============+
| Citus-64-8-65536 | (1. Running) | ycsb       | (3 Running) |
+------------------+--------------+------------+-------------+
```

The code `1730133803` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1730133803` (removes everything that is related to experiment `1730133803`).

### Evaluate Results

At the end of a benchmark you will see a summary like

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 484s 
    Code: 1742844516
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-64-8-65536-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:153709796
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:25047912
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:136222144
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:785979628
    eval_parameters
        code:1742844516
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Citus-64-8-65536               1       64   65536          8           0                   55415.896735                20192.0             1000000                              2457.5

### Execution
                    experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Citus-64-8-65536-1               1       64   65536          1           0                       50989.19               196120.0           4997358                            1867.0             5002642                              1850.0

### Workflow

#### Actual
DBMS Citus-64-8-65536 - Pods [[1]]

#### Planned
DBMS Citus-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1       147.5     0.01          8.73                 9.66

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1        0.05        0          0.01                 0.01

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1     2094.44     9.66          9.95                11.39

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1     1050.52     7.79          0.62                 0.63

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

To see the summary again you can simply call `bexperiments summary -e 1730133803` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexperiments jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888




## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the Citus cluster.


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  --workload a \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_citus_2.log &
```
The following status shows we have one volume of type `shared`.
Every Citus experiment will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of Citus mounts the volume and generates the data.
All other instances just use the database without generating and loading data.
Bexhoma uses two types of volumes.
The first one is attached to the coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.


```
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-citus-ycsb-1           | citus           | ycsb-1       | True         |                26 | Citus           | shared               | 50Gi      | Bound    | 50.0G  | 40.0M  |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+

+-----------------------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| Volumes of Workers                            | configuration     |   experiment | dbms   | storage_class_name   | storage   | status   | size   | used   |
+===============================================+===================+==============+========+======================+===========+==========+========+========+
| bexhoma-workers-bexhoma-worker-citus-ycsb-1-0 | Citus-64-8-65536  |   1742471862 | Citus  | shared               | 50Gi      | Bound    | 50.0G  | 1.4G   |
+-----------------------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bexhoma-workers-bexhoma-worker-citus-ycsb-1-1 | Citus-64-8-65536  |   1742471862 | Citus  | shared               | 50Gi      | Bound    | 50.0G  | 1.4G   |
+-----------------------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bexhoma-workers-bexhoma-worker-citus-ycsb-1-2 | Citus-64-8-65536  |   1742471862 | Citus  | shared               | 50Gi      | Bound    | 50.0G  | 1.2G   |
+-----------------------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
```

The result looks something like


```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 813s 
    Code: 1742845087
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Citus-64-8-65536-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:153668376
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:135340880
        volume_size:50.0G
        volume_used:1.4G
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:785204084
        volume_size:50.0G
        volume_used:1.4G
    worker 2
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:24183888
        volume_size:50.0G
        volume_used:1.2G
    eval_parameters
        code:1742845087
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3
Citus-64-8-65536-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:153668364
    volume_size:50.0G
    volume_used:3.9G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:135341076
        volume_size:50.0G
        volume_used:1.4G
    worker 1
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:24183904
        volume_size:50.0G
        volume_used:1.4G
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:785217812
        volume_size:50.0G
        volume_used:1.2G
    eval_parameters
        code:1742845087
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Citus-64-8-65536               1       64   65536          8           0                   62437.553921                16076.0             1000000                             4343.75

### Execution
                      experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Citus-64-8-65536-1-1               1       64   65536          1           0                       64574.04               154861.0           5000713                             801.0             4999287                              1131.0
Citus-64-8-65536-2-1               2       64   65536          1           0                       64670.50               154630.0           5001750                             820.0             4998250                              1320.0

### Workflow

#### Actual
DBMS Citus-64-8-65536 - Pods [[1], [1]]

#### Planned
DBMS Citus-64-8-65536 - Pods [[1], [1]]

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1      2403.1     0.01          9.11                10.55

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1           0        0           0.0                  0.0

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1        2.46     0.01          7.66                  8.9
Citus-64-8-65536-2-1       13.35     0.01          7.66                  8.9

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1      736.73     6.99          0.62                 0.63
Citus-64-8-65536-2-1      736.73     7.14          0.62                 0.63

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```
'Citus': {
    'loadData': 'psql -U postgres < {scriptname}',
    'attachWorker': "psql -U postgres --command=\"SELECT * from master_add_node('{worker}.{service_sut}', 5432);\"",
    'template': {
        'version': '10.0.2',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
         'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", "password1234"],
            'url': 'jdbc:postgresql://{serverip}:9091/postgres',#/{dbname}',
            'jar': 'postgresql-42.5.0.jar'
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
},
```

where
* `loadData`: This command is used to create the schema
* `JDBC`: These infos are used to configure YCSB


Citus uses the PostgreSQL JDBC driver.



### Schema SQL File

Before ingestion, we run a script to create and distribute the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Citus/initschema-ycsb.sql

After ingestion, we run a script to check the distributions.
The script also vacuums and analyzes the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/ycsb/Citus/checkschema-ycsb.sql








## Benchbase's TPC-C

Before ingestion, we run a script to create and distribute the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/benchbase/Citus/initschema-benchbase.sql

After ingestion, we run a script to check the distributions.
The script also vacuums and analyzes the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/benchbase/Citus/checkschema-benchbase.sql

### Benchbase Simple Example

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
Citus has 3 workers.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_1.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 1062s 
    Code: 1743071725
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-1-1-1024-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:184428864
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:137636304
    worker 1
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:62175396
    worker 2
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:189693056
    eval_parameters
                code:1743071725
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:3
Citus-1-1-1024-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:184451484
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:138106472
    worker 1
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:62562716
    worker 2
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:190017660
    eval_parameters
                code:1743071725
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:3

### Execution
                  experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1               1         16   16384          1  300.0                        914.50                                                      42561.0                                              17485.0
Citus-1-1-1024-2               1         16   16384          2  300.0                        850.55                                                      46012.0                                              18799.5

Warehouses: 16

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2]]

### Loading
                  time_load  terminals  pods  Imported warehouses [1/h]
Citus-1-1-1024-1      172.0        1.0   1.0                 334.883721
Citus-1-1-1024-2      172.0        1.0   2.0                 334.883721

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### Benchbase More Complex

TPC-C is performed at 128 warehouses.
The 64 threads of the client are split into a cascading sequence of 1,2,4 and 8 pods.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 60 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_2.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
Benchbase Workload SF=128 (warehouses for TPC-C)
    Type: benchbase
    Duration: 16124s 
    Code: 1742847127
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 128. Benchmarking runs for 60 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-1-1-1024-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:189662516
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:25962032
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:137763992
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:787358472
    eval_parameters
                code:1742847127
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:3
Citus-1-1-1024-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:211164612
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:29501860
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:143520092
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:792518068
    eval_parameters
                code:1742847127
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:3
Citus-1-1-1024-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:220994664
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:31000552
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:145903004
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:794542312
    eval_parameters
                code:1742847127
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:3
Citus-1-1-1024-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:229392188
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:31779000
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:146736940
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:796108048
    eval_parameters
                code:1742847127
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:3

### Execution
                  experiment_run  terminals  target  pod_count    time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1               1         64   16384          1  3600.0                       3695.67                                                      43832.0                                             17313.00
Citus-1-1-1024-2               1         64   16384          2  3600.0                       3567.21                                                      42594.0                                             17936.50
Citus-1-1-1024-3               1         64   16384          4  3600.0                       3135.21                                                      44479.0                                             20408.25
Citus-1-1-1024-4               1         64   16384          8  3600.0                       1865.48                                                      85947.0                                             34300.88

Warehouses: 128

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[8, 4, 2, 1]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                  time_load  terminals  pods  Imported warehouses [1/h]
Citus-1-1-1024-1      724.0        1.0   1.0                 636.464088
Citus-1-1-1024-2      724.0        1.0   2.0                 636.464088
Citus-1-1-1024-3      724.0        1.0   4.0                 636.464088
Citus-1-1-1024-4      724.0        1.0   8.0                 636.464088

### Ingestion - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1      427.65     1.01         11.08                14.06
Citus-1-1-1024-2      427.65     1.01         11.08                14.06
Citus-1-1-1024-3      427.65     1.01         11.08                14.06
Citus-1-1-1024-4      427.65     1.01         11.08                14.06

### Ingestion - Loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1    14919.04    34.63          1.33                 1.33
Citus-1-1-1024-2    14919.04    34.63          1.33                 1.33
Citus-1-1-1024-3    14919.04    34.63          1.33                 1.33
Citus-1-1-1024-4    14919.04    34.63          1.33                 1.33

### Execution - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1    46334.89    12.96         13.97                18.85
Citus-1-1-1024-2    49302.13    11.36         15.40                21.51
Citus-1-1-1024-3    45039.15    10.06         16.62                23.82
Citus-1-1-1024-4    29339.99     8.19         17.25                25.14

### Execution - Benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1    25316.65     7.10          2.28                 2.48
Citus-1-1-1024-2    25316.65     6.01          5.08                 5.28
Citus-1-1-1024-3    21103.52     5.59          8.24                 8.24
Citus-1-1-1024-4    19618.08     2.79         11.71                11.71

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



### Benchbase Realistic

At first, we clean old PVC.

```bash
kubectl delete pvc bexhoma-storage-citus-ycsb-1
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-ycsb-1-0
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-ycsb-1-1
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-ycsb-1-2
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-ycsb-1-3
```

We run a benchmark with
* PVCs for persistent database
* monitoring
* a sensible number of workers (4)
* a sensible size (128 warehouses)
* a sensible number of threads (1024)
* suitable splittings (1x1024, 2x512, 4x256, 8x1028)
* logging the state every 30 seconds
* a realistic target (4096 transactions per second)
* a realistic duration (20 minutes)
* a repetition (`-nc` is 2)

Note that the number of threads for each pod is a multiple of the number of warehouses.
At start, Benchbase assigns each thread to a fixed warehouse.
This way, we distribute the threads equally to the warehouses.
Each thread also gets assigned a fixed range of districts per warehouse.
Please also note, that this is not compliant to the TPC-C specifications, which state: *For each active warehouse in the database, the SUT must accept requests for transactions from a population of 10 terminals.*

```bash
python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 20 \
  -slg 30 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -nbp 1,2,4,8 \
  -nbt 1024 \
  -nbf 4 \
  -tb 1024 \
  -m -mc \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_3.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
Benchbase Workload SF=128 (warehouses for TPC-C)
    Type: benchbase
    Duration: 6869s 
    Code: 1743284733
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 128. Benchmarking runs for 20 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [1014] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-1-1-1024-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:197390416
    volume_size:100.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:136560912
        volume_size:100.0G
        volume_used:6.3G
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:812579492
        volume_size:100.0G
        volume_used:6.3G
    worker 2
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:86370932
        volume_size:100.0G
        volume_used:40.0M
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80555468
        volume_size:100.0G
        volume_used:6.3G
    eval_parameters
                code:1743284733
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:197390416
    volume_size:100.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:136561416
        volume_size:100.0G
        volume_used:12.2G
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:812581944
        volume_size:100.0G
        volume_used:6.3G
    worker 2
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:86371052
        volume_size:100.0G
        volume_used:6.3G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80555500
        volume_size:100.0G
        volume_used:6.3G
    eval_parameters
                code:1743284733
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:197390588
    volume_size:100.0G
    volume_used:668.0M
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:136561956
        volume_size:100.0G
        volume_used:18.8G
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:812584304
        volume_size:100.0G
        volume_used:14.5G
    worker 2
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:86371116
        volume_size:100.0G
        volume_used:12.8G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80555536
        volume_size:100.0G
        volume_used:14.8G
    eval_parameters
                code:1743284733
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:197390588
    volume_size:100.0G
    volume_used:668.0M
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:136447956
        volume_size:100.0G
        volume_used:23.9G
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:812598124
        volume_size:100.0G
        volume_used:19.8G
    worker 2
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:86371240
        volume_size:100.0G
        volume_used:12.8G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80555620
        volume_size:100.0G
        volume_used:20.1G
    eval_parameters
                code:1743284733
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4

### Execution
                  experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1               1       1014    4096          1  1200.0          65                       3748.46                                                    1020144.0                                             270403.0
Citus-1-1-1024-2               1       1014    4096          2  1200.0          44                       3428.29                                                    1178130.0                                             295583.0
Citus-1-1-1024-3               1       1012    4096          4  1200.0          32                       3296.20                                                    1273102.0                                             306796.5
Citus-1-1-1024-4               1       1008    4096          8  1200.0          35                       3380.49                                                    1155013.0                                             298003.5

Warehouses: 128

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[1, 2, 4, 8]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                  time_load  terminals  pods  Imported warehouses [1/h]
Citus-1-1-1024-1      753.0        1.0   1.0                 611.952191
Citus-1-1-1024-2      753.0        1.0   2.0                 611.952191
Citus-1-1-1024-3      753.0        1.0   4.0                 611.952191
Citus-1-1-1024-4      753.0        1.0   8.0                 611.952191

### Ingestion - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1     2427.81     3.02         22.87                35.54
Citus-1-1-1024-2     2427.81     3.02         22.87                35.54
Citus-1-1-1024-3     2427.81     3.02         22.87                35.54
Citus-1-1-1024-4     2427.81     3.02         22.87                35.54

### Ingestion - Loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1    12632.98    31.15          1.33                 1.33
Citus-1-1-1024-2    12632.98    31.15          1.33                 1.33
Citus-1-1-1024-3    12632.98    31.15          1.33                 1.33
Citus-1-1-1024-4    12632.98    31.15          1.33                 1.33

### Execution - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1   180615.44    81.92         90.55               107.72
Citus-1-1-1024-2   168155.44    84.35        100.68               121.96
Citus-1-1-1024-3   165719.59   120.60        110.38               135.43
Citus-1-1-1024-4   174005.03    81.77        120.80               150.01

### Execution - Benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1     6112.48     5.34          9.28                 9.28
Citus-1-1-1024-2     6112.48     5.30          9.28                 9.28
Citus-1-1-1024-3     6162.40     3.89          5.06                 5.06
Citus-1-1-1024-4     6334.93     4.17          2.95                 2.95

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```





## HammerDB's TPC-C

HammerDB provides an option to benchmark PostgreSQL with citus compatibility activated.
This generates the tables and functions in an empty database and additionally distributes tables and functions: https://github.com/TPC-Council/HammerDB/blob/master/src/postgresql/pgoltp.tcl

After ingestion, we run a script to check the distributions.
The script also vacuums and analyzes the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/tpcc/Citus/checkschema-tpcc.sql

### HammerDB Simple Example

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
Citus has 3 workers.


```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms Citus \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/doc_hammerdb_citus_1.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1319s 
    Code: 1743575053
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker23.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-BHT-8-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86432660
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:160047388
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:931299488
    worker 2
        RAM:540595896320
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker24
        disk:96570296

### Execution
                 experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]     NOPM       TPM  duration  errors
Citus-BHT-8-1-1               1      16       1          1     29.22     63.92  49005.0  112642.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS Citus-BHT-8-1 - Pods [[1]]

#### Planned
DBMS Citus-BHT-8-1 - Pods [[1]]

### Loading
                 time_load  terminals  pods  Imported warehouses [1/h]
Citus-BHT-8-1-1      115.0        1.0   1.0                 500.869565

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```

### HammerDB More Complex Example

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 128 \
  -sd 30 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlp 1 \
  -nlt 128 \
  -nbp 1,2,4,8 \
  -nbt 128 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/doc_hammerdb_citus_2.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
HammerDB Workload SF=128 (warehouses for TPC-C)
    Type: tpcc
    Duration: 20062s
    Code: 1743535146
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 128. Benchmarking runs for 30 minutes.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker23.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [128] threads, split into [1] pods.
    Benchmarking is tested with [128] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Citus-BHT-128-1-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86386468
    volume_size:100.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:930038956
        volume_size:100.0G
        volume_used:6.4G
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:158696524
        volume_size:100.0G
        volume_used:40.0M
    worker 2
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80565072
        volume_size:100.0G
        volume_used:40.0M
    worker 3
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211604728
        volume_size:100.0G
        volume_used:40.0M
Citus-BHT-128-1-1-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86386568
    volume_size:100.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:930042332
        volume_size:100.0G
        volume_used:17.6G
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:158697300
        volume_size:100.0G
        volume_used:9.9G
    worker 2
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80565180
        volume_size:100.0G
        volume_used:9.2G
    worker 3
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211608428
        volume_size:100.0G
        volume_used:10.0G
Citus-BHT-128-1-1-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86386724
    volume_size:100.0G
    volume_used:84.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:930053976
        volume_size:100.0G
        volume_used:23.8G
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:158706196
        volume_size:100.0G
        volume_used:19.4G
    worker 2
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80565232
        volume_size:100.0G
        volume_used:17.5G
    worker 3
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211612060
        volume_size:100.0G
        volume_used:19.4G
Citus-BHT-128-1-1-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86386876
    volume_size:100.0G
    volume_used:84.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:930057532
        volume_size:100.0G
        volume_used:35.2G
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:158715188
        volume_size:100.0G
        volume_used:25.3G
    worker 2
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80565336
        volume_size:100.0G
        volume_used:21.3G
    worker 3
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211615708
        volume_size:100.0G
        volume_used:25.5G
Citus-BHT-128-1-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86387096
    volume_size:100.0G
    volume_used:84.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:158717592
        volume_size:100.0G
        volume_used:39.0G
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:930072196
        volume_size:100.0G
        volume_used:27.1G
    worker 2
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211622268
        volume_size:100.0G
        volume_used:22.5G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80565476
        volume_size:100.0G
        volume_used:21.3G
Citus-BHT-128-1-2-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86387196
    volume_size:100.0G
    volume_used:84.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:158726548
        volume_size:100.0G
        volume_used:39.0G
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:930075564
        volume_size:100.0G
        volume_used:27.1G
    worker 2
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211625952
        volume_size:100.0G
        volume_used:22.5G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80565528
        volume_size:100.0G
        volume_used:21.3G
Citus-BHT-128-1-2-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86387352
    volume_size:100.0G
    volume_used:84.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:158727252
        volume_size:100.0G
        volume_used:39.0G
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:930079028
        volume_size:100.0G
        volume_used:27.1G
    worker 2
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211629604
        volume_size:100.0G
        volume_used:22.5G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80565636
        volume_size:100.0G
        volume_used:21.3G
Citus-BHT-128-1-2-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86387508
    volume_size:100.0G
    volume_used:84.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:158728032
        volume_size:100.0G
        volume_used:39.0G
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:946294928
        volume_size:100.0G
        volume_used:27.1G
    worker 2
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211633348
        volume_size:100.0G
        volume_used:27.4G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80565736
        volume_size:100.0G
        volume_used:26.2G

### Execution
                     experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]       NOPM        TPM  duration  errors
Citus-BHT-128-1-1-1               1     128       1          1    153.66    534.52  108937.00  250561.00        30       0
Citus-BHT-128-1-1-2               1     128       2          2    153.63    541.50   99546.00  228914.00        30       0
Citus-BHT-128-1-1-3               1     128       3          4    159.06    521.44  108795.50  250150.75        30       0
Citus-BHT-128-1-1-4               1     128       4          8    154.82    488.14  108588.12  249824.00        30       0
Citus-BHT-128-1-2-1               2     128       1          1    147.51    457.69  110144.00  253281.00        30       0
Citus-BHT-128-1-2-2               2     128       2          2    157.47    527.28   90604.50  208438.00        30       0
Citus-BHT-128-1-2-3               2     128       3          4    176.13    570.77   84797.00  195024.25        30       0
Citus-BHT-128-1-2-4               2     128       4          8    183.12    565.45   76188.25  175214.38        30       0

Warehouses: 128

### Workflow

#### Actual
DBMS Citus-BHT-128-1 - Pods [[1, 2, 4, 8], [1, 2, 4, 8]]

#### Planned
DBMS Citus-BHT-128-1 - Pods [[1, 2, 4, 8], [1, 2, 4, 8]]

### Loading
                     time_load  terminals  pods  Imported warehouses [1/h]
Citus-BHT-128-1-1-1      411.0        1.0   1.0                1121.167883
Citus-BHT-128-1-1-2      411.0        1.0   2.0                1121.167883
Citus-BHT-128-1-1-3      411.0        1.0   4.0                1121.167883
Citus-BHT-128-1-1-4      411.0        1.0   8.0                1121.167883
Citus-BHT-128-1-2-1      411.0        1.0   1.0                1121.167883
Citus-BHT-128-1-2-2      411.0        1.0   2.0                1121.167883
Citus-BHT-128-1-2-3      411.0        1.0   4.0                1121.167883
Citus-BHT-128-1-2-4      411.0        1.0   8.0                1121.167883

### Ingestion - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1-1      935.07     1.01         21.72                34.49
Citus-BHT-128-1-1-2      935.07     1.01         21.72                34.49
Citus-BHT-128-1-1-3      935.07     1.01         21.72                34.49
Citus-BHT-128-1-1-4      935.07     1.01         21.72                34.49

### Ingestion - Loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1-1     4685.53    26.87          0.69                  0.7
Citus-BHT-128-1-1-2     4685.53    26.87          0.69                  0.7
Citus-BHT-128-1-1-3     4685.53    26.87          0.69                  0.7
Citus-BHT-128-1-1-4     4685.53    26.87          0.69                  0.7

### Execution - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1-1   200473.99    67.63         36.83                56.72
Citus-BHT-128-1-1-2   188592.36    57.00         43.76                73.98
Citus-BHT-128-1-1-3   216648.77    86.03         51.55                90.49
Citus-BHT-128-1-1-4   256759.81    89.57         59.14               104.39
Citus-BHT-128-1-2-1   272501.52    82.69         49.25               109.29
Citus-BHT-128-1-2-2   279029.98    93.85         58.29               126.59
Citus-BHT-128-1-2-3   296269.05   104.04         66.29               133.45
Citus-BHT-128-1-2-4   324950.87   114.55         72.26               141.01

### Execution - Benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1-1     2721.81     1.64          2.51                 2.51
Citus-BHT-128-1-1-2     2721.81     1.48          2.51                 2.51
Citus-BHT-128-1-1-3     2767.10     1.17          1.19                 1.19
Citus-BHT-128-1-1-4     2768.79     0.91          0.65                 0.65
Citus-BHT-128-1-2-1     2719.37     1.50          2.70                 2.70
Citus-BHT-128-1-2-2     2719.37     1.24          2.70                 2.70
Citus-BHT-128-1-2-3     2280.13     0.93          1.02                 1.02
Citus-BHT-128-1-2-4     2160.12     0.64          0.53                 0.53

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


### HammerDB Referenced Paper

We here run HammerDB TPROC-C benchmark against Citus similar to [1].
We in particular copy the setting 500 warehouses, 250 virtual users and 4 worker nodes.
There has been made a contribution to HammerDB by [2] and we assume this reflects the configuration used in [1]:
*In case of Citus, we converted the items table to a reference table
and the remaining tables to co-located distributed tables with the
warehouse ID column as the distribution column. Additionally, we
configured Citus to delegate stored procedure calls to worker nodes
based on the warehouse ID argument.*
We configure the experiment to use 48 shards, run for 20 minutes and split the 250 virtual users (sequentially) into 1,2,5 and 10 pods.
Database is persisted on PVCs.
The experiment runs twice for confidence.

Note: In [1] YCSB is run as this: *For this benchmark, the coordinator’s CPU usage becomes a scaling bottleneck. Hence, we ran the benchmark with every worker node acting as coordinator and configured YCSB to load balance across all nodes.* This apparently uses [4], part of the Citus benchmark toolkit [3], and PostgreSQL loadbalancer feature [5].

[1] [Citus: Distributed PostgreSQL for Data-Intensive Applications](https://dl.acm.org/doi/10.1145/3448016.3457551)
> Umur Cubukcu, Ozgun Erdogan, Sumedh Pathak, Sudhakar Sannakkayala, and Marco Slot.
> 2021. In Proceedings of the 2021 International Conference on Management of Data (SIGMOD '21).
> Association for Computing Machinery, New York, NY, USA, 2490–2502.
> https://dl.acm.org/doi/10.1145/3448016.3457551

[2] [How to benchmark performance of Citus and Postgres with HammerDB on Azure](https://techcommunity.microsoft.com/blog/adforpostgresql/how-to-benchmark-performance-of-citus-and-postgres-with-hammerdb-on-azure/3254918)
> JelteF, Microsoft.
> Retrieved April 1, 2025, from https://techcommunity.microsoft.com/blog/adforpostgresql/how-to-benchmark-performance-of-citus-and-postgres-with-hammerdb-on-azure/3254918

[3] https://github.com/citusdata/citus-benchmark

[4] https://github.com/citusdata/citus-benchmark/blob/master/run.tcl

[5] https://www.citusdata.com/blog/2023/09/22/adding-postgres-16-support-to-citus-12-1


```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 500 \
  -sd 20 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlp 1 \
  -nlt 500 \
  -nbp 1,2,5,10 \
  -nbt 250 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 200Gi \
  run </dev/null &>$LOG_DIR/doc_hammerdb_citus_3.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
HammerDB Workload SF=500 (warehouses for TPC-C)
    Type: tpcc
    Duration: 16770s
    Code: 1743497186
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 500. Benchmarking runs for 20 minutes.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker23.
    Database is persisted to disk of type shared and size 200Gi.
    Loading is tested with [500] threads, split into [1] pods.
    Benchmarking is tested with [250] threads, split into [1, 2, 5, 10] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Citus-BHT-500-1-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86384160
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:137173756
        volume_size:200.0G
        volume_used:59.0G
    worker 1
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80563656
        volume_size:200.0G
        volume_used:48.1G
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:894091524
        volume_size:200.0G
        volume_used:47.9G
    worker 3
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:700387028
        volume_size:200.0G
        volume_used:62.7G
Citus-BHT-500-1-1-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86384236
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:137174264
        volume_size:200.0G
        volume_used:59.0G
    worker 1
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80563692
        volume_size:200.0G
        volume_used:48.1G
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:901864272
        volume_size:200.0G
        volume_used:47.9G
    worker 3
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:700387412
        volume_size:200.0G
        volume_used:62.7G
Citus-BHT-500-1-1-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86384304
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:137183064
        volume_size:200.0G
        volume_used:59.0G
    worker 1
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80563728
        volume_size:200.0G
        volume_used:48.1G
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:901866732
        volume_size:200.0G
        volume_used:47.9G
    worker 3
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:700387712
        volume_size:200.0G
        volume_used:62.7G
Citus-BHT-500-1-1-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86384432
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:137183592
        volume_size:200.0G
        volume_used:59.0G
    worker 1
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80563820
        volume_size:200.0G
        volume_used:48.1G
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:887132264
        volume_size:200.0G
        volume_used:47.9G
    worker 3
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:700396276
        volume_size:200.0G
        volume_used:62.7G
Citus-BHT-500-1-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86384792
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:137194016
        volume_size:200.0G
        volume_used:68.9G
    worker 1
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80563972
        volume_size:200.0G
        volume_used:54.3G
    worker 2
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211558356
        volume_size:200.0G
        volume_used:52.2G
    worker 3
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:86384796
        volume_size:200.0G
        volume_used:67.7G
Citus-BHT-500-1-2-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86384864
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:137202792
        volume_size:200.0G
        volume_used:68.9G
    worker 1
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80564064
        volume_size:200.0G
        volume_used:54.3G
    worker 2
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211558512
        volume_size:200.0G
        volume_used:52.2G
    worker 3
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:86384868
        volume_size:200.0G
        volume_used:67.7G
Citus-BHT-500-1-2-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86384988
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:137203300
        volume_size:200.0G
        volume_used:68.9G
    worker 1
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80564100
        volume_size:200.0G
        volume_used:54.3G
    worker 2
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211561244
        volume_size:200.0G
        volume_used:52.2G
    worker 3
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:86384992
        volume_size:200.0G
        volume_used:67.7G
Citus-BHT-500-1-2-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:86385064
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:137212064
        volume_size:200.0G
        volume_used:68.9G
    worker 1
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:80564136
        volume_size:200.0G
        volume_used:54.3G
    worker 2
        RAM:1081650966528
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:211563904
        volume_size:200.0G
        volume_used:52.2G
    worker 3
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:86385064
        volume_size:200.0G
        volume_used:67.7G

### Execution
                     experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]      NOPM       TPM  duration  errors
Citus-BHT-500-1-1-1               1     250       1          1    279.77    975.12  131780.0  302731.0        20       0
Citus-BHT-500-1-1-2               1     250       2          2    253.37    942.30  122736.0  282265.0        20       0
Citus-BHT-500-1-1-3               1     250       3          5    289.81   1098.57  121265.6  278954.6        20       0
Citus-BHT-500-1-1-4               1     250       4         10    298.37   1118.25  111066.1  255331.5        20       0
Citus-BHT-500-1-2-1               2     250       1          1    275.36    931.49  123117.0  282986.0        20       0
Citus-BHT-500-1-2-2               2     250       2          2    279.73    964.50  115636.0  266063.0        20       0
Citus-BHT-500-1-2-3               2     250       3          5    297.32   1000.17  117759.0  270781.4        20       0
Citus-BHT-500-1-2-4               2     250       4         10    295.59   1102.34  104349.1  239878.4        20       0

Warehouses: 500

### Workflow

#### Actual
DBMS Citus-BHT-500-1 - Pods [[1, 2, 5, 10], [1, 2, 5, 10]]

#### Planned
DBMS Citus-BHT-500-1 - Pods [[1, 2, 5, 10], [1, 2, 5, 10]]

### Loading
                     time_load  terminals  pods  Imported warehouses [1/h]
Citus-BHT-500-1-1-1      966.0        1.0   1.0                1863.354037
Citus-BHT-500-1-1-2      966.0        1.0   2.0                1863.354037
Citus-BHT-500-1-1-3      966.0        1.0   5.0                1863.354037
Citus-BHT-500-1-1-4      966.0        1.0  10.0                1863.354037
Citus-BHT-500-1-2-1      966.0        1.0   1.0                1863.354037
Citus-BHT-500-1-2-2      966.0        1.0   2.0                1863.354037
Citus-BHT-500-1-2-3      966.0        1.0   5.0                1863.354037
Citus-BHT-500-1-2-4      966.0        1.0  10.0                1863.354037

### Execution - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-500-1-1-1   255962.82   155.93         61.54               192.80
Citus-BHT-500-1-1-2   259596.23   142.59         73.51               217.66
Citus-BHT-500-1-1-3   243092.54   125.58         82.50               228.67
Citus-BHT-500-1-1-4   251510.83   155.50         91.96               232.58
Citus-BHT-500-1-2-1   276866.56   158.97         71.75               243.96
Citus-BHT-500-1-2-2   264411.89   154.96         82.84               257.16
Citus-BHT-500-1-2-3   281864.62   137.71         91.50               258.01
Citus-BHT-500-1-2-4   280052.56   165.21         99.05               258.26

### Execution - Benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-500-1-1-1     2223.47     2.03          2.41                 2.41
Citus-BHT-500-1-1-2     2223.47     1.91          2.41                 2.41
Citus-BHT-500-1-1-3     2215.88     1.26          1.22                 1.22
Citus-BHT-500-1-1-4     2118.87     1.04          0.58                 0.58
Citus-BHT-500-1-2-1     2099.47     1.81          2.80                 2.80
Citus-BHT-500-1-2-2     2099.47     1.65          2.80                 2.80
Citus-BHT-500-1-2-3     2012.92     1.01          1.05                 1.05
Citus-BHT-500-1-2-4     2049.88     0.93          0.44                 0.44

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


