# Example: Benchmark PGBouncer

This differs from the default behaviour of bexhoma, since we benchmark a DBMS **with a pooling component, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

**PgBouncer** [1] is a lightweight and high-performance connection pooler for PostgreSQL. It manages and reuses database connections to reduce the overhead of frequent connection creation, which is especially useful for applications with high concurrency or short-lived queries. By sitting between your application and the PostgreSQL server, PgBouncer helps improve scalability, reduce resource usage, and optimize connection handling.
We use the Docker image provided by [2].

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. PGBouncer: https://www.pgbouncer.org/
1. PGBouncer Docker Container: https://hub.docker.com/r/edoburu/pgbouncer/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
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
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 16 \
  -nlt 64 \
  -nlf 11 \
  -nbp 16 \
  -nbt 128 \
  -nbf 11 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -npp 4 \
  -npi 128 \
  -npo 64 \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_1.log &
```

This
* loops over `n` in [16] and `t` in [11]
  * starts a clean instance of PostgreSQL with PGBouncer (`-dbms`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 16.000.000 rows (i.e., SF=16, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [16] and `s` in [11]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 16.000.000 operations (`-sfo`)
      * workload C = 100% (`--workload`)
      * target throughput is `s` * 16384
      * threads = 64/`m` (`-nbt`)
      * PGBouncer has 4 instances (`-npp`) with 128 inbound connections (`-npi`) and 64 outbound connections (`-npo`)
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
+-----------------+--------------+--------------+------------+-------------+--------------+
| 1745062608      | sut          |   loaded [s] | use case   | pool        | loading      |
+=================+==============+==============+============+=============+==============+
| pgb-64-4-128-64 | (1. Running) |            3 | ycsb       | 4 (Running) | (16 Running) |
+-----------------+--------------+--------------+------------+-------------+--------------+
```

The code `1745062608` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1745062608` (removes everything that is related to experiment `1745062608`).

### Evaluate Results

At the end of a benchmark you will see a summary like

test_ycsb_testcase_pgbouncer_1.log
```markdown
﻿## Show Summary

### Workload
YCSB SF=16
    Type: ycsb
    Duration: 1470s 
    Code: 1771183694
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'C'.
    Number of rows to insert is 16000000.
    Ordering of inserts is hashed.
    Number of operations is 16000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [11].
    Factors for benchmarking are [11].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PGBouncer'].
    Import is handled by 16 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [16] pods.
    Benchmarking is tested with [128] threads, split into [16] pods.
    Pooling is done with [4] pods having [128] inbound and [64] outbound connections in total.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
pgb-64-4-128-64-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:135805
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1771183694

### Loading
                 experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
pgb-64-4-128-64               1       64  180224         16           0                   29107.128865               557479.0            16000000                             5426.25

### Execution
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)
pgb-64-4-128-64-1               1      128  180224         16           0                       64661.11               258627.0          16000000                            2493.0

### Workflow

#### Actual
DBMS pgb-64-4-128-64 - Pods [[16]]

#### Planned
DBMS pgb-64-4-128-64 - Pods [[16]]

### Monitoring

### Loading phase: component pool
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1      805.59     1.95          0.02                 0.02

### Loading phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     3540.96     8.19         23.98                42.24

### Loading phase: component loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     1262.92     3.51          0.11                 0.11

### Execution phase: component pool
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1      666.65     3.99          0.01                 0.01

### Execution phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     2540.27    16.57          26.7                44.96

### Execution phase: component benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     1116.08     6.72          0.11                 0.11

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component pool contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```

To see the summary again you can simply call `bexperiments summary -e 1745062608` with the experiment code.

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
In this example, this means that used memory, CPU time, etc. are summed across all 4 pods of PGBouncer.


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 16 \
  -nlt 64 \
  -nlf 11 \
  -nbp 16 \
  -nbt 128 \
  -nbf 11 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -npp 4 \
  -npi 128 \
  -npo 64 \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_2.log &
```
The following status shows we have one volume of type `shared`.
Every PGBouncer experiment (and every PostgreSQL experiment) will take the database from this volume and skip loading.
This makes the database persistent.
PGBouncer itself is stateless.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of the experiment mounts the volume and generates the data.
All other instances just use the database without generating and loading data.


```bash
+----------------------------------------------+-----------------+--------------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                      | configuration   | experiment         | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+==============================================+=================+====================+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-postgresql-ycsb-16           | postgresql      | ycsb-16            | True         |               734 | PGBouncer       | shared               | 100Gi     | Bound    | 100G   | 38G    |
+----------------------------------------------+-----------------+--------------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

test_ycsb_testcase_pgbouncer_2.log
```markdown
﻿## Show Summary

### Workload
YCSB SF=16
    Type: ycsb
    Duration: 2104s 
    Code: 1771188775
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'C'.
    Number of rows to insert is 16000000.
    Ordering of inserts is hashed.
    Number of operations is 16000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [11].
    Factors for benchmarking are [11].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PGBouncer'].
    Import is handled by 16 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 100Gi. Persistent storage is removed at experiment start.
    Loading is tested with [64] threads, split into [16] pods.
    Benchmarking is tested with [128] threads, split into [16] pods.
    Pooling is done with [4] pods having [128] inbound and [64] outbound connections in total.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
pgb-64-4-128-64-1-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97597
    volume_size:100G
    volume_used:38G
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1771188775
pgb-64-4-128-64-2-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:97597
    volume_size:100G
    volume_used:38G
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1771188775

### Loading
                 experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
