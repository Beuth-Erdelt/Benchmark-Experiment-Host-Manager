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

```bash
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
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 798s 
    Code: 1748850094
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
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:316353076
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
        disk:224757412
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:326266624
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:362021104
    eval_parameters
        code:1748850094
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Citus-64-8-65536               1       64   65536          8           0                   32750.020559                33275.0             1000000                              4843.5

### Execution
                    experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Citus-64-8-65536-1               1       64   65536          1           0                       64673.85               154622.0           4999423                            3225.0             5000577                              3269.0

### Workflow

#### Actual
DBMS Citus-64-8-65536 - Pods [[1]]

#### Planned
DBMS Citus-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1      146.49     0.27          12.2                12.73

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1        0.08        0          0.01                 0.01

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1     4874.24    10.93         17.43                18.94

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1     1133.59     8.21          0.62                 0.63

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


```bash
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
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1601s 
    Code: 1748850965
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
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:316311664
    volume_size:50.0G
    volume_used:40.0M
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
        disk:223872664
        volume_size:50.0G
        volume_used:40.0M
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:325379820
        volume_size:50.0G
        volume_used:40.0M
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:361131272
        volume_size:50.0G
        volume_used:40.0M
    eval_parameters
        code:1748850965
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3
Citus-64-8-65536-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:316311660
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:223877000
        volume_size:50.0G
        volume_used:1.4G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:325381092
        volume_size:50.0G
        volume_used:1.4G
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:361131272
        volume_size:50.0G
        volume_used:1.4G
    eval_parameters
        code:1748850965
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Citus-64-8-65536               1       64   65536          8           0                   32304.397529                33417.0             1000000                              5271.5

### Execution
                      experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Citus-64-8-65536-1-1               1       64   65536          1           0                       64620.36               154750.0           4996520                            3255.0             5003480                              3307.0
Citus-64-8-65536-2-1               2       64   65536          1           0                       64634.14               154717.0           4999773                            2923.0             5000227                              2921.0

### Workflow

#### Actual
DBMS Citus-64-8-65536 - Pods [[1], [1]]

#### Planned
DBMS Citus-64-8-65536 - Pods [[1], [1]]

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1      424.12     2.44         12.93                 14.2

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1        0.01        0           0.0                  0.0

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1     4476.36    14.18         17.37                18.88
Citus-64-8-65536-2-1     3819.10    14.10         17.45                19.32

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1-1     1137.33     8.23          0.63                 0.63
Citus-64-8-65536-2-1      964.66     8.67          0.63                 0.63

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


## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
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
```markdown
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1414s 
    Code: 1748852646
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:316353824
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
        disk:225406680
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:326659204
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:362406656
    eval_parameters
                code:1748852646
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:3
Citus-1-1-1024-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:316373636
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225678360
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:326898552
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:362605216
    eval_parameters
                code:1748852646
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:3

### Execution
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1               1         16   16384          1  300.0           0                        508.58                     506.35         0.0                                                      64912.0                                              31446.0
Citus-1-1-1024-2               1         16   16384          2  300.0           0                        472.79                     469.02         0.0                                                      70572.0                                              33824.5

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
Citus-1-1-1024-1      181.0        1.0   1.0         318.232044
Citus-1-1-1024-2      181.0        1.0   2.0         318.232044

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
  -sd 20 \
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
```markdown
## Show Summary

