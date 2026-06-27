## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 4065s 
* Code: 1780345196
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
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

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
    * code:1780345196
* MariaDB-1-2-1 uses docker image mariadb:11.4.7
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
    * code:1780345196

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1], [1]]

#### Planned

* DBMS MariaDB-1 - Pods [[1], [1]]

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-0-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.16 |              1177492.00 |            125000.00 |                           1288191.00 |
| MariaDB-1-1-0-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.11 |              1177978.00 |            125000.00 |                           1309695.00 |
| MariaDB-1-1-0-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.17 |              1177394.00 |            125000.00 |                           1287167.00 |
| MariaDB-1-1-0-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.13 |              1177808.00 |            125000.00 |                           1286143.00 |
| MariaDB-1-1-0-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.10 |              1178188.00 |            125000.00 |                           1304575.00 |
| MariaDB-1-1-0-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.16 |              1177486.00 |            125000.00 |                           1298431.00 |
| MariaDB-1-1-0-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.12 |              1177939.00 |            125000.00 |                           1311743.00 |
| MariaDB-1-1-0-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.07 |              1178413.00 |            125000.00 |                           1309695.00 |

#### Per Run

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                          849.01 |              1178413.00 |           1000000.00 |                           1299455.00 |

### Execution

#### Per Connection

| DBMS            | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1-1 | MariaDB-1       |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1023.26 |               977266.00 |             499819 |                            1833.00 |               500181 |                            229759.00 |
| MariaDB-1-2-1-1 | MariaDB-1       |                2 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1023.44 |               977094.00 |             499534 |                            1602.00 |               500466 |                            212863.00 |

#### Per Phase

| DBMS          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1023.26 |               977266.00 |          499819.00 |                            1833.00 |            500181.00 |                            229759.00 |
| MariaDB-1-2-1 |             2.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1023.44 |               977094.00 |          499534.00 |                            1602.00 |            500466.00 |                            212863.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
