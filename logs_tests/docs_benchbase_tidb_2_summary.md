## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 3489s 
* Code: 1792083169
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Experiment uses bexhoma version 0.11.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 1 processes (pods).
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* tidb-1-1-1-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:368361
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368361
    * cpu_list:0-127
  * sut 1
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:1986668
    * cpu_list:0-55
  * sut 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:856022
    * cpu_list:0-255
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368361
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:540590784512
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-138-generic
    * node:cl-worker24
    * disk:164943
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-95
  * pd 2
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:1986668
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-55
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368361
    * volume_size:49G
    * volume_used:7.4G
    * cpu_list:0-127
  * tikv 1
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:1986668
    * volume_size:49G
    * volume_used:7.4G
    * cpu_list:0-55
  * tikv 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:856022
    * volume_size:49G
    * volume_used:7.3G
    * cpu_list:0-255
  * eval_parameters
    * code:1792083169
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-1-2-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:368363
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368363
    * cpu_list:0-127
  * sut 1
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:1986668
    * cpu_list:0-55
  * sut 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:856028
    * cpu_list:0-255
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368363
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:540590784512
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-138-generic
    * node:cl-worker24
    * disk:164948
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-95
  * pd 2
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:1986668
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-55
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368363
    * volume_size:49G
    * volume_used:6.1G
    * cpu_list:0-127
  * tikv 1
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:1986668
    * volume_size:49G
    * volume_used:6.0G
    * cpu_list:0-55
  * tikv 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:856032
    * volume_size:49G
    * volume_used:5.9G
    * cpu_list:0-255
  * eval_parameters
    * code:1792083169
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-2-1-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:540590792704
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker25
  * disk:157843
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:157843
    * cpu_list:0-95
  * sut 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:289121
    * cpu_list:0-255
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368354
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368354
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:1986488
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-55
  * pd 2
    * RAM:540590784512
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-138-generic
    * node:cl-worker24
    * disk:164944
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-95
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368354
    * volume_size:49G
    * volume_used:5.6G
    * cpu_list:0-127
  * tikv 1
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:1986487
    * volume_size:49G
    * volume_used:5.6G
    * cpu_list:0-55
  * tikv 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:855847
    * volume_size:49G
    * volume_used:5.5G
    * cpu_list:0-255
  * eval_parameters
    * code:1792083169
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-2-2-1 uses docker image pingcap/tidb:v7.1.6
  * RAM:540590792704
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-146-generic
  * node:cl-worker25
  * disk:157844
  * cpu_list:0-95
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:157845
    * cpu_list:0-95
  * sut 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:289094
    * cpu_list:0-255
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368355
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368355
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:1986488
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-55
  * pd 2
    * RAM:540590784512
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-138-generic
    * node:cl-worker24
    * disk:175432
    * volume_size:49G
    * volume_used:123M
    * cpu_list:0-95
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:368355
    * volume_size:49G
    * volume_used:7.8G
    * cpu_list:0-127
  * tikv 1
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:1986488
    * volume_size:49G
    * volume_used:7.7G
    * cpu_list:0-55
  * tikv 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:855840
    * volume_size:49G
    * volume_used:7.8G
    * cpu_list:0-255
  * eval_parameters
    * code:1792083169
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: TiDB-1-2

