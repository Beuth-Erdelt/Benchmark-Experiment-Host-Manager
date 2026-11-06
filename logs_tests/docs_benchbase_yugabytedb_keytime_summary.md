## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 8154s 
* Code: 1793225792
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking has keying and thinking times activated. Benchmarking runs for 20 minutes.
  * Status is logged every 30ms.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1280] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:378586
  * datadisk:39
  * volume_size:1.8T
  * volume_used:370G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:607142
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:378458
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:528508
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:378270
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:528315
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:606890
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793225792
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:372781
  * datadisk:39
  * volume_size:1.8T
  * volume_used:365G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:601459
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:372781
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:522693
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:372782
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:522697
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:601459
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793225792
* yugabytedb-1-1-3-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:373026
  * datadisk:39
  * volume_size:1.8T
  * volume_used:365G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:497563
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:373026
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:522866
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:373026
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:522866
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:497563
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793225792
* yugabytedb-1-1-4-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:427066
  * datadisk:39
  * volume_size:1.8T
  * volume_used:418G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:500459
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:426869
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:523102
    * cpu_list:0-127
  * yb-master 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:426869
    * cpu_list:0-223
  * yb-master 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:523102
    * cpu_list:0-127
  * yb-master 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:500459
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793225792

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1793225792-76d8b7867f-6k2kq: 0
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
* DBMS YugabyteDB-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 4: benchbase (10 pods)

#### Planned

