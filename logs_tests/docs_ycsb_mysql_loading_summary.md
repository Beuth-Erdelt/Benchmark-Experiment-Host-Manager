## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2493s 
* Code: 1794702462
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
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 4 and 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [32, 64] threads, split into [4, 8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1197901
  * datadisk:34750
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794702462
* mysql-2-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1197890
  * datadisk:34722
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794702462
* mysql-3-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1197901
  * datadisk:34750
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794702462
* mysql-4-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1197901
  * datadisk:34722
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794702462

### Ingestion
* MySQL-1: 4 of 4 units ok
* MySQL-2: 8 of 8 units ok
* MySQL-3: 4 of 4 units ok
* MySQL-4: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794702462-7cb84bc6d9-qk24g: 0
* bexhoma-sut-mysql-2-1794702462-6c6c49695f-tpzwp: 0
* bexhoma-sut-mysql-3-1794702462-7fb9f858b9-d927n: 0
* bexhoma-sut-mysql-4-1794702462-5ddbcb7f95-v5zcs: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-4 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-3 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-4 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.77 |               977453.00 |            250000.00 |                              1242.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.77 |               977434.00 |            250000.00 |                              1241.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.74 |               977550.00 |            250000.00 |                              1269.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |   256.00 |        4.00 |     0.00 |                          255.75 |               977535.00 |            250000.00 |                              1197.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-1 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.90 |               977292.00 |            125000.00 |                              1322.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-2 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.90 |               977299.00 |            125000.00 |                              1363.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-3 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.91 |               977256.00 |            125000.00 |                              1312.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-4 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.90 |               977296.00 |            125000.00 |                              1298.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-5 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.89 |               977430.00 |            125000.00 |                              1326.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-6 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.89 |               977382.00 |            125000.00 |                              1332.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-7 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.90 |               977306.00 |            125000.00 |                              1336.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-8 |             1.00 |      4.00 |   128.00 |        8.00 |     0.00 |                          127.89 |               977383.00 |            125000.00 |                              1329.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-1 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.61 |               978071.00 |            250000.00 |                              1325.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-2 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.60 |               978109.00 |            250000.00 |                              1386.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-3 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.56 |               978251.00 |            250000.00 |                              1399.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-4 |             1.00 |     16.00 |   256.00 |        4.00 |     0.00 |                          255.62 |               978011.00 |            250000.00 |                              1335.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.83 |               977846.00 |            125000.00 |                              1442.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.82 |               977945.00 |            125000.00 |                              1373.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.82 |               977957.00 |            125000.00 |                              1394.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.84 |               977775.00 |            125000.00 |                              1392.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.84 |               977809.00 |            125000.00 |                              1392.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.83 |               977890.00 |            125000.00 |                              1353.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.82 |               977972.00 |            125000.00 |                              1368.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |     0.00 |                          127.81 |               977999.00 |            125000.00 |                              1373.00 | 1.00 |                3.68 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     32.00 |  1024.00 |        4.00 |     0.00 | 1.00 |                3.68 |                         1023.03 |               977550.00 |           1000000.00 |                              1237.25 |
| MySQL-2-1 |             1.00 |     32.00 |  1024.00 |        8.00 |     0.00 | 1.00 |                3.68 |                         1023.20 |               977430.00 |           1000000.00 |                              1327.25 |
| MySQL-3-1 |             1.00 |     64.00 |  1024.00 |        4.00 |     0.00 | 1.00 |                3.68 |                         1022.38 |               978251.00 |           1000000.00 |                              1361.25 |
| MySQL-4-1 |             1.00 |     64.00 |  1024.00 |        8.00 |     0.00 | 1.00 |                3.68 |                         1022.60 |               977999.00 |           1000000.00 |                              1385.88 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1020.96 |               979472.00 |             499891 |                            1193.00 |               500109 |                              4415.00 |
| mysql-2-1-1-1-1 | mysql-2-1-1 | mysql-2-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1020.61 |               979806.00 |             499712 |                            1198.00 |               500288 |                              4391.00 |
| mysql-3-1-1-1-1 | mysql-3-1-1 | mysql-3-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1021.46 |               978991.00 |             499652 |                            1186.00 |               500348 |                              4391.00 |
| mysql-4-1-1-1-1 | mysql-4-1-1 | mysql-4-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1021.21 |               979226.00 |             500122 |                            1202.00 |               499878 |                              4391.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1020.96 |               979472.00 |             499891 |                            1193.00 |               500109 |                              4415.00 |
| mysql-2-1-1 | mysql-2-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1020.61 |               979806.00 |             499712 |                            1198.00 |               500288 |                              4391.00 |
| mysql-3-1-1 | mysql-3-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1021.46 |               978991.00 |             499652 |                            1186.00 |               500348 |                              4391.00 |
| mysql-4-1-1 | mysql-4-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1021.21 |               979226.00 |             500122 |                            1202.00 |               499878 |                              4391.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
