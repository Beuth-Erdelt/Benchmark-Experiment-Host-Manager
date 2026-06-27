## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1190s 
* Code: 1781466611
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Experiment uses bexhoma version 0.9.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:247628
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781466611
* MySQL-1-1-2-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:251070
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781466611
* MySQL-1-1-3-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:254511
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781466611
* MySQL-1-1-4-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:257955
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781466611

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1, 8, 1, 8]]

#### Planned

* DBMS MySQL-1 - Pods [[1, 8, 1, 8]]

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| MySQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4718.46 |                79475.00 |            375000.00 |                              4971.00 | 3.00 |              135.89 |
| MySQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4686.62 |                80015.00 |            375000.00 |                              4923.00 | 3.00 |              134.97 |
| MySQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4713.96 |                79551.00 |            375000.00 |                              4875.00 | 3.00 |              135.76 |
| MySQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4667.08 |                80350.00 |            375000.00 |                              4971.00 | 3.00 |              134.41 |
| MySQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4704.55 |                79710.00 |            375000.00 |                              4887.00 | 3.00 |              135.49 |
| MySQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4693.48 |                79898.00 |            375000.00 |                              4915.00 | 3.00 |              135.17 |
| MySQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4695.01 |                79872.00 |            375000.00 |                              5019.00 | 3.00 |              135.22 |
| MySQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         4709.46 |                79627.00 |            375000.00 |                              4923.00 | 3.00 |              135.63 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              134.41 |                        37588.63 |                80350.00 |           3000000.00 |                              4935.50 |

### Execution

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32062.24 |                93568.00 |            1499830 |                             962.00 |              1500170 |                              4795.00 |
| MySQL-1-1-2-1-5 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4053.66 |                92509.00 |             187576 |                             940.00 |               187424 |                              3401.00 |
| MySQL-1-1-2-1-6 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4046.40 |                92675.00 |             187426 |                             873.00 |               187574 |                              3351.00 |
| MySQL-1-1-2-1-2 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4052.70 |                92531.00 |             187686 |                             893.00 |               187314 |                              3373.00 |
| MySQL-1-1-2-1-1 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4045.35 |                92699.00 |             187333 |                             880.00 |               187667 |                              3319.00 |
| MySQL-1-1-2-1-3 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4057.91 |                92412.00 |             187446 |                             947.00 |               187554 |                              3385.00 |
| MySQL-1-1-2-1-8 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4058.84 |                92391.00 |             187362 |                             957.00 |               187638 |                              3421.00 |
| MySQL-1-1-2-1-4 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4050.46 |                92582.00 |             188262 |                             897.00 |               186738 |                              3361.00 |
| MySQL-1-1-2-1-7 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4052.56 |                92534.00 |             186837 |                             929.00 |               188163 |                              3377.00 |
| MySQL-1-1-3-1-1 | MySQL-1-1-3 | MySQL-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        47533.79 |                63113.00 |            1499322 |                             843.00 |              1500678 |                              6119.00 |
| MySQL-1-1-4-1-2 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6048.29 |                62001.00 |             187484 |                             926.00 |               187516 |                              4391.00 |
| MySQL-1-1-4-1-5 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6055.81 |                61924.00 |             187489 |                             942.00 |               187511 |                              4399.00 |
| MySQL-1-1-4-1-3 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6060.21 |                61879.00 |             186996 |                             932.00 |               188004 |                              4247.00 |
| MySQL-1-1-4-1-4 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6040.20 |                62084.00 |             187320 |                             913.00 |               187680 |                              4287.00 |
| MySQL-1-1-4-1-7 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6049.36 |                61990.00 |             187470 |                             924.00 |               187530 |                              4363.00 |
| MySQL-1-1-4-1-8 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6062.08 |                61860.00 |             186951 |                            1100.00 |               188049 |                              4247.00 |
| MySQL-1-1-4-1-1 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6045.56 |                62029.00 |             187630 |                             876.00 |               187370 |                              4271.00 |
| MySQL-1-1-4-1-6 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6033.60 |                62152.00 |             187418 |                             875.00 |               187582 |                              4235.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32062.24 |                93568.00 |            1499830 |                             962.00 |              1500170 |                              4795.00 |
| MySQL-1-1-2 | MySQL-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32417.88 |                92699.00 |            1499928 |                             957.00 |              1500072 |                              3421.00 |
| MySQL-1-1-3 | MySQL-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        47533.79 |                63113.00 |            1499322 |                             843.00 |              1500678 |                              6119.00 |
| MySQL-1-1-4 | MySQL-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48395.11 |                62152.00 |            1498758 |                            1100.00 |              1501242 |                              4399.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      1353.14 |     16.86 |          25.64 |                 35.75 |
| MySQL-1-1-2-1 |      1353.14 |     16.86 |          25.64 |                 35.75 |
| MySQL-1-1-3-1 |      1353.14 |     16.86 |          25.64 |                 35.75 |
| MySQL-1-1-4-1 |      1353.14 |     16.86 |          25.64 |                 35.75 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       414.16 |      6.19 |           0.13 |                  0.13 |
| MySQL-1-1-2-1 |       414.16 |      6.19 |           0.13 |                  0.13 |
| MySQL-1-1-3-1 |       414.16 |      6.19 |           0.13 |                  0.13 |
| MySQL-1-1-4-1 |       414.16 |      6.19 |           0.13 |                  0.13 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       845.40 |     12.81 |          25.78 |                 39.06 |
| MySQL-1-1-2-1 |       985.36 |     12.65 |          25.94 |                 44.24 |
| MySQL-1-1-3-1 |       754.84 |     15.73 |          26.07 |                 48.40 |
| MySQL-1-1-4-1 |       939.77 |     15.96 |          26.23 |                 53.84 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       307.65 |      5.95 |           0.16 |                  0.16 |
| MySQL-1-1-2-1 |       422.90 |      8.05 |           0.16 |                  0.16 |
| MySQL-1-1-3-1 |       278.53 |     11.49 |           0.15 |                  0.16 |
| MySQL-1-1-4-1 |       144.26 |     16.11 |           0.15 |                  0.16 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           0.00 |                   12536.22 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-2-1 |                           0.00 |                   12536.22 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-3-1 |                           0.00 |                   12536.22 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-4-1 |                           0.00 |                   12536.22 |                     0.04 |                0.00 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                   19427.26 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-2-1 |                           1.00 |                   21135.29 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-3-1 |                           0.00 |                   18595.57 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-4-1 |                           0.00 |                   16969.27 |                     0.04 |                0.00 |                    0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
