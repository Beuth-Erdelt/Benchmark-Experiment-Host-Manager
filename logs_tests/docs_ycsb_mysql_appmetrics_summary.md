## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1198s 
* Code: 1783877650
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
  * Experiment uses bexhoma version 0.10.5.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:2164173213696
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1109714
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783877650
* MySQL-1-1-2-1 uses docker image mysql:8.4.0
  * RAM:2164173213696
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1109715
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783877650
* MySQL-1-1-3-1 uses docker image mysql:8.4.0
  * RAM:2164173213696
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1109716
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783877650
* MySQL-1-1-4-1 uses docker image mysql:8.4.0
  * RAM:2164173213696
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1109716
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1783877650

### SUT Container Restarts
* bexhoma-sut-mysql-1-1783877650-7c85cbbc77-xxwd8: 0 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: ycsb (8 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: ycsb (8 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| MySQL-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7415.02 |                50573.00 |            375000.00 |                             12535.00 | 3.00 |              213.55 |
| MySQL-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7366.37 |                50907.00 |            375000.00 |                             12239.00 | 3.00 |              212.15 |
| MySQL-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7283.53 |                51486.00 |            375000.00 |                             12383.00 | 3.00 |              209.77 |
| MySQL-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7449.05 |                50342.00 |            375000.00 |                             12207.00 | 3.00 |              214.53 |
| MySQL-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7361.31 |                50942.00 |            375000.00 |                             12375.00 | 3.00 |              212.01 |
| MySQL-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7460.31 |                50266.00 |            375000.00 |                             12191.00 | 3.00 |              214.86 |
| MySQL-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7368.69 |                50891.00 |            375000.00 |                             12279.00 | 3.00 |              212.22 |
| MySQL-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7334.10 |                51131.00 |            375000.00 |                             12599.00 | 3.00 |              211.22 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              209.77 |                        59038.40 |                51486.00 |           3000000.00 |                             12351.00 |

### Execution

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32157.44 |                93291.00 |            1500723 |                             751.00 |              1499277 |                               680.00 |
| MySQL-1-1-2-1-1 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4046.70 |                92668.00 |             187081 |                             769.00 |               187919 |                               680.00 |
| MySQL-1-1-2-1-2 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4051.38 |                92561.00 |             187061 |                             895.00 |               187939 |                               777.00 |
| MySQL-1-1-2-1-3 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4057.39 |                92424.00 |             187159 |                             815.00 |               187841 |                               702.00 |
| MySQL-1-1-2-1-4 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4047.71 |                92645.00 |             188096 |                             760.00 |               186904 |                               679.00 |
| MySQL-1-1-2-1-5 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4052.56 |                92534.00 |             187269 |                             879.00 |               187731 |                               794.00 |
| MySQL-1-1-2-1-6 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4047.49 |                92650.00 |             187430 |                             757.00 |               187570 |                               685.00 |
| MySQL-1-1-2-1-7 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4049.33 |                92608.00 |             187279 |                             774.00 |               187721 |                               678.00 |
| MySQL-1-1-2-1-8 | MySQL-1-1-2 | MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4054.58 |                92488.00 |             187392 |                             826.00 |               187608 |                               712.00 |
| MySQL-1-1-3-1-1 | MySQL-1-1-3 | MySQL-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        47647.79 |                62962.00 |            1500175 |                            1045.00 |              1499825 |                               818.00 |
| MySQL-1-1-4-1-1 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6032.92 |                62159.00 |             187570 |                             849.00 |               187430 |                               739.00 |
| MySQL-1-1-4-1-2 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6048.87 |                61995.00 |             187591 |                            1033.00 |               187409 |                               853.00 |
| MySQL-1-1-4-1-3 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6058.75 |                61894.00 |             187010 |                            1128.00 |               187990 |                               960.00 |
| MySQL-1-1-4-1-4 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6041.96 |                62066.00 |             188050 |                             866.00 |               186950 |                               744.00 |
| MySQL-1-1-4-1-5 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6054.34 |                61939.00 |             187559 |                            1057.00 |               187441 |                               852.00 |
| MySQL-1-1-4-1-6 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6032.04 |                62168.00 |             187159 |                             830.00 |               187841 |                               706.00 |
| MySQL-1-1-4-1-7 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6040.69 |                62079.00 |             187653 |                            1001.00 |               187347 |                               791.00 |
| MySQL-1-1-4-1-8 | MySQL-1-1-4 | MySQL-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6051.90 |                61964.00 |             187073 |                            1048.00 |               187927 |                               878.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32157.44 |                93291.00 |            1500723 |                             751.00 |              1499277 |                               680.00 |
| MySQL-1-1-2 | MySQL-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32407.14 |                92668.00 |            1498767 |                             895.00 |              1501233 |                               794.00 |
| MySQL-1-1-3 | MySQL-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        47647.79 |                62962.00 |            1500175 |                            1045.00 |              1499825 |                               818.00 |
| MySQL-1-1-4 | MySQL-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48361.47 |                62168.00 |            1499665 |                            1128.00 |              1500335 |                               960.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       611.00 |     12.04 |          25.52 |                 31.34 |
| MySQL-1-1-2-1 |       611.00 |     12.04 |          25.52 |                 31.34 |
| MySQL-1-1-3-1 |       611.00 |     12.04 |          25.52 |                 31.34 |
| MySQL-1-1-4-1 |       611.00 |     12.04 |          25.52 |                 31.34 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       319.53 |     11.06 |           0.13 |                  0.14 |
| MySQL-1-1-2-1 |       319.53 |     11.06 |           0.13 |                  0.14 |
| MySQL-1-1-3-1 |       319.53 |     11.06 |           0.13 |                  0.14 |
| MySQL-1-1-4-1 |       319.53 |     11.06 |           0.13 |                  0.14 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       324.86 |      3.89 |          25.57 |                 32.08 |
| MySQL-1-1-2-1 |       284.84 |      3.90 |          25.60 |                 32.78 |
| MySQL-1-1-3-1 |       148.34 |      5.39 |          25.63 |                 33.29 |
| MySQL-1-1-4-1 |       259.83 |      5.14 |          25.67 |                 34.38 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       371.22 |      4.05 |           0.16 |                  0.16 |
| MySQL-1-1-2-1 |       392.49 |      8.94 |           0.16 |                  0.16 |
| MySQL-1-1-3-1 |       427.58 |     11.16 |           0.16 |                  0.16 |
| MySQL-1-1-4-1 |       238.27 |     14.50 |           0.16 |                  0.16 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           0.00 |                   14306.98 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-2-1 |                           0.00 |                   14306.98 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-3-1 |                           0.00 |                   14306.98 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-4-1 |                           0.00 |                   14306.98 |                     0.04 |                0.00 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                   18726.11 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-2-1 |                           1.00 |                   20525.17 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-3-1 |                           0.00 |                   21969.72 |                     0.04 |                0.00 |                    0.00 |
| MySQL-1-1-4-1 |                           0.00 |                   20976.62 |                     0.04 |                0.00 |                    0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
