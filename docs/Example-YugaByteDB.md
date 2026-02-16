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

This will deploy master and tserver worker.
The master pods manage table metadata and keep track of which nodes store which data.
They handle automatic sharding and tablet distribution and manage Raft-based leader election for tablets (shards).
The number of master pods is 3 or 5 typically.
The tserver worker store the actual data (tablets) and execute SQL queries via the YSQL or YCQL API.
The number of tserver depends on the size of the data and the cluster.

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
tserver.ysql_max_connections=1280,\
replicas.master=3,\
replicas.tserver=3,\
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
```bash
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

```bash
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

doc_ycsb_yugabytedb_1.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 957s 
    Code: 1770048432
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['YugabyteDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96156
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1770048432

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-65536               1       64   65536          8           0                   15398.593486                65177.0             1000000                             43851.0

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1           0                       15454.59               647057.0           4997636                           59807.0             5002364                             62079.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component yb-tserver
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     1891.31    28.05          2.78                 8.13

### Loading phase: component yb-master
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1        5.68     0.07          0.18                 0.22

### Loading phase: component loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1       73.94        0          0.11                 0.11

### Execution phase: component yb-tserver
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1    20703.63     37.1          5.07                16.59

### Execution phase: component yb-master
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1        18.6     0.07          0.19                 0.23

### Execution phase: component benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1      523.74     0.99          0.14                 0.14

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
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

doc_ycsb_yugabytedb_2.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 800s 
    Code: 1770049453
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['YugabyteDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is skipped.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96156
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1770049453

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1           0                       16067.48               622375.0           4998449                           58047.0             5001551                             60351.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Monitoring

### Execution phase: component yb-tserver
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     20761.2    38.53          7.32                17.67

### Execution phase: component yb-master
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1       18.06     0.07           0.2                 0.24

### Execution phase: component benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1      534.16     1.11          0.13                 0.14

### Tests
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
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

```bash
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

doc_ycsb_yugabytedb_3.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 551s 
    Code: 1770894703
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['YugabyteDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 1Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96182
    volume_size:1.0G
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1770894703

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-65536               1       64   65536          8           0                   19418.560362                52860.0             1000000                             15951.0

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1           0                       41062.87               243529.0           5001011                           16991.0             4998989                             40255.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component yb-tserver
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     1081.23    17.49          5.81                13.26

### Loading phase: component yb-master
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1        5.24     0.07          0.21                 0.24

### Loading phase: component loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1       78.42        0          0.11                 0.11

### Execution phase: component yb-tserver
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     9280.15    41.99         10.55                22.08

### Execution phase: component yb-master
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1       11.76     0.09          0.22                 0.24

### Execution phase: component benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1      440.68     2.26          0.14                 0.14

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```

### Persist YugabyteDB

If you want YugabyteDB to have real persistent storage, remove the line `storage.ephemeral=true,\` from the installation.


## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
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
```bash
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
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_1.log &
```

yields

doc_benchbase_yugabytedb_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1079s 
    Code: 1770897417
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['YugabyteDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-1-1-1024-1 uses docker image postgres:15.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96220
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1770897417
YugabyteDB-1-1-1024-2 uses docker image postgres:15.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:96221
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1770897417

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
YugabyteDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    515.249970                 513.026637         0.0                                                      82791.0                                              31044.0
YugabyteDB-1-1-1024-2-1               1          8    8192       2      1  300.0           0                    219.533327                 218.269994         0.0                                                      95978.0                                              36430.0
YugabyteDB-1-1-1024-2-2               1          8    8192       2      2  300.0           0                    209.249920                 208.093254         0.0                                                      99039.0                                              38220.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
YugabyteDB-1-1-1024-1               1         16   16384          1  300.0           0                        515.25                     513.03         0.0                                                      82791.0                                              31044.0
YugabyteDB-1-1-1024-2               1         16   16384          2  300.0           0                        428.78                     426.36         0.0                                                      99039.0                                              37325.0

### Workflow

#### Actual
DBMS YugabyteDB-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
YugabyteDB-1-1-1024-1      153.0        1.0   1.0         376.470588
YugabyteDB-1-1-1024-2      153.0        1.0   2.0         376.470588

### Monitoring

### Loading phase: component yb-tserver
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1     2053.55    17.26          7.83                14.98
YugabyteDB-1-1-1024-2     4010.39    33.72          8.41                16.52

### Loading phase: component yb-master
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1       78.01     0.06          0.24                 0.27
YugabyteDB-1-1-1024-2       78.01     0.06          0.24                 0.27

### Loading phase: component loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1     1120.44    10.78          0.25                 0.25
YugabyteDB-1-1-1024-2     1120.44    10.78          0.25                 0.25

### Execution phase: component yb-tserver
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1    10080.50    37.20         10.18                20.66
YugabyteDB-1-1-1024-2     9269.65    34.37         11.15                23.74

### Execution phase: component yb-master
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1       11.73     0.06          0.23                 0.26
YugabyteDB-1-1-1024-2       15.96     0.08          0.25                 0.28

### Execution phase: component benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1      237.16     0.82          0.29                 0.29
YugabyteDB-1-1-1024-2      237.16     1.54          0.29                 0.29

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

### Benchbase Example Explained

The setup is the same as for YCSB (see above).

However the connection string this time is not read from `cluster.config`, but instead constructed from parameters that are set explicitly in the workflow file `benchbase.py`:

```bash
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
  -slg 30 \
  -sd 20 \
  -xkey \
  -dbms YugabyteDB \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_2.log &
```

yields

doc_benchbase_yugabytedb_2.log
```markdown

```

