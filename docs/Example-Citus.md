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
      * generates YCSB data = 10.000.000 rows (i.e., SF=10, `-sf`)
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

doc_ycsb_citus_1.log
```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1375s 
    Code: 1747735357
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.5.
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
    disk:254049352
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:151974184
    worker 1
        RAM:540595920896
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-139-generic
        node:cl-worker23
        disk:545591700
    worker 2
        RAM:540590923776
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-60-generic
        node:cl-worker25
        disk:145640764
    eval_parameters
        code:1747735357
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Citus-64-8-65536               1       64   65536          8           0                   32816.910411                32165.0             1000000                              7036.0

### Execution
                    experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Citus-64-8-65536-1               1       64   65536          1           0                       64589.47               154824.0           4998483                            1332.0             5001517                              1312.0

### Workflow

#### Actual
DBMS Citus-64-8-65536 - Pods [[1]]

#### Planned
DBMS Citus-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1      194.85     0.05          12.2                 12.7

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1        0.05        0          0.01                 0.01

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1     4247.36    14.27         17.45                18.97

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1     1078.63     7.92          0.63                 0.63

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
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

+-----------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| Volumes of Workers                | configuration     |   experiment | dbms   | storage_class_name   | storage   | status   | size   | used   |
+===================================+===================+==============+========+======================+===========+==========+========+========+
| bxw-bexhoma-worker-citus-ycsb-1-0 | Citus-64-8-65536  |   1742471862 | Citus  | shared               | 50Gi      | Bound    | 50.0G  | 1.4G   |
+-----------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bxw-bexhoma-worker-citus-ycsb-1-1 | Citus-64-8-65536  |   1742471862 | Citus  | shared               | 50Gi      | Bound    | 50.0G  | 1.4G   |
+-----------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bxw-bexhoma-worker-citus-ycsb-1-2 | Citus-64-8-65536  |   1742471862 | Citus  | shared               | 50Gi      | Bound    | 50.0G  | 1.2G   |
+-----------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

doc_ycsb_citus_2.log
```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1809s 
    Code: 1744731317
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.4.
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
    disk:202342908
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:982980992
        volume_size:50.0G
        volume_used:40.0M
    worker 1
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:115943464
        volume_size:50.0G
        volume_used:40.0M
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:163876460
        volume_size:50.0G
        volume_used:40.0M
    eval_parameters
        code:1744731317
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3
Citus-64-8-65536-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202343068
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:982977948
        volume_size:50.0G
        volume_used:1.4G
    worker 1
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:115944420
        volume_size:50.0G
        volume_used:1.4G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:163876612
        volume_size:50.0G
        volume_used:1.4G
    eval_parameters
        code:1744731317
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Citus-64-8-65536               1       64   65536          8           0                   47203.424087                22102.0             1000000                              4681.0

### Execution
                      experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Citus-64-8-65536-1-1               1       64   65536          1           0                       37347.16               267758.0           4998375                            4887.0             5001625                              5011.0
Citus-64-8-65536-2-1               2       64   65536          1           0                       49968.27               200127.0           4998443                            4387.0             5001557                              4423.0

### Workflow

#### Actual
DBMS Citus-64-8-65536 - Pods [[1], [1]]

#### Planned
DBMS Citus-64-8-65536 - Pods [[1], [1]]

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1      159.24     0.55          9.06                10.06

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1       85.26        0          2.89                 2.93

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1     3905.95     9.84         13.41                14.93
Citus-64-8-65536-2-1     3596.33     5.24         13.51                14.95

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1     1295.50     6.90          0.63                 0.67
Citus-64-8-65536-2-1     1270.08     6.67          0.63                 0.63

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

doc_benchbase_citus_1.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1419s 
    Code: 1744733178
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.4.
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
    disk:202385032
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:984406844
    worker 1
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:161143388
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:165151968
    eval_parameters
                code:1744733178
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:3
Citus-1-1-1024-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202406148
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:984693436
    worker 1
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:161504272
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:165453560
    eval_parameters
                code:1744733178
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:3

### Execution
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1               1         16   16384          1  300.0           0                        712.78                     709.74         0.0                                                      48135.0                                              22434.0
Citus-1-1-1024-2               1         16   16384          2  300.0           1                        670.29                     664.76         0.0                                                      50671.0                                              23855.5

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
Citus-1-1-1024-1      185.0        1.0   1.0         311.351351
Citus-1-1-1024-2      185.0        1.0   2.0         311.351351

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### Benchbase More Complex

TPC-C is performed at 128 warehouses.
The 64 threads of the client are split into a cascading sequence of 1,2,4 and 8 pods.
At first, we remove old PVC:

```bash
kubectl delete pvc bexhoma-storage-citus-benchbase-128
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-128-0
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-128-1
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-128-2
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-128-3
```

