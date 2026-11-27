## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 7849s 
* Code: 1795706682
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking has keying and thinking times activated. Benchmarking runs for 20 minutes.
  * Status is logged every 30ms.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.4.
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
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* yugabytedb-1-1-1-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:655220
  * datadisk:39
  * volume_size:1.8T
  * volume_used:640G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081742733312
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:736622
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:1081853997056
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:252052
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:655028
    * cpu_list:0-223
  * yb-master 0
    * RAM:1081742733312
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:736494
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:654964
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081853997056
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:251860
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795706682
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:649181
  * datadisk:39
  * volume_size:1.8T
  * volume_used:634G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081742733312
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:732358
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:1081853997056
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:246258
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:649181
    * cpu_list:0-223
  * yb-master 0
    * RAM:1081742733312
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:732442
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:649181
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081853997056
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:246258
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795706682
* yugabytedb-1-1-3-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:649399
  * datadisk:39
  * volume_size:1.8T
  * volume_used:635G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081742733312
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:731605
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:1081853997056
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:246313
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:649399
    * cpu_list:0-223
  * yb-master 0
    * RAM:1081742733312
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:731605
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:649399
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081853997056
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:246313
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795706682
* yugabytedb-1-1-4-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:649608
  * datadisk:39
  * volume_size:1.8T
  * volume_used:635G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081742733312
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:732572
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:1081853997056
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:246421
    * cpu_list:0-127
  * yb-tserver 2
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:649608
    * cpu_list:0-223
  * yb-master 0
    * RAM:1081742733312
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:732572
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:649609
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081853997056
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:246421
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795706682

### Ingestion
* YugabyteDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1795706682-6bc6486d6f-hbhpb: 0
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

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| YugabyteDB-1-1 |                1 |  128 |     2115.00 |         306.00 |            0.00 |       1808.00 |            1.00 |              1 |         1 |             | None           |             0 | False         |              217.87 | False               |

### Benchmarking

#### Per Connection

