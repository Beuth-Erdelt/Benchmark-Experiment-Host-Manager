## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 4625s 
* Code: 1794705531
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1280] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1044397
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381323
    * datadisk:9938
    * volume_size:98G
    * volume_used:9.8G
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1044397
    * datadisk:9706
    * volume_size:98G
    * volume_used:9.5G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662999
    * datadisk:9774
    * volume_size:98G
    * volume_used:9.6G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794705531
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045212
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381324
    * datadisk:12752
    * volume_size:98G
    * volume_used:13G
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1045212
    * datadisk:12539
    * volume_size:98G
    * volume_used:13G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:663011
    * datadisk:12536
    * volume_size:98G
    * volume_used:13G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794705531
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045205
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381325
    * datadisk:14888
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1045205
    * datadisk:14668
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:663022
    * datadisk:14660
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794705531
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045208
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381326
    * datadisk:17985
    * volume_size:98G
    * volume_used:18G
    * cpu_list:0-127
  * worker 1
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1045208
    * datadisk:16474
    * volume_size:98G
    * volume_used:17G
    * cpu_list:0-223
  * worker 2
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:663051
    * datadisk:16499
    * volume_size:98G
    * volume_used:17G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794705531
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* CockroachDB-1: skipped initschema-benchbase.sql

### Ingestion
* CockroachDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794705531-bd5b6b5b5-gn59l: 0
* bx-w-cr-nvme-benchbase-tpcc-128-0: 0
* bx-w-cr-nvme-benchbase-tpcc-128-1: 0
* bx-w-cr-nvme-benchbase-tpcc-128-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 4: benchbase (8 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 4: benchbase (8 pods)

### Loading

#### Per Run

| DBMS            |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |  128 |     1713.00 |           2.00 |            0.00 |       1707.00 |            4.00 |              1 |         1 |             | None           |             0 | False         |              269.00 | False               |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2871.62 |                     2847.70 |         0.00 |                                                    2355994.00 |                                             444720.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       1 |       640 |     8192 |          -1 | 600.00 |        0 |                        1399.20 |                     1391.18 |         0.00 |                                                    2365752.00 |                                             456580.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       2 |       640 |     8192 |          -1 | 600.00 |        0 |                        1403.20 |                     1395.22 |         0.00 |                                                    2365486.00 |                                             455616.00 |
| cockroachdb-1-1-3-1-1 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       1 |       320 |     4096 |          -1 | 600.00 |        0 |                         661.60 |                      658.56 |         0.00 |                                                    2139641.00 |                                             482960.00 |
| cockroachdb-1-1-3-1-2 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       2 |       320 |     4096 |          -1 | 600.00 |        0 |                         663.23 |                      660.18 |         0.00 |                                                    2138966.00 |                                             482021.00 |
| cockroachdb-1-1-3-1-3 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       3 |       320 |     4096 |          -1 | 600.00 |        0 |                         665.87 |                      662.76 |         0.00 |                                                    2145533.00 |                                             480138.00 |
| cockroachdb-1-1-3-1-4 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |        3 |               1 |       4 |       320 |     4096 |          -1 | 600.00 |        0 |                         660.88 |                      657.77 |         0.00 |                                                    2144677.00 |                                             483755.00 |
| cockroachdb-1-1-4-1-1 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       1 |       160 |     2048 |          -1 | 600.00 |        0 |                         330.61 |                      328.95 |         0.00 |                                                    1947662.00 |                                             483412.00 |
| cockroachdb-1-1-4-1-2 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       2 |       160 |     2048 |          -1 | 600.00 |        0 |                         332.23 |                      330.60 |         0.00 |                                                    1955637.00 |                                             481499.00 |
| cockroachdb-1-1-4-1-3 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       3 |       160 |     2048 |          -1 | 600.00 |        0 |                         329.79 |                      328.18 |         0.00 |                                                    1957572.00 |                                             484657.00 |
| cockroachdb-1-1-4-1-4 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       4 |       160 |     2048 |          -1 | 600.00 |        0 |                         330.58 |                      329.02 |         0.00 |                                                    1956024.00 |                                             483616.00 |
| cockroachdb-1-1-4-1-5 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       5 |       160 |     2048 |          -1 | 600.00 |        0 |                         331.43 |                      329.90 |         0.00 |                                                    1951266.00 |                                             482269.00 |
| cockroachdb-1-1-4-1-6 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       6 |       160 |     2048 |          -1 | 600.00 |        0 |                         329.69 |                      328.11 |         0.00 |                                                    1958370.00 |                                             484851.00 |
| cockroachdb-1-1-4-1-7 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       7 |       160 |     2048 |          -1 | 600.00 |        0 |                         331.57 |                      329.85 |         0.00 |                                                    1948739.00 |                                             482145.00 |
| cockroachdb-1-1-4-1-8 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |        4 |               1 |       8 |       160 |     2048 |          -1 | 600.00 |        0 |                         330.99 |                      329.50 |         0.00 |                                                    1951355.00 |                                             482870.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2871.62 |                     2847.70 |         0.00 |                                                    2355994.00 |                                             444720.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        2 |               1 |           2 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2802.41 |                     2786.40 |         0.00 |                                                    2365752.00 |                                             456098.00 |
| cockroachdb-1-1-3 | cockroachdb-1-1-3 |                1 |        3 |               1 |           4 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2651.57 |                     2639.28 |         0.00 |                                                    2145533.00 |                                             482218.50 |
| cockroachdb-1-1-4 | cockroachdb-1-1-4 |                1 |        4 |               1 |           8 |      1280 |    16384 |          -1 | 600.00 |        0 |                        2646.89 |                     2634.12 |         0.00 |                                                    1958370.00 |                                             483164.88 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     15791.25 |     44.63 |          21.95 |                 47.21 |
| cockroachdb-1-1-2-1 |     15791.25 |     44.63 |          21.95 |                 47.21 |
| cockroachdb-1-1-3-1 |     15791.25 |     44.63 |          21.95 |                 47.21 |
| cockroachdb-1-1-4-1 |     15791.25 |     44.63 |          21.95 |                 47.21 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |    188831.13 |    121.08 |           0.36 |                  0.36 |
| cockroachdb-1-1-2-1 |    188831.13 |    121.08 |           0.36 |                  0.36 |
| cockroachdb-1-1-3-1 |    188831.13 |    121.08 |           0.36 |                  0.36 |
| cockroachdb-1-1-4-1 |    188831.13 |    121.08 |           0.36 |                  0.36 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |    104697.97 |    191.46 |          34.68 |                 67.63 |
| cockroachdb-1-1-2-1 |    105556.06 |    181.41 |          37.53 |                 77.59 |
| cockroachdb-1-1-3-1 |    100791.74 |    177.42 |          39.31 |                 84.37 |
| cockroachdb-1-1-4-1 |    104238.23 |    177.56 |          39.88 |                 92.12 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      2242.13 |      7.94 |           4.25 |                  4.25 |
| cockroachdb-1-1-2-1 |      2422.76 |      7.57 |           3.57 |                  3.57 |
| cockroachdb-1-1-3-1 |      2333.41 |      4.20 |           2.07 |                  2.07 |
| cockroachdb-1-1-4-1 |      2903.18 |      7.00 |           1.57 |                  1.57 |

### Missing Monitoring Metrics
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-2-1 (bexhoma-metrics-cockroachdb-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-3-1 (bexhoma-metrics-cockroachdb-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-4-1 (bexhoma-metrics-cockroachdb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-4-1 (bexhoma-metrics-cockroachdb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-4-1 (bexhoma-metrics-cockroachdb-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-4-1 (bexhoma-metrics-cockroachdb-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                     7933.31 |             47190224.72 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                     7933.31 |             47190224.72 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-3-1 |                                     7933.31 |             47190224.72 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-4-1 |                                     7933.31 |             47190224.72 |                              0.00 |                                      0.00 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                   153131.36 |             58223903.91 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                   153833.04 |             58673019.62 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-3-1 |                                   152963.29 |             58051039.01 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-4-1 |                                   154448.71 |             59590821.83 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
