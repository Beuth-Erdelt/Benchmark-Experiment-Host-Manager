# Example: Application Metrics

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

In the following we demonstrate how to collect application metrics, that is, metrics of a DBMS.


## Perform Benchmark

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

## PostgreSQL

Example:
```bash
nohup python benchbase.py -m -mc -ma -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_postgresql_appmetrics.log &
```

This
* activates monitoring (`-m`) cluster-wide (`-mc`)
* starts a clean instance of PostgreSQL (`-dbms`)
  * with a sidecar container for monitoring (`-ma`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-sd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-tb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Evaluate Results


doc_benchbase_run_postgresql_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1274s 
    Code: 1758633612
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:440088376
    datadisk:4307
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758633612
PostgreSQL-1-1-1024-2 uses docker image postgres:17.5
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:440766148
    datadisk:4969
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758633612

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1        160   16384       1      1  300.0           3                   1969.699193                1951.909200         0.0                                                     279561.0                                              81186.0
PostgreSQL-1-1-1024-2-2               1         80    8192       2      1  300.0           1                    903.579693                 895.726362         0.0                                                     316165.0                                              88501.0
PostgreSQL-1-1-1024-2-1               1         80    8192       2      2  300.0           1                    903.306563                 895.543231         0.0                                                     316789.0                                              88526.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1        160   16384          1  300.0           3                       1969.70                    1951.91         0.0                                                     279561.0                                              81186.0
PostgreSQL-1-1-1024-2               1        160   16384          2  300.0           2                       1806.89                    1791.27         0.0                                                     316789.0                                              88513.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      304.0        1.0   1.0         189.473684
PostgreSQL-1-1-1024-2      304.0        1.0   2.0         189.473684

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       636.7     4.38          8.06                 9.67
PostgreSQL-1-1-1024-2       636.7     4.38          8.06                 9.67

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      930.28     5.64          0.26                 0.26
PostgreSQL-1-1-1024-2      930.28     5.64          0.26                 0.26

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     2563.32     8.96         10.23                12.45
PostgreSQL-1-1-1024-2     2113.64     8.20         10.81                13.49

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1129.76     4.67          1.17                 1.17
PostgreSQL-1-1-1024-2     1129.76     6.64          1.17                 1.17

### Application Metrics
                       Active Backends Waiting on I/O  Active Backends Waiting on WAL  Active Backends Waiting on Locks  Max Transaction Duration (I/O Wait)  Max Transaction Duration (WAL Wait)
PostgreSQL-1-1-1024-1                             2.0                            42.0                             123.0                                 0.15                                 1.23
PostgreSQL-1-1-1024-2                             1.0                            48.0                             124.0                                 0.27                                 0.94

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

The summary shows the first 5 application metrics aggregated per execution run.
An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/dev).


## MySQL

Example:
```bash
nohup python benchbase.py -m -mc -ma -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms MySQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_mysql_appmetrics.log &
```

This
* activates monitoring (`-m`) cluster-wide (`-mc`)
* starts a clean instance of MySQL (`-dbms`)
  * with a sidecar container for monitoring (`-ma`)
  * data directory inside a Docker container
* starts 1 loader pod (per DBMS) that
  * creates TPC-C schema in the database
  * imports data for 16 (`-sf`) warehouses into the DBMS
  * using all threads of driver machine (benchbase setting)
* runs streams of TPC-C queries (per DBMS)
    * running for 5 (`-sd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-tb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary


### Evaluate Results

doc_benchbase_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1330s 
    Code: 1758634933
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.12.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-1-1-1024-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:442875080
    datadisk:7028
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1758634933
MySQL-1-1-1024-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:445062304
    datadisk:9164
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1758634933

### Execution

#### Per Pod
                    experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                
MySQL-1-1-1024-1-1               1        160   16384       1      1  300.0           0                   1171.889856                1146.926526         0.0                                                     663149.0                                             136404.0
MySQL-1-1-1024-2-1               1         80    8192       2      1  300.0           0                    619.296595                 606.789929         0.0                                                     730746.0                                             129150.0
MySQL-1-1-1024-2-2               1         80    8192       2      2  300.0           0                    618.576540                 606.673209         0.0                                                     730075.0                                             129302.0

#### Aggregated Parallel
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1        160   16384          1  300.0           0                       1171.89                    1146.93         0.0                                                     663149.0                                             136404.0
MySQL-1-1-1024-2               1        160   16384          2  300.0           0                       1237.87                    1213.46         0.0                                                     730746.0                                             129226.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1, 2]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1      355.0        1.0   1.0         162.253521
MySQL-1-1-1024-2      355.0        1.0   2.0         162.253521

### Ingestion - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1188.23     5.81          5.85                 9.31
MySQL-1-1-1024-2     1188.23     5.81          5.85                 9.31

### Ingestion - Loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1670.37     9.49          0.48                 0.48
MySQL-1-1-1024-2     1670.37     9.49          0.48                 0.48

### Execution - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     2224.78     9.78          6.37                11.99
MySQL-1-1-1024-2     3031.34    10.50          6.80                15.40

### Execution - Benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1247.45     5.46          1.16                 1.16
MySQL-1-1-1024-2     1247.45    10.74          1.16                 1.16

### Application Metrics
                  InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-1-1-1024-1                           1.0                  27807.47                    0.11               0.56                    0.0
MySQL-1-1-1024-2                           0.0                  29977.77                    0.11               0.55                    0.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

The summary shows the first 5 application metrics aggregated per execution run.
An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/dev).

