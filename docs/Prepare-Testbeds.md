# Prepare Testbeds

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

A workflow consists of several parts.

1. A DBMS (system under test) is started.
1. Monitoring is started.
1. A loading phase runs.
1. A benchmarking phase runs.
1. Collected measurements are evaluated.
1. All components are removed from the cluster.

The following shows how to call the individual phases.
**This is usually not necessary. Generally, you want all phases to run.**
For debugging, to extend the implementation, or for traceability, it can be helpful to stop the process earlier.
All of the following examples do not remove the DBMS from the cluster, they keep the DBMS running after experiment has finished.
The evaluation includes a "Services" section that shows how to connect to the DBMS.


You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

## YCSB

You can watch for all components of these experiments by

```bash
kubectl get all -l app=bexhoma,usecase=ycsb
```

You can remove all components of these experiments by

```bash
kubectl delete all -l app=bexhoma,usecase=ycsb
```

### Start DBMS

```bash
nohup python ycsb.py -ms 1 -tr \
  --dbms PostgreSQL \
  --workload c \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start </dev/null &>$LOG_DIR/test_ycsb_start_postgresql.log &
```

test_ycsb_start_postgresql.log
```markdown
## Show Summary

### Workload
YCSB Start DBMS
    Type: ycsb
    Duration: 185s 
    Code: 1749627467
    Intro: Start DBMS and do not load data.
    This just starts a SUT.
    Workload is 'C'.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-1-1-16384
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-1-1-16384-1749627467 9091:9091

### Connections
PostgreSQL-1-1-16384-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387183600
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749627467

### Tests
TEST passed: Result contains no FAILED column
```


### Start DBMS and Load Data

```bash
nohup python ycsb.py -ms 1 -tr \
  --dbms PostgreSQL \
  --workload c \
  -m -mc \
  -nlp 8 -nlt 64 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load </dev/null &>$LOG_DIR/test_ycsb_load_postgresql.log &
```

test_ycsb_load_postgresql.log
```markdown
## Show Summary

### Workload
YCSB Data Loading SF=1
    Type: ycsb
    Duration: 329s 
    Code: 1749627711
    Intro: YCSB driver runs the experiment.
    This imports YCSB data sets.
    Workload is 'C'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Target is based on multiples of '16384'.
    Factors for loading are [1].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Experiment is run once.

### Services
PostgreSQL-64-8-16384
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-64-8-16384-1749627711 9091:9091

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:389594652
    datadisk:2393
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749627711

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-16384               1       64   16384          8           0                   16319.503604                61292.0             1000000                            1176.125

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      168.17     2.84          3.87                 4.73

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1       50.89        0          3.39                 3.42

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Result contains no FAILED column
```


### Start DBMS and Load Data and Run Workload

```bash
nohup python ycsb.py -ms 1 -tr \
  --dbms PostgreSQL \
  --workload c \
  -m -mc \
  -nlp 8 -nlt 64 -nbp 8 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_ycsb_run_postgresql.log &
```

test_ycsb_run_postgresql.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 444s 
    Code: 1749628094
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'C'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Services
PostgreSQL-64-8-16384
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-64-8-16384-1749628094 9091:9091

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:389579728
    datadisk:2393
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749628094

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-16384               1       64   16384          8           0                   16317.972165                61290.0             1000000                             1014.25

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)
PostgreSQL-64-8-16384-1               1       64   16384          8           0                       16317.77                61311.0           1000000                             466.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-16384 - Pods [[8]]

