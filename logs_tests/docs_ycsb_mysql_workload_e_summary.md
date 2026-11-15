## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1378s 
* Code: 1794715697
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
  * Experiment uses bexhoma version 0.11.17.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046837
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
    * code:1794715697

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794715697-57f6f85456-rnclb: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |         8 |      128 |        0 |                          127.82 |               977965.00 |                 6276 |                              8431.00 |             118724 |                            5943.00 |
| mysql-1-1-1-1-2 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       2 |         8 |      128 |        0 |                          127.83 |               977830.00 |                 6289 |                              8591.00 |             118711 |                            5975.00 |
| mysql-1-1-1-1-3 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       3 |         8 |      128 |        0 |                          127.80 |               978092.00 |                 6206 |                              8407.00 |             118794 |                            5883.00 |
| mysql-1-1-1-1-4 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       4 |         8 |      128 |        0 |                          127.82 |               977942.00 |                 6326 |                              8351.00 |             118674 |                            5827.00 |
| mysql-1-1-1-1-5 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       5 |         8 |      128 |        0 |                          127.83 |               977868.00 |                 6245 |                              8231.00 |             118755 |                            5847.00 |
| mysql-1-1-1-1-6 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       6 |         8 |      128 |        0 |                          127.83 |               977840.00 |                 6281 |                              8743.00 |             118719 |                            6015.00 |
| mysql-1-1-1-1-7 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       7 |         8 |      128 |        0 |                          127.84 |               977779.00 |                 6327 |                              8495.00 |             118673 |                            5915.00 |
| mysql-1-1-1-1-8 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       8 |         8 |      128 |        0 |                          127.83 |               977860.00 |                 6251 |                              8107.00 |             118749 |                            6131.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           8 |        64 |     1024 |        0 |                         1022.60 |               978092.00 |                50201 |                              8743.00 |             949799 |                            6131.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
