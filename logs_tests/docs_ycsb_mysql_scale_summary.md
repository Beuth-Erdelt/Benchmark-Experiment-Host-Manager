## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 6878s 
* Code: 1794708786
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
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045210
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
    * code:1794708786
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045209
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
    * code:1794708786
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045196
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
    * code:1794708786
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046009
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
    * code:1794708786
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046824
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
    * code:1794708786
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046827
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
    * code:1794708786
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046829
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
    * code:1794708786
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046833
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
    * code:1794708786

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: DDL values of the volume: row_format=DYNAMIC, collation=utf8mb4_0900_ai_ci
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794708786-6678755dd4-llmk5: 0
* bexhoma-sut-mysql-1-1794708786-68b7954975-kt9pj: 0

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
| mysql-1-1-1-1-1  | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1021.90 |               978567.00 |             500452 |                            1744.00 |               499548 |                              7235.00 |
| mysql-1-1-2-1-1  | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1017.22 |               491535.00 |             250249 |                            1506.00 |               249751 |                              6831.00 |
| mysql-1-1-2-1-2  | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1015.72 |               492262.00 |             250137 |                            1495.00 |               249863 |                              6919.00 |
| mysql-1-1-3-1-1  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.87 |               977585.00 |              62872 |                            1780.00 |                62128 |                              7291.00 |
| mysql-1-1-3-1-2  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.84 |               977763.00 |              62568 |                            1661.00 |                62432 |                              7387.00 |
| mysql-1-1-3-1-3  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.82 |               977968.00 |              62540 |                            1693.00 |                62460 |                              7415.00 |
| mysql-1-1-3-1-4  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.87 |               977554.00 |              62548 |                            1690.00 |                62452 |                              7283.00 |
| mysql-1-1-3-1-5  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.80 |               978084.00 |              62577 |                            1776.00 |                62423 |                              7183.00 |
| mysql-1-1-3-1-6  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.83 |               977824.00 |              62307 |                            1843.00 |                62693 |                              7459.00 |
| mysql-1-1-3-1-7  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.84 |               977804.00 |              62505 |                            1755.00 |                62495 |                              7503.00 |
| mysql-1-1-3-1-8  | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.87 |               977536.00 |              62754 |                            1757.00 |                62246 |                              7479.00 |
| mysql-1-1-4-1-1  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.74 |               489282.00 |              31199 |                            1583.00 |                31301 |                              6783.00 |
| mysql-1-1-4-1-2  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.72 |               489358.00 |              31389 |                            1606.00 |                31111 |                              6763.00 |
| mysql-1-1-4-1-3  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.75 |               489233.00 |              31195 |                            1595.00 |                31305 |                              6823.00 |
| mysql-1-1-4-1-4  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.75 |               489254.00 |              31403 |                            1627.00 |                31097 |                              6707.00 |
| mysql-1-1-4-1-5  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.74 |               489294.00 |              30959 |                            1662.00 |                31541 |                              6811.00 |
| mysql-1-1-4-1-6  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.75 |               489230.00 |              31418 |                            1657.00 |                31082 |                              6763.00 |
| mysql-1-1-4-1-7  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.74 |               489290.00 |              31215 |                            1584.00 |                31285 |                              6735.00 |
| mysql-1-1-4-1-8  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.74 |               489293.00 |              31055 |                            1600.00 |                31445 |                              6627.00 |
| mysql-1-1-4-1-9  | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.74 |               489286.00 |              31303 |                            1660.00 |                31197 |                              6787.00 |
| mysql-1-1-4-1-10 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.75 |               489242.00 |              31545 |                            1605.00 |                30955 |                              6699.00 |
| mysql-1-1-4-1-11 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.75 |               489226.00 |              31167 |                            1557.00 |                31333 |                              6675.00 |
| mysql-1-1-4-1-12 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.71 |               489388.00 |              31235 |                            1676.00 |                31265 |                              6699.00 |
| mysql-1-1-4-1-13 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.74 |               489273.00 |              31144 |                            1695.00 |                31356 |                              6767.00 |
| mysql-1-1-4-1-14 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.75 |               489239.00 |              31358 |                            1610.00 |                31142 |                              6739.00 |
| mysql-1-1-4-1-15 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.75 |               489222.00 |              31339 |                            1576.00 |                31161 |                              6571.00 |
| mysql-1-1-4-1-16 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.75 |               489235.00 |              31014 |                            1620.00 |                31486 |                              6863.00 |
| mysql-1-2-1-1-1  | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1021.67 |               978788.00 |             499502 |                            2113.00 |               500498 |                              7243.00 |
| mysql-1-2-2-1-1  | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1016.97 |               491655.00 |             250219 |                            1498.00 |               249781 |                              6843.00 |
| mysql-1-2-2-1-2  | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1018.09 |               491114.00 |             249679 |                            1455.00 |               250321 |                              6851.00 |
| mysql-1-2-3-1-1  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.81 |               978039.00 |              62418 |                            1642.00 |                62582 |                              6691.00 |
| mysql-1-2-3-1-2  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.84 |               977761.00 |              62028 |                            1572.00 |                62972 |                              6515.00 |
| mysql-1-2-3-1-3  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.83 |               977826.00 |              62227 |                            1727.00 |                62773 |                              6703.00 |
| mysql-1-2-3-1-4  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.84 |               977751.00 |              62515 |                            1671.00 |                62485 |                              6455.00 |
| mysql-1-2-3-1-5  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.83 |               977844.00 |              62271 |                            1613.00 |                62729 |                              6451.00 |
| mysql-1-2-3-1-6  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.80 |               978056.00 |              62572 |                            1658.00 |                62428 |                              6567.00 |
| mysql-1-2-3-1-7  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.82 |               977915.00 |              62481 |                            1596.00 |                62519 |                              6839.00 |
| mysql-1-2-3-1-8  | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.84 |               977770.00 |              62439 |                            1589.00 |                62561 |                              6603.00 |
| mysql-1-2-4-1-1  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.75 |               489224.00 |              31185 |                            1703.00 |                31315 |                              7067.00 |
| mysql-1-2-4-1-2  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.73 |               489299.00 |              31232 |                            1615.00 |                31268 |                              7103.00 |
| mysql-1-2-4-1-3  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.76 |               489195.00 |              31330 |                            1612.00 |                31170 |                              6819.00 |
| mysql-1-2-4-1-4  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.73 |               489301.00 |              31271 |                            1622.00 |                31229 |                              7075.00 |
| mysql-1-2-4-1-5  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.74 |               489294.00 |              31222 |                            1570.00 |                31278 |                              7011.00 |
| mysql-1-2-4-1-6  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.76 |               489188.00 |              31228 |                            1627.00 |                31272 |                              6891.00 |
| mysql-1-2-4-1-7  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.74 |               489257.00 |              31321 |                            1646.00 |                31179 |                              6907.00 |
| mysql-1-2-4-1-8  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.74 |               489284.00 |              31432 |                            1597.00 |                31068 |                              6959.00 |
| mysql-1-2-4-1-9  | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.74 |               489274.00 |              31396 |                            1579.00 |                31104 |                              6987.00 |
| mysql-1-2-4-1-10 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.75 |               489230.00 |              31318 |                            1642.00 |                31182 |                              7003.00 |
| mysql-1-2-4-1-11 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.72 |               489351.00 |              31151 |                            1675.00 |                31349 |                              6979.00 |
| mysql-1-2-4-1-12 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.77 |               489173.00 |              31170 |                            1646.00 |                31330 |                              6927.00 |
| mysql-1-2-4-1-13 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.72 |               489357.00 |              31221 |                            1682.00 |                31279 |                              7083.00 |
| mysql-1-2-4-1-14 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.75 |               489231.00 |              31317 |                            1624.00 |                31183 |                              6963.00 |
| mysql-1-2-4-1-15 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.73 |               489332.00 |              31306 |                            1592.00 |                31194 |                              7011.00 |
| mysql-1-2-4-1-16 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.74 |               489290.00 |              31212 |                            1583.00 |                31288 |                              7031.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1021.90 |               978567.00 |             500452 |                            1744.00 |               499548 |                              7235.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2032.94 |               492262.00 |             500386 |                            1506.00 |               499614 |                              6919.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1022.74 |               978084.00 |             500671 |                            1843.00 |               499329 |                              7503.00 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2043.85 |               489388.00 |             499938 |                            1695.00 |               500062 |                              6863.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1021.67 |               978788.00 |             499502 |                            2113.00 |               500498 |                              7243.00 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2035.07 |               491655.00 |             499898 |                            1498.00 |               500102 |                              6851.00 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1022.63 |               978056.00 |             498951 |                            1727.00 |               501049 |                              6839.00 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2043.87 |               489357.00 |             500312 |                            1703.00 |               499688 |                              7103.00 |

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
