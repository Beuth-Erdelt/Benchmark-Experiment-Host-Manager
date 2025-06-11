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

```bash
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

doc_ycsb_cockroachdb_1.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1240s 
    Code: 1748438236
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
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301220952
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081854078976
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:223383180
        datadisk:266360
        volume_size:1000G
        volume_used:258G
    worker 1
        RAM:1081649897472
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:323720816
        datadisk:266414
        volume_size:1000G
        volume_used:258G
    worker 2
        RAM:1081965461504
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1441681096
        datadisk:266439
        volume_size:1000G
        volume_used:258G
    worker 3
        node:cl-worker13
    eval_parameters
        code:1748438236
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                   14750.277198                68275.0             1000000                             11415.0

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1               1       64   65536          1           0                       11573.15               864069.0           5002321                            6479.0             4997679                            163967.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1     1213.67     5.65          3.33                 6.31

### Ingestion - Loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      129.18     0.99          4.45                 4.47

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1    23596.05    19.59         10.88                23.89

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      1240.9     1.57           0.6                 0.61

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
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the CockroachDB cluster.


## Use Persistent Storage


The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 1 \
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


```bash
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

doc_ycsb_cockroachdb_2.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 74989s 
    Code: 1747843568
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
    disk:256981884
    volume_size:50G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081854078976
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:152104060
        datadisk:266088
        volume_size:50G
        volume_used:2.2G
    worker 1
        RAM:540595920896
        Cores:96
        host:5.15.0-139-generic
        node:cl-worker23
        disk:544508332
        datadisk:264708
        volume_size:50G
        volume_used:832M
    worker 2
        RAM:1081965461504
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1391894684
        datadisk:264807
        volume_size:50G
        volume_used:928M
    eval_parameters
        code:1747843568
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3
CockroachDB-64-8-65536-2-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256983084
    volume_size:50G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    worker 0
        RAM:1081854078976
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:152200472
        datadisk:268965
        volume_size:50G
        volume_used:5.0G
    worker 1
        RAM:1081742848000
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker29
        disk:550971288
        datadisk:264518
        volume_size:50G
        volume_used:640M
    worker 2
        RAM:1081965461504
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1391930664
        datadisk:264581
        volume_size:50G
        volume_used:688M
    worker 3
        node:cl-worker2
    eval_parameters
        code:1747843568
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                     172.155279              5809147.0             1000000                           5010943.0

### Execution
                            experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)  [READ-FAILED].Operations  [READ-FAILED].99thPercentileLatency(us)
CockroachDB-64-8-65536-1-1               1       64   65536          1           0                         375.33             26642894.0           4998111                          115711.0             5001889                           6836223.0                         0                                      0.0
CockroachDB-64-8-65536-2-1               2       64   65536          1           0                         238.57             41916628.0           5000546                          212735.0             4999453                           8888319.0                         1                               72155135.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1], [1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1], [1]]

### Ingestion - SUT
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1     4706.22     1.11          4.59                 8.51

### Ingestion - Loader
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1      299.49     0.04          4.58                  4.6

### Execution - SUT
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1    47582.59     2.36         10.97                18.37
CockroachDB-64-8-65536-2-1    63450.15     2.13         13.18                22.10

### Execution - Benchmarker
                            CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1-1     1455.27     0.11          0.61                 0.61