| connection            | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |    time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|--------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1  | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |      1280 |    16384 |          -1 | 1200.00 |        0 |                          58.04 |                       57.80 |        94.80 |                                                     128341.00 |                                            1106385.00 |
| yugabytedb-1-1-2-1-1  | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       1 |       640 |     8192 |          -1 | 1200.00 |        0 |                          29.38 |                       29.27 |        48.00 |                                                     122490.00 |                                             941645.00 |
| yugabytedb-1-1-2-1-2  | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       2 |       640 |     8192 |          -1 | 1200.00 |        0 |                          29.15 |                       29.03 |        47.62 |                                                     119536.00 |                                             986953.00 |
| yugabytedb-1-1-3-1-1  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |        3 |               1 |       1 |       256 |     3276 |          -1 | 1200.00 |        0 |                          11.70 |                       11.63 |        19.08 |                                                     131504.00 |                                             939114.00 |
| yugabytedb-1-1-3-1-2  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |        3 |               1 |       2 |       256 |     3276 |          -1 | 1200.00 |        0 |                          11.78 |                       11.73 |        19.24 |                                                     133786.00 |                                             841805.00 |
| yugabytedb-1-1-3-1-3  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |        3 |               1 |       3 |       256 |     3276 |          -1 | 1200.00 |        0 |                          11.63 |                       11.58 |        18.99 |                                                     135875.00 |                                             942913.00 |
| yugabytedb-1-1-3-1-4  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |        3 |               1 |       4 |       256 |     3276 |          -1 | 1200.00 |        0 |                          11.75 |                       11.70 |        19.19 |                                                     133095.00 |                                             909201.00 |
| yugabytedb-1-1-3-1-5  | yugabytedb-1-1-3 | yugabytedb-1-1-3-1 |                1 |        3 |               1 |       5 |       256 |     3276 |          -1 | 1200.00 |        0 |                          11.59 |                       11.54 |        18.92 |                                                     132972.00 |                                             909251.00 |
| yugabytedb-1-1-4-1-1  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       1 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.85 |                        5.83 |         9.57 |                                                     141822.00 |                                             904394.00 |
| yugabytedb-1-1-4-1-2  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       2 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.87 |                        5.85 |         9.60 |                                                     143802.00 |                                             906644.00 |
| yugabytedb-1-1-4-1-3  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       3 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.84 |                        5.81 |         9.53 |                                                     149758.00 |                                             804004.00 |
| yugabytedb-1-1-4-1-4  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       4 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.90 |                        5.88 |         9.64 |                                                     138677.00 |                                             895478.00 |
| yugabytedb-1-1-4-1-5  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       5 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.90 |                        5.88 |         9.64 |                                                     137757.00 |                                             892530.00 |
| yugabytedb-1-1-4-1-6  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       6 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.96 |                        5.93 |         9.73 |                                                     143589.00 |                                             882392.00 |
| yugabytedb-1-1-4-1-7  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       7 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.83 |                        5.81 |         9.53 |                                                     142389.00 |                                             827616.00 |
| yugabytedb-1-1-4-1-8  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       8 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.88 |                        5.84 |         9.59 |                                                     139836.00 |                                             887385.00 |
| yugabytedb-1-1-4-1-9  | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |       9 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.83 |                        5.80 |         9.51 |                                                     141562.00 |                                             898917.00 |
| yugabytedb-1-1-4-1-10 | yugabytedb-1-1-4 | yugabytedb-1-1-4-1 |                1 |        4 |               1 |      10 |       128 |     1638 |          -1 | 1200.00 |        0 |                           5.83 |                        5.80 |         9.51 |                                                     143078.00 |                                             870424.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |    time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|--------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |      1280 |    16384 |          -1 | 1200.00 |        0 |                          58.04 |                       57.80 |        94.80 |                                                     128341.00 |                                            1106385.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |        2 |               1 |           2 |      1280 |    16384 |          -1 | 1200.00 |        0 |                          58.53 |                       58.30 |        95.62 |                                                     122490.00 |                                             964299.00 |
| yugabytedb-1-1-3 | yugabytedb-1-1-3 |                1 |        3 |               1 |           5 |      1280 |    16380 |          -1 | 1200.00 |        0 |                          58.45 |                       58.18 |        95.42 |                                                     135875.00 |                                             908456.80 |
| yugabytedb-1-1-4 | yugabytedb-1-1-4 |                1 |        4 |               1 |          10 |      1280 |    16380 |          -1 | 1200.00 |        0 |                          58.69 |                       58.43 |        95.84 |                                                     149758.00 |                                             876978.40 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     29430.88 |     38.26 |          21.20 |                 48.03 |
| yugabytedb-1-1-2-1 |     29430.88 |     38.26 |          21.20 |                 48.03 |
| yugabytedb-1-1-3-1 |     29430.88 |     38.26 |          21.20 |                 48.03 |
| yugabytedb-1-1-4-1 |     29430.88 |     38.26 |          21.20 |                 48.03 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       102.35 |      0.20 |           0.30 |                  0.33 |
| yugabytedb-1-1-2-1 |       102.35 |      0.20 |           0.30 |                  0.33 |
| yugabytedb-1-1-3-1 |       102.35 |      0.20 |           0.30 |                  0.33 |
| yugabytedb-1-1-4-1 |       102.35 |      0.20 |           0.30 |                  0.33 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |    141539.38 |    122.28 |           0.39 |                  0.39 |
| yugabytedb-1-1-2-1 |    141539.38 |    122.28 |           0.39 |                  0.39 |
| yugabytedb-1-1-3-1 |    141539.38 |    122.28 |           0.39 |                  0.39 |
| yugabytedb-1-1-4-1 |    141539.38 |    122.28 |           0.39 |                  0.39 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     12854.18 |     20.81 |          38.84 |                 48.04 |
| yugabytedb-1-1-2-1 |     12301.34 |     19.15 |          40.59 |                 48.03 |
| yugabytedb-1-1-3-1 |     13004.97 |     19.43 |          41.32 |                 47.83 |
| yugabytedb-1-1-4-1 |     13072.01 |     19.04 |          41.06 |                 47.86 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       462.13 |      4.02 |           0.40 |                  0.43 |
| yugabytedb-1-1-2-1 |       454.26 |      4.01 |           0.41 |                  0.43 |
| yugabytedb-1-1-3-1 |       449.41 |      4.01 |           0.41 |                  0.44 |
| yugabytedb-1-1-4-1 |       441.83 |      4.01 |           0.41 |                  0.44 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       626.63 |      1.64 |           3.98 |                  3.98 |
| yugabytedb-1-1-2-1 |       680.11 |      2.55 |           2.23 |                  2.23 |
| yugabytedb-1-1-3-1 |       943.20 |      5.30 |           0.96 |                  0.96 |
| yugabytedb-1-1-4-1 |      1318.14 |     11.55 |           0.64 |                  0.64 |

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
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Loading phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-tserver contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component yb-master contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Monitoring returned data
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: efficiency contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Every pod ran for the configured time
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
