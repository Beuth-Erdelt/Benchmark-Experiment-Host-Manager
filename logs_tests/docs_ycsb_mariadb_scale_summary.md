## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 6750s 
* Code: 1794785817
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
  * Experiment uses bexhoma version 0.11.18.
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
  * disk:1053184
  * datadisk:1766
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
    * code:1794785817
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053191
  * datadisk:1766
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
    * code:1794785817
* mariadb-1-1-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053184
  * datadisk:1766
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
    * code:1794785817
* mariadb-1-1-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053186
  * datadisk:1766
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
    * code:1794785817
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053189
  * datadisk:1766
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
    * code:1794785817
* mariadb-1-2-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053185
  * datadisk:1766
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
    * code:1794785817
* mariadb-1-2-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053189
  * datadisk:1766
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
    * code:1794785817
* mariadb-1-2-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053194
  * datadisk:1766
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
    * code:1794785817

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: DDL values of the volume: row_format=default, collation=default
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794785817-6cfd87994d-9wshj: 0
* bexhoma-sut-mariadb-1-1794785817-78dd4db5ff-4ssth: 0

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
| mariadb-1-1-1-1-1  | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.51 |               977034.00 |             499848 |                            1211.00 |               500152 |                              4031.00 |
| mariadb-1-1-2-1-1  | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1022.97 |               488775.00 |             250589 |                            1221.00 |               249411 |                              4231.00 |
| mariadb-1-1-2-1-2  | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1022.94 |               488788.00 |             248952 |                            1210.00 |               251048 |                              4279.00 |
| mariadb-1-1-3-1-1  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.96 |               976899.00 |              62644 |                            1246.00 |                62356 |                              4077.00 |
| mariadb-1-1-3-1-2  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.96 |               976904.00 |              62503 |                            1246.00 |                62497 |                              4259.00 |
| mariadb-1-1-3-1-3  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.96 |               976895.00 |              62563 |                            1217.00 |                62437 |                              4207.00 |
| mariadb-1-1-3-1-4  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.95 |               976915.00 |              62465 |                            1216.00 |                62535 |                              4049.00 |
| mariadb-1-1-3-1-5  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.96 |               976901.00 |              62403 |                            1242.00 |                62597 |                              4147.00 |
| mariadb-1-1-3-1-6  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.95 |               976906.00 |              62585 |                            1243.00 |                62415 |                              3865.00 |
| mariadb-1-1-3-1-7  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.95 |               976908.00 |              62426 |                            1232.00 |                62574 |                              4041.00 |
| mariadb-1-1-3-1-8  | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.96 |               976891.00 |              62221 |                            1243.00 |                62779 |                              4211.00 |
| mariadb-1-1-4-1-1  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.92 |               488603.00 |              31139 |                            1266.00 |                31361 |                              4099.00 |
| mariadb-1-1-4-1-2  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.92 |               488588.00 |              31144 |                            1295.00 |                31356 |                              4079.00 |
| mariadb-1-1-4-1-3  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.92 |               488589.00 |              31289 |                            1237.00 |                31211 |                              4093.00 |
| mariadb-1-1-4-1-4  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.91 |               488611.00 |              31280 |                            1251.00 |                31220 |                              4287.00 |
| mariadb-1-1-4-1-5  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.92 |               488598.00 |              31215 |                            1252.00 |                31285 |                              4139.00 |
| mariadb-1-1-4-1-6  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.92 |               488575.00 |              31355 |                            1242.00 |                31145 |                              4035.00 |
| mariadb-1-1-4-1-7  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.92 |               488585.00 |              31139 |                            1242.00 |                31361 |                              4091.00 |
| mariadb-1-1-4-1-8  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.92 |               488589.00 |              31236 |                            1222.00 |                31264 |                              4053.00 |
| mariadb-1-1-4-1-9  | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.92 |               488605.00 |              31310 |                            1225.00 |                31190 |                              4155.00 |
| mariadb-1-1-4-1-10 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.92 |               488604.00 |              31345 |                            1222.00 |                31155 |                              4191.00 |
| mariadb-1-1-4-1-11 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.92 |               488572.00 |              31401 |                            1223.00 |                31099 |                              4123.00 |
| mariadb-1-1-4-1-12 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.92 |               488590.00 |              31283 |                            1225.00 |                31217 |                              3947.00 |
| mariadb-1-1-4-1-13 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.92 |               488602.00 |              31225 |                            1225.00 |                31275 |                              4033.00 |
| mariadb-1-1-4-1-14 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.92 |               488593.00 |              31351 |                            1196.00 |                31149 |                              4027.00 |
| mariadb-1-1-4-1-15 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.92 |               488581.00 |              31239 |                            1234.00 |                31261 |                              4085.00 |
| mariadb-1-1-4-1-16 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.91 |               488608.00 |              31535 |                            1249.00 |                30965 |                              4103.00 |
| mariadb-1-2-1-1-1  | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |     1024 |        0 |                         1023.54 |               977001.00 |             500611 |                            1186.00 |               499389 |                              3643.00 |
| mariadb-1-2-2-1-1  | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       1 |        64 |     1024 |        0 |                         1022.96 |               488777.00 |             250246 |                            1200.00 |               249754 |                              4063.00 |
| mariadb-1-2-2-1-2  | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       2 |        64 |     1024 |        0 |                         1023.00 |               488758.00 |             249457 |                            1206.00 |               250543 |                              4111.00 |
| mariadb-1-2-3-1-1  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       1 |         8 |      128 |        0 |                          127.96 |               976894.00 |              62461 |                            1202.00 |                62539 |                              3383.00 |
| mariadb-1-2-3-1-2  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       2 |         8 |      128 |        0 |                          127.95 |               976910.00 |              62811 |                            1202.00 |                62189 |                              3509.00 |
| mariadb-1-2-3-1-3  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       3 |         8 |      128 |        0 |                          127.96 |               976867.00 |              62540 |                            1184.00 |                62460 |                              3387.00 |
| mariadb-1-2-3-1-4  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       4 |         8 |      128 |        0 |                          127.95 |               976923.00 |              62443 |                            1196.00 |                62557 |                              3549.00 |
| mariadb-1-2-3-1-5  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       5 |         8 |      128 |        0 |                          127.95 |               976911.00 |              62662 |                            1187.00 |                62338 |                              3459.00 |
| mariadb-1-2-3-1-6  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       6 |         8 |      128 |        0 |                          127.95 |               976909.00 |              62290 |                            1249.00 |                62710 |                              3463.00 |
| mariadb-1-2-3-1-7  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       7 |         8 |      128 |        0 |                          127.95 |               976933.00 |              62447 |                            1225.00 |                62553 |                              3501.00 |
| mariadb-1-2-3-1-8  | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       8 |         8 |      128 |        0 |                          127.96 |               976897.00 |              62697 |                            1185.00 |                62303 |                              3265.00 |
| mariadb-1-2-4-1-1  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       1 |         8 |      128 |        0 |                          127.91 |               488642.00 |              31290 |                            1272.00 |                31210 |                              4447.00 |
| mariadb-1-2-4-1-2  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       2 |         8 |      128 |        0 |                          127.90 |               488652.00 |              30965 |                            1210.00 |                31535 |                              4615.00 |
| mariadb-1-2-4-1-3  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       3 |         8 |      128 |        0 |                          127.90 |               488645.00 |              30998 |                            1215.00 |                31502 |                              4359.00 |
| mariadb-1-2-4-1-4  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       4 |         8 |      128 |        0 |                          127.91 |               488635.00 |              31181 |                            1240.00 |                31319 |                              4331.00 |
| mariadb-1-2-4-1-5  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       5 |         8 |      128 |        0 |                          127.90 |               488672.00 |              31148 |                            1250.00 |                31352 |                              4463.00 |
| mariadb-1-2-4-1-6  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       6 |         8 |      128 |        0 |                          127.91 |               488634.00 |              31196 |                            1235.00 |                31304 |                              4315.00 |
| mariadb-1-2-4-1-7  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       7 |         8 |      128 |        0 |                          127.90 |               488661.00 |              31233 |                            1385.00 |                31267 |                              4479.00 |
| mariadb-1-2-4-1-8  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       8 |         8 |      128 |        0 |                          127.90 |               488670.00 |              31221 |                            1223.00 |                31279 |                              4255.00 |
| mariadb-1-2-4-1-9  | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       9 |         8 |      128 |        0 |                          127.91 |               488641.00 |              31158 |                            1228.00 |                31342 |                              4347.00 |
| mariadb-1-2-4-1-10 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      10 |         8 |      128 |        0 |                          127.90 |               488676.00 |              31236 |                            1247.00 |                31264 |                              4311.00 |
| mariadb-1-2-4-1-11 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      11 |         8 |      128 |        0 |                          127.90 |               488663.00 |              31415 |                            1267.00 |                31085 |                              4431.00 |
| mariadb-1-2-4-1-12 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      12 |         8 |      128 |        0 |                          127.90 |               488657.00 |              31319 |                            1263.00 |                31181 |                              4511.00 |
| mariadb-1-2-4-1-13 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      13 |         8 |      128 |        0 |                          127.90 |               488678.00 |              31216 |                            1231.00 |                31284 |                              4439.00 |
| mariadb-1-2-4-1-14 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      14 |         8 |      128 |        0 |                          127.91 |               488637.00 |              31365 |                            1226.00 |                31135 |                              4307.00 |
| mariadb-1-2-4-1-15 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      15 |         8 |      128 |        0 |                          127.90 |               488669.00 |              31331 |                            1237.00 |                31169 |                              4471.00 |
| mariadb-1-2-4-1-16 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |      16 |         8 |      128 |        0 |                          127.91 |               488641.00 |              31262 |                            1244.00 |                31238 |                              4483.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.51 |               977034.00 |             499848 |                            1211.00 |               500152 |                              4031.00 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2045.90 |               488788.00 |             499541 |                            1221.00 |               500459 |                              4279.00 |
| mariadb-1-1-3 | mariadb-1-1-3 |                1 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1023.64 |               976915.00 |             499810 |                            1246.00 |               500190 |                              4259.00 |
| mariadb-1-1-4 | mariadb-1-1-4 |                1 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2046.69 |               488611.00 |             500486 |                            1295.00 |               499514 |                              4287.00 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 |        64 |     1024 |        0 |                         1023.54 |               977001.00 |             500611 |                            1186.00 |               499389 |                              3643.00 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 |       128 |     2048 |        0 |                         2045.96 |               488777.00 |             499703 |                            1206.00 |               500297 |                              4111.00 |
| mariadb-1-2-3 | mariadb-1-2-3 |                2 |        3 |               1 |           8 |        64 |     1024 |        0 |                         1023.64 |               976933.00 |             500351 |                            1249.00 |               499649 |                              3549.00 |
| mariadb-1-2-4 | mariadb-1-2-4 |                2 |        4 |               1 |          16 |       128 |     2048 |        0 |                         2046.44 |               488678.00 |             499534 |                            1385.00 |               500466 |                              4615.00 |

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MariaDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
