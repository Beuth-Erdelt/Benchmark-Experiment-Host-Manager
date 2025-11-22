# Example: Benchmark TiDB

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.
TiDB is a disaggregated DBMS.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

TiDB offers several installation methods, including an operator [1].
We here rely on a [manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-TiDB.yml) for a version that is suitable for bexhoma.
TiDB clusters consist of three core components: TiDB, PD (Placement Driver), and TiKV.
Unlike traditional databases, TiDB does not require a single coordinator node—PD handles cluster metadata management and scheduling.
In Bexhoma, TiDB pods are deployed as a Deployment, PD as a StatefulSet, and TiKV as another StatefulSet to ensure stable identities and persistent storage.
A Kubernetes Service exposes TiDB for external communication within the cluster, while headless Services enable internal discovery and communication between PD and TiKV pods.

This can be managed by bexhoma.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Get started with TiDB:  https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/
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
  -sfo 1 \
  -nw 3 \
  -nwr 3 \
  -nsr 3 \
  --workload a \
  -dbms TiDB \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_tidb_1.log &
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of TiDB (`-dbms`) with 3 workers (`-nw`), i.e., PD and TiKV, with 3 main pods (`-nsr`), i.e. TiDB, and replication factor 3 (`-nwr`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 1.000.000 rows (i.e., SF=10, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [1]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 1.000.000 operations (`-sfo`)
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
+-----------------+--------------+--------------+------------+-------------+
| 1761748555      | sut          |   loaded [s] | use case   | worker      |
+=================+==============+==============+============+=============+
| TiDB-64-8-16384 | (1. Running) |          409 | ycsb       | (3 Running) |
+-----------------+--------------+--------------+------------+-------------+
```

The code `1761748555` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1761748555` (removes everything that is related to experiment `1761748555`).

### Evaluate Results

At the end of a benchmark you will see a summary like

doc_ycsb_tidb_1.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1328s 
    Code: 1763836378
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.8.15.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['TiDB'].
    Import is handled by 8 processes (pods).
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
TiDB-64-8-16384-1 uses docker image pingcap/tidb:v7.1.0
    RAM:337974857728
    CPU:Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz
    Cores:32
    host:5.15.0-153-generic
    node:cl-worker17
    disk:1655758
    cpu_list:0-31
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    sut 0
        RAM:337974857728
        CPU:Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz
        Cores:32
        host:5.15.0-153-generic
        node:cl-worker17
        disk:1655758
        cpu_list:0-31
    sut 1
        RAM:1081649913856
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-60-generic
        node:cl-worker34
        disk:330662
        cpu_list:0-55
    sut 2
        RAM:811500781568
        CPU:Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz
        Cores:40
        host:6.8.0-1041-nvidia
        node:cl-worker19
        cpu_list:0-39
    worker 0
        RAM:337974857728
        CPU:Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz
        Cores:32
        host:5.15.0-153-generic
        node:cl-worker17
        disk:1655758
        cpu_list:0-31
    worker 1
        RAM:810205974528
        CPU:Intel(R) Xeon(R) Silver 4110 CPU @ 2.10GHz
        Cores:32
        host:6.8.0-60-generic
        node:cl-worker20
        disk:586951
        cpu_list:0-31
    worker 2
        RAM:811500781568
        CPU:Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz
        Cores:40
        host:6.8.0-1041-nvidia
        node:cl-worker19
        disk:1471831
        cpu_list:0-39
    store 0
        RAM:540579323904
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker22
        disk:424322
        cpu_list:0-127
    store 1
        RAM:1081965486080
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1401797
        cpu_list:0-255
    store 2
        RAM:540492984320
        CPU:Intel(R) Xeon(R) Gold 6430
        Cores:128
        host:6.8.0-60-generic
        node:cl-worker38
        disk:577961
        cpu_list:0-127
    eval_parameters
        code:1763836378
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                 experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
TiDB-64-8-16384               1       64   16384          8           0                   16216.200547                61742.0             1000000                             11574.0

### Execution
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
TiDB-64-8-16384-1               1       64   16384          1           0                        1933.25               517265.0            499761                            2277.0              500239                            135551.0

### Workflow

#### Actual
DBMS TiDB-64-8-16384 - Pods [[1]]

#### Planned
DBMS TiDB-64-8-16384 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      823.14    10.81          2.24                 3.01

### Loading phase: component worker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      118.83     1.08          0.31                 0.31

### Loading phase: component store
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      481.37     6.81          5.64                14.86

### Loading phase: component loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       99.53     0.63          0.25                 0.26

### Execution phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1     1044.64      5.4          1.84                 2.61

### Execution phase: component worker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      226.41     0.82          0.31                 0.31

### Execution phase: component store
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      811.38      2.8          8.79                22.63

### Execution phase: component benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      136.06     0.31          0.14                 0.14

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```

To see the summary again you can simply call `bexperiments summary -e 1761748555` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexperiments jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888




## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components of the same type.
In this example, this means that used memory, CPU time, etc. are summed across all nodes of the TiDB cluster for the components PD, TiKV and TiDB resp.

## Use Persistent Storage

**Persistent storage currently is not yet implemented.**


## YCSB Example Explained

### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'TiDB': {
    'loadData': 'mysql --local-infile -h 127.0.0.1 -P 4000 < {scriptname}',
    'delay_prepare': 60,
    'template': {
        'version': 'CE 8.0.22',
        'alias': 'General-C',
        'docker_alias': 'GP-C',
        'dialect': 'MySQL',
        'JDBC': {
            'driver': "com.mysql.cj.jdbc.Driver",
            'auth': ["root", "root"],
            'url': 'jdbc:mysql://{serverip}:9091/{dbname}',
            'jar': ['mysql-connector-j-8.0.31.jar', 'slf4j-simple-1.7.21.jar'],
            'database': 'test',
        }
    },
    'logfile': '/var/log/mysqld.log',
    'datadir': '/var/lib/mysql/',
    'priceperhourdollar': 0.0,
    'worker_port': 2379,
    'store_args': False,
},
```

where
* `loadData`: This command is used to create the schema
* `JDBC`: These infos are used to configure YCSB
* `worker_port`: This tells bexhoma what the port for internal communication is
* `store_args`: This tells bexhoma not to log args of the containers, since they do not contain parameters

TiDB uses the MySQL JDBC driver.



### Schema SQL File

If data should be loaded, bexhoma at first creates a schema according to: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/TiDB







## Benchbase's TPC-C

### Simple Run

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
TiDB has 3 workers (TiDB, PD and TiKV).

```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -nwr 3 \
  -nsr 3 \
  -dbms TiDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  run </dev/null &>$LOG_DIR/doc_benchbase_tidb_1.log &
```

### Evaluate Results

doc_benchbase_tidb_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1636s 
    Code: 1761920297
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.15.
    Experiment is limited to DBMS ['TiDB'].
    Import is handled by 1 processes (pods).
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
TiDB-1-1-1024-1 uses docker image pingcap/tidb:v7.1.0
    RAM:1077382864896
    CPU:AMD EPYC 7742 64-Core Processor
    Cores:256
    host:6.8.0-1025-nvidia
    node:cl-worker28
    disk:1323330
    cpu_list:0-255
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    sut 0
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1323494
        cpu_list:0-255
    sut 1
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:417096
        cpu_list:0-223
    sut 2
        RAM:1081742749696
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1306772
        cpu_list:0-127
    worker 0
        RAM:1081965486080
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1396020
        cpu_list:0-255
    worker 1
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1323330
        cpu_list:0-255
    worker 2
        RAM:540590792704
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-86-generic
        node:cl-worker24
        disk:156185
        cpu_list:0-95
    eval_parameters
                code:1761920297
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
TiDB-1-1-1024-2 uses docker image pingcap/tidb:v7.1.0
    RAM:1077382864896
    CPU:AMD EPYC 7742 64-Core Processor
    Cores:256
    host:6.8.0-1025-nvidia
    node:cl-worker28
    disk:1323599
    cpu_list:0-255
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    sut 0
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1323599
        cpu_list:0-255
    sut 1
        RAM:2164173279232
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-79-generic
        node:cl-worker36
        disk:415630
        cpu_list:0-223
    sut 2
        RAM:1081742749696
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-86-generic
        node:cl-worker29
        disk:1305743
        cpu_list:0-127
    worker 0
        RAM:1081965486080
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1075-nvidia
        node:cl-worker27
        disk:1394891
        cpu_list:0-255
    worker 1
        RAM:1077382864896
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1025-nvidia
        node:cl-worker28
        disk:1323599
        cpu_list:0-255
    worker 2
        RAM:540590792704
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-86-generic
        node:cl-worker24
        disk:156186
        cpu_list:0-95
    eval_parameters
                code:1761920297
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                   experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                               
TiDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    365.556564                 363.983231         0.0                                                      92467.0                                              43750.0
TiDB-1-1-1024-2-1               1          8    8192       2      1  300.0           0                    175.599983                 173.856649         0.0                                                     106076.0                                              45539.0
TiDB-1-1-1024-2-2               1          8    8192       2      2  300.0           0                    165.083325                 163.556659         0.0                                                     105602.0                                              48440.0

#### Aggregated Parallel
                 experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
TiDB-1-1-1024-1               1         16   16384          1  300.0           0                        365.56                     363.98         0.0                                                      92467.0                                              43750.0
TiDB-1-1-1024-2               1         16   16384          2  300.0           0                        340.68                     337.41         0.0                                                     106076.0                                              46989.5

### Workflow

#### Actual
DBMS TiDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS TiDB-1-1-1024 - Pods [[1, 2]]

### Loading
                 time_load  terminals  pods  Throughput [SF/h]
TiDB-1-1-1024-1      213.0        1.0   1.0         270.422535
TiDB-1-1-1024-2      213.0        1.0   2.0         270.422535

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```
