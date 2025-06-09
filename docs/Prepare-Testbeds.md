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
```markdown
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR
```

## YCSB

You can watch for all components of these experiments by

```markdown
kubectl get all -l app=bexhoma,usecase=ycsb
```

You can remove all components of these experiments by

```markdown
kubectl delete all -l app=bexhoma,usecase=ycsb
```

### Start DBMS

test_ycsb_start_postgresql.log
```markdown
## Show Summary

### Workload
YCSB Start DBMS
    Type: ycsb
    Duration: 202s 
    Code: 1749475854
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
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1-16384-1749475854 9091:9091

### Connections
PostgreSQL-1-1-16384-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:378495280
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749475854

### Tests
TEST passed: Result contains no FAILED column
```


### Start DBMS and Load Data

test_ycsb_load_postgresql.log
```markdown
## Show Summary

### Workload
YCSB Data Loading SF=1
    Type: ycsb
    Duration: 412s 
    Code: 1749476406
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
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-64-8-16384-1749476406 9091:9091

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:380955340
    datadisk:2394
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749476406

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-16384               1       64   16384          8           0                   16318.438788                61305.0             1000000                            1172.625

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      191.25      0.0          3.52                 4.47

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1       58.98        0          0.51                 0.51

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Result contains no FAILED column
```


### Start DBMS and Load Data and Run Workload

test_ycsb_run_postgresql.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 633s 
    Code: 1749476893
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
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-64-8-16384-1749476893 9091:9091

### Connections
PostgreSQL-64-8-16384-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:380989076
    datadisk:2393
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749476893

### Loading
|                       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-64-8-16384 |                1 |        64 |    16384 |           8 |            0 |                         16319.8 |                   61289 |                1e+06 |                              1311.12 |

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)
PostgreSQL-64-8-16384-1               1       64   16384          8           0                       16318.77                61307.0           1000000                             508.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-16384 - Pods [[8]]

#### Planned
DBMS PostgreSQL-64-8-16384 - Pods [[8]]

### Ingestion - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      192.29        0          3.52                 4.45

### Ingestion - Loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      102.52        0          0.57                 0.57

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1      132.47     1.54          3.79                 4.72

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-16384-1       83.61        0          0.27                 0.28

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

```markdown
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
```

You can remove all components of these experiments by

```markdown
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc
```

### Start DBMS

test_benchbase_start_postgresql.log
```markdown
## Show Summary

### Workload
Benchbase Start DBMS
    Type: benchbase
    Duration: 204s 
    Code: 1749477942
    Intro: Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-1-1-1024
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1-1024-1749477942 9091:9091

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:378633652
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749477942

### Tests
```


### Start DBMS and Load Data

test_benchbase_load_postgresql.log
```markdown
## Show Summary

### Workload
Benchbase Data tpcc Loading SF=1
    Type: benchbase
    Duration: 379s 
    Code: 1749478207
    Intro: Benchbase runs a TPC-C experiment.
    This imports a Benchbase data set.
    Benchbase data is generated and loaded using several threads. Scaling factor is 1. Target is based on multiples of '1024'.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [64] threads, split into [1] pods.
    Experiment is run once.

### Services
PostgreSQL-1-1-1024
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1-1024-1749478207 9091:9091

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:378961356
    datadisk:331
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749478207

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       68.0        1.0   1.0                0.0

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       53.23      0.0          2.47                 2.61

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1       13.85     0.24          0.31                 0.31

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
```


### Start DBMS and Load Data and Run Workload

test_benchbase_run_postgresql.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=1
    Type: benchbase
    Duration: 800s 
    Code: 1749478649
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
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-1-1-1024-1749478649 9091:9091

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:378986804
    datadisk:331
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749478649

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         64    1024          8  300.0           0                        410.35                     406.62         0.0                                                     836226.0                                             155744.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[8]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[8]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1       67.0        1.0   8.0          53.731343

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1        61.8        0          2.47                 2.61

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1        9.88        0          0.21                 0.21

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      696.73     2.34          2.98                 3.25

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      270.01     0.49          0.25                 0.25

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

```markdown
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
```

You can remove all components of these experiments by

```markdown
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc
```

### Start DBMS

test_hammerdb_start_postgresql.log
```markdown
## Show Summary

### Workload
HammerDB Start DBMS
    Type: tpcc
    Duration: 202s 
    Code: 1749479830
    Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-BHT-1-1
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-1-1-1749479830 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:378758360
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749479830

### Tests
```


### Start DBMS and Load Data

test_hammerdb_load_postgresql.log
```markdown
## Show Summary

### Workload
HammerDB Data Loading SF=1 (warehouses for TPC-C)
    Type: tpcc
    Duration: 381s 
    Code: 1749480089
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
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-1-1-1749480089 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:379038776
    datadisk:281
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749480089

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1-1       36.0        1.0   1.0                        0.0

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1       15.28        0          2.46                 2.54

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1           0        0           0.0                  0.0

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
```


