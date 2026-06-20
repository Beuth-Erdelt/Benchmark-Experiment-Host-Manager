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
BEXHOMA_MS=1

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [benchbase file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/benchbase.py).

## PostgreSQL

### Benchbase's TPC-C

Example:
```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_postgresql_appmetrics.log
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
    * running for 5 (`-xsd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-xtb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary

### Evaluate Results


doc_benchbase_run_postgresql_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1162s 
* Code: 1781459265
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:207333
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781459265
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:210837
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781459265
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      320.00 |           1.00 |            0.00 |        146.00 |          173.00 |              1 |           1 |             |                |             0 | False         |              180.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 |           0 | 300.00 |           98 |                       11368.45 |                    11192.43 |         0.00 |                                                      34033.00 |                                              14066.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 |           0 | 300.00 |           32 |                        4841.27 |                     4771.42 |         0.00 |                                                      41736.00 |                                              16513.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 |           0 | 300.00 |           32 |                        4924.96 |                     4854.95 |         0.00 |                                                      41805.00 |                                              16236.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |    16384 |               1 |           1 |           0 | 300.00 |           98 |                       11368.45 |                    11192.43 |         0.00 |                                                      34033.00 |                                              14066.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         160 |    16384 |               1 |           2 |           0 | 300.00 |           64 |                        9766.23 |                     9626.37 |         0.00 |                                                      41805.00 |                                              16374.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       573.27 |      8.62 |           0.38 |                  2.98 |
| PostgreSQL-1-1-2-1 |       573.27 |      8.62 |           0.38 |                  2.98 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1502.29 |     14.34 |           0.25 |                  0.25 |
| PostgreSQL-1-1-2-1 |      1502.29 |     14.34 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      7901.93 |     27.76 |           0.98 |                  7.11 |
| PostgreSQL-1-1-2-1 |      6378.33 |     21.60 |           1.05 |                  9.39 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      5159.12 |     18.51 |           1.62 |                  1.62 |
| PostgreSQL-1-1-2-1 |      4919.29 |     35.03 |           1.62 |                  1.62 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       15.00 |                                   14.00 |
| PostgreSQL-1-1-2-1 |                     16.00 |                                     0.00 |                                             0.00 |                       15.00 |                                   14.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      9.00 |                                    75.00 |                                             0.00 |                      162.00 |                                  160.00 |
| PostgreSQL-1-1-2-1 |                      9.00 |                                    53.00 |                                             0.00 |                      161.00 |                                  160.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

The summary shows the first 5 application metrics aggregated per execution run.
An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/dev).



### HammerDB's TPC-C

Example:
```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -xlat \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_appmetrics.log
```

doc_hammerdb_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1334s 
* Code: 1781463910
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:207272
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781463910
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:210953
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781463910

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 2]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 2]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      117.00 |           1.00 |            0.00 |         44.00 |           72.00 |              1 |          16 |             | None           |             0 | False         |              492.31 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 231637 | 533155 |         0.00 |          5 |        0 |       2.65 |       9.72 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        8 |        2 |               1 |       1 | 209201 | 480859 |         0.00 |          5 |        0 |       3.09 |      12.15 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        8 |        2 |               1 |       1 | 209239 | 481428 |         0.00 |          5 |        0 |       3.16 |      12.19 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       16 |        1 |               1 |           1 |       2.65 |       9.72 |         0.00 | 231637.00 | 533155.00 |          5 |        0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |       16 |        2 |               1 |           2 |       3.16 |      12.19 |         0.00 | 209220.00 | 481143.50 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        91.71 |      2.51 |           0.28 |                  2.85 |
| PostgreSQL-1-1-2-1 |        91.71 |      2.51 |           0.28 |                  2.85 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       290.63 |      9.64 |           0.15 |                  0.15 |
| PostgreSQL-1-1-2-1 |       290.63 |      9.64 |           0.15 |                  0.15 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3823.83 |      9.57 |           0.59 |                  6.69 |
| PostgreSQL-1-1-2-1 |      3647.63 |     10.03 |           0.63 |                  9.35 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       607.90 |      1.80 |           1.38 |                  1.38 |
| PostgreSQL-1-1-2-1 |       607.90 |      2.86 |           1.38 |                  1.38 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     16.00 |                                     0.00 |                                             0.00 |                       17.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                     16.00 |                                     0.00 |                                             0.00 |                       17.00 |                                    0.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     11.00 |                                     0.00 |                                             0.00 |                       19.00 |                                    0.00 |
| PostgreSQL-1-1-2-1 |                     10.00 |                                     0.00 |                                             0.00 |                       19.00 |                                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```


### TPC-H

Example:
```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_appmetrics.log
```

doc_tpch_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 595s 
* Code: 1781461542
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:210570
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781461542

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      259.00 |           1.00 |           14.00 |         22.00 |          214.00 |              8 |           0 |             |                |             0 | False         |               41.70 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         60 |            1.68 |             6602.39 |           3960.00 |           0 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         60 |            1.68 |             6602.39 |           3960.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                5089.66 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                1163.28 |
| Shipping Priority (TPC-H Q3)                        |                1811.95 |
| Order Priority Checking Query (TPC-H Q4)            |                 773.47 |
| Local Supplier Volume (TPC-H Q5)                    |                2533.89 |
| Forecasting Revenue Change (TPC-H Q6)               |                1378.17 |
| Forecasting Revenue Change (TPC-H Q7)               |                2488.15 |
| National Market Share (TPC-H Q8)                    |                 963.91 |
| Product Type Profit Measure (TPC-H Q9)              |                6716.80 |
| Forecasting Revenue Change (TPC-H Q10)              |                2330.31 |
| Important Stock Identification (TPC-H Q11)          |                 650.40 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                1888.13 |
| Customer Distribution (TPC-H Q13)                   |                1588.77 |
| Forecasting Revenue Change (TPC-H Q14)              |                1472.84 |
| Top Supplier Query (TPC-H Q15)                      |                1656.21 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 931.08 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                4080.85 |
| Large Volume Customer (TPC-H Q18)                   |                9041.67 |
| Discounted Revenue (TPC-H Q19)                      |                 184.44 |
| Potential Part Promotion (TPC-H Q20)                |                1143.29 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                5337.52 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 251.46 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       205.83 |      3.55 |           0.43 |                  6.22 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.17 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       135.46 |      2.19 |           0.46 |                  6.26 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        16.30 |      0.15 |           0.33 |                  0.33 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        8.00 |                                    7.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        2.00 |                                    3.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```


### TPC-DS

Example:
```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_appmetrics.log
```

doc_tpcds_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 1546s 
* Code: 1781462191
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:212915
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781462191

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1]]

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      493.00 |           1.00 |            0.00 |        141.00 |          344.00 |              8 |           0 |             | None           |             0 | False         |               21.91 |

### Execution

#### Per Connection

