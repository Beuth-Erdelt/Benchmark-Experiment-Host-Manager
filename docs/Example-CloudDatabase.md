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

```bash
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
```markdown
﻿## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 432s 
    Code: 1770021926
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['DatabaseService'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DBS-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95637
    datadisk:39
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1770021926

### Loading
                experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
DBS-64-8-65536               1       64   65536          8           0                   64525.023063                15517.0             1000000                             3249.75

### Execution
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
DBS-64-8-65536-1               1       64   65536          1           0                       64354.21                15539.0            499599                             380.0              500401                               526.0

### Workflow

#### Actual
DBMS DBS-64-8-65536 - Pods [[1]]

#### Planned
DBMS DBS-64-8-65536 - Pods [[1]]

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
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
```markdown
﻿## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 423s 
    Code: 1770022407
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
    Experiment is limited to DBMS ['DatabaseService'].
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
DBS-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95637
    datadisk:39
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1770022407

### Execution
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
DBS-64-8-65536-1               1       64   65536          1           0                       65406.93               152889.0           5000880                             361.0             4999120                               441.0

### Workflow

#### Actual
DBMS DBS-64-8-65536 - Pods [[1]]

#### Planned
DBMS DBS-64-8-65536 - Pods [[1]]

### Monitoring

### Execution phase: component benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DBS-64-8-65536-1      507.73     4.34          0.13                 0.14

### Tests
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
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

```bash
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
```markdown
﻿## Show Summary

### Workload
YCSB SF=5
    Type: ycsb
    Duration: 563s 
    Code: 1770023227
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 5000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['DatabaseService'].
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
DBS-64-8-65536-1 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95599
    datadisk:39
    volume_size:1.0G
    volume_used:36M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1770023227

### Loading
                experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
DBS-64-8-65536               1       64   65536          8           0                   65334.817539                76544.0             5000000                             2950.25

### Execution
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
DBS-64-8-65536-1               1       64   65536          1           0                       65411.21               152879.0           5000229                             394.0             4999771                               549.0

### Workflow

#### Actual
DBMS DBS-64-8-65536 - Pods [[1]]

#### Planned
DBMS DBS-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DBS-64-8-65536-1      449.57     6.73          0.11                 0.11

### Execution phase: component benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DBS-64-8-65536-1      487.65     4.51          0.13                 0.13

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```

## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
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
```bash
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
```markdown
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1124s 
    Code: 1770023868
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['DatabaseService'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DBS-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95638
    datadisk:39
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1770023868
DBS-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95638
    datadisk:39
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1770023868

### Execution

#### Per Pod
                  experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                              
DBS-1-1-1024-1-1               1         16   16384       1      1  300.0           0                   4194.929755                4175.883089         0.0                                                       8048.0                                               3812.0
DBS-1-1-1024-2-1               1          8    8192       2      1  300.0           0                   1923.152613                1905.305953         0.0                                                       9602.0                                               4157.0
DBS-1-1-1024-2-2               1          8    8192       2      2  300.0           2                   1926.136593                1908.153260         0.0                                                       9540.0                                               4150.0

#### Aggregated Parallel
                experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
DBS-1-1-1024-1               1         16   16384          1  300.0           0                       4194.93                    4175.88         0.0                                                       8048.0                                               3812.0
DBS-1-1-1024-2               1         16   16384          2  300.0           2                       3849.29                    3813.46         0.0                                                       9602.0                                               4153.5

### Workflow

#### Actual
DBMS DBS-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS DBS-1-1-1024 - Pods [[1, 2]]

### Loading
                time_load  terminals  pods  Throughput [SF/h]
DBS-1-1-1024-1      147.0        1.0   1.0         391.836735
DBS-1-1-1024-2      147.0        1.0   2.0         391.836735

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### Benchbase Example Explained

The setup is the same as for YCSB (see above).

However the connection string this time is not only read from `cluster.config`, but are also constructed from parameters that are set explicitly in the workflow file `benchbase.py`:

```bash
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
```markdown
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 928s 
    Code: 1770025008
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['DatabaseService'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is skipped.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DBS-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95638
    datadisk:39
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1770025008
DBS-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95638
    datadisk:39
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1770025008

### Execution

#### Per Pod
                  experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                              
DBS-1-1-1024-1-1               1         16   16384       1      1  300.0           0                   4236.779164                4218.015834         0.0                                                       8145.0                                               3774.0
DBS-1-1-1024-2-1               1          8    8192       2      1  300.0           3                   1947.856369                1928.746372         0.0                                                       9277.0                                               4103.0
DBS-1-1-1024-2-2               1          8    8192       2      2  300.0           2                   1959.836444                1940.699779         0.0                                                       9306.0                                               4078.0

#### Aggregated Parallel
                experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
DBS-1-1-1024-1               1         16   16384          1  300.0           0                       4236.78                    4218.02         0.0                                                       8145.0                                               3774.0
DBS-1-1-1024-2               1         16   16384          2  300.0           5                       3907.69                    3869.45         0.0                                                       9306.0                                               4090.5

### Workflow

#### Actual
DBMS DBS-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS DBS-1-1-1024 - Pods [[1, 2]]

### Loading
                time_load  terminals  pods  Throughput [SF/h]
DBS-1-1-1024-1          0          1     1                inf
DBS-1-1-1024-2          0          1     2                inf

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
```markdown
﻿## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 331s 
    Code: 1770026669
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['DatabaseService'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is skipped.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DBS-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95638
    datadisk:39
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1770026669

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DBS-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                          3255.56
Minimum Cost Supplier Query (TPC-H Q2)                     1021.21
Shipping Priority (TPC-H Q3)                               1431.78
Order Priority Checking Query (TPC-H Q4)                   1989.65
Local Supplier Volume (TPC-H Q5)                           1285.98
Forecasting Revenue Change (TPC-H Q6)                       690.38
Forecasting Revenue Change (TPC-H Q7)                      1270.43
National Market Share (TPC-H Q8)                            873.18
Product Type Profit Measure (TPC-H Q9)                     2124.62
Forecasting Revenue Change (TPC-H Q10)                     1611.95
Important Stock Identification (TPC-H Q11)                  332.01
Shipping Modes and Order Priority (TPC-H Q12)              1492.37
Customer Distribution (TPC-H Q13)                          4015.32
Forecasting Revenue Change (TPC-H Q14)                      760.89
Top Supplier Query (TPC-H Q15)                              784.28
Parts/Supplier Relationship (TPC-H Q16)                     734.32
Small-Quantity-Order Revenue (TPC-H Q17)                   3154.54
Large Volume Customer (TPC-H Q18)                         10315.88
Discounted Revenue (TPC-H Q19)                             1085.44
Potential Part Promotion (TPC-H Q20)                        604.28
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)        1483.49
Global Sales Opportunity Query (TPC-H Q22)                  272.17

### Loading [s]
               timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DBS-BHT-8-1-1             0              0           0          0         0

### Geometric Mean of Medians of Timer Run [s]
               Geo Times [s]
DBMS                        
DBS-BHT-8-1-1           1.34

### Power@Size ((3600*SF)/(geo times))
               Power@Size [~Q/h]
DBMS                            
DBS-BHT-8-1-1            8418.43

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                           time [s]  count   SF  Throughput@Size
DBMS        SF  num_experiment num_client                                       
DBS-BHT-8-1 3.0 1              1                 47      1  3.0          5055.32

### Workflow
                 orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
DBS-BHT-8-1-1  DBS-BHT-8-1  3.0     8               1           1       1770026898     1770026945

#### Actual
DBMS DBS-BHT-8 - Pods [[1]]

#### Planned
DBMS DBS-BHT-8 - Pods [[1]]

### Execution - Benchmarker
             CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DBS-BHT-8-1           0        0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
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
```markdown
﻿## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 636s 
    Code: 1770027140
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['DatabaseService'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 1Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DBS-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95599
    datadisk:39
    volume_size:1.0G
    volume_used:36M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1770027140

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DBS-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                          3311.45
Minimum Cost Supplier Query (TPC-H Q2)                     1030.73
Shipping Priority (TPC-H Q3)                               1463.99
Order Priority Checking Query (TPC-H Q4)                   2025.43
Local Supplier Volume (TPC-H Q5)                           1314.89
Forecasting Revenue Change (TPC-H Q6)                       706.22
Forecasting Revenue Change (TPC-H Q7)                      1316.59
National Market Share (TPC-H Q8)                            897.64
Product Type Profit Measure (TPC-H Q9)                     2122.85
Forecasting Revenue Change (TPC-H Q10)                     1635.44
Important Stock Identification (TPC-H Q11)                  321.04
Shipping Modes and Order Priority (TPC-H Q12)              1428.78
Customer Distribution (TPC-H Q13)                          3783.11
Forecasting Revenue Change (TPC-H Q14)                      764.48
Top Supplier Query (TPC-H Q15)                              804.45
Parts/Supplier Relationship (TPC-H Q16)                     735.08
Small-Quantity-Order Revenue (TPC-H Q17)                   3111.23
Large Volume Customer (TPC-H Q18)                         10341.22
Discounted Revenue (TPC-H Q19)                             1115.25
Potential Part Promotion (TPC-H Q20)                        604.73
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)        1505.44
Global Sales Opportunity Query (TPC-H Q22)                  276.40

### Loading [s]
               timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DBS-BHT-8-1-1          24.0           52.0         1.0      267.0     348.0

### Geometric Mean of Medians of Timer Run [s]
               Geo Times [s]
DBMS                        
DBS-BHT-8-1-1           1.35

### Power@Size ((3600*SF)/(geo times))
               Power@Size [~Q/h]
DBMS                            
DBS-BHT-8-1-1            8369.13

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                           time [s]  count   SF  Throughput@Size
DBMS        SF  num_experiment num_client                                       
DBS-BHT-8-1 3.0 1              1                 48      1  3.0           4950.0

### Workflow
                 orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
DBS-BHT-8-1-1  DBS-BHT-8-1  3.0     8               1           1       1770027664     1770027712

#### Actual
DBMS DBS-BHT-8 - Pods [[1]]

#### Planned
DBMS DBS-BHT-8 - Pods [[1]]

### Ingestion - Loader
             CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DBS-BHT-8-1        22.8        0           0.0                 0.28

### Execution - Benchmarker
             CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DBS-BHT-8-1        0.02        0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
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
```markdown
﻿## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 363s 
    Code: 1770027860
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['DatabaseService'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 1Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
DBS-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:95599
    datadisk:39
    volume_size:1.0G
    volume_used:36M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1770027860

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 DBS-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                          3271.95
Minimum Cost Supplier Query (TPC-H Q2)                     1022.68
Shipping Priority (TPC-H Q3)                               1492.51
Order Priority Checking Query (TPC-H Q4)                   1960.39
Local Supplier Volume (TPC-H Q5)                           1304.60
Forecasting Revenue Change (TPC-H Q6)                       711.05
Forecasting Revenue Change (TPC-H Q7)                      1279.19
National Market Share (TPC-H Q8)                            875.71
Product Type Profit Measure (TPC-H Q9)                     2158.35
Forecasting Revenue Change (TPC-H Q10)                     1576.68
Important Stock Identification (TPC-H Q11)                  333.58
Shipping Modes and Order Priority (TPC-H Q12)              1402.53
Customer Distribution (TPC-H Q13)                          4195.88
Forecasting Revenue Change (TPC-H Q14)                      774.27
Top Supplier Query (TPC-H Q15)                              797.79
Parts/Supplier Relationship (TPC-H Q16)                     709.22
Small-Quantity-Order Revenue (TPC-H Q17)                   3076.76
Large Volume Customer (TPC-H Q18)                         10399.91
Discounted Revenue (TPC-H Q19)                             1097.23
Potential Part Promotion (TPC-H Q20)                        572.90
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)        1518.35
Global Sales Opportunity Query (TPC-H Q22)                  269.54

### Loading [s]
               timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
DBS-BHT-8-1-1          24.0           52.0         1.0      267.0     348.0

### Geometric Mean of Medians of Timer Run [s]
               Geo Times [s]
DBMS                        
DBS-BHT-8-1-1           1.34

### Power@Size ((3600*SF)/(geo times))
               Power@Size [~Q/h]
DBMS                            
DBS-BHT-8-1-1            8410.41

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                           time [s]  count   SF  Throughput@Size
DBMS        SF  num_experiment num_client                                       
DBS-BHT-8-1 3.0 1              1                 47      1  3.0          5055.32

### Workflow
                 orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
DBS-BHT-8-1-1  DBS-BHT-8-1  3.0     8               1           1       1770028123     1770028170

#### Actual
DBMS DBS-BHT-8 - Pods [[1]]

#### Planned
DBMS DBS-BHT-8 - Pods [[1]]

### Execution - Benchmarker
             CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
DBS-BHT-8-1        11.0        0          0.27                 0.27

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```
