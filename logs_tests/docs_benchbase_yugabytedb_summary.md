## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1322s 
* Code: 1794853811
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['YugabyteDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
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
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1276537
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:661027
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1276618
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406628
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:661018
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1276621
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1406432
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794853811
* yugabytedb-1-1-2-1 uses docker image postgres:15.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1278724
  * datadisk:39
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * yb-tserver 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:661934
    * cpu_list:0-127
  * yb-tserver 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1278727
    * cpu_list:0-223
  * yb-tserver 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1407373
    * cpu_list:0-127
  * yb-master 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:661936
    * cpu_list:0-127
  * yb-master 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1278788
    * cpu_list:0-223
  * yb-master 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1407373
    * cpu_list:0-127
  * resources_total: 0.25 CPU, 0.5 GiB RAM requested in 1 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794853811

### Ingestion
* YugabyteDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-yugabytedb-1-1794853811-6955bcbbf9-x5x4l: 0
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

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| YugabyteDB-1-1 |                1 |   16 |      445.00 |         305.00 |            0.00 |        138.00 |            2.00 |              1 |         1 |             | None           |             0 | False         |              129.44 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1-1-1 | yugabytedb-1-1-1 | yugabytedb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         319.79 |                      318.62 |         0.00 |                                                     127120.00 |                                              50013.00 |
| yugabytedb-1-1-2-1-1 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                         150.57 |                      149.83 |         0.00 |                                                     132826.00 |                                              53103.00 |
| yugabytedb-1-1-2-1-2 | yugabytedb-1-1-2 | yugabytedb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        0 |                         146.76 |                      146.11 |         0.00 |                                                     132883.00 |                                              54484.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| yugabytedb-1-1-1 | yugabytedb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         319.79 |                      318.62 |         0.00 |                                                     127120.00 |                                              50013.00 |
| yugabytedb-1-1-2 | yugabytedb-1-1-2 |                1 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        0 |                         297.32 |                      295.94 |         0.00 |                                                     132883.00 |                                              53793.50 |

### Monitoring

### Loading phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |      2847.97 |     26.94 |           8.53 |                 16.28 |
| yugabytedb-1-1-2-1 |      2847.97 |     26.94 |           8.53 |                 16.28 |

### Loading phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        26.08 |      0.12 |           0.30 |                  0.33 |
| yugabytedb-1-1-2-1 |        26.08 |      0.12 |           0.30 |                  0.33 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       727.07 |     12.16 |           0.26 |                  0.26 |
| yugabytedb-1-1-2-1 |       727.07 |     12.16 |           0.26 |                  0.26 |

### Benchmarking phase: component yb-tserver

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |     10231.11 |     38.02 |          10.60 |                 19.92 |
| yugabytedb-1-1-2-1 |      9767.29 |     35.25 |          11.27 |                 22.33 |

### Benchmarking phase: component yb-master

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |        17.27 |      0.18 |           0.31 |                  0.34 |
| yugabytedb-1-1-2-1 |        20.42 |      0.18 |           0.32 |                  0.34 |

### Benchmarking phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| yugabytedb-1-1-1-1 |       143.68 |      1.00 |           0.31 |                  0.31 |
| yugabytedb-1-1-2-1 |       272.25 |      1.20 |           0.27 |                  0.27 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-1-1 (bexhoma-metrics-yugabytedb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection yugabytedb-1-1-2-1 (bexhoma-metrics-yugabytedb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
           : storage bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-1 exists
TiDB-1                        : storage bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-2 exists
TiDB-1                        : storage bxw-bx-pd-ti-nvme-benchbase-tpcc-16-0 exists
TiDB-1                        : storage bxw-bx-pd-ti-nvme-benchbase-tpcc-16-1 exists
TiDB-1                        : storage bxw-bx-pd-ti-nvme-benchbase-tpcc-16-2 exists
Loop pass                     : took 2.5s (1 kubectl calls 1.3s, 17 API requests 0.7s)
- waiting 30s -               : done
TiDB-1                        : waits for health check to succeed
Loop pass                     : took 1.0s (0 kubectl calls 0.0s, 23 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : worker pods found: ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : found 3 / 3 running workers (component pd)
TiDB-1                        : worker pods found: ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : found 3 / 3 running workers (component tikv)
TiDB-1                        : will start benchmarking but not before 2026-11-14 16:20:11 (that is in 60 secs)
Loop pass                     : took 2.6s (0 kubectl calls 0.0s, 37 API requests 1.7s)
- waiting 30s -               : done
TiDB-1                        : will start benchmarking but not before 2026-11-14 16:20:11
Loop pass                     : took 0.7s (0 kubectl calls 0.0s, 16 API requests 0.7s)
- waiting 30s -               : done
Experiment                    : Reset experiment counter. This is first run of client number 1.
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-2-1-TiDB-1-1794671794 initialized to 1.
TiDB-1                        : benchmarks done 1 of 2. This will be client 1
tidb-1-2-1-1                  : start benchmarking (benchmark_run=1)
TiDB-1                        : worker pods found: ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : worker pods found: ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-5t8qc
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-7fclf
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-pxpmr
tidb-1-2-1-1                  : needs monitoring (common metrics) for deployment sut
tidb-1-2-1-1                  : needs monitoring (custom metrics) for stateful set pd
tidb-1-2-1-1                  : needs monitoring (custom metrics) for stateful set tikv
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : benchmarking results in folder D:\data\benchmarks/1794671794
TiDB-1                        : submitted benchmarker job in 51.6s (6 kubectl calls 6.5s, 169 API requests 41.0s)
Loop pass                     : took 54.4s (6 kubectl calls 6.5s, 192 API requests 42.5s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 23 API requests 0.8s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.9s (0 kubectl calls 0.0s, 21 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.2s (0 kubectl calls 0.0s, 21 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 21 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 0.9s (0 kubectl calls 0.0s, 21 API requests 0.9s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 21 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.1s (0 kubectl calls 0.0s, 21 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.9s (0 kubectl calls 0.0s, 21 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 2.6s (0 kubectl calls 0.0s, 21 API requests 1.1s)
- waiting 30s -               : done
tidb-1-2-1-1                  : wrote benchmarking_timespans to D:/data/benchmarks/1794671794/tidb-1-2-1-1.config
tidb-1-2-1-1                  : showing benchmarker times
tidb-1-2-1-1                  : benchmarker timespan job from 1794673266 to 1794673587
tidb-1-2-1-1                  : benchmarker timespan pods from 1794673269 to 1794673571
tidb-1-2-1-1                  : benchmarker timespan (start to end single container [s]) = 302
tidb-1-2-1-1                  : benchmarker times (start/end per pod and container) = [(1794673269, 1794673571)]
tidb-1-2-1-1                  : found and updated times {'benchmarker': [(1794673269, 1794673571)]}
tidb-1-2-1-1                  : needs monitoring (common metrics) for deployment sut
tidb-1-2-1-1                  : collecting execution metrics of SUT at connection tidb-1-2-1-1
tidb-1-2-1-1                  : needs monitoring (custom metrics) for stateful set pd
tidb-1-2-1-1                  : collecting execution metrics of pd at connection tidb-1-2-1-1
tidb-1-2-1-1                  : needs monitoring (custom metrics) for stateful set tikv
tidb-1-2-1-1                  : collecting execution metrics of tikv at connection tidb-1-2-1-1
tidb-1-2-1-1                  : collecting metrics of benchmarker at connection tidb-1-2-1-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-2
tidb-1-2-1-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)tidb-1-1794671794(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)tidb-1-1794671794(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-1-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)bx-pd-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)bx-pd-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-1-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)bx-tikv-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)bx-tikv-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-1-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-tidb-1-1794671794-2-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-tidb-1-1794671794-2-1-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-1-1                  : WARNING metric missing for benchmarking: CPU Throttling Rate [s/s]
tidb-1-2-1-1                  : WARNING metric missing for benchmarking: CPU Throttled Time [s]
tidb-1-2-1-1                  : WARNING metric missing for benchmarker: CPU Throttling Rate [s/s]
tidb-1-2-1-1                  : WARNING metric missing for benchmarker: CPU Throttled Time [s]
tidb-1-2-1-1                  : WARNING metric missing for tikvbenchmarking: CPU Throttling Rate [s/s]
tidb-1-2-1-1                  : WARNING metric missing for tikvbenchmarking: CPU Throttled Time [s]
Experiment                    : fetched 4 metric sets in 6s (4 at once, 0 repeated, 0 follow-up actions; 6 kubectl calls 16.7s, 0 API requests 0.0s)
Loop pass                     : took 18.1s (14 kubectl calls 25.3s, 32 API requests 2.8s)
Experiment                    : Reset experiment counter. This is first run of client number 2.
Experiment                    : Round pod counter bexhoma-benchmarker-podcount-round-2-2-TiDB-1-1794671794 initialized to 2.
TiDB-1                        : benchmarks done 1 of 2. This will be client 2
tidb-1-2-2-1                  : start benchmarking (benchmark_run=1)
TiDB-1                        : worker pods found: ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : distributed system - get host info for worker bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : worker pods found: ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : distributed system - get host info for worker bx-tikv-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-5t8qc
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-7fclf
TiDB-1                        : distributed system - get host info for sut bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-pxpmr
tidb-1-2-2-1                  : needs monitoring (common metrics) for deployment sut
tidb-1-2-2-1                  : needs monitoring (custom metrics) for stateful set pd
tidb-1-2-2-1                  : needs monitoring (custom metrics) for stateful set tikv
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : benchmarking results in folder D:\data\benchmarks/1794671794
TiDB-1                        : submitted benchmarker job in 12.9s (3 kubectl calls 3.5s, 66 API requests 8.4s)
Loop pass                     : took 14.6s (3 kubectl calls 3.5s, 90 API requests 9.6s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.3s (0 kubectl calls 0.0s, 24 API requests 1.2s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 22 API requests 1.2s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.2s (0 kubectl calls 0.0s, 22 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 22 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.2s (0 kubectl calls 0.0s, 22 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 22 API requests 1.1s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 9.8s (0 kubectl calls 0.0s, 22 API requests 1.0s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 2.0s (0 kubectl calls 0.0s, 22 API requests 1.2s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.2s (0 kubectl calls 0.0s, 22 API requests 1.2s)
- waiting 30s -               : done
TiDB-1                        : has running benchmarks
Loop pass                     : took 1.8s (0 kubectl calls 0.0s, 22 API requests 0.9s)
- waiting 30s -               : done
tidb-1-2-2-1                  : wrote benchmarking_timespans to D:/data/benchmarks/1794671794/tidb-1-2-2-1.config
tidb-1-2-2-1                  : showing benchmarker times
tidb-1-2-2-1                  : benchmarker timespan job from 1794673615 to 1794673980
tidb-1-2-2-1                  : benchmarker timespan pods from 1794673632 to 1794673934
tidb-1-2-2-1                  : benchmarker timespan (start to end single container [s]) = 302
tidb-1-2-2-1                  : benchmarker times (start/end per pod and container) = [(1794673632, 1794673934), (1794673632, 1794673934)]
tidb-1-2-2-1                  : found and updated times {'benchmarker': [(1794673632, 1794673934), (1794673632, 1794673934)]}
tidb-1-2-2-1                  : needs monitoring (common metrics) for deployment sut
tidb-1-2-2-1                  : collecting execution metrics of SUT at connection tidb-1-2-2-1
tidb-1-2-2-1                  : needs monitoring (custom metrics) for stateful set pd
tidb-1-2-2-1                  : collecting execution metrics of pd at connection tidb-1-2-2-1
tidb-1-2-2-1                  : needs monitoring (custom metrics) for stateful set tikv
tidb-1-2-2-1                  : collecting execution metrics of tikv at connection tidb-1-2-2-1
tidb-1-2-2-1                  : collecting metrics of benchmarker at connection tidb-1-2-2-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-pd-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-0 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-1 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : get size via pod bx-tikv-ti-nvme-benchbase-tpcc-16-2 and write to pvc bxw-bx-tikv-ti-nvme-benchbase-tpcc-16-2
tidb-1-2-2-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)tidb-1-1794671794(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)tidb-1-1794671794(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-2-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)bx-pd-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)bx-pd-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-2-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"(.*)bx-tikv-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"(.*)bx-tikv-ti-nvme-benchbase-tpcc-16-(.*)", namespace="perdelt", container="dbms"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-2-1                  : example metric {'type': 'cluster', 'active': True, 'metric': 'gauge', 'query': '(sum(max((container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-tidb-1-1794671794-2-2-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"} and (time() - timestamp(container_memory_working_set_bytes{pod=~"bexhoma-benchmarker-tidb-1-1794671794-2-2-1-[a-z0-9]{5}", namespace="perdelt", container="dbmsbenchmarker"})) < 90)) by (instance)))/1024/1024', 'title': 'Memory Usage, Working Set [MiB]'}
tidb-1-2-2-1                  : WARNING metric missing for benchmarker: CPU Throttling Rate [s/s]
tidb-1-2-2-1                  : WARNING metric missing for benchmarker: CPU Throttled Time [s]
tidb-1-2-2-1                  : WARNING metric missing for tikvbenchmarking: CPU Throttling Rate [s/s]
tidb-1-2-2-1                  : WARNING metric missing for tikvbenchmarking: CPU Throttled Time [s]
tidb-1-2-2-1                  : WARNING metric missing for benchmarking: CPU Throttling Rate [s/s]
tidb-1-2-2-1                  : WARNING metric missing for benchmarking: CPU Throttled Time [s]
Experiment                    : fetched 4 metric sets in 7s (4 at once, 0 repeated, 0 follow-up actions; 6 kubectl calls 19.8s, 0 API requests 0.0s)
Loop pass                     : took 20.7s (16 kubectl calls 30.7s, 36 API requests 2.9s)
TiDB-1                        : can be stopped
TiDB-1                        : had 0 restarts at worker bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-5t8qc
TiDB-1                        : had 0 restarts at worker bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-7fclf
TiDB-1                        : had 0 restarts at worker bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-pxpmr
TiDB-1                        : worker pods found: ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-pd-ti-nvme-benchbase-tpcc-16-0', 'bx-pd-ti-nvme-benchbase-tpcc-16-1', 'bx-pd-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : had 0 restarts at worker bx-pd-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : had 0 restarts at worker bx-pd-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : had 0 restarts at worker bx-pd-ti-nvme-benchbase-tpcc-16-2
TiDB-1                        : worker pods found: ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : worker pods found (only stateful set pods): ['bx-tikv-ti-nvme-benchbase-tpcc-16-0', 'bx-tikv-ti-nvme-benchbase-tpcc-16-1', 'bx-tikv-ti-nvme-benchbase-tpcc-16-2']
TiDB-1                        : had 0 restarts at worker bx-tikv-ti-nvme-benchbase-tpcc-16-0
TiDB-1                        : had 0 restarts at worker bx-tikv-ti-nvme-benchbase-tpcc-16-1
TiDB-1                        : had 0 restarts at worker bx-tikv-ti-nvme-benchbase-tpcc-16-2
Loop pass                     : took 25.0s (19 kubectl calls 21.0s, 59 API requests 2.5s)
Experiment                    : ends at 2026-11-14 17:33:40.835045 (310562.1913098) - 2224.48s total
Experiment                    : transforming metrics for loading
Experiment                    : transforming metrics for loading completed
Experiment                    : transforming metrics for benchmarking
Experiment                    : transforming metrics for benchmarking completed
Experiment                    : transforming metrics for loader
Experiment                    : transforming metrics for loader completed
Experiment                    : transforming metrics for benchmarker
Experiment                    : transforming metrics for benchmarker completed
Experiment                    : transforming metrics for loading
Experiment                    : transforming metrics for loading completed
Experiment                    : transforming metrics for pdloading
Experiment                    : transforming metrics for pdloading completed
Experiment                    : transforming metrics for tikvloading
Experiment                    : transforming metrics for tikvloading completed
Experiment                    : transforming metrics for loader
Experiment                    : transforming metrics for loader completed
Experiment                    : transforming metrics for benchmarking
Experiment                    : transforming metrics for benchmarking completed
Experiment                    : transforming metrics for pdbenchmarking
Experiment                    : transforming metrics for pdbenchmarking completed
Experiment                    : transforming metrics for tikvbenchmarking
Experiment                    : transforming metrics for tikvbenchmarking completed
Experiment                    : transforming metrics for benchmarker
Experiment                    : transforming metrics for benchmarker completed
Experiment                    : downloading partial results
Experiment                    : uploading full results
Experiment                    : uploading workload file
Result workflow complete

## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2225s 
* Code: 1794671794
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 1 processes (pods).
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
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
* tidb-1-1-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:613794
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
    * disk:613794
    * cpu_list:0-127
  * sut 1
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:282051
    * cpu_list:0-255
  * sut 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384403
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:613794
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146787
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-223
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384403
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:613794
    * datadisk:7591
    * volume_size:49G
    * volume_used:7.5G
    * cpu_list:0-127
  * tikv 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146788
    * datadisk:5380
    * volume_size:49G
    * volume_used:5.3G
    * cpu_list:0-223
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384403
    * datadisk:7576
    * volume_size:49G
    * volume_used:7.4G
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794671794
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-1-2-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1081853952000
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-137-generic
  * node:cl-worker37
  * disk:613793
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
    * disk:613793
    * cpu_list:0-127
  * sut 1
    * RAM:540597886976
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:282054
    * cpu_list:0-255
  * sut 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384319
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:613793
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146790
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-223
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384319
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:613793
    * datadisk:5121
    * volume_size:49G
    * volume_used:5.1G
    * cpu_list:0-127
  * tikv 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146790
    * datadisk:7004
    * volume_size:49G
    * volume_used:6.9G
    * cpu_list:0-223
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1384319
    * datadisk:5025
    * volume_size:49G
    * volume_used:5.0G
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794671794
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* tidb-1-2-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:770370
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:770366
    * cpu_list:0-255
  * sut 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * cpu_list:0-127
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146789
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-223
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * datadisk:4608
    * volume_size:49G
    * volume_used:4.5G
    * cpu_list:0-127
  * tikv 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146789
    * datadisk:4631
    * volume_size:49G
    * volume_used:4.6G
    * cpu_list:0-223
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * datadisk:4647
    * volume_size:49G
    * volume_used:4.6G
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794671794
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
    * ddl_num_worker_replicas:3
* tidb-1-2-2-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:787183
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * sut 0
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:787183
    * cpu_list:0-255
  * sut 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * cpu_list:0-127
  * sut 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * pd 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146790
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-223
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * datadisk:123
    * volume_size:9.8G
    * volume_used:123M
    * cpu_list:0-127
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:614875
    * datadisk:7042
    * volume_size:49G
    * volume_used:6.9G
    * cpu_list:0-127
  * tikv 1
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1146790
    * datadisk:7038
    * volume_size:49G
    * volume_used:6.9G
    * cpu_list:0-223
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1383524
    * datadisk:7056
    * volume_size:49G
    * volume_used:6.9G
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 385.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794671794
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
    * ddl_num_worker_replicas:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: TiDB-1-2

### Data Parameters of Reused Volumes
* TiDB-1: DDL values of the volume: num_worker_replicas=3
* TiDB-1: loading values of the volume: script=Schema, indexing=Checks

### Ingestion
* TiDB-1: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-tidb-1-1794671794-57cb8499bb-b4d9s: 0
* bexhoma-sut-tidb-1-1794671794-57cb8499bb-g2bk6: 0
* bexhoma-sut-tidb-1-1794671794-57cb8499bb-kvwfc: 0
* bx-pd-ti-nvme-benchbase-tpcc-16-0: 0
* bx-pd-ti-nvme-benchbase-tpcc-16-1: 0
* bx-pd-ti-nvme-benchbase-tpcc-16-2: 0
* bx-tikv-ti-nvme-benchbase-tpcc-16-0: 0
* bx-tikv-ti-nvme-benchbase-tpcc-16-1: 0
* bx-tikv-ti-nvme-benchbase-tpcc-16-2: 0
* bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-5t8qc: 0
* bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-7fclf: 0
* bexhoma-sut-tidb-1-1794671794-84d8d7b8f7-pxpmr: 0

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

| DBMS     |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| TiDB-1-1 |                1 |   16 |      178.00 |           4.00 |            0.00 |        171.00 |            3.00 |              1 |         1 |             | None           |             0 | False         |              323.60 | False               |
| TiDB-1-2 |                2 |   16 |      178.00 |           4.00 |            0.00 |        171.00 |            3.00 |              1 |         1 |             | None           |             0 | False         |              323.60 | True                |

### Benchmarking

#### Per Connection

| connection     | phase      | job          |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:-----------|:-------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         261.16 |                      260.01 |         0.00 |                                                     142258.00 |                                              61251.00 |
| tidb-1-1-2-1-1 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                          85.64 |                       84.82 |         0.00 |                                                     261190.00 |                                              92643.00 |
| tidb-1-1-2-1-2 | tidb-1-1-2 | tidb-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        0 |                          85.32 |                       84.48 |         0.00 |                                                     265375.00 |                                              93375.00 |
| tidb-1-2-1-1-1 | tidb-1-2-1 | tidb-1-2-1-1 |                2 |        1 |               1 |       1 |        16 |    16384 |          -1 | 300.00 |        0 |                         388.18 |                      386.37 |         0.00 |                                                      90154.00 |                                              41209.00 |
| tidb-1-2-2-1-1 | tidb-1-2-2 | tidb-1-2-2-1 |                2 |        2 |               1 |       1 |         8 |     8192 |          -1 | 300.00 |        0 |                         142.10 |                      140.59 |         0.00 |                                                     129096.00 |                                              56263.00 |
| tidb-1-2-2-1-2 | tidb-1-2-2 | tidb-1-2-2-1 |                2 |        2 |               1 |       2 |         8 |     8192 |          -1 | 300.00 |        0 |                         154.61 |                      152.86 |         0.00 |                                                     121664.00 |                                              51716.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------|:-----------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         261.16 |                      260.01 |         0.00 |                                                     142258.00 |                                              61251.00 |
| tidb-1-1-2 | tidb-1-1-2 |                1 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        0 |                         170.96 |                      169.31 |         0.00 |                                                     265375.00 |                                              93009.00 |
| tidb-1-2-1 | tidb-1-2-1 |                2 |        1 |               1 |           1 |        16 |    16384 |          -1 | 300.00 |        0 |                         388.18 |                      386.37 |         0.00 |                                                      90154.00 |                                              41209.00 |
| tidb-1-2-2 | tidb-1-2-2 |                2 |        2 |               1 |           2 |        16 |    16384 |          -1 | 300.00 |        0 |                         296.71 |                      293.46 |         0.00 |                                                     129096.00 |                                              53989.50 |

### Monitoring

### Loading phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      1190.33 |      8.95 |           3.35 |                  3.93 |
| tidb-1-1-2-1 |      1190.33 |      8.95 |           3.35 |                  3.93 |

### Loading phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |        84.65 |      0.52 |           0.21 |                  0.21 |
| tidb-1-1-2-1 |        84.65 |      0.52 |           0.21 |                  0.21 |

### Loading phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      2696.38 |     20.81 |          13.34 |                 29.84 |
| tidb-1-1-2-1 |      2696.38 |     20.81 |          13.34 |                 29.84 |

### Loading phase: component loader

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       114.52 |      1.34 |           0.56 |                  0.56 |
| tidb-1-1-2-1 |       114.52 |      1.34 |           0.56 |                  0.56 |

### Benchmarking phase: SUT deployment

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      2800.82 |     10.08 |           3.35 |                  3.93 |
| tidb-1-1-2-1 |      1947.22 |      9.28 |           2.15 |                  2.73 |
| tidb-1-2-1-1 |      3035.57 |     10.96 |           1.87 |                  2.45 |
| tidb-1-2-2-1 |      2621.77 |      8.97 |           2.49 |                  3.07 |

### Benchmarking phase: component pd

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       301.46 |      1.04 |           0.22 |                  0.22 |
| tidb-1-1-2-1 |       248.62 |      1.05 |           0.22 |                  0.22 |
| tidb-1-2-1-1 |       164.32 |      0.65 |           0.26 |                  0.26 |
| tidb-1-2-2-1 |       176.05 |      0.69 |           0.27 |                  0.27 |

### Benchmarking phase: component tikv

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |      3781.57 |     16.05 |          14.75 |                 31.95 |
| tidb-1-1-2-1 |      2708.51 |     13.63 |          16.13 |                 32.26 |
| tidb-1-2-1-1 |      4528.13 |     17.29 |          11.46 |                 26.18 |
| tidb-1-2-2-1 |      3807.01 |     15.66 |          13.45 |                 32.14 |

### Benchmarking phase: component benchmarker

| DBMS         |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------|-------------:|----------:|---------------:|----------------------:|
| tidb-1-1-1-1 |       145.34 |      0.55 |           0.32 |                  0.32 |
| tidb-1-1-2-1 |       117.71 |      0.46 |           0.29 |                  0.29 |
| tidb-1-2-1-1 |       182.46 |      0.86 |           0.32 |                  0.32 |
| tidb-1-2-2-1 |       412.57 |      1.54 |           0.30 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-1-1 (bexhoma-metrics-tidb-1-1-1-1-tikvloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-1-2-1 (bexhoma-metrics-tidb-1-1-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-1-1 (bexhoma-metrics-tidb-1-2-1-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection tidb-1-2-2-1 (bexhoma-metrics-tidb-1-2-2-1-tikvbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
