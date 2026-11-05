## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 6706s 
* Code: 1793648842
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
  * Experiment is limited to DBMS ['MariaDB'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808746
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
    * code:1793648842
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808759
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
    * code:1793648842
* mariadb-1-1-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808752
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
    * code:1793648842
* mariadb-1-1-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808758
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
    * code:1793648842
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808771
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
    * code:1793648842
* mariadb-1-2-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808777
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
    * code:1793648842
* mariadb-1-2-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808780
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
    * code:1793648842
* mariadb-1-2-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:808777
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
    * code:1793648842

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793648842-7f599f687b-hwmz2: 0
* bexhoma-sut-mariadb-1-1793648842-dffdd7c7c-64bfc: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: ycsb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: ycsb (8 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: ycsb (16 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: ycsb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: ycsb (8 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: ycsb (16 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: ycsb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: ycsb (8 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: ycsb (16 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: ycsb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: ycsb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: ycsb (8 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: ycsb (16 pods)

### Benchmarking

#### Per Connection

| DBMS               | phase         | job             | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:--------------|:----------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1  | mariadb-1-1-1 | mariadb-1-1-1-1 | MariaDB-1       |                1 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.41 |               977130.00 |             499755 |                            1177.00 |               500245 |                              3623.00 |
| mariadb-1-1-2-1-1  | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                         1023.04 |               488741.00 |             249147 |                            1219.00 |               250853 |                              4179.00 |
| mariadb-1-1-2-1-2  | mariadb-1-1-2 | mariadb-1-1-2-1 | MariaDB-1       |                1 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                         1022.97 |               488775.00 |             249843 |                            1216.00 |               250157 |                              4139.00 |
| mariadb-1-1-3-1-1  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.97 |               976810.00 |              62611 |                            1182.00 |                62389 |                              3741.00 |
| mariadb-1-1-3-1-2  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.97 |               976825.00 |              62424 |                            1200.00 |                62576 |                              3879.00 |
| mariadb-1-1-3-1-3  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976850.00 |              62430 |                            1247.00 |                62570 |                              3879.00 |
| mariadb-1-1-3-1-4  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976833.00 |              62687 |                            1205.00 |                62313 |                              3677.00 |
| mariadb-1-1-3-1-5  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.97 |               976822.00 |              62336 |                            1197.00 |                62664 |                              3929.00 |
| mariadb-1-1-3-1-6  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.97 |               976826.00 |              62584 |                            1189.00 |                62416 |                              3819.00 |
| mariadb-1-1-3-1-7  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.97 |               976827.00 |              62635 |                            1197.00 |                62365 |                              3827.00 |
| mariadb-1-1-3-1-8  | mariadb-1-1-3 | mariadb-1-1-3-1 | MariaDB-1       |                1 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976842.00 |              62714 |                            1217.00 |                62286 |                              3921.00 |
| mariadb-1-1-4-1-1  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                          127.92 |               488599.00 |              31331 |                            1240.00 |                31169 |                              4063.00 |
| mariadb-1-1-4-1-2  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                          127.92 |               488604.00 |              30974 |                            1184.00 |                31526 |                              3739.00 |
| mariadb-1-1-4-1-3  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                          127.92 |               488571.00 |              31190 |                            1225.00 |                31310 |                              3969.00 |
| mariadb-1-1-4-1-4  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                          127.92 |               488577.00 |              30981 |                            1224.00 |                31519 |                              3797.00 |
| mariadb-1-1-4-1-5  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                          127.92 |               488598.00 |              31153 |                            1185.00 |                31347 |                              3741.00 |
| mariadb-1-1-4-1-6  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                          127.92 |               488605.00 |              31158 |                            1263.00 |                31342 |                              3905.00 |
| mariadb-1-1-4-1-7  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                          127.92 |               488581.00 |              31100 |                            1187.00 |                31400 |                              3945.00 |
| mariadb-1-1-4-1-8  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                          127.92 |               488603.00 |              31141 |                            1203.00 |                31359 |                              3879.00 |
| mariadb-1-1-4-1-9  | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                          127.91 |               488608.00 |              31406 |                            1183.00 |                31094 |                              3833.00 |
| mariadb-1-1-4-1-10 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                          127.92 |               488584.00 |              31170 |                            1175.00 |                31330 |                              3893.00 |
| mariadb-1-1-4-1-11 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                          127.92 |               488582.00 |              31253 |                            1196.00 |                31247 |                              3743.00 |
| mariadb-1-1-4-1-12 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                          127.91 |               488615.00 |              31132 |                            1231.00 |                31368 |                              3799.00 |
| mariadb-1-1-4-1-13 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                          127.92 |               488592.00 |              31202 |                            1210.00 |                31298 |                              3905.00 |
| mariadb-1-1-4-1-14 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                          127.93 |               488551.00 |              31144 |                            1219.00 |                31356 |                              3915.00 |
| mariadb-1-1-4-1-15 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                          127.92 |               488583.00 |              31316 |                            1193.00 |                31184 |                              3997.00 |
| mariadb-1-1-4-1-16 | mariadb-1-1-4 | mariadb-1-1-4-1 | MariaDB-1       |                1 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                          127.92 |               488589.00 |              31204 |                            1232.00 |                31296 |                              4009.00 |
| mariadb-1-2-1-1-1  | mariadb-1-2-1 | mariadb-1-2-1-1 | MariaDB-1       |                2 |        1 |               1 |       1 |        64 |     1024 |           1 |            0 |                         1023.30 |               977231.00 |             500238 |                            1202.00 |               499762 |                              3963.00 |
| mariadb-1-2-2-1-1  | mariadb-1-2-2 | mariadb-1-2-2-1 | MariaDB-1       |                2 |        2 |               1 |       1 |        64 |     1024 |           2 |            0 |                         1022.92 |               488797.00 |             250286 |                            1212.00 |               249714 |                              4001.00 |
| mariadb-1-2-2-1-2  | mariadb-1-2-2 | mariadb-1-2-2-1 | MariaDB-1       |                2 |        2 |               1 |       2 |        64 |     1024 |           2 |            0 |                         1023.01 |               488754.00 |             250199 |                            1199.00 |               249801 |                              3965.00 |
| mariadb-1-2-3-1-1  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976881.00 |              62484 |                            1240.00 |                62516 |                              3875.00 |
| mariadb-1-2-3-1-2  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       2 |         8 |      128 |           8 |            0 |                          127.95 |               976919.00 |              62796 |                            1231.00 |                62204 |                              3665.00 |
| mariadb-1-2-3-1-3  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       3 |         8 |      128 |           8 |            0 |                          127.95 |               976910.00 |              62474 |                            1231.00 |                62526 |                              3647.00 |
| mariadb-1-2-3-1-4  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       4 |         8 |      128 |           8 |            0 |                          127.95 |               976910.00 |              62464 |                            1310.00 |                62536 |                              3625.00 |
| mariadb-1-2-3-1-5  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       5 |         8 |      128 |           8 |            0 |                          127.95 |               976913.00 |              62425 |                            1306.00 |                62575 |                              3681.00 |
| mariadb-1-2-3-1-6  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976904.00 |              62445 |                            1221.00 |                62555 |                              3417.00 |
| mariadb-1-2-3-1-7  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       7 |         8 |      128 |           8 |            0 |                          127.95 |               976907.00 |              62759 |                            1246.00 |                62241 |                              3811.00 |
| mariadb-1-2-3-1-8  | mariadb-1-2-3 | mariadb-1-2-3-1 | MariaDB-1       |                2 |        3 |               1 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976894.00 |              62310 |                            1221.00 |                62690 |                              3739.00 |
| mariadb-1-2-4-1-1  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       1 |         8 |      128 |          16 |            0 |                          127.90 |               488669.00 |              30967 |                            1240.00 |                31533 |                              4089.00 |
| mariadb-1-2-4-1-2  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       2 |         8 |      128 |          16 |            0 |                          127.90 |               488678.00 |              31309 |                            1235.00 |                31191 |                              3947.00 |
| mariadb-1-2-4-1-3  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       3 |         8 |      128 |          16 |            0 |                          127.91 |               488632.00 |              31105 |                            1241.00 |                31395 |                              4119.00 |
| mariadb-1-2-4-1-4  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       4 |         8 |      128 |          16 |            0 |                          127.90 |               488645.00 |              31340 |                            1233.00 |                31160 |                              4259.00 |
| mariadb-1-2-4-1-5  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       5 |         8 |      128 |          16 |            0 |                          127.90 |               488647.00 |              31463 |                            1255.00 |                31037 |                              4191.00 |
| mariadb-1-2-4-1-6  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       6 |         8 |      128 |          16 |            0 |                          127.90 |               488648.00 |              31280 |                            1229.00 |                31220 |                              4215.00 |
| mariadb-1-2-4-1-7  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       7 |         8 |      128 |          16 |            0 |                          127.91 |               488630.00 |              31105 |                            1245.00 |                31395 |                              4223.00 |
| mariadb-1-2-4-1-8  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       8 |         8 |      128 |          16 |            0 |                          127.90 |               488662.00 |              31054 |                            1192.00 |                31446 |                              4073.00 |
| mariadb-1-2-4-1-9  | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |       9 |         8 |      128 |          16 |            0 |                          127.91 |               488643.00 |              31329 |                            1224.00 |                31171 |                              4167.00 |
| mariadb-1-2-4-1-10 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      10 |         8 |      128 |          16 |            0 |                          127.90 |               488672.00 |              31103 |                            1258.00 |                31397 |                              4107.00 |
| mariadb-1-2-4-1-11 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      11 |         8 |      128 |          16 |            0 |                          127.90 |               488649.00 |              31438 |                            1248.00 |                31062 |                              4199.00 |
| mariadb-1-2-4-1-12 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      12 |         8 |      128 |          16 |            0 |                          127.90 |               488648.00 |              31218 |                            1238.00 |                31282 |                              4065.00 |
| mariadb-1-2-4-1-13 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      13 |         8 |      128 |          16 |            0 |                          127.90 |               488653.00 |              31438 |                            1213.00 |                31062 |                              4203.00 |
| mariadb-1-2-4-1-14 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      14 |         8 |      128 |          16 |            0 |                          127.90 |               488649.00 |              31324 |                            1241.00 |                31176 |                              4187.00 |
| mariadb-1-2-4-1-15 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      15 |         8 |      128 |          16 |            0 |                          127.91 |               488641.00 |              31268 |                            1256.00 |                31232 |                              4187.00 |
| mariadb-1-2-4-1-16 | mariadb-1-2-4 | mariadb-1-2-4-1 | MariaDB-1       |                2 |        4 |               1 |      16 |         8 |      128 |          16 |            0 |                          127.90 |               488662.00 |              31582 |                            1234.00 |                30918 |                              4295.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        64 |     1024 |               1 |           1 |            0 |                         1023.41 |               977130.00 |             499755 |                            1177.00 |               500245 |                              3623.00 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |       128 |     2048 |               1 |           2 |            0 |                         2046.00 |               488775.00 |             498990 |                            1219.00 |               501010 |                              4179.00 |
| mariadb-1-1-3 | mariadb-1-1-3 |                1 |        64 |     1024 |               1 |           8 |            0 |                         1023.72 |               976850.00 |             500421 |                            1247.00 |               499579 |                              3929.00 |
| mariadb-1-1-4 | mariadb-1-1-4 |                1 |       128 |     2048 |               1 |          16 |            0 |                         2046.71 |               488615.00 |             498855 |                            1263.00 |               501145 |                              4063.00 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        64 |     1024 |               1 |           1 |            0 |                         1023.30 |               977231.00 |             500238 |                            1202.00 |               499762 |                              3963.00 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |       128 |     2048 |               1 |           2 |            0 |                         2045.93 |               488797.00 |             500485 |                            1212.00 |               499515 |                              4001.00 |
| mariadb-1-2-3 | mariadb-1-2-3 |                2 |        64 |     1024 |               1 |           8 |            0 |                         1023.64 |               976919.00 |             500157 |                            1310.00 |               499843 |                              3875.00 |
| mariadb-1-2-4 | mariadb-1-2-4 |                2 |       128 |     2048 |               1 |          16 |            0 |                         2046.45 |               488678.00 |             500323 |                            1258.00 |               499677 |                              4295.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MariaDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