|                      | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |        906 |            1.38 |             7882.93 |           1180.13 |          -1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |        906 |            1.38 |             7882.93 |           1180.13 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   PostgreSQL-1-1-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                 356.27 |
| TPC-DS Q2     |                1901.93 |
| TPC-DS Q3     |                 640.71 |
| TPC-DS Q4     |               32464.23 |
| TPC-DS Q5     |                3303.09 |
| TPC-DS Q6     |              224696.05 |
| TPC-DS Q7     |                1379.57 |
| TPC-DS Q8     |                 169.15 |
| TPC-DS Q9     |                8249.72 |
| TPC-DS Q10    |                2307.15 |
| TPC-DS Q11    |               19756.81 |
| TPC-DS Q12    |                 294.36 |
| TPC-DS Q13    |                1797.06 |
| TPC-DS Q14a+b |               13304.64 |
| TPC-DS Q15    |                 666.30 |
| TPC-DS Q16    |                 664.19 |
| TPC-DS Q17    |                1666.29 |
| TPC-DS Q18    |                1282.87 |
| TPC-DS Q19    |                 983.46 |
| TPC-DS Q20    |                 638.78 |
| TPC-DS Q21    |                1095.31 |
| TPC-DS Q22    |               11111.22 |
| TPC-DS Q23a+b |               28278.35 |
| TPC-DS Q24a+b |                2572.52 |
| TPC-DS Q25    |                1449.86 |
| TPC-DS Q26    |                 930.07 |
| TPC-DS Q27    |                  63.71 |
| TPC-DS Q28    |                4970.23 |
| TPC-DS Q29    |                1638.26 |
| TPC-DS Q30    |               75398.08 |
| TPC-DS Q31    |                5634.18 |
| TPC-DS Q32    |                 640.84 |
| TPC-DS Q33    |                1956.82 |
| TPC-DS Q34    |                  60.85 |
| TPC-DS Q35    |                2640.06 |
| TPC-DS Q36    |                1134.99 |
| TPC-DS Q37    |                 930.04 |
| TPC-DS Q38    |                3574.83 |
| TPC-DS Q39a+b |                9181.49 |
| TPC-DS Q40    |                 502.69 |
| TPC-DS Q41    |                2786.31 |
| TPC-DS Q42    |                 617.03 |
| TPC-DS Q43    |                  80.45 |
| TPC-DS Q44    |                   4.07 |
| TPC-DS Q45    |                 395.27 |
| TPC-DS Q46    |                  96.70 |
| TPC-DS Q47    |                4970.10 |
| TPC-DS Q48    |                1898.82 |
| TPC-DS Q49    |                2024.72 |
| TPC-DS Q50    |                1116.72 |
| TPC-DS Q51    |                3239.74 |
| TPC-DS Q52    |                 600.97 |
| TPC-DS Q53    |                 731.19 |
| TPC-DS Q54    |                1211.63 |
| TPC-DS Q55    |                 603.27 |
| TPC-DS Q56    |                1746.17 |
| TPC-DS Q57    |                2077.95 |
| TPC-DS Q58    |                1637.61 |
| TPC-DS Q59    |                2352.65 |
| TPC-DS Q60    |                1577.40 |
| TPC-DS Q61    |                 176.33 |
| TPC-DS Q62    |                 540.78 |
| TPC-DS Q63    |                 675.32 |
| TPC-DS Q64    |                2051.97 |
| TPC-DS Q65    |                2414.51 |
| TPC-DS Q66    |                 979.45 |
| TPC-DS Q67    |                8691.14 |
| TPC-DS Q68    |                  85.82 |
| TPC-DS Q69    |                1199.45 |
| TPC-DS Q70    |                1791.87 |
| TPC-DS Q71    |                1659.26 |
| TPC-DS Q72    |                3030.50 |
| TPC-DS Q73    |                  57.26 |
| TPC-DS Q74    |                6658.89 |
| TPC-DS Q75    |                4975.60 |
| TPC-DS Q76    |                 844.95 |
| TPC-DS Q77    |                1455.01 |
| TPC-DS Q78    |                3294.85 |
| TPC-DS Q79    |                 846.92 |
| TPC-DS Q80    |                1523.61 |
| TPC-DS Q81    |              318326.04 |
| TPC-DS Q82    |                1246.06 |
| TPC-DS Q83    |                 270.36 |
| TPC-DS Q84    |                 172.34 |
| TPC-DS Q85    |                 691.58 |
| TPC-DS Q86    |                 460.38 |
| TPC-DS Q87    |                4085.21 |
| TPC-DS Q88    |                6132.60 |
| TPC-DS Q89    |                 706.66 |
| TPC-DS Q90    |                 700.33 |
| TPC-DS Q91    |                 281.37 |
| TPC-DS Q92    |                 342.69 |
| TPC-DS Q93    |                 825.32 |
| TPC-DS Q94    |                 619.32 |
| TPC-DS Q95    |                8948.80 |
| TPC-DS Q96    |                 583.19 |
| TPC-DS Q97    |                1983.87 |
| TPC-DS Q98    |                 896.92 |
| TPC-DS Q99    |                1106.04 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       415.46 |      5.17 |           0.49 |                  8.82 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        21.77 |      0.26 |           0.01 |                  2.21 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1253.75 |      2.45 |           0.59 |                 10.45 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        20.46 |      0.06 |           0.32 |                  0.32 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    7.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        4.00 |                                    5.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```



### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2,3 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_appmetrics.log
```

doc_ycsb_testcase_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1051s 
* Code: 1781460454
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:209191
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781460454
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:209720
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781460454
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:209816
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781460454
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:209870
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781460454

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Pods [[1, 8, 1, 8]]

#### Planned

* DBMS PostgreSQL-1 - Pods [[1, 8, 1, 8]]

### Loading

#### Per Connection

| connection           |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| PostgreSQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8147.57 |                46026.00 |            375000.00 |                              4663.00 | 3.00 |              234.65 |
| PostgreSQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8149.69 |                46014.00 |            375000.00 |                              4931.00 | 3.00 |              234.71 |
| PostgreSQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8148.45 |                46021.00 |            375000.00 |                              4807.00 | 3.00 |              234.68 |
| PostgreSQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8148.10 |                46023.00 |            375000.00 |                              4691.00 | 3.00 |              234.67 |
| PostgreSQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8150.76 |                46008.00 |            375000.00 |                              4839.00 | 3.00 |              234.74 |
| PostgreSQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8146.68 |                46031.00 |            375000.00 |                              4815.00 | 3.00 |              234.62 |
| PostgreSQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8150.05 |                46012.00 |            375000.00 |                              4763.00 | 3.00 |              234.72 |
| PostgreSQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8152.35 |                45999.00 |            375000.00 |                              4679.00 | 3.00 |              234.79 |

#### Per Run

| DBMS           |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              234.62 |                        65193.66 |                46031.00 |           3000000.00 |                              4773.50 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------|:-----------------|:-------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 | PostgreSQL-1    |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32665.15 |                91841.00 |            1499978 |                             656.00 |              1500022 |                              5463.00 |
| PostgreSQL-1-1-2-1-8 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4084.92 |                91801.00 |             187584 |                             602.00 |               187416 |                              6615.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4081.94 |                91868.00 |             187200 |                             684.00 |               187800 |                              6511.00 |
| PostgreSQL-1-1-2-1-7 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4085.55 |                91787.00 |             187722 |                             596.00 |               187278 |                              6675.00 |
| PostgreSQL-1-1-2-1-5 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4085.77 |                91782.00 |             187341 |                             617.00 |               187659 |                              6631.00 |
| PostgreSQL-1-1-2-1-4 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4085.90 |                91779.00 |             187621 |                             669.00 |               187379 |                              6695.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4085.41 |                91790.00 |             187172 |                             577.00 |               187828 |                              6479.00 |
| PostgreSQL-1-1-2-1-3 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4085.72 |                91783.00 |             187419 |                             677.00 |               187581 |                              6535.00 |
| PostgreSQL-1-1-2-1-6 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 | PostgreSQL-1    |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4086.48 |                91766.00 |             187715 |                             573.00 |               187285 |                              6483.00 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 | PostgreSQL-1    |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        48922.08 |                61322.00 |            1499514 |                             876.00 |              1500486 |                             12495.00 |
| PostgreSQL-1-1-4-1-8 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6112.17 |                61353.00 |             187606 |                             577.00 |               187394 |                              4495.00 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6120.05 |                61274.00 |             187399 |                             574.00 |               187601 |                              4703.00 |
| PostgreSQL-1-1-4-1-7 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6119.75 |                61277.00 |             187019 |                             564.00 |               187981 |                              4519.00 |
| PostgreSQL-1-1-4-1-3 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6111.87 |                61356.00 |             187229 |                             608.00 |               187771 |                              4583.00 |
| PostgreSQL-1-1-4-1-5 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6120.55 |                61269.00 |             187172 |                             582.00 |               187828 |                              4663.00 |
| PostgreSQL-1-1-4-1-4 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6120.25 |                61272.00 |             187723 |                             597.00 |               187277 |                              4695.00 |
| PostgreSQL-1-1-4-1-6 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6120.75 |                61267.00 |             187242 |                             591.00 |               187758 |                              4523.00 |
| PostgreSQL-1-1-4-1-2 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 | PostgreSQL-1    |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6120.05 |                61274.00 |             187726 |                             573.00 |               187274 |                              4771.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32665.15 |                91841.00 |            1499978 |                             656.00 |              1500022 |                              5463.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32681.70 |                91868.00 |            1499774 |                             684.00 |              1500226 |                              6695.00 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        48922.08 |                61322.00 |            1499514 |                             876.00 |              1500486 |                             12495.00 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48945.45 |                61356.00 |            1499116 |                             608.00 |              1500884 |                              4771.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       528.77 |      8.53 |           0.40 |                  4.75 |
| PostgreSQL-1-1-2-1 |       528.77 |      8.53 |           0.40 |                  4.75 |
| PostgreSQL-1-1-3-1 |       528.77 |      8.53 |           0.40 |                  4.75 |
| PostgreSQL-1-1-4-1 |       528.77 |      8.53 |           0.40 |                  4.75 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       141.10 |      1.49 |           0.11 |                  0.11 |
| PostgreSQL-1-1-2-1 |       141.10 |      1.49 |           0.11 |                  0.11 |
| PostgreSQL-1-1-3-1 |       141.10 |      1.49 |           0.11 |                  0.11 |
| PostgreSQL-1-1-4-1 |       141.10 |      1.49 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       580.19 |      7.17 |           0.53 |                  5.46 |
| PostgreSQL-1-1-2-1 |       522.01 |      6.99 |           0.48 |                  5.53 |
| PostgreSQL-1-1-3-1 |       347.03 |     11.17 |           0.48 |                  5.55 |
| PostgreSQL-1-1-4-1 |       314.85 |      8.92 |           0.48 |                  5.60 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       139.96 |      2.12 |           0.13 |                  0.13 |
| PostgreSQL-1-1-2-1 |       177.64 |      5.19 |           0.13 |                  0.13 |
| PostgreSQL-1-1-3-1 |       105.49 |      5.49 |           0.13 |                  0.13 |
| PostgreSQL-1-1-4-1 |       138.63 |      7.67 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     18.00 |                                     0.00 |                                             0.00 |                       47.00 |                                   47.00 |
| PostgreSQL-1-1-2-1 |                     18.00 |                                     0.00 |                                             0.00 |                       47.00 |                                   47.00 |
| PostgreSQL-1-1-3-1 |                     18.00 |                                     0.00 |                                             0.00 |                       47.00 |                                   47.00 |
| PostgreSQL-1-1-4-1 |                     18.00 |                                     0.00 |                                             0.00 |                       47.00 |                                   47.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                     58.00 |                                     0.00 |                                             0.00 |                       13.00 |                                   13.00 |
| PostgreSQL-1-1-2-1 |                     59.00 |                                     0.00 |                                             0.00 |                        9.00 |                                   10.00 |
| PostgreSQL-1-1-3-1 |                     59.00 |                                     0.00 |                                             0.00 |                       15.00 |                                   15.00 |
| PostgreSQL-1-1-4-1 |                     60.00 |                                     0.00 |                                             0.00 |                       10.00 |                                   11.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```



















## MySQL

### Benchbase's TPC-C

Example:
```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_mysql_appmetrics.log
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
    * running for 5 (`-xsd`) minutes
    * each stream (pod) having 16 threads to simulate 16 users (`-nbt`)
    * `-nbp`: first stream 1 pod, second stream 2 pods (8 threads each)
    * target is 16x(`-ltf`) 1024 (`-xtb`) ops