pgb-64-4-128-64               1       64  180224         16           0                   23425.458887               688318.0            16000000                              7603.5

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)
pgb-64-4-128-64-1-1               1      128  180224         16           0                       74311.62               219972.0          16000000                            2719.0
pgb-64-4-128-64-2-1               2      128  180224         16           0                       47501.63               338075.0          16000000                            3455.0

### Workflow

#### Actual
DBMS pgb-64-4-128-64 - Pods [[16], [16]]

#### Planned
DBMS pgb-64-4-128-64 - Pods [[16], [16]]

### Monitoring

### Loading phase: component pool
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1      795.64     1.35          0.02                 0.02

### Loading phase: SUT deployment
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1     3662.34     6.39         23.56                41.88

### Loading phase: component loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1     1299.14     3.47          0.11                 0.11

### Execution phase: component pool
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1      688.22      4.0          0.01                 0.01
pgb-64-4-128-64-2-1     1508.65      4.0          0.02                 0.02

### Execution phase: SUT deployment
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1     2207.89    15.77         26.21                44.47
pgb-64-4-128-64-2-1     6885.48    13.56         24.90                43.35

### Execution phase: component benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1     1057.32     7.03          0.11                 0.11
pgb-64-4-128-64-2-1     1028.40     5.16          0.11                 0.11

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component pool contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```


## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'PGBouncer': {
    'loadData': 'psql -U postgres < {scriptname}',
    'template': {
        'version': 'v11.4',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
         'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/postgres?reWriteBatchedInserts=true',
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




### Schema SQL File

Before ingestion, we run a script to create and distribute the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/PostgreSQL/initschema-ycsb.sql

After ingestion, we run a script to check the distributions.
The script also vacuums and analyzes the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/ycsb/PostgreSQL/checkschema-ycsb.sql





## Benchbase's TPC-C


Benchbase allows to activate new-connection-per-transaction [1].
The default value is "false" [2].
When activated, after each transaction the connections is closed [3].
A new connection will be opened right before the next transaction.
This behavior can be expected to affect throughput and latency.
It can also be expected that a connection pooler like PGBouncer will help here.

1. Example: https://illuminatedcomputing.com/posts/2024/08/benchbase-documentation/
1. Default value: https://github.com/cmu-db/benchbase/blob/main/src/main/java/com/oltpbenchmark/DBWorkload.java#L143
1. Implementation: https://github.com/cmu-db/benchbase/blob/main/src/main/java/com/oltpbenchmark/api/Worker.java

### Benchbase Reconnect

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
We activate the new-connection-per-transaction feature with `-xconn`.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 10 \
  -xconn \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_newconn.log &
```

### Evaluate Results

doc_benchbase_testcase_newconn.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1834s 
    Code: 1771190951
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. There is a reconnect for each transaction. Benchmarking runs for 10 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:101903
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1771190951
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:102298
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1771190951
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1         32   16384       1      1  600.0           1                    979.664848                 446.781597         0.0                                                      59857.0                                              32658.0
PostgreSQL-1-1-1024-2-1               1         16    8192       2      1  600.0           0                    343.501649                 341.168316         0.0                                                      75400.0                                              46568.0
PostgreSQL-1-1-1024-2-2               1         16    8192       2      2  600.0           0                    343.338302                 341.019969         0.0                                                      75351.0                                              46592.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         32   16384          1  600.0           1                        979.66                     446.78         0.0                                                      59857.0                                              32658.0
PostgreSQL-1-1-1024-2               1         32   16384          2  600.0           0                        686.84                     682.19         0.0                                                      75400.0                                              46580.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      241.0        1.0   1.0         239.004149
PostgreSQL-1-1-1024-2      241.0        1.0   2.0         239.004149

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### Benchbase Reconnect via Pool

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
We activate the new-connection-per-transaction feature.
This time there will be a connection pool of size 32, handled by 2 pods of PGBouncer.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 10 \
  -xconn \
  -dbms PGBouncer \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -npp 2 \
  -npi 32 \
  -npo 32 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_newconn_pool.log &
```

### Evaluate Results

doc_benchbase_testcase_newconn_pool.log
```markdown
﻿## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1774s 
    Code: 1771192792
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. There is a reconnect for each transaction. Benchmarking runs for 10 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['PGBouncer'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [32] threads, split into [1, 2] pods.
    Pooling is done with [2] pods having [32] inbound and [32] outbound connections in total.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
pgb-1-2-32-32-1 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:101904
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1771192792
pgb-1-2-32-32-2 uses docker image postgres:17.5
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:102180
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1771192792

### Execution

#### Per Pod
                   experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                               
pgb-1-2-32-32-1-1               1         32   16384       1      1  600.0           2                   1403.251649                 466.909994         0.0                                                      42529.0                                              22800.0
pgb-1-2-32-32-2-1               1         16    8192       2      1  600.0           0                    578.534909                 443.496597         0.0                                                      53670.0                                              27649.0
pgb-1-2-32-32-2-2               1         16    8192       2      2  600.0           0                    580.254926                 443.414943         0.0                                                      53809.0                                              27567.0

#### Aggregated Parallel
                 experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
pgb-1-2-32-32-1               1         32   16384          1  600.0           2                       1403.25                     466.91         0.0                                                      42529.0                                              22800.0
pgb-1-2-32-32-2               1         32   16384          2  600.0           0                       1158.79                     886.91         0.0                                                      53809.0                                              27608.0

### Workflow

#### Actual
DBMS pgb-1-2-32-32 - Pods [[1, 2]]

#### Planned
DBMS pgb-1-2-32-32 - Pods [[1, 2]]

### Loading
                 time_load  terminals  pods  Throughput [SF/h]
pgb-1-2-32-32-1      172.0        1.0   1.0         334.883721
pgb-1-2-32-32-2      172.0        1.0   2.0         334.883721

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```



