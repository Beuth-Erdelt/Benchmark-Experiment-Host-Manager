## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1317s 
* Code: 1792344739
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:853969
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:143579
    * datadisk:691715
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:879746
    * datadisk:691506
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * worker 2
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:154257
    * datadisk:691678
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792344739
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:853973
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:143760
    * datadisk:691888
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:1077382627328
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:879853
    * datadisk:691676
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-255
  * worker 2
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:154330
    * datadisk:691746
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792344739
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792344739-7f9dd56c5f-vrdf2: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-0: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-1: 0
* bexhoma-worker-cockroachdb-benchbase-tpcc-16-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |   16 |      299.00 |           4.00 |            0.00 |        290.00 |            5.00 |              1 |           1 |             | None           |             0 | False         |              192.64 | False               |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         267.31 |                      266.09 |         0.00 |                                                     187956.00 |                                              59837.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         122.59 |                      122.07 |         0.00 |                                                     191186.00 |                                              65239.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         119.22 |                      118.78 |         0.00 |                                                     190421.00 |                                              67092.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         267.31 |                      266.09 |         0.00 |                                                     187956.00 |                                              59837.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         241.81 |                      240.85 |         0.00 |                                                     191186.00 |                                              66165.50 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      2625.98 |     19.22 |           7.54 |                 11.44 |
| cockroachdb-1-1-2-1 |      2625.98 |     19.22 |           7.54 |                 11.44 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       964.88 |      9.36 |           0.27 |                  0.27 |
| cockroachdb-1-1-2-1 |       964.88 |      9.36 |           0.27 |                  0.27 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      4113.62 |     15.73 |           7.92 |                 11.92 |
| cockroachdb-1-1-2-1 |      3767.58 |     13.56 |           7.80 |                 12.17 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       145.74 |      0.55 |           0.30 |                  0.30 |
| cockroachdb-1-1-2-1 |       145.74 |      1.34 |           0.30 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                     1354.31 |             13646676.41 |                              0.00 |                                      0.38 |                              0.00 |
| cockroachdb-1-1-2-1 |                                     1354.31 |             13646676.41 |                              0.00 |                                      0.38 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                    14453.18 |             10715075.91 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                    13422.10 |              5603661.82 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