### Workload
Benchbase Workload SF=128
    Type: benchbase
    Duration: 16223s 
    Code: 1748854117
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 128. Benchmarking runs for 60 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:316311888
    volume_size:100.0G
    volume_used:40.0M
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
        disk:223892384
        volume_size:100.0G
        volume_used:6.3G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:325385896
        volume_size:100.0G
        volume_used:6.3G
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:361131512
        volume_size:100.0G
        volume_used:40.0M
    worker 3
        RAM:540590923776
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-60-generic
        node:cl-worker25
        disk:131061124
        volume_size:100.0G
        volume_used:6.3G
    eval_parameters
                code:1748854117
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:316312104
    volume_size:100.0G
    volume_used:284.0M
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:223898756
        volume_size:100.0G
        volume_used:12.9G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:325393576
        volume_size:100.0G
        volume_used:9.1G
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:361679540
        volume_size:100.0G
        volume_used:7.7G
    worker 3
        RAM:540590923776
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-60-generic
        node:cl-worker25
        disk:131062580
        volume_size:100.0G
        volume_used:9.5G
    eval_parameters
                code:1748854117
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:316312320
    volume_size:100.0G
    volume_used:284.0M
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:223915676
        volume_size:100.0G
        volume_used:19.2G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:325398924
        volume_size:100.0G
        volume_used:12.1G
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:361681840
        volume_size:100.0G
        volume_used:10.3G
    worker 3
        RAM:540590923776
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-60-generic
        node:cl-worker25
        disk:131064088
        volume_size:100.0G
        volume_used:12.4G
    eval_parameters
                code:1748854117
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:316312540
    volume_size:100.0G
    volume_used:284.0M
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:223924048
        volume_size:100.0G
        volume_used:19.2G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:325404352
        volume_size:100.0G
        volume_used:12.1G
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:361847524
        volume_size:100.0G
        volume_used:10.3G
    worker 3
        RAM:540590923776
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-60-generic
        node:cl-worker25
        disk:131068972
        volume_size:100.0G
        volume_used:12.4G
    eval_parameters
                code:1748854117
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4

### Execution
                  experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1               1         64   16384          1  3600.0           0                        999.12                     994.60         0.0                                                     163420.0                                             64049.00
Citus-1-1-1024-2               1         64   16384          2  3600.0           9                        753.47                     748.18         0.0                                                     315464.0                                             84929.50
Citus-1-1-1024-3               1         64   16384          4  3600.0          17                        605.22                     599.67         0.0                                                     403222.0                                            105734.50
Citus-1-1-1024-4               1         64   16384          8  3600.0          15                        359.78                     356.36         0.0                                                     696861.0                                            177872.88

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[8, 4, 1, 2]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
Citus-1-1-1024-1      809.0        1.0   1.0         569.592089
Citus-1-1-1024-2      809.0        1.0   2.0         569.592089
Citus-1-1-1024-3      809.0        1.0   4.0         569.592089
Citus-1-1-1024-4      809.0        1.0   8.0         569.592089

### Ingestion - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1      4931.9      4.6         29.07                41.75
Citus-1-1-1024-2      4931.9      4.6         29.07                41.75
Citus-1-1-1024-3      4931.9      4.6         29.07                41.75
Citus-1-1-1024-4      4931.9      4.6         29.07                41.75

### Ingestion - Loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1    13003.68     24.0          1.33                 1.33
Citus-1-1-1024-2    13003.68     24.0          1.33                 1.33
Citus-1-1-1024-3    13003.68     24.0          1.33                 1.33
Citus-1-1-1024-4    13003.68     24.0          1.33                 1.33

### Execution - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1   139391.19    26.68         36.09                52.17
Citus-1-1-1024-2   111293.62    22.36         38.68                57.10
Citus-1-1-1024-3    90379.30    14.74         40.69                60.98
Citus-1-1-1024-4    53115.98    10.96         41.68                63.12

