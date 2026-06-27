## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 4009s 
* Code: 1780436349
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:47G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780436349
* MySQL-1-1-2 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:48G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780436349

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1, 8]]

#### Planned

* DBMS MySQL-1 - Pods [[1, 8]]

### Execution

#### Per Connection

| DBMS          | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                          652.25 |              1533148.00 |             500318 |                           46815.00 |               499682 |                           3174399.00 |
| MySQL-1-1-2-8 | MySQL-1         |                1 |        2 |       8 |         8 |      128 |           8 |            0 |                           81.87 |              1526776.00 |              62363 |                            1977.00 |                62637 |                           3074047.00 |
| MySQL-1-1-2-2 | MySQL-1         |                1 |        2 |       2 |         8 |      128 |           8 |            0 |                           81.80 |              1528065.00 |              62418 |                            1949.00 |                62582 |                           3078143.00 |
| MySQL-1-1-2-4 | MySQL-1         |                1 |        2 |       4 |         8 |      128 |           8 |            0 |                           81.97 |              1524923.00 |              62545 |                            1914.00 |                62455 |                           3176447.00 |
| MySQL-1-1-2-6 | MySQL-1         |                1 |        2 |       6 |         8 |      128 |           8 |            0 |                           82.01 |              1524218.00 |              62333 |                            1935.00 |                62667 |                           3194879.00 |
| MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |       1 |         8 |      128 |           8 |            0 |                           81.97 |              1525016.00 |              62588 |                            1965.00 |                62412 |                           3112959.00 |
| MySQL-1-1-2-3 | MySQL-1         |                1 |        2 |       3 |         8 |      128 |           8 |            0 |                           81.88 |              1526538.00 |              62284 |                            1931.00 |                62716 |                           3258367.00 |
| MySQL-1-1-2-5 | MySQL-1         |                1 |        2 |       5 |         8 |      128 |           8 |            0 |                           82.03 |              1523873.00 |              62546 |                            1947.00 |                62454 |                           3299327.00 |
| MySQL-1-1-2-7 | MySQL-1         |                1 |        2 |       7 |         8 |      128 |           8 |            0 |                           81.85 |              1527182.00 |              62627 |                            1922.00 |                62373 |                           3217407.00 |

#### Per Phase

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                          652.25 |              1533148.00 |          500318.00 |                           46815.00 |            499682.00 |                           3174399.00 |
| MySQL-1-1-2 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                          655.38 |              1528065.00 |          499704.00 |                            1977.00 |            500296.00 |                           3299327.00 |

### Monitoring

### Execution phase: SUT deployment

| DBMS        |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1 |       934.57 |      1.20 |           9.66 |                 42.24 |
| MySQL-1-1-2 |       887.17 |      1.20 |           9.68 |                 43.42 |

### Execution phase: component benchmarker

| DBMS        |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1 |       213.59 |      0.21 |           0.17 |                  0.17 |
| MySQL-1-1-2 |       213.59 |      0.79 |           0.16 |                  0.16 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
