# Example: Benchmark a Cloud Database

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>


The following example treats **a cloud database that is compatible to PostgreSQL**.

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

#### PostgreSQL-compatible Cloud Service - Test Environment Placeholder

In order to have a test environment, we install a placeholder instance PostgreSQL and treat it like an external service.

Create the test placeholder
```bash
# start database service
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml
```

This starts a deployment `bexhoma-deployment-postgres` with a service `bexhoma-service`.

We can delete these after the experiment has finished by
```bash
# delete database service
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service
```

All demonstration and test runs in the following are run against this placeholder.






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
nohup python ycsb.py -ms 2 -tr \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_databaseservice_1.log &
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
    * with a maximum of 1 DBMS per time (`-ms`) (plus 1 for the placeholder)
* tests if results match workflow (`-tr`)
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

doc_ycsb_databaseservice_1.log
```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 385s 
    Code: 1748446240
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.7.
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
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301260764
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1748446240

### Loading
                            experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
DatabaseService-64-8-65536               1       64   65536          8           0                   64327.577784                15642.0             1000000                              4663.5

### Execution
                              experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
DatabaseService-64-8-65536-1               1       64   65536          1           0                       63471.91                15755.0            501144                            1681.0              498856                              2429.0

### Workflow

#### Actual
DBMS DatabaseService-64-8-65536 - Pods [[1]]

#### Planned
DBMS DatabaseService-64-8-65536 - Pods [[1]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
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
nohup python ycsb.py -ms 2 -tr \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_databaseservice_2.log &
```

This skips loading (`-sl`), as data is already present in the database.

doc_ycsb_databaseservice_2.log
```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 413s 
    Code: 1748446660
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
    Benchmark is limited to DBMS ['DatabaseService'].
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
DatabaseService-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301260760
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1748446660

### Execution
                              experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
DatabaseService-64-8-65536-1               1       64   65536          1           0                       65327.88               153074.0           4999406                            1545.0             5000594                              2119.0

### Workflow

#### Actual
DBMS DatabaseService-64-8-65536 - Pods [[1]]

#### Planned
DBMS DatabaseService-64-8-65536 - Pods [[1]]

### Execution - Benchmarker
                              CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-64-8-65536-1      860.16     6.97           0.6                 0.61

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
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
nohup python ycsb.py -ms 2 -tr \
  -sf 5 \
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
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_databaseservice_3.log &
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

doc_ycsb_databaseservice_3.log
```bash
## Show Summary

### Workload
YCSB SF=5
    Type: ycsb
    Duration: 647s 
    Code: 1748447481
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 5000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['DatabaseService'].
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
DatabaseService-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301221604
    datadisk:39
    volume_size:1.0G
    volume_used:36M
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1748447481

### Loading
                            experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
DatabaseService-64-8-65536               1       64   65536          8           0                    43458.11845               115916.0             5000000                              6277.0

### Execution
                              experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
DatabaseService-64-8-65536-1               1       64   65536          1           0                       65335.14               153057.0           5000426                            1626.0             4999574                              2397.0

### Workflow

#### Actual
DBMS DatabaseService-64-8-65536 - Pods [[1]]

#### Planned
DBMS DatabaseService-64-8-65536 - Pods [[1]]

### Ingestion - Loader
                              CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-64-8-65536-1      517.95     1.67          4.61                 4.64

### Execution - Benchmarker
                              CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-64-8-65536-1      660.48        0           0.6                 0.61

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```

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

Please make sure to adjust this to the cloud service you want to benchmark.


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
* `config.monitoring_sut = False`: SUT cannot be monitored since it is outside of K8s
















## Benchbase's TPC-C

```bash
nohup python benchbase.py -ms 2 -tr \
  -sf 16 \
  -sd 5 \
  -dbms DatabaseService \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_databaseservice_1.log &
