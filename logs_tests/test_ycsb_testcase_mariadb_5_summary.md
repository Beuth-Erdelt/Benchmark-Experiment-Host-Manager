## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2404s 
* Code: 1780357927
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
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780357927
* MariaDB-1-1-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780357927

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1, 8]]

#### Planned

* DBMS MariaDB-1 - Pods [[1, 8]]

### Loading

#### Per Connection



#### Per Run



### Execution

#### Per Connection

| DBMS            | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1-1 | MariaDB-1       |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1023.41 |               977124.00 |             499187 |                            1738.00 |               500813 |                            271103.00 |
| MariaDB-1-1-2-6 | MariaDB-1       |                1 |        2 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976875.00 |              62590 |                            2109.00 |                62410 |                            342783.00 |
| MariaDB-1-1-2-2 | MariaDB-1       |                1 |        2 |       2 |         8 |      128 |           8 |            0 |                          127.96 |               976849.00 |              62447 |                            2097.00 |                62553 |                            340479.00 |
| MariaDB-1-1-2-8 | MariaDB-1       |                1 |        2 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976868.00 |              62478 |                            2187.00 |                62522 |                            343807.00 |
| MariaDB-1-1-2-1 | MariaDB-1       |                1 |        2 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976861.00 |              62654 |                            2149.00 |                62346 |                            343039.00 |
| MariaDB-1-1-2-4 | MariaDB-1       |                1 |        2 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976854.00 |              62596 |                            2063.00 |                62404 |                            345087.00 |
| MariaDB-1-1-2-3 | MariaDB-1       |                1 |        2 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976867.00 |              62520 |                            2129.00 |                62480 |                            337407.00 |
| MariaDB-1-1-2-5 | MariaDB-1       |                1 |        2 |       5 |         8 |      128 |           8 |            0 |                          127.96 |               976862.00 |              62215 |                            2243.00 |                62785 |                            346111.00 |
| MariaDB-1-1-2-7 | MariaDB-1       |                1 |        2 |       7 |         8 |      128 |           8 |            0 |                          127.96 |               976856.00 |              62386 |                            2161.00 |                62614 |                            346111.00 |

#### Per Phase

| DBMS          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1023.41 |               977124.00 |          499187.00 |                            1738.00 |            500813.00 |                            271103.00 |
| MariaDB-1-1-2 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                         1023.69 |               976875.00 |          499886.00 |                            2243.00 |            500114.00 |                            346111.00 |

### Monitoring

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       607.29 |      2.85 |           6.86 |                  6.96 |
| MariaDB-1-1-2 |       545.60 |      0.72 |           6.86 |                  6.96 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       143.19 |      0.37 |           0.13 |                  0.13 |
| MariaDB-1-1-2 |       143.19 |      0.63 |           0.13 |                  0.13 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading Phase: [OVERALL].Throughput(ops/sec) contains 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
