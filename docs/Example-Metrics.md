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

### Benchbase's TPC-C

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
    Duration: 1446s 
    Code: 1772581479
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:151826
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772581479
                TENANT_VOL:False
PostgreSQL-1-1-1024-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:152767
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772581479
                TENANT_VOL:False

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
PostgreSQL-1-1-1024-1-1               1        160   16384       1      1  300.0           6                   1991.432914                1974.689585         0.0                                                     279727.0                                              80308.0
PostgreSQL-1-1-1024-2-1               1         80    8192       2      1  300.0           1                    913.859667                 905.976336         0.0                                                     314555.0                                              87525.0
PostgreSQL-1-1-1024-2-2               1         80    8192       2      2  300.0           1                    915.949728                 908.009730         0.0                                                     316546.0                                              87268.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1        160   16384          1  300.0           6                       1991.43                    1974.69         0.0                                                     279727.0                                              80308.0
PostgreSQL-1-1-1024-2               1        160   16384          2  300.0           2                       1829.81                    1813.99         0.0                                                     316546.0                                              87396.5

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      242.0        1.0   1.0         238.016529
PostgreSQL-1-1-1024-2      242.0        1.0   2.0         238.016529

### Monitoring

### Loading phase: SUT deployment
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      714.67     4.15           7.4                 9.04
PostgreSQL-1-1-1024-2      714.67     4.15           7.4                 9.04

### Loading phase: component loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1250.19      9.7          0.26                 0.26
PostgreSQL-1-1-1024-2     1250.19      9.7          0.26                 0.26

### Execution phase: SUT deployment
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     2638.93     9.14          9.66                11.91
PostgreSQL-1-1-1024-2     2380.62     8.71         10.30                13.04

### Execution phase: component benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      557.09     2.16          0.76                 0.76
PostgreSQL-1-1-1024-2      557.09     2.57          0.76                 0.76

### Application Metrics

#### Loading phase: SUT deployment
                       Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-1-1-1024-1                       15                                       0                                               0                         17                                     16
PostgreSQL-1-1-1024-2                       15                                       0                                               0                         17                                     16

#### Execution phase: SUT deployment
                       Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-1-1-1024-1                     10.0                                    18.0                                             0.0                      158.0                                  158.0
PostgreSQL-1-1-1024-2                      9.0                                    15.0                                             0.0                      160.0                                  160.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

The summary shows the first 5 application metrics aggregated per execution run.
An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/dev).



### HammerDB's TPC-C

Example:
```bash
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_appmetrics.log &
```

doc_hammerdb_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1314s 
    Code: 1771361129
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [16] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-16-1-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:102202
    datadisk:3299
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771361129
PostgreSQL-BHT-16-1-2 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:103193
    datadisk:4290
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1771361129

### Execution
                       experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-16-1-1               1      16       1          1     33.83     50.67         0.0  16246.0  37518.0         5       0
PostgreSQL-BHT-16-1-2               1      16       2          2     33.80     58.61         0.0  19568.5  45451.5         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-16-1 - Pods [[2, 1]]

#### Planned
DBMS PostgreSQL-BHT-16-1 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-16-1-1       94.0        1.0   1.0                 612.765957
PostgreSQL-BHT-16-1-2       94.0        1.0   2.0                 612.765957

### Monitoring

### Loading phase: SUT deployment
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       123.5     1.49          7.16                 7.82
PostgreSQL-BHT-16-1-2       123.5     1.49          7.16                 7.82

### Loading phase: component loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      224.42        0          0.15                 0.15
PostgreSQL-BHT-16-1-2      224.42        0          0.15                 0.15

### Execution phase: SUT deployment
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1      329.14     0.79          7.63                 8.46
PostgreSQL-BHT-16-1-2      340.92     0.90          8.06                 9.12

### Execution phase: component benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-16-1-1       59.93     0.14          0.16                 0.16
PostgreSQL-BHT-16-1-2       54.25     0.32          0.16                 0.16

### Application Metrics
                       Active Backends Waiting on I/O  Active Backends Waiting on WAL  Active Backends Waiting on Locks  Max Transaction Duration (I/O Wait)  Max Transaction Duration (WAL Wait)
PostgreSQL-BHT-16-1-1                             1.0                            13.0                               9.0                                 0.19                                 0.31
PostgreSQL-BHT-16-1-2                             2.0                            15.0                               6.0                                 0.14                                 0.22

### Tests
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```


### TPC-H

Example:
```bash
nohup python tpch.py -ms 1 -dt -tr -lr 64Gi \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_appmetrics.log &
```

doc_tpch_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 655s 
    Code: 1772627833
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:155709
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1772627833

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                                 4945.41
Minimum Cost Supplier Query (TPC-H Q2)                            1342.66
Shipping Priority (TPC-H Q3)                                      1516.39
Order Priority Checking Query (TPC-H Q4)                           739.54
Local Supplier Volume (TPC-H Q5)                                  1422.49
Forecasting Revenue Change (TPC-H Q6)                              983.96
Forecasting Revenue Change (TPC-H Q7)                             1726.25
National Market Share (TPC-H Q8)                                  1029.41
Product Type Profit Measure (TPC-H Q9)                            2508.72
Forecasting Revenue Change (TPC-H Q10)                            3351.44
Important Stock Identification (TPC-H Q11)                         548.35
Shipping Modes and Order Priority (TPC-H Q12)                     1553.62
Customer Distribution (TPC-H Q13)                                 5958.15
Forecasting Revenue Change (TPC-H Q14)                            1637.12
Top Supplier Query (TPC-H Q15)                                    1256.17
Parts/Supplier Relationship (TPC-H Q16)                           1227.87
Small-Quantity-Order Revenue (TPC-H Q17)                          5067.05
Large Volume Customer (TPC-H Q18)                                16191.98
Discounted Revenue (TPC-H Q19)                                     233.43
Potential Part Promotion (TPC-H Q20)                               803.12
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               1668.58
Global Sales Opportunity Query (TPC-H Q22)                         409.17

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           4.0          130.0         1.0      308.0     450.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           1.62

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            6870.64

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1 3.0 1              1                 63      1  3.0          3771.43

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  3.0     8               1           1       1772628363     1772628426

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      299.47     1.69          9.73                13.97

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       24.84     0.11           0.0                 0.28

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1      127.23     2.38         10.22                14.46

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1        16.5     0.28          0.36                 0.36

### Application Metrics
                    Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
PostgreSQL-BHT-8-1                      0.0                                     0.0                                             0.0                          5                                      5

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```


### TPC-DS

Example:
```bash
nohup python tpcds.py -ms 1 -dt -tr -lr 64Gi \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_appmetrics.log &
```

