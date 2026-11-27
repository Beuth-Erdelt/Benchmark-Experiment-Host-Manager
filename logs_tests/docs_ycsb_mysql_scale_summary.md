## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 6808s 
* Code: 1795689963
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
  * Experiment uses bexhoma version 0.12.4.
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636120
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
    * code:1795689963
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636131
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
    * code:1795689963
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636133
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
    * code:1795689963
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636138
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
    * code:1795689963
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:638093
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
    * code:1795689963
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636127
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
    * code:1795689963
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636131
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
    * code:1795689963
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636136
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
    * code:1795689963

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1795689963-54477c7b4d-vd2c8: 0
* bexhoma-sut-mysql-1-1795689963-6c6fb546f9-xmq98: 0

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

| connection       | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1  | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1020.55 |               979865.00 |             498349 |                            2069.00 |               501651 |                              7271.00 |
| mysql-1-1-2-1-1  | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1019.53 |               490420.00 |             250500 |                            1371.00 |               249500 |                              6943.00 |
| mysql-1-1-2-1-2  | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1020.06 |               490165.00 |             249728 |                            1368.00 |               250272 |                              6971.00 |
| mysql-1-1-3-1-1  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.83 |               977835.00 |              62435 |                            1550.00 |                62565 |                              6799.00 |
| mysql-1-1-3-1-2  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.84 |               977748.00 |              62357 |                            1588.00 |                62643 |                              7011.00 |
| mysql-1-1-3-1-3  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.83 |               977897.00 |              62631 |                            1607.00 |                62369 |                              6999.00 |
| mysql-1-1-3-1-4  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.80 |               978057.00 |              62464 |                            1567.00 |                62536 |                              7043.00 |
| mysql-1-1-3-1-5  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.85 |               977733.00 |              62667 |                            1501.00 |                62333 |                              7071.00 |
| mysql-1-1-3-1-6  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.86 |               977643.00 |              62323 |                            1508.00 |                62677 |                              6963.00 |
| mysql-1-1-3-1-7  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.85 |               977692.00 |              62258 |                            1537.00 |                62742 |                              7111.00 |
| mysql-1-1-3-1-8  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.83 |               977876.00 |              62155 |                            1572.00 |                62845 |                              6939.00 |
| mysql-1-1-4-1-1  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.65 |               489627.00 |              31112 |                            1605.00 |                31388 |                              7003.00 |
| mysql-1-1-4-1-2  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.60 |               489818.00 |              31214 |                            1559.00 |                31286 |                              7015.00 |
| mysql-1-1-4-1-3  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.65 |               489629.00 |              31325 |                            1660.00 |                31175 |                              7175.00 |
| mysql-1-1-4-1-4  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.61 |               489765.00 |              31280 |                            1690.00 |                31220 |                              7211.00 |
| mysql-1-1-4-1-5  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.66 |               489583.00 |              31231 |                            1618.00 |                31269 |                              7039.00 |
| mysql-1-1-4-1-6  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.57 |               489912.00 |              31302 |                            1652.00 |                31198 |                              7099.00 |
| mysql-1-1-4-1-7  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.59 |               489845.00 |              31379 |                            1615.00 |                31121 |                              7219.00 |
| mysql-1-1-4-1-8  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.62 |               489749.00 |              31223 |                            1644.00 |                31277 |                              7031.00 |
| mysql-1-1-4-1-9  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.65 |               489626.00 |              31409 |                            1543.00 |                31091 |                              7095.00 |
| mysql-1-1-4-1-10 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.60 |               489831.00 |              31268 |                            1746.00 |                31232 |                              7075.00 |
| mysql-1-1-4-1-11 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.64 |               489647.00 |              31128 |                            1635.00 |                31372 |                              7295.00 |
| mysql-1-1-4-1-12 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.67 |               489526.00 |              31195 |                            1571.00 |                31305 |                              7159.00 |
| mysql-1-1-4-1-13 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.64 |               489662.00 |              31234 |                            1603.00 |                31266 |                              7223.00 |
| mysql-1-1-4-1-14 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.66 |               489597.00 |              31222 |                            1673.00 |                31278 |                              7063.00 |
| mysql-1-1-4-1-15 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.59 |               489867.00 |              31192 |                            1594.00 |                31308 |                              7187.00 |
| mysql-1-1-4-1-16 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.65 |               489627.00 |              31267 |                            1594.00 |                31233 |                              7099.00 |
| mysql-1-2-1-1-1  | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1020.20 |               980196.00 |             500091 |                            2097.00 |               499909 |                              6575.00 |
| mysql-1-2-2-1-1  | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1016.77 |               491753.00 |             250009 |                            1485.00 |               249991 |                              7171.00 |
| mysql-1-2-2-1-2  | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1017.32 |               491489.00 |             250063 |                            1464.00 |               249937 |                              7131.00 |
| mysql-1-2-3-1-1  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.82 |               977971.00 |              62627 |                            1508.00 |                62373 |                              7119.00 |
| mysql-1-2-3-1-2  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.83 |               977888.00 |              62395 |                            1448.00 |                62605 |                              7019.00 |
| mysql-1-2-3-1-3  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.83 |               977883.00 |              62586 |                            1420.00 |                62414 |                              7015.00 |
| mysql-1-2-3-1-4  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.79 |               978147.00 |              62547 |                            1442.00 |                62453 |                              7199.00 |
| mysql-1-2-3-1-5  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.82 |               977926.00 |              62435 |                            1450.00 |                62565 |                              6807.00 |
| mysql-1-2-3-1-6  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.81 |               978037.00 |              62455 |                            1457.00 |                62545 |                              7139.00 |
| mysql-1-2-3-1-7  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.85 |               977728.00 |              62492 |                            1479.00 |                62508 |                              7175.00 |
| mysql-1-2-3-1-8  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.83 |               977829.00 |              62885 |                            1437.00 |                62115 |                              7139.00 |
| mysql-1-2-4-1-1  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.65 |               489610.00 |              31103 |                            1633.00 |                31397 |                              6399.00 |
| mysql-1-2-4-1-2  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.66 |               489591.00 |              31280 |                            1647.00 |                31220 |                              6431.00 |
| mysql-1-2-4-1-3  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.57 |               489944.00 |              31131 |                            1575.00 |                31369 |                              6363.00 |
| mysql-1-2-4-1-4  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.67 |               489541.00 |              31237 |                            1617.00 |                31263 |                              6471.00 |
| mysql-1-2-4-1-5  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.59 |               489833.00 |              31095 |                            1665.00 |                31405 |                              6479.00 |
| mysql-1-2-4-1-6  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.64 |               489677.00 |              31122 |                            1637.00 |                31378 |                              6431.00 |
| mysql-1-2-4-1-7  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.57 |               489927.00 |              31133 |                            1613.00 |                31367 |                              6387.00 |
| mysql-1-2-4-1-8  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.69 |               489461.00 |              31398 |                            1546.00 |                31102 |                              6323.00 |
| mysql-1-2-4-1-9  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.66 |               489578.00 |              31109 |                            1564.00 |                31391 |                              6383.00 |
| mysql-1-2-4-1-10 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.60 |               489820.00 |              31196 |                            1570.00 |                31304 |                              6459.00 |
| mysql-1-2-4-1-11 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.64 |               489661.00 |              30951 |                            1647.00 |                31549 |                              6387.00 |
| mysql-1-2-4-1-12 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.63 |               489696.00 |              31275 |                            1579.00 |                31225 |                              6463.00 |
| mysql-1-2-4-1-13 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.64 |               489641.00 |              31251 |                            1676.00 |                31249 |                              6463.00 |
| mysql-1-2-4-1-14 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.57 |               489936.00 |              31315 |                            1609.00 |                31185 |                              6527.00 |
| mysql-1-2-4-1-15 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.61 |               489790.00 |              31282 |                            1632.00 |                31218 |                              6411.00 |
| mysql-1-2-4-1-16 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.60 |               489807.00 |              31165 |                            1648.00 |                31335 |                              6439.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1020.55 |               979865.00 |             498349 |                            2069.00 |               501651 |                              7271.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2039.60 |               490420.00 |             500228 |                            1371.00 |               499772 |                              6971.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1022.69 |               978057.00 |             499290 |                            1607.00 |               500710 |                              7111.00 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2042.04 |               489912.00 |             499981 |                            1746.00 |               500019 |                              7295.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1020.20 |               980196.00 |             500091 |                            2097.00 |               499909 |                              6575.00 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2034.09 |               491753.00 |             500072 |                            1485.00 |               499928 |                              7171.00 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1022.57 |               978147.00 |             500422 |                            1508.00 |               499578 |                              7199.00 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2041.99 |               489944.00 |             499043 |                            1676.00 |               500957 |                              6527.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: SUT pods not replaced
* TEST passed: Host information complete
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Execution Phase: every pod ran its configured operations
* TEST passed: Results of all benchmarker pods
* TEST passed: Benchmarker pods without errors

Test successful!