The benchmark is run via

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 60 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_2.log &
```

### Evaluate Results

doc_benchbase_citus_2.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=128
    Type: benchbase
    Duration: 16199s 
    Code: 1744734649
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 128. Benchmarking runs for 60 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.4.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
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
    disk:202343256
    volume_size:100.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:982878804
        volume_size:100.0G
        volume_used:6.3G
    worker 1
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:160002240
        volume_size:100.0G
        volume_used:6.3G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:163885340
        volume_size:100.0G
        volume_used:40.0M
    worker 3
        RAM:540590956544
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker24
        disk:109323016
        volume_size:100.0G
        volume_used:6.3G
    eval_parameters
                code:1744734649
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202343428
    volume_size:100.0G
    volume_used:336.0M
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:982879476
        volume_size:100.0G
        volume_used:13.2G
    worker 1
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:160091660
        volume_size:100.0G
        volume_used:9.9G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:163885892
        volume_size:100.0G
        volume_used:8.2G
    worker 3
        RAM:540590956544
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker24
        disk:109324632
        volume_size:100.0G
        volume_used:10.1G
    eval_parameters
                code:1744734649
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202343600
    volume_size:100.0G
    volume_used:336.0M
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:982945896
        volume_size:100.0G
        volume_used:20.0G
    worker 1
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:160198060
        volume_size:100.0G
        volume_used:13.8G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:163886440
        volume_size:100.0G
        volume_used:11.7G
    worker 3
        RAM:540590956544
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker24
        disk:109334664
        volume_size:100.0G
        volume_used:13.5G
    eval_parameters
                code:1744734649
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202343772
    volume_size:100.0G
    volume_used:336.0M
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:982880688
        volume_size:100.0G
        volume_used:20.0G
    worker 1
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:160305552
        volume_size:100.0G
        volume_used:13.8G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:151090456
        volume_size:100.0G
        volume_used:11.7G
    worker 3
        RAM:540590956544
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker24
        disk:109335864
        volume_size:100.0G
        volume_used:13.5G
    eval_parameters
                code:1744734649
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4

### Execution
                  experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1               1         64   16384          1  3600.0           0                       1180.57                    1175.26         0.0                                                     183619.0                                             54201.00
Citus-1-1-1024-2               1         64   16384          2  3600.0          13                        940.52                     934.46         0.0                                                     303991.0                                             68037.50
Citus-1-1-1024-3               1         64   16384          4  3600.0          21                        608.63                     603.56         0.0                                                     466360.0                                            105142.00
Citus-1-1-1024-4               1         64   16384          8  3600.0           9                        377.71                     374.23         0.0                                                     735010.0                                            169424.12

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[2, 8, 4, 1]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
Citus-1-1-1024-1      765.0        1.0   1.0         602.352941
Citus-1-1-1024-2      765.0        1.0   2.0         602.352941
Citus-1-1-1024-3      765.0        1.0   4.0         602.352941
Citus-1-1-1024-4      765.0        1.0   8.0         602.352941

### Ingestion - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1     3297.83     3.62         24.14                36.84
Citus-1-1-1024-2     3297.83     3.62         24.14                36.84
Citus-1-1-1024-3     3297.83     3.62         24.14                36.84
Citus-1-1-1024-4     3297.83     3.62         24.14                36.84

### Ingestion - Loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1    12853.45    30.66          1.32                 1.32
Citus-1-1-1024-2    12853.45    30.66          1.32                 1.32
Citus-1-1-1024-3    12853.45    30.66          1.32                 1.32
Citus-1-1-1024-4    12853.45    30.66          1.32                 1.32

### Execution - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1   170683.87    36.19         31.74                48.47
Citus-1-1-1024-2   141296.88    30.15         34.93                54.56
Citus-1-1-1024-3    75371.87    16.85         36.85                58.40
Citus-1-1-1024-4    42240.17     8.77         37.97                60.74

### Execution - Benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1     9167.22     2.95          1.66                 1.66
Citus-1-1-1024-2     9167.22     2.51          2.94                 2.94
Citus-1-1-1024-3     7970.36     1.41          5.43                 5.43
Citus-1-1-1024-4     5546.95     0.97          7.08                 7.09

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



### Benchbase Realistic

We run a benchmark with
* PVCs for persistent database
* monitoring
* a sensible number of workers (4)
* a sensible size (128 warehouses)
* a sensible number of threads (1024)
* suitable splittings (1x1280, 2x640, 5x256, 10x128)
* logging the state every 30 seconds
* a realistic target (4096 transactions per second)
* a realistic duration (20 minutes)
* a repetition (`-nc` is 2)
* keying and thinking tima activated (`-xkey`)

Note that the number of threads for each pod is a multiple of the number of warehouses.
At start, Benchbase assigns each thread to a fixed warehouse.
This way, we distribute the threads equally to the warehouses.
Each thread also gets assigned a fixed range of districts per warehouse.
Please also note, that this is not compliant to the TPC-C specifications, which state: *For each active warehouse in the database, the SUT must accept requests for transactions from a population of 10 terminals.*

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 20 \
  -slg 30 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xkey \
  -dbms Citus \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -nbf 4 \
  -tb 1024 \
  -m -mc \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_3.log &
```

### Evaluate Results

doc_benchbase_citus_3.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=128 (warehouses for TPC-C)
    Type: benchbase
    Duration: 12524s 
    Code: 1744225690
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 128. Benchmarking runs for 20 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [4]. Benchmarking has keying and thinking times activated.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [1280] threads, split into [1, 2, 5, 10] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Citus-1-1-1024-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201979472
    volume_size:100.0G
    volume_used:604.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081965506560
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1196110348
        volume_size:100.0G
        volume_used:22.0G
    worker 1
        RAM:540595875840
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:275391888
        volume_size:100.0G
        volume_used:14.4G
    worker 2
        RAM:540587528192
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-136-generic
        node:cl-worker22
        disk:363180784
        volume_size:100.0G
        volume_used:12.9G
    worker 3
        RAM:1081650987008
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:317648696
        volume_size:100.0G
        volume_used:13.8G
    eval_parameters
                code:1744225690
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-1-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201979644
    volume_size:100.0G
    volume_used:604.0M
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1081965506560
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1196112900
        volume_size:100.0G
        volume_used:22.0G
    worker 1
        RAM:540595875840
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:275392008
        volume_size:100.0G
        volume_used:14.4G
    worker 2
        RAM:540587528192
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-136-generic
        node:cl-worker22
        disk:363189352
        volume_size:100.0G
        volume_used:12.9G
    worker 3
        RAM:1081650987008
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:317650884
        volume_size:100.0G
        volume_used:13.8G
    eval_parameters
                code:1744225690
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-1-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201979644
    volume_size:100.0G
    volume_used:604.0M
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:1081965506560
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1196115280
        volume_size:100.0G
        volume_used:22.0G
    worker 1
        RAM:540595875840
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:275392072
        volume_size:100.0G
        volume_used:14.4G
    worker 2
        RAM:540587528192
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-136-generic
        node:cl-worker22
        disk:363189740
        volume_size:100.0G
        volume_used:12.9G
    worker 3
        RAM:1081650987008
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:317652984
        volume_size:100.0G
        volume_used:13.8G
    eval_parameters
                code:1744225690
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-1-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201979644
    volume_size:100.0G
    volume_used:604.0M
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:1081965506560
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1196117652
        volume_size:100.0G
        volume_used:22.0G
    worker 1
        RAM:540595875840
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:275392136
        volume_size:100.0G
        volume_used:14.4G
    worker 2
        RAM:540587528192
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-136-generic
        node:cl-worker22
        disk:363198244
        volume_size:100.0G
        volume_used:12.9G
    worker 3
        RAM:1081650987008
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-134-generic
        node:cl-worker34
        disk:317655140
        volume_size:100.0G
        volume_used:13.8G
    eval_parameters
                code:1744225690
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201979820
    volume_size:100.0G
    volume_used:604.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:540587528192
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-136-generic
        node:cl-worker22
        disk:363199300
        volume_size:100.0G
        volume_used:20.9G
    worker 1
        RAM:540595875840
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:275392292
        volume_size:100.0G
        volume_used:13.6G
    worker 2
        RAM:1081965506560
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1196121040
        volume_size:100.0G
        volume_used:12.2G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:204351340
        volume_size:100.0G
        volume_used:12.9G
    eval_parameters
                code:1744225690
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201979820
    volume_size:100.0G
    volume_used:604.0M
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    worker 0
        RAM:540587528192
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-136-generic
        node:cl-worker22
        disk:363200180
        volume_size:100.0G
        volume_used:20.9G
    worker 1
        RAM:540595875840
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:275392356
        volume_size:100.0G
        volume_used:13.6G
    worker 2
        RAM:1081965506560
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1196123464
        volume_size:100.0G
        volume_used:12.2G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:204351424
        volume_size:100.0G
        volume_used:12.9G
    eval_parameters
                code:1744225690
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201979996
    volume_size:100.0G
    volume_used:604.0M
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    worker 0
        RAM:540587528192
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-136-generic
        node:cl-worker22
        disk:363208700
        volume_size:100.0G
        volume_used:20.9G
    worker 1
        RAM:540595875840
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:275392480
        volume_size:100.0G
        volume_used:13.6G
    worker 2
        RAM:1081965506560
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1196126044
        volume_size:100.0G
        volume_used:12.2G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:204351456
        volume_size:100.0G
        volume_used:12.9G
    eval_parameters
                code:1744225690
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201979996
    volume_size:100.0G
    volume_used:604.0M
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    worker 0
        RAM:540587528192
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-136-generic
        node:cl-worker22
        disk:363209068
        volume_size:100.0G
        volume_used:20.9G
    worker 1
        RAM:540595875840
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:275392540
        volume_size:100.0G
        volume_used:13.6G
    worker 2
        RAM:1081965506560
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1196128244
        volume_size:100.0G
        volume_used:12.2G
    worker 3
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:204351488
        volume_size:100.0G
        volume_used:12.9G
    eval_parameters
                code:1744225690
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4