CockroachDB-64-8-65536-2-1     1465.15     0.11          0.61                 0.61

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST failed: Result contains FAILED column
```

## YCSB Example Explained



### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
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

doc_benchbase_cockroachdb_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1235s 
    Code: 1747918651
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.5.
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
    disk:256997096
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081854078976
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:157304120
        datadisk:266371
        volume_size:1000G
        volume_used:258G
    worker 1
        RAM:1081742848000
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker29
        disk:553338216
        datadisk:266165
        volume_size:1000G
        volume_used:258G
    worker 2
        RAM:1081965461504
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1394672648
        datadisk:266167
        volume_size:1000G
        volume_used:258G
    eval_parameters
                code:1747918651
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256997096
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1081854078976
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:157557524
        datadisk:266617
        volume_size:1000G
        volume_used:258G
    worker 1
        RAM:1081742848000
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker29
        disk:553586500
        datadisk:266407
        volume_size:1000G
        volume_used:258G
    worker 2
        RAM:1081965461504
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1394921844
        datadisk:266408
        volume_size:1000G
        volume_used:258G
    eval_parameters
                code:1747918651
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         16   16384          1  300.0           0                        382.89                     381.20         0.0                                                     110298.0                                              41768.0
CockroachDB-1-1-1024-2               1         16   16384          2  300.0           0                        342.73                     341.15         0.0                                                     121782.0                                              46664.0

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1      276.0        1.0   1.0         208.695652
CockroachDB-1-1-1024-2      276.0        1.0   2.0         208.695652

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

doc_benchbase_cockroachdb_2.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=128
    Type: benchbase
    Duration: 16137s 
    Code: 1747919911
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 128. Benchmarking runs for 60 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.5.
    Benchmark is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256997096
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081854078976
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:164842396
        datadisk:273711
        volume_size:1000G
        volume_used:258G
    worker 1
        RAM:1081965461504
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1402197580
        datadisk:273504
        volume_size:1000G
        volume_used:258G
    worker 2
        RAM:1077382844416
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1423525672
        datadisk:273511
        volume_size:1000G
        volume_used:258G
    eval_parameters
                code:1747919911
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256997268
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1081854078976
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:171351032
        datadisk:280057
        volume_size:1000G
        volume_used:258G
    worker 1
        RAM:1081965461504
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1408675364
        datadisk:279817
        volume_size:1000G
        volume_used:258G
    worker 2
        RAM:1077382844416
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1429941212
        datadisk:279765
        volume_size:1000G
        volume_used:258G
    eval_parameters
                code:1747919911
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-3 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256997440
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:1081854078976
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:175208220
        datadisk:283808
        volume_size:1000G
        volume_used:258G
    worker 1
        RAM:1081965461504
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1412523480
        datadisk:283572
        volume_size:1000G
        volume_used:258G
    worker 2
        RAM:1077382844416
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1433860968
        datadisk:283594
        volume_size:1000G
        volume_used:258G
    eval_parameters
                code:1747919911
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-4 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008592896
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256997788
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:1081854078976
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker37
        disk:178341212
        datadisk:286867
        volume_size:1000G
        volume_used:258G
    worker 1
        RAM:1081965461504
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:1415682144
        datadisk:286657
        volume_size:1000G
        volume_used:258G
    worker 2
        RAM:1077382844416
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1437057980
        datadisk:286710
        volume_size:1000G
        volume_used:258G
    eval_parameters
                code:1747919911
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution
                        experiment_run  terminals  target  pod_count    time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         64   16384          1  3600.0           0                       1217.07                    1211.56         0.0                                                     141878.0                                             52578.00
CockroachDB-1-1-1024-2               1         64   16384          2  3600.0           0                       1103.96                    1099.04         0.0                                                     159135.0                                             57966.50
CockroachDB-1-1-1024-3               1         64   16384          4  3600.0           0                        987.17                     982.45         0.0                                                     169318.0                                             64827.00
CockroachDB-1-1-1024-4               1         64   16384          8  3600.0           0                        660.25                     654.14         0.0                                                     237516.0                                             96951.12

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[8, 1, 2, 4]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1     1199.0        1.0   1.0         384.320267
CockroachDB-1-1-1024-2     1199.0        1.0   2.0         384.320267
CockroachDB-1-1-1024-3     1199.0        1.0   4.0         384.320267
CockroachDB-1-1-1024-4     1199.0        1.0   8.0         384.320267

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


### Benchbase Example Explained

The setup is the same as for YCSB (see above).

