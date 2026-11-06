## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2439s 
* Code: 1793626129
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
  * Experiment uses bexhoma version 0.11.12.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:838530
  * datadisk:34754
  * volume_size:1.8T
  * volume_used:819G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793626129
* mysql-2-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:838530
  * datadisk:34722
  * volume_size:1.8T
  * volume_used:819G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793626129
* mysql-3-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:838530
  * datadisk:34750
  * volume_size:1.8T
  * volume_used:819G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793626129
* mysql-4-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:838530
  * datadisk:34722
  * volume_size:1.8T
  * volume_used:819G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793626129

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793626129-5bc9754b5-dxnqt: 0
* bexhoma-sut-mysql-2-1793626129-6864d4dfdc-tghth: 0
* bexhoma-sut-mysql-3-1793626129-7566786f9c-jdllp: 0
* bexhoma-sut-mysql-4-1793626129-697866cbf9-jcgrk: 0

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

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.77 |               977455.00 |            250000.00 |                              1275.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.77 |               977458.00 |            250000.00 |                              1269.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.77 |               977448.00 |            250000.00 |                              1260.00 | 1.00 |                3.68 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          255.77 |               977446.00 |            250000.00 |                              1248.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-1 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977399.00 |            125000.00 |                              1284.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-2 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977368.00 |            125000.00 |                              1271.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-3 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977363.00 |            125000.00 |                              1263.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-4 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977304.00 |            125000.00 |                              1306.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-5 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977293.00 |            125000.00 |                              1284.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-6 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.91 |               977278.00 |            125000.00 |                              1302.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-7 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977315.00 |            125000.00 |                              1295.00 | 1.00 |                3.68 |
| mysql-2-1-0-1-8 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977302.00 |            125000.00 |                              1225.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-1 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.68 |               977780.00 |            250000.00 |                              1398.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-2 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.72 |               977644.00 |            250000.00 |                              1372.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-3 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.70 |               977727.00 |            250000.00 |                              1395.00 | 1.00 |                3.68 |
| mysql-3-1-0-1-4 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          255.67 |               977818.00 |            250000.00 |                              1372.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977581.00 |            125000.00 |                              1423.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977448.00 |            125000.00 |                              1361.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977505.00 |            125000.00 |                              1388.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977557.00 |            125000.00 |                              1336.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977409.00 |            125000.00 |                              1411.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977565.00 |            125000.00 |                              1425.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977499.00 |            125000.00 |                              1377.00 | 1.00 |                3.68 |
| mysql-4-1-0-1-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977547.00 |            125000.00 |                              1403.00 | 1.00 |                3.68 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     32.00 |  1024.00 |        4.00 |         0.00 | 1.00 |                3.68 |                         1023.07 |               977458.00 |           1000000.00 |                              1263.00 |
| MySQL-2-1 |             1.00 |     32.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.68 |                         1023.20 |               977399.00 |           1000000.00 |                              1278.75 |
| MySQL-3-1 |             1.00 |     64.00 |  1024.00 |        4.00 |         0.00 | 1.00 |                3.68 |                         1022.76 |               977818.00 |           1000000.00 |                              1384.25 |
| MySQL-4-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 | 1.00 |                3.68 |                         1023.00 |               977581.00 |           1000000.00 |                              1390.50 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.58 |               978878.00 |             499524 |                            1321.00 |               500476 |                              3217.00 |
| mysql-2-1-1-1-1 | mysql-2-1-1 | mysql-2-1-1-1 | MySQL-2         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.88 |               978590.00 |             499825 |                            1317.00 |               500175 |                              3199.00 |
| mysql-3-1-1-1-1 | mysql-3-1-1 | mysql-3-1-1-1 | MySQL-3         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.63 |               978830.00 |             501045 |                            1325.00 |               498955 |                              3237.00 |
| mysql-4-1-1-1-1 | mysql-4-1-1 | mysql-4-1-1-1 | MySQL-4         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.37 |               979076.00 |             499813 |                            1320.00 |               500187 |                              3193.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.58 |               978878.00 |             499524 |                            1321.00 |               500476 |                              3217.00 |
| mysql-2-1-1 | mysql-2-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.88 |               978590.00 |             499825 |                            1317.00 |               500175 |                              3199.00 |
| mysql-3-1-1 | mysql-3-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.63 |               978830.00 |             501045 |                            1325.00 |               498955 |                              3237.00 |
| mysql-4-1-1 | mysql-4-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.37 |               979076.00 |             499813 |                            1320.00 |               500187 |                              3193.00 |

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