### Execution
                    experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1-1               1       1280    4096          1  1200.0           0                         60.77                      60.49       99.22                                                     194436.0                                             137768.0
Citus-1-1-1024-1-2               1       1280    4096          2  1200.0           0                         61.02                      60.73       99.61                                                     135335.0                                              44913.5
Citus-1-1-1024-1-3               1       1280    4095          5  1200.0           0                         61.32                      61.03      100.10                                                     129204.0                                              45583.0
Citus-1-1-1024-1-4               1       1280    4090         10  1200.0           0                         60.99                      60.72       99.60                                                     150526.0                                              46910.0
Citus-1-1-1024-2-1               2       1280    4096          1  1200.0           0                         60.98                      60.73       99.61                                                     193737.0                                              58991.0
Citus-1-1-1024-2-2               2       1280    4096          2  1200.0           0                         61.19                      60.89       99.88                                                     147501.0                                              45104.0
Citus-1-1-1024-2-3               2       1280    4095          5  1200.0           0                         61.20                      60.93       99.95                                                     130050.0                                              42462.4
Citus-1-1-1024-2-4               2       1280    4090         10  1200.0           0                         61.15                      60.88       99.86                                                     122215.0                                              43099.0

Warehouses: 128

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[10, 5, 2, 1], [5, 10, 2, 1]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2, 5, 10], [1, 2, 5, 10]]

### Loading
                    time_load  terminals  pods  Imported warehouses [1/h]
Citus-1-1-1024-1-1      840.0        1.0   1.0                 548.571429
Citus-1-1-1024-1-2      840.0        1.0   2.0                 548.571429
Citus-1-1-1024-1-3      840.0        1.0   5.0                 548.571429
Citus-1-1-1024-1-4      840.0        1.0  10.0                 548.571429
Citus-1-1-1024-2-1      840.0        1.0   1.0                 548.571429
Citus-1-1-1024-2-2      840.0        1.0   2.0                 548.571429
Citus-1-1-1024-2-3      840.0        1.0   5.0                 548.571429
Citus-1-1-1024-2-4      840.0        1.0  10.0                 548.571429

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1-1     3213.56     1.24         33.36                54.50
Citus-1-1-1024-1-2     3148.25     0.99         34.48                56.97
Citus-1-1-1024-1-3     3137.68     0.93         34.91                58.53
Citus-1-1-1024-1-4     3160.31     1.54         35.07                59.37
Citus-1-1-1024-2-1     3090.74     1.28         30.93                51.07
Citus-1-1-1024-2-2     3116.33     1.65         32.42                54.01
Citus-1-1-1024-2-3     3123.71     1.37         33.38                56.32
Citus-1-1-1024-2-4     3114.01     1.17         33.95                57.72

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1-1      352.42     1.00          4.04                 4.04
Citus-1-1-1024-1-2      352.42     0.60          7.90                 7.90
Citus-1-1-1024-1-3      486.89     1.01         10.70                10.70
Citus-1-1-1024-1-4      618.90     1.40         15.16                15.16
Citus-1-1-1024-2-1      364.47     0.66          4.05                 4.05
Citus-1-1-1024-2-2      364.47     1.00          7.95                 7.95
Citus-1-1-1024-2-3      544.68     1.93          9.79                 9.79
Citus-1-1-1024-2-4      636.80     1.04         14.26                14.26

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
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
  -xlat \
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

doc_hammerdb_citus_1.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1117s 
    Code: 1743765273
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-BHT-8-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201377888
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:151410852
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:234755912
    worker 2
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:977073952

### Execution
                 experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency     NOPM       TPM  duration  errors
Citus-BHT-8-1-1               1      16       1          1     30.12     60.59         0.0  47853.0  109891.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS Citus-BHT-8-1 - Pods [[1]]

#### Planned
DBMS Citus-BHT-8-1 - Pods [[1]]

### Loading
                 time_load  terminals  pods  Imported warehouses [1/h]
