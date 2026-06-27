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
