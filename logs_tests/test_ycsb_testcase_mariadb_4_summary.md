## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1317s 
* Code: 1780356598
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'E'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
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
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780356598

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[8]]

#### Planned

* DBMS MariaDB-1 - Pods [[8]]

### Loading

#### Per Connection



#### Per Run



### Execution

#### Per Connection

| DBMS            | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| MariaDB-1-1-1-7 | MariaDB-1       |                1 |        1 |       7 |         8 |      128 |           8 |            0 |                          127.96 |               976885.00 |                 6177 |                            182399.00 |             118823 |                            2427.00 |                            0 |                                        0.00 |
| MariaDB-1-1-1-8 | MariaDB-1       |                1 |        1 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976879.00 |                 6352 |                            159743.00 |             118648 |                            2379.00 |                            0 |                                        0.00 |
| MariaDB-1-1-1-6 | MariaDB-1       |                1 |        1 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976871.00 |                 6143 |                            172927.00 |             118857 |                            2359.00 |                            0 |                                        0.00 |
| MariaDB-1-1-1-3 | MariaDB-1       |                1 |        1 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976861.00 |                 6250 |                            154367.00 |             118695 |                            2339.00 |                           55 |                                     1623.00 |
| MariaDB-1-1-1-4 | MariaDB-1       |                1 |        1 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976863.00 |                 6250 |                            174463.00 |             118559 |                            2399.00 |                          191 |                                     1504.00 |
| MariaDB-1-1-1-1 | MariaDB-1       |                1 |        1 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976859.00 |                 6250 |                            155135.00 |             118605 |                            2363.00 |                          145 |                                     1684.00 |
| MariaDB-1-1-1-5 | MariaDB-1       |                1 |        1 |       5 |         8 |      128 |           8 |            0 |                          127.96 |               976869.00 |                 6250 |                            168703.00 |             118748 |                            2437.00 |                            2 |                                     7987.00 |
| MariaDB-1-1-1-2 | MariaDB-1       |                1 |        1 |       2 |         8 |      128 |           8 |            0 |                          127.96 |               976866.00 |                 6232 |                            171647.00 |             118768 |                            2281.00 |                            0 |                                        0.00 |

#### Per Phase

| DBMS          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| MariaDB-1-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                         1023.68 |               976885.00 |             49904.00 |                            182399.00 |          949703.00 |                            2437.00 |                       393.00 |                                     7987.00 |

### Tests
* TEST failed: Loading Phase: [OVERALL].Throughput(ops/sec) contains 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