* with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* shows a summary


### Evaluate Results

doc_benchbase_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1316s 
* Code: 1781465271
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:241143
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781465271
    * TENANT_VOL:False
* MySQL-1-1-2-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:256625
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1781465271
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1, 2]]

#### Planned

* DBMS MySQL-1 - Pods [[1, 2]]

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   16 |      314.00 |           0.00 |            0.00 |        148.00 |          166.00 |              1 |           1 |             |                |             0 | False         |              183.44 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |         160 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        8796.05 |                     8655.10 |         0.00 |                                                      35165.00 |                                              18181.00 |
| MySQL-1-1-2-1-1 | MySQL-1-1-2 | MySQL-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                        3794.42 |                     3739.25 |         0.00 |                                                      41906.00 |                                              21074.00 |
| MySQL-1-1-2-1-2 | MySQL-1-1-2 | MySQL-1-1-2-1 |                1 |          80 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                        3958.98 |                     3901.04 |         0.00 |                                                      41742.00 |                                              20198.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |         160 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                        8796.05 |                     8655.10 |         0.00 |                                                      35165.00 |                                              18181.00 |
| MySQL-1-1-2 | MySQL-1-1-2 |                1 |         160 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                        7753.40 |                     7640.30 |         0.00 |                                                      41906.00 |                                              20636.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       391.50 |      5.67 |           9.67 |                 13.10 |
| MySQL-1-1-2-1 |       391.50 |      5.67 |           9.67 |                 13.10 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      1749.21 |     14.67 |           0.55 |                  0.55 |
| MySQL-1-1-2-1 |      1749.21 |     14.67 |           0.55 |                  0.55 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      8053.92 |     32.05 |          11.61 |                 16.00 |
| MySQL-1-1-2-1 |      6906.19 |     23.56 |          13.23 |                 16.00 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      7117.05 |     26.36 |           1.35 |                  1.35 |
| MySQL-1-1-2-1 |      7117.05 |     50.24 |           1.35 |                  1.35 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           0.00 |                     444.56 |                     0.01 |                0.00 |                    0.00 |
| MySQL-1-1-2-1 |                           0.00 |                     444.56 |                     0.01 |                0.00 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                  213803.86 |                     0.11 |                0.00 |                    0.00 |
| MySQL-1-1-2-1 |                           0.00 |                  189479.38 |                     0.11 |                0.00 |                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

The summary shows the first 5 application metrics aggregated per execution run.
An extensive example for an evaluation is in the [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/dev).



### HammerDB's TPC-C

Example:
```bash
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -xsd 5 \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -xlat \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_run_mysql_appmetrics.log
```

doc_hammerdb_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1453s 
* Code: 1781472802
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Benchmarking also logs latencies.
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [16] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:240891
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781472802
* MySQL-1-1-2-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:258825
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781472802

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1, 2]]

#### Planned

* DBMS MySQL-1 - Pods [[1, 2]]

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   16 |      128.00 |           8.00 |            0.00 |         49.00 |           71.00 |              1 |          16 |             | None           |             0 | False         |              450.00 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:----------------|:------------|:--------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 169236 | 393189 |         0.00 |          5 |        0 |       4.02 |       5.74 |
| MySQL-1-1-2-1-1 | MySQL-1-1-2 | MySQL-1-1-2-1 |                1 |        8 |        2 |               1 |       1 | 166645 | 387243 |         0.00 |          5 |        0 |       3.91 |       5.56 |
| MySQL-1-1-2-1-1 | MySQL-1-1-2 | MySQL-1-1-2-1 |                1 |        8 |        2 |               1 |       1 | 166597 | 387114 |         0.00 |          5 |        0 |       3.92 |       5.59 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|----------:|-----------:|---------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |       16 |        1 |               1 |           1 |       4.02 |       5.74 |         0.00 | 169236.00 | 393189.00 |          5 |        0 |
| MySQL-1-1-2 | MySQL-1-1-2 |                1 |       16 |        2 |               1 |           2 |       3.92 |       5.59 |         0.00 | 166621.00 | 387178.50 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       246.47 |      5.93 |          22.26 |                 25.25 |
| MySQL-1-1-2-1 |       246.47 |      5.93 |          22.26 |                 25.25 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       368.80 |      9.18 |           0.17 |                  0.17 |
| MySQL-1-1-2-1 |       368.80 |      9.18 |           0.17 |                  0.17 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      4532.66 |     11.19 |          24.14 |                 52.24 |
| MySQL-1-1-2-1 |      4471.39 |     11.37 |          25.60 |                 64.00 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       590.05 |      1.57 |           0.83 |                  0.83 |
| MySQL-1-1-2-1 |       590.05 |      3.20 |           0.83 |                  0.83 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                     499.13 |                     0.01 |                0.00 |                    0.00 |
| MySQL-1-1-2-1 |                           1.00 |                     499.13 |                     0.01 |                0.00 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                  935795.44 |                     0.01 |                0.00 |                    0.00 |
| MySQL-1-1-2-1 |                           0.00 |                  923585.57 |                     0.01 |                0.00 |                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```


### TPC-H

Example:
```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_run_mysql_appmetrics.log
```

doc_tpch_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 817s 
* Code: 1781467828
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:246260
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781467828

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1]]

#### Planned

* DBMS MySQL-1 - Pods [[1]]

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |    3 |      284.00 |           1.00 |           24.00 |         54.00 |          201.00 |              8 |           0 |             | None           |             0 | False         |               38.03 |

### Execution

#### Per Connection

|                 | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        169 |            3.33 |             3346.01 |           1405.92 |          -1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |        169 |            3.33 |             3346.01 |           1405.92 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MySQL-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          22978.40 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            307.68 |
| Shipping Priority (TPC-H Q3)                        |           4799.50 |
| Order Priority Checking Query (TPC-H Q4)            |           1459.10 |
| Local Supplier Volume (TPC-H Q5)                    |           5006.85 |
| Forecasting Revenue Change (TPC-H Q6)               |           4363.84 |
| Forecasting Revenue Change (TPC-H Q7)               |           2961.28 |
| National Market Share (TPC-H Q8)                    |          10254.50 |
| Product Type Profit Measure (TPC-H Q9)              |           7850.46 |
| Forecasting Revenue Change (TPC-H Q10)              |           4576.51 |
| Important Stock Identification (TPC-H Q11)          |            564.77 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           6342.61 |
| Customer Distribution (TPC-H Q13)                   |          19403.29 |
| Forecasting Revenue Change (TPC-H Q14)              |           4502.62 |
| Top Supplier Query (TPC-H Q15)                      |          44330.23 |
| Parts/Supplier Relationship (TPC-H Q16)             |            996.19 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            868.70 |
| Large Volume Customer (TPC-H Q18)                   |           5139.17 |
| Discounted Revenue (TPC-H Q19)                      |            411.65 |
| Potential Part Promotion (TPC-H Q20)                |            831.02 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |          14619.70 |
| Global Sales Opportunity Query (TPC-H Q22)          |            430.94 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       571.85 |      6.85 |          13.14 |                 21.24 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        11.67 |      0.45 |           0.01 |                  0.28 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       142.48 |      1.01 |          13.18 |                 21.29 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        14.07 |      0.02 |           0.31 |                  0.32 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       1.22 |                     0.01 |                0.04 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       1.52 |                     0.00 |                0.03 |                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```


### TPC-DS

Example:
```bash
bexhoma tpcds \
  -dbms MySQL \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_run_mysql_appmetrics.log
```

doc_tpcds_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
* Type: tpcds
* Duration: 4004s 
* Code: 1781468695
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:252787
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781468695

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1]]

#### Planned

* DBMS MySQL-1 - Pods [[1]]

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |    3 |     2151.00 |           2.00 |            1.00 |        238.00 |         1903.00 |              8 |           0 |             | None           |             0 | False         |                5.02 |

### Execution

#### Per Connection