### Start DBMS and Load Data and Run Workload

test_hammerdb_run_postgresql.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=1 (warehouses for TPC-C)
    Type: tpcc
    Duration: 925s 
    Code: 1749480531
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
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-1-1-1749480531 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:379074088
    datadisk:281
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749480531

### Execution
                      experiment_run  vusers  client  pod_count  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-1-1-1               1      64       1          1         0.0  19783.0  53346.0         5       0

Warehouses: 1

### Workflow

#### Actual
DBMS PostgreSQL-BHT-1-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-1-1-1       36.0        1.0   1.0                      100.0

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1       15.24     0.05          2.46                 2.54

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1       16.58        0          0.02                 0.02

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1    10185.28    22.67          3.47                 3.88

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1-1       95.52     0.29          0.19                 0.19

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

```markdown
kubectl get all -l app=bexhoma,usecase=tpc-h
```

You can remove all components of these experiments by

```markdown
kubectl delete all -l app=bexhoma,usecase=tpc-h
```

### Start DBMS

test_tpch_start_postgresql.log
```markdown
## Show Summary

### Workload
TPC-H Start DBMS
    Type: tpch
    Duration: 204s 
    Code: 1749481527
    Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-1-1749481527 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:378892260
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749481527

### Tests
```


### Start DBMS and Load Data

test_tpch_load_postgresql.log
```markdown
## Show Summary

### Workload
TPC-H Data Loading SF=1
    Type: tpch
    Duration: 507s 
    Code: 1749481784
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
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-1-1749481784 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:381718232
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749481784

### Loading [s]
                    timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1           0.0           74.0         4.0       92.0     172.0

### Tests
```


### Start DBMS and Load Data and Run Workload

test_tpch_run_postgresql.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 558s 
    Code: 1749482338
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
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-1-1749482338 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:381763564
    datadisk:2757
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749482338

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-1-1-1
Pricing Summary Report (TPC-H Q1)                                 2624.38
Minimum Cost Supplier Query (TPC-H Q2)                             477.51
Shipping Priority (TPC-H Q3)                                       757.73
Order Priority Checking Query (TPC-H Q4)                          1298.87
Local Supplier Volume (TPC-H Q5)                                   644.87
Forecasting Revenue Change (TPC-H Q6)                              501.28
Forecasting Revenue Change (TPC-H Q7)                              774.39
National Market Share (TPC-H Q8)                                   602.51
Product Type Profit Measure (TPC-H Q9)                            1139.51
Forecasting Revenue Change (TPC-H Q10)                            1262.92
Important Stock Identification (TPC-H Q11)                         253.28
Shipping Modes and Order Priority (TPC-H Q12)                     1005.31
Customer Distribution (TPC-H Q13)                                 1991.53
Forecasting Revenue Change (TPC-H Q14)                             540.14
Top Supplier Query (TPC-H Q15)                                     557.50
Parts/Supplier Relationship (TPC-H Q16)                            571.59
Small-Quantity-Order Revenue (TPC-H Q17)                          1908.32
Large Volume Customer (TPC-H Q18)                                 7122.61
Discounted Revenue (TPC-H Q19)                                     700.37
Potential Part Promotion (TPC-H Q20)                               683.79
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                905.22
Global Sales Opportunity Query (TPC-H Q22)                         256.30

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1-1           0.0           67.0         3.0       94.0     166.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-1-1-1           0.86

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-1-1-1            4191.02

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-1-1 1  1              1                 28      1   1          2828.57

### Workflow

#### Actual
DBMS PostgreSQL-BHT - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1      141.65     0.98          3.78                 5.32

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1        9.57        0           0.0                 0.73

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-1-1       111.6        0          3.85                 5.39

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

```markdown
kubectl get all -l app=bexhoma,usecase=tpc-ds
```

You can remove all components of these experiments by

```markdown
kubectl delete all -l app=bexhoma,usecase=tpc-ds
```

### Start DBMS

test_tpcds_start_postgresql.log
```markdown
## Show Summary

### Workload
TPC-DS Start DBMS
    Type: tpcds
    Duration: 219s 
    Code: 1749482968
    Start DBMS and do not load data.
    This just starts a SUT.
    Experiment uses bexhoma version 0.8.7.
    Experiment is limited to DBMS ['PostgreSQL'].
    SUT is fixed to cl-worker11.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-1-1749482968 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:379000608
    datadisk:39
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749482968

### Tests
```


### Start DBMS and Load Data

test_tpcds_load_postgresql.log
```markdown
## Show Summary

### Workload
TPC-DS Data Loading SF=1
    Type: tpcds
    Duration: 303s 
    Code: 1749483265
    This includes the reading queries of TPC-DS.
    This imports TPC-DS data sets.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Experiment is run once.

### Services
PostgreSQL-BHT-1
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-1-1749483265 9091:9091

### Connections
PostgreSQL-BHT-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:379024788
    datadisk:40
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749483265

### Loading [s]
                    timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1           0.0            0.0         5.0        7.0      13.0

### Tests
```


