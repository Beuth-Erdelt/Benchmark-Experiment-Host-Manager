# Example: Benchmark Citus

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Citus is a PostgreSQL extension, that introduces sharding [1].
A cluster has an instance of PostgreSQL with Citus as a coordinator (here called master, managed by a Kubernetes deployment).
More instances can register at the master as worker nodes (here managed by Kubernetes stateful sets).

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Citus: https://www.citusdata.com/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
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
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Citus \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_citus_1.log &
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of Citus (`-dbms`) with 3 workers (`-nw`)
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
+------------------+--------------+------------+-------------+
| 1741884177       | sut          | use case   | worker      |
+==================+==============+============+=============+
| Citus-64-8-65536 | (1. Running) | ycsb       | (3 Running) |
+------------------+--------------+------------+-------------+
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
    Duration: 547s 
    Code: 1741943211
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker13.
    Benchmarking is fixed to cl-worker13.
    SUT is fixed to cl-worker20.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Citus-64-8-65536-1 uses docker image citusdata/citus:13.0.2-alpine
    RAM:810204672000
    CPU:Intel(R) Xeon(R) Silver 4110 CPU @ 2.10GHz
    Cores:32
    host:5.15.0-126-generic
    node:cl-worker20
    disk:476257712
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081650974720
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:5.15.0-133-generic
        node:cl-worker34
        disk:138983112
    worker 1
        RAM:540595875840
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-126-generic
        node:cl-worker25
        disk:384079056
    worker 2
        RAM:540595888128
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:5.15.0-127-generic
        node:cl-worker24
        disk:158990540

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Citus-64-8-65536               1       64   65536          8           0                   31406.745886                32286.0             1000000                              3408.5

### Execution
                    experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Citus-64-8-65536-1               1       64   65536          1           0                       42070.72               237695.0           4998591                            1961.0             5001409                              6347.0

### Workflow

#### Actual
DBMS Citus-64-8-65536 - Pods [[1]]

#### Planned
DBMS Citus-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1      527.67     3.17          1.11                 2.87

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1      146.39        0          4.36                 4.42

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1     7360.49    21.31          2.95                 6.04

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-64-8-65536-1       904.4     7.09          0.62                 0.63

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




## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the Citus cluster.


## Use Persistent Storage

To be described: Persistent storage is per experiment here, because K8s statefulsets derive their pvc names directly from pod names.

## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```
'Citus': {
    'loadData': 'psql -U postgres < {scriptname}',
    'attachWorker': "psql -U postgres --command=\"SELECT * from master_add_node('{worker}.{service_sut}', 5432);\"",
    'template': {
        'version': '10.0.2',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
         'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", "password1234"],
            'url': 'jdbc:postgresql://{serverip}:9091/postgres',#/{dbname}',
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


Citus uses the PostgreSQL JDBC driver.



### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Citus









## Benchbase's TPC-C

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
Citus has 3 workers.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -dbms Citus \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_1.log &
```

### Evaluate Results

```bash
## Show Summary
```

### Benchbase More Complex

TPC-C is performed at 128 warehouses.
The 64 threads of the client are split into a cascading sequence of 1,2,4 and 8 pods.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 60 \
  -nw 3 \
  -dbms Citus \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_2.log &
```

### Evaluate Results

```bash
## Show Summary
```


## Benchbase Example Explained

The setup is the same as for YCSB (see above).

