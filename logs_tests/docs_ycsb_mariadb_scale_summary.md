## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 6700s 
* Code: 1795683054
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mariadb', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mariadb-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:622529
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:768498
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-1-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:772513
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-1-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:774234
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:635284
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-2-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636100
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-2-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636103
  * datadisk:1774
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
    * code:1795683054
* mariadb-1-2-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:636304
  * datadisk:1774
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
    * code:1795683054

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1795683054-6556cdb4b7-9gslz: 0
* bexhoma-sut-mariadb-1-1795683054-84d6f98fb-swhf2: 0

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

| connection         | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1-1-1  | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.39 |               977140.00 |             500398 |                            1252.00 |               499602 |                              4267.00 |
| mariadb-1-1-2-1-1  | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1022.59 |               488955.00 |             249919 |                            1089.00 |               250081 |                              4171.00 |
| mariadb-1-1-2-1-2  | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1022.63 |               488935.00 |             250493 |                            1092.00 |               249507 |                              4099.00 |
| mariadb-1-1-3-1-1  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.95 |               976924.00 |              62704 |                            1151.00 |                62296 |                              3887.00 |
| mariadb-1-1-3-1-2  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.96 |               976903.00 |              62635 |                            1165.00 |                62365 |                              3781.00 |
| mariadb-1-1-3-1-3  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.95 |               976918.00 |              62579 |                            1157.00 |                62421 |                              3737.00 |
| mariadb-1-1-3-1-4  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.96 |               976887.00 |              62644 |                            1170.00 |                62356 |                              3843.00 |
| mariadb-1-1-3-1-5  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.96 |               976894.00 |              62316 |                            1116.00 |                62684 |                              3811.00 |
| mariadb-1-1-3-1-6  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.96 |               976905.00 |              62818 |                            1181.00 |                62182 |                              3895.00 |
| mariadb-1-1-3-1-7  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.95 |               976912.00 |              62410 |                            1152.00 |                62590 |                              3859.00 |
| mariadb-1-1-3-1-8  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.95 |               976928.00 |              62159 |                            1154.00 |                62841 |                              3861.00 |
| mariadb-1-1-4-1-1  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.90 |               488673.00 |              31345 |                            1205.00 |                31155 |                              4243.00 |
| mariadb-1-1-4-1-2  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.90 |               488667.00 |              31230 |                            1163.00 |                31270 |                              4315.00 |
| mariadb-1-1-4-1-3  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.90 |               488653.00 |              31107 |                            1268.00 |                31393 |                              4243.00 |
| mariadb-1-1-4-1-4  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.90 |               488647.00 |              31243 |                            1220.00 |                31257 |                              4443.00 |
| mariadb-1-1-4-1-5  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.90 |               488674.00 |              31201 |                            1233.00 |                31299 |                              4187.00 |
| mariadb-1-1-4-1-6  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.91 |               488627.00 |              31411 |                            1224.00 |                31089 |                              4351.00 |
| mariadb-1-1-4-1-7  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.90 |               488647.00 |              31346 |                            1233.00 |                31154 |                              4355.00 |
| mariadb-1-1-4-1-8  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.90 |               488669.00 |              31222 |                            1228.00 |                31278 |                              4131.00 |
| mariadb-1-1-4-1-9  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.91 |               488640.00 |              31325 |                            1203.00 |                31175 |                              4187.00 |
| mariadb-1-1-4-1-10 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.90 |               488655.00 |              31314 |                            1201.00 |                31186 |                              4311.00 |
| mariadb-1-1-4-1-11 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.90 |               488657.00 |              31285 |                            1227.00 |                31215 |                              4163.00 |
| mariadb-1-1-4-1-12 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.90 |               488657.00 |              31203 |                            1227.00 |                31297 |                              4399.00 |
| mariadb-1-1-4-1-13 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.90 |               488644.00 |              31074 |                            1173.00 |                31426 |                              4175.00 |
| mariadb-1-1-4-1-14 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.91 |               488636.00 |              31398 |                            1212.00 |                31102 |                              4383.00 |
| mariadb-1-1-4-1-15 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.90 |               488662.00 |              31270 |                            1235.00 |                31230 |                              4299.00 |
| mariadb-1-1-4-1-16 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.90 |               488667.00 |              31186 |                            1253.00 |                31314 |                              4279.00 |
| mariadb-1-2-1-1-1  | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.36 |               977177.00 |             499560 |                            1221.00 |               500440 |                              3723.00 |
| mariadb-1-2-2-1-1  | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1022.99 |               488761.00 |             250098 |                            1151.00 |               249902 |                              3991.00 |
| mariadb-1-2-2-1-2  | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1023.02 |               488750.00 |             249469 |                            1153.00 |               250531 |                              4001.00 |
| mariadb-1-2-3-1-1  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.96 |               976838.00 |              62415 |                            1221.00 |                62585 |                              3647.00 |
| mariadb-1-2-3-1-2  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.96 |               976852.00 |              62482 |                            1211.00 |                62518 |                              3845.00 |
| mariadb-1-2-3-1-3  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.96 |               976853.00 |              62496 |                            1213.00 |                62504 |                              3789.00 |
| mariadb-1-2-3-1-4  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.96 |               976859.00 |              62539 |                            1222.00 |                62461 |                              3665.00 |
| mariadb-1-2-3-1-5  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.97 |               976829.00 |              62476 |                            1208.00 |                62524 |                              3553.00 |
| mariadb-1-2-3-1-6  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.96 |               976843.00 |              62510 |                            1219.00 |                62490 |                              3625.00 |
| mariadb-1-2-3-1-7  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.96 |               976847.00 |              62495 |                            1229.00 |                62505 |                              3917.00 |
| mariadb-1-2-3-1-8  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.96 |               976839.00 |              62602 |                            1215.00 |                62398 |                              3765.00 |
| mariadb-1-2-4-1-1  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.91 |               488621.00 |              31157 |                            1224.00 |                31343 |                              3663.00 |
| mariadb-1-2-4-1-2  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.90 |               488650.00 |              31157 |                            1227.00 |                31343 |                              3575.00 |
| mariadb-1-2-4-1-3  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.90 |               488648.00 |              31348 |                            1170.00 |                31152 |                              3659.00 |
| mariadb-1-2-4-1-4  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.90 |               488663.00 |              31104 |                            1209.00 |                31396 |                              3775.00 |
| mariadb-1-2-4-1-5  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.90 |               488659.00 |              31247 |                            1219.00 |                31253 |                              3645.00 |
| mariadb-1-2-4-1-6  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.91 |               488641.00 |              31356 |                            1214.00 |                31144 |                              3633.00 |
| mariadb-1-2-4-1-7  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.89 |               488684.00 |              31357 |                            1219.00 |                31143 |                              3739.00 |
| mariadb-1-2-4-1-8  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.90 |               488650.00 |              31298 |                            1198.00 |                31202 |                              3741.00 |
| mariadb-1-2-4-1-9  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.90 |               488664.00 |              31117 |                            1212.00 |                31383 |                              3603.00 |
| mariadb-1-2-4-1-10 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.90 |               488661.00 |              31289 |                            1231.00 |                31211 |                              3625.00 |
| mariadb-1-2-4-1-11 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.90 |               488656.00 |              31450 |                            1184.00 |                31050 |                              3655.00 |
| mariadb-1-2-4-1-12 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.90 |               488658.00 |              31205 |                            1245.00 |                31295 |                              3697.00 |
| mariadb-1-2-4-1-13 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.90 |               488644.00 |              31119 |                            1225.00 |                31381 |                              3667.00 |
| mariadb-1-2-4-1-14 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.89 |               488694.00 |              31271 |                            1207.00 |                31229 |                              3681.00 |
| mariadb-1-2-4-1-15 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.89 |               488685.00 |              31305 |                            1211.00 |                31195 |                              3597.00 |
| mariadb-1-2-4-1-16 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.90 |               488672.00 |              31197 |                            1198.00 |                31303 |                              3595.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.39 |               977140.00 |             500398 |                            1252.00 |               499602 |                              4267.00 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2045.22 |               488955.00 |             500412 |                            1092.00 |               499588 |                              4171.00 |
| mariadb-1-1-3 | mariadb-1-1-3 |                1 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1023.64 |               976928.00 |             500265 |                            1181.00 |               499735 |                              3895.00 |
| mariadb-1-1-4 | mariadb-1-1-4 |                1 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2046.43 |               488674.00 |             500160 |                            1268.00 |               499840 |                              4443.00 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.36 |               977177.00 |             499560 |                            1221.00 |               500440 |                              3723.00 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2046.01 |               488761.00 |             499567 |                            1153.00 |               500433 |                              4001.00 |
| mariadb-1-2-3 | mariadb-1-2-3 |                2 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1023.70 |               976859.00 |             500015 |                            1229.00 |               499985 |                              3917.00 |
| mariadb-1-2-4 | mariadb-1-2-4 |                2 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2046.42 |               488694.00 |             499977 |                            1245.00 |               500023 |                              3775.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MariaDB-1)
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