### Execution - Benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1     8588.53     2.85          1.64                 1.64
Citus-1-1-1024-2     8566.38     2.37          2.93                 2.93
Citus-1-1-1024-3     6813.78     1.29          5.46                 5.46
Citus-1-1-1024-4     5723.73     0.68          7.09                 7.09

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
```markdown
## Show Summary

### Workload
Benchbase Workload SF=128
    Type: benchbase
    Duration: 12550s 
    Code: 1748870442
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 128. Benchmarking runs for 20 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [4]. Benchmarking has keying and thinking times activated.
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317388476
    volume_size:100.0G
    volume_used:480.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:361486720
        volume_size:100.0G
        volume_used:20.4G
    worker 1
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:224036232
        volume_size:100.0G
        volume_used:13.4G
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:362655184
        volume_size:100.0G
        volume_used:11.5G
    worker 3
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:434860384
        volume_size:100.0G
        volume_used:12.8G
    eval_parameters
                code:1748870442
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-1-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317382036
    volume_size:100.0G
    volume_used:480.0M
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:356977844
        volume_size:100.0G
        volume_used:20.4G
    worker 1
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:224965112
        volume_size:100.0G
        volume_used:13.4G
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364360200
        volume_size:100.0G
        volume_used:11.5G
    worker 3
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435663576
        volume_size:100.0G
        volume_used:12.8G
    eval_parameters
                code:1748870442
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-1-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317382048
    volume_size:100.0G
    volume_used:480.0M
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:358345232
        volume_size:100.0G
        volume_used:20.4G
    worker 1
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:224961756
        volume_size:100.0G
        volume_used:13.4G
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364356364
        volume_size:100.0G
        volume_used:11.5G
    worker 3
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435540052
        volume_size:100.0G
        volume_used:12.8G
    eval_parameters
                code:1748870442
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-1-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317382240
    volume_size:100.0G
    volume_used:480.0M
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:344722988
        volume_size:100.0G
        volume_used:20.5G
    worker 1
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:224965136
        volume_size:100.0G
        volume_used:13.4G
    worker 2
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364360768
        volume_size:100.0G
        volume_used:11.5G
    worker 3
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435528068
        volume_size:100.0G
        volume_used:12.8G
    eval_parameters
                code:1748870442
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317382260
    volume_size:100.0G
    volume_used:464.0M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435541456
        volume_size:100.0G
        volume_used:19.4G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:344738532
        volume_size:100.0G
        volume_used:12.6G
    worker 2
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:224988908
        volume_size:100.0G
        volume_used:10.8G
    worker 3
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364367480
        volume_size:100.0G
        volume_used:11.9G
    eval_parameters
                code:1748870442
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317382456
    volume_size:100.0G
    volume_used:464.0M
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    worker 0
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435541672
        volume_size:100.0G
        volume_used:19.4G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:344740640
        volume_size:100.0G
        volume_used:12.6G
    worker 2
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:224992160
        volume_size:100.0G
        volume_used:10.8G
    worker 3
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364372704
        volume_size:100.0G
        volume_used:11.9G
    eval_parameters
                code:1748870442
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317382468
    volume_size:100.0G
    volume_used:464.0M
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    worker 0
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435529284
        volume_size:100.0G
        volume_used:19.4G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:344730080
        volume_size:100.0G
        volume_used:12.6G
    worker 2
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:224982784
        volume_size:100.0G
        volume_used:10.8G
    worker 3
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364376000
        volume_size:100.0G
        volume_used:11.9G
    eval_parameters
                code:1748870442
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4
Citus-1-1-1024-2-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317382660
    volume_size:100.0G
    volume_used:464.0M
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    worker 0
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435529412
        volume_size:100.0G
        volume_used:19.4G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:344732060
        volume_size:100.0G
        volume_used:12.6G
    worker 2
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:224985936
        volume_size:100.0G
        volume_used:10.8G
    worker 3
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364380020
        volume_size:100.0G
        volume_used:11.9G
    eval_parameters
                code:1748870442
                BEXHOMA_REPLICAS:1
                BEXHOMA_SHARDS:48
                BEXHOMA_WORKERS:4

### Execution
                    experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
Citus-1-1-1024-1-1               1       1280    4096          1  1200.0           0                         60.66                      60.38       99.04                                                     217944.0                                             135049.0
Citus-1-1-1024-1-2               1       1280    4096          2  1200.0           0                         61.00                      60.70       99.56                                                     160434.0                                              52965.5
Citus-1-1-1024-1-3               1       1280    4095          5  1200.0           0                         60.98                      60.69       99.55                                                     137720.0                                              51431.6
Citus-1-1-1024-1-4               1       1280    4090         10  1200.0           0                         60.98                      60.73       99.62                                                     144851.0                                              51534.2
Citus-1-1-1024-2-1               2       1280    4096          1  1200.0           0                         60.94                      60.66       99.50                                                     211963.0                                              65532.0
Citus-1-1-1024-2-2               2       1280    4096          2  1200.0           0                         61.47                      61.19      100.37                                                     141000.0                                              50541.0
Citus-1-1-1024-2-3               2       1280    4095          5  1200.0           0                         61.06                      60.78       99.70                                                     131773.0                                              48938.2
Citus-1-1-1024-2-4               2       1280    4090         10  1200.0           0                         61.14                      60.86       99.83                                                     123939.0                                              54983.3

### Workflow

#### Actual
DBMS Citus-1-1-1024 - Pods [[10, 2, 5, 1], [5, 2, 10, 1]]

#### Planned
DBMS Citus-1-1-1024 - Pods [[1, 2, 5, 10], [1, 2, 5, 10]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
Citus-1-1-1024-1-1      809.0        1.0   1.0         569.592089
Citus-1-1-1024-1-2      809.0        1.0   2.0         569.592089
Citus-1-1-1024-1-3      809.0        1.0   5.0         569.592089
Citus-1-1-1024-1-4      809.0        1.0  10.0         569.592089
Citus-1-1-1024-2-1      809.0        1.0   1.0         569.592089
Citus-1-1-1024-2-2      809.0        1.0   2.0         569.592089
Citus-1-1-1024-2-3      809.0        1.0   5.0         569.592089
Citus-1-1-1024-2-4      809.0        1.0  10.0         569.592089

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1-1     5163.28     1.82         39.53                57.11
Citus-1-1-1024-1-2     8203.95     1.45         40.17                59.40
Citus-1-1-1024-1-3     5934.14     1.57         40.84                60.93
Citus-1-1-1024-1-4     4074.21     1.59         41.34                62.06
Citus-1-1-1024-2-1     3964.31     2.38         37.33                54.67
Citus-1-1-1024-2-2     7189.77     1.87         38.84                57.53
Citus-1-1-1024-2-3     3958.14     2.27         39.49                59.26
Citus-1-1-1024-2-4     4007.93     1.85         40.28                60.71

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-1-1-1024-1-1      299.42     0.21          5.11                 5.11
Citus-1-1-1024-1-2      341.25     0.24          9.03                 9.03
Citus-1-1-1024-1-3      530.53     3.19         10.99                10.99
Citus-1-1-1024-1-4      812.79     2.35         13.35                13.35
Citus-1-1-1024-2-1      313.08     0.79          4.03                 4.03
Citus-1-1-1024-2-2      391.33     1.05          9.10                 9.10
Citus-1-1-1024-2-3      505.76     1.24         13.11                13.11
Citus-1-1-1024-2-4      775.80     3.07         14.32                14.32

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
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1153s 
    Code: 1748883105
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317426456
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:436861832
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:345853416
    worker 2
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:226115648
    eval_parameters
        code:1748883105
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:3

### Execution
                 experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency     NOPM       TPM  duration  errors
Citus-BHT-8-1-1               1      16       1          1      33.8     69.47         0.0  45897.0  105337.0         5       0

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
```markdown
## Show Summary

