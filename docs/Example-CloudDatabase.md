# Example: Benchmark a Cloud Database

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

## Types of DBMS

### Managed by Bexhoma

We included [CockroachDB](Example-CockroachDB) as an example for a distributed DBMS, that is managed by bexhoma.

Advantages
* Bexhoma can monitor all components
* Bexhoma knows about loaded databases, their status and timings

Disadvantages
* This is only implemented for some examples
* This cannot be applied to Cloud services (or any other database outside of the Kubernetes cluster)

### Not Managed by Bexhoma

We included [YugaByteDB](Example-YugaByteDB) as an example for a distributed DBMS, that is not managed by bexhoma, but runs in the same Kubernetes cluster.

Advantages
* Can be applied to all systems running in Kubernetes
* Bexhoma can monitor all components

Disadvantages
* Bexhoma not necessarily knows about loaded databases, their status and timings - they might be affected by outside services
* This cannot be applied to Cloud services (or any other database outside of the Kubernetes cluster)

### Outside of Kubernetes

Here we present an example for a DBMS, that is not managed by bexhoma and might be running outside of the Kubernetes cluster.

Advantages
* This can be applied to all Cloud services (or any other database outside of the Kubernetes cluster) with a JDBC interface

Disadvantages
* The SUT cannot be monitored by Bexhoma
* Bexhoma not necessarily knows about loaded databases, their status and timings - they might be affected by outside services









## PostgreSQL-compatible Cloud Service

The following example treats **a cloud database that is compatible to PostgreSQL**.

Important implications of this:
* Bexhoma can do the ingestion - example PostgreSQL compatible (or sandbox?)
* skip loading should be possible
* PVC useful to skip loading in future?

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that is not managed by bexhoma and does not exist in the Kubernetes cluster in the same namespace**.

Important implications of this:
* Bexhoma does neither start nor stop the DBMS.
* There can only be one DBMS in the cluster at the same time.
* Bexhoma does not know what resides inside of the database.
* Bexhoma still can only monitor the components of the experiment other than the SUT.

In order to be fully functional, bexhoma installs an instance of PostgreSQL, that does nothing (a container with psql would be enough).
Bexhoma writes infos about the status of the experiment to this "SUT" pod to mimick it has access to the DBMS.
Moreover the container is used to install a schema to the database via psql.

