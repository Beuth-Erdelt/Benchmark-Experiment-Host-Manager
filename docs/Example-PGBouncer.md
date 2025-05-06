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
      * 10.000.000 operations (`-sfo`)
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

```
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

```bash
## Show Summary

### Workload
YCSB SF=16
    Type: ycsb
    Duration: 1593s
    Code: 1745062608
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'C'.
    Number of rows to insert is 16000000.
    Number of operations is 16000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [11].
    Factors for benchmarking are [11].
    Experiment uses bexhoma version 0.8.4.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PGBouncer'].
    Import is handled by 16 processes (pods).
    Loading is fixed to cl-worker13.
    Benchmarking is fixed to cl-worker13.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [16] pods.
    Benchmarking is tested with [128] threads, split into [16] pods.
    Pooling is done with [4] pods having [128] inbound and [64] outbound connections in total.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
pgb-64-4-128-64-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:241554848
    datadisk:38276
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1745062608

### Loading
                 experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
pgb-64-4-128-64               1       64  180224         16           0                   28817.563319               568643.0            16000000                             5900.75

### Execution
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)
pgb-64-4-128-64-1               1      128  180224         16          20                       76904.14               198420.0          14750000                            2497.0

### Workflow

#### Actual
DBMS pgb-64-4-128-64 - Pods [[16]]

#### Planned
DBMS pgb-64-4-128-64 - Pods [[16]]

### Ingestion - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     2788.21     5.49         23.38                32.23

### Ingestion - Loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     1988.22     1.28          0.58                 0.58

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     2082.37    14.23         25.64                35.87

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     1404.68     2.76          0.57                 0.58

### Execution - Pooling
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1      596.15      1.0          0.01                 0.01

### Ingestion - Pooling
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1      735.21     0.81          0.01                 0.01

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
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


```
+----------------------------------------------+-----------------+--------------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                      | configuration   | experiment         | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+==============================================+=================+====================+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-postgresql-ycsb-16           | postgresql      | ycsb-16            | True         |               734 | PGBouncer       | shared               | 100Gi     | Bound    | 100G   | 38G    |
+----------------------------------------------+-----------------+--------------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
```

The result looks something like


```bash
## Show Summary

### Workload
YCSB SF=16
    Type: ycsb
    Duration: 2537s
    Code: 1745066294
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'C'.
    Number of rows to insert is 16000000.
    Number of operations is 16000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [11].
    Factors for benchmarking are [11].
    Experiment uses bexhoma version 0.8.4.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PGBouncer'].
    Import is handled by 16 processes (pods).
    Loading is fixed to cl-worker13.
    Benchmarking is fixed to cl-worker13.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [64] threads, split into [16] pods.
    Benchmarking is tested with [128] threads, split into [16] pods.
    Pooling is done with [4] pods having [128] inbound and [64] outbound connections in total.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
pgb-64-4-128-64-1-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202361324
    datadisk:38277
    volume_size:100G
    volume_used:38G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1745066294
pgb-64-4-128-64-2-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:202361316
    datadisk:38216
    volume_size:100G
    volume_used:38G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1745066294

### Loading
                 experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
pgb-64-4-128-64               1       64  180224         16           0                   22943.376844               725185.0            16000000                             6951.25

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)
pgb-64-4-128-64-1-1               1      128  180224         16          16                       80318.76               189995.0          15000000                            2553.0
pgb-64-4-128-64-2-1               2      128  180224         16          14                       72783.33               214992.0          15125000                            2955.0

### Workflow

#### Actual
DBMS pgb-64-4-128-64 - Pods [[16], [16]]

#### Planned
DBMS pgb-64-4-128-64 - Pods [[16], [16]]

### Ingestion - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1     2790.74     3.89         23.14                41.46

### Ingestion - Loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1     1991.34     1.69          0.58                 0.58

### Execution - SUT
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1     2160.26    10.41         25.45                43.77
pgb-64-4-128-64-2-1     2155.42    13.67         24.13                42.65

### Execution - Benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1     1365.00     2.21          0.57                 0.58
pgb-64-4-128-64-2-1     1384.65     3.59          0.57                 0.57

### Execution - Pooling
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1      596.37      1.0          0.01                 0.01
pgb-64-4-128-64-2-1      590.51      2.0          0.01                 0.01

### Ingestion - Pooling
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1-1      747.22     0.64          0.01                 0.01

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```
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
  -sd 5 \
  -xconn \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_newconn.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1181s 
    Code: 1745302456
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.4.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:206799668
    datadisk:4324
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1745302456
PostgreSQL-1-1-1024-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:207525888
    datadisk:5033
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1745302456

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16   16384          1  300.0           0                        803.23                     468.27         0.0                                                      35400.0                                              19912.0
PostgreSQL-1-1-1024-2               1         16   16384          2  300.0           0                        657.23                     653.14         0.0                                                      38464.0                                              24330.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      169.0        1.0   1.0         340.828402
PostgreSQL-1-1-1024-2      169.0        1.0   2.0         340.828402

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
  -sd 5 \
  -xconn \
  -dbms PGBouncer \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -npp 2 \
  -npi 32 \
  -npo 32 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_newconn_pool.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1997s 
    Code: 1745330708
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Experiment uses bexhoma version 0.8.4.
    Benchmark is limited to DBMS ['PGBouncer'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Pooling is done with [2] pods having [32] inbound and [32] outbound connections in total.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
pgb-1-2-32-32-1 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:206800728
    datadisk:4323
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1745330708
pgb-1-2-32-32-2 uses docker image postgres:16.1
    RAM:541008592896
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-134-generic
    node:cl-worker11
    disk:207458900
    datadisk:4966
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1745330708

### Execution
                 experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
pgb-1-2-32-32-1               1         16   16384          1  300.0           0                        936.98                     468.51         0.0                                                      35352.0                                              17069.0
pgb-1-2-32-32-2               1         16   16384          2  300.0           2                        766.86                     760.68         0.0                                                      41835.0                                              20850.0

### Workflow

#### Actual
DBMS pgb-1-2-32-32 - Pods [[2, 1]]

#### Planned
DBMS pgb-1-2-32-32 - Pods [[1, 2]]

### Loading
                 time_load  terminals  pods  Throughput [SF/h]
pgb-1-2-32-32-1      148.0        1.0   1.0         389.189189
pgb-1-2-32-32-2      148.0        1.0   2.0         389.189189

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

