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

```bash
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 354s 
    Code: 1734663459
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 1000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are [4]. Factors for benchmarking are [4].
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
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249256012
    datadisk:39348
    requests_cpu:4
    requests_memory:16Gi

### Loading
                            experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
DatabaseService-64-8-65536               1       64   65536          8                   49973.150502                20251.0             1000000                             25397.0

### Execution
                              experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
DatabaseService-64-8-65536-1               1       64   65536          1                       55202.87                18115.0            499487                            2095.0              500513                             42239.0

### Workflow

#### Actual
DBMS DatabaseService-64-8-65536 - Pods [[1]]

#### Planned
DBMS DatabaseService-64-8-65536 - Pods [[1]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
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

```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 262s 
    Code: 1734667671
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
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
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249256216
    datadisk:39348
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DatabaseService-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                      6149.40
Minimum Cost Supplier Query (TPC-H Q2)                                 2110.09
Shipping Priority (TPC-H Q3)                                           2435.87
Order Priority Checking Query (TPC-H Q4)                               3075.44
Local Supplier Volume (TPC-H Q5)                                       2234.95
Forecasting Revenue Change (TPC-H Q6)                                  1171.11
Forecasting Revenue Change (TPC-H Q7)                                  2288.60
National Market Share (TPC-H Q8)                                       1388.84
Product Type Profit Measure (TPC-H Q9)                                 3168.23
Forecasting Revenue Change (TPC-H Q10)                                 3075.63
Important Stock Identification (TPC-H Q11)                              563.29
Shipping Modes and Order Priority (TPC-H Q12)                          2453.85
Customer Distribution (TPC-H Q13)                                      6242.59
Forecasting Revenue Change (TPC-H Q14)                                 1271.74
Top Supplier Query (TPC-H Q15)                                         1382.80
Parts/Supplier Relationship (TPC-H Q16)                                1349.50
Small-Quantity-Order Revenue (TPC-H Q17)                               5621.15
Large Volume Customer (TPC-H Q18)                                     18750.06
Discounted Revenue (TPC-H Q19)                                         1919.85
Potential Part Promotion (TPC-H Q20)                                   1131.92
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                    2704.33
Global Sales Opportunity Query (TPC-H Q22)                              444.20

### Loading [s]
                           timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DatabaseService-BHT-8-1-1             0              0           0          0         0

### Geometric Mean of Medians of Timer Run [s]
                           Geo Times [s]
DBMS                                    
DatabaseService-BHT-8-1-1           2.29

### Power@Size
                           Power@Size [~Q/h]
DBMS                                        
DatabaseService-BHT-8-1-1            4850.83

### Throughput@Size
                                                      time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                    SF num_experiment num_client                                              
DatabaseService-BHT-8-1 3  1              1                 76      1   3                  3126.32

### Workflow

#### Actual
DBMS DatabaseService-BHT-8 - Pods [[1]]

#### Planned
DBMS DatabaseService-BHT-8 - Pods [[1]]

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1       11.36        0          0.22                 0.24

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
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

```bash
## Show Summary

### Workload
YCSB SF=5
    Type: ycsb
    Duration: 3718s 
    Code: 1734700853
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 5000000. Number of operations is 10000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are [4]. Factors for benchmarking are [4].
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
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:250060572
    datadisk:39192
    volume_size:1.0G
    volume_used:36M
    requests_cpu:4
    requests_memory:16Gi

### Loading
                            experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
DatabaseService-64-8-65536               1       64   65536          8                   34656.857878               145263.0             5000000                              6815.5

### Execution
                              experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
DatabaseService-64-8-65536-1               1       64   65536          1                        65353.5               153014.0           4997965                             653.0             5002035                              1296.0

### Workflow

#### Actual
DBMS DatabaseService-64-8-65536 - Pods [[1]]

#### Planned
DBMS DatabaseService-64-8-65536 - Pods [[1]]

### Ingestion - Loader
                              CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-64-8-65536-1      397.12     0.88           4.6                 4.62

### Execution - Benchmarker
                              CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-64-8-65536-1      743.75     5.11           0.6                 0.61

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
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

```bash
## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 1091s 
    Code: 1734664810
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
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
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249256016
    datadisk:39348
    requests_cpu:4
    requests_memory:16Gi