|                 | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |       1665 |            2.79 |             3882.06 |            642.16 |          -1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               99 |       1665 |            2.79 |             3882.06 |            642.16 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MySQL-1-1-1-1-1 |
|:--------------|------------------:|
| TPC-DS Q1     |             68.68 |
| TPC-DS Q2     |          13646.06 |
| TPC-DS Q3     |             24.53 |
| TPC-DS Q4     |         130145.38 |
| TPC-DS Q5     |          36280.40 |
| TPC-DS Q6     |         302405.04 |
| TPC-DS Q7     |           1239.93 |
| TPC-DS Q8     |           1082.79 |
| TPC-DS Q9     |          14441.72 |
| TPC-DS Q10    |            244.11 |
| TPC-DS Q11    |          81358.53 |
| TPC-DS Q12    |            903.46 |
| TPC-DS Q13    |           3977.42 |
| TPC-DS Q14a+b |         133585.12 |
| TPC-DS Q15    |            676.98 |
| TPC-DS Q16    |            464.33 |
| TPC-DS Q17    |           1533.39 |
| TPC-DS Q18    |           1791.16 |
| TPC-DS Q19    |           1077.69 |
| TPC-DS Q20    |           1689.41 |
| TPC-DS Q21    |          71182.57 |
| TPC-DS Q22    |          12586.22 |
| TPC-DS Q23a+b |         178036.43 |
| TPC-DS Q24a+b |           6074.00 |
| TPC-DS Q25    |            535.56 |
| TPC-DS Q26    |            919.83 |
| TPC-DS Q27    |           1024.27 |
| TPC-DS Q28    |          11082.82 |
| TPC-DS Q29    |            502.74 |
| TPC-DS Q30    |           4904.70 |
| TPC-DS Q31    |          40607.21 |
| TPC-DS Q32    |            586.57 |
| TPC-DS Q33    |            781.82 |
| TPC-DS Q34    |           2167.75 |
| TPC-DS Q35    |           8486.08 |
| TPC-DS Q36    |           4809.33 |
| TPC-DS Q37    |             21.36 |
| TPC-DS Q38    |          25968.18 |
| TPC-DS Q39a+b |           6149.33 |
| TPC-DS Q40    |            536.23 |
| TPC-DS Q41    |           6023.55 |
| TPC-DS Q42    |            960.84 |
| TPC-DS Q43    |              4.89 |
| TPC-DS Q44    |              3.10 |
| TPC-DS Q45    |            446.36 |
| TPC-DS Q46    |           4204.75 |
| TPC-DS Q47    |          11764.01 |
| TPC-DS Q48    |           4653.84 |
| TPC-DS Q49    |           1798.71 |
| TPC-DS Q50    |             76.55 |
| TPC-DS Q51    |          20381.38 |
| TPC-DS Q52    |            981.64 |
| TPC-DS Q53    |            740.55 |
| TPC-DS Q54    |           8778.52 |
| TPC-DS Q55    |            938.12 |
| TPC-DS Q56    |            785.82 |
| TPC-DS Q57    |          10805.37 |
| TPC-DS Q58    |          20543.70 |
| TPC-DS Q59    |          21638.50 |
| TPC-DS Q60    |           1714.03 |
| TPC-DS Q61    |           2208.16 |
| TPC-DS Q62    |           9088.95 |
| TPC-DS Q63    |            774.55 |
| TPC-DS Q64    |           1238.58 |
| TPC-DS Q65    |          23766.86 |
| TPC-DS Q66    |           6998.86 |
| TPC-DS Q67    |          27165.87 |
| TPC-DS Q68    |           1036.31 |
| TPC-DS Q69    |           1683.86 |
| TPC-DS Q70    |          40588.79 |
| TPC-DS Q71    |           1695.29 |
| TPC-DS Q72    |          48356.36 |
| TPC-DS Q73    |            941.51 |
| TPC-DS Q74    |          18004.11 |
| TPC-DS Q75    |           5967.71 |
| TPC-DS Q76    |           1467.64 |
| TPC-DS Q77    |          31422.89 |
| TPC-DS Q78    |          41830.03 |
| TPC-DS Q79    |           3200.76 |
| TPC-DS Q80    |          29073.93 |
| TPC-DS Q81    |           3708.45 |
| TPC-DS Q82    |             86.01 |
| TPC-DS Q83    |           2350.93 |
| TPC-DS Q84    |            125.61 |
| TPC-DS Q85    |            272.76 |
| TPC-DS Q86    |           3590.40 |
| TPC-DS Q87    |          26068.76 |
| TPC-DS Q88    |          32857.42 |
| TPC-DS Q89    |           7201.31 |
| TPC-DS Q90    |           1272.61 |
| TPC-DS Q91    |             58.97 |
| TPC-DS Q92    |             87.19 |
| TPC-DS Q93    |            134.55 |
| TPC-DS Q94    |           1339.34 |
| TPC-DS Q95    |          12762.98 |
| TPC-DS Q96    |           2824.45 |
| TPC-DS Q97    |          19786.22 |
| TPC-DS Q98    |           3388.30 |
| TPC-DS Q99    |          17564.79 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      4078.54 |      7.41 |          27.17 |                 54.75 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        14.39 |      0.37 |           0.01 |                  2.43 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      1643.22 |      1.02 |          31.64 |                 59.45 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        25.31 |      0.53 |           0.40 |                  0.41 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       0.97 |                     0.01 |                0.04 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       0.81 |                     0.00 |                0.03 |                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading phase: component data generator contains 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```



### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms MySQL \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2,3 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_run_mysql_appmetrics.log
```

doc_ycsb_run_mysql_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1190s 
* Code: 1781466611
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:247628
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781466611
* MySQL-1-1-2-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:251070
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781466611
* MySQL-1-1-3-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:254511
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781466611
* MySQL-1-1-4-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:257955
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781466611

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1, 8, 1, 8]]

#### Planned

* DBMS MySQL-1 - Pods [[1, 8, 1, 8]]

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| MySQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4718.46 |                79475.00 |            375000.00 |                              4971.00 | 3.00 |              135.89 |
| MySQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4686.62 |                80015.00 |            375000.00 |                              4923.00 | 3.00 |              134.97 |
| MySQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4713.96 |                79551.00 |            375000.00 |                              4875.00 | 3.00 |              135.76 |
| MySQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4667.08 |                80350.00 |            375000.00 |                              4971.00 | 3.00 |              134.41 |
| MySQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4704.55 |                79710.00 |            375000.00 |                              4887.00 | 3.00 |              135.49 |
| MySQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4693.48 |                79898.00 |            375000.00 |                              4915.00 | 3.00 |              135.17 |
| MySQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4695.01 |                79872.00 |            375000.00 |                              5019.00 | 3.00 |              135.22 |
| MySQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4709.46 |                79627.00 |            375000.00 |                              4923.00 | 3.00 |              135.63 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              134.41 |                        37588.63 |                80350.00 |           3000000.00 |                              4935.50 |

### Execution

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32062.24 |                93568.00 |            1499830 |                             962.00 |              1500170 |                              4795.00 |
| MySQL-1-1-2-1-5 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4053.66 |                92509.00 |             187576 |                             940.00 |               187424 |                              3401.00 |
| MySQL-1-1-2-1-6 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4046.40 |                92675.00 |             187426 |                             873.00 |               187574 |                              3351.00 |
| MySQL-1-1-2-1-2 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4052.70 |                92531.00 |             187686 |                             893.00 |               187314 |                              3373.00 |
| MySQL-1-1-2-1-1 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4045.35 |                92699.00 |             187333 |                             880.00 |               187667 |                              3319.00 |
| MySQL-1-1-2-1-3 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4057.91 |                92412.00 |             187446 |                             947.00 |               187554 |                              3385.00 |
| MySQL-1-1-2-1-8 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4058.84 |                92391.00 |             187362 |                             957.00 |               187638 |                              3421.00 |
| MySQL-1-1-2-1-4 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4050.46 |                92582.00 |             188262 |                             897.00 |               186738 |                              3361.00 |
| MySQL-1-1-2-1-7 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4052.56 |                92534.00 |             186837 |                             929.00 |               188163 |                              3377.00 |
| MySQL-1-1-3-1-1 | MySQL-1-1-3 | MySQL-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        47533.79 |                63113.00 |            1499322 |                             843.00 |              1500678 |                              6119.00 |
| MySQL-1-1-4-1-2 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6048.29 |                62001.00 |             187484 |                             926.00 |               187516 |                              4391.00 |
| MySQL-1-1-4-1-5 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6055.81 |                61924.00 |             187489 |                             942.00 |               187511 |                              4399.00 |
| MySQL-1-1-4-1-3 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6060.21 |                61879.00 |             186996 |                             932.00 |               188004 |                              4247.00 |
| MySQL-1-1-4-1-4 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6040.20 |                62084.00 |             187320 |                             913.00 |               187680 |                              4287.00 |
| MySQL-1-1-4-1-7 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6049.36 |                61990.00 |             187470 |                             924.00 |               187530 |                              4363.00 |
| MySQL-1-1-4-1-8 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6062.08 |                61860.00 |             186951 |                            1100.00 |               188049 |                              4247.00 |
| MySQL-1-1-4-1-1 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6045.56 |                62029.00 |             187630 |                             876.00 |               187370 |                              4271.00 |
| MySQL-1-1-4-1-6 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6033.60 |                62152.00 |             187418 |                             875.00 |               187582 |                              4235.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32062.24 |                93568.00 |            1499830 |                             962.00 |              1500170 |                              4795.00 |
| MySQL-1-1-2 | MySQL-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32417.88 |                92699.00 |            1499928 |                             957.00 |              1500072 |                              3421.00 |
| MySQL-1-1-3 | MySQL-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        47533.79 |                63113.00 |            1499322 |                             843.00 |              1500678 |                              6119.00 |
| MySQL-1-1-4 | MySQL-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48395.11 |                62152.00 |            1498758 |                            1100.00 |              1501242 |                              4399.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      1353.14 |     16.86 |          25.64 |                 35.75 |
| MySQL-1-1-2-1 |      1353.14 |     16.86 |          25.64 |                 35.75 |
| MySQL-1-1-3-1 |      1353.14 |     16.86 |          25.64 |                 35.75 |
| MySQL-1-1-4-1 |      1353.14 |     16.86 |          25.64 |                 35.75 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       414.16 |      6.19 |           0.13 |                  0.13 |
| MySQL-1-1-2-1 |       414.16 |      6.19 |           0.13 |                  0.13 |
| MySQL-1-1-3-1 |       414.16 |      6.19 |           0.13 |                  0.13 |
| MySQL-1-1-4-1 |       414.16 |      6.19 |           0.13 |                  0.13 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       845.40 |     12.81 |          25.78 |                 39.06 |
| MySQL-1-1-2-1 |       985.36 |     12.65 |          25.94 |                 44.24 |
| MySQL-1-1-3-1 |       754.84 |     15.73 |          26.07 |                 48.40 |
| MySQL-1-1-4-1 |       939.77 |     15.96 |          26.23 |                 53.84 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       307.65 |      5.95 |           0.16 |                  0.16 |
| MySQL-1-1-2-1 |       422.90 |      8.05 |           0.16 |                  0.16 |
| MySQL-1-1-3-1 |       278.53 |     11.49 |           0.15 |                  0.16 |
| MySQL-1-1-4-1 |       144.26 |     16.11 |           0.15 |                  0.16 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           0.00 |                   12536.22 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-2-1 |                           0.00 |                   12536.22 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-3-1 |                           0.00 |                   12536.22 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-4-1 |                           0.00 |                   12536.22 |                     0.04 |                0.00 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                   19427.26 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-2-1 |                           1.00 |                   21135.29 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-3-1 |                           0.00 |                   18595.57 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-4-1 |                           0.00 |                   16969.27 |                     0.04 |                0.00 |                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```








## CockroachDB

### YCSB

Example:
```bash
bexhoma ycsb \
  -dbms CockroachDB \
  -sf 10 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 3 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_run_cockroachdb_appmetrics.log