#### Planned
DBMS PostgreSQL-64-8-16384 - Pods [[8]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      124.99        0          3.53                 4.14

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      119.93     1.17          4.54                 4.56

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1       79.08        0          3.79                 4.71

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1       84.38        0          1.88                  1.9

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```


## Benchbase

You can watch for all components of these experiments by

```bash
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
```

You can remove all components of these experiments by

```bash
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc
```

### Start DBMS

```bash
nohup python benchbase.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start </dev/null &>$LOG_DIR/test_benchbase_start_postgresql.log &
```

test_benchbase_start_postgresql.log
```markdown
## Show Summary

### Workload
Benchbase Start DBMS
    Type: benchbase
    Duration: 187s 
    Code: 1749628596
    Intro: Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-1-1-1024
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-1-1-1024-1749628596 9091:9091

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387168592
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749628596

### Tests
```


### Start DBMS and Load Data

```bash
nohup python benchbase.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 8 -nlt 64 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load </dev/null &>$LOG_DIR/test_benchbase_load_postgresql.log &
```

test_benchbase_load_postgresql.log
```markdown
## Show Summary

### Workload
Benchbase Data tpcc Loading SF=1
    Type: benchbase
    Duration: 325s 
    Code: 1749628840
    Intro: Benchbase runs a TPC-C experiment.
    This imports a Benchbase data set.
    Benchbase data is generated and loaded using several threads. Scaling factor is 1. Target is based on multiples of '1024'.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [8] pods.
    Experiment is run once.

### Services
PostgreSQL-1-1-1024
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-1-1-1024-1749628840 9091:9091

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387465856
    datadisk:331
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749628840

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       64.0        1.0   1.0                0.0

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       59.84     0.44           2.5                 2.65

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       11.39        0          0.23                 0.23

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
```


### Start DBMS and Load Data and Run Workload

```bash
nohup python benchbase.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 1 -nlt 64 -nbp 8 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql.log &
```

test_benchbase_run_postgresql.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 686s 
    Code: 1749629205
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Services
PostgreSQL-1-1-1024
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-1-1-1024-1749629205 9091:9091

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387465804
    datadisk:331
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749629205

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         64    1024          8  300.0           0                        418.06                     414.25         0.0                                                     800425.0                                            152900.62

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[8]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[8]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       66.0        1.0   8.0          54.545455

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       61.02     0.77          2.47                 2.61

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       11.48        0          0.23                 0.23

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       712.8     2.26          2.96                 3.22

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      279.33     0.36          1.95                 1.95

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


## HammerDB

You can watch for all components of these experiments by

```bash
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
```

You can remove all components of these experiments by

```bash
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc
```

### Start DBMS

```bash
nohup python hammerdb.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start </dev/null &>$LOG_DIR/test_hammerdb_start_postgresql.log &
```

test_hammerdb_start_postgresql.log
```markdown
## Show Summary

### Workload
HammerDB Start DBMS
    Type: tpcc
    Duration: 186s 
    Code: 1749629932
    Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-BHT-1-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1-1749629932 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:386794388
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749629932

### Tests
```


### Start DBMS and Load Data

```bash
nohup python hammerdb.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 1 -nlt 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load </dev/null &>$LOG_DIR/test_hammerdb_load_postgresql.log &
```

test_hammerdb_load_postgresql.log
```markdown
## Show Summary

### Workload
HammerDB Data Loading SF=1 (warehouses for TPC-C)
    Type: tpcc
    Duration: 293s 
    Code: 1749630175
    HammerDB runs the benchmark.
    This imports TPC-C data sets.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 1.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Experiment is run once.

### Services
PostgreSQL-BHT-1-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1-1749630175 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387041488
    datadisk:281
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749630175

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1-1       36.0        1.0   1.0                        0.0

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1        4.97        0          2.43                  2.5

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1       11.94        0          0.02                 0.02

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
```


### Start DBMS and Load Data and Run Workload

```bash
nohup python hammerdb.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_hammerdb_run_postgresql.log &
```

test_hammerdb_run_postgresql.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=1 (warehouses for TPC-C)
    Type: tpcc
    Duration: 798s 
    Code: 1749630540
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 1. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Services
PostgreSQL-BHT-1-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1-1749630540 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387041208
    datadisk:281
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749630540

### Execution
                      experiment_run  vusers  client  pod_count  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-1-1-1               1      64       1          1         0.0  19670.0  53038.0         5       0

Warehouses: 1

### Workflow

#### Actual
DBMS PostgreSQL-BHT-1-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1-1       31.0        1.0   1.0                 116.129032

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1        3.46        0          2.41                 2.47

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1       12.11        0          0.02                 0.02

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1    10120.59     23.8          3.49                 3.91

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1        88.8     0.22          0.19                 0.19

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```



## TPC-H

You can watch for all components of these experiments by

```bash
kubectl get all -l app=bexhoma,usecase=tpc-h
```

You can remove all components of these experiments by

```bash
kubectl delete all -l app=bexhoma,usecase=tpc-h
```

### Start DBMS

```bash
nohup python tpch.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start </dev/null &>$LOG_DIR/test_tpch_start_postgresql.log &
```

test_tpch_start_postgresql.log
```markdown
## Show Summary

### Workload
TPC-H Start DBMS
    Type: tpch
    Duration: 186s 
    Code: 1749631401
    Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749631401 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:386626208
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749631401

### Tests
```


### Start DBMS and Load Data

```bash
nohup python tpch.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load </dev/null &>$LOG_DIR/test_tpch_load_postgresql.log &
```

test_tpch_load_postgresql.log
```markdown
## Show Summary

### Workload
TPC-H Data Loading SF=1
    Type: tpch
    Duration: 413s 
    Code: 1749631645
    This includes the reading queries of TPC-H.
    This imports TPC-H data sets.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749631645 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:389395728
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749631645

### Loading [s]
                    timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1           0.0           89.0         1.0       89.0     180.0

### Tests
```


### Start DBMS and Load Data and Run Workload

```bash
nohup python tpch.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss  \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql.log &
```

test_tpch_run_postgresql.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 506s 
    Code: 1749632089
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749632089 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:389393760
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749632089

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-1-1
Pricing Summary Report (TPC-H Q1)                                 2558.68
Minimum Cost Supplier Query (TPC-H Q2)                             440.98
Shipping Priority (TPC-H Q3)                                       772.87
Order Priority Checking Query (TPC-H Q4)                          1290.26
Local Supplier Volume (TPC-H Q5)                                   673.11
Forecasting Revenue Change (TPC-H Q6)                              508.40
Forecasting Revenue Change (TPC-H Q7)                              794.26
National Market Share (TPC-H Q8)                                   636.57
Product Type Profit Measure (TPC-H Q9)                            1154.01
Forecasting Revenue Change (TPC-H Q10)                            1275.45
Important Stock Identification (TPC-H Q11)                         254.67
Shipping Modes and Order Priority (TPC-H Q12)                     1065.38
Customer Distribution (TPC-H Q13)                                 1991.37
Forecasting Revenue Change (TPC-H Q14)                             567.41
Top Supplier Query (TPC-H Q15)                                     558.84
Parts/Supplier Relationship (TPC-H Q16)                            570.01
Small-Quantity-Order Revenue (TPC-H Q17)                          1884.79
Large Volume Customer (TPC-H Q18)                                 7194.80
Discounted Revenue (TPC-H Q19)                                     709.86
Potential Part Promotion (TPC-H Q20)                               661.73
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                920.74
Global Sales Opportunity Query (TPC-H Q22)                         248.82

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1-1           0.0           87.0         1.0       88.0     177.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-1-1-1           0.86

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-1-1-1            4163.28

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-1-1 1  1              1                 29      1   1          2731.03

### Workflow

#### Actual
DBMS PostgreSQL-BHT - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      144.14     0.04          3.79                 5.33

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1        4.97        0           0.0                 0.73

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      121.82        0          3.85                 5.39

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1           0        0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST failed: Workflow not as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
```



## TPC-DS

You can watch for all components of these experiments by

```bash
kubectl get all -l app=bexhoma,usecase=tpc-ds
```

You can remove all components of these experiments by

```bash
kubectl delete all -l app=bexhoma,usecase=tpc-ds
```

### Start DBMS

```bash
nohup python tpcds.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start </dev/null &>$LOG_DIR/test_tpcds_start_postgresql.log &
```

test_tpcds_start_postgresql.log
```markdown
## Show Summary

### Workload
TPC-DS Start DBMS
    Type: tpcds
    Duration: 189s 
    Code: 1749632646
    Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749632646 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:386609984
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749632646

### Tests
```


### Start DBMS and Load Data

```bash
nohup python tpcds.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load </dev/null &>$LOG_DIR/test_tpcds_load_postgresql.log &
```

test_tpcds_load_postgresql.log
```markdown
## Show Summary

### Workload
TPC-DS Data Loading SF=1
    Type: tpcds
    Duration: 268s 
    Code: 1749632890
    This includes the reading queries of TPC-DS.
    This imports TPC-DS data sets.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749632890 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:386611056
    datadisk:40
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749632890

### Loading [s]
                    timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1           0.0            0.0         1.0        1.0       3.0

### Tests
```


### Start DBMS and Load Data and Run Workload

```bash
nohup python tpcds.py -ms 1 -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss  \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_tpcds_run_postgresql.log &
```

test_tpcds_run_postgresql.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 350s 
    Code: 1749633193
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749633193 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:386610852
    datadisk:40
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749633193

### Errors (failed queries)
            PostgreSQL-BHT-1-1-1
TPC-DS Q90                  True
TPC-DS Q90
PostgreSQL-BHT-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: division by zero

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-1-1-1
TPC-DS Q1                     49.55
TPC-DS Q2                      7.15
TPC-DS Q3                      3.42
TPC-DS Q4                     11.50
TPC-DS Q5                     11.24
TPC-DS Q6                      3.75
TPC-DS Q7                      3.06
TPC-DS Q8                      5.80
TPC-DS Q9                      4.27
TPC-DS Q10                     5.08
TPC-DS Q11                     4.47
TPC-DS Q12                     3.37
TPC-DS Q13                     5.07
TPC-DS Q14a+b                 24.71
TPC-DS Q15                     2.28
TPC-DS Q16                     4.71
TPC-DS Q17                    11.98
TPC-DS Q18                     4.43
TPC-DS Q19                     4.27
TPC-DS Q20                     2.17
TPC-DS Q21                     3.75
TPC-DS Q22                     2.12
TPC-DS Q23a+b                 10.88
TPC-DS Q24a+b                  8.88
TPC-DS Q25                    21.37
TPC-DS Q26                     2.47
TPC-DS Q27                     2.45
TPC-DS Q28                  1721.81
TPC-DS Q29                    16.58
TPC-DS Q30                     3.09
TPC-DS Q31                     5.68
TPC-DS Q32                     2.40
TPC-DS Q33                     5.38
TPC-DS Q34                     2.96
TPC-DS Q35                     4.64
TPC-DS Q36                     2.93
TPC-DS Q37                     2.11
TPC-DS Q38                     3.15
TPC-DS Q39a+b                  5.61
TPC-DS Q40                     3.36
TPC-DS Q41                     2.57
TPC-DS Q42                     1.80
TPC-DS Q43                     2.29
TPC-DS Q44                     2.77
TPC-DS Q45                     2.37
TPC-DS Q46                     2.88
TPC-DS Q47                     3.18
TPC-DS Q48                     2.35
TPC-DS Q49                     4.83
TPC-DS Q50                     3.29
TPC-DS Q51                     2.80
TPC-DS Q52                     1.52
TPC-DS Q53                     2.09
TPC-DS Q54                     3.61
TPC-DS Q55                     1.44
TPC-DS Q56                     4.19
TPC-DS Q57                     3.02
TPC-DS Q58                     4.70
TPC-DS Q59                     3.82
TPC-DS Q60                     4.20
TPC-DS Q61                  1841.66
TPC-DS Q62                     3.76
TPC-DS Q63                     2.52
TPC-DS Q64                   120.22
TPC-DS Q65                     2.34
TPC-DS Q66                     8.31
TPC-DS Q67                     2.42
TPC-DS Q68                     2.46
TPC-DS Q69                     3.36
TPC-DS Q70                     2.93
TPC-DS Q71                     2.46
TPC-DS Q72                     8.93
TPC-DS Q73                     2.08
TPC-DS Q74                     3.27
TPC-DS Q75                     5.32
TPC-DS Q76                     2.42
TPC-DS Q77                  2355.24
TPC-DS Q78                     5.07
TPC-DS Q79                     1.91
TPC-DS Q80                     8.25
TPC-DS Q81                     2.44
TPC-DS Q82                     1.85
TPC-DS Q83                     3.60
TPC-DS Q84                     2.25
TPC-DS Q85                     8.81
TPC-DS Q86                     1.83
TPC-DS Q87                     2.27
TPC-DS Q88                  2933.43
TPC-DS Q89                     2.65
TPC-DS Q91                     3.66
TPC-DS Q92                     1.79
TPC-DS Q93                     1.63
TPC-DS Q94                     2.90
TPC-DS Q95                     3.70
TPC-DS Q96                     1.43
TPC-DS Q97                     1.93
TPC-DS Q98                     1.61
TPC-DS Q99                     2.07

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1-1           0.0            0.0         1.0        1.0       3.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-1-1-1            0.0

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-1-1-1          730912.95

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-1-1 1  1              1                 17      1   1         20752.94

### Workflow

#### Actual
DBMS PostgreSQL-BHT - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1         0.0      0.0          2.35                 2.38

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1           0        0           0.0                  0.0

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1       10.35     0.18          2.36                 2.39

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1           0        0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST passed: No SQL warnings
TEST failed: Workflow not as planned
TEST failed: Ingestion SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
```