DatabaseService-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249256020
    datadisk:39348
    requests_cpu:4
    requests_memory:16Gi

### Execution
                            experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
DatabaseService-1-1-1024-1               1         16   16384          1  300.0                       1873.16                                                      19246.0                                               8535.0
DatabaseService-1-1-1024-2               1         16   16384          2  300.0                       1820.81                                                      21236.0                                               8782.5

Warehouses: 16

### Workflow

#### Actual
DBMS DatabaseService-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS DatabaseService-1-1-1024 - Pods [[1, 2]]

### Loading
                            time_load  terminals  pods  Imported warehouses [1/h]
DatabaseService-1-1-1024-1      150.0        1.0   1.0                      384.0
DatabaseService-1-1-1024-2      150.0        1.0   2.0                      384.0

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

```bash
## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 814s 
    Code: 1734665950
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
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
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249256028
    datadisk:39348
    requests_cpu:4
    requests_memory:16Gi
DatabaseService-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249256028
    datadisk:39348
    requests_cpu:4
    requests_memory:16Gi

### Execution
                            experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
DatabaseService-1-1-1024-1               1         16   16384          1  300.0                       1948.43                                                      18329.0                                               8206.0
DatabaseService-1-1-1024-2               1         16   16384          2  300.0                       1774.67                                                      21116.0                                               9008.5

Warehouses: 16

### Workflow

#### Actual
DBMS DatabaseService-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS DatabaseService-1-1-1024 - Pods [[1, 2]]

### Loading
                            time_load  terminals  pods  Imported warehouses [1/h]
DatabaseService-1-1-1024-1          0          1     1                        inf
DatabaseService-1-1-1024-2          0          1     2                        inf

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

```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 765s 
    Code: 1734666830
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
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
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249256232
    datadisk:39348
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DatabaseService-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                      6184.88
Minimum Cost Supplier Query (TPC-H Q2)                                 2121.70
Shipping Priority (TPC-H Q3)                                           2477.89
Order Priority Checking Query (TPC-H Q4)                               3120.41
Local Supplier Volume (TPC-H Q5)                                       2263.59
Forecasting Revenue Change (TPC-H Q6)                                  1158.38
Forecasting Revenue Change (TPC-H Q7)                                  2326.20
National Market Share (TPC-H Q8)                                       1410.37
Product Type Profit Measure (TPC-H Q9)                                 3187.17
Forecasting Revenue Change (TPC-H Q10)                                 3063.93
Important Stock Identification (TPC-H Q11)                              561.36
Shipping Modes and Order Priority (TPC-H Q12)                          2457.12
Customer Distribution (TPC-H Q13)                                      6562.69
Forecasting Revenue Change (TPC-H Q14)                                 1280.33
Top Supplier Query (TPC-H Q15)                                         1396.18
Parts/Supplier Relationship (TPC-H Q16)                                1346.35
Small-Quantity-Order Revenue (TPC-H Q17)                               5626.89
Large Volume Customer (TPC-H Q18)                                     19220.56
Discounted Revenue (TPC-H Q19)                                         1909.47
Potential Part Promotion (TPC-H Q20)                                   1216.54
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                    2784.81
Global Sales Opportunity Query (TPC-H Q22)                              465.76

### Loading [s]
                           timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DatabaseService-BHT-8-1-1           1.0           97.0         1.0      216.0     322.0

### Geometric Mean of Medians of Timer Run [s]
                           Geo Times [s]
DBMS                                    
DatabaseService-BHT-8-1-1           2.32

### Power@Size
                           Power@Size [~Q/h]
