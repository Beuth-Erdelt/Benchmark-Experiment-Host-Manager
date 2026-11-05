## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1320s 
* Code: 1793871122
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 1 processes (pods).
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:540597891072
  * CPU:Intel(R) Xeon(R) 6767P
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker39
  * disk:246718
  * datadisk:39
  * volume_size:439G
  * volume_used:241G
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:676234
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:902650
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:697572
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:697572
    * cpu_list:0-127
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:676234
    * cpu_list:0-127
  * yb-master 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:902651
    * cpu_list:0-223
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793871122
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:540597891072
  * CPU:Intel(R) Xeon(R) 6767P
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker39
  * disk:246711
  * datadisk:39
  * volume_size:439G
  * volume_used:241G
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:678140
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:927204
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:698721
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:698736
    * cpu_list:0-127
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:678140
    * cpu_list:0-127
  * yb-master 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:927432
    * cpu_list:0-223
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793871122

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793871122-5584c5b57-bj7w8: 0
* yb-tserver-0: 0
* yb-tserver-1: 0
* yb-tserver-2: 0
* yb-master-0: 0
* yb-master-1: 0
* yb-master-2: 0

### Workflow

#### Actual

* DBMS YugabyteDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| YugabyteDB-1-1 |                1 |   16 |      435.00 |         304.00 |            0.00 |        130.00 |            1.00 |              1 |           1 |             | None           |             0 | False         |              132.41 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         356.39 |                      354.75 |         0.00 |                                                     112017.00 |                                              44882.00 |
| yugabytedb-1-1-2-1-1 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         153.84 |                      153.17 |         0.00 |                                                     127947.00 |                                              51971.00 |
| yugabytedb-1-1-2-1-2 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         162.78 |                      161.98 |         0.00 |                                                     119486.00 |                                              49117.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         356.39 |                      354.75 |         0.00 |                                                     112017.00 |                                              44882.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         316.62 |                      315.15 |         0.00 |                                                     127947.00 |                                              50544.00 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      2851.11 |     30.26 |           8.89 |                 16.65 |
| yugabytedb-1-1-2-1 |      2851.11 |     30.26 |           8.89 |                 16.65 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        24.41 |      0.12 |           0.36 |                  0.39 |
| yugabytedb-1-1-2-1 |        24.41 |      0.12 |           0.36 |                  0.39 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       550.00 |      9.03 |           0.32 |                  0.32 |
| yugabytedb-1-1-2-1 |       550.00 |      9.03 |           0.32 |                  0.32 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     10393.06 |     37.98 |          10.47 |                 20.47 |
| yugabytedb-1-1-2-1 |      8960.43 |     31.23 |          11.49 |                 22.96 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        16.62 |      0.15 |           0.41 |                  0.44 |
| yugabytedb-1-1-2-1 |        17.92 |      0.15 |           0.43 |                  0.46 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       177.38 |      0.68 |           0.29 |                  0.29 |
| yugabytedb-1-1-2-1 |       307.31 |      1.08 |           0.28 |                  0.28 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Node Max Core Utilization [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log)
* Node Core Utilization Variance [%^2] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log)
* Node I/O Wait CPU Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log)
* Node I/O Wait, Share of Busy CPU Time [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Node Core Utilization Variance [%^2] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log)
* Node I/O Wait, Share of Busy CPU Time [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log)
* Node Max Core Utilization [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log)
* Node I/O Wait CPU Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log)
* Node Core Utilization Variance [%^2] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-masterbenchmarking.log)
* Node Max Core Utilization [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-masterbenchmarking.log)
* Node I/O Wait, Share of Busy CPU Time [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-masterbenchmarking.log)
* Node I/O Wait CPU Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-masterbenchmarking.log)
* Node Core Utilization Variance [%^2] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-masterloading.log)
* Node I/O Wait, Share of Busy CPU Time [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-masterloading.log)
* Node Max Core Utilization [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-masterloading.log)
* Node I/O Wait CPU Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-masterloading.log)
* Node Core Utilization Variance [%^2] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverbenchmarking.log)
* Node Max Core Utilization [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverbenchmarking.log)
* Node I/O Wait, Share of Busy CPU Time [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverbenchmarking.log)
* Node I/O Wait CPU Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverbenchmarking.log)
* Active YSQL Connections for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverbenchmarking.log)
* Node Core Utilization Variance [%^2] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverloading.log)
* Node Max Core Utilization [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverloading.log)
* Node I/O Wait, Share of Busy CPU Time [%] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverloading.log)
* Node I/O Wait CPU Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverloading.log)
* Active YSQL Connections for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverloading.log)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Node Max Core Utilization [%] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log)
* Node I/O Wait, Share of Busy CPU Time [%] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log)
* Node I/O Wait CPU Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log)
* Node Core Utilization Variance [%^2] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log)
* Node Core Utilization Variance [%^2] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-masterbenchmarking.log)
* Node I/O Wait CPU Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-masterbenchmarking.log)
* Node I/O Wait, Share of Busy CPU Time [%] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-masterbenchmarking.log)
* Node Max Core Utilization [%] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-masterbenchmarking.log)
* Node Core Utilization Variance [%^2] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-tserverbenchmarking.log)
* Node Max Core Utilization [%] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-tserverbenchmarking.log)
* Node I/O Wait, Share of Busy CPU Time [%] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-tserverbenchmarking.log)
* Node I/O Wait CPU Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-tserverbenchmarking.log)
* Active YSQL Connections for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-tserverbenchmarking.log)

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                     238.81 |                                        0.80 |                                        11.75 |                      0.00 |                      621.00 |
| yugabytedb-1-1-2-1 |                                     238.81 |                                        0.80 |                                        11.75 |                      0.00 |                      621.00 |

#### Loading phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               2.17 |                                         1.04 |                                0.04 |                       500.06 |                               2.17 |
| yugabytedb-1-1-2-1 |                               2.17 |                                         1.04 |                                0.04 |                       500.06 |                               2.17 |

#### Benchmarking phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                   12547.27 |                                        0.37 |                                         9.61 |                      0.00 |                      609.00 |
| yugabytedb-1-1-2-1 |                                   11472.67 |                                        0.39 |                                         1.39 |                      0.00 |                      620.00 |

#### Benchmarking phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               2.19 |                                         0.05 |                                0.00 |                       500.17 |                               2.19 |
| yugabytedb-1-1-2-1 |                               0.14 |                                         0.04 |                                0.00 |                       500.31 |                               0.14 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
