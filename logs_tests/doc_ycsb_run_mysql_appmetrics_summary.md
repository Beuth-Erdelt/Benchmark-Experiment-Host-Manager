## Show Summary

### Workload
YCSB SF=3
    Type: ycsb
    Duration: 25277s 
    Code: 1772846566
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 3000000.
    Ordering of inserts is hashed.
    Number of operations is 3000000.
    Batch size is ''.
    Target is based on multiples of '16384'.
    Factors for loading are [4].
    Factors for benchmarking are [2, 3].
    Experiment uses bexhoma version 0.9.1.
    System metrics are monitored by a cluster-wide installation.
    Application metrics are monitored by sidecar containers.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-64-8-65536-1 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:190003
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1772846566
MySQL-64-8-65536-2 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:193475
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1772846566
MySQL-64-8-65536-3 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:196921
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1772846566
MySQL-64-8-65536-4 uses docker image mysql:8.4.0
    RAM:541008474112
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:200363
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    limits_memory:64Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1772846566

### Loading
                  experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
MySQL-64-8-65536               1       64   65536          8           0                     633.607259              4736619.0             3000000                            295903.0

### Execution
                    experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
MySQL-64-8-65536-1               1       64   32768          1           0                         530.91              5650681.0           1500583                            1283.0             1499417                           3960831.0
MySQL-64-8-65536-2               1       64   32768          8           0                         627.54              4808141.0           1498553                            1248.0             1501447                           3467263.0
MySQL-64-8-65536-3               1       64   49152          1           0                         653.43              4591190.0           1499590                            1256.0             1500410                           3201023.0
MySQL-64-8-65536-4               1       64   49152          8           0                         641.87              4704412.0           1498668                            1232.0             1501332                           3317759.0

### Workflow

#### Actual
DBMS MySQL-64-8-65536 - Pods [[1, 8, 1, 8]]

#### Planned
DBMS MySQL-64-8-65536 - Pods [[1, 8, 1, 8]]

### Monitoring

### Loading phase: SUT deployment
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1     2497.34     0.67         25.65                35.75
MySQL-64-8-65536-2     2497.34     0.67         25.65                35.75
MySQL-64-8-65536-3     2497.34     0.67         25.65                35.75
MySQL-64-8-65536-4     2497.34     0.67         25.65                35.75

### Loading phase: component loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1      762.95     0.48          0.13                 0.13
MySQL-64-8-65536-2      762.95     0.48          0.13                 0.13
MySQL-64-8-65536-3      762.95     0.48          0.13                 0.13
MySQL-64-8-65536-4      762.95     0.48          0.13                 0.13

### Execution phase: SUT deployment
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1     1614.56     0.32         25.81                40.29
MySQL-64-8-65536-2     1567.04     0.38         25.98                44.84
MySQL-64-8-65536-3     1553.36     0.37         26.15                49.39
MySQL-64-8-65536-4     1548.54     0.38         26.30                53.92

### Execution phase: component benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-64-8-65536-1      579.12     0.10          0.16                 0.16
MySQL-64-8-65536-2      577.81     0.41          0.15                 0.15
MySQL-64-8-65536-3      617.54     0.16          0.16                 0.16
MySQL-64-8-65536-4      564.58     0.37          0.15                 0.15

### Application Metrics

#### Loading phase: SUT deployment
                    InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-64-8-65536-1                           1.0                    714.48                    0.04                  0                      0
MySQL-64-8-65536-2                           1.0                    714.48                    0.04                  0                      0
MySQL-64-8-65536-3                           1.0                    714.48                    0.04                  0                      0
MySQL-64-8-65536-4                           1.0                    714.48                    0.04                  0                      0

#### Execution phase: SUT deployment
                    InnoDB Buffer Pool Hit Ratio  Queries Per Second (QPS)  Connection Usage Ratio  Slow Queries Rate  InnoDB Log Waits Rate
MySQL-64-8-65536-1                           1.0                    575.94                    0.04                0.0                    0.0
MySQL-64-8-65536-2                           0.0                    714.85                    0.04                0.0                    0.0
MySQL-64-8-65536-3                           0.0                    689.63                    0.04                0.0                    0.0
MySQL-64-8-65536-4                           0.0                    697.59                    0.04                0.0                    0.0

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
