## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1318s 
* Code: 1793639198
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
  * Experiment is limited to DBMS ['MySQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699450
  * datadisk:34723
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1793639198

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793639198-558dfb6986-ph9g2: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.87 |               977542.00 |                 6241 |                              9143.00 |             118759 |                            5875.00 |                            0 |                                        0.00 |
| mysql-1-1-1-1-2 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.89 |               977406.00 |                 6228 |                              8655.00 |             118772 |                            6095.00 |                            0 |                                        0.00 |
| mysql-1-1-1-1-3 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.89 |               977437.00 |                 6250 |                              8615.00 |             118707 |                            5959.00 |                           43 |                                    23023.00 |
| mysql-1-1-1-1-4 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.88 |               977505.00 |                 6250 |                              8511.00 |             118717 |                            5847.00 |                           33 |                                    21695.00 |
| mysql-1-1-1-1-5 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.88 |               977484.00 |                 6203 |                              8559.00 |             118797 |                            5827.00 |                            0 |                                        0.00 |
| mysql-1-1-1-1-6 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.87 |               977585.00 |                 6038 |                              8975.00 |             118962 |                            6103.00 |                            0 |                                        0.00 |
| mysql-1-1-1-1-7 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.87 |               977577.00 |                 6250 |                              9007.00 |             118726 |                            6011.00 |                           24 |                                    22959.00 |
| mysql-1-1-1-1-8 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.89 |               977440.00 |                 6317 |                              8535.00 |             118683 |                            6067.00 |                            0 |                                        0.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.02 |               977585.00 |                49777 |                              9143.00 |             950123 |                            6103.00 |                          100 |                                    23023.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