All metrics in monitoring are summed across all matching components.

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
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
  -sfo 1 \
  --workload a \
  -dbms DatabaseService \
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
  run </dev/null &>$LOG_DIR/test_ycsb_databaseservice_tmp1.log &
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of a dummy container as a placeholder for the DatabaseService (`-dbms`)
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
+----------------------------+--------------+--------------+------------+---------------+
| 1730133803                 | sut          |   loaded [s] | use case   | benchmarker   |
+============================+==============+==============+============+===============+
| DatabaseService-64-8-65536 | (1. Running) |           41 | ycsb       | (1. Running)  |
+----------------------------+--------------+--------------+------------+---------------+
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
    Duration: 378s 
    Code: 1732808631
    This includes no queries. YCSB runs the benchmark
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are [4]. Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['DatabaseService'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DatabaseService-64-8-65536-1 uses docker image postgres:16.1
    node:cl-worker11
    requests_cpu:4
    requests_memory:16Gi

### Loading
                            experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
DatabaseService-64-8-65536               1       64   65536          8                   24211.574786                41517.0             1000000                             21027.0

### Execution
                              experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
DatabaseService-64-8-65536-1               1       64   65536          1                       30987.57                32271.0            499597                           39007.0              500403                             44095.0

### Workflow

#### Actual
DBMS DatabaseService-64-8-65536 - Pods [[1]]

#### Planned
DBMS DatabaseService-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                              CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-64-8-65536-1        0.24        0          2.35                 2.38

### Ingestion - Loader
                              CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-64-8-65536-1       82.45        0           4.2                 4.23

### Execution - SUT
                              CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-64-8-65536-1        0.15        0          2.35                 2.38

### Execution - Benchmarker
                              CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-64-8-65536-1       58.46        0          0.53                 0.53

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
  -dbms DatabaseService \
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
  run </dev/null &>$LOG_DIR/test_ycsb_databaseservice_tmp2.log &
```

This skips loading (`-sl`), as data is already present in the database.

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 690s 
    Code: 1730223222
    This includes no queries. YCSB runs the benchmark
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
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254319248
    datadisk:39268
    requests_cpu:4
    requests_memory:16Gi

### Execution
                         experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1                       19547.36               511578.0           4998778                           64703.0             5001222                             66239.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     19802.0    26.15         14.21                24.03

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1     1039.41     2.13          0.61                 0.61

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

The `-mc` option is mandatory here: The sidecar container approach is not working (since bexhoma does not manage the deployment), so either you have Prometheus / Node exporter already installed in your cluster or a daemonset is needed.
Moreover the SUT itself cannot be monitored, since it is outside of the cluster.
For further explanation see the monitoring section of this documentation.


## Use Persistent Storage

### Bexhoma Status Volume

Persistent Storage is not managed by bexhoma, but by the Cloud service.
We can add the request for a PVC to the experiment setup:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 1 \
  --workload a \
  -dbms DatabaseService \
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
  run </dev/null &>$LOG_DIR/test_ycsb_databaseservice_tmp3.log &
```
This will add a PVC to the Dummy DBMS.
Nothing will be stored there, but it maintains status information about previous loading processes.

```
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-databaseservice-ycsb-1 | databaseservice | ycsb-1       | True         |                65 | DatabaseService | shared               | 1Gi       | Bound    | 1.0G   | 36M    |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
```

The above means there has been a YCSB loading process (managed by bexhoma) of size SF=1, that has been completed.
All following calls of such an experiment will skip loading, since the PVC tells it has been finished.
This thus helps to spare the `-sl` parameter.

However bexhoma cannot verify such information.
If data is delete somehow, this PVC information will be outdated and wrong.

This approach helps bexhoma to persist status information, but it does not persist data inside the Cloud database.



## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```
'DatabaseService': {
    'loadData': 'psql -U postgres --host mydatabase.example.com --port 5432 < {scriptname}',
    'template': {
        'version': 'v1234',
        'alias': 'Cloud-A',
        'docker_alias': 'CL-A',
         'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", ""],
            'url': 'jdbc:postgresql://mydatabase.example.com:5432/postgres?reWriteBatchedInserts=true',
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


### Preparation of YCSB

In the Docker files for YCSB
* https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ycsb/generator/Dockerfile
* https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/ycsb/benchmarker/Dockerfile

there is a section about including the needed JDBC driver:
```
######### Specific version of PostgreSQL JDBC #########
RUN wget https://jdbc.postgresql.org/download/postgresql-42.5.0.jar --no-check-certificate
RUN cp postgresql-42.5.0.jar jars/postgresql-42.5.0.jar
```


### Dummy SUT

Bexhoma deploys a pod to carry status informations.
Here it is an instance of PostgreSQL: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-DatabaseService.yml


### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/DatabaseService


### Workflow of YCSB

In `ycsb.py` there is a section about DatabaseService.

Watch for
* `config.sut_service_name`: Fixed name for the service of the SUT (="yb-tserver-service")
* `config.sut_container_name`: Fixed name for the container of the SUT (="yb-tserver")
* `config.create_monitoring()`: Method to create names for monitored components (for SUT = "yb-tserver-")
* `config.get_worker_endpoints()`: ?
* `config.set_metric_of_config()`: Method to create promql queries from templates (pod like "yb-tserver", no container name)
















## Benchbase's TPC-C

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
    Duration: 1026s 
    Code: 1730223936
    This includes no queries. Benchbase runs the benchmark
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
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254319408
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi
YugabyteDB-1-1-1024-2 uses docker image postgres:15.0
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254319580
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
YugabyteDB-1-1-1024-1               1         16   16384          1  300.0                        395.54                                                     100821.0                                              40433.0
YugabyteDB-1-1-1024-2               1         16   16384          2  300.0                        346.81                                                     112470.0                                              46113.5

Warehouses: 16

### Workflow

#### Actual
DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
YugabyteDB-1-1-1024-1      200.0        1.0   1.0                      288.0
YugabyteDB-1-1-1024-2      200.0        1.0   2.0                      288.0

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

```
## Show Summary

### Workload
Benchbase Workload SF=128 (warehouses for TPC-C)
    Type: benchbase
    Duration: 16098s 
    Code: 1730226312
    This includes no queries. Benchbase runs the benchmark
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
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254319580
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi
YugabyteDB-1-1-1024-2 uses docker image postgres:15.0
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254319748
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi
YugabyteDB-1-1-1024-3 uses docker image postgres:15.0
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254319920
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi
YugabyteDB-1-1-1024-4 uses docker image postgres:15.0
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254320088
    datadisk:39428
    requests_cpu:4
    requests_memory:16Gi

### Execution
                       experiment_run  terminals  target  pod_count    time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
YugabyteDB-1-1-1024-1               1         64   16384          1  3600.0                        469.61                                                     327056.0                                            136271.00
YugabyteDB-1-1-1024-2               1         64   16384          2  3600.0                        450.66                                                     357886.0                                            141998.50
YugabyteDB-1-1-1024-3               1         64   16384          4  3600.0                        402.57                                                     409184.0                                            159129.50
YugabyteDB-1-1-1024-4               1         64   16384          8  3600.0                        247.49                                                     896527.0                                            258644.62

Warehouses: 128

### Workflow

#### Actual
DBMS YugabyteDB-1-1-1024 - Pods [[1, 4, 2, 8]]

#### Planned
DBMS YugabyteDB-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
YugabyteDB-1-1-1024-1     1151.0        1.0   1.0                 400.347524
YugabyteDB-1-1-1024-2     1151.0        1.0   2.0                 400.347524
YugabyteDB-1-1-1024-3     1151.0        1.0   4.0                 400.347524
YugabyteDB-1-1-1024-4     1151.0        1.0   8.0                 400.347524

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

