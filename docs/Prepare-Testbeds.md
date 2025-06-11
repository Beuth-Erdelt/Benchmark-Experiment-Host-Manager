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
    Duration: 186s 
    Code: 1749546838
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-1-1-16384-1749546838 9091:9091

### Connections
PostgreSQL-1-1-16384-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:386213960
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749546838

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
    Code: 1749547082
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-64-8-16384-1749547082 9091:9091

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:388650608
    datadisk:2393
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749547082

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-16384               1       64   16384          8           0                   16319.038422                61317.0             1000000                            1421.125

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      194.11     0.02          3.57                 4.47

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1        8.68        0          0.49                  0.5

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
    Code: 1749547458
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-64-8-16384-1749547458 9091:9091

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:388676316
    datadisk:2393
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749547458

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-16384               1       64   16384          8           0                   16319.870124                61298.0             1000000                            1090.625

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)
PostgreSQL-64-8-16384-1               1       64   16384          8           0                       16316.81                61359.0           1000000                             426.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-16384 - Pods [[8]]

#### Planned
DBMS PostgreSQL-64-8-16384 - Pods [[8]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      108.08     1.85          3.35                 3.93

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      108.62        0          4.54                 4.56

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1       71.63        0           3.8                  4.8

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1       71.92        0          1.64                 1.66

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
    Duration: 185s 
    Code: 1749557000
    Intro: Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-1-1-1024
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-1-1-1024-1749557000 9091:9091

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:388116548
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749557000

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
    Duration: 323s 
    Code: 1749557244
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-1-1-1024-1749557244 9091:9091

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:388444332
    datadisk:331
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749557244

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       65.0        1.0   1.0                0.0

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       44.47        0          2.47                  2.6

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       13.78        0          0.29                 0.29

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
    Duration: 685s 
    Code: 1749557610
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-1-1-1024-1749557610 9091:9091

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:389204736
    datadisk:331
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749557610

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         64    1024          8  300.0           2                        403.38                     399.78         0.0                                                     831837.0                                             158444.5

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
PostgreSQL-1-1-1024-1       31.34     0.58          2.45                 2.57

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       13.45        0          0.27                 0.27

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      601.58     2.33          2.96                 3.22

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      281.83     0.52          2.02                 2.02

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
    Duration: 185s 
    Code: 1749558337
    Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-BHT-1-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1-1749558337 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:388952032
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749558337

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
    Code: 1749558582
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1-1749558582 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:389223792
    datadisk:281
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749558582

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1-1       36.0        1.0   1.0                        0.0

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1        5.16     0.11          2.44                  2.5

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1           0        0           0.0                  0.0

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
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
    Code: 1749558955
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1-1749558955 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:389248752
    datadisk:281
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749558955

### Execution
                      experiment_run  vusers  client  pod_count  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-1-1-1               1      64       1          1         0.0  19433.0  52610.0         5       0

Warehouses: 1

### Workflow

#### Actual
DBMS PostgreSQL-BHT-1-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1-1       35.0        1.0   1.0                 102.857143

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1        3.31     0.06           2.4                 2.46

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1       16.67        0          0.02                 0.02

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1     9934.96    24.46           3.5                 3.92

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1       86.81     0.26          0.19                 0.19

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
    Duration: 216s 
    Code: 1749623589
    Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749623589 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392432036
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749623589

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
    Duration: 478s 
    Code: 1749623832
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749623832 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394490480
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749623832

### Loading [s]
                    timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1           0.0          109.0         1.0       92.0     203.0

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
    Duration: 557s 
    Code: 1749624420
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749624420 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392131340
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749624420

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-1-1
Pricing Summary Report (TPC-H Q1)                                 2578.59
Minimum Cost Supplier Query (TPC-H Q2)                             436.17
Shipping Priority (TPC-H Q3)                                       762.57
Order Priority Checking Query (TPC-H Q4)                          1277.13
Local Supplier Volume (TPC-H Q5)                                   674.93
Forecasting Revenue Change (TPC-H Q6)                              503.71
Forecasting Revenue Change (TPC-H Q7)                              794.98
National Market Share (TPC-H Q8)                                   626.29
Product Type Profit Measure (TPC-H Q9)                            1090.04
Forecasting Revenue Change (TPC-H Q10)                            1294.25
Important Stock Identification (TPC-H Q11)                         256.94
Shipping Modes and Order Priority (TPC-H Q12)                     1022.04
Customer Distribution (TPC-H Q13)                                 2102.37
Forecasting Revenue Change (TPC-H Q14)                             554.96
Top Supplier Query (TPC-H Q15)                                     548.31
Parts/Supplier Relationship (TPC-H Q16)                            571.49
Small-Quantity-Order Revenue (TPC-H Q17)                          1970.46
Large Volume Customer (TPC-H Q18)                                 7249.02
Discounted Revenue (TPC-H Q19)                                     709.77
Potential Part Promotion (TPC-H Q20)                              5024.21
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                949.99
Global Sales Opportunity Query (TPC-H Q22)                         241.19

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1-1           0.0          115.0         1.0       93.0     211.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-1-1-1           0.95

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-1-1-1            3806.53

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-1-1 1  1              1                 33      1   1           2400.0

### Workflow

#### Actual
DBMS PostgreSQL-BHT - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      151.73      1.0          3.77                 5.32

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1        8.56        0           0.0                 0.73

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      108.26        0          3.81                 5.35

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
    Duration: 190s 
    Code: 1749625066
    Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749625066 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387775060
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749625066

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
    Duration: 267s 
    Code: 1749625317
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749625317 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387181832
    datadisk:40
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749625317

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
    Duration: 328s 
    Code: 1749625623
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
    kubectl --context perdelt port-forward service/bexhoma-sut-postgresql-bht-1-1749625623 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:387181608
    datadisk:40
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749625623

### Errors (failed queries)
            PostgreSQL-BHT-1-1-1
TPC-DS Q90                  True
TPC-DS Q90
PostgreSQL-BHT-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: division by zero

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-1-1-1
TPC-DS Q1                     48.84
TPC-DS Q2                      6.42
TPC-DS Q3                      2.93
TPC-DS Q4                     11.92
TPC-DS Q5                     10.32
TPC-DS Q6                      3.27
TPC-DS Q7                      3.51
TPC-DS Q8                      5.22
TPC-DS Q9                      3.76
TPC-DS Q10                     5.13
TPC-DS Q11                     4.82
TPC-DS Q12                     2.92
TPC-DS Q13                     5.09
TPC-DS Q14a+b                 16.70
TPC-DS Q15                     2.17
TPC-DS Q16                     4.84
TPC-DS Q17                    12.92
TPC-DS Q18                     4.92
TPC-DS Q19                     3.34
TPC-DS Q20                     2.64
TPC-DS Q21                     4.49
TPC-DS Q22                     2.49
TPC-DS Q23a+b                 11.17
TPC-DS Q24a+b                  8.53
TPC-DS Q25                    22.29
TPC-DS Q26                     2.54
TPC-DS Q27                     2.35
TPC-DS Q28                  1716.68
TPC-DS Q29                    17.61
TPC-DS Q30                     3.26
TPC-DS Q31                     6.20
TPC-DS Q32                     2.37
TPC-DS Q33                     5.41
TPC-DS Q34                     3.21
TPC-DS Q35                     4.54
TPC-DS Q36                     2.78
TPC-DS Q37                     2.43
TPC-DS Q38                     2.96
TPC-DS Q39a+b                  5.44
TPC-DS Q40                     2.95
TPC-DS Q41                     2.77
TPC-DS Q42                     2.45
TPC-DS Q43                     2.62
TPC-DS Q44                     2.52
TPC-DS Q45                     2.89
TPC-DS Q46                     2.61
TPC-DS Q47                     3.25
TPC-DS Q48                     2.64
TPC-DS Q49                     6.56
TPC-DS Q50                     2.76
TPC-DS Q51                     2.49
TPC-DS Q52                     1.43
TPC-DS Q53                     2.56
TPC-DS Q54                     4.02
TPC-DS Q55                     1.71
TPC-DS Q56                     4.31
TPC-DS Q57                     3.36
TPC-DS Q58                     4.36
TPC-DS Q59                     3.98
TPC-DS Q60                     4.70
TPC-DS Q61                  1836.64
TPC-DS Q62                     3.55
TPC-DS Q63                     2.18
TPC-DS Q64                   120.97
TPC-DS Q65                     2.45
TPC-DS Q66                     8.64
TPC-DS Q67                     2.47
TPC-DS Q68                     2.49
TPC-DS Q69                     3.11
TPC-DS Q70                     2.74
TPC-DS Q71                     2.42
TPC-DS Q72                     9.11
TPC-DS Q73                     2.01
TPC-DS Q74                     2.99
TPC-DS Q75                     5.10
TPC-DS Q76                     2.47
TPC-DS Q77                  2251.74
TPC-DS Q78                     4.90
TPC-DS Q79                     2.10
TPC-DS Q80                     8.25
TPC-DS Q81                     2.10
TPC-DS Q82                     1.65
TPC-DS Q83                     3.37
TPC-DS Q84                     2.33
TPC-DS Q85                     8.88
TPC-DS Q86                     1.61
TPC-DS Q87                     2.53
TPC-DS Q88                  2897.69
TPC-DS Q89                     2.74
TPC-DS Q91                     3.76
TPC-DS Q92                     1.87
TPC-DS Q93                     1.73
TPC-DS Q94                     2.79
TPC-DS Q95                     3.20
TPC-DS Q96                     1.39
TPC-DS Q97                     2.87
TPC-DS Q98                     2.55
TPC-DS Q99                     3.09

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1-1           0.0            0.0         1.0        1.0       4.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-1-1-1            0.0

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-1-1-1          720369.85

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-1-1 1  1              1                 18      1   1          19600.0

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
PostgreSQL-BHT-1-1         0.0        0          2.35                 2.39

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
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
```

