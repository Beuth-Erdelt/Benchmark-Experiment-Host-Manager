# Example: Benchmark YugabyteDB

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that is not managed by bexhoma, but exists in the Kubernetes cluster in the same namespace**.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Important implications of this:
* Bexhoma does neither start nor stop the DBMS.
* There can only be one DBMS in the cluster at the same time.
* Bexhoma does not know what resides inside of the database.
* Bexhoma still can monitor all components of the experiment, including the DBMS itself.

In order to be fully functional, bexhoma installs an instance of PostgreSQL, that does nothing (a container with psql would be enough).
Bexhoma writes infos about the status of the experiment to this "SUT" pod to mimick it has access to the DBMS.
Moreover the container is used to install a schema to YugabyteDB via psql.

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the YugabyteDB cluster.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. YugabyteDB YCSB: https://docs.yugabyte.com/preview/benchmark/ycsb-jdbc/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. Benchbase Repository: https://github.com/cmu-db/benchbase/wiki/TPC-C
1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Install YugabyteDB

Get the helm chart and follow the instructions: https://docs.yugabyte.com/stable/deploy/kubernetes/single-zone/oss/helm-chart/


```bash
helm install bexhoma yugabytedb/yugabyte \
--version 2.23.0 \
--set \
gflags.tserver.ysql_enable_packed_row=true,\
resource.master.limits.cpu=2,\
resource.master.limits.memory=8Gi,\
resource.master.requests.cpu=2,\
resource.master.requests.memory=8Gi,\
resource.tserver.limits.cpu=8,\
resource.tserver.limits.memory=8Gi,\
resource.tserver.requests.cpu=8,\
resource.tserver.requests.memory=8Gi,\
storage.master.size=100Gi,\
storage.tserver.size=100Gi,\
storage.ephemeral=true,\
tserver.tolerations[0].effect=NoSchedule,\
tserver.tolerations[0].key=nvidia.com/gpu,\
enableLoadBalancer=True
```


Test the installation
```bash
helm status bexhoma
```


After the experiment: Remove the installation
```bash
helm delete bexhoma
kubectl delete pvc -l app=yb-tserver
kubectl delete pvc -l app=yb-master
```

Optionally: Connect to the installation
* to DBMS: `kubectl port-forward service/yb-tserver-service 5433:5433`
* to GUI: `kubectl port-forward service/yb-master-ui 8080:7000`