doc_tpcds_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 2561s 
    Code: 1771358428
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:113158
    datadisk:14255
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1771358428

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-8-1-1
TPC-DS Q1                    531.27
TPC-DS Q2                   1788.27
TPC-DS Q3                   1201.61
TPC-DS Q4                  46720.55
TPC-DS Q5                   2682.32
TPC-DS Q6                 756080.92
TPC-DS Q7                   1765.44
TPC-DS Q8                    293.58
TPC-DS Q9                   7814.92
TPC-DS Q10                  3363.30
TPC-DS Q11                 26018.12
TPC-DS Q12                   416.62
TPC-DS Q13                  4105.91
TPC-DS Q14a+b              19868.07
TPC-DS Q15                   828.35
TPC-DS Q16                  1282.74
TPC-DS Q17                  2050.33
TPC-DS Q18                  1899.90
TPC-DS Q19                  1149.19
TPC-DS Q20                   746.11
TPC-DS Q21                  1049.01
TPC-DS Q22                 23864.92
TPC-DS Q23a+b              31691.97
TPC-DS Q24a+b               4172.68
TPC-DS Q25                  1969.92
TPC-DS Q26                  1404.84
TPC-DS Q27                   120.42
TPC-DS Q28                  6057.62
TPC-DS Q29                  2304.47
TPC-DS Q30                236752.33
TPC-DS Q31                 11780.53
TPC-DS Q32                  1748.44
TPC-DS Q33                  2314.07
TPC-DS Q34                   102.45
TPC-DS Q35                  3867.77
TPC-DS Q36                   108.12
TPC-DS Q37                  1352.71
TPC-DS Q38                  7383.00
TPC-DS Q39a+b              13596.70
TPC-DS Q40                   707.51
TPC-DS Q41                  9093.39
TPC-DS Q42                   507.87
TPC-DS Q43                   151.59
TPC-DS Q44                     2.83
TPC-DS Q45                   500.69
TPC-DS Q46                   171.33
TPC-DS Q47                  8819.38
TPC-DS Q48                  3709.11
TPC-DS Q49                  3692.21
TPC-DS Q50                  3605.21
TPC-DS Q51                  7137.61
TPC-DS Q52                   511.91
TPC-DS Q53                   676.49
TPC-DS Q54                   190.01
TPC-DS Q55                   506.32
TPC-DS Q56                  2420.33
TPC-DS Q57                  6619.67
TPC-DS Q58                  2342.03
TPC-DS Q59                  2686.89
TPC-DS Q60                  2740.95
TPC-DS Q61                   337.00
TPC-DS Q62                   591.78
TPC-DS Q63                   648.58
TPC-DS Q64                  3354.56
TPC-DS Q65                  3676.64
TPC-DS Q66                  1813.00
TPC-DS Q67                 26249.85
TPC-DS Q68                   167.31
TPC-DS Q69                  1172.36
TPC-DS Q70                  2605.99
TPC-DS Q71                  2052.08
TPC-DS Q72                  7151.19
TPC-DS Q73                    99.66
TPC-DS Q74                  7166.97
TPC-DS Q75                  9705.04
TPC-DS Q76                  1015.61
TPC-DS Q77                  1378.23
TPC-DS Q78                  6881.67
TPC-DS Q79                  1118.23
TPC-DS Q80                  2198.37
TPC-DS Q81                179948.42
TPC-DS Q82                  1412.02
TPC-DS Q83                   426.88
TPC-DS Q84                   256.25
TPC-DS Q85                   951.36
TPC-DS Q86                  1460.45
TPC-DS Q87                  7396.66
TPC-DS Q88                  7636.49
TPC-DS Q89                   680.05
TPC-DS Q90                  1045.43
TPC-DS Q91                   482.90
TPC-DS Q92                   252.93
TPC-DS Q93                  1284.75
TPC-DS Q94                  1028.50
TPC-DS Q95                 24602.92
TPC-DS Q96                   516.76
TPC-DS Q97                  2385.47
TPC-DS Q98                  1194.23
TPC-DS Q99                   917.56

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          348.0         1.0      688.0    1049.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           1.94

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            5618.37

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1 3.0 1              1               1614      1  3.0           662.45

### Workflow
                               orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1  PostgreSQL-BHT-8-1  3.0     8               1           1       1771359313     1771360927

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       30.69     0.15          0.01                 2.65

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1     2124.06     2.66         12.45                19.15

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       21.23     0.03          0.31                 0.32

### Application Metrics
                    Active Backends Waiting on I/O  Active Backends Waiting on WAL  Active Backends Waiting on Locks  Max Transaction Duration (I/O Wait)  Max Transaction Duration (WAL Wait)
PostgreSQL-BHT-8-1                             0.0                             0.0                               0.0                                  0.0                                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```



### YCSB

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_appmetrics.log &
```