```

doc_ycsb_run_cockroachdb_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 2230s 
* Code: 1781474280
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* CockroachDB-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:206042
  * cpu_list:0-127
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1077381271552
    * Cores:256
    * host:6.8.0-111-generic
    * node:cl-worker27
    * disk:1359213
    * volume_size:1000G
    * volume_used:686G
    * cpu_list:0-255
  * worker 1
    * RAM:2164173246464
    * Cores:224
    * host:6.8.0-111-generic
    * node:cl-worker36
    * disk:1200034
    * volume_size:1000G
    * volume_used:686G
    * cpu_list:0-223
  * worker 2
    * RAM:1081649803264
    * Cores:56
    * host:6.8.0-111-generic
    * node:cl-worker34
    * disk:316911
    * volume_size:1000G
    * volume_used:686G
    * cpu_list:0-55
  * eval_parameters
    * code:1781474280
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Workflow

#### Actual

* DBMS CockroachDB-1 - Pods [[1]]

#### Planned

* DBMS CockroachDB-1 - Pods [[1]]

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| CockroachDB-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1446.67 |               864055.00 |           1250000.00 |                             43007.00 | 10.00 |               41.66 |
| CockroachDB-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1442.77 |               866390.00 |           1250000.00 |                             43295.00 | 10.00 |               41.55 |
| CockroachDB-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1443.44 |               865985.00 |           1250000.00 |                             43135.00 | 10.00 |               41.57 |
| CockroachDB-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1445.62 |               864680.00 |           1250000.00 |                             43327.00 | 10.00 |               41.63 |
| CockroachDB-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1443.89 |               865715.00 |           1250000.00 |                             42943.00 | 10.00 |               41.58 |
| CockroachDB-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1444.84 |               865145.00 |           1250000.00 |                             43039.00 | 10.00 |               41.61 |
| CockroachDB-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1444.33 |               865456.00 |           1250000.00 |                             43071.00 | 10.00 |               41.60 |
| CockroachDB-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         1446.08 |               864408.00 |           1250000.00 |                             42783.00 | 10.00 |               41.65 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |               41.55 |                        11557.64 |               866390.00 |          10000000.00 |                             43075.00 |

### Execution

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1-1-1 | CockroachDB-1-1-1 | CockroachDB-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        10418.33 |               959847.00 |            5001013 |                            6927.00 |              4998987 |                            171263.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1-1 | CockroachDB-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        10418.33 |               959847.00 |            5001013 |                            6927.00 |              4998987 |                            171263.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     16674.48 |     24.42 |          20.29 |                 58.18 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       876.34 |      1.87 |           0.11 |                  0.11 |

### Execution phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |     18702.37 |     23.36 |          23.10 |                 66.41 |

### Execution phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| CockroachDB-1-1-1-1 |       689.93 |      0.86 |           0.13 |                  0.13 |

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                    43198.22 |                   34637133.52 |                                    0.00 |                                      0.00 |                              0.00 |

#### Execution phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In (Bytes/sec) |   Raft Recovery Snapshot In (Bytes/sec) |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------------:|----------------------------------------:|------------------------------------------:|----------------------------------:|
| CockroachDB-1-1-1-1 |                                    11465.09 |                    9130677.66 |                                    0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```


### Benchbase's TPC-C

Example:
```bash
bexhoma benchbase \
  -dbms CockroachDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -nw 3 \
  -nwr 3 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_cockroachdb_appmetrics.log
```

doc_benchbase_run_cockroachdb_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1352s 
    Code: 1772842492
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.9.1.
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
    disk:147811
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173209600
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:702318
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081853952000
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:417146
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081965416448
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1311724
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1772842492
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
CockroachDB-1-1-1024-2 uses docker image cockroachdb/cockroach:v24.2.4
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:147809
    cpu_list:0-63
    args:['-c', 'while true; do echo hello; sleep 10;done']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    worker 0
        RAM:2164173209600
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:702628
        volume_size:1000G
        volume_used:283G
        cpu_list:0-223
    worker 1
        RAM:1081853952000
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:417451
        volume_size:1000G
        volume_used:283G
        cpu_list:0-127
    worker 2
        RAM:1081965416448
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1312034
        volume_size:1000G
        volume_used:283G
        cpu_list:0-255
    eval_parameters
                code:1772842492
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                          experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                      
CockroachDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    514.413285                 512.263285         0.0                                                      72389.0                                              31093.0
CockroachDB-1-1-1024-2-2               1          8    8192       2      1  300.0           0                    253.056659                 251.999992         0.0                                                      74727.0                                              31603.0
CockroachDB-1-1-1024-2-1               1          8    8192       2      2  300.0           0                    242.359930                 241.326597         0.0                                                      82723.0                                              32998.0

#### Aggregated Parallel
                        experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
CockroachDB-1-1-1024-1               1         16   16384          1  300.0           0                        514.41                     512.26         0.0                                                      72389.0                                              31093.0
CockroachDB-1-1-1024-2               1         16   16384          2  300.0           0                        495.42                     493.33         0.0                                                      82723.0                                              32300.5

### Workflow

#### Actual
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS CockroachDB-1-1-1024 - Pods [[1, 2]]

### Loading
                        time_load  terminals  pods  Throughput [SF/h]
CockroachDB-1-1-1024-1      221.0        1.0   1.0         260.633484
CockroachDB-1-1-1024-2      221.0        1.0   2.0         260.633484

### Monitoring

### Loading phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1     2163.53    19.11          6.32                 9.84
CockroachDB-1-1-1024-2     2163.53    19.11          6.32                 9.84

### Loading phase: component loader
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1     1356.21    13.52          0.25                 0.25
CockroachDB-1-1-1024-2     1356.21    13.52          0.25                 0.25

### Execution phase: component worker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1     6428.38    24.07          8.94                12.82
CockroachDB-1-1-1024-2     6361.03    22.33          7.80                12.57

### Execution phase: component benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
CockroachDB-1-1-1024-1       250.0     0.92          0.32                 0.32
CockroachDB-1-1-1024-2       250.0     1.70          0.32                 0.32

### Application Metrics

#### Loading phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                    1363.87                  12895218.38                                      0                                        0                                0
CockroachDB-1-1-1024-2                                    1363.87                  12895218.38                                      0                                        0                                0

#### Execution phase: component worker
                        Raft Messages Received (AppResp) [msgs/s]  Raft Network In (Bytes/sec)  Raft Recovery Snapshot In (Bytes/sec)  Replicate Queue Adds Attempted [adds/s]  Replicate Queue Purgatory Count
CockroachDB-1-1-1024-1                                   27334.79                   5029922.02                                    0.0                                      0.0                              0.0
CockroachDB-1-1-1024-2                                    9909.29                   3968858.30                                    0.0                                      0.0                              0.0

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
bexhoma ycsb \
  -dbms Redis \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -nwr 1 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_run_redis_appmetrics.log
