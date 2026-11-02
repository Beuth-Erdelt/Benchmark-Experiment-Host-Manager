## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 6843s 
* Code: 1793632316
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
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699365
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
    * code:1793632316
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699371
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
    * code:1793632316
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699374
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
    * code:1793632316
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699381
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
    * code:1793632316
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699405
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
    * code:1793632316
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699432
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
    * code:1793632316
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699435
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
    * code:1793632316
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:699443
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
    * code:1793632316

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1793632316-bd7c65ccb-fjxlk: 0
* bexhoma-sut-mysql-1-1793632316-649f7bc8cc-thjch: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: ycsb (16 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: ycsb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: ycsb (16 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: ycsb (16 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: ycsb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: ycsb (16 pods)

### Benchmarking

#### Per Connection

| DBMS             | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1  | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1021.93 |               978544.00 |             499989 |                            1975.00 |               500011 |                              6611.00 |
| mysql-1-1-2-1-1  | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                         1019.90 |               490244.00 |             249863 |                            1310.00 |               250137 |                              8099.00 |
| mysql-1-1-2-1-2  | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                         1019.82 |               490284.00 |             250239 |                            1330.00 |               249761 |                              7487.00 |
| mysql-1-1-3-1-1  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.89 |               977431.00 |              62389 |                            1408.00 |                62611 |                              7347.00 |
| mysql-1-1-3-1-2  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.87 |               977521.00 |              62436 |                            1384.00 |                62564 |                              7047.00 |
| mysql-1-1-3-1-3  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.87 |               977557.00 |              62471 |                            1474.00 |                62529 |                              7327.00 |
| mysql-1-1-3-1-4  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.89 |               977423.00 |              62299 |                            1405.00 |                62701 |                              7327.00 |
| mysql-1-1-3-1-5  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.88 |               977475.00 |              62143 |                            1389.00 |                62857 |                              7283.00 |
| mysql-1-1-3-1-6  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.88 |               977457.00 |              62350 |                            1377.00 |                62650 |                              7083.00 |
| mysql-1-1-3-1-7  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.88 |               977491.00 |              62463 |                            1376.00 |                62537 |                              7379.00 |
| mysql-1-1-3-1-8  | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.88 |               977471.00 |              62481 |                            1389.00 |                62519 |                              7543.00 |
| mysql-1-1-4-1-1  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                          127.65 |               489602.00 |              31124 |                            1681.00 |                31376 |                              6523.00 |
| mysql-1-1-4-1-2  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                          127.56 |               489955.00 |              31322 |                            1582.00 |                31178 |                              6471.00 |
| mysql-1-1-4-1-3  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                          127.59 |               489863.00 |              31317 |                            1791.00 |                31183 |                              6523.00 |
| mysql-1-1-4-1-4  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                          127.57 |               489915.00 |              31347 |                            1772.00 |                31153 |                              6515.00 |
| mysql-1-1-4-1-5  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                          127.62 |               489748.00 |              31293 |                            1782.00 |                31207 |                              6323.00 |
| mysql-1-1-4-1-6  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                          127.58 |               489903.00 |              31130 |                            1715.00 |                31370 |                              6499.00 |
| mysql-1-1-4-1-7  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                          127.60 |               489801.00 |              31346 |                            1726.00 |                31154 |                              6371.00 |
| mysql-1-1-4-1-8  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                          127.64 |               489660.00 |              31330 |                            1679.00 |                31170 |                              6411.00 |
| mysql-1-1-4-1-9  | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                          127.63 |               489702.00 |              31465 |                            1696.00 |                31035 |                              6335.00 |
| mysql-1-1-4-1-10 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                          127.58 |               489878.00 |              31376 |                            1711.00 |                31124 |                              6351.00 |
| mysql-1-1-4-1-11 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                          127.62 |               489720.00 |              31178 |                            1682.00 |                31322 |                              6527.00 |
| mysql-1-1-4-1-12 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                          127.62 |               489747.00 |              31178 |                            1657.00 |                31322 |                              6471.00 |
| mysql-1-1-4-1-13 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                          127.58 |               489906.00 |              31296 |                            1819.00 |                31204 |                              6443.00 |
| mysql-1-1-4-1-14 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                          127.60 |               489826.00 |              31228 |                            1812.00 |                31272 |                              6491.00 |
| mysql-1-1-4-1-15 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                          127.60 |               489819.00 |              31360 |                            1646.00 |                31140 |                              6343.00 |
| mysql-1-1-4-1-16 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                          127.61 |               489767.00 |              30896 |                            1651.00 |                31604 |                              6455.00 |
| mysql-1-2-1-1-1  | mysql-1-2-1 | mysql-1-2-1-1 | MySQL-1         |                2 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1022.16 |               978323.00 |             500218 |                            2101.00 |               499782 |                              7455.00 |
| mysql-1-2-2-1-1  | mysql-1-2-2 | mysql-1-2-2-1 | MySQL-1         |                2 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                         1019.35 |               490511.00 |             250095 |                            1401.00 |               249905 |                              6843.00 |
| mysql-1-2-2-1-2  | mysql-1-2-2 | mysql-1-2-2-1 | MySQL-1         |                2 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                         1019.94 |               490223.00 |             250373 |                            1404.00 |               249627 |                              6871.00 |
| mysql-1-2-3-1-1  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.80 |               978067.00 |              62508 |                            1468.00 |                62492 |                              6423.00 |
| mysql-1-2-3-1-2  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.84 |               977801.00 |              62361 |                            1550.00 |                62639 |                              6847.00 |
| mysql-1-2-3-1-3  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.83 |               977866.00 |              62491 |                            1465.00 |                62509 |                              6591.00 |
| mysql-1-2-3-1-4  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.85 |               977726.00 |              62727 |                            1434.00 |                62273 |                              6715.00 |
| mysql-1-2-3-1-5  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.81 |               978017.00 |              62491 |                            1491.00 |                62509 |                              6779.00 |
| mysql-1-2-3-1-6  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.84 |               977777.00 |              62711 |                            1440.00 |                62289 |                              6683.00 |
| mysql-1-2-3-1-7  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.81 |               978024.00 |              62383 |                            1475.00 |                62617 |                              6871.00 |
| mysql-1-2-3-1-8  | mysql-1-2-3 | mysql-1-2-3-1 | MySQL-1         |                2 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.84 |               977791.00 |              62578 |                            1452.00 |                62422 |                              6727.00 |
| mysql-1-2-4-1-1  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                          127.71 |               489405.00 |              31317 |                            1693.00 |                31183 |                              7543.00 |
| mysql-1-2-4-1-2  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                          127.67 |               489547.00 |              31227 |                            1647.00 |                31273 |                              7395.00 |
| mysql-1-2-4-1-3  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                          127.64 |               489669.00 |              31444 |                            1655.00 |                31056 |                              7423.00 |
| mysql-1-2-4-1-4  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                          127.71 |               489373.00 |              30956 |                            1743.00 |                31544 |                              7479.00 |
| mysql-1-2-4-1-5  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                          127.68 |               489491.00 |              31402 |                            1650.00 |                31098 |                              7531.00 |
| mysql-1-2-4-1-6  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                          127.68 |               489515.00 |              31291 |                            1675.00 |                31209 |                              7491.00 |
| mysql-1-2-4-1-7  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                          127.72 |               489346.00 |              31262 |                            1657.00 |                31238 |                              7283.00 |
| mysql-1-2-4-1-8  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                          127.70 |               489419.00 |              31247 |                            1682.00 |                31253 |                              7479.00 |
| mysql-1-2-4-1-9  | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                          127.67 |               489529.00 |              31223 |                            1583.00 |                31277 |                              7411.00 |
| mysql-1-2-4-1-10 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                          127.71 |               489377.00 |              31099 |                            1755.00 |                31401 |                              7531.00 |
| mysql-1-2-4-1-11 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                          127.71 |               489397.00 |              31093 |                            1718.00 |                31407 |                              7507.00 |
| mysql-1-2-4-1-12 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                          127.68 |               489497.00 |              31342 |                            1701.00 |                31158 |                              7483.00 |
| mysql-1-2-4-1-13 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                          127.73 |               489316.00 |              31228 |                            1717.00 |                31272 |                              7495.00 |
| mysql-1-2-4-1-14 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                          127.72 |               489365.00 |              31309 |                            1751.00 |                31191 |                              7471.00 |
| mysql-1-2-4-1-15 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                          127.69 |               489478.00 |              31426 |                            1678.00 |                31074 |                              7459.00 |
| mysql-1-2-4-1-16 | mysql-1-2-4 | mysql-1-2-4-1 | MySQL-1         |                2 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                          127.68 |               489521.00 |              31263 |                            1661.00 |                31237 |                              7447.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1021.93 |               978544.00 |             499989 |                            1975.00 |               500011 |                              6611.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |       128 |     2048 |               1 |           2 |            0 |                         2039.72 |               490284.00 |             500102 |                            1330.00 |               499898 |                              8099.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.04 |               977557.00 |             499032 |                            1474.00 |               500968 |                              7543.00 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |       128 |     2048 |               1 |          16 |            0 |                         2041.65 |               489955.00 |             500186 |                            1819.00 |               499814 |                              6527.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        64 |     1024 |               1 |           1 |            0 |                         1022.16 |               978323.00 |             500218 |                            2101.00 |               499782 |                              7455.00 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |       128 |     2048 |               1 |           2 |            0 |                         2039.29 |               490511.00 |             500468 |                            1404.00 |               499532 |                              6871.00 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |        64 |     1024 |               1 |           8 |            0 |                         1022.62 |               978067.00 |             500250 |                            1550.00 |               499750 |                              6871.00 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |       128 |     2048 |               1 |          16 |            0 |                         2043.10 |               489669.00 |             500129 |                            1755.00 |               499871 |                              7543.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
