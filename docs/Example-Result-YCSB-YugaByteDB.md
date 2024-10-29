# Example: YCSB in YugabyteDB

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

**The results are not official benchmark results. The exact performance depends on a collection of parameters.
The purpose of this example is to illustrate the usage of bexhoma and to show how to evaluate results.**

This experiment differs from the default behaviour of bexhoma, since we benchmark a DBMS, that is not managed by bexhoma, but exists in the Kubernetes cluster in the same namespace.

Important implications of this:
* Bexhoma does neither start nor stop the DBMS.
* There can only be one DBMS in the cluster at the same time.
* Bexhoma does not know what resides inside of the database.
* Bexhoma still can monitor all components of the experiment, including the DBMS itself.

In order to be fully functional, bexhoma installs an instance of PostgreSQL, that does nothing (a container with psql would be enough).
Bexhoma writes infos about the status of the experiment to this "SUT" pod to mimick it has access to the dbms.
Moreover the container is used to install a schema to YugabyteDB via psql.

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the YugabyteDB cluster.

References:
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. YugabyteDB YCSB: https://docs.yugabyte.com/preview/benchmark/ycsb-jdbc/
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9

## Install YugabyteDB

Get the helm chart and follow the instructions: https://docs.yugabyte.com/stable/deploy/kubernetes/single-zone/oss/helm-chart/


## Perform Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
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
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_yugabytedb_1.log &
```

This
* loops over `n` in [1,8] and `t` in [1,4]
  * starts a clean instance of PostgreSQL (`-dbms`)
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
+-----------------------+--------------+--------------+------------+-------------+
| 1730133803            | sut          |   loaded [s] | use case   | loading     |
+=======================+==============+==============+============+=============+
| PostgreSQL-64-1-16384 | (1. Running) |            1 | ycsb       | (1 Running) |
+-----------------------+--------------+--------------+------------+-------------+
```

The code `1730133803` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1730133803` (removes everything that is related to experiment `1730133803`).

## Evaluate Results

At the end of a benchmark you will see a summary like

```bash
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 1495s 
    Code: 1730133803
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 10000000. Number of operations is 10000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are [1]. Factors for benchmarking are [1].
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
YugabyteDB-64-8-131072-1 uses docker image postgres:15.0
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254315324
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi

### Loading
                        experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-131072               1       64  131072          8                   15974.538188               628780.0            10000000                             56699.0

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-131072-1               1       64  131072          1                       15960.37               626552.0           5000179                           60031.0             4999821                             63231.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-131072 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-131072 - Pods [[1]]

### Ingestion - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-131072-1    27027.86    15.59         17.41                24.05

### Ingestion - Loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-131072-1     1504.53     1.38          4.63                 4.65

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-131072-1    21956.83    22.12         18.72                24.05

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-131072-1     1057.01     2.12          0.61                 0.61

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


## Perform Execution Benchmark

The default behaviour of bexhoma is that several different settings of the loading component are compared.
We might only want to benchmark the workloads of YCSB in different configurations and have a fixed loading phase.

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -sl \
  --workload a \
  -dbms YugabyteDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_yugabytedb_2.log &
```

This skips loading (`-sl`), as data is already present in the database.

```bash
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 688s 
    Code: 1730137438
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 10000000. Number of operations is 10000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '131072'. Factors for loading are [1]. Factors for benchmarking are [1].
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
YugabyteDB-64-8-131072-1 uses docker image postgres:15.0
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254315156
    datadisk:39268
    requests_cpu:4
    requests_memory:16Gi

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-131072-1               1       64  131072          1                       19735.97               506689.0           4999996                           53823.0             5000004                             59679.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-131072 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-131072 - Pods [[1]]

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-131072-1    21313.77    21.88          19.5                24.05

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-131072-1      957.17      2.0          0.61                 0.61

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

## Use Persistent Storage

Persistent Storage is not managed by bexhoma, but by YugabyteDB.

## Example Explained

### Configuration of Bexhoma

In `cluster.config` there is a section:

```
'YugabyteDB': {
    'loadData': 'psql -U yugabyte --host yb-tserver-service.perdelt.svc.cluster.local --port 5433 < {scriptname}',
    'template': {
        'version': '2.17.1',
        'alias': 'Cloud-Native-1',
        'docker_alias': 'CN1',
         'JDBC': {
            'driver': "com.yugabyte.Driver",
            'auth': ["yugabyte", ""],
            'url': 'jdbc:yugabytedb://yb-tserver-service.perdelt.svc.cluster.local:5433/yugabyte?load-balance=true',#/{dbname}',
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
* `config.sut_container_name`: Fixed name for the container of the SUT (="yb-tserver")
* `config.create_monitoring()`: Method to create names for monitored components (for SUT = "yb-tserver-")
* `config.get_worker_endpoints()`: ?
* `config.set_metric_of_config()`: Method to create promql queries from templates (pod like "yb-tserver", no container name)