* DBMS YugabyteDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS YugabyteDB-1 - Experiment 1 Client 4: benchbase (10 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| YugabyteDB-1-1 |                1 |  128 |     2374.00 |         304.00 |            0.00 |       2067.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              194.10 | False               |

### Benchmarking

#### Per Connection

| DBMS                  | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1  | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1280 |    16384 |        1 |               1 |       1 |          -1 | 1200.00 |            0 |                          58.13 |                       57.88 |        94.94 |                                                     185516.00 |                                            1062245.00 |
| yugabytedb-1-1-2-1-1  | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       1 |          -1 | 1200.00 |            0 |                          29.83 |                       29.70 |        48.72 |                                                     137472.00 |                                             560839.00 |
| yugabytedb-1-1-2-1-2  | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |         640 |     8192 |        2 |               1 |       2 |          -1 | 1200.00 |            0 |                          29.72 |                       29.60 |        48.55 |                                                     135969.00 |                                             609022.00 |
| yugabytedb-1-1-3-1-1  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |         256 |     3276 |        3 |               1 |       1 |          -1 | 1200.00 |            0 |                          11.39 |                       11.33 |        18.59 |                                                    1884007.00 |                                            1395181.00 |
| yugabytedb-1-1-3-1-2  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |         256 |     3276 |        3 |               1 |       2 |          -1 | 1200.00 |            1 |                          11.57 |                       11.52 |        18.89 |                                                    1527155.00 |                                            1288270.00 |
| yugabytedb-1-1-3-1-3  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |         256 |     3276 |        3 |               1 |       3 |          -1 | 1200.00 |            0 |                          11.53 |                       11.47 |        18.82 |                                                    1605499.00 |                                            1391541.00 |
| yugabytedb-1-1-3-1-4  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |         256 |     3276 |        3 |               1 |       4 |          -1 | 1200.00 |            0 |                          11.48 |                       11.43 |        18.74 |                                                    1619872.00 |                                            1358638.00 |
| yugabytedb-1-1-3-1-5  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |         256 |     3276 |        3 |               1 |       5 |          -1 | 1200.00 |            1 |                          11.41 |                       11.35 |        18.62 |                                                    1585992.00 |                                            1381496.00 |
| yugabytedb-1-1-4-1-1  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       1 |          -1 | 1200.00 |            0 |                           5.83 |                        5.80 |         9.52 |                                                     143473.00 |                                            1156846.00 |
| yugabytedb-1-1-4-1-2  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       2 |          -1 | 1200.00 |            0 |                           5.78 |                        5.75 |         9.43 |                                                     145184.00 |                                            1140761.00 |
| yugabytedb-1-1-4-1-3  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       3 |          -1 | 1200.00 |            0 |                           5.88 |                        5.84 |         9.57 |                                                     145975.00 |                                            1112021.00 |
| yugabytedb-1-1-4-1-4  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       4 |          -1 | 1200.00 |            0 |                           5.83 |                        5.81 |         9.53 |                                                     146387.00 |                                            1201594.00 |
| yugabytedb-1-1-4-1-5  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       5 |          -1 | 1200.00 |            0 |                           5.80 |                        5.78 |         9.48 |                                                     146063.00 |                                            1126176.00 |
| yugabytedb-1-1-4-1-6  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       6 |          -1 | 1200.00 |            0 |                           5.78 |                        5.76 |         9.45 |                                                     144188.00 |                                            1148348.00 |
| yugabytedb-1-1-4-1-7  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       7 |          -1 | 1200.00 |            0 |                           5.85 |                        5.82 |         9.55 |                                                     144463.00 |                                            1088968.00 |
| yugabytedb-1-1-4-1-8  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       8 |          -1 | 1200.00 |            0 |                           5.87 |                        5.84 |         9.58 |                                                     146056.00 |                                            1147027.00 |
| yugabytedb-1-1-4-1-9  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |       9 |          -1 | 1200.00 |            0 |                           5.84 |                        5.82 |         9.54 |                                                     145644.00 |                                            1086011.00 |
| yugabytedb-1-1-4-1-10 | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |         128 |     1638 |        4 |               1 |      10 |          -1 | 1200.00 |            0 |                           5.73 |                        5.71 |         9.36 |                                                     151583.00 |                                            1053560.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1280 |    16384 |               1 |           1 |          -1 | 1200.00 |            0 |                          58.13 |                       57.88 |        94.94 |                                                     185516.00 |                                            1062245.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |        1280 |    16384 |               1 |           2 |          -1 | 1200.00 |            0 |                          59.55 |                       59.30 |        97.27 |                                                     137472.00 |                                             584930.50 |
| yugabytedb-1-1-3 | yugabytedb-1-1-3 |                1 |        1280 |    16380 |               1 |           5 |          -1 | 1200.00 |            2 |                          57.38 |                       57.10 |        93.67 |                                                    1884007.00 |                                            1363025.20 |
| yugabytedb-1-1-4 | yugabytedb-1-1-4 |                1 |        1280 |    16380 |               1 |          10 |          -1 | 1200.00 |            0 |                          58.20 |                       57.93 |        95.02 |                                                     151583.00 |                                            1126131.20 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     26653.00 |     40.09 |          21.26 |                 48.02 |
| yugabytedb-1-1-2-1 |     26653.00 |     40.09 |          21.26 |                 48.02 |
| yugabytedb-1-1-3-1 |     26653.00 |     40.09 |          21.26 |                 48.02 |
| yugabytedb-1-1-4-1 |     26653.00 |     40.09 |          21.26 |                 48.02 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       110.72 |      0.14 |           0.25 |                  0.27 |
| yugabytedb-1-1-2-1 |       110.72 |      0.14 |           0.25 |                  0.27 |
| yugabytedb-1-1-3-1 |       110.72 |      0.14 |           0.25 |                  0.27 |
| yugabytedb-1-1-4-1 |       110.72 |      0.14 |           0.25 |                  0.27 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |    190409.81 |    122.95 |           0.39 |                  0.39 |
| yugabytedb-1-1-2-1 |    190409.81 |    122.95 |           0.39 |                  0.39 |
| yugabytedb-1-1-3-1 |    190409.81 |    122.95 |           0.39 |                  0.39 |
| yugabytedb-1-1-4-1 |    190409.81 |    122.95 |           0.39 |                  0.39 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     14522.96 |     19.79 |          39.18 |                 48.04 |
| yugabytedb-1-1-2-1 |     13301.04 |     20.11 |          39.93 |                 48.04 |
| yugabytedb-1-1-3-1 |     14240.26 |     22.55 |          41.05 |                 47.83 |
| yugabytedb-1-1-4-1 |     13763.11 |     22.26 |          42.28 |                 48.04 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       495.30 |      4.01 |           0.36 |                  0.39 |
| yugabytedb-1-1-2-1 |       381.72 |      3.61 |           0.36 |                  0.38 |
| yugabytedb-1-1-3-1 |       576.17 |      4.02 |           0.36 |                  0.39 |
| yugabytedb-1-1-4-1 |       502.57 |      4.01 |           0.36 |                  0.39 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       559.68 |      1.01 |           3.57 |                  3.57 |
| yugabytedb-1-1-2-1 |       632.36 |      2.65 |           2.25 |                  2.25 |
| yugabytedb-1-1-3-1 |       905.34 |      6.16 |           0.98 |                  0.98 |
| yugabytedb-1-1-4-1 |      1347.17 |     13.94 |           0.64 |                  0.64 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-3-1 (bexhoma-metrics-yugabytedb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-3-1 (bexhoma-metrics-yugabytedb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-4-1 (bexhoma-metrics-yugabytedb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-4-1 (bexhoma-metrics-yugabytedb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)

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
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: efficiency contains no 0 or NaN
* TEST passed: Workflow as planned