### Workload
HammerDB Workload SF=128 (warehouses for TPC-C)
    Type: tpcc
    Duration: 9473s 
    Code: 1748884337
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 128. Benchmarking runs for 30 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317382888
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435529288
        volume_size:50.0G
        volume_used:6.1G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:344737420
        volume_size:50.0G
        volume_used:3.2G
    worker 2
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225002952
        volume_size:50.0G
        volume_used:3.2G
    worker 3
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364393464
        volume_size:50.0G
        volume_used:6.1G
    eval_parameters
        code:1748884337
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-128-1-2 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317382908
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435529520
        volume_size:50.0G
        volume_used:14.4G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:344740480
        volume_size:50.0G
        volume_used:9.8G
    worker 2
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225005720
        volume_size:50.0G
        volume_used:9.2G
    worker 3
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364399232
        volume_size:50.0G
        volume_used:9.9G
    eval_parameters
        code:1748884337
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-128-1-3 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317383108
    volume_size:50.0G
    volume_used:84.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435529720
        volume_size:50.0G
        volume_used:27.1G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:344743492
        volume_size:50.0G
        volume_used:17.3G
    worker 2
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225012688
        volume_size:50.0G
        volume_used:14.0G
    worker 3
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364403100
        volume_size:50.0G
        volume_used:14.3G
    eval_parameters
        code:1748884337
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
Citus-BHT-128-1-4 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317383128
    volume_size:50.0G
    volume_used:84.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579409920
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker22
        disk:435530552
        volume_size:50.0G
        volume_used:33.9G
    worker 1
        RAM:1081649897472
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:344749088
        volume_size:50.0G
        volume_used:22.6G
    worker 2
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225033820
        volume_size:50.0G
        volume_used:19.9G
    worker 3
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:364409744
        volume_size:50.0G
        volume_used:19.3G
    eval_parameters
        code:1748884337
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4

### Execution
                   experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency      NOPM       TPM  duration  errors