Optionally: Use [YugabyteDB connection manager](https://docs.yugabyte.com/preview/explore/going-beyond-sql/connection-mgr-ysql/) by adding
```
gflags.tserver.enable_ysql_conn_mgr=true,\
gflags.tserver.allowed_preview_flags_csv=enable_ysql_conn_mgr,\
```

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
  --workload a \
  -dbms YugabyteDB \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_1.log &
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of a dummy container as a placeholder for YugabyteDB (`-dbms`)
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
+-----------------------+--------------+--------------+------------+---------------+
| 1730133803            | sut          |   loaded [s] | use case   | benchmarker   |
+=======================+==============+==============+============+===============+
| YugabyteDB-64-8-65536 | (1. Running) |           41 | ycsb       | (1. Running)  |
+-----------------------+--------------+--------------+------------+---------------+
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
    Duration: 562s 
    Code: 1734625544
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 10000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are [4]. Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['YugabyteDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249253840
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081966526464
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker28
        disk:439206828
    worker 1
        RAM:540587499520
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-126-generic
        node:cl-worker22
        disk:122936080
    worker 2
        RAM:1081965555712
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker27
        disk:584264864

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-65536               1       64   65536          8                   28456.559524                35509.0             1000000                             15762.0

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1                       31861.75               313856.0           4998066                           37663.0             5001934                             43039.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1      925.63     4.64          1.75                 5.32

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1        0.09        0          0.01                 0.01

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     13499.7    15.99          4.92                16.26

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1      932.99      3.2          0.61                 0.61

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


## Perform YCSB Benchmark - Execution only

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
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
  -sl \
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_2.log &
```

This skips loading (`-sl`), as data is already present in the database.

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 511s 
    Code: 1734598346
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 10000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are [4]. Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['YugabyteDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is skipped.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:248621276
    datadisk:39268
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081966526464
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker28
        disk:444140892
    worker 1
        RAM:540587499520
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-126-generic
        node:cl-worker22
        disk:125097616
    worker 2
        RAM:1081965555712
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker27
        disk:561947884

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1                       30985.17               322735.0           4997322                           39711.0             5002678                             44959.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1    14114.83    15.67          7.24                23.99

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1       962.1     3.24          0.61                 0.61

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the YugabyteDB cluster.

The `-mc` option is mandatory here: The sidecar container approach is not working (since bexhoma does not manage the deployment), so either you have Prometheus / Node exporter already installed in your cluster or a daemonset is needed.
For further explanation see the monitoring section of this documentation.


## Use Persistent Storage

### Bexhoma Status Volume

Persistent Storage is not managed by bexhoma, but by YugabyteDB.
We can add the request for a PVC to the experiment setup.
Make sure to reset the database before this test as it should not contain data from previous test runs.
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
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
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_3.log &
```
This will add a PVC to the Dummy DBMS.
Nothing will be stored there, but it maintains status information about previous loading processes.

```
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                 | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+=========================================+=================+==============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-yugabytedb-ycsb-1       | yugabytedb      | ycsb-1       | True         |               300 | YugabyteDB | shared               | 1Gi       | Bound    | 1.0G   | 36M    |
+-----------------------------------------+-----------------+--------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

The above means there has been a YCSB loading process (managed by bexhoma) of size SF=1, that has been completed.
All following calls of such an experiment will skip loading, since the PVC tells it has been finished.
This thus helps to spare the `-sl` parameter.

However bexhoma cannot verify such information.
If YugabyteDB is restarted or data is delete somehow, this PVC information will be outdated and wrong.

This approach helps bexhoma to persist status information, but it does not persist data inside YugabyteDB.

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 562s 
    Code: 1734599008
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 10000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are [4]. Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['YugabyteDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 1Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:248582020
    datadisk:39262
    volume_size:1.0G
    volume_used:36M
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081966526464
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker28
        disk:441849660
    worker 1
        RAM:1081965555712
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker27
        disk:559737852
    worker 2
        RAM:540587499520
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-126-generic
        node:cl-worker22
        disk:122889020

### Loading
                       experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-65536               1       64   65536          8                   29685.991562                34115.0             1000000                             11968.0

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1                       31292.83               319562.0           4998841                           26335.0             5001159                             40159.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1    25686.07     1.15          6.32                20.86

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1       36.85        0          2.05                 2.06

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1    14651.28    15.71          5.01                16.47

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     1009.99     3.37          0.61                 0.61

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

### Persist YugabyteDB

If you want YugabyteDB to have real persistent storage, remove the line `storage.ephemeral=true,\` from the installation.


## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```
'YugabyteDB': {
    'loadData': 'psql -U yugabyte --host yb-tserver-service.{namespace}.svc.cluster.local --port 5433 < {scriptname}',
    'template': {
        'version': '2.17.1',
        'alias': 'Cloud-Native-1',
        'docker_alias': 'CN1',
         'JDBC': {
            'driver': "com.yugabyte.Driver",
            'auth': ["yugabyte", ""],
            'url': 'jdbc:yugabytedb://yb-tserver-service.{namespace}.svc.cluster.local:5433/yugabyte?load-balance=true',
            'jar': 'jdbc-yugabytedb-42.3.5-yb-2.jar'
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


### Preparation of YCSB

In the Docker files for YCSB
* https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ycsb/generator/Dockerfile
* https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ycsb/benchmarker/Dockerfile

there is a section about including the needed JDBC driver:
```
######### Specific version of YugabyteDB JDBC #########
RUN wget https://github.com/yugabyte/pgjdbc/releases/download/v42.3.5-yb-2/jdbc-yugabytedb-42.3.5-yb-2.jar
RUN cp jdbc-yugabytedb-42.3.5-yb-2.jar jars/jdbc-yugabytedb-42.3.5-yb-2.jar
```


### Dummy SUT

Bexhoma deploys a pod to carry status informations.
Here it is an instance of PostgreSQL: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-YugabyteDB.yml


### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/YugabyteDB


### Workflow of YCSB

In `ycsb.py` there is a section about YugabyteDB.

Watch for
* `config.sut_service_name`: Fixed name for the service of the SUT (="yb-tserver-service")
* `config.sut_container_name`: Fixed name for the container of the SUT (="")
* `config.get_worker_pods()`: Method to find the pods of worker nodes (['yb-tserver-0', 'yb-tserver-1', 'yb-tserver-2']). This allows getting host infos like CPU, RAM, node name, ...
* `config.create_monitoring()`: Method to create names for monitored components (for SUT = "yb-tserver-"). This avoids the SUT dummy contributing to the monitoring.
* `config.get_worker_endpoints()`: This is neccessary, when we have sidecar containers attached to workers of a distributed dbms. Monitoring needs to find these containers.
* `config.set_metric_of_config()`: Method to create promql queries from templates (pod like "yb-tserver", no container name, for our SUT)









## Benchbase's TPC-C

TPC-C is performed at 16 warehouses. The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms YugabyteDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_1.log &
```

yields

```bash
## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 1034s 
    Code: 1734601765
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Benchmark is limited to DBMS ['YugabyteDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-1-1-1024-1 uses docker image postgres:15.0
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:248621648
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081966526464
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker28
        disk:443073852
    worker 1
        RAM:540587499520
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-126-generic
        node:cl-worker22
        disk:124173692
    worker 2
        RAM:1081965555712
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker27
        disk:560979688
YugabyteDB-1-1-1024-2 uses docker image postgres:15.0
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:248621648
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081966526464
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker28
        disk:443885248
    worker 1
        RAM:540587499520
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-126-generic
        node:cl-worker22
        disk:124976104
    worker 2
        RAM:1081965555712
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker27
        disk:561773616

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
YugabyteDB-1-1-1024-1               1         16   16384          1  300.0                        364.30                                                     107743.0                                              43901.0
YugabyteDB-1-1-1024-2               1         16   16384          2  300.0                        381.44                                                     105259.0                                              41945.5

Warehouses: 16

### Workflow

#### Actual
DBMS YugabyteDB-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
YugabyteDB-1-1-1024-1      204.0        1.0   1.0                 282.352941
YugabyteDB-1-1-1024-2      204.0        1.0   2.0                 282.352941

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### Benchbase Example Explained

The setup is the same as for YCSB (see above).

However the connection string this time is not read from `cluster.config`, but instead constructed from parameters that are set explicitly in the workflow file `benchbase.py`:

```
BENCHBASE_PROFILE = 'postgres',
BEXHOMA_DATABASE = 'yugabyte',
BEXHOMA_USER = "yugabyte",
BEXHOMA_PASSWORD = "",
BEXHOMA_PORT = 5433,
```

### More Complex Example 

We now run Benchbase's TPC-C variant with more data, for a longer period of time and with a varying number of pods for execution.
Make sure to reset the database before this test as it should not contain data from previous test runs.


```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 60 \
  -dbms YugabyteDB \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_2.log &
```

yields

```bash
```

