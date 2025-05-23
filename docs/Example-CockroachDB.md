# Example: Benchmark CockroachDB

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

CockroachDB offers several installation methods [1].
We here rely on *CockroachDB insecure test cluster in a single Kubernetes cluster* [2].
The benefit of this approach is we can use a [manifest](https://github.com/cockroachdb/cockroach/blob/master/cloud/kubernetes/cockroachdb-statefulset.yaml) for a stateful set provided by CockroachDB.
See [dummy manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-CockroachDB.yml) for a version that is suitable for bexhoma.
CockroachDB cluster does not require a coordinator.
Bexhoma still deploys a main pod (called master) as a substitute for a single point of contact and to annotate status of experiments.
Bexhoma also deploys a service for communication external to CockroachDB (from within the cluster) and a headless service for communication between the pods of the Redis cluster.

This can be managed by bexhoma.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Install CockroachDB:  https://www.cockroachlabs.com/docs/v24.2/install-cockroachdb-linux.html
1. Deploy CockroachDB in a Single Kubernetes Cluster (Insecure): https://www.cockroachlabs.com/docs/v24.2/deploy-cockroachdb-with-kubernetes-insecure
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
  -nwr 3 \
  --workload a \
  -dbms CockroachDB \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_1.log &
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of CockroachDB (`-dbms`) with 3 workers (`-nw`)
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
+----------------------+--------------+--------------+----------------+-------------------------------+-------------+
| 1734624013           | sut          |   loaded [s] | use case       | worker                        | loading     |
+======================+==============+==============+================+===============================+=============+
| CockroachDB-1-1-1024 | (1. Running) |            2 | benchbase_tpcc | (Running) (Running) (Running) | (1 Running) |
+----------------------+--------------+--------------+----------------+-------------------------------+-------------+
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
    Duration: 1571s 
    Code: 1744894145
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
    Benchmark is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-64-8-65536-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202352972
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173475840
        Cores:224
        host:6.8.0-57-generic
        node:cl-worker36
        disk:379856116
        datadisk:228237
        volume_size:1000G
        volume_used:221G
    worker 1
        RAM:1077382836224
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1053560448
        datadisk:227879
        volume_size:1000G
        volume_used:221G
    worker 2
        RAM:1081965461504
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1353017828
        datadisk:228115
        volume_size:1000G
        volume_used:221G
    worker 3
        node:cl-worker4
    eval_parameters
        code:1744894145
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                   15663.045837                65176.0             1000000                              7783.0

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1               1       64   65536          1           0                        8450.75              1183327.0           4999801                            8599.0             5000199                            260351.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1     1110.86     6.41          3.57                 7.32

### Ingestion - Loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      137.12        0          4.44                 4.46

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1    24082.93    15.78         10.23                 23.9

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1     1275.08     1.78          0.61                 0.61

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
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the CockroachDB cluster.


## Use Persistent Storage


The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 3 \
  --workload a \
  -dbms CockroachDB \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_2.log &
```
The following status shows we have one volume of type `shared`.
Every Citus experiment will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of CockroachDB mounts the volume and generates the data.
All other instances just use the database without generating and loading data.
Bexhoma uses two types of volumes.
The first volume is attached to the (dummy) coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.


```
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-cockroachdb-ycsb-1     | cockroachdb     | ycsb-1       | True         |              1589 | CockroachDB     | shared               | 50Gi      | Bound    | 50G    | 0      |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+

+-----------------------------------------+------------------------+--------------+-------------+----------------------+-----------+----------+--------+--------+
| Volumes of Workers                      | configuration          |   experiment | dbms        | storage_class_name   | storage   | status   | size   | used   |
+=========================================+========================+==============+=============+======================+===========+==========+========+========+
| bxw-bexhoma-worker-cockroachdb-ycsb-1-0 | CockroachDB-64-8-65536 |   1742540515 | CockroachDB | shared               | 50Gi      | Bound    | 50G    | 4.8G   |
+-----------------------------------------+------------------------+--------------+-------------+----------------------+-----------+----------+--------+--------+
| bxw-bexhoma-worker-cockroachdb-ycsb-1-1 | CockroachDB-64-8-65536 |   1742540515 | CockroachDB | shared               | 50Gi      | Bound    | 50G    | 4.7G   |
+-----------------------------------------+------------------------+--------------+-------------+----------------------+-----------+----------+--------+--------+
| bxw-bexhoma-worker-cockroachdb-ycsb-1-2 | CockroachDB-64-8-65536 |   1742540515 | CockroachDB | shared               | 50Gi      | Bound    | 50G    | 4.8G   |
+-----------------------------------------+------------------------+--------------+-------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like


```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 29880s 
    Code: 1742540515
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
    Benchmark is limited to DBMS ['CockroachDB'].
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
CockroachDB-64-8-65536-1-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:150617372
    volume_size:50G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081965510656
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:623044044
        datadisk:216761
        volume_size:50G
        volume_used:1.9G
    worker 1
        RAM:1081751007232
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker29
        disk:200940376
        datadisk:216700
        volume_size:50G
        volume_used:1.8G
    worker 2
        RAM:1081966518272
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:535939132
        datadisk:216701
        volume_size:50G
        volume_used:1.8G
    eval_parameters
        code:1742540515
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3
CockroachDB-64-8-65536-2-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:150618212
    volume_size:50G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:1081966518272
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:556433168
        datadisk:219693
        volume_size:50G
        volume_used:4.8G
    worker 1
        RAM:1081751007232
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker29
        disk:200941008
        datadisk:219682
        volume_size:50G
        volume_used:4.7G
    worker 2
        RAM:1081965510656
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:725014044
        datadisk:219702
        volume_size:50G
        volume_used:4.8G
    worker 3
        node:cl-worker12
    eval_parameters
        code:1742540515
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                     632.916222              1581488.0             1000000                            648831.0

### Execution
                            experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1-1               1       64   65536          1           0                         665.77             15020105.0           5001201                          178431.0             4998799                           3799039.0
CockroachDB-64-8-65536-2-1               2       64   65536          1           0                         811.99             12315418.0           5000886                          154239.0             4999114                           2883583.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1], [1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1], [1]]

### Ingestion - SUT
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1     2291.65     0.98          5.68                10.68

### Ingestion - Loader
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1      250.61     0.16          0.57                 0.58

### Execution - SUT
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1    32993.85     1.52         10.93                23.30
CockroachDB-64-8-65536-2-1    29951.43     1.67         13.99                29.68

### Execution - Benchmarker
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1     1377.39     0.22          0.61                 0.61
CockroachDB-64-8-65536-2-1     1380.38     0.15          0.61                 0.61

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
'CockroachDB': {
    'loadData': 'cockroach sql --host {service_name} --port 9091 --insecure --file {scriptname}',
    'delay_prepare': 120,
    'template': {
        'version': 'v24.2.4',
        'alias': 'Cloud-Native-2',
        'docker_alias': 'CN2',
         'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["root", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/defaultdb?reWriteBatchedInserts=true',
            'jar': 'postgresql-42.5.0.jar'
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/cockroach/cockroach-data',
    'priceperhourdollar': 0.0,
},
```

where
* `loadData`: This command is used to create the schema
* `JDBC`: These infos are used to configure YCSB


CockroachDB uses the PostgreSQL JDBC driver.



### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/CockroachDB









## Benchbase's TPC-C

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
CockroachDB has 3 workers.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -dbms CockroachDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_1.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 1326s 
    Code: 1742509695
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Benchmark is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081965510656
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:592949108
        datadisk:217366
        volume_size:1000G
        volume_used:210G
    worker 1
        RAM:1081751007232
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker29
        disk:203296244
        datadisk:217159
        volume_size:1000G
        volume_used:210G
    worker 2
        RAM:1081966518272
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:538377272
        datadisk:217230
        volume_size:1000G
        volume_used:210G
    eval_parameters
                code:1742509695
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:150615432
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1081965510656
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:601355976
        datadisk:217658
        volume_size:1000G
        volume_used:210G
    worker 1
        RAM:1081751007232
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker29
        disk:203588460
        datadisk:217444
        volume_size:1000G
        volume_used:210G
    worker 2
        RAM:1081966518272
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:538665536
        datadisk:217510
        volume_size:1000G
        volume_used:210G
    eval_parameters
                code:1742509695

### Execution
                        experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         16   16384          1  300.0                        472.82                                                      81818.0                                              33825.0
CockroachDB-1-1-1024-2               1         16   16384          2  300.0                        398.20                                                     103928.0                                              40165.0

Warehouses: 16

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
CockroachDB-1-1-1024-1      177.0        1.0   1.0                 325.423729
CockroachDB-1-1-1024-2      177.0        1.0   2.0                 325.423729

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### Benchbase More Complex

TPC-C is performed at 128 warehouses.
The 1280 threads of the client are split into a cascading sequence of 1,2,5 and 10 pods.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 20 \
  -nw 4 \
  -nwr 1 \
  -xkey \
  -dbms CockroachDB \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_2.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
Benchbase Workload SF=128 (warehouses for TPC-C)
    Type: benchbase
    Duration: 6940s 
    Code: 1744394934
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 128. Benchmarking runs for 20 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking has keying and thinking times activated.
    Benchmark is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [1280] threads, split into [1, 2, 5, 10] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201988344
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081966514176
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:966607168
        datadisk:233351
        volume_size:1000G
        volume_used:221G
    worker 1
        RAM:1081751007232
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker29
        disk:372159320
        datadisk:233181
        volume_size:1000G
        volume_used:221G
    worker 2
        RAM:1081965506560
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1274119432
        datadisk:233646
        volume_size:1000G
        volume_used:221G
    worker 3
        RAM:540595875840
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:299429352
        datadisk:232341
        volume_size:1000G
        volume_used:221G
    eval_parameters
                code:1744394934
                BEXHOMA_REPLICAS:1
                BEXHOMA_WORKERS:4
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201988344
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1081966514176
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:966739224
        datadisk:233478
        volume_size:1000G
        volume_used:221G
    worker 1
        RAM:1081751007232
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker29
        disk:372325488
        datadisk:233343
        volume_size:1000G
        volume_used:221G
    worker 2
        RAM:1081965506560
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1274180396
        datadisk:233704
        volume_size:1000G
        volume_used:221G
    worker 3
        RAM:540595875840
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:299628108
        datadisk:232535
        volume_size:1000G
        volume_used:221G
    eval_parameters
                code:1744394934
                BEXHOMA_REPLICAS:1
                BEXHOMA_WORKERS:4
CockroachDB-1-1-1024-3 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201988516
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:1081966514176
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:966878164
        datadisk:233613
        volume_size:1000G
        volume_used:221G
    worker 1
        RAM:1081751007232
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker29
        disk:372461324
        datadisk:233476
        volume_size:1000G
        volume_used:221G
    worker 2
        RAM:1081965506560
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1274293636
        datadisk:233814
        volume_size:1000G
        volume_used:221G
    worker 3
        RAM:540595875840
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:299731120
        datadisk:232635
        volume_size:1000G
        volume_used:221G
    eval_parameters
                code:1744394934
                BEXHOMA_REPLICAS:1
                BEXHOMA_WORKERS:4
CockroachDB-1-1-1024-4 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:201988516
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:1081966514176
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:967013976
        datadisk:233744
        volume_size:1000G
        volume_used:221G
    worker 1
        RAM:1081751007232
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker29
        disk:372601084
        datadisk:233612
        volume_size:1000G
        volume_used:221G
    worker 2
        RAM:1081965506560
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1274428820
        datadisk:233945
        volume_size:1000G
        volume_used:221G
    worker 3
        RAM:540595875840
        Cores:96
        host:5.15.0-136-generic
        node:cl-worker23
        disk:299840092
        datadisk:232741
        volume_size:1000G
        volume_used:221G
    eval_parameters
                code:1744394934
                BEXHOMA_REPLICAS:1
                BEXHOMA_WORKERS:4

### Execution
                        experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1       1280   16384          1  1200.0           0                         61.35                      61.08      100.18                                                      94311.0                                              38281.0
CockroachDB-1-1-1024-2               1       1280   16384          2  1200.0           0                         61.09                      60.82       99.75                                                      94083.0                                              36669.0
CockroachDB-1-1-1024-3               1       1280   16380          5  1200.0           0                         61.21                      60.91       99.92                                                      95072.0                                              36116.0
CockroachDB-1-1-1024-4               1       1280   16380         10  1200.0           0                         61.17                      60.89       99.88                                                     104708.0                                              37183.9

Warehouses: 128

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 5, 10]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 5, 10]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
CockroachDB-1-1-1024-1      835.0        1.0   1.0                 551.856287
CockroachDB-1-1-1024-2      835.0        1.0   2.0                 551.856287
CockroachDB-1-1-1024-3      835.0        1.0   5.0                 551.856287
CockroachDB-1-1-1024-4      835.0        1.0  10.0                 551.856287

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### Benchbase Example Explained

The setup is the same as for YCSB (see above).