Citus-BHT-128-1-1               1     128       1          1    173.44    608.33         0.0  91939.00  211453.0        30       0
Citus-BHT-128-1-2               1     128       2          2    173.05    650.18         0.0  82877.00  190530.0        30       0
Citus-BHT-128-1-3               1     128       3          4    173.62    629.57         0.0  81228.25  186899.0        30       0
Citus-BHT-128-1-4               1     128       4          8    179.27    638.08         0.0  80607.50  185477.5        30       0

Warehouses: 128

### Workflow

#### Actual
DBMS Citus-BHT-128-1 - Pods [[4, 8, 2, 1]]

#### Planned
DBMS Citus-BHT-128-1 - Pods [[1, 2, 4, 8]]

### Loading
                   time_load  terminals  pods  Imported warehouses [1/h]
Citus-BHT-128-1-1      476.0        1.0   1.0                 968.067227
Citus-BHT-128-1-2      476.0        1.0   2.0                 968.067227
Citus-BHT-128-1-3      476.0        1.0   4.0                 968.067227
Citus-BHT-128-1-4      476.0        1.0   8.0                 968.067227

### Ingestion - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1     1337.24     1.67          26.9                40.13
Citus-BHT-128-1-2     1337.24     1.67          26.9                40.13
Citus-BHT-128-1-3     1337.24     1.67          26.9                40.13
Citus-BHT-128-1-4     1337.24     1.67          26.9                40.13