### Start DBMS and Load Data and Run Workload

test_tpcds_run_postgresql.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 404s 
    Code: 1749483645
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
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
    kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-1-1749483645 9091:9091

### Connections
PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:379054424
    datadisk:40
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1749483645

### Errors (failed queries)
            PostgreSQL-BHT-1-1-1
TPC-DS Q90                  True
TPC-DS Q90
PostgreSQL-BHT-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: division by zero

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-1-1-1
TPC-DS Q1                     42.52
TPC-DS Q2                      6.01
TPC-DS Q3                      2.23
TPC-DS Q4                      9.52
TPC-DS Q5                      8.26
TPC-DS Q6                      2.60
TPC-DS Q7                      2.17
TPC-DS Q8                      3.63
TPC-DS Q9                      2.79
TPC-DS Q10                     3.73
TPC-DS Q11                     3.46
TPC-DS Q12                     1.79
TPC-DS Q13                     3.55
TPC-DS Q14a+b                 13.29
TPC-DS Q15                     1.66
TPC-DS Q16                     3.30
TPC-DS Q17                    11.10
TPC-DS Q18                     3.54
TPC-DS Q19                     2.76
TPC-DS Q20                     1.54
TPC-DS Q21                     2.84
TPC-DS Q22                     1.27
TPC-DS Q23a+b                  9.65
TPC-DS Q24a+b                  7.52
TPC-DS Q25                    31.01
TPC-DS Q26                     2.72
TPC-DS Q27                     2.71
TPC-DS Q28                  1727.67
TPC-DS Q29                    16.76
TPC-DS Q30                     3.08
TPC-DS Q31                     5.75
TPC-DS Q32                     2.24
TPC-DS Q33                     5.48
TPC-DS Q34                     3.07
TPC-DS Q35                     5.23
TPC-DS Q36                     2.59
TPC-DS Q37                     2.87
TPC-DS Q38                     3.20
TPC-DS Q39a+b                  5.15
TPC-DS Q40                     3.57
TPC-DS Q41                     2.83
TPC-DS Q42                     2.43
TPC-DS Q43                     2.54
TPC-DS Q44                     2.90
TPC-DS Q45                     2.75
TPC-DS Q46                     2.82
TPC-DS Q47                     3.13
TPC-DS Q48                     2.62
TPC-DS Q49                     4.91
TPC-DS Q50                     2.75
TPC-DS Q51                     2.70
TPC-DS Q52                     1.87
TPC-DS Q53                     1.94
TPC-DS Q54                     3.61
TPC-DS Q55                     1.55
TPC-DS Q56                     4.13
TPC-DS Q57                     2.86
TPC-DS Q58                     4.61
TPC-DS Q59                     3.90
TPC-DS Q60                     4.75
TPC-DS Q61                  1892.71
TPC-DS Q62                     5.04
TPC-DS Q63                     2.33
TPC-DS Q64                   127.25
TPC-DS Q65                     2.45
TPC-DS Q66                     8.81
TPC-DS Q67                     2.92
TPC-DS Q68                     2.82
TPC-DS Q69                     3.18
TPC-DS Q70                     2.87
TPC-DS Q71                     2.92
TPC-DS Q72                     9.34
TPC-DS Q73                     2.62
TPC-DS Q74                     3.28
TPC-DS Q75                     5.72
TPC-DS Q76                     2.50
TPC-DS Q77                  2346.77
TPC-DS Q78                     5.14
TPC-DS Q79                     2.56
TPC-DS Q80                     8.78
TPC-DS Q81                     2.50
TPC-DS Q82                     1.98
TPC-DS Q83                     4.04
TPC-DS Q84                     2.37
TPC-DS Q85                     9.16
TPC-DS Q86                     1.87
TPC-DS Q87                     2.48
TPC-DS Q88                  2952.98
TPC-DS Q89                     2.61
TPC-DS Q91                     3.70
TPC-DS Q92                     2.04
TPC-DS Q93                     1.94
TPC-DS Q94                     3.02
TPC-DS Q95                     3.51
TPC-DS Q96                     1.46
TPC-DS Q97                     2.09
TPC-DS Q98                     1.78
TPC-DS Q99                     2.29

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-1-1-1           0.0            0.0         4.0        7.0      13.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-1-1-1            0.0

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-1-1-1          758175.57

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                 time [s]  count  SF  Throughput@Size
DBMS               SF num_experiment num_client                                      
PostgreSQL-BHT-1-1 1  1              1                 13      1   1         27138.46

### Workflow

#### Actual
DBMS PostgreSQL-BHT - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST passed: No SQL warnings
TEST failed: Workflow not as planned
```