Citus-BHT-8-1-1      105.0        1.0   1.0                 548.571429

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```

### HammerDB More Complex Example

```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 128 \
  -sd 30 \
  -xlat \
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
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/doc_hammerdb_citus_2.log &
```

### Evaluate Results

doc_hammerdb_citus_2.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=128 (warehouses for TPC-C)
    Type: tpcc
    Duration: 9480s 
    Code: 1744750944
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 128. Benchmarking runs for 30 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.4.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [128] threads, split into [1] pods.
    Benchmarking is tested with [128] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-BHT-128-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202343936
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:151091148
        volume_size:50.0G
        volume_used:6.1G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:982881444
        volume_size:50.0G
        volume_used:3.2G
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:359384420
        volume_size:50.0G
        volume_used:3.2G
    worker 3
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:160448564
        volume_size:50.0G
        volume_used:6.1G
    eval_parameters
        code:1744750944
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-128-1-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202344108
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:151091464
        volume_size:50.0G
        volume_used:14.4G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:982881772
        volume_size:50.0G
        volume_used:9.8G
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:359384764
        volume_size:50.0G
        volume_used:9.3G
    worker 3
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:223546292
        volume_size:50.0G
        volume_used:10.1G
    eval_parameters
        code:1744750944
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-128-1-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202344108
    volume_size:50.0G
    volume_used:84.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:151091760
        volume_size:50.0G
        volume_used:22.9G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1006681476
        volume_size:50.0G
        volume_used:16.8G
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:359385164
        volume_size:50.0G
        volume_used:14.2G
    worker 3
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:248673404
        volume_size:50.0G
        volume_used:18.1G
    eval_parameters
        code:1744750944
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-128-1-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202344280
    volume_size:50.0G
    volume_used:84.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:151092080
        volume_size:50.0G
        volume_used:30.3G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1006681848
        volume_size:50.0G
        volume_used:21.7G
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:359385556
        volume_size:50.0G
        volume_used:20.0G
    worker 3
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:247911304
        volume_size:50.0G
        volume_used:25.6G
    eval_parameters
        code:1744750944
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4

### Execution
                   experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency      NOPM        TPM  duration  errors
Citus-BHT-128-1-1               1     128       1          1    175.64    731.47         0.0  90461.00  207968.00        30       0
Citus-BHT-128-1-2               1     128       2          2    181.98    763.57         0.0  81288.00  186906.00        30       0
Citus-BHT-128-1-3               1     128       3          4    187.10    731.18         0.0  90084.25  207212.75        30       0
Citus-BHT-128-1-4               1     128       4          8    180.99    697.19         0.0  89054.25  204935.75        30       0

Warehouses: 128

### Workflow

#### Actual
DBMS Citus-BHT-128-1 - Pods [[8, 4, 2, 1]]

#### Planned
DBMS Citus-BHT-128-1 - Pods [[1, 2, 4, 8]]

### Loading
                   time_load  terminals  pods  Imported warehouses [1/h]
Citus-BHT-128-1-1      446.0        1.0   1.0                1033.183857
Citus-BHT-128-1-2      446.0        1.0   2.0                1033.183857
Citus-BHT-128-1-3      446.0        1.0   4.0                1033.183857
Citus-BHT-128-1-4      446.0        1.0   8.0                1033.183857

### Ingestion - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1      900.36     0.84         21.89                35.03
Citus-BHT-128-1-2      900.36     0.84         21.89                35.03
Citus-BHT-128-1-3      900.36     0.84         21.89                35.03
Citus-BHT-128-1-4      900.36     0.84         21.89                35.03

### Ingestion - Loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1     4520.77     8.71          0.72                 0.75
Citus-BHT-128-1-2     4520.77     8.71          0.72                 0.75
Citus-BHT-128-1-3     4520.77     8.71          0.72                 0.75
Citus-BHT-128-1-4     4520.77     8.71          0.72                 0.75

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1   167836.87    68.67         33.89                53.94
Citus-BHT-128-1-2   157110.72    57.48         40.27                68.89
Citus-BHT-128-1-3   184903.68    68.66         46.32                82.87
Citus-BHT-128-1-4   211648.87    66.18         52.86                94.89

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1     2315.83     1.38          2.60                 2.60
Citus-BHT-128-1-2     2278.81     1.32          3.09                 3.10
Citus-BHT-128-1-3     2221.49     0.96          2.31                 2.32
Citus-BHT-128-1-4     2270.59     0.80          2.57                 2.57

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

[3] [Citus Data Benchmark Toolkit](https://github.com/citusdata/citus-benchmark)
> Citus Data.
> Retrieved April 1, 2025, from https://github.com/citusdata/citus-benchmark

[4] [Citus Data Benchmark Toolkit HammerDB settings](https://github.com/citusdata/citus-benchmark/blob/master/run.tcl)
> Citus Data.
> Retrieved April 1, 2025, from https://github.com/citusdata/citus-benchmark/blob/master/run.tcl

[5] [Adding Postgres 16 support to Citus 12.1, plus schema-based sharding improvements](https://www.citusdata.com/blog/2023/09/22/adding-postgres-16-support-to-citus-12-1)
> Naisila Puka, September 22, 2023.
> Retrieved April 1, 2025, from https://www.citusdata.com/blog/2023/09/22/adding-postgres-16-support-to-citus-12-1

[6] [Understand what you run before publishing your (silly) benchmark results](https://dev.to/yugabyte/understand-what-you-run-before-publishing-your-silly-benchmark-results-48bb)
> Franck Pachot, YugabyteDB.
> Retrieved April 1, 2025, from https://dev.to/yugabyte/understand-what-you-run-before-publishing-your-silly-benchmark-results-48bb


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
  -nlt 250 \
  -nbp 1,2,5,10 \
  -nbt 250 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 200Gi \
  run </dev/null &>$LOG_DIR/doc_hammerdb_citus_3.log &
```

### Evaluate Results