DBMS                                        
DatabaseService-BHT-8-1-1            4783.05

### Throughput@Size
                                                      time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                    SF num_experiment num_client                                              
DatabaseService-BHT-8-1 3  1              1                 77      1   3                  3085.71

### Workflow

#### Actual
DBMS DatabaseService-BHT-8 - Pods [[1]]

#### Planned
DBMS DatabaseService-BHT-8 - Pods [[1]]

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1        30.9     0.21          0.03                 2.27

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1       11.41        0          0.23                 0.24

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
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

```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 262s 
    Code: 1734667671
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
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
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249256216
    datadisk:39348
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DatabaseService-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                      6149.40
Minimum Cost Supplier Query (TPC-H Q2)                                 2110.09
Shipping Priority (TPC-H Q3)                                           2435.87
Order Priority Checking Query (TPC-H Q4)                               3075.44
Local Supplier Volume (TPC-H Q5)                                       2234.95
Forecasting Revenue Change (TPC-H Q6)                                  1171.11
Forecasting Revenue Change (TPC-H Q7)                                  2288.60
National Market Share (TPC-H Q8)                                       1388.84
Product Type Profit Measure (TPC-H Q9)                                 3168.23
Forecasting Revenue Change (TPC-H Q10)                                 3075.63
Important Stock Identification (TPC-H Q11)                              563.29
Shipping Modes and Order Priority (TPC-H Q12)                          2453.85
Customer Distribution (TPC-H Q13)                                      6242.59
Forecasting Revenue Change (TPC-H Q14)                                 1271.74
Top Supplier Query (TPC-H Q15)                                         1382.80
Parts/Supplier Relationship (TPC-H Q16)                                1349.50
Small-Quantity-Order Revenue (TPC-H Q17)                               5621.15
Large Volume Customer (TPC-H Q18)                                     18750.06
Discounted Revenue (TPC-H Q19)                                         1919.85
Potential Part Promotion (TPC-H Q20)                                   1131.92
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                    2704.33
Global Sales Opportunity Query (TPC-H Q22)                              444.20

### Loading [s]
                           timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DatabaseService-BHT-8-1-1             0              0           0          0         0

### Geometric Mean of Medians of Timer Run [s]
                           Geo Times [s]
DBMS                                    
DatabaseService-BHT-8-1-1           2.29

### Power@Size
                           Power@Size [~Q/h]
DBMS                                        
DatabaseService-BHT-8-1-1            4850.83

### Throughput@Size
                                                      time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                    SF num_experiment num_client                                              
DatabaseService-BHT-8-1 3  1              1                 76      1   3                  3126.32

### Workflow

#### Actual
DBMS DatabaseService-BHT-8 - Pods [[1]]

#### Planned
DBMS DatabaseService-BHT-8 - Pods [[1]]

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1       11.36        0          0.22                 0.24

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
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

```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 798s 
    Code: 1734668021
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
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
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249216892
    datadisk:39192
    volume_size:1.0G
    volume_used:36M
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DatabaseService-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                      5793.75
Minimum Cost Supplier Query (TPC-H Q2)                                 1922.31
Shipping Priority (TPC-H Q3)                                           2231.66
Order Priority Checking Query (TPC-H Q4)                               2835.42
Local Supplier Volume (TPC-H Q5)                                       2072.36
Forecasting Revenue Change (TPC-H Q6)                                  1066.68
Forecasting Revenue Change (TPC-H Q7)                                  2155.03
National Market Share (TPC-H Q8)                                       1301.26
Product Type Profit Measure (TPC-H Q9)                                 2787.60
Forecasting Revenue Change (TPC-H Q10)                                 2791.42
Important Stock Identification (TPC-H Q11)                              559.95
Shipping Modes and Order Priority (TPC-H Q12)                          2143.46
Customer Distribution (TPC-H Q13)                                      5364.32
Forecasting Revenue Change (TPC-H Q14)                                 1190.47
Top Supplier Query (TPC-H Q15)                                         1291.81
Parts/Supplier Relationship (TPC-H Q16)                                1127.44
Small-Quantity-Order Revenue (TPC-H Q17)                               4912.21
Large Volume Customer (TPC-H Q18)                                     16174.10
Discounted Revenue (TPC-H Q19)                                         1735.84
Potential Part Promotion (TPC-H Q20)                                   1088.33
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                    2474.25
Global Sales Opportunity Query (TPC-H Q22)                              488.84