```

doc_ycsb_run_redis_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 571s 
    Code: 1772838599
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
    Experiment uses bexhoma version 0.9.1.
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
    disk:147809
    cpu_list:0-63
    args:['--maxclients', '10000', '--io-threads', '64']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    worker 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:700519
        cpu_list:0-223
    worker 1
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1171673
        cpu_list:0-95
    worker 2
        RAM:1081853952000
        CPU:Intel(R) Xeon(R) Gold 6438Y+
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker37
        disk:415550
        cpu_list:0-127
    worker 3
        RAM:1081965416448
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1310048
        cpu_list:0-255
    worker 4
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:175536
        cpu_list:0-95
    worker 5
        RAM:1081742741504
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-100-generic
        node:cl-worker29
        disk:630174
        cpu_list:0-127
    eval_parameters
        code:1772838599
        BEXHOMA_REPLICAS:1
        BEXHOMA_WORKERS:3

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
Redis-64-8-196608               1       64  196608          8           0                   20457.227018                49240.0             1000000                              6076.0

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
Redis-64-8-196608-1               1      128   65536          1           0                       60921.37               164146.0           5000261                            1076.0             4999739                              1058.0

### Workflow

#### Actual
DBMS Redis-64-8-196608 - Pods [[1]]

#### Planned
DBMS Redis-64-8-196608 - Pods [[1]]

### Monitoring

### Loading phase: component worker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      180.77     2.53          3.51                 3.72

### Loading phase: component loader
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1       83.14        0          0.12                 0.12

### Execution phase: component worker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      438.04     3.84          3.62                 3.65

### Execution phase: component benchmarker
                     CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Redis-64-8-196608-1      519.49     4.76           0.3                  0.3

### Application Metrics

#### Loading phase: component worker
                     Redis Cluster State  Connected Clients [count]  Redis Memory Used [Gi]  Redis Master Link Status  Redis Operations Rate [ops/s]
Redis-64-8-196608-1                    6                        201                    3.48                         3                        5902.63

#### Execution phase: component worker
                     Redis Cluster State  Connected Clients [count]  Redis Memory Used [Gi]  Redis Master Link Status  Redis Operations Rate [ops/s]
Redis-64-8-196608-1                    6                        393                    3.51                         3                        7661.37

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
bexhoma ycsb \
  -dbms TiDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xnsr 3 \
  -nw 3 \
  -nwr 3 \
  -xop 1 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  run &>$LOG_DIR/doc_ycsb_run_tidb_appmetrics.log
```

doc_ycsb_run_tidb_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 953s 
* Code: 1773414636
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* TiDB-64-8-16384-1 uses docker image pingcap/tidb:v7.1.0
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-90-generic
  * node:cl-worker37
  * disk:470827
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-90-generic
    * node:cl-worker37
    * disk:470827
    * cpu_list:0-127
  * sut 1
    * RAM:540579303424
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-94-generic
    * node:cl-worker22
    * disk:387018
    * cpu_list:0-127
  * sut 2
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:1241159
    * cpu_list:0-223
  * pd 0
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:1241156
    * cpu_list:0-223
  * pd 1
    * RAM:1081649823744
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-90-generic
    * node:cl-worker34
    * disk:305321
    * cpu_list:0-55
  * pd 2
    * RAM:1081965416448
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:5.15.0-1093-nvidia
    * node:cl-worker27
    * disk:1128780
    * cpu_list:0-255
  * tikv 0
    * RAM:2164173209600
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-90-generic
    * node:cl-worker36
    * disk:1241157
    * cpu_list:0-223
  * tikv 1
    * RAM:540579303424
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-94-generic
    * node:cl-worker22
    * disk:387015
    * cpu_list:0-127
  * tikv 2
    * RAM:1081742741504
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-100-generic
    * node:cl-worker29
    * disk:650970
    * cpu_list:0-127
  * eval_parameters
    * code:1773414636
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Loading

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-64-8-16384 |                1 |        64 |    16384 |           8 |            0 |                         11763.4 |                   85889 |                1e+06 |                                16502 |

### Execution

| DBMS              |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| TiDB-64-8-16384-1 |                1 |        64 |    16384 |           1 |            0 |                         9747.73 |                  102588 |             500646 |                               3283 |               499354 |                               215551 |

### Workflow

#### Actual

* DBMS TiDB-64-8-16384 - Pods [[1]]

#### Planned

* DBMS TiDB-64-8-16384 - Pods [[1]]

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |       888.77 |      8.86 |           4.96 |                  5.85 |

### Loading phase: component pd

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |        72.65 |      0.56 |           0.28 |                  0.28 |

### Loading phase: component tikv

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |       561.69 |      6.14 |            5.5 |                 15.89 |

### Loading phase: component loader

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |        63.49 |         0 |           0.11 |                  0.11 |

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |       448.05 |         7 |           1.45 |                  2.35 |

### Execution phase: component pd

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |        61.95 |      0.61 |           0.28 |                  0.28 |

### Execution phase: component tikv

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |       473.72 |      7.09 |           6.74 |                 19.26 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| TiDB-64-8-16384-1 |        34.04 |         0 |           0.14 |                  0.14 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration [ms] |
|:------------------|----------------------------------------:|-------------------------------:|
| TiDB-64-8-16384-1 |                                  4023.6 |                           4.77 |

#### Loading phase: component pd

| DBMS              |   PD Cluster Leader Count |   PD Leader Balance Actions [ops] |
|:------------------|--------------------------:|----------------------------------:|
| TiDB-64-8-16384-1 |                        64 |                                14 |

#### Loading phase: component tikv

| DBMS              |   TiKV Store Used [%] |   TiKV Compaction Time Median [s] |   TiKV Compaction Flow [Gi] |   TiKV Compaction Pending [Gi] |
|:------------------|----------------------:|----------------------------------:|----------------------------:|-------------------------------:|
| TiDB-64-8-16384-1 |                  0.18 |                       9.44679e+07 |                        7.19 |                           1.43 |

#### Execution phase: SUT deployment

| DBMS              |   TiDB SQL Statement Throughput [ops/s] |   TiDB Avg Query Duration [ms] |
|:------------------|----------------------------------------:|-------------------------------:|
| TiDB-64-8-16384-1 |                                 3330.06 |                           5.37 |

#### Execution phase: component pd

| DBMS              |   PD Cluster Leader Count |   PD Leader Balance Actions [ops] |
|:------------------|--------------------------:|----------------------------------:|
| TiDB-64-8-16384-1 |                        69 |                                 6 |

#### Execution phase: component tikv

| DBMS              |   TiKV Store Used [%] |   TiKV Compaction Time Median [s] |   TiKV Compaction Flow [Gi] |   TiKV Compaction Pending [Gi] |
|:------------------|----------------------:|----------------------------------:|----------------------------:|-------------------------------:|
| TiDB-64-8-16384-1 |                  0.22 |                                 0 |                        0.35 |                           0.95 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```


### Benchbase's TPC-C

Example:
```bash

bexhoma benchbase \
  -dbms TiDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -xnsr 3 \
  -nw 3 \
  -nwr 3 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  run &>$LOG_DIR/doc_benchbase_run_tidb_appmetrics.log