doc_hammerdb_citus_3.log
```bash
## Show Summary

### Workload
HammerDB Workload SF=500 (warehouses for TPC-C)
    Type: tpcc
    Duration: 16725s 
    Code: 1744876650
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 500. Benchmarking runs for 20 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.4.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 200Gi.
    Loading is tested with [500] threads, split into [1] pods.
    Benchmarking is tested with [250] threads, split into [1, 2, 5, 10] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Citus-BHT-500-1-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202352260
    volume_size:200.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152082228
        volume_size:200.0G
        volume_used:24.3G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1051560540
        volume_size:200.0G
        volume_used:12.6G
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:379672364
        volume_size:200.0G
        volume_used:12.6G
    worker 3
        RAM:540590956544
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker24
        disk:136060772
        volume_size:200.0G
        volume_used:24.3G
    eval_parameters
        code:1744876650
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-500-1-1-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202352284
    volume_size:200.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152082460
        volume_size:200.0G
        volume_used:31.6G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1051560956
        volume_size:200.0G
        volume_used:24.7G
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:379672608
        volume_size:200.0G
        volume_used:23.2G
    worker 3
        RAM:540590956544
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker24
        disk:136246180
        volume_size:200.0G
        volume_used:31.5G
    eval_parameters
        code:1744876650
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-500-1-1-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202352504
    volume_size:200.0G
    volume_used:240.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152082660
        volume_size:200.0G
        volume_used:42.2G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1051561648
        volume_size:200.0G
        volume_used:27.4G
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:379672908
        volume_size:200.0G
        volume_used:26.4G
    worker 3
        RAM:540590956544
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker24
        disk:136523088
        volume_size:200.0G
        volume_used:42.1G
    eval_parameters
        code:1744876650
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-500-1-1-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202352520
    volume_size:200.0G
    volume_used:240.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152082872
        volume_size:200.0G
        volume_used:49.4G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1051173976
        volume_size:200.0G
        volume_used:38.2G
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:379673144
        volume_size:200.0G
        volume_used:37.2G
    worker 3
        RAM:540590956544
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker24
        disk:181106972
        volume_size:200.0G
        volume_used:48.7G
    eval_parameters
        code:1744876650
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-500-1-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202352716
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:376836832
        volume_size:200.0G
        volume_used:51.3G
    worker 1
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:379673944
        volume_size:200.0G
        volume_used:44.6G
    worker 2
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1051109388
        volume_size:200.0G
        volume_used:40.7G
    worker 3
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152083616
        volume_size:200.0G
        volume_used:50.3G
    eval_parameters
        code:1744876650
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-500-1-2-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202352888
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:376880144
        volume_size:200.0G
        volume_used:51.3G
    worker 1
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:379674244
        volume_size:200.0G
        volume_used:44.6G
    worker 2
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1051109660
        volume_size:200.0G
        volume_used:40.7G
    worker 3
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152083832
        volume_size:200.0G
        volume_used:50.3G
    eval_parameters
        code:1744876650
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-500-1-2-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202352812
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:376923608
        volume_size:200.0G
        volume_used:51.3G
    worker 1
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:379674484
        volume_size:200.0G
        volume_used:44.6G
    worker 2
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1051109880
        volume_size:200.0G
        volume_used:40.7G
    worker 3
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152084072
        volume_size:200.0G
        volume_used:50.3G
    eval_parameters
        code:1744876650
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-500-1-2-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202352952
    volume_size:200.0G
    volume_used:236.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:2164173475840
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:376965756
        volume_size:200.0G
        volume_used:51.3G
    worker 1
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:379674776
        volume_size:200.0G
        volume_used:44.6G
    worker 2
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1051110168
        volume_size:200.0G
        volume_used:40.7G
    worker 3
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152084280
        volume_size:200.0G
        volume_used:50.3G
    eval_parameters
        code:1744876650
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4

### Execution
                     experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency      NOPM       TPM  duration  errors
Citus-BHT-500-1-1-1               1     250       1          1    323.92   1127.25         0.0   85314.0  196268.0        20       0
Citus-BHT-500-1-1-2               1     250       2          2    351.24   1214.07         0.0   86173.5  198181.0        20       0
Citus-BHT-500-1-1-3               1     250       3          5    333.16   1180.07         0.0  106589.8  245256.2        20       0
Citus-BHT-500-1-1-4               1     250       4         10    323.61   1133.99         0.0  106287.4  244406.2        20       0
Citus-BHT-500-1-2-1               2     250       1          1    309.62   1018.56         0.0  121803.0  279843.0        20       0
Citus-BHT-500-1-2-2               2     250       2          2    339.30   1071.64         0.0  117844.5  270945.0        20       0
Citus-BHT-500-1-2-3               2     250       3          5    352.60   1177.73         0.0   81072.6  186345.8        20       0
Citus-BHT-500-1-2-4               2     250       4         10    330.36   1223.48         0.0  107350.8  246932.1        20       0

Warehouses: 500

### Workflow

#### Actual
DBMS Citus-BHT-500-1 - Pods [[10, 1, 5, 2], [5, 2, 10, 1]]

#### Planned
DBMS Citus-BHT-500-1 - Pods [[1, 2, 5, 10], [1, 2, 5, 10]]

### Loading
                     time_load  terminals  pods  Imported warehouses [1/h]
Citus-BHT-500-1-1-1     1142.0        1.0   1.0                1576.182137
Citus-BHT-500-1-1-2     1142.0        1.0   2.0                1576.182137
Citus-BHT-500-1-1-3     1142.0        1.0   5.0                1576.182137
Citus-BHT-500-1-1-4     1142.0        1.0  10.0                1576.182137
Citus-BHT-500-1-2-1     1142.0        1.0   1.0                1576.182137
Citus-BHT-500-1-2-2     1142.0        1.0   2.0                1576.182137
Citus-BHT-500-1-2-3     1142.0        1.0   5.0                1576.182137
Citus-BHT-500-1-2-4     1142.0        1.0  10.0                1576.182137

### Ingestion - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-500-1-1-1     3958.52      2.7          58.1               112.13
Citus-BHT-500-1-1-2     3958.52      2.7          58.1               112.13
Citus-BHT-500-1-1-3     3958.52      2.7          58.1               112.13
Citus-BHT-500-1-1-4     3958.52      2.7          58.1               112.13

### Ingestion - Loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-500-1-1-1     18441.5    32.07          2.42                 2.42
Citus-BHT-500-1-1-2     18441.5    32.07          2.42                 2.42
Citus-BHT-500-1-1-3     18441.5    32.07          2.42                 2.42
Citus-BHT-500-1-1-4     18441.5    32.07          2.42                 2.42

### Execution - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-500-1-1-1   276046.63   139.64         82.73               137.84
Citus-BHT-500-1-1-2   255307.15   122.19         87.76               151.97
Citus-BHT-500-1-1-3   294404.63   118.22         94.11               166.56
Citus-BHT-500-1-1-4   250797.54   123.65        100.06               182.28
Citus-BHT-500-1-2-1   223777.77   108.71         64.63               222.91
Citus-BHT-500-1-2-2   226418.36   107.47         75.15               225.46
Citus-BHT-500-1-2-3   173524.63   108.58         82.56               220.75
Citus-BHT-500-1-2-4   218394.51   105.73         89.41               211.31

### Execution - Benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-500-1-1-1     1521.00     1.50          1.84                 1.84
Citus-BHT-500-1-1-2     1521.00     1.44          2.63                 2.64
Citus-BHT-500-1-1-3     1726.17     0.97          2.68                 2.69
Citus-BHT-500-1-1-4     1849.01     0.98          2.90                 2.90
Citus-BHT-500-1-2-1     2093.54     1.96          2.30                 2.30
Citus-BHT-500-1-2-2     2093.54     1.88          3.13                 3.13
Citus-BHT-500-1-2-3     2068.97     1.42          3.19                 3.19
Citus-BHT-500-1-2-4     1829.70     0.94          2.74                 2.74

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


## TPC-H

We build the schema similar to [2] in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/tpch/Citus/initschema-tpch.sql

```sql
select create_reference_table('nation');
select create_reference_table('region');
select create_reference_table('part');
select create_reference_table('supplier');
select create_reference_table('partsupp');
select create_reference_table('customer');
select create_distributed_table('orders', 'o_orderkey');
select create_distributed_table('lineitem', 'l_orderkey');
```

It is also mentioned in [1] that the big tables `orders` and `linetime` should be distributed and the others should be replicated.
As the paper used Citus 9.5, columnar storage has not been included in Citus [3].
Note that columnar storage has some limitations as no UPDATEs, no DELETEs and no FOREIGN KEYs.
Also note that Citus does not support all TPC-H queries.
In a correlated subquery there cannot be a replicated table, so we have to rewrite Q22.

[1] [Citus: Distributed PostgreSQL for Data-Intensive Applications](https://dl.acm.org/doi/10.1145/3448016.3457551)
> Umur Cubukcu, Ozgun Erdogan, Sumedh Pathak, Sudhakar Sannakkayala, and Marco Slot.
> 2021. In Proceedings of the 2021 International Conference on Management of Data (SIGMOD '21).
> Association for Computing Machinery, New York, NY, USA, 2490–2502.
> https://dl.acm.org/doi/10.1145/3448016.3457551

[2] [Citus TPC-H tests - schema](https://github.com/dimitri/tpch-citus/tree/master/schema)
> Dimitri Fontaine.
> Retrieved April 1, 2025, from https://github.com/dimitri/tpch-citus/tree/master/schema

[3] [Citus columnar storage](https://docs.citusdata.com/en/stable/admin_guide/table_management.html#columnar-storage)
> Citus Data.
> Retrieved April 1, 2025, from https://docs.citusdata.com/en/stable/admin_guide/table_management.html#columnar-storage


### TPC-H Simple Example


```bash
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dt \
  -t 1200 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_citus_1.log &
