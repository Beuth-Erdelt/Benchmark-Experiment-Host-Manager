## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 4369s 
* Code: 1793792062
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 10 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * disk:850120
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
    * disk:602467
    * datadisk:10823
    * volume_size:98G
    * volume_used:11G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:605370
    * datadisk:9800
    * volume_size:98G
    * volume_used:9.6G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:850161
    * datadisk:9917
    * volume_size:98G
    * volume_used:9.7G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793792062
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:849171
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
    * disk:602467
    * datadisk:13594
    * volume_size:98G
    * volume_used:14G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:605373
    * datadisk:13472
    * volume_size:98G
    * volume_used:14G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:849213
    * datadisk:13537
    * volume_size:98G
    * volume_used:14G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793792062
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-3-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:795141
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
    * disk:602467
    * datadisk:15983
    * volume_size:98G
    * volume_used:16G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:605365
    * datadisk:15881
    * volume_size:98G
    * volume_used:16G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:795141
    * datadisk:15954
    * volume_size:98G
    * volume_used:16G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793792062
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-4-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:815540
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
    * disk:606159
    * datadisk:17986
    * volume_size:98G
    * volume_used:18G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:609315
    * datadisk:17896
    * volume_size:98G
    * volume_used:18G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:816368
    * datadisk:17997
    * volume_size:98G
    * volume_used:18G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793792062
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* CockroachDB-1: skipped initschema-benchbase.sql

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1793792062-59b9f95ccc-484q6: 0
* bx-w-cockroachdb-nvme-benchbase-tpcc-128-0: 0
* bx-w-cockroachdb-nvme-benchbase-tpcc-128-1: 0
* bx-w-cockroachdb-nvme-benchbase-tpcc-128-2: 0

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