```

doc_benchbase_run_tidb_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1578s 
    Code: 1772840860
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.9.1.
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
    disk:148720
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
        disk:148720
        cpu_list:0-63
    sut 1
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148720
        cpu_list:0-63
    sut 2
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148720
        cpu_list:0-63
    pd 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:724538
        cpu_list:0-223
    pd 1
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:174949
        cpu_list:0-95
    pd 2
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1196808
        cpu_list:0-95
    tikv 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:724539
        cpu_list:0-223
    tikv 1
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1196808
        cpu_list:0-95
    tikv 2
        RAM:1081965416448
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1334107
        cpu_list:0-255
    eval_parameters
                code:1772840860
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3
TiDB-1-1-1024-2 uses docker image pingcap/tidb:v7.1.0
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:148720
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
        disk:148720
        cpu_list:0-63
    sut 1
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148720
        cpu_list:0-63
    sut 2
        RAM:541008474112
        CPU:AMD Opteron(tm) Processor 6378
        Cores:64
        host:5.15.0-164-generic
        node:cl-worker14
        disk:148720
        cpu_list:0-63
    pd 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:722552
        cpu_list:0-223
    pd 1
        RAM:540590821376
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker24
        disk:174952
        cpu_list:0-95
    pd 2
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1196584
        cpu_list:0-95
    tikv 0
        RAM:2164173209600
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:722556
        cpu_list:0-223
    tikv 1
        RAM:540590817280
        CPU:AMD EPYC 7352 24-Core Processor
        Cores:96
        host:6.8.0-90-generic
        node:cl-worker23
        disk:1196585
        cpu_list:0-95
    tikv 2
        RAM:1081965416448
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:5.15.0-1093-nvidia
        node:cl-worker27
        disk:1332317
        cpu_list:0-255
    eval_parameters
                code:1772840860
                BEXHOMA_REPLICAS:3
                BEXHOMA_WORKERS:3

### Execution

#### Per Pod
                   experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                               
TiDB-1-1-1024-1-1               1         16   16384       1      1  300.0           0                    284.479903                 283.173237         0.0                                                     120500.0                                              56225.0
TiDB-1-1-1024-2-1               1          8    8192       2      1  300.0           0                    132.453299                 131.119966         0.0                                                     137658.0                                              60372.0
TiDB-1-1-1024-2-2               1          8    8192       2      2  300.0           0                    134.706630                 133.229964         0.0                                                     136249.0                                              59362.0

#### Aggregated Parallel
                 experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
TiDB-1-1-1024-1               1         16   16384          1  300.0           0                        284.48                     283.17         0.0                                                     120500.0                                              56225.0
TiDB-1-1-1024-2               1         16   16384          2  300.0           0                        267.16                     264.35         0.0                                                     137658.0                                              59867.0

### Workflow

#### Actual
DBMS TiDB-1-1-1024 - Pods [[1, 2]]

#### Planned
DBMS TiDB-1-1-1024 - Pods [[1, 2]]

### Loading
                 time_load  terminals  pods  Throughput [SF/h]
TiDB-1-1-1024-1      245.0        1.0   1.0         235.102041
TiDB-1-1-1024-2      245.0        1.0   2.0         235.102041

### Monitoring

### Loading phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1599.63     11.2          2.81                 3.07
TiDB-1-1-1024-2     1599.63     11.2          2.81                 3.07

### Loading phase: component pd
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1       76.92     0.36           0.3                  0.3
TiDB-1-1-1024-2       76.92     0.36           0.3                  0.3

### Loading phase: component tikv
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1768.17    12.01          9.63                29.16
TiDB-1-1-1024-2     1768.17    12.01          9.63                29.16

### Loading phase: component loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1041.97     9.76          0.38                 0.38
TiDB-1-1-1024-2     1041.97     9.76          0.38                 0.38

### Execution phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     3394.86    12.09           0.9                 1.15
TiDB-1-1-1024-2     2979.46    11.07           0.9                 1.16

### Execution phase: component pd
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      237.67     0.91          0.31                 0.32
TiDB-1-1-1024-2      231.88     0.92          0.32                 0.32

### Execution phase: component tikv
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1     1289.46     5.25         12.09                31.37
TiDB-1-1-1024-2     1269.16     5.46         13.43                31.93

### Execution phase: component benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
TiDB-1-1-1024-1      209.87     1.11          0.32                 0.32
TiDB-1-1-1024-2      263.50     0.85          0.32                 0.32

### Application Metrics

#### Loading phase: SUT deployment
                 TiDB SQL Statement Throughput [ops/s]  TiDB Avg Query Duration [ms]
TiDB-1-1-1024-1                                 432.95                          19.4
TiDB-1-1-1024-2                                 432.95                          19.4

#### Loading phase: component pd
                 PD Cluster Leader Count  PD Leader Balance Actions [ops]
TiDB-1-1-1024-1                      118                               44
TiDB-1-1-1024-2                      118                               44

#### Loading phase: component tikv
                 TiKV Store Used [%]  TiKV Compaction Time Median [s]  TiKV Compaction Flow [Gi]  TiKV Compaction Pending [Gi]
TiDB-1-1-1024-1                 0.18                         68746.15                       13.4                          1.57
TiDB-1-1-1024-2                 0.18                         68746.15                       13.4                          1.57

#### Execution phase: SUT deployment
                 TiDB SQL Statement Throughput [ops/s]  TiDB Avg Query Duration [ms]
TiDB-1-1-1024-1                                6799.77                         19.15
TiDB-1-1-1024-2                                4318.23                          3.39

#### Execution phase: component pd
                 PD Cluster Leader Count  PD Leader Balance Actions [ops]
TiDB-1-1-1024-1                      119                               10
TiDB-1-1-1024-2                      122                                0

#### Execution phase: component tikv
                 TiKV Store Used [%]  TiKV Compaction Time Median [s]  TiKV Compaction Flow [Gi]  TiKV Compaction Pending [Gi]
TiDB-1-1-1024-1                 0.24                          37575.0                       2.46                          0.73
TiDB-1-1-1024-2                 0.30                          36411.0                       2.77                          0.70

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
bexhoma ycsb \
  -dbms PGBouncer \
  -sf 16 \
  -xwl c \
  -xtb 16384 \
  -xnbf 11 \
  -xnlf 11 \
  -nc 1 \
  -ne 1 \
  -nlp 16 \
  -nlt 64 \
  -nbp 16 \
  -nbt 128 \
  -xnpp 4 \
  -xnpi 128 \
  -xnpo 64 \
  -xop 16 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_run_pgbouncer_appmetrics.log
```

doc_ycsb_run_pgbouncer_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=16
    Type: ycsb
    Duration: 1603s 
    Code: 1772839205
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
    Experiment uses bexhoma version 0.9.1.
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
    disk:186025
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:64Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1772839205

### Loading
                 experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
pgb-64-4-128-64               1       64  180224         16           0                   30841.466284               523522.0            16000000                             5978.75

### Execution
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)
pgb-64-4-128-64-1               1      128  180224         16           0                       71466.95               230896.0          16000000                            2489.0

### Workflow

#### Actual
DBMS pgb-64-4-128-64 - Pods [[16]]

#### Planned
DBMS pgb-64-4-128-64 - Pods [[16]]

### Monitoring

### Loading phase: component pool
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1        1.92      0.0          0.09                 0.09

### Loading phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     3744.87     9.48          24.1                42.38

### Loading phase: component loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     1311.06     3.62          0.11                 0.11

### Execution phase: component pool
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1         0.4      0.0          0.09                 0.09

### Execution phase: SUT deployment
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     2576.29    18.76         26.75                45.01

### Execution phase: component benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-64-4-128-64-1     1274.91     9.63           0.1                 0.11

### Application Metrics

#### Loading phase: component pool
                   PgBouncer Query Throughput [queries/s]  PgBouncer Waiting Clients [s]  PgBouncer Waiting Clients [clients]  PgBouncer Idle Connections [connections]  PgBouncer Pool Load Pressure [%]
pgb-64-4-128-64-1                                33452.14                           0.63                                    0                                       155                             100.0

#### Loading phase: SUT deployment
                   Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
pgb-64-4-128-64-1                      257                                       0                                               0                         65                                     64

#### Execution phase: component pool
                   PgBouncer Query Throughput [queries/s]  PgBouncer Waiting Clients [s]  PgBouncer Waiting Clients [clients]  PgBouncer Idle Connections [connections]  PgBouncer Pool Load Pressure [%]
pgb-64-4-128-64-1                                58204.56                           0.11                                    0                                        40                             100.0

#### Execution phase: SUT deployment
                   Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
pgb-64-4-128-64-1                      256                                       0                                               0                         12                                     12

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
bexhoma benchbase \
  -dbms PGBouncer \
  -sf 16 \
  -xsd 10 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 32 \
  -xnpp 2 \
  -xnpi 32 \
  -xnpo 32 \
  -xconn \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_pgbouncer_appmetrics.log
```

doc_benchbase_run_pgbouncer_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 1738s 
    Code: 1772843882
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. There is a reconnect for each transaction. Benchmarking runs for 10 minutes.
    Experiment uses bexhoma version 0.9.1.
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
    disk:152117
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1772843882
pgb-1-2-32-32-2 uses docker image postgres:18.3
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:152392
    cpu_list:0-63
    args:['-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=64GB', '-c', 'max_connections=2048', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=64GB', '-c', 'maintenance_work_mem=2GB', '-c', 'wal_buffers=1GB', '-c', 'work_mem=32GB', '-c', 'temp_buffers=4GB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=7MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'synchronous_commit=off', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=off', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=1000', '-c', 'random_page_cost=60']
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1772843882

### Execution

#### Per Pod
                   experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                               
pgb-1-2-32-32-1-1               1         32   16384       1      1  600.0           2                   1419.373316                 467.336661         0.0                                                      42104.0                                              22541.0
pgb-1-2-32-32-2-1               1         16    8192       2      1  600.0           1                    595.639960                 445.091637         0.0                                                      52955.0                                              26854.0
pgb-1-2-32-32-2-2               1         16    8192       2      2  600.0           0                    615.298234                 445.133261         0.0                                                      52476.0                                              25996.0

#### Aggregated Parallel
                 experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
pgb-1-2-32-32-1               1         32   16384          1  600.0           2                       1419.37                     467.34         0.0                                                      42104.0                                              22541.0
pgb-1-2-32-32-2               1         32   16384          2  600.0           1                       1210.94                     890.22         0.0                                                      52955.0                                              26425.0

### Workflow

#### Actual
DBMS pgb-1-2-32-32 - Pods [[1, 2]]

#### Planned
DBMS pgb-1-2-32-32 - Pods [[1, 2]]

### Loading
                 time_load  terminals  pods  Throughput [SF/h]
pgb-1-2-32-32-1      152.0        1.0   1.0         378.947368
pgb-1-2-32-32-2      152.0        1.0   2.0         378.947368

### Monitoring

### Loading phase: component pool
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1        0.41      0.0          0.04                 0.04
pgb-1-2-32-32-2        0.41      0.0          0.04                 0.04

### Loading phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1      705.11     7.79          4.71                 6.34
pgb-1-2-32-32-2      705.11     7.79          4.71                 6.34

### Loading phase: component loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1     1271.66    12.76          0.26                 0.26
pgb-1-2-32-32-2     1271.66    12.76          0.26                 0.26

### Execution phase: component pool
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1        1.18      0.0          0.04                 0.04
pgb-1-2-32-32-2        1.12      0.0          0.04                 0.04

### Execution phase: SUT deployment
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1     2161.66     4.05          5.01                 6.91
pgb-1-2-32-32-2     3957.94     8.22          5.51                 7.83

### Execution phase: component benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
pgb-1-2-32-32-1    12049.58    24.20          0.48                 0.48
pgb-1-2-32-32-2    12049.58    23.12          0.48                 0.48

### Application Metrics

#### Loading phase: component pool
                 PgBouncer Query Throughput [queries/s]  PgBouncer Waiting Clients [s]  PgBouncer Waiting Clients [clients]  PgBouncer Idle Connections [connections]  PgBouncer Pool Load Pressure [%]
pgb-1-2-32-32-1                                  224.53                           0.19                                    0                                        48                             100.0
pgb-1-2-32-32-2                                  224.53                           0.19                                    0                                        48                             100.0

#### Loading phase: SUT deployment
                 Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
pgb-1-2-32-32-1                       65                                       0                                               0                         15                                     14
pgb-1-2-32-32-2                       65                                       0                                               0                         15                                     14

#### Execution phase: component pool
                 PgBouncer Query Throughput [queries/s]  PgBouncer Waiting Clients [s]  PgBouncer Waiting Clients [clients]  PgBouncer Idle Connections [connections]  PgBouncer Pool Load Pressure [%]
pgb-1-2-32-32-1                                 9640.80                           0.35                                    0                                        56                             100.0
pgb-1-2-32-32-2                                18880.11                           0.09                                    0                                        55                             100.0

#### Execution phase: SUT deployment
                 Number of Idle Sessions  Number of Idle-in-transaction Sessions  Number of Idle-in-transaction Aborted Sessions  Number of Active Sessions  Number of Active Application Sessions
pgb-1-2-32-32-1                       65                                      21                                               0                         19                                     18
pgb-1-2-32-32-2                       65                                      21                                               0                         17                                     17

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
bexhoma ycsb \
  -dbms YugabyteDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  run &>$LOG_DIR/doc_ycsb_run_yugabytedb_appmetrics.log
```