```

yields

doc_benchbase_databaseservice_1.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1153s 
    Code: 1748448241
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['DatabaseService'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DatabaseService-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301260956
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748448241
DatabaseService-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301260960
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1748448241

### Execution
                            experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
DatabaseService-1-1-1024-1               1         16   16384          1  300.0           0                       1819.79                    1811.94         0.0                                                      20223.0                                               8784.0
DatabaseService-1-1-1024-2               1         16   16384          2  300.0           2                       1694.17                    1678.63         0.0                                                      21579.0                                               9434.5

### Workflow

#### Actual
DBMS DatabaseService-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS DatabaseService-1-1-1024 - Pods [[1, 2]]

### Loading
                            time_load  terminals  pods  Throughput [SF/h]
DatabaseService-1-1-1024-1      138.0        1.0   1.0         417.391304
DatabaseService-1-1-1024-2      138.0        1.0   2.0         417.391304

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### Benchbase Example Explained

The setup is the same as for YCSB (see above).

However the connection string this time is not only read from `cluster.config`, but are also constructed from parameters that are set explicitly in the workflow file `benchbase.py`:

```
BENCHBASE_PROFILE = 'postgres',
BEXHOMA_DATABASE = 'postgres',
```

### Only Execution

This time we skip loading (`-sl`), since the database is already present.

```bash
nohup python benchbase.py -ms 2 -tr \
  -sf 16 \
  -sd 5 \
  -dbms DatabaseService \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -sl \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_databaseservice_2.log &
