## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 18369s 
* Code: 1780401423
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
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MySQL-1-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:36G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780401423
* MySQL-1-2-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:37G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780401423

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1], [1]]

#### Planned

* DBMS MySQL-1 - Pods [[1], [1]]

### Loading

#### Per Connection

| connection    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-0-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13859599.00 |            125000.00 |                          15671295.00 |
| MySQL-1-1-0-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13859976.00 |            125000.00 |                          15704063.00 |
| MySQL-1-1-0-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13859372.00 |            125000.00 |                          15302655.00 |
| MySQL-1-1-0-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13860975.00 |            125000.00 |                          15597567.00 |
| MySQL-1-1-0-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.03 |             13838752.00 |            125000.00 |                          15359999.00 |
| MySQL-1-1-0-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.03 |             13850251.00 |            125000.00 |                          15376383.00 |
| MySQL-1-1-0-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13859977.00 |            125000.00 |                          15278079.00 |
| MySQL-1-1-0-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13861550.00 |            125000.00 |                          15294463.00 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                           72.17 |             13861550.00 |           1000000.00 |                          15448063.00 |

### Execution

#### Per Connection

| DBMS          | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                          870.36 |              1148951.00 |             500404 |                            1849.00 |               499596 |                           2787327.00 |
| MySQL-1-2-1-1 | MySQL-1         |                2 |        1 |       1 |        64 |     1024 |           1 |            0 |                          721.94 |              1385149.00 |             500619 |                            2027.00 |               499381 |                           3078143.00 |

#### Per Phase

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                          870.36 |              1148951.00 |          500404.00 |                            1849.00 |            499596.00 |                           2787327.00 |
| MySQL-1-2-1 |             2.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                          721.94 |              1385149.00 |          500619.00 |                            2027.00 |            499381.00 |                           3078143.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