### Ingestion - Loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1     4170.86    22.32          0.69                 0.69
Citus-BHT-128-1-2     4170.86    22.32          0.69                 0.69
Citus-BHT-128-1-3     4170.86    22.32          0.69                 0.69
Citus-BHT-128-1-4     4170.86    22.32          0.69                 0.69

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1   202888.94    86.38         38.95                59.22
Citus-BHT-128-1-2   190444.86    85.57         45.27                74.26
Citus-BHT-128-1-3   220809.40    88.65         51.34                86.47
Citus-BHT-128-1-4   249980.03    92.11         56.46                97.15

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-128-1-1     2359.58     1.37          2.21                 2.22
Citus-BHT-128-1-2     2359.58     1.07          2.72                 2.72
Citus-BHT-128-1-3     2154.44     0.82          2.71                 2.71
Citus-BHT-128-1-4     2071.25     0.59          2.41                 2.41

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
```markdown
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
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 827s 
    Code: 1748897692
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-BHT-8-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317425384
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:226574880
    worker 1
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:366622104
    worker 2
        RAM:1081965518848
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1385417836
    worker 3
        RAM:540595884032
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-140-generic
        node:cl-worker23
        disk:539662916
    eval_parameters
        code:1748897692
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 Citus-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             292.29
Minimum Cost Supplier Query (TPC-H Q2)                        247.41
Shipping Priority (TPC-H Q3)                                  250.34
Order Priority Checking Query (TPC-H Q4)                      188.47
Local Supplier Volume (TPC-H Q5)                              256.45
Forecasting Revenue Change (TPC-H Q6)                         151.03
Forecasting Revenue Change (TPC-H Q7)                         244.44
National Market Share (TPC-H Q8)                              261.66
Product Type Profit Measure (TPC-H Q9)                        440.15
Forecasting Revenue Change (TPC-H Q10)                        491.41
Important Stock Identification (TPC-H Q11)                    133.87
Shipping Modes and Order Priority (TPC-H Q12)                 195.31
Customer Distribution (TPC-H Q13)                            2807.08
Forecasting Revenue Change (TPC-H Q14)                        211.06
Top Supplier Query (TPC-H Q15)                                503.47
Parts/Supplier Relationship (TPC-H Q16)                       518.48
Small-Quantity-Order Revenue (TPC-H Q17)                     9139.12
Large Volume Customer (TPC-H Q18)                             362.21
Discounted Revenue (TPC-H Q19)                                237.26
Potential Part Promotion (TPC-H Q20)                         4971.61
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           233.35
Global Sales Opportunity Query (TPC-H Q22)                   2480.23

### Loading [s]
                 timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
Citus-BHT-8-1-1           1.0           28.0         2.0       31.0      70.0

### Geometric Mean of Medians of Timer Run [s]
                 Geo Times [s]
DBMS                          
Citus-BHT-8-1-1           0.47

### Power@Size ((3600*SF)/(geo times))
                 Power@Size [~Q/h]
DBMS                              
Citus-BHT-8-1-1            8124.71

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                            time [s]  count  SF  Throughput@Size
DBMS          SF num_experiment num_client                                      
Citus-BHT-8-1 1  1              1                 30      1   1           2640.0

### Workflow

#### Actual
DBMS Citus-BHT-8 - Pods [[1]]

#### Planned
DBMS Citus-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
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
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
    Type: tpch
    Duration: 3782s 
    Code: 1748898623
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 14400.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317383764
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225058956
        volume_size:50.0G
        volume_used:11.6G
    worker 1
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:365106864
        volume_size:50.0G
        volume_used:11.8G
    worker 2
        RAM:1081965518848
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1383902012
        volume_size:50.0G
        volume_used:11.7G
    worker 3
        RAM:540595884032
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-140-generic
        node:cl-worker23
        disk:538144788
        volume_size:50.0G
        volume_used:11.7G
    eval_parameters
        code:1748898623
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False
Citus-BHT-8-1-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317383768
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225059744
        volume_size:50.0G
        volume_used:11.6G
    worker 1
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:365106932
        volume_size:50.0G
        volume_used:11.8G
    worker 2
        RAM:1081965518848
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1383902444
        volume_size:50.0G
        volume_used:11.7G
    worker 3
        RAM:540595884032
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-140-generic
        node:cl-worker23
        disk:538144788
        volume_size:50.0G
        volume_used:11.7G
    eval_parameters
        code:1748898623
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False
Citus-BHT-8-2-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317383756
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225063988
        volume_size:50.0G
        volume_used:13.8G
    worker 1
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:365205080
        volume_size:50.0G
        volume_used:13.8G
    worker 2
        RAM:1081965518848
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1383912620
        volume_size:50.0G
        volume_used:13.8G
    worker 3
        RAM:540595884032
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-140-generic
        node:cl-worker23
        disk:538144792
        volume_size:50.0G
        volume_used:13.8G
    eval_parameters
        code:1748898623
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False
Citus-BHT-8-2-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317383760
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225070376
        volume_size:50.0G
        volume_used:13.8G
    worker 1
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:365205924
        volume_size:50.0G
        volume_used:13.8G
    worker 2
        RAM:1081965518848
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1383913064
        volume_size:50.0G
        volume_used:13.8G
    worker 3
        RAM:540595884032
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-140-generic
        node:cl-worker23
        disk:538144844
        volume_size:50.0G
        volume_used:13.8G
    eval_parameters
        code:1748898623
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
Pricing Summary Report (TPC-H Q1)                               772.13             760.69            2211.08             770.15
Minimum Cost Supplier Query (TPC-H Q2)                         1686.22            1720.91            3487.26            1727.55
Shipping Priority (TPC-H Q3)                                    878.62             879.44            1961.36             983.70
Order Priority Checking Query (TPC-H Q4)                        446.44             454.47             534.03             542.96
Local Supplier Volume (TPC-H Q5)                               1113.40            1199.73            1131.10            1141.38
Forecasting Revenue Change (TPC-H Q6)                           397.86             360.37             426.90             433.58
Forecasting Revenue Change (TPC-H Q7)                           925.47             927.51            1006.13            1044.76
National Market Share (TPC-H Q8)                                918.49             903.53            1222.85            1066.63
Product Type Profit Measure (TPC-H Q9)                         1917.06            2000.14            3191.85            1913.20
Forecasting Revenue Change (TPC-H Q10)                         3942.10            3915.77            3920.12            3883.22
Important Stock Identification (TPC-H Q11)                      881.32            1167.72            1233.90            1214.08
Shipping Modes and Order Priority (TPC-H Q12)                   577.95             601.75             597.33             617.72
Customer Distribution (TPC-H Q13)                             27598.57           30339.18           28588.22           30600.60
Forecasting Revenue Change (TPC-H Q14)                          789.67             760.94             858.29             856.79
Top Supplier Query (TPC-H Q15)                                 3750.88            4009.43            4008.74            3911.98
Parts/Supplier Relationship (TPC-H Q16)                        2217.93            1728.66            1929.16            1957.22
Small-Quantity-Order Revenue (TPC-H Q17)                      90197.68           88147.77           96600.31           94505.42
Large Volume Customer (TPC-H Q18)                              2422.86            2351.42            2950.68            2983.78
Discounted Revenue (TPC-H Q19)                                  883.04             877.06             981.86            1037.90
Potential Part Promotion (TPC-H Q20)                          91247.95           98070.12           89160.61           93758.77
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)             623.51             605.14             966.54             668.51
Global Sales Opportunity Query (TPC-H Q22)                    23998.09           24250.15           26319.95           27603.84

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
Citus-BHT-8-1-1-1           1.0          336.0         5.0      191.0     540.0
Citus-BHT-8-1-2-1           1.0          336.0         5.0      191.0     540.0
Citus-BHT-8-2-1-1           1.0          336.0         5.0      191.0     540.0
Citus-BHT-8-2-2-1           1.0          336.0         5.0      191.0     540.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
Citus-BHT-8-1-1-1           2.25
Citus-BHT-8-1-2-1           2.29
Citus-BHT-8-2-1-1           2.83
Citus-BHT-8-2-2-1           2.45

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
Citus-BHT-8-1-1-1           16337.55
Citus-BHT-8-1-2-1           16181.53
Citus-BHT-8-2-1-1           13007.05
Citus-BHT-8-2-2-1           15028.90

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
Citus-BHT-8-1-1 10 1              1                265      1  10          2988.68
Citus-BHT-8-1-2 10 1              2                274      1  10          2890.51
Citus-BHT-8-2-1 10 2              1                280      1  10          2828.57
Citus-BHT-8-2-2 10 2              2                280      1  10          2828.57

### Workflow

#### Actual
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1     2000.05     3.48         39.63                71.96
Citus-BHT-8-1-2     2000.05     3.48         39.63                71.96

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1      174.28     0.53          0.04                10.53
Citus-BHT-8-1-2      174.28     0.53          0.04                10.53

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1     1283.84     2.47         44.82                74.52
Citus-BHT-8-1-2     1269.07     3.89         45.94                75.64
Citus-BHT-8-2-1     1348.47     2.86         45.52                99.35
Citus-BHT-8-2-2     1321.92     2.24         46.10               100.70

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1       18.01     0.00          0.29                 0.30
Citus-BHT-8-1-2       18.97     0.00          0.60                 0.61
Citus-BHT-8-2-1       17.36     0.00          0.31                 0.33
Citus-BHT-8-2-2       17.36     0.07          0.60                 0.63

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
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
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
    Type: tpch
    Duration: 4519s 
    Code: 1748902675
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 14400.
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317383980
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225063144
        volume_size:50.0G
        volume_used:9.2G
    worker 1
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:365212836
        volume_size:50.0G
        volume_used:8.9G
    worker 2
        RAM:1081965518848
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1383915080
        volume_size:50.0G
        volume_used:9.2G
    worker 3
        RAM:540595884032
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-140-generic
        node:cl-worker23
        disk:538144848
        volume_size:50.0G
        volume_used:9.2G
    eval_parameters
        code:1748902675
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True
Citus-BHT-8-1-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317383984
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225064644
        volume_size:50.0G
        volume_used:9.2G
    worker 1
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:365571580
        volume_size:50.0G
        volume_used:8.9G
    worker 2
        RAM:1081965518848
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1383915900
        volume_size:50.0G
        volume_used:9.2G
    worker 3
        RAM:540595884032
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-140-generic
        node:cl-worker23
        disk:538144852
        volume_size:50.0G
        volume_used:9.2G
    eval_parameters
        code:1748902675
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True
Citus-BHT-8-2-1-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317383980
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225068544
        volume_size:50.0G
        volume_used:5.7G
    worker 1
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:365275056
        volume_size:50.0G
        volume_used:9.9G
    worker 2
        RAM:1081965518848
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1383917812
        volume_size:50.0G
        volume_used:9.9G
    worker 3
        RAM:540595884032
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-140-generic
        node:cl-worker23
        disk:538144908
        volume_size:50.0G
        volume_used:9.9G
    eval_parameters
        code:1748902675
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True
Citus-BHT-8-2-2-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317383988
    volume_size:50.0G
    volume_used:40.0M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081854078976
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:225078404
        volume_size:50.0G
        volume_used:5.7G
    worker 1
        RAM:541008568320
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-140-generic
        node:cl-worker13
        disk:365276208
        volume_size:50.0G
        volume_used:9.9G
    worker 2
        RAM:1081965518848
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1383918792
        volume_size:50.0G
        volume_used:9.9G
    worker 3
        RAM:540595884032
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-140-generic
        node:cl-worker23
        disk:538144908
        volume_size:50.0G
        volume_used:9.9G
    eval_parameters
        code:1748902675
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
Pricing Summary Report (TPC-H Q1)                              2855.53            2812.06            6166.27            2801.93
Minimum Cost Supplier Query (TPC-H Q2)                         1979.67            1613.43           39226.85            1663.56
Shipping Priority (TPC-H Q3)                                   1457.18            1463.28           13244.54            1468.41
Order Priority Checking Query (TPC-H Q4)                       1017.24             909.43            1030.99             907.58
Local Supplier Volume (TPC-H Q5)                               1590.07            1649.01            2343.29            1575.04
Forecasting Revenue Change (TPC-H Q6)                           900.84             782.24             900.00             823.29
Forecasting Revenue Change (TPC-H Q7)                          1801.83            1736.49            1712.24            1726.13
National Market Share (TPC-H Q8)                               2016.15            2004.03            6297.90            1952.18
Product Type Profit Measure (TPC-H Q9)                       214500.24          214681.00          208638.16          208128.14
Forecasting Revenue Change (TPC-H Q10)                         4106.59            4164.91            4162.21            4273.84
Important Stock Identification (TPC-H Q11)                     1080.25            1221.36             962.92            1317.01
Shipping Modes and Order Priority (TPC-H Q12)                  1382.17            1396.79            1380.60            1395.24
Customer Distribution (TPC-H Q13)                             28936.13           28673.15           29686.14           29343.50
Forecasting Revenue Change (TPC-H Q14)                         1177.08            1195.82            1205.81            1206.44
Top Supplier Query (TPC-H Q15)                                 4126.40            4073.89            4120.36            4111.30
Parts/Supplier Relationship (TPC-H Q16)                        1967.17            1430.60            2062.84            1858.80
Small-Quantity-Order Revenue (TPC-H Q17)                     128720.36          129668.77          129807.11          131959.46
Large Volume Customer (TPC-H Q18)                              2642.24            2651.70            2572.33            2654.44
Discounted Revenue (TPC-H Q19)                                 2038.93            1977.92            2048.13            1970.63
Potential Part Promotion (TPC-H Q20)                          65072.33           80178.53           76002.29           61120.93
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)           92980.74           93094.75           93961.48           93262.55
Global Sales Opportunity Query (TPC-H Q22)                    23700.75           24223.63           24351.63           24346.21

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
Citus-BHT-8-1-1-1           1.0          269.0         6.0       64.0     348.0
Citus-BHT-8-1-2-1           1.0          269.0         6.0       64.0     348.0
Citus-BHT-8-2-1-1           1.0          269.0         6.0       64.0     348.0
Citus-BHT-8-2-2-1           1.0          269.0         6.0       64.0     348.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
Citus-BHT-8-1-1-1           5.03
Citus-BHT-8-1-2-1           4.95
Citus-BHT-8-2-1-1           7.10
Citus-BHT-8-2-2-1           4.96

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
Citus-BHT-8-1-1-1            7336.62
Citus-BHT-8-1-2-1            7484.68
Citus-BHT-8-2-1-1            5194.54
Citus-BHT-8-2-2-1            7442.66

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
Citus-BHT-8-1-1 10 1              1                593      1  10          1335.58
Citus-BHT-8-1-2 10 1              2                609      1  10          1300.49
Citus-BHT-8-2-1 10 2              1                660      1  10          1200.00
Citus-BHT-8-2-2 10 2              2                587      1  10          1349.23

### Workflow

#### Actual
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1     1958.66     6.13         28.77                48.25
Citus-BHT-8-1-2     1958.66     6.13         28.77                48.25

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1      171.37     0.23          0.04                10.53
Citus-BHT-8-1-2      171.37     0.23          0.04                10.53

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1    27431.82    48.00         65.13                85.41
Citus-BHT-8-1-2    27452.60    48.00         66.13                86.42
Citus-BHT-8-2-1    27143.60    47.95         58.66                71.52
Citus-BHT-8-2-2    27071.06    78.78         62.31                78.35

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1       19.90     0.02          0.30                 0.30
Citus-BHT-8-1-2       19.90     0.26          0.54                 0.56
Citus-BHT-8-2-1       18.15     0.01          0.30                 0.32
Citus-BHT-8-2-2       18.15     0.23          0.54                 0.57

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