```


### Evaluate Results

test_tpch_testcase_citus_1.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 1316s 
    Code: 1743612001
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker23.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-BHT-8-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:540595900416
    CPU:AMD EPYC 7352 24-Core Processor
    Cores:96
    host:5.15.0-134-generic
    node:cl-worker23
    disk:151625644
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:229673792
    worker 1
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:966307088
    worker 2
        RAM:540595879936
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker25
        disk:132956400
    worker 3
        RAM:540595900416
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-134-generic
        node:cl-worker23
        disk:151625652

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 Citus-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             199.73
Minimum Cost Supplier Query (TPC-H Q2)                        292.55
Shipping Priority (TPC-H Q3)                                  169.66
Order Priority Checking Query (TPC-H Q4)                      130.10
Local Supplier Volume (TPC-H Q5)                              168.90
Forecasting Revenue Change (TPC-H Q6)                         109.08
Forecasting Revenue Change (TPC-H Q7)                         170.97
National Market Share (TPC-H Q8)                              173.83
Product Type Profit Measure (TPC-H Q9)                        243.36
Forecasting Revenue Change (TPC-H Q10)                        278.42
Important Stock Identification (TPC-H Q11)                    163.41
Shipping Modes and Order Priority (TPC-H Q12)                 122.43
Customer Distribution (TPC-H Q13)                            1527.17
Forecasting Revenue Change (TPC-H Q14)                        139.66
Top Supplier Query (TPC-H Q15)                                281.32
Parts/Supplier Relationship (TPC-H Q16)                       395.22
Small-Quantity-Order Revenue (TPC-H Q17)                     4942.78
Large Volume Customer (TPC-H Q18)                             218.35
Discounted Revenue (TPC-H Q19)                                168.64
Potential Part Promotion (TPC-H Q20)                         3104.19
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           155.45
Global Sales Opportunity Query (TPC-H Q22)                   1456.73

### Loading [s]
                 timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
Citus-BHT-8-1-1           1.0           18.0         5.0       24.0      54.0

### Geometric Mean of Medians of Timer Run [s]
                 Geo Times [s]
DBMS                          
Citus-BHT-8-1-1           0.32

### Power@Size
                 Power@Size [~Q/h]
DBMS                              
Citus-BHT-8-1-1           12042.26

### Throughput@Size
                                            time [s]  count  SF  Throughput@Size [~GB/h]
DBMS          SF num_experiment num_client                                              
Citus-BHT-8-1 1  1              1                 19      1   1                  4168.42

### Workflow

#### Actual
DBMS Citus-BHT-8 - Pods [[1]]

#### Planned
DBMS Citus-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```

### TPC-H More Complex Example

At first we remove possibly existing PVC:

```bash
kubectl delete pvc bexhoma-storage-citus-tpch-10
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-0
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-1
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-2
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-3
```

Then we run TPC-H Power Test at SF=10.
Note that this takes a lot of disk space including for indexes.

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 10 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dt \
  -t 7200 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,1 \
  -nc 2 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_citus_2.log &
