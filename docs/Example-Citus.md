# Example: Benchmark Citus

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Citus is a PostgreSQL extension, that introduces sharding [1].
A cluster has an instance of PostgreSQL with Citus as a coordinator (here called master, managed by a Kubernetes deployment).
More instances can register at the master as worker nodes (here managed by Kubernetes stateful sets).
Bexhoma also deploys a service for communication external to Citus (from within the cluster) and a headless service for communication between the pods of the Redis cluster.


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
  -nws 32 \
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
    Duration: 610s 
    Code: 1742470123
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
    disk:150654820
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
        disk:22185140
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:117515584
    worker 2
        RAM:540595896320
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker24
        disk:145890680
    eval_parameters
        code:1742470123
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:32
        BEXHOMA_WORKERS:3

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Citus-64-8-65536               1       64   65536          8           0                   54265.612053                19580.0             1000000                              2367.0

### Execution
                    experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Citus-64-8-65536-1               1       64   65536          1           0                       51756.35               193213.0           5000036                            1962.0             4999964                              1964.0

### Workflow

#### Actual
DBMS Citus-64-8-65536 - Pods [[1]]

#### Planned
DBMS Citus-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1      391.64     7.46          2.55                 2.59

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1       92.96        0          0.58                 0.58

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1      3583.4    13.69          2.77                  2.8

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1     1233.96        0          0.62                 0.63

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
  -nws 32 \
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
    Duration: 1126s 
    Code: 1742471862
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
    disk:150613572
    volume_size:50.0G
    volume_used:40.0M
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
        disk:21321380
        volume_size:50.0G
        volume_used:40.0M
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:459593372
        volume_size:50.0G
        volume_used:40.0M
    worker 2
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:417269456
        volume_size:50.0G
        volume_used:40.0M
    eval_parameters
        code:1742471862
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:32
        BEXHOMA_WORKERS:3
Citus-64-8-65536-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:150613564
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:459593456
        volume_size:50.0G
        volume_used:1.4G
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:116643040
        volume_size:50.0G
        volume_used:1.4G
    worker 2
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:21321404
        volume_size:50.0G
        volume_used:1.2G
    eval_parameters
        code:1742471862
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:32
        BEXHOMA_WORKERS:3

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Citus-64-8-65536               1       64   65536          8           0                   54322.322678                19711.0             1000000                              2183.5

### Execution
                      experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Citus-64-8-65536-1-1               1       64   65536          1           0                       53002.60               188670.0           4998485                            1944.0             5001515                              1954.0
Citus-64-8-65536-2-1               2       64   65536          1           0                       49923.87               200305.0           4998279                            1992.0             5001721                              2005.0

### Workflow

#### Actual
DBMS Citus-64-8-65536 - Pods [[1], [1]]

#### Planned
DBMS Citus-64-8-65536 - Pods [[1], [1]]

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1      385.11     6.74          2.55                 2.59

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1        99.5        0          0.58                 0.59

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1     3487.03    20.02          2.77                 2.81
Citus-64-8-65536-2-1     3938.43    16.78          2.76                 3.05

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1     1154.11     8.04          0.62                 0.63
Citus-64-8-65536-2-1     1333.43     7.88          0.62                 0.63

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
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

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Citus









## Benchbase's TPC-C

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
Citus has 3 workers.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
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
    Duration: 1272s
    Code: 1742473090
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
    disk:155025016
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
        disk:116684536
    worker 1
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:417310916
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:459634868
    eval_parameters
                code:1742473090
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:32
                BEXHOMA_WORKERS:3
Citus-1-1-1024-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:158069900
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
        disk:116684644
    worker 1
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:417310960
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:459634916
    eval_parameters
                code:1742473090
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:32
                BEXHOMA_WORKERS:3

### Execution
                  experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1               1         16   16384          1  300.0                       2440.37
                    14925.0                                               6550.0
Citus-1-1-1024-2               1         16   16384          2  300.0                       2207.94
                    16869.0                                               7239.5

Warehouses: 16

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[1, 2]]

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
  -dbms Citus \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_2.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
Benchbase Workload SF=128 (warehouses for TPC-C)
    Type: benchbase
    Duration: 15809s 
    Code: 1742228675
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 128. Benchmarking runs for 60 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
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
    disk:180558040
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
        disk:21341444
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:101793644
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:326746868
    eval_parameters
                code:1742228675
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:32
                BEXHOMA_WORKERS:3
Citus-1-1-1024-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:205684788
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
        disk:24277644
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:106401480
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:330737352
    eval_parameters
                code:1742228675
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:32
                BEXHOMA_WORKERS:3
Citus-1-1-1024-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:218862228
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
        disk:25365060
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:108128780
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:332066900
    eval_parameters
                code:1742228675
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:32
                BEXHOMA_WORKERS:3
Citus-1-1-1024-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:229785872
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
        disk:25587696
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:108138036
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:332639084
    eval_parameters
                code:1742228675
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:32
                BEXHOMA_WORKERS:3

### Execution
                  experiment_run  terminals  target  pod_count    time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1               1         64   16384          1  3600.0                       4340.48                                                      31481.0                                             14740.00
Citus-1-1-1024-2               1         64   16384          2  3600.0                       4213.02                                                      31791.0                                             15187.00
Citus-1-1-1024-3               1         64   16384          4  3600.0                       3574.33                                                      36360.0                                             17901.00
Citus-1-1-1024-4               1         64   16384          8  3600.0                       2053.90                                                      82549.0                                             31153.62

Warehouses: 128

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[8, 4, 1, 2]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                  time_load  terminals  pods  Imported warehouses [1/h]
Citus-1-1-1024-1      766.0        1.0   1.0                  601.56658
Citus-1-1-1024-2      766.0        1.0   2.0                  601.56658
Citus-1-1-1024-3      766.0        1.0   4.0                  601.56658
Citus-1-1-1024-4      766.0        1.0   8.0                  601.56658

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


## Benchbase Example Explained

The setup is the same as for YCSB (see above).

After ingestion with Benchbase, we run a script to distribute the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/benchbase/Citus/checkschema-benchbase.sql
