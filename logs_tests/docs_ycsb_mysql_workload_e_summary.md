## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2400s 
* Code: 1793824142
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
  * disk:850944
  * datadisk:34722
  * volume_size:49G
  * volume_used:34G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793824142

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793824142-57db6db5ff-smw4q: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (8 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (8 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.84 |               977786.00 |            125000.00 |                              1588.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.84 |               977789.00 |            125000.00 |                              1566.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.82 |               977953.00 |            125000.00 |                              1635.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.81 |               977996.00 |            125000.00 |                              1618.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.83 |               977871.00 |            125000.00 |                              1560.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.80 |               978083.00 |            125000.00 |                              1559.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.84 |               977798.00 |            125000.00 |                              1600.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.81 |               977985.00 |            125000.00 |                              1553.00 | 1.00 |                3.68 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.68 |                         1022.59 |               978083.00 |           1000000.00 |                              1584.88 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.87 |               977533.00 |                 6267 |                              8223.00 |             118733 |                            4687.00 |
| mysql-1-1-1-1-2 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.87 |               977547.00 |                 6211 |                              8711.00 |             118789 |                            4523.00 |
| mysql-1-1-1-1-3 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.89 |               977411.00 |                 6286 |                              8187.00 |             118714 |                            4435.00 |
| mysql-1-1-1-1-4 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.88 |               977449.00 |                 6204 |                              8471.00 |             118796 |                            4335.00 |
| mysql-1-1-1-1-5 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.87 |               977533.00 |                 6218 |                              8807.00 |             118782 |                            4331.00 |
| mysql-1-1-1-1-6 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.88 |               977474.00 |                 6336 |                              8391.00 |             118664 |                            4343.00 |
| mysql-1-1-1-1-7 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.87 |               977554.00 |                 6217 |                              8455.00 |             118783 |                            4399.00 |
| mysql-1-1-1-1-8 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.88 |               977458.00 |                 6253 |                              8231.00 |             118747 |                            4447.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.02 |               977554.00 |                49992 |                              8807.00 |             950008 |                            4687.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