```

### Evaluate Results

test_tpch_testcase_citus_2.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=10
    Type: tpch
    Duration: 3755s 
    Code: 1744815465
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 14400.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.4.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Citus-BHT-8-1-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202349328
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965461504
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1343452816
        volume_size:50.0G
        volume_used:11.5G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1046001560
        volume_size:50.0G
        volume_used:14.0G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152097984
        volume_size:50.0G
        volume_used:11.7G
    worker 3
        RAM:1081649926144
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-57-generic
        node:cl-worker34
        disk:351524872
        volume_size:50.0G
        volume_used:13.8G
    eval_parameters
        code:1744815465
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False
Citus-BHT-8-1-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202349328
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965461504
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1345147172
        volume_size:50.0G
        volume_used:13.9G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1047789896
        volume_size:50.0G
        volume_used:14.0G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152098028
        volume_size:50.0G
        volume_used:11.7G
    worker 3
        RAM:1081649926144
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-57-generic
        node:cl-worker34
        disk:351525496
        volume_size:50.0G
        volume_used:13.8G
    eval_parameters
        code:1744815465
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False
Citus-BHT-8-2-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202349304
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965461504
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1347328352
        volume_size:50.0G
        volume_used:13.8G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1047696428
        volume_size:50.0G
        volume_used:13.8G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152098424
        volume_size:50.0G
        volume_used:13.8G
    worker 3
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:359889828
        volume_size:50.0G
        volume_used:13.8G
    eval_parameters
        code:1744815465
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False
Citus-BHT-8-2-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202349304
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965461504
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1347672124
        volume_size:50.0G
        volume_used:13.8G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1047696476
        volume_size:50.0G
        volume_used:13.8G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152098472
        volume_size:50.0G
        volume_used:13.8G
    worker 3
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:359889888
        volume_size:50.0G
        volume_used:13.8G
    eval_parameters
        code:1744815465
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 Citus-BHT-8-1-1-1  Citus-BHT-8-1-2-1  Citus-BHT-8-2-1-1  Citus-BHT-8-2-2-1
Pricing Summary Report (TPC-H Q1)                               443.82             444.59            1860.83             437.99
Minimum Cost Supplier Query (TPC-H Q2)                         2615.95            2477.54            2864.75            2838.51
Shipping Priority (TPC-H Q3)                                    537.23             541.93            1661.67             551.20
Order Priority Checking Query (TPC-H Q4)                        303.47             306.14             306.65             306.34
Local Supplier Volume (TPC-H Q5)                                791.98             803.74             774.55             766.24
Forecasting Revenue Change (TPC-H Q6)                           263.13             260.39             245.19             249.11
Forecasting Revenue Change (TPC-H Q7)                           540.53             550.11             528.63             539.27
National Market Share (TPC-H Q8)                                536.52             540.47             701.36             535.15
Product Type Profit Measure (TPC-H Q9)                         1416.31            1375.44            2693.62            1395.79
Forecasting Revenue Change (TPC-H Q10)                         3916.89            3923.61            3937.84            3931.78
Important Stock Identification (TPC-H Q11)                     1072.78            1025.88            1077.38            1228.61
Shipping Modes and Order Priority (TPC-H Q12)                   408.14             430.25             434.41             439.38
Customer Distribution (TPC-H Q13)                             35439.58           35626.94           28437.23           28217.75
Forecasting Revenue Change (TPC-H Q14)                          442.56             425.67             449.14             450.61
Top Supplier Query (TPC-H Q15)                                 3722.10            4008.66            3742.02            3961.52
Parts/Supplier Relationship (TPC-H Q16)                        2086.74            1963.68            2086.38            2187.50
Small-Quantity-Order Revenue (TPC-H Q17)                      89759.71           89029.70           89422.64           89259.54
Large Volume Customer (TPC-H Q18)                              1270.68            1273.51            1234.56            1346.52
Discounted Revenue (TPC-H Q19)                                  576.64             551.96             542.52             557.74
Potential Part Promotion (TPC-H Q20)                          90892.59           85358.68           92801.01           92126.22
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)             424.73             405.02            1394.19             391.89
Global Sales Opportunity Query (TPC-H Q22)                    25895.98           28064.43           27326.80           24445.61

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
Citus-BHT-8-1-1-1           1.0          389.0         3.0      141.0     541.0
Citus-BHT-8-1-2-1           1.0          389.0         3.0      141.0     541.0
Citus-BHT-8-2-1-1           1.0          389.0         3.0      141.0     541.0
Citus-BHT-8-2-2-1           1.0          389.0         3.0      141.0     541.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
Citus-BHT-8-1-1-1           1.79
Citus-BHT-8-1-2-1           1.78
Citus-BHT-8-2-1-1           2.20
Citus-BHT-8-2-2-1           1.79

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
Citus-BHT-8-1-1-1           20570.16
Citus-BHT-8-1-2-1           20687.63
Citus-BHT-8-2-1-1           16764.43
Citus-BHT-8-2-2-1           20566.88

### Throughput@Size
                                              time [s]  count  SF  Throughput@Size [~GB/h]
DBMS            SF num_experiment num_client                                              
Citus-BHT-8-1-1 10 1              1                270      1  10                  2933.33
Citus-BHT-8-1-2 10 1              2                268      1  10                  2955.22
Citus-BHT-8-2-1 10 2              1                273      1  10                  2901.10
Citus-BHT-8-2-2 10 2              2                265      1  10                  2988.68

### Workflow

#### Actual
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1     1522.86     2.51         40.34                74.73
Citus-BHT-8-1-2     1522.86     2.51         40.34                74.73

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1      172.47     0.29          0.05                10.54
Citus-BHT-8-1-2      172.47     0.29          0.05                10.54

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1     1091.66     2.47         45.01                74.74
Citus-BHT-8-1-2     1034.25     5.27         46.13                75.87
Citus-BHT-8-2-1     1137.02     5.96         44.98                98.05
Citus-BHT-8-2-2     1088.87     2.52         46.11               100.17

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1       18.03     0.08          0.33                 0.52
Citus-BHT-8-1-2       18.03     0.26          0.63                 0.82
Citus-BHT-8-2-1       18.88     0.00          0.30                 0.32
Citus-BHT-8-2-2       18.96     0.31          0.60                 0.63

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


### TPC-H Test Columnar Storage

Citus provides the option to make a table using columnar storage via `USING COLUMNAR`.
For Bexhoma's TPC-H, you can activate makeing the distributed tables `orders` and `lineitem` use columnar storage via `-icol`.
Note that this also means there will be no foreign key constraints and no indexes on these tables.

At first we remove possibly existing PVC:

```bash
kubectl delete pvc bexhoma-storage-citus-tpch-10
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-0
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-1
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-2
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-3
```

The experiment runs like this:

```bash
nohup python tpch.py -ms 1 -tr \
  -sf 10 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dt \
  -t 7200 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -icol \
  -nlp 8 \
  -nbp 1 \
  -ne 1,1 \
  -nc 2 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_citus_3.log &