doc_ycsb_run_yugabytedb_appmetrics.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 950s 
* Code: 1773432301
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* YugabyteDB-64-8-65536-1 uses docker image postgres:15.0
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1294649
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773432301

### Loading

| DBMS                  |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-64-8-65536 |                1 |        64 |    65536 |           8 |            0 |                         19489.3 |                   52544 |                1e+06 |                                 8961 |

### Execution

| DBMS                    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| YugabyteDB-64-8-65536-1 |                1 |        64 |    65536 |           1 |            0 |                         34422.5 |                  290508 |        5.00119e+06 |                               7643 |          4.99881e+06 |                                43583 |

### Workflow

#### Actual

* DBMS YugabyteDB-64-8-65536 - Pods [[1]]

#### Planned

* DBMS YugabyteDB-64-8-65536 - Pods [[1]]

### Monitoring

### Loading phase: component yb-tserver

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |      1234.82 |     13.47 |            5.6 |                  13.6 |

### Loading phase: component yb-master

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |         6.87 |      0.04 |           0.24 |                  0.26 |

### Loading phase: component loader

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |        38.93 |         0 |           0.11 |                  0.11 |

### Execution phase: component yb-tserver

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |      10378.5 |     39.73 |           9.51 |                 20.76 |

### Execution phase: component yb-master

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |        10.69 |      0.06 |           0.26 |                  0.29 |

### Execution phase: component benchmarker

| DBMS                    |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-64-8-65536-1 |       319.68 |      1.25 |           0.14 |                  0.14 |

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS                    |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:------------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-64-8-65536-1 |                         3754.31 |                       0.42 |                        7.06 |                         0 |                         617 |

#### Loading phase: component yb-master

| DBMS                    |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:------------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-64-8-65536-1 |                               0.02 |                             0.54 |                                   0 |               5.017e+08 |                               0.02 |

#### Execution phase: component yb-tserver

| DBMS                    |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:------------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-64-8-65536-1 |                         31676.4 |                       0.67 |                        2.47 |                         0 |                         585 |

#### Execution phase: component yb-master

| DBMS                    |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:------------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-64-8-65536-1 |                               0.01 |                             0.52 |                                   0 |             5.01948e+08 |                               0.01 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```



### Benchbase's TPC-C

Example:
```bash
bexhoma benchbase \
  -dbms YugabyteDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  run &>$LOG_DIR/doc_benchbase_run_yugabytedb_appmetrics.log
```

doc_benchbase_run_yugabytedb_appmetrics.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1265s 
* Code: 1773430865
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.4.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 1 processes (pods).
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* YugabyteDB-1-1-1024-1 uses docker image postgres:15.0
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1262462
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773430865
* YugabyteDB-1-1-1024-2 uses docker image postgres:15.0
  * RAM:2164173209600
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-90-generic
  * node:cl-worker36
  * disk:1263692
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1773430865

### Execution

#### Per Pod

| DBMS                    |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| YugabyteDB-1-1-1024-1-1 |                1 |          16 |    16384 |        1 |       1 |    300 |            0 |                        475.947 |                     473.847 |            0 |                                                         81863 |                                                 33609 |
| YugabyteDB-1-1-1024-2-1 |                1 |           8 |     8192 |        2 |       1 |    300 |            0 |                        225.253 |                     224.247 |            0 |                                                         94011 |                                                 35505 |
| YugabyteDB-1-1-1024-2-2 |                1 |           8 |     8192 |        2 |       2 |    300 |            0 |                        214.683 |                     213.59  |            0 |                                                         97092 |                                                 37254 |

#### Aggregated Parallel

| DBMS                  |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| YugabyteDB-1-1-1024-1 |                1 |          16 |    16384 |           1 |    300 |            0 |                         475.95 |                      473.85 |            0 |                                                         81863 |                                               33609   |
| YugabyteDB-1-1-1024-2 |                1 |          16 |    16384 |           2 |    300 |            0 |                         439.94 |                      437.84 |            0 |                                                         97092 |                                               36379.5 |

### Workflow

#### Actual

* DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

#### Planned

* DBMS YugabyteDB-1-1-1024 - Pods [[1, 2]]

### Loading

| DBMS                  |   time_load |   terminals |   pods |   Throughput [SF/h] |
|:----------------------|------------:|------------:|-------:|--------------------:|
| YugabyteDB-1-1-1024-1 |         102 |           1 |      1 |             564.706 |
| YugabyteDB-1-1-1024-2 |         102 |           1 |      2 |             564.706 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |      2010.86 |     22.68 |           7.39 |                 16.15 |
| YugabyteDB-1-1-1024-2 |      2508.42 |     22.68 |           7.39 |                 16.15 |

### Loading phase: component yb-master

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |        17.84 |      0.21 |           0.34 |                  0.38 |
| YugabyteDB-1-1-1024-2 |        24.18 |      0.21 |           0.36 |                  0.4  |

### Loading phase: component loader

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |        75.68 |         0 |           0.25 |                  0.26 |
| YugabyteDB-1-1-1024-2 |        75.68 |         0 |           0.25 |                  0.26 |

### Execution phase: component yb-tserver

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |     10821.6  |     39.06 |          10.15 |                 20.45 |
| YugabyteDB-1-1-1024-2 |      9532.47 |     36.81 |          11.15 |                 22.77 |

### Execution phase: component yb-master

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |        13.01 |      0.07 |           0.39 |                  0.43 |
| YugabyteDB-1-1-1024-2 |        17.1  |      0.08 |           0.45 |                  0.49 |

### Execution phase: component benchmarker

| DBMS                  |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------------|-------------:|----------:|---------------:|----------------------:|
| YugabyteDB-1-1-1024-1 |       102.58 |      0.52 |            0.3 |                   0.3 |
| YugabyteDB-1-1-1024-2 |        92.67 |      0.98 |            0.3 |                   0.3 |

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS                  |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:----------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-1-1-1024-1 |                          243.83 |                       0.44 |                       26.87 |                         0 |                         856 |
| YugabyteDB-1-1-1024-2 |                         3048.64 |                       0.44 |                       26.87 |                         0 |                         856 |

#### Loading phase: component yb-master

| DBMS                  |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:----------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-1-1-1024-1 |                               3.05 |                            22.47 |                                0.04 |             5.00068e+08 |                               3.01 |
| YugabyteDB-1-1-1024-2 |                               3.05 |                            22.47 |                                0.04 |             5.00234e+08 |                               3.01 |

#### Execution phase: component yb-tserver

| DBMS                  |   YSQL Query Throughput [ops/s] |   Tablet Read Latency [ms] |   Tablet Write Latency [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:----------------------|--------------------------------:|---------------------------:|----------------------------:|--------------------------:|----------------------------:|
| YugabyteDB-1-1-1024-1 |                        16629.5  |                       0.28 |                       11.22 |                         0 |                         599 |
| YugabyteDB-1-1-1024-2 |                         7310.32 |                       0.31 |                        1.19 |                         0 |                         612 |

#### Execution phase: component yb-master

| DBMS                  |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error |   Tablet Location Requests [ops/s] |
|:----------------------|-----------------------------------:|---------------------------------:|------------------------------------:|------------------------:|-----------------------------------:|
| YugabyteDB-1-1-1024-1 |                               3.02 |                             0.44 |                                0.03 |             5.00262e+08 |                               2.99 |
| YugabyteDB-1-1-1024-2 |                               1.11 |                             0.32 |                                0    |             5.01112e+08 |                               1.11 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```