|                 |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| CockroachDB-1-1 |                1 |  128 |     1416.00 |           1.00 |            0.00 |       1412.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              325.42 | False               |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:------------------|:--------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 600.00 |            0 |                        3807.61 |                     3786.57 |         0.00 |                                                    1233100.00 |                                             335645.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 600.00 |            0 |                        1650.50 |                     1642.40 |         0.00 |                                                    1329415.00 |                                             387417.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 600.00 |            0 |                        1648.00 |                     1639.70 |         0.00 |                                                    1330926.00 |                                             388191.00 |
| cockroachdb-1-1-3-1-1 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       1 |          -1 | 600.00 |            0 |                         795.94 |                      791.93 |         0.00 |                                                    1481091.00 |                                             401871.00 |
| cockroachdb-1-1-3-1-2 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       2 |          -1 | 600.00 |            0 |                         798.54 |                      794.65 |         0.00 |                                                    1477996.00 |                                             400390.00 |
| cockroachdb-1-1-3-1-3 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       3 |          -1 | 600.00 |            0 |                         799.07 |                      795.12 |         0.00 |                                                    1477305.00 |                                             400125.00 |
| cockroachdb-1-1-3-1-4 | cockroachdb-1-1-3 | cockroachdb-1-1-3-1 |                1 |         320 |     4096 |        3 |               1 |       4 |          -1 | 600.00 |            0 |                         797.14 |                      793.24 |         0.00 |                                                    1477607.00 |                                             401033.00 |
| cockroachdb-1-1-4-1-1 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       1 |          -1 | 600.00 |            0 |                         370.03 |                      367.93 |         0.00 |                                                    1615661.00 |                                             431898.00 |
| cockroachdb-1-1-4-1-2 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       2 |          -1 | 600.00 |            0 |                         371.71 |                      369.74 |         0.00 |                                                    1610577.00 |                                             430085.00 |
| cockroachdb-1-1-4-1-3 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       3 |          -1 | 600.00 |            0 |                         376.97 |                      374.97 |         0.00 |                                                    1589969.00 |                                             424006.00 |
| cockroachdb-1-1-4-1-4 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       4 |          -1 | 600.00 |            0 |                         374.75 |                      372.71 |         0.00 |                                                    1592247.00 |                                             426391.00 |
| cockroachdb-1-1-4-1-5 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       5 |          -1 | 600.00 |            0 |                         375.79 |                      373.84 |         0.00 |                                                    1595918.00 |                                             425409.00 |
| cockroachdb-1-1-4-1-6 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       6 |          -1 | 600.00 |            0 |                         373.48 |                      371.51 |         0.00 |                                                    1607527.00 |                                             428032.00 |
| cockroachdb-1-1-4-1-7 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       7 |          -1 | 600.00 |            0 |                         376.50 |                      374.46 |         0.00 |                                                    1588877.00 |                                             424506.00 |
| cockroachdb-1-1-4-1-8 | cockroachdb-1-1-4 | cockroachdb-1-1-4-1 |                1 |         160 |     2048 |        4 |               1 |       8 |          -1 | 600.00 |            0 |                         375.26 |                      373.41 |         0.00 |                                                    1587703.00 |                                             425839.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:------------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 600.00 |            0 |                        3807.61 |                     3786.57 |         0.00 |                                                    1233100.00 |                                             335645.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 600.00 |            0 |                        3298.50 |                     3282.11 |         0.00 |                                                    1330926.00 |                                             387804.00 |
| cockroachdb-1-1-3 | cockroachdb-1-1-3 |                1 |        1280 |    16384 |               1 |           4 |          -1 | 600.00 |            0 |                        3190.70 |                     3174.95 |         0.00 |                                                    1481091.00 |                                             400854.75 |
| cockroachdb-1-1-4 | cockroachdb-1-1-4 |                1 |        1280 |    16384 |               1 |           8 |          -1 | 600.00 |            0 |                        2994.51 |                     2978.57 |         0.00 |                                                    1615661.00 |                                             427020.75 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     14157.46 |     30.69 |          25.77 |                 54.73 |
| cockroachdb-1-1-2-1 |     14157.46 |     30.69 |          25.77 |                 54.73 |
| cockroachdb-1-1-3-1 |     14157.46 |     30.69 |          25.77 |                 54.73 |
| cockroachdb-1-1-4-1 |     14157.46 |     30.69 |          25.77 |                 54.73 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |    145742.29 |    122.81 |           0.35 |                  0.35 |
| cockroachdb-1-1-2-1 |    145742.29 |    122.81 |           0.35 |                  0.35 |
| cockroachdb-1-1-3-1 |    145742.29 |    122.81 |           0.35 |                  0.35 |
| cockroachdb-1-1-4-1 |    145742.29 |    122.81 |           0.35 |                  0.35 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |    137417.61 |    251.86 |          39.35 |                 75.82 |
| cockroachdb-1-1-2-1 |    118832.81 |    204.52 |          38.95 |                 83.14 |
| cockroachdb-1-1-3-1 |    115783.18 |    197.76 |          40.55 |                 89.16 |
| cockroachdb-1-1-4-1 |    115494.02 |    199.54 |          42.53 |                100.46 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      2624.97 |      4.96 |           4.25 |                  4.25 |
| cockroachdb-1-1-2-1 |      2559.82 |      4.78 |           2.71 |                  2.71 |
| cockroachdb-1-1-3-1 |      2746.49 |      5.45 |           1.83 |                  1.83 |
| cockroachdb-1-1-4-1 |      3006.85 |     10.03 |           1.63 |                  1.63 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
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
| cockroachdb-1-1-1-1 |                                     6525.45 |             43145551.36 |                              0.00 |                                      0.18 |                              0.00 |
| cockroachdb-1-1-2-1 |                                     6525.45 |             43145551.36 |                              0.00 |                                      0.18 |                              0.00 |
| cockroachdb-1-1-3-1 |                                     6525.45 |             43145551.36 |                              0.00 |                                      0.18 |                              0.00 |
| cockroachdb-1-1-4-1 |                                     6525.45 |             43145551.36 |                              0.00 |                                      0.18 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                   186830.00 |             79207625.90 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-2-1 |                                   173091.94 |             69124480.58 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-3-1 |                                   170647.15 |             67660608.76 |                              0.00 |                                      0.00 |                              0.00 |
| cockroachdb-1-1-4-1 |                                   168503.62 |             67611036.55 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
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
