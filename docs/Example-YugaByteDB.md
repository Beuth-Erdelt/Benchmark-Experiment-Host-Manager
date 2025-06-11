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
    Duration: 1622s 
    Code: 1747941852
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
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:257038492
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1747941852

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-65536               1       64   65536          8           0                    8661.212432               116122.0             1000000                             52015.0

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1           0                        8013.67              1247867.0           4999782                           64991.0             5000218                             67903.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     2691.54    18.93           2.9                 8.24

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1      186.93     0.37          4.51                 4.54

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1    31465.52    23.37          4.86                 15.6

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     1124.23     1.42          0.61                 0.61

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
    Duration: 1419s 
    Code: 1747943533
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
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:257038500
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1747943533

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1           0                         8096.1              1235162.0           5000336                           57503.0             4999664                             61023.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1    33657.92    24.27          7.08                15.46

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     1167.45     1.35          0.61                 0.61

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
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
    Duration: 1598s 
    Code: 1747945245
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
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:256999240
    volume_size:1.0G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1747945245

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-65536               1       64   65536          8           0                    8505.880838               118120.0             1000000                             48683.0

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1           0                        8163.15              1225018.0           5000874                           61535.0             4999126                             64511.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     3544.26     7.99          2.61                 7.87

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1       145.2     0.61          4.46                 4.48

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1    34408.75    16.01          4.64                15.04

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     1134.83     1.36          0.61                 0.61

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
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1266s 
    Code: 1748462231
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301261896
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748462231
YugabyteDB-1-1-1024-2 uses docker image postgres:15.0
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301261900
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1748462231

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
YugabyteDB-1-1-1024-1               1         16   16384          1  300.0           0                        130.27                     129.72         0.0                                                     330908.0                                             122732.0
YugabyteDB-1-1-1024-2               1         16   16384          2  300.0           0                        160.55                     159.73         0.0                                                     279105.0                                              99666.0

### Workflow

#### Actual
DBMS YugabyteDB-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
YugabyteDB-1-1-1024-1      336.0        1.0   1.0         171.428571
YugabyteDB-1-1-1024-2      336.0        1.0   2.0         171.428571

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1     8344.07    10.97          4.98                12.98
YugabyteDB-1-1-1024-2     8344.07    10.97          4.98                12.98

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1     1014.93     9.53           1.3                  1.3
YugabyteDB-1-1-1024-2     1014.93     9.53           1.3                  1.3

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1     9926.98    20.46          4.92                14.00
YugabyteDB-1-1-1024-2    12709.70    14.19          5.19                14.85

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1      137.64     0.52          0.35                 0.35
YugabyteDB-1-1-1024-2      119.33     0.29          0.81                 0.81

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
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
## Show Summary

### Workload
Benchbase Workload SF=128 (warehouses for TPC-C)
    Type: benchbase
    Duration: 16174s 
    Code: 1742828251
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 128. Benchmarking runs for 60 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Benchmark is limited to DBMS ['YugabyteDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-1-1-1024-1 uses docker image postgres:15.0
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:154012200
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:805565536
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:156245956
    worker 2
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:638185628
    eval_parameters
                code:1742828251
YugabyteDB-1-1-1024-2 uses docker image postgres:15.0
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:153722712
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:797960204
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:148533720
    worker 2
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:630513748
    eval_parameters
                code:1742828251
YugabyteDB-1-1-1024-3 uses docker image postgres:15.0
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:153722880
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    worker 0
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:798603116
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:148980828
    worker 2
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:630885236
    eval_parameters
                code:1742828251
YugabyteDB-1-1-1024-4 uses docker image postgres:15.0
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:153723052
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    worker 0
        RAM:1081965510656
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker27
        disk:798538756
    worker 1
        RAM:540587544576
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:5.15.0-134-generic
        node:cl-worker22
        disk:148775208
    worker 2
        RAM:1081966518272
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1073-nvidia
        node:cl-worker28
        disk:630888728
    eval_parameters
                code:1742828251

### Execution
                       experiment_run  terminals  target  pod_count    time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
YugabyteDB-1-1-1024-1               1         64   16384          1  3600.0                        483.16                                                     350455.0                                             132450.0
YugabyteDB-1-1-1024-2               1         64   16384          2  3600.0                        417.69                                                     393714.0                                             153224.0
YugabyteDB-1-1-1024-3               1         64   16384          4  3600.0                        384.33                                                     416268.0                                             166231.5
YugabyteDB-1-1-1024-4               1         64   16384          8  3600.0                        200.53                                                     999790.0                                             317128.5

Warehouses: 128

### Workflow

#### Actual
DBMS YugabyteDB-1-1-1024 - Pods [[8, 4, 1, 2]]

#### Planned
DBMS YugabyteDB-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
YugabyteDB-1-1-1024-1     1058.0        1.0   1.0                 435.538752
YugabyteDB-1-1-1024-2     1058.0        1.0   2.0                 435.538752
YugabyteDB-1-1-1024-3     1058.0        1.0   4.0                 435.538752
YugabyteDB-1-1-1024-4     1058.0        1.0   8.0                 435.538752

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