```

yields

doc_benchbase_databaseservice_2.log
```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 904s 
    Code: 1748449442
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['DatabaseService'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is skipped.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DatabaseService-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301260964
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748449442
DatabaseService-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301260968
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1748449442

### Execution
                            experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
DatabaseService-1-1-1024-1               1         16   16384          1  300.0           0                       1719.43                    1711.63         0.0                                                      21103.0                                               9298.0
DatabaseService-1-1-1024-2               1         16   16384          2  300.0           3                       1645.82                    1630.34         0.0                                                      21870.0                                               9713.0

### Workflow

#### Actual
DBMS DatabaseService-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS DatabaseService-1-1-1024 - Pods [[1, 2]]

### Loading
                            time_load  terminals  pods  Throughput [SF/h]
DatabaseService-1-1-1024-1          0          1     1                inf
DatabaseService-1-1-1024-2          0          1     2                inf

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```




## TPC-H

In the following we run TPC-H against the Cloud Database Service.


### Simple Run

At first we run a simple power test against SF=3.
Components are monitored.

```bash
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_1.log &
```

yields

doc_tpch_testcase_databaseservice_1.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 803s 
    Code: 1748450442
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['DatabaseService'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DatabaseService-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301261000
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748450442

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DatabaseService-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                      6224.53
Minimum Cost Supplier Query (TPC-H Q2)                                 2168.21
Shipping Priority (TPC-H Q3)                                           2485.19
Order Priority Checking Query (TPC-H Q4)                               3136.59
Local Supplier Volume (TPC-H Q5)                                       2270.49
Forecasting Revenue Change (TPC-H Q6)                                  1179.99
Forecasting Revenue Change (TPC-H Q7)                                  2313.20
National Market Share (TPC-H Q8)                                       1417.29
Product Type Profit Measure (TPC-H Q9)                                 3226.65
Forecasting Revenue Change (TPC-H Q10)                                 3100.73
Important Stock Identification (TPC-H Q11)                              581.37
Shipping Modes and Order Priority (TPC-H Q12)                          2449.89
Customer Distribution (TPC-H Q13)                                      6188.59
Forecasting Revenue Change (TPC-H Q14)                                 1263.02
Top Supplier Query (TPC-H Q15)                                         1405.49
Parts/Supplier Relationship (TPC-H Q16)                                1264.50
Small-Quantity-Order Revenue (TPC-H Q17)                               6185.77
Large Volume Customer (TPC-H Q18)                                     20826.41
Discounted Revenue (TPC-H Q19)                                         1948.81
Potential Part Promotion (TPC-H Q20)                                   1198.02
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                    2774.38
Global Sales Opportunity Query (TPC-H Q22)                              473.37

### Loading [s]
                           timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DatabaseService-BHT-8-1-1           1.0          106.0         1.0      222.0     337.0

### Geometric Mean of Medians of Timer Run [s]
                           Geo Times [s]
DBMS                                    
DatabaseService-BHT-8-1-1           2.35

### Power@Size ((3600*SF)/(geo times))
                           Power@Size [~Q/h]
DBMS                                        
DatabaseService-BHT-8-1-1            4744.63

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                      time [s]  count  SF  Throughput@Size
DBMS                    SF num_experiment num_client                                      
DatabaseService-BHT-8-1 3  1              1                 80      1   3           2970.0

### Workflow

#### Actual
DBMS DatabaseService-BHT-8 - Pods [[1]]

#### Planned
DBMS DatabaseService-BHT-8 - Pods [[1]]

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1       29.73     0.13          0.03                 2.27

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1       13.11        0          0.24                 0.25

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

### Execution Only

Now loading is skipped (`-sl`) as data is already present in the Cloud system.

```bash
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -sl \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_2.log &
```

yields

doc_tpch_testcase_databaseservice_2.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 356s 
    Code: 1748451283
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['DatabaseService'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is skipped.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DatabaseService-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301261168
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748451283

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DatabaseService-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                      6103.48
Minimum Cost Supplier Query (TPC-H Q2)                                 2128.07
Shipping Priority (TPC-H Q3)                                           2509.14
Order Priority Checking Query (TPC-H Q4)                               3125.44
Local Supplier Volume (TPC-H Q5)                                       2280.83
Forecasting Revenue Change (TPC-H Q6)                                  1172.20
Forecasting Revenue Change (TPC-H Q7)                                  2272.18
National Market Share (TPC-H Q8)                                       1456.72
Product Type Profit Measure (TPC-H Q9)                                 3146.07
Forecasting Revenue Change (TPC-H Q10)                                 3055.84
Important Stock Identification (TPC-H Q11)                              575.48
Shipping Modes and Order Priority (TPC-H Q12)                          2469.13
Customer Distribution (TPC-H Q13)                                      6326.06
Forecasting Revenue Change (TPC-H Q14)                                 1260.00
Top Supplier Query (TPC-H Q15)                                         1394.92
Parts/Supplier Relationship (TPC-H Q16)                                1371.46
Small-Quantity-Order Revenue (TPC-H Q17)                               5731.77
Large Volume Customer (TPC-H Q18)                                     21455.66
Discounted Revenue (TPC-H Q19)                                         1953.47
Potential Part Promotion (TPC-H Q20)                                   1098.27
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                    2715.51
Global Sales Opportunity Query (TPC-H Q22)                              441.81

### Loading [s]
                           timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DatabaseService-BHT-8-1-1             0              0           0          0         0

### Geometric Mean of Medians of Timer Run [s]
                           Geo Times [s]
DBMS                                    
DatabaseService-BHT-8-1-1           2.32

### Power@Size ((3600*SF)/(geo times))
                           Power@Size [~Q/h]
DBMS                                        
DatabaseService-BHT-8-1-1            4786.94

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                      time [s]  count  SF  Throughput@Size
DBMS                    SF num_experiment num_client                                      
DatabaseService-BHT-8-1 3  1              1                 80      1   3           2970.0

### Workflow

#### Actual
DBMS DatabaseService-BHT-8 - Pods [[1]]

#### Planned
DBMS DatabaseService-BHT-8 - Pods [[1]]

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1       14.24        0          0.25                 0.26

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


### Persistent Storage

We now use a PVC to store infos about the loading process.
At first, we remove the placeholder and recreate it again.
```bash
# delete pvc of placeholder
kubectl delete pvc bexhoma-storage-databaseservice-tpch-3

sleep 10

# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

sleep 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

sleep 10
```

### Ingestion with Persistent Storage

```bash
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_3.log &
```

yields

doc_tpch_testcase_databaseservice_3.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 797s 
    Code: 1748451753
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['DatabaseService'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 1Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DatabaseService-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301221844
    datadisk:39
    volume_size:1.0G
    volume_used:36M
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748451753

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DatabaseService-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                      6357.74
Minimum Cost Supplier Query (TPC-H Q2)                                 2135.17
Shipping Priority (TPC-H Q3)                                           2504.64
Order Priority Checking Query (TPC-H Q4)                               3144.02
Local Supplier Volume (TPC-H Q5)                                       2288.10
Forecasting Revenue Change (TPC-H Q6)                                  1195.12
Forecasting Revenue Change (TPC-H Q7)                                  2350.99
National Market Share (TPC-H Q8)                                       1436.89
Product Type Profit Measure (TPC-H Q9)                                 3269.30
Forecasting Revenue Change (TPC-H Q10)                                 3054.53
Important Stock Identification (TPC-H Q11)                              568.73
Shipping Modes and Order Priority (TPC-H Q12)                          2437.11
Customer Distribution (TPC-H Q13)                                      6173.29
Forecasting Revenue Change (TPC-H Q14)                                 1280.12
Top Supplier Query (TPC-H Q15)                                         1424.75
Parts/Supplier Relationship (TPC-H Q16)                                1286.89
Small-Quantity-Order Revenue (TPC-H Q17)                               6146.37
Large Volume Customer (TPC-H Q18)                                     17883.03
Discounted Revenue (TPC-H Q19)                                         1923.28
Potential Part Promotion (TPC-H Q20)                                   1246.67
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                    2818.44
Global Sales Opportunity Query (TPC-H Q22)                              464.29

### Loading [s]
                           timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DatabaseService-BHT-8-1-1           1.0          115.0         1.0      219.0     343.0

### Geometric Mean of Medians of Timer Run [s]
                           Geo Times [s]
DBMS                                    
DatabaseService-BHT-8-1-1           2.34

### Power@Size ((3600*SF)/(geo times))
                           Power@Size [~Q/h]
DBMS                                        
DatabaseService-BHT-8-1-1            4756.79

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                      time [s]  count  SF  Throughput@Size
DBMS                    SF num_experiment num_client                                      
DatabaseService-BHT-8-1 3  1              1                 77      1   3          3085.71

### Workflow

#### Actual
DBMS DatabaseService-BHT-8 - Pods [[1]]

#### Planned
DBMS DatabaseService-BHT-8 - Pods [[1]]

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1       30.12     0.06          0.03                 2.27

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1       15.65     0.29          0.27                 0.28

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

### Execution Only with Persistent Storage

Data is now present in the database.
The persistent volume helps to memorize this.
We can rerun the experiment without explicitly skipping ingestion (no `-sl`).

```bash
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_4.log &
```

yields

doc_tpch_testcase_databaseservice_4.log
```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 416s 
    Code: 1748452594
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['DatabaseService'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 1Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DatabaseService-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:301221828
    datadisk:39
    volume_size:1.0G
    volume_used:36M
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748452594

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DatabaseService-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                      6263.50
Minimum Cost Supplier Query (TPC-H Q2)                                 2133.18
Shipping Priority (TPC-H Q3)                                           2482.10
Order Priority Checking Query (TPC-H Q4)                               3149.55
Local Supplier Volume (TPC-H Q5)                                       2294.43
Forecasting Revenue Change (TPC-H Q6)                                  1216.18
Forecasting Revenue Change (TPC-H Q7)                                  2326.49
National Market Share (TPC-H Q8)                                       1460.17
Product Type Profit Measure (TPC-H Q9)                                 3149.31
Forecasting Revenue Change (TPC-H Q10)                                 3091.49
Important Stock Identification (TPC-H Q11)                              574.96
Shipping Modes and Order Priority (TPC-H Q12)                          2474.71
Customer Distribution (TPC-H Q13)                                      6408.21
Forecasting Revenue Change (TPC-H Q14)                                 1287.85
Top Supplier Query (TPC-H Q15)                                         1452.80
Parts/Supplier Relationship (TPC-H Q16)                                1282.46
Small-Quantity-Order Revenue (TPC-H Q17)                               6328.12
Large Volume Customer (TPC-H Q18)                                     19081.41
Discounted Revenue (TPC-H Q19)                                         1934.88
Potential Part Promotion (TPC-H Q20)                                   1167.20
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                    2720.93
Global Sales Opportunity Query (TPC-H Q22)                              450.14

### Loading [s]
                           timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DatabaseService-BHT-8-1-1           1.0          115.0         1.0      219.0     343.0

### Geometric Mean of Medians of Timer Run [s]
                           Geo Times [s]
DBMS                                    
DatabaseService-BHT-8-1-1           2.34

### Power@Size ((3600*SF)/(geo times))
                           Power@Size [~Q/h]
DBMS                                        
DatabaseService-BHT-8-1-1            4750.11

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                      time [s]  count  SF  Throughput@Size
DBMS                    SF num_experiment num_client                                      
DatabaseService-BHT-8-1 3  1              1                 79      1   3          3007.59

### Workflow

#### Actual
DBMS DatabaseService-BHT-8 - Pods [[1]]

#### Planned
DBMS DatabaseService-BHT-8 - Pods [[1]]

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1        15.2     0.26          0.27                 0.28

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```
