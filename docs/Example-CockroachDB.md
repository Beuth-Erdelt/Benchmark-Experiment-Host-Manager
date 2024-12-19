# Example: Benchmark CockroachDB

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

CockroachDB offers several installation methods [1].
We here rely on *CockroachDB insecure test cluster in a single Kubernetes cluster* [2].
The benefit of this approach is we can use a [manifest](https://github.com/cockroachdb/cockroach/blob/master/cloud/kubernetes/cockroachdb-statefulset.yaml) for a stateful set provided by CockroachDB.
See [dummy deployment](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-CockroachDB.yml) for a version that is suitable for bexhoma.

This can be managed by bexhoma.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Install CockroachDB:  https://www.cockroachlabs.com/docs/v24.2/install-cockroachdb-linux.html
1. Deploy CockroachDB in a Single Kubernetes Cluster (Insecure): https://www.cockroachlabs.com/docs/v24.2/deploy-cockroachdb-with-kubernetes-insecure
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
  -dbms CockroachDB \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_1.log &
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of CockroachDB (`-dbms`) with 3 workers (`-nw`)
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
+------------------------+--------------+--------------+------------+---------------+
| 1730133803             | sut          |   loaded [s] | use case   | benchmarker   |
+========================+==============+==============+============+===============+
| CockroachDB-64-8-65536 | (1. Running) |           41 | ycsb       | (1. Running)  |
+------------------------+--------------+--------------+------------+---------------+
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
    Duration: 1055s 
    Code: 1734604175
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'. Number of rows to insert is 1000000. Number of operations is 10000000. Batch size is ''.
    YCSB is performed using several threads and processes. Target is based on multiples of '16384'. Factors for loading are [4]. Factors for benchmarking are [4].
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-64-8-65536-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008576512
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249207160
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081965555712
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker27
        disk:560813152
        datadisk:116276744
        volume_size:1000G
        volume_used:109G
    worker 1
        RAM:1081966526464
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker28
        disk:442719496
        datadisk:116066508
        volume_size:1000G
        volume_used:109G
    worker 2
        RAM:1081751019520
        Cores:128
        host:5.15.0-126-generic
        node:cl-worker29
        disk:153230928
        datadisk:116065692
        volume_size:1000G
        volume_used:109G

### Loading
                        experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8                   17071.978081                58791.0             1000000                              7190.0

### Execution
                          experiment_run  threads  target  pod_count  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1               1       64   65536          1                       14391.04               694877.0           5000111                            5691.0             4999889                            126207.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1]]

### Ingestion - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1     1295.39     6.78          3.68                 6.88

### Ingestion - Loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1       22.52     0.41          0.58                 0.59

### Execution - SUT
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1    21640.62    21.35         12.76                28.74

### Execution - Benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1     1181.64     1.78           0.6                 0.61

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
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the CockroachDB cluster.


## Use Persistent Storage

To be described: Persistent storage is per experiment here, because K8s statefulsets derive their pvc names directly from pod names.

## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```
'CockroachDB': {
    'loadData': 'cockroach sql --host {service_name} --port 9091 --insecure --file {scriptname}',
    'delay_prepare': 120,
    'template': {
        'version': 'v24.2.4',
        'alias': 'Cloud-Native-2',
        'docker_alias': 'CN2',
         'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["root", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/defaultdb?reWriteBatchedInserts=true',
            'jar': 'postgresql-42.5.0.jar'
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/cockroach/cockroach-data',
    'priceperhourdollar': 0.0,
},
```

where
* `loadData`: This command is used to create the schema
* `JDBC`: These infos are used to configure YCSB


CockroachDB uses the PostgreSQL JDBC driver.



### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/CockroachDB









## Benchbase's TPC-C

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
CockroachDB has 3 workers.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -dbms CockroachDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_1.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
Benchbase Workload SF=16 (warehouses for TPC-C)
    Type: benchbase
    Duration: 1047s 
    Code: 1734624013
    Benchbase runs the benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Benchmark is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008576512
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249214372
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081966526464
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker28
        disk:439691956
        datadisk:116318604
        volume_size:1000G
        volume_used:109G
    worker 1
        RAM:1081751019520
        Cores:128
        host:5.15.0-126-generic
        node:cl-worker29
        disk:153273172
        datadisk:116107360
        volume_size:1000G
        volume_used:109G
    worker 2
        RAM:1081965555712
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker27
        disk:584549888
        datadisk:116107116
        volume_size:1000G
        volume_used:109G
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008576512
    Cores:64
    host:5.15.0-126-generic
    node:cl-worker11
    disk:249214372
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:1081966526464
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker28
        disk:439986660
        datadisk:116611832
        volume_size:1000G
        volume_used:109G
    worker 1
        RAM:1081751019520
        Cores:128
        host:5.15.0-126-generic
        node:cl-worker29
        disk:153570092
        datadisk:116404276
        volume_size:1000G
        volume_used:109G
    worker 2
        RAM:1081965555712
        Cores:256
        host:5.15.0-1067-nvidia
        node:cl-worker27
        disk:584845212
        datadisk:116401204
        volume_size:1000G
        volume_used:109G

### Execution
                        experiment_run  terminals  target  pod_count   time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         16   16384          1  300.0                        481.72                                                      84008.0                                              33199.0
CockroachDB-1-1-1024-2               1         16   16384          2  300.0                        448.16                                                      95345.0                                              35721.0

Warehouses: 16

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
CockroachDB-1-1-1024-1      142.0        1.0   1.0                 405.633803
CockroachDB-1-1-1024-2      142.0        1.0   2.0                 405.633803

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```

### Benchbase More Complex

TPC-C is performed at 128 warehouses.
The 64 threads of the client are split into a cascading sequence of 1,2,4 and 8 pods.

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 60 \
  -nw 3 \
  -dbms CockroachDB \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_2.log &
```

### Evaluate Results

```bash
## Show Summary

### Workload
Benchbase Workload SF=128 (warehouses for TPC-C)
    Type: benchbase
    Duration: 15418s 
    Code: 1730374413
    This includes no queries. Benchbase runs the benchmark
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor (e.g., number of warehouses) is 128. Benchmarking runs for 60 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [16].
    Benchmark is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1, 2, 4, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254912048
    requests_cpu:4
    requests_memory:16Gi
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254912216
    requests_cpu:4
    requests_memory:16Gi
CockroachDB-1-1-1024-3 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254912388
    requests_cpu:4
    requests_memory:16Gi
CockroachDB-1-1-1024-4 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008605184
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:254912556
    requests_cpu:4
    requests_memory:16Gi

### Execution
                        experiment_run  terminals  target  pod_count    time  Throughput (requests/second)  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         64   16384          1  3600.0                        696.70                                                     233544.0                                             91853.00
CockroachDB-1-1-1024-2               1         64   16384          2  3600.0                        653.01                                                     247449.0                                             97998.00
CockroachDB-1-1-1024-3               1         64   16384          4  3600.0                        599.12                                                     258276.0                                            106813.50
CockroachDB-1-1-1024-4               1         64   16384          8  3600.0                        538.01                                                     262975.0                                            118944.88

Warehouses: 128

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[8, 4, 2, 1]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2, 4, 8]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
CockroachDB-1-1-1024-1      531.0        1.0   1.0                  867.79661
CockroachDB-1-1-1024-2      531.0        1.0   2.0                  867.79661
CockroachDB-1-1-1024-3      531.0        1.0   4.0                  867.79661
CockroachDB-1-1-1024-4      531.0        1.0   8.0                  867.79661

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


## Benchbase Example Explained

The setup is the same as for YCSB (see above).

