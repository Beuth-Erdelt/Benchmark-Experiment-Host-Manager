## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2060s 
* Code: 1780434280
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
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
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
    * code:1780434280

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[8]]

#### Planned

* DBMS MySQL-1 - Pods [[8]]

### Execution

#### Per Connection

| DBMS          | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:--------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| MySQL-1-1-1-6 | MySQL-1         |                1 |        1 |       6 |         8 |      128 |           8 |            0 |                          120.68 |              1035758.00 |                 6204 |                            500991.00 |             118796 |                            9911.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-8 | MySQL-1         |                1 |        1 |       8 |         8 |      128 |           8 |            0 |                          120.76 |              1035129.00 |                 6294 |                            499199.00 |             118706 |                           10063.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-2 | MySQL-1         |                1 |        1 |       2 |         8 |      128 |           8 |            0 |                          120.68 |              1035786.00 |                 6163 |                            520703.00 |             118837 |                            9663.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |       1 |         8 |      128 |           8 |            0 |                          120.92 |              1033741.00 |                 6156 |                            499199.00 |             118844 |                            9575.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-4 | MySQL-1         |                1 |        1 |       4 |         8 |      128 |           8 |            0 |                          120.61 |              1036361.00 |                 6206 |                            506623.00 |             118794 |                           10783.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-5 | MySQL-1         |                1 |        1 |       5 |         8 |      128 |           8 |            0 |                          120.80 |              1034731.00 |                 6250 |                            503295.00 |             118666 |                           10231.00 |                           84 |                                     8019.00 |
| MySQL-1-1-1-3 | MySQL-1         |                1 |        1 |       3 |         8 |      128 |           8 |            0 |                          120.77 |              1035015.00 |                 6185 |                            516607.00 |             118815 |                           10183.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-7 | MySQL-1         |                1 |        1 |       7 |         8 |      128 |           8 |            0 |                          120.68 |              1035769.00 |                 6250 |                            502527.00 |             118678 |                           10631.00 |                           72 |                                    17871.00 |

#### Per Phase

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| MySQL-1-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                          965.92 |              1036361.00 |             49708.00 |                            520703.00 |          950136.00 |                           10783.00 |                       156.00 |                                    17871.00 |

### Tests
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
