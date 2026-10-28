## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1507s 
* Code: 1793235355
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
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
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1226303
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:365790
    * cpu_list:0-223
  * yb-tserver 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:492578
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:515504
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:365790
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:492578
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:515504
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793235355
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1226326
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:366717
    * cpu_list:0-223
  * yb-tserver 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:493602
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:516403
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:366717
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:493602
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:516403
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793235355

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793235355-57ff8f75b9-4jnqz: 0
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
| YugabyteDB-1-1 |                1 |   16 |      415.00 |         305.00 |            0.00 |        107.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              138.80 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         332.47 |                      330.97 |         0.00 |                                                     123369.00 |                                              48112.00 |
| yugabytedb-1-1-2-1-1 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         147.94 |                      147.23 |         0.00 |                                                     134383.00 |                                              54061.00 |
| yugabytedb-1-1-2-1-2 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            1 |                         141.30 |                      140.63 |         0.00 |                                                     138880.00 |                                              56600.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         332.47 |                      330.97 |         0.00 |                                                     123369.00 |                                              48112.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            1 |                         289.25 |                      287.85 |         0.00 |                                                     138880.00 |                                              55330.50 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      3055.70 |     35.08 |           8.63 |                 17.22 |
| yugabytedb-1-1-2-1 |      3055.70 |     35.08 |           8.63 |                 17.22 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        29.27 |      0.10 |           0.31 |                  0.34 |
| yugabytedb-1-1-2-1 |        29.27 |      0.10 |           0.31 |                  0.34 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        37.54 |      0.82 |           0.28 |                  0.28 |
| yugabytedb-1-1-2-1 |        37.54 |      0.82 |           0.28 |                  0.28 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     10423.52 |     39.36 |          10.29 |                 19.67 |
| yugabytedb-1-1-2-1 |     10342.54 |     37.25 |          11.89 |                 21.70 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        19.46 |      0.18 |           0.37 |                  0.40 |
| yugabytedb-1-1-2-1 |        22.67 |      0.17 |           0.41 |                  0.43 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       105.23 |      0.38 |           0.31 |                  0.31 |
| yugabytedb-1-1-2-1 |        99.24 |      0.64 |           0.26 |                  0.26 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Active YSQL Connections for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverbenchmarking.log)
* Active YSQL Connections for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-yb-tserverloading.log)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Active YSQL Connections for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-yb-tserverbenchmarking.log)

### Application Metrics

#### Loading phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                     240.06 |                                        0.97 |                                        14.18 |                      0.00 |                      619.00 |
| yugabytedb-1-1-2-1 |                                     240.06 |                                        0.97 |                                        14.18 |                      0.00 |                      619.00 |

#### Loading phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               1.97 |                                         1.22 |                                0.04 |                       500.47 |                               1.97 |
| yugabytedb-1-1-2-1 |                               1.97 |                                         1.22 |                                0.04 |                       500.47 |                               1.97 |

#### Benchmarking phase: component yb-tserver

| DBMS               |   Tablet Read+Write RPC Throughput [ops/s] |   Tablet Read Latency, Avg since Start [ms] |   Tablet Write Latency, Avg since Start [ms] |   Active YSQL Connections |   TServer Follower Lag [ms] |
|:-------------------|-------------------------------------------:|--------------------------------------------:|---------------------------------------------:|--------------------------:|----------------------------:|
| yugabytedb-1-1-1-1 |                                   11732.49 |                                        0.41 |                                        12.75 |                      0.00 |                      611.00 |
| yugabytedb-1-1-2-1 |                                   10444.97 |                                        0.45 |                                         1.79 |                      0.00 |                      597.00 |

#### Benchmarking phase: component yb-master

| DBMS               |   YB-Master RPC Throughput [ops/s] |   YB-Master Avg RPC Latency since Start [ms] |   Table Metadata Operations [ops/s] |   YB-Master Clock Error [ms] |   Tablet Location Requests [ops/s] |
|:-------------------|-----------------------------------:|---------------------------------------------:|------------------------------------:|-----------------------------:|-----------------------------------:|
| yugabytedb-1-1-1-1 |                               1.89 |                                         0.05 |                                0.00 |                       500.49 |                               1.89 |
| yugabytedb-1-1-2-1 |                               0.00 |                                         0.05 |                                0.00 |                       500.39 |                               0.00 |

### Tests
* TEST passed: Loading measured in this experiment
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