doc_ycsb_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=3
    Type: ycsb
    Duration: 5801s 
    Code: 1771351887
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 3000000.
    Ordering of inserts is hashed.
    Number of operations is 3000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [2, 3].
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-65536-1 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:105993
    datadisk:7090
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1771351887
PostgreSQL-64-8-65536-2 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:107451
    datadisk:8549
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1771351887
PostgreSQL-64-8-65536-3 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:108433
    datadisk:9530
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1771351887
PostgreSQL-64-8-65536-4 uses docker image postgres:18.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:109310
    datadisk:10407
    cpu_list:0-63
    args:['-c', 'max_connections=3000', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1771351887

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-65536               1       64   65536          8           0                    3298.366095               909645.0             3000000                             77455.0

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-65536-1               1       64   32768          1           0                        2847.60              1053517.0           1498998                             847.0             1501002                            878591.0
PostgreSQL-64-8-65536-2               1       64   32768          8           0                        2862.28              1057291.0           1499498                             770.0             1500502                            902655.0
PostgreSQL-64-8-65536-3               1       64   49152          1           0                        2838.27              1056983.0           1499484                             756.0             1500516                            879103.0
PostgreSQL-64-8-65536-4               1       64   49152          8           0                        2848.42              1058915.0           1500611                             746.0             1499389                            912895.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-65536 - Pods [[8, 8, 1, 1]]

#### Planned
DBMS PostgreSQL-64-8-65536 - Pods [[1, 8, 1, 8]]

### Monitoring

### Loading phase: SUT deployment
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1     1055.57     1.13          9.78                12.74
PostgreSQL-64-8-65536-2     1055.57     1.13          9.78                12.74
PostgreSQL-64-8-65536-3     1055.57     1.13          9.78                12.74
PostgreSQL-64-8-65536-4     1055.57     1.13          9.78                12.74

### Loading phase: component loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      432.97     0.51          0.11                 0.11
PostgreSQL-64-8-65536-2      432.97     0.51          0.11                 0.11
PostgreSQL-64-8-65536-3      432.97     0.51          0.11                 0.11
PostgreSQL-64-8-65536-4      432.97     0.51          0.11                 0.11

### Execution phase: SUT deployment
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      970.90     1.11         10.93                15.14
PostgreSQL-64-8-65536-2      897.92     0.94         11.37                15.99
PostgreSQL-64-8-65536-3      907.21     0.92         11.74                16.00
PostgreSQL-64-8-65536-4      912.15     0.90         12.11                16.00

### Execution phase: component benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-65536-1      271.50     0.28          0.13                 0.13
PostgreSQL-64-8-65536-2      269.54     0.54          0.12                 0.12
PostgreSQL-64-8-65536-3      286.73     0.40          0.13                 0.13
PostgreSQL-64-8-65536-4      264.12     0.50          0.13                 0.13

### Application Metrics

#### Loading phase: SUT deployment
                         Active Backends Waiting on I/O  Active Backends Waiting on WAL  Active Backends Waiting on Locks  Max Transaction Duration (I/O Wait)  Max Transaction Duration (WAL Wait)
PostgreSQL-64-8-65536-1                             2.0                            64.0                              16.0                                 0.26                                 0.26
PostgreSQL-64-8-65536-2                             2.0                            64.0                              16.0                                 0.26                                 0.26
PostgreSQL-64-8-65536-3                             2.0                            64.0                              16.0                                 0.26                                 0.26
PostgreSQL-64-8-65536-4                             2.0                            64.0                              16.0                                 0.26                                 0.26

#### Execution phase: SUT deployment
                         Active Backends Waiting on I/O  Active Backends Waiting on WAL  Active Backends Waiting on Locks  Max Transaction Duration (I/O Wait)  Max Transaction Duration (WAL Wait)
PostgreSQL-64-8-65536-1                             1.0                            35.0                              44.0                                 0.07                                 1.71
PostgreSQL-64-8-65536-2                             1.0                            35.0                              47.0                                 0.05                                 2.77
PostgreSQL-64-8-65536-3                             2.0                            33.0                              45.0                                 0.08                                 2.87
PostgreSQL-64-8-65536-4                             1.0                            32.0                              43.0                                 0.07                                 2.48

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```



















## MySQL

### Benchbase's TPC-C

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
    Duration: 1532s 
    Code: 1771362510
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-1-1-1024-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:134611
    datadisk:35708
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1771362510
                TENANT_VOL:False
MySQL-1-1-1024-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:135499
    datadisk:36596
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1771362510
                TENANT_VOL:False

### Execution

#### Per Pod
                    experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                
MySQL-1-1-1024-1-1               1        160   16384       1      1  300.0           0                    452.559916                 449.943250         0.0                                                     894251.0                                             353090.0
MySQL-1-1-1024-2-2               1         80    8192       2      1  300.0           0                    205.463329                 204.309996         0.0                                                     911769.0                                             388838.0
MySQL-1-1-1024-2-1               1         80    8192       2      2  300.0           0                    206.163283                 205.133283         0.0                                                     911606.0                                             387621.0

#### Aggregated Parallel
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1        160   16384          1  300.0           0                        452.56                     449.94         0.0                                                     894251.0                                             353090.0
MySQL-1-1-1024-2               1        160   16384          2  300.0           0                        411.63                     409.44         0.0                                                     911769.0                                             388229.5

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[2, 1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1, 2]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1      494.0        1.0   1.0          116.59919
MySQL-1-1-1024-2      494.0        1.0   2.0          116.59919

### Monitoring

### Loading phase: SUT deployment
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1      710.72     2.18           9.7                13.17
MySQL-1-1-1024-2      710.72     2.18           9.7                13.17

### Loading phase: component loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1      1385.5     6.17          0.29                 0.29
MySQL-1-1-1024-2      1385.5     6.17          0.29                 0.29

### Execution phase: SUT deployment
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1      853.41     4.13         10.00                14.44
MySQL-1-1-1024-2      918.90     3.19         10.19                15.87

### Execution phase: component benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1      321.36     1.33          0.74                 0.74
MySQL-1-1-1024-2      321.36     2.43          0.74                 0.74

### Application Metrics

#### Loading phase: SUT deployment
                  InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-1-1-1024-1                           1.0                    332.18                    0.01                0.0                    0.0
MySQL-1-1-1024-2                           1.0                    332.18                    0.01                0.0                    0.0

#### Execution phase: SUT deployment
                  InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-1-1-1024-1                           1.0                  11221.44                    0.11                0.0                    0.0
MySQL-1-1-1024-2                           0.0                  10215.05                    0.11                0.0                    0.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

The summary shows the first 5 application metrics aggregated per execution run.
An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/dev).



### HammerDB's TPC-C

Example:
```bash
nohup python hammerdb.py -ms 1 -tr -lr 64Gi \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms MySQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_run_mysql_appmetrics.log &
```

doc_hammerdb_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1625s 
    Code: 1771426367
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [16] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-16-1-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:134610
    datadisk:35460
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1771426367
MySQL-BHT-16-1-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:134965
    datadisk:35815
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1771426367

### Execution
                  experiment_run  vusers  client  pod_count  P95 [ms]  P99 [ms]  efficiency    NOPM     TPM  duration  errors
MySQL-BHT-16-1-1               1      16       1          1    192.44    275.82         0.0  2843.0  6658.0         5       0
MySQL-BHT-16-1-2               1      16       2          2    200.59    284.37         0.0  3758.0  8679.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MySQL-BHT-16-1 - Pods [[2, 1]]

#### Planned
DBMS MySQL-BHT-16-1 - Pods [[1, 2]]

### Loading
                  time_load  terminals  pods  Imported warehouses [1/h]
MySQL-BHT-16-1-1      199.0        1.0   1.0                 289.447236
MySQL-BHT-16-1-2      199.0        1.0   2.0                 289.447236

### Monitoring

### Loading phase: SUT deployment
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-16-1-1      469.22     3.36         22.14                24.82
MySQL-BHT-16-1-2      469.22     3.36         22.14                24.82

### Loading phase: component loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-16-1-1      344.66     2.75          0.17                 0.17
MySQL-BHT-16-1-2      344.66     2.75          0.17                 0.17

### Execution phase: SUT deployment
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-16-1-1      208.68     1.64         22.32                25.79
MySQL-BHT-16-1-2      272.89     0.65         22.38                26.42

### Execution phase: component benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-16-1-1       20.85     0.05          0.09                 0.09
MySQL-BHT-16-1-2       18.87     0.09          0.09                 0.09

### Application Metrics
                  InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-BHT-16-1-1                           1.0                  15651.17                    0.01                0.0                    0.0
MySQL-BHT-16-1-2                           0.0                  20625.42                    0.01                0.0                    0.0

### Tests
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```


### TPC-H

Example:
```bash
nohup python tpch.py -ms 1 -dt -tr -lr 64Gi \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_run_mysql_appmetrics.log &
```

doc_tpch_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
    Type: tpch
    Duration: 8309s 
    Code: 1771392638
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:140282
    datadisk:41376
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    eval_parameters
        code:1771392638

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MySQL-BHT-64-1-1
Pricing Summary Report (TPC-H Q1)                            89908.45
Minimum Cost Supplier Query (TPC-H Q2)                        1043.41
Shipping Priority (TPC-H Q3)                                 14071.09
Order Priority Checking Query (TPC-H Q4)                      4827.17
Local Supplier Volume (TPC-H Q5)                             11534.73
Forecasting Revenue Change (TPC-H Q6)                        12379.74
Forecasting Revenue Change (TPC-H Q7)                        18225.99
National Market Share (TPC-H Q8)                             28691.12
Product Type Profit Measure (TPC-H Q9)                       22471.19
Forecasting Revenue Change (TPC-H Q10)                       15240.33
Important Stock Identification (TPC-H Q11)                    1472.39
Shipping Modes and Order Priority (TPC-H Q12)                20921.31
Customer Distribution (TPC-H Q13)                            72464.24
Forecasting Revenue Change (TPC-H Q14)                       15833.20
Top Supplier Query (TPC-H Q15)                              124102.32
Parts/Supplier Relationship (TPC-H Q16)                       2563.40
Small-Quantity-Order Revenue (TPC-H Q17)                      3626.70
Large Volume Customer (TPC-H Q18)                            18347.22
Discounted Revenue (TPC-H Q19)                                1289.25
Potential Part Promotion (TPC-H Q20)                          2380.03
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          11265.65
Global Sales Opportunity Query (TPC-H Q22)                    1541.46

### Loading [s]
                  timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-64-1-1          18.0          700.0         3.0     7376.0    8103.0

### Geometric Mean of Medians of Timer Run [s]
                  Geo Times [s]
DBMS                           
MySQL-BHT-64-1-1           9.93

### Power@Size ((3600*SF)/(geo times))
                  Power@Size [~Q/h]
DBMS                               
MySQL-BHT-64-1-1            1101.39

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                              time [s]  count   SF  Throughput@Size
DBMS           SF  num_experiment num_client                                       
MySQL-BHT-64-1 3.0 1              1                503      1  3.0           472.37

### Workflow
                       orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MySQL-BHT-64-1-1  MySQL-BHT-64-1  3.0     8               1           1       1771400377     1771400880

#### Actual
DBMS MySQL-BHT-64 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-64 - Pods [[1]]

### Ingestion - Loader
                CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-64-1        15.4     0.09          0.01                 0.39

### Execution - SUT
                CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-64-1      518.86     1.02         31.53                 64.0

### Execution - Benchmarker
                CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-64-1       14.25     0.01          0.32                 0.32

### Application Metrics
                InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-BHT-64-1                          0.52                       0.7                     0.0               0.04                    0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```


### TPC-DS

Example:
```bash
nohup python tpcds.py -ms 1 -dt -tr -lr 64Gi \
  -rr 64Gi -lr 64Gi \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_run_mysql_appmetrics.log &
```

doc_tpcds_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 24521s 
    Code: 1771584628
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-64-1-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:146007
    datadisk:46385
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    eval_parameters
        code:1771584628

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MySQL-BHT-64-1-1
TPC-DS Q1                 66.10
TPC-DS Q2              60220.98
TPC-DS Q3                137.65
TPC-DS Q4             503216.44
TPC-DS Q5             163976.58
TPC-DS Q6            1192587.67
TPC-DS Q7             121009.76
TPC-DS Q8               3768.93
TPC-DS Q9              48573.80
TPC-DS Q10              1275.05
TPC-DS Q11            307173.99
TPC-DS Q12              4030.35
TPC-DS Q13             13439.28
TPC-DS Q14a+b         688603.48
TPC-DS Q15              2526.26
TPC-DS Q16              1417.31
TPC-DS Q17              7777.87
TPC-DS Q18              6189.38
TPC-DS Q19              4165.34
TPC-DS Q20              7502.47
TPC-DS Q21            324885.54
TPC-DS Q22             58184.25
TPC-DS Q23a+b         450748.22
TPC-DS Q24a+b          56284.81
TPC-DS Q25              1968.09
TPC-DS Q26              3136.60
TPC-DS Q27             39105.28
TPC-DS Q28             37904.14
TPC-DS Q29              1980.07
TPC-DS Q30             14123.61
TPC-DS Q31            162051.11
TPC-DS Q32              7073.27
TPC-DS Q33              3151.79
TPC-DS Q34             12652.11
TPC-DS Q35             28830.66
TPC-DS Q36             18518.01
TPC-DS Q37                52.79
TPC-DS Q38            115703.93
TPC-DS Q39a+b          23416.22
TPC-DS Q40              2450.99
TPC-DS Q41             25096.43
TPC-DS Q42              3247.70
TPC-DS Q43                 4.08
TPC-DS Q44                 2.50
TPC-DS Q45              1797.58
TPC-DS Q46             16107.99
TPC-DS Q47             56185.08
TPC-DS Q48             15909.86
TPC-DS Q49              5017.69
TPC-DS Q50               245.43
TPC-DS Q51             84646.87
TPC-DS Q52              3301.94
TPC-DS Q53              4001.20
TPC-DS Q54             36753.10
TPC-DS Q55              4483.47
TPC-DS Q56              2868.10
TPC-DS Q57             49502.50
TPC-DS Q58             92699.12
TPC-DS Q59             93902.42
TPC-DS Q60              6354.53
TPC-DS Q61              7882.74
TPC-DS Q62             41476.71
TPC-DS Q63              3648.79
TPC-DS Q64              4987.81
TPC-DS Q65            108494.90
TPC-DS Q66             30721.71
TPC-DS Q67            122478.74
TPC-DS Q68              3806.31
TPC-DS Q69              5890.99
TPC-DS Q70            180052.64
TPC-DS Q71              7001.48
TPC-DS Q72            193325.23
TPC-DS Q73              4028.17
TPC-DS Q74             71237.17
TPC-DS Q75             22856.29
TPC-DS Q76              7991.00
TPC-DS Q77            127451.14
TPC-DS Q78            158176.91
TPC-DS Q79             11742.77
TPC-DS Q80            117803.97
TPC-DS Q81             61424.18
TPC-DS Q82                70.30
TPC-DS Q83             10457.95
TPC-DS Q84               466.89
TPC-DS Q85              2957.11
TPC-DS Q86             16190.82
TPC-DS Q87            117585.01
TPC-DS Q88            145850.46
TPC-DS Q89             28527.88
TPC-DS Q90             19509.30
TPC-DS Q91               189.89
TPC-DS Q92               249.87
TPC-DS Q93               412.04
TPC-DS Q94              6060.08
TPC-DS Q95             47188.21
TPC-DS Q96              9758.15
TPC-DS Q97             84372.43
TPC-DS Q98             15624.73
TPC-DS Q99             78621.16

### Loading [s]
                  timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-64-1-1           1.0          929.0         8.0    17291.0   18235.0

### Geometric Mean of Medians of Timer Run [s]
                  Geo Times [s]
DBMS                           
MySQL-BHT-64-1-1          11.68

### Power@Size ((3600*SF)/(geo times))
                  Power@Size [~Q/h]
DBMS                               
MySQL-BHT-64-1-1             926.25

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                              time [s]  count   SF  Throughput@Size
DBMS           SF  num_experiment num_client                                       
MySQL-BHT-64-1 3.0 1              1               6894      1  3.0           155.09

### Workflow
                       orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
MySQL-BHT-64-1-1  MySQL-BHT-64-1  3.0     8               1           1       1771602183     1771609077

#### Actual
DBMS MySQL-BHT-64 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-64 - Pods [[1]]

### Ingestion - Loader
                CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-64-1        11.1     0.02          0.01                 2.66

### Execution - SUT
                CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-64-1    12119.43     2.07         52.82                 64.0

### Execution - Benchmarker
                CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-64-1       32.71     0.32          0.43                 0.44

### Application Metrics
                InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-BHT-64-1                          0.12                      0.66                     0.0               0.03                    0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```



### YCSB

Example:
```bash
nohup python ycsb.py -ms 1 -tr -lr 64Gi \
  -sf 3 \
  --workload a \
  -dbms MySQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_run_mysql_appmetrics.log &
```

doc_ycsb_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=3
    Type: ycsb
    Duration: 29727s 
    Code: 1772594813
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 3000000.
    Ordering of inserts is hashed.
    Number of operations is 3000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [2, 3].
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-64-8-65536-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:189717
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1772594813
MySQL-64-8-65536-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:193158
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1772594813
MySQL-64-8-65536-3 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:196600
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1772594813
MySQL-64-8-65536-4 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:200042
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1772594813

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
MySQL-64-8-65536               1       64   65536          8           0                      637.60476              4706572.0             3000000                            284511.0

### Execution
                    experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
MySQL-64-8-65536-1               1       64   32768          1           0                         529.89              5661502.0           1500463                            1256.0             1499537                           3960831.0
MySQL-64-8-65536-2               1       64   32768          8           0                         500.53              6028037.0           1500052                            1253.0             1499948                           4218879.0
MySQL-64-8-65536-3               1       64   49152          1           0                         492.92              6086213.0           1499910                            1273.0             1500090                           4235263.0
MySQL-64-8-65536-4               1       64   49152          8           0                         489.67              6168830.0           1500586                            1275.0             1499414                           4304895.0

### Workflow

#### Actual
DBMS MySQL-64-8-65536 - Pods [[1, 8, 1, 8]]

#### Planned
DBMS MySQL-64-8-65536 - Pods [[1, 8, 1, 8]]

### Monitoring

### Loading phase: SUT deployment
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1      2385.9     0.64         25.66                35.76
MySQL-64-8-65536-2      2385.9     0.64         25.66                35.76
MySQL-64-8-65536-3      2385.9     0.64         25.66                35.76
MySQL-64-8-65536-4      2385.9     0.64         25.66                35.76

### Loading phase: component loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1       763.7     0.94          0.13                 0.13
MySQL-64-8-65536-2       763.7     0.94          0.13                 0.13
MySQL-64-8-65536-3       763.7     0.94          0.13                 0.13
MySQL-64-8-65536-4       763.7     0.94          0.13                 0.13

### Execution phase: SUT deployment
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1     1574.08     0.30         25.83                40.31
MySQL-64-8-65536-2     1586.40     0.31         26.00                44.86
MySQL-64-8-65536-3     1585.97     0.32         26.16                49.40
MySQL-64-8-65536-4     1584.90     0.31         26.31                53.93

### Execution phase: component benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1      591.11     1.06          0.16                 0.16
MySQL-64-8-65536-2      589.36     0.37          0.15                 0.15
MySQL-64-8-65536-3      594.44     0.12          0.16                 0.16
MySQL-64-8-65536-4      598.05     0.36          0.15                 0.16

### Application Metrics

#### Loading phase: SUT deployment
                    InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-64-8-65536-1                           1.0                    691.86                    0.04                  0                      0
MySQL-64-8-65536-2                           1.0                    691.86                    0.04                  0                      0
MySQL-64-8-65536-3                           1.0                    691.86                    0.04                  0                      0
MySQL-64-8-65536-4                           1.0                    691.86                    0.04                  0                      0

#### Execution phase: SUT deployment
                    InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-64-8-65536-1                           1.0                    566.32                    0.04                0.0                    0.0
MySQL-64-8-65536-2                           0.0                    573.00                    0.04                0.0                    0.0
MySQL-64-8-65536-3                           0.0                    590.40                    0.04                0.0                    0.0
MySQL-64-8-65536-4                           0.0                    548.30                    0.04                0.0                    0.0

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```








## CockroachDB

### YCSB

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  -sfo 10 \
  -nw 3 \
  -nwr 3 \
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
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_ycsb_run_cockroachdb_appmetrics.log &
```

doc_ycsb_run_cockroachdb_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=10
    Type: ycsb
    Duration: 2373s 
    Code: 1772582969
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 10000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-64-8-65536-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147519
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1241112
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1286031
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    worker 2
        RAM:1081649823744
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:340146
        volume_size:1000G
        volume_used:283G
        cpu_list:0-55
    eval_parameters
        code:1772582969
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
CockroachDB-64-8-65536               1       64   65536          8           0                   11044.001737               906372.0            10000000                             36739.0

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
CockroachDB-64-8-65536-1               1       64   65536          1           0                       11407.91               876585.0           4998723                            8287.0             5001277                            164863.0

### Workflow

#### Actual
DBMS CockroachDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS CockroachDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component worker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1    17936.67    22.76         20.38                58.57

### Loading phase: component loader
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1       874.6      1.4          0.11                 0.11

### Execution phase: component worker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1    18645.75    22.97          22.2                62.33

### Execution phase: component benchmarker
                          CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-64-8-65536-1      632.17     0.75          0.13                 0.13

### Application Metrics

#### Loading phase: component worker
                          Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-64-8-65536-1                                   42555.88                  31441801.98                                      0                                        0                                0

#### Execution phase: component worker
                          Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-64-8-65536-1                                   19133.88                  12917918.59                                      0                                        0                                0

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```


### Benchbase's TPC-C

Example:
```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_cockroachdb_appmetrics.log &
```

doc_benchbase_run_cockroachdb_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1571s 
    Code: 1772591339
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['CockroachDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
CockroachDB-1-1-1024-1 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147520
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1240196
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:399212
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1281080
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1772591339
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147520
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:2164173176832
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1240363
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:540579303424
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:399390
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1077382688768
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1281172
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1772591339
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    266.609977                 265.453310         0.0                                                     124961.0                                              59993.0
CockroachDB-1-1-1024-2-1               1          8    8192       2      1  300.0           0                    104.399971                 103.933304         0.0                                                     162332.0                                              76598.0
CockroachDB-1-1-1024-2-2               1          8    8192       2      2  300.0           0                    106.676663                 106.203330         0.0                                                     161278.0                                              74979.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         16   16384          1  300.0           0                        266.61                     265.45         0.0                                                     124961.0                                              59993.0
CockroachDB-1-1-1024-2               1         16   16384          2  300.0           0                        211.08                     210.14         0.0                                                     162332.0                                              75788.5

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1      254.0        1.0   1.0         226.771654
CockroachDB-1-1-1024-2      254.0        1.0   2.0         226.771654

### Monitoring

### Loading phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1      2330.7     18.1          6.52                 10.3
CockroachDB-1-1-1024-2      2330.7     18.1          6.52                 10.3

### Loading phase: component loader
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1     1256.16    12.42          0.25                 0.25
CockroachDB-1-1-1024-2     1256.16    12.42          0.25                 0.25

### Execution phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1     3011.34    11.59          7.84                11.82
CockroachDB-1-1-1024-2     2412.10     9.91          6.52                10.91

### Execution phase: component benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1      144.19     0.50          0.29                 0.29
CockroachDB-1-1-1024-2      144.19     0.84          0.29                 0.29

### Application Metrics

#### Loading phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                     1149.1                   12026477.3                                      0                                        0                                0
CockroachDB-1-1-1024-2                                     1149.1                   12026477.3                                      0                                        0                                0

#### Execution phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                   12878.18                   3373575.38                                      0                                        0                                0
CockroachDB-1-1-1024-2                                    6218.44                   2567988.43                                      0                                        0                                0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```





## Redis

### YCSB

Example:
```bash
nohup python ycsb.py -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_ycsb_run_redis_appmetrics.log &
```

doc_ycsb_run_redis_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 574s 
    Code: 1772796836
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 10000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [12].
    Factors for benchmarking are [4].
    Experiment uses bexhoma version 0.8.22.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['Redis'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [128] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
Redis-64-8-196608-1 uses docker image redis:7.4.2
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147806
    cpu_list:0-63
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1156453
        cpu_list:0-95
    worker 1
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:330073
        cpu_list:0-55
    worker 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:411568
        cpu_list:0-127
    worker 3
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1286179
        cpu_list:0-255
    worker 4
        RAM:1081965416448
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1307312
        cpu_list:0-255
    worker 5
        RAM:1081853952000
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:414951
        cpu_list:0-127
    eval_parameters
        code:1772796836
        BEXHOMA_REPLICAS:1
        BEXHOMA_WORKERS:3

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   26064.186909                38595.0             1000000                              4865.5

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1               1      128   65536          1           0                       61076.54               163729.0           5001247                            3595.0             4998753                              3595.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component worker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      182.23     2.42          3.53                 3.54

### Loading phase: component loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1       77.11        0          0.12                 0.12

### Execution phase: component worker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      470.22     4.22          3.73                 3.79

### Execution phase: component benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      501.08     4.83           0.3                  0.3

### Application Metrics

#### Loading phase: component worker
                     Redis Cluster State  Connected Clients [count]  Redis Memory Used [Gi]  Redis Master Link Status  Redis Operations Rate [ops/s]
Redis-64-8-196608-1                    6                        201                    3.47                         3                        5923.78

#### Execution phase: component worker
                     Redis Cluster State  Connected Clients [count]  Redis Memory Used [Gi]  Redis Master Link Status  Redis Operations Rate [ops/s]
Redis-64-8-196608-1                    6                        437                     3.5                         3                        7442.91

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```









## TiDB

### YCSB

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
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_ycsb_run_tidb_appmetrics.log &
```

doc_ycsb_run_tidb_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1241s 
    Code: 1772624660
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
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['TiDB'].
    Import is handled by 8 processes (pods).
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
TiDB-64-8-16384-1 uses docker image pingcap/tidb:v7.1.0
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:1385144
    cpu_list:0-223
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    sut 0
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1385360
        cpu_list:0-223
    sut 1
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:410240
        cpu_list:0-127
    sut 2
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:342523
        cpu_list:0-55
    pd 0
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:342522
        cpu_list:0-55
    pd 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1385144
        cpu_list:0-223
    pd 2
        RAM:1081853952000
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:427848
        cpu_list:0-127
    tikv 0
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1385144
        cpu_list:0-223
    tikv 1
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:342523
        cpu_list:0-55
    tikv 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:410240
        cpu_list:0-127
    eval_parameters
        code:1772624660
        BEXHOMA_REPLICAS:3
        BEXHOMA_WORKERS:3

### Loading
                 experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
TiDB-64-8-16384               1       64   16384          8           0                    11535.45218                88459.0             1000000                             50735.0

### Execution
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
TiDB-64-8-16384-1               1       64   16384          1           0                         1653.8               604669.0            500690                            2909.0              499310                            254463.0

### Workflow

#### Actual
DBMS TiDB-64-8-16384 - Pods [[1]]

#### Planned
DBMS TiDB-64-8-16384 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      596.03     8.29          1.08                 1.96

### Loading phase: component pd
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1        50.4     0.64          0.29                 0.29

### Loading phase: component tikv
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      170.21     2.66          5.11                11.71

### Loading phase: component loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       93.03     1.48          0.24                 0.24

### Execution phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1     1009.25     4.16          1.98                 2.86

### Execution phase: component pd
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      135.89     0.41           0.3                  0.3

### Execution phase: component tikv
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1      799.28     2.69          8.37                21.89

### Execution phase: component benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-64-8-16384-1       67.25     0.29          0.14                 0.14

### Application Metrics

#### Loading phase: SUT deployment
                   TiDB SQL Statement Throughput [ops/s]  TiDB Avg Query Duration [ms]
TiDB-64-8-16384-1                                4060.77                          5.63

#### Loading phase: component pd
                   PD Cluster Leader Count  PD Leader Balance Actions [ops]
TiDB-64-8-16384-1                       63                               14

#### Loading phase: component tikv
                   TiKV Store Used [%]  TiKV Compaction Time Median [s]  TiKV Compaction Flow [Gi]  TiKV Compaction Pending [Gi]
TiDB-64-8-16384-1                 0.25                         59885127                       3.84                          1.44

#### Execution phase: SUT deployment
                   TiDB SQL Statement Throughput [ops/s]  TiDB Avg Query Duration [ms]
TiDB-64-8-16384-1                                3051.81                         19.69

#### Execution phase: component pd
                   PD Cluster Leader Count  PD Leader Balance Actions [ops]
TiDB-64-8-16384-1                       68                                2

#### Execution phase: component tikv
                   TiKV Store Used [%]  TiKV Compaction Time Median [s]  TiKV Compaction Flow [Gi]  TiKV Compaction Pending [Gi]
TiDB-64-8-16384-1                 0.36                         52127188                       2.41                          0.96

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component pd contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component tikv contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```


### Benchbase's TPC-C

Example:
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
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_tidb_appmetrics.log &
```

doc_benchbase_run_tidb_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1849s 
    Code: 1772625941
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['TiDB'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
TiDB-1-1-1024-1 uses docker image pingcap/tidb:v7.1.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:148452
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    sut 0
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148452
        cpu_list:0-63
    sut 1
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148452
        cpu_list:0-63
    sut 2
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148452
        cpu_list:0-63
    pd 0
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1393182
        cpu_list:0-223
    pd 1
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:347735
        cpu_list:0-55
    pd 2
        RAM:1081853952000
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:427849
        cpu_list:0-127
    tikv 0
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:1413646
        cpu_list:0-223
    tikv 1
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:347735
        cpu_list:0-55
    tikv 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:413382
        cpu_list:0-127
    eval_parameters
                code:1772625941
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
TiDB-1-1-1024-2 uses docker image pingcap/tidb:v7.1.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:148452
    cpu_list:0-63
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    sut 0
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148452
        cpu_list:0-63
    sut 1
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148452
        cpu_list:0-63
    sut 2
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148452
        cpu_list:0-63
    pd 0
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:718762
        cpu_list:0-223
    pd 1
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:345947
        cpu_list:0-55
    pd 2
        RAM:1081853952000
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:427849
        cpu_list:0-127
    tikv 0
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:718764
        cpu_list:0-223
    tikv 1
        RAM:1081649823744
        CPU:AMD EPYC 7453 28-Core Processor
        Cores:56
        host:6.8.0-90-generic
        node:cl-worker34
        disk:345947
        cpu_list:0-55
    tikv 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:411310
        cpu_list:0-127
    eval_parameters
                code:1772625941
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                   experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                               
TiDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    153.976643                 153.219977         0.0                                                     245805.0                                             103887.0
TiDB-1-1-1024-2-2               1          8    8192       2      1  300.0           0                     50.433331                  50.063331         0.0                                                     298438.0                                             158586.0
TiDB-1-1-1024-2-1               1          8    8192       2      2  300.0           0                     50.503329                  50.219995         0.0                                                     298906.0                                             158346.0

#### Aggregated Parallel
                 experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
TiDB-1-1-1024-1               1         16   16384          1  300.0           0                        153.98                     153.22         0.0                                                     245805.0                                             103887.0
TiDB-1-1-1024-2               1         16   16384          2  300.0           0                        100.94                     100.28         0.0                                                     298906.0                                             158466.0

### Workflow

#### Actual
DBMS TiDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS TiDB-1-1-1024 - Pods [[1, 2]]

### Loading
                 time_load  terminals  pods  Throughput [SF/h]
TiDB-1-1-1024-1      656.0        1.0   1.0          87.804878
TiDB-1-1-1024-2      656.0        1.0   2.0          87.804878

### Monitoring

### Loading phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     2098.32     4.71          0.77                 1.04
TiDB-1-1-1024-2     2098.32     4.71          0.77                 1.04

### Loading phase: component pd
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      108.99     0.18          0.29                 0.29
TiDB-1-1-1024-2      108.99     0.18          0.29                 0.29

### Loading phase: component tikv
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1980.27     4.35          9.84                 28.9
TiDB-1-1-1024-2     1980.27     4.35          9.84                 28.9

### Loading phase: component loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      593.24     3.29          0.34                 0.34
TiDB-1-1-1024-2      593.24     3.29          0.34                 0.34

### Execution phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1799.72     7.43          0.86                 1.13
TiDB-1-1-1024-2     1260.18     4.65          2.38                 2.65

### Execution phase: component pd
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      113.90     0.45          0.29                  0.3
TiDB-1-1-1024-2       94.74     0.36          0.30                  0.3

### Execution phase: component tikv
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      705.14     3.29         12.23                31.80
TiDB-1-1-1024-2      504.90     2.04         12.54                26.39

### Execution phase: component benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      141.91     0.77          0.29                 0.29
TiDB-1-1-1024-2      141.91     0.67          0.29                 0.29

### Application Metrics

#### Loading phase: SUT deployment
                 TiDB SQL Statement Throughput [ops/s]  TiDB Avg Query Duration [ms]
TiDB-1-1-1024-1                                 227.29                         64.54
TiDB-1-1-1024-2                                 227.29                         64.54

#### Loading phase: component pd
                 PD Cluster Leader Count  PD Leader Balance Actions [ops]
TiDB-1-1-1024-1                      109                               76
TiDB-1-1-1024-2                      109                               76

#### Loading phase: component tikv
                 TiKV Store Used [%]  TiKV Compaction Time Median [s]  TiKV Compaction Flow [Gi]  TiKV Compaction Pending [Gi]
TiDB-1-1-1024-1                 0.33                        514707.84                       14.4                          1.22
TiDB-1-1-1024-2                 0.33                        514707.84                       14.4                          1.22

#### Execution phase: SUT deployment
                 TiDB SQL Statement Throughput [ops/s]  TiDB Avg Query Duration [ms]
TiDB-1-1-1024-1                                3827.00                         62.67
TiDB-1-1-1024-2                                1445.08                         11.10

#### Execution phase: component pd
                 PD Cluster Leader Count  PD Leader Balance Actions [ops]
TiDB-1-1-1024-1                    111.0                              2.0
TiDB-1-1-1024-2                    111.0                              0.0

#### Execution phase: component tikv
                 TiKV Store Used [%]  TiKV Compaction Time Median [s]  TiKV Compaction Flow [Gi]  TiKV Compaction Pending [Gi]
TiDB-1-1-1024-1                 0.37                          80400.0                       2.36                          0.72
TiDB-1-1-1024-2                 0.41                          70563.0                       0.09                          0.00

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component pd contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component tikv contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```






## PGBouncer

### YCSB

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rr 64Gi -lr 64Gi \
  -tb 16384 \
  -nlp 16 \
  -nlt 64 \
  -nlf 11 \
  -nbp 16 \
  -nbt 128 \
  -nbf 11 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -npp 4 \
  -npi 128 \
  -npo 64 \
  run </dev/null &>$LOG_DIR/doc_ycsb_run_pgbouncer_appmetrics.log &
```

doc_ycsb_run_pgbouncer_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=16
    Type: ycsb
    Duration: 1778s 
    Code: 1772587497
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
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
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
pgb-64-4-128-64-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:185735
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1772587497

### Loading
                 experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
pgb-64-4-128-64               1       64  180224         16           0                   31685.999617               511871.0            16000000                             5594.25

### Execution
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)
pgb-64-4-128-64-1               1      128  180224         16           0                       61934.42               261601.0          16000000                            3171.0

### Workflow

#### Actual
DBMS pgb-64-4-128-64 - Pods [[16]]

#### Planned
DBMS pgb-64-4-128-64 - Pods [[16]]

### Monitoring

### Loading phase: component pool
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1        1.54      0.0          0.06                 0.06

### Loading phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1      3721.9     7.78         24.08                42.36

### Loading phase: component loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     1263.84     2.77          0.11                 0.11

### Execution phase: component pool
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1        0.35      0.0          0.05                 0.05

### Execution phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     2544.35    17.02         26.76                45.03

### Execution phase: component benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     1160.24     6.93           0.1                 0.11

### Application Metrics

#### Loading phase: component pool
                   PgBouncer Query Throughput [queries/s]  PgBouncer Waiting Clients [s]  PgBouncer Waiting Clients [clients]  PgBouncer Idle Connections [connections]  PgBouncer Pool Load Pressure [%]
pgb-64-4-128-64-1                                33700.13                           0.59                                    0                                       162                             100.0

#### Loading phase: SUT deployment
                   Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
pgb-64-4-128-64-1                      257                                       0                                               0                         64                                     64

#### Execution phase: component pool
                   PgBouncer Query Throughput [queries/s]  PgBouncer Waiting Clients [s]  PgBouncer Waiting Clients [clients]  PgBouncer Idle Connections [connections]  PgBouncer Pool Load Pressure [%]
pgb-64-4-128-64-1                                58141.36                           0.11                                    0                                        33                             100.0

#### Execution phase: SUT deployment
                   Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
pgb-64-4-128-64-1                      256                                       0                                               0                         12                                     13

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


### Benchbase's TPC-C

Example:
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
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_pgbouncer_appmetrics.log &
```

doc_benchbase_run_pgbouncer_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1815s 
    Code: 1772592948
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. There is a reconnect for each transaction. Benchmarking runs for 10 minutes.
    Experiment uses bexhoma version 0.8.21.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
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
pgb-1-2-32-32-1 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:151827
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772592948
pgb-1-2-32-32-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:152104
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772592948

### Execution

#### Per Pod
                   experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                               
pgb-1-2-32-32-1-1               1         32   16384       1      1  600.0           3                   1474.916647                 467.353327         0.0                                                      36458.0                                              21692.0
pgb-1-2-32-32-2-1               1         16    8192       2      1  600.0           1                    640.718304                 447.353313         0.0                                                      48435.0                                              24965.0
pgb-1-2-32-32-2-2               1         16    8192       2      2  600.0           0                    620.064947                 447.126629         0.0                                                      48819.0                                              25796.0

#### Aggregated Parallel
                 experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
pgb-1-2-32-32-1               1         32   16384          1  600.0           3                       1474.92                     467.35         0.0                                                      36458.0                                              21692.0
pgb-1-2-32-32-2               1         32   16384          2  600.0           1                       1260.78                     894.48         0.0                                                      48819.0                                              25380.5

### Workflow

#### Actual
DBMS pgb-1-2-32-32 - Pods [[1, 2]]

#### Planned
DBMS pgb-1-2-32-32 - Pods [[1, 2]]

### Loading
                 time_load  terminals  pods  Throughput [SF/h]
pgb-1-2-32-32-1      148.0        1.0   1.0         389.189189
pgb-1-2-32-32-2      148.0        1.0   2.0         389.189189

### Monitoring

### Loading phase: component pool
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1         0.4      0.0          0.03                 0.03
pgb-1-2-32-32-2         0.4      0.0          0.03                 0.03

### Loading phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1       704.7     6.73          4.72                 6.36
pgb-1-2-32-32-2       704.7     6.73          4.72                 6.36

### Loading phase: component loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1     1204.44    13.06          0.26                 0.26
pgb-1-2-32-32-2     1204.44    13.06          0.26                 0.26

### Execution phase: component pool
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1        1.03      0.0          0.03                 0.03
pgb-1-2-32-32-2        1.09      0.0          0.03                 0.03

### Execution phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1     2057.56     4.15          5.00                 6.89
pgb-1-2-32-32-2     4108.60     7.75          5.53                 7.86

### Execution phase: component benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1    13656.64    25.48          0.53                 0.53
pgb-1-2-32-32-2    13656.64    32.91          0.53                 0.53

### Application Metrics

#### Loading phase: component pool
                 PgBouncer Query Throughput [queries/s]  PgBouncer Waiting Clients [s]  PgBouncer Waiting Clients [clients]  PgBouncer Idle Connections [connections]  PgBouncer Pool Load Pressure [%]
pgb-1-2-32-32-1                                  223.43                           0.61                                    0                                        48                             100.0
pgb-1-2-32-32-2                                  223.43                           0.61                                    0                                        48                             100.0

#### Loading phase: SUT deployment
                 Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
pgb-1-2-32-32-1                       65                                       0                                               0                         16                                     15
pgb-1-2-32-32-2                       65                                       0                                               0                         16                                     15

#### Execution phase: component pool
                 PgBouncer Query Throughput [queries/s]  PgBouncer Waiting Clients [s]  PgBouncer Waiting Clients [clients]  PgBouncer Idle Connections [connections]  PgBouncer Pool Load Pressure [%]
pgb-1-2-32-32-1                                 9629.75                           0.51                                  0.0                                      57.0                             100.0
pgb-1-2-32-32-2                                19082.34                           0.13                                  0.0                                      55.0                             100.0

#### Execution phase: SUT deployment
                 Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
pgb-1-2-32-32-1                     65.0                                    21.0                                             0.0                       16.0                                   15.0
pgb-1-2-32-32-2                     64.0                                    21.0                                             0.0                       19.0                                   19.0

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: component pool contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component pool contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```




## YugabyteDB

Make sure to have YugabyteDB installed [externally](https://bexhoma.readthedocs.io/en/latest/Example-YugaByteDB.html), because bexhoma does not manage it.

### YCSB

Example:
```bash
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_ycsb_run_yugabytedb_appmetrics.log &
```

doc_ycsb_run_yugabytedb_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 949s 
    Code: 1772721387
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
    Experiment uses bexhoma version 0.8.22.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['YugabyteDB'].
    Import is handled by 8 processes (pods).
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:745494
    cpu_list:0-223
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1772721387

### Loading
                       experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
YugabyteDB-64-8-65536               1       64   65536          8           0                   21126.562218                47969.0             1000000                             15194.0

### Execution
                         experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
YugabyteDB-64-8-65536-1               1       64   65536          1           0                       20796.25               480856.0           5000690                           48671.0             4999310                             62367.0

### Workflow

#### Actual
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned
DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component yb-tserver
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1    22723.47    17.78          6.71                14.72

### Loading phase: component yb-master
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1       61.57     0.04          0.34                 0.37

### Loading phase: component loader
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1       58.92     0.95          0.23                 0.23

### Execution phase: component yb-tserver
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1    13361.53    31.92         10.25                 21.3

### Execution phase: component yb-master
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1        14.9     0.05          0.24                 0.27

### Execution phase: component benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-64-8-65536-1      348.42     0.87          0.13                 0.14

### Application Metrics

#### Loading phase: component yb-tserver
                         YSQL Query Throughput [ops/s]  Tablet Read Latency [ms]  Tablet Write Latency [ms]  Active YSQL Connections  TServer Follower Lag [ms]
YugabyteDB-64-8-65536-1                        3872.35                      0.27                       2.57                        0                       3036

#### Loading phase: component yb-master
                         YB-Master RPC Throughput [ops/s]  YB-Master Avg RPC Latency [ms]  Table Metadata Operations [ops/s]  YB-Master Clock Error  Tablet Location Requests [ops/s]
YugabyteDB-64-8-65536-1                              0.03                            0.41                                0.0              500926000                              0.02

#### Execution phase: component yb-tserver
                         YSQL Query Throughput [ops/s]  Tablet Read Latency [ms]  Tablet Write Latency [ms]  Active YSQL Connections  TServer Follower Lag [ms]
YugabyteDB-64-8-65536-1                       18575.42                      0.61                        2.8                        0                        596

#### Execution phase: component yb-master
                         YB-Master RPC Throughput [ops/s]  YB-Master Avg RPC Latency [ms]  Table Metadata Operations [ops/s]  YB-Master Clock Error  Tablet Location Requests [ops/s]
YugabyteDB-64-8-65536-1                              0.02                            0.41                                0.0              501021000                              0.02

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```



### Benchbase's TPC-C

Example:
```bash
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms YugabyteDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_yugabytedb_appmetrics.log &
```

doc_benchbase_run_yugabytedb_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1086s 
    Code: 1772720146
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.22.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['YugabyteDB'].
    Import is handled by 1 processes (pods).
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
YugabyteDB-1-1-1024-1 uses docker image postgres:15.0
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:746847
    cpu_list:0-223
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772720146
YugabyteDB-1-1-1024-2 uses docker image postgres:15.0
    RAM:2164173176832
    CPU:INTEL(R) XEON(R) PLATINUM 8570
    Cores:224
    host:6.8.0-90-generic
    node:cl-worker36
    disk:763518
    cpu_list:0-223
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772720146

### Execution

#### Per Pod
                         experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                     
YugabyteDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    339.639960                 338.106627         0.0                                                     116768.0                                              47090.0
YugabyteDB-1-1-1024-2-1               1          8    8192       2      1  300.0           0                    180.176657                 179.353324         0.0                                                     104688.0                                              44384.0
YugabyteDB-1-1-1024-2-2               1          8    8192       2      2  300.0           1                    185.809957                 184.956624         0.0                                                     103239.0                                              43041.0

#### Aggregated Parallel
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
YugabyteDB-1-1-1024-1               1         16   16384          1  300.0           0                        339.64                     338.11         0.0                                                     116768.0                                              47090.0
YugabyteDB-1-1-1024-2               1         16   16384          2  300.0           1                        365.99                     364.31         0.0                                                     104688.0                                              43712.5

### Workflow

#### Actual
DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
YugabyteDB-1-1-1024-1      107.0        1.0   1.0         538.317757
YugabyteDB-1-1-1024-2      107.0        1.0   2.0         538.317757

### Monitoring

### Loading phase: component yb-tserver
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1     2247.78    21.94          7.59                15.47
YugabyteDB-1-1-1024-2     3912.93    27.88          8.07                16.06

### Loading phase: component yb-master
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1        8.74     0.06          0.25                 0.27
YugabyteDB-1-1-1024-2       14.97     0.06          0.26                 0.29

### Loading phase: component loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1      149.45     3.11          0.26                 0.26
YugabyteDB-1-1-1024-2      149.45     3.11          0.26                 0.26

### Execution phase: component yb-tserver
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1     8889.01    33.17          9.06                18.53
YugabyteDB-1-1-1024-2     9703.40    36.66          9.82                21.75

### Execution phase: component yb-master
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1       12.18     0.06          0.29                 0.32
YugabyteDB-1-1-1024-2       16.55     0.07          0.34                 0.37

### Execution phase: component benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
YugabyteDB-1-1-1024-1      101.25     0.43          0.31                 0.31
YugabyteDB-1-1-1024-2      101.25     0.84          0.56                 0.56

### Application Metrics

#### Loading phase: component yb-tserver
                       YSQL Query Throughput [ops/s]  Tablet Read Latency [ms]  Tablet Write Latency [ms]  Active YSQL Connections  TServer Follower Lag [ms]
YugabyteDB-1-1-1024-1                         243.97                      0.26                      27.12                      0.0                     1632.0
YugabyteDB-1-1-1024-2                        4245.55                      0.35                      27.12                      0.0                     1632.0

#### Loading phase: component yb-master
                       YB-Master RPC Throughput [ops/s]  YB-Master Avg RPC Latency [ms]  Table Metadata Operations [ops/s]  YB-Master Clock Error  Tablet Location Requests [ops/s]
YugabyteDB-1-1-1024-1                              2.58                            1.17                               0.04            502993000.0                              2.54
YugabyteDB-1-1-1024-2                              2.58                            1.17                               0.04            502997000.0                              2.54

#### Execution phase: component yb-tserver
                       YSQL Query Throughput [ops/s]  Tablet Read Latency [ms]  Tablet Write Latency [ms]  Active YSQL Connections  TServer Follower Lag [ms]
YugabyteDB-1-1-1024-1                       11826.25                      0.35                      14.19                        0                        601
YugabyteDB-1-1-1024-2                        4519.30                      0.36                       1.67                        0                        980

#### Execution phase: component yb-master
                       YB-Master RPC Throughput [ops/s]  YB-Master Avg RPC Latency [ms]  Table Metadata Operations [ops/s]  YB-Master Clock Error  Tablet Location Requests [ops/s]
YugabyteDB-1-1-1024-1                              2.56                            0.05                               0.03              502997000                              2.52
YugabyteDB-1-1-1024-2                              0.00                            0.05                               0.00              502030000                              0.00

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```
