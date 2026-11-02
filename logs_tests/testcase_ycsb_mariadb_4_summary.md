## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1262s 
* Code: 1793655586
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
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808782
  * datadisk:1770
  * volume_size:49G
  * volume_used:1.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793655586

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793655586-7fb9968978-2fczb: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (8 pods)

### Benchmarking

#### Per Connection

| DBMS              | phase         | job             | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:------------------|:--------------|:----------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976867.00 |                 6250 |                              3991.00 |             118743 |                            1539.00 |                            7 |                                    12575.00 |
| mariadb-1-1-1-1-2 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.96 |               976882.00 |                 6076 |                              3857.00 |             118924 |                            1589.00 |                            0 |                                        0.00 |
| mariadb-1-1-1-1-3 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.95 |               976908.00 |                 6206 |                              3919.00 |             118794 |                            1494.00 |                            0 |                                        0.00 |
| mariadb-1-1-1-1-4 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.95 |               976922.00 |                 6216 |                              3857.00 |             118784 |                            1586.00 |                            0 |                                        0.00 |
| mariadb-1-1-1-1-5 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.96 |               976879.00 |                 6113 |                              3993.00 |             118887 |                            1551.00 |                            0 |                                        0.00 |
| mariadb-1-1-1-1-6 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976902.00 |                 6250 |                              3699.00 |             118697 |                            1515.00 |                           53 |                                     2209.00 |
| mariadb-1-1-1-1-7 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.96 |               976905.00 |                 6250 |                              3933.00 |             118748 |                            1522.00 |                            2 |                                     9879.00 |
| mariadb-1-1-1-1-8 | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976872.00 |                 6390 |                              3801.00 |             118610 |                            1551.00 |                            0 |                                        0.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.65 |               976922.00 |                49751 |                              3993.00 |             950187 |                            1589.00 |                           62 |                                    12575.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MariaDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