### SUT Container Restarts
* bexhoma-sut-tidb-1-1792083169-bfdf777dd-527ft: 0
* bexhoma-sut-tidb-1-1792083169-bfdf777dd-7c2b4: 0
* bexhoma-sut-tidb-1-1792083169-bfdf777dd-gxggv: 0
* bexhoma-pd-tidb-nvme-benchbase-tpcc-16-0: 0
* bexhoma-pd-tidb-nvme-benchbase-tpcc-16-1: 0
* bexhoma-pd-tidb-nvme-benchbase-tpcc-16-2: 0
* bexhoma-tikv-tidb-nvme-benchbase-tpcc-16-0: 0
* bexhoma-tikv-tidb-nvme-benchbase-tpcc-16-1: 0
* bexhoma-tikv-tidb-nvme-benchbase-tpcc-16-2: 0
* bexhoma-sut-tidb-1-1792083169-78bd6b8dfd-ffd4z: 0
* bexhoma-sut-tidb-1-1792083169-78bd6b8dfd-fxjqk: 0
* bexhoma-sut-tidb-1-1792083169-78bd6b8dfd-prgjt: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS TiDB-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 2 Client 2: benchbase (2 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS TiDB-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS TiDB-1 - Experiment 2 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|          |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| TiDB-1-1 |                1 |   16 |      203.00 |           3.00 |            0.00 |        197.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              283.74 | False               |
| TiDB-1-2 |                2 |   16 |      203.00 |           3.00 |            0.00 |        197.00 |            3.00 |              1 |           1 |             | None           |             0 | False         |              283.74 | True                |

### Benchmarking

#### Per Connection

| DBMS           | phase      | job          |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:-----------|:-------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         370.14 |                      368.51 |         0.00 |                                                      87553.00 |                                              43204.00 |
| tidb-1-1-2-1-1 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         207.46 |                      205.39 |         0.00 |                                                      91508.00 |                                              38552.00 |
| tidb-1-1-2-1-2 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         165.19 |                      163.49 |         0.00 |                                                      98121.00 |                                              48402.00 |
| tidb-1-2-1-1-1 | tidb-1-2-1 | tidb-1-2-1-1 |                2 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                         349.68 |                      348.05 |         0.00 |                                                     101100.00 |                                              45747.00 |
| tidb-1-2-2-1-1 | tidb-1-2-2 | tidb-1-2-2-1 |                2 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            0 |                         143.40 |                      141.82 |         0.00 |                                                     121089.00 |                                              55770.00 |
| tidb-1-2-2-1-2 | tidb-1-2-2 | tidb-1-2-2-1 |                2 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         166.10 |                      164.52 |         0.00 |                                                     117709.00 |                                              48142.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------|:-----------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         370.14 |                      368.51 |         0.00 |                                                      87553.00 |                                              43204.00 |
| tidb-1-1-2 | tidb-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         372.65 |                      368.88 |         0.00 |                                                      98121.00 |                                              43477.00 |
| tidb-1-2-1 | tidb-1-2-1 |                2 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                         349.68 |                      348.05 |         0.00 |                                                     101100.00 |                                              45747.00 |
| tidb-1-2-2 | tidb-1-2-2 |                2 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            0 |                         309.50 |                      306.35 |         0.00 |                                                     121089.00 |                                              51956.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      1242.11 |      8.80 |           2.17 |                  2.70 |
| tidb-1-1-2-1 |      1242.11 |      8.80 |           2.17 |                  2.70 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        63.07 |      0.32 |           0.25 |                  0.26 |
| tidb-1-1-2-1 |        63.07 |      0.32 |           0.25 |                  0.26 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      2292.20 |     16.41 |          11.27 |                 30.35 |
| tidb-1-1-2-1 |      2292.20 |     16.41 |          11.27 |                 30.35 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       119.07 |      1.29 |           0.46 |                  0.46 |
| tidb-1-1-2-1 |       119.07 |      1.29 |           0.46 |                  0.46 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      2652.84 |      9.24 |           1.88 |                  2.41 |
| tidb-1-1-2-1 |      2534.62 |      9.09 |           2.48 |                  3.00 |
| tidb-1-2-1-1 |      3360.97 |     12.24 |           1.57 |                  2.10 |
| tidb-1-2-2-1 |      2885.48 |     10.40 |           2.08 |                  2.61 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       359.92 |      1.33 |           0.24 |                  0.25 |
| tidb-1-1-2-1 |       384.85 |      1.29 |           0.25 |                  0.25 |
| tidb-1-2-1-1 |       575.73 |      2.00 |           0.28 |                  0.29 |
| tidb-1-2-2-1 |       465.16 |      1.77 |           0.29 |                  0.30 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      3705.53 |     13.51 |          14.06 |                 32.66 |
| tidb-1-1-2-1 |      3817.01 |     14.99 |          16.28 |                 35.02 |
| tidb-1-2-1-1 |      3574.73 |     12.69 |           9.74 |                 27.87 |
| tidb-1-2-2-1 |      2955.52 |     11.90 |          10.66 |                 32.12 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       411.25 |      1.46 |           0.35 |                  0.35 |
| tidb-1-1-2-1 |       302.50 |      1.12 |           0.58 |                  0.58 |
| tidb-1-2-1-1 |       153.83 |      0.86 |           0.32 |                  0.32 |
| tidb-1-2-2-1 |       272.85 |      1.20 |           0.59 |                  0.59 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-pdbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-pdbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-pdloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-pdloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-pdbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-pdbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-pdloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-pdloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-pdbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-pdbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-pdbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-pdbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component pd contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component tikv contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