```

### Evaluate Results

test_tpch_testcase_citus_3.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=10
    Type: tpch
    Duration: 19368s 
    Code: 1744819457
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 14400.
    Experiment uses bexhoma version 0.8.4.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Citus-BHT-8-1-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202349496
    volume_size:50.0G
    volume_used:22.7G
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1049393936
        volume_size:50.0G
        volume_used:13.8G
    worker 1
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152099016
        volume_size:50.0G
        volume_used:13.9G
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:359890364
        volume_size:50.0G
        volume_used:13.8G
    worker 3
        RAM:1081649926144
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-57-generic
        node:cl-worker34
        disk:351533204
        volume_size:50.0G
        volume_used:13.8G
    eval_parameters
        code:1744819457
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True
Citus-BHT-8-1-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202349668
    volume_size:50.0G
    volume_used:22.6G
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1049394604
        volume_size:50.0G
        volume_used:13.8G
    worker 1
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152099656
        volume_size:50.0G
        volume_used:13.9G
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:359891092
        volume_size:50.0G
        volume_used:13.8G
    worker 3
        RAM:1081649926144
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-57-generic
        node:cl-worker34
        disk:351540804
        volume_size:50.0G
        volume_used:13.8G
    eval_parameters
        code:1744819457
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True
Citus-BHT-8-2-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202349992
    volume_size:50.0G
    volume_used:22.6G
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965461504
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1347683628
        volume_size:50.0G
        volume_used:13.8G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1049461132
        volume_size:50.0G
        volume_used:13.9G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152100208
        volume_size:50.0G
        volume_used:13.8G
    worker 3
        RAM:1081649926144
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-57-generic
        node:cl-worker34
        disk:358780364
        volume_size:50.0G
        volume_used:13.8G
    eval_parameters
        code:1744819457
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True
Citus-BHT-8-2-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202350164
    volume_size:50.0G
    volume_used:22.6G
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965461504
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1347685420
        volume_size:50.0G
        volume_used:13.8G
    worker 1
        RAM:1077382836224
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1049395984
        volume_size:50.0G
        volume_used:13.9G
    worker 2
        RAM:540590919680
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-57-generic
        node:cl-worker25
        disk:152100820
        volume_size:50.0G
        volume_used:13.8G
    worker 3
        RAM:1081649926144
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-57-generic
        node:cl-worker34
        disk:358787652
        volume_size:50.0G
        volume_used:13.8G
    eval_parameters
        code:1744819457
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 Citus-BHT-8-1-1-1  Citus-BHT-8-1-2-1  Citus-BHT-8-2-1-1  Citus-BHT-8-2-2-1
Pricing Summary Report (TPC-H Q1)                             65779.99           63511.25           98018.61           61711.61
Minimum Cost Supplier Query (TPC-H Q2)                         4401.91            3973.34           40628.68            3973.79
Shipping Priority (TPC-H Q3)                                  28435.81           28629.42           45500.19           27990.34
Order Priority Checking Query (TPC-H Q4)                      23872.90           23865.39           24730.36           24289.51
Local Supplier Volume (TPC-H Q5)                              31405.97           30205.39           30654.05           30075.84
Forecasting Revenue Change (TPC-H Q6)                         20157.67           20206.86           20228.05           20126.39
Forecasting Revenue Change (TPC-H Q7)                         30587.42           30484.55           30461.12           30487.10
National Market Share (TPC-H Q8)                              31841.77           32619.63           32341.27           31872.98
Product Type Profit Measure (TPC-H Q9)                       207802.43          203000.45          222922.00          204829.02
Forecasting Revenue Change (TPC-H Q10)                        29413.22           29454.66           29961.48           29842.85
Important Stock Identification (TPC-H Q11)                     1942.21            1937.09            1954.27            1961.53
Shipping Modes and Order Priority (TPC-H Q12)                 33015.23           32823.54           32935.46           32907.28
Customer Distribution (TPC-H Q13)                             24518.88           24399.19           24735.34           25024.94
Forecasting Revenue Change (TPC-H Q14)                        18856.41           18856.08           19086.12           18944.99
Top Supplier Query (TPC-H Q15)                                19565.83           19594.17           19775.17           19552.01
Parts/Supplier Relationship (TPC-H Q16)                        3585.90            3587.43            3562.15            3597.15
Small-Quantity-Order Revenue (TPC-H Q17)                      59878.22           59718.86           59654.29           58633.14
Large Volume Customer (TPC-H Q18)                             58962.27           59364.37           58353.81           59691.41
Discounted Revenue (TPC-H Q19)                                36038.94           36033.96           36279.05           35942.15
Potential Part Promotion (TPC-H Q20)                          27387.59           28264.77           27799.12           28371.86
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)         3272881.36         3290031.65         3227600.38         3253855.82
Global Sales Opportunity Query (TPC-H Q22)                     8956.66            8866.38            8767.24            8632.93

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
Citus-BHT-8-1-1-1           1.0          576.0         4.0      582.0    1170.0
Citus-BHT-8-1-2-1           1.0          576.0         4.0      582.0    1170.0
Citus-BHT-8-2-1-1           1.0          576.0         4.0      582.0    1170.0
Citus-BHT-8-2-2-1           1.0          576.0         4.0      582.0    1170.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
Citus-BHT-8-1-1-1          29.48
Citus-BHT-8-1-2-1          29.28
Citus-BHT-8-2-1-1          34.08
Citus-BHT-8-2-2-1          29.20

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
Citus-BHT-8-1-1-1            1238.23
Citus-BHT-8-1-2-1            1246.69
Citus-BHT-8-2-1-1            1070.28
Citus-BHT-8-2-2-1            1249.33

### Throughput@Size
                                              time [s]  count  SF  Throughput@Size [~GB/h]
DBMS            SF num_experiment num_client                                              
Citus-BHT-8-1-1 10 1              1               4048      1  10                   195.65
Citus-BHT-8-1-2 10 1              2               4060      1  10                   195.07
Citus-BHT-8-2-1 10 2              1               4103      1  10                   193.03
Citus-BHT-8-2-2 10 2              2               4021      1  10                   196.97

### Workflow

#### Actual
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1        24.4     0.01         15.43                15.94
Citus-BHT-8-1-2        24.4     0.01         15.43                15.94

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1      171.75     0.29          0.05                10.53
Citus-BHT-8-1-2      171.75     0.29          0.05                10.53

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1       77.51     0.02         15.43                15.94
Citus-BHT-8-1-2       77.81     0.01         15.43                15.94
Citus-BHT-8-2-1       84.50     0.02         15.41                15.74
Citus-BHT-8-2-2       81.41     0.02         15.42                15.74

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1       23.73     0.02          0.31                 0.31
Citus-BHT-8-1-2       23.73     0.21          0.55                 0.57
Citus-BHT-8-2-1       24.19     0.01          0.30                 0.32
Citus-BHT-8-2-2       24.19     0.06          0.54                 0.57

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