### Loading [s]
                           timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DatabaseService-BHT-8-1-1           1.0          123.0         1.0      196.0     326.0

### Geometric Mean of Medians of Timer Run [s]
                           Geo Times [s]
DBMS                                    
DatabaseService-BHT-8-1-1           2.11

### Power@Size
                           Power@Size [~Q/h]
DBMS                                        
DatabaseService-BHT-8-1-1            5279.56

### Throughput@Size
                                                      time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                    SF num_experiment num_client                                              
DatabaseService-BHT-8-1 3  1              1                 70      1   3                  3394.29

### Workflow

#### Actual
DBMS DatabaseService-BHT-8 - Pods [[1]]

#### Planned
DBMS DatabaseService-BHT-8 - Pods [[1]]

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1       41.77     0.04          0.02                  2.8

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1       15.95        0          0.26                 0.27

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
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

```bash
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 273s 
    Code: 1734668861
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
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
    RAM:541008576512
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249216876
    datadisk:39192
    volume_size:1.0G
    volume_used:36M
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DatabaseService-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                      5785.36
Minimum Cost Supplier Query (TPC-H Q2)                                 1938.19
Shipping Priority (TPC-H Q3)                                           2255.59
Order Priority Checking Query (TPC-H Q4)                               2827.21
Local Supplier Volume (TPC-H Q5)                                       2018.18
Forecasting Revenue Change (TPC-H Q6)                                  1062.37
Forecasting Revenue Change (TPC-H Q7)                                  2075.73
National Market Share (TPC-H Q8)                                       1336.07
Product Type Profit Measure (TPC-H Q9)                                 2808.84
Forecasting Revenue Change (TPC-H Q10)                                 2804.71
Important Stock Identification (TPC-H Q11)                              583.68
Shipping Modes and Order Priority (TPC-H Q12)                          2137.04
Customer Distribution (TPC-H Q13)                                      5569.93
Forecasting Revenue Change (TPC-H Q14)                                 1130.83
Top Supplier Query (TPC-H Q15)                                         1321.32
Parts/Supplier Relationship (TPC-H Q16)                                1239.32
Small-Quantity-Order Revenue (TPC-H Q17)                               5228.78
Large Volume Customer (TPC-H Q18)                                     17602.90
Discounted Revenue (TPC-H Q19)                                         1735.06
Potential Part Promotion (TPC-H Q20)                                   1018.27
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                    2464.08
Global Sales Opportunity Query (TPC-H Q22)                              451.76

### Loading [s]
                           timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DatabaseService-BHT-8-1-1           1.0          123.0         1.0      196.0     326.0

### Geometric Mean of Medians of Timer Run [s]
                           Geo Times [s]
DBMS                                    
DatabaseService-BHT-8-1-1           2.11

### Power@Size
                           Power@Size [~Q/h]
DBMS                                        
DatabaseService-BHT-8-1-1            5249.82

### Throughput@Size
                                                      time [s]  count  SF  Throughput@Size [~GB/h]
DBMS                    SF num_experiment num_client                                              
DatabaseService-BHT-8-1 3  1              1                 71      1   3                  3346.48

### Workflow

#### Actual
DBMS DatabaseService-BHT-8 - Pods [[1]]

#### Planned
DBMS DatabaseService-BHT-8 - Pods [[1]]

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DatabaseService-BHT-8-1        16.0        0          0.25                 0.27

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```
