## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 14280s 
* Code: 1780419828
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
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MySQL-1-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:38G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-1-2 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:39G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-1-3 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:40G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-1-4 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:41G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-2-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:42G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-2-2 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:43G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-2-3 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:45G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-2-4 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:46G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

#### Planned

* DBMS MySQL-1 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

### Execution

#### Per Connection

| DBMS           | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:---------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|-----------------------------:|--------------------------------------------:|
| MySQL-1-1-1-1  | MySQL-1         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                          799.12 |              1251370.00 |             499858 |                            3715.00 |               500142 |                           2648063.00 |                            0 |                                        0.00 |
| MySQL-1-1-2-1  | MySQL-1         |                1 |        2 |       1 |        64 |     1024 |           2 |            0 |                          317.95 |              1572571.00 |             249489 |                            1995.00 |               250511 |                          10338303.00 |                            0 |                                        0.00 |
| MySQL-1-1-2-2  | MySQL-1         |                1 |        2 |       2 |        64 |     1024 |           2 |            0 |                          317.75 |              1573578.00 |             249971 |                            2020.00 |               250029 |                          10264575.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-6  | MySQL-1         |                1 |        3 |       6 |         8 |      128 |           8 |            0 |                           86.87 |              1438964.00 |              62549 |                            2001.00 |                62451 |                           3461119.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-5  | MySQL-1         |                1 |        3 |       5 |         8 |      128 |           8 |            0 |                           86.65 |              1442551.00 |              62392 |                            2019.00 |                62608 |                           3383295.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-4  | MySQL-1         |                1 |        3 |       4 |         8 |      128 |           8 |            0 |                           86.71 |              1441583.00 |              62464 |                            1996.00 |                62536 |                           3477503.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-3  | MySQL-1         |                1 |        3 |       3 |         8 |      128 |           8 |            0 |                           86.71 |              1441629.00 |              62683 |                            2003.00 |                62317 |                           3522559.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-1  | MySQL-1         |                1 |        3 |       1 |         8 |      128 |           8 |            0 |                           87.12 |              1434739.00 |              62433 |                            1967.00 |                62567 |                           3463167.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-7  | MySQL-1         |                1 |        3 |       7 |         8 |      128 |           8 |            0 |                           86.74 |              1441125.00 |              62557 |                            2067.00 |                62443 |                           3471359.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-2  | MySQL-1         |                1 |        3 |       2 |         8 |      128 |           8 |            0 |                           86.83 |              1439515.00 |              62275 |                            2027.00 |                62725 |                           3309567.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-8  | MySQL-1         |                1 |        3 |       8 |         8 |      128 |           8 |            0 |                           86.64 |              1442721.00 |              62417 |                            1967.00 |                62583 |                           3383295.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-15 | MySQL-1         |                1 |        4 |      15 |         8 |      128 |          16 |            0 |                           44.02 |              1419810.00 |              31207 |                            1996.00 |                31293 |                           9428991.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-12 | MySQL-1         |                1 |        4 |      12 |         8 |      128 |          16 |            0 |                           44.06 |              1418399.00 |              31251 |                            1992.00 |                31249 |                           9297919.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-14 | MySQL-1         |                1 |        4 |      14 |         8 |      128 |          16 |            0 |                           44.01 |              1420260.00 |              31367 |                            2003.00 |                31133 |                           9150463.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-16 | MySQL-1         |                1 |        4 |      16 |         8 |      128 |          16 |            0 |                           43.91 |              1423264.00 |              31373 |                            2010.00 |                31127 |                           9191423.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-7  | MySQL-1         |                1 |        4 |       7 |         8 |      128 |          16 |            0 |                           43.87 |              1424547.00 |              31150 |                            1932.00 |                31350 |                           9576447.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-6  | MySQL-1         |                1 |        4 |       6 |         8 |      128 |          16 |            0 |                           43.94 |              1422349.00 |              31287 |                            1985.00 |                31213 |                           9093119.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-8  | MySQL-1         |                1 |        4 |       8 |         8 |      128 |          16 |            0 |                           43.87 |              1424554.00 |              31353 |                            1924.00 |                31147 |                           9347071.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-13 | MySQL-1         |                1 |        4 |      13 |         8 |      128 |          16 |            0 |                           43.81 |              1426530.00 |              31151 |                            1978.00 |                31349 |                           9682943.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-2  | MySQL-1         |                1 |        4 |       2 |         8 |      128 |          16 |            0 |                           43.92 |              1422925.00 |              31166 |                            2025.00 |                31334 |                           9510911.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-10 | MySQL-1         |                1 |        4 |      10 |         8 |      128 |          16 |            0 |                           43.91 |              1423479.00 |              31278 |                            2003.00 |                31222 |                           9650175.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-11 | MySQL-1         |                1 |        4 |      11 |         8 |      128 |          16 |            0 |                           43.95 |              1422210.00 |              31181 |                            1981.00 |                31319 |                           9428991.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-3  | MySQL-1         |                1 |        4 |       3 |         8 |      128 |          16 |            0 |                           43.92 |              1423130.00 |              31370 |                            1924.00 |                31130 |                           9437183.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-1  | MySQL-1         |                1 |        4 |       1 |         8 |      128 |          16 |            0 |                           43.97 |              1421566.00 |              31036 |                            1974.00 |                31464 |                           9535487.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-5  | MySQL-1         |                1 |        4 |       5 |         8 |      128 |          16 |            0 |                           43.82 |              1426251.00 |              31139 |                            1990.00 |                31361 |                           9347071.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-4  | MySQL-1         |                1 |        4 |       4 |         8 |      128 |          16 |            0 |                           44.14 |              1415857.00 |              31329 |                            1977.00 |                31171 |                           9355263.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-9  | MySQL-1         |                1 |        4 |       9 |         8 |      128 |          16 |            0 |                           43.97 |              1421577.00 |              31304 |                            1916.00 |                31196 |                           9347071.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-6  | MySQL-1         |                2 |        4 |       6 |         8 |      128 |          16 |            0 |                           47.23 |              1323341.00 |              31286 |                            1927.00 |                31214 |                           7749631.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-10 | MySQL-1         |                2 |        4 |      10 |         8 |      128 |          16 |            0 |                           47.09 |              1327367.00 |              30946 |                            2001.00 |                31553 |                           7737343.00 |                            1 |                                 50102271.00 |
| MySQL-1-2-4-11 | MySQL-1         |                2 |        4 |      11 |         8 |      128 |          16 |            0 |                           47.12 |              1326408.00 |              31134 |                            1946.00 |                31365 |                           7688191.00 |                            1 |                                 50888703.00 |
| MySQL-1-2-4-4  | MySQL-1         |                2 |        4 |       4 |         8 |      128 |          16 |            0 |                           47.31 |              1321003.00 |              31401 |                            1920.00 |                31098 |                           7692287.00 |                            1 |                                 50888703.00 |
| MySQL-1-2-4-12 | MySQL-1         |                2 |        4 |      12 |         8 |      128 |          16 |            0 |                           47.33 |              1320481.00 |              31286 |                            1999.00 |                31214 |                           7647231.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-16 | MySQL-1         |                2 |        4 |      16 |         8 |      128 |          16 |            0 |                           47.15 |              1325516.00 |              31368 |                            2042.00 |                31132 |                           8011775.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-13 | MySQL-1         |                2 |        4 |      13 |         8 |      128 |          16 |            0 |                           47.14 |              1325750.00 |              31170 |                            1972.00 |                31330 |                           7647231.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-5  | MySQL-1         |                2 |        4 |       5 |         8 |      128 |          16 |            0 |                           47.18 |              1324636.00 |              31034 |                            1946.00 |                31466 |                           7827455.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-1  | MySQL-1         |                2 |        4 |       1 |         8 |      128 |          16 |            0 |                           47.14 |              1325850.00 |              31057 |                            1946.00 |                31443 |                           7622655.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-7  | MySQL-1         |                2 |        4 |       7 |         8 |      128 |          16 |            0 |                           47.18 |              1324723.00 |              31258 |                            1944.00 |                31241 |                           7651327.00 |                            1 |                                 50167807.00 |
| MySQL-1-2-4-8  | MySQL-1         |                2 |        4 |       8 |         8 |      128 |          16 |            0 |                           47.20 |              1324175.00 |              31333 |                            2021.00 |                31167 |                           7778303.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-3  | MySQL-1         |                2 |        4 |       3 |         8 |      128 |          16 |            0 |                           47.22 |              1323649.00 |              30973 |                            1989.00 |                31526 |                           7770111.00 |                            1 |                                 50102271.00 |
| MySQL-1-2-4-2  | MySQL-1         |                2 |        4 |       2 |         8 |      128 |          16 |            0 |                           47.24 |              1323105.00 |              31411 |                            1912.00 |                31089 |                           7757823.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-9  | MySQL-1         |                2 |        4 |       9 |         8 |      128 |          16 |            0 |                           47.11 |              1326685.00 |              31164 |                            1924.00 |                31333 |                           7704575.00 |                            3 |                                 50364415.00 |
| MySQL-1-2-1-1  | MySQL-1         |                2 |        1 |       1 |        64 |     1024 |           1 |            0 |                          673.11 |              1485637.00 |             500509 |                            2063.00 |               499491 |                           3090431.00 |                            0 |                                        0.00 |
| MySQL-1-2-2-1  | MySQL-1         |                2 |        2 |       1 |        64 |     1024 |           2 |            0 |                          351.74 |              1421499.00 |             249566 |                            1984.00 |               250434 |                           8437759.00 |                            0 |                                        0.00 |
| MySQL-1-2-2-2  | MySQL-1         |                2 |        2 |       2 |        64 |     1024 |           2 |            0 |                          351.75 |              1421453.00 |             249874 |                            1988.00 |               250126 |                           8536063.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-1  | MySQL-1         |                2 |        3 |       1 |         8 |      128 |           8 |            0 |                           77.33 |              1616421.00 |              62630 |                            1859.00 |                62370 |                           3301375.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-6  | MySQL-1         |                2 |        3 |       6 |         8 |      128 |           8 |            0 |                           79.69 |              1568582.00 |              62561 |                            1917.00 |                62439 |                           3235839.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-7  | MySQL-1         |                2 |        3 |       7 |         8 |      128 |           8 |            0 |                           80.53 |              1552262.00 |              62129 |                            1912.00 |                62871 |                           3102719.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-2  | MySQL-1         |                2 |        3 |       2 |         8 |      128 |           8 |            0 |                           80.40 |              1554681.00 |              62478 |                            1911.00 |                62522 |                           3170303.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-5  | MySQL-1         |                2 |        3 |       5 |         8 |      128 |           8 |            0 |                           80.05 |              1561613.00 |              62351 |                            1923.00 |                62649 |                           3207167.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-4  | MySQL-1         |                2 |        3 |       4 |         8 |      128 |           8 |            0 |                           79.21 |              1578158.00 |              62447 |                            1878.00 |                62553 |                           3235839.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-3  | MySQL-1         |                2 |        3 |       3 |         8 |      128 |           8 |            0 |                           79.12 |              1579887.00 |              62739 |                            1873.00 |                62261 |                           3223551.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-8  | MySQL-1         |                2 |        3 |       8 |         8 |      128 |           8 |            0 |                           80.33 |              1556101.00 |              62439 |                            1948.00 |                62561 |                           3172351.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-14 | MySQL-1         |                2 |        4 |      14 |         8 |      128 |          16 |            0 |                           47.18 |              1324659.00 |              31349 |                            1887.00 |                31151 |                           7749631.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-15 | MySQL-1         |                2 |        4 |      15 |         8 |      128 |          16 |            0 |                           47.10 |              1326985.00 |              31303 |                            1909.00 |                31197 |                           7770111.00 |                            0 |                                        0.00 |

#### Per Phase

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|-----------------------------:|--------------------------------------------:|
| MySQL-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                          799.12 |              1251370.00 |          499858.00 |                            3715.00 |            500142.00 |                           2648063.00 |                         0.00 |                                        0.00 |
| MySQL-1-1-2 |             1.00 |    128.00 |  2048.00 |        2.00 |         0.00 |                          635.70 |              1573578.00 |          499460.00 |                            2020.00 |            500540.00 |                          10338303.00 |                         0.00 |                                        0.00 |
| MySQL-1-1-3 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                          694.28 |              1442721.00 |          499770.00 |                            2067.00 |            500230.00 |                           3522559.00 |                         0.00 |                                        0.00 |
| MySQL-1-1-4 |             1.00 |    128.00 |  2048.00 |       16.00 |         0.00 |                          703.09 |              1426530.00 |          499942.00 |                            2025.00 |            500058.00 |                           9682943.00 |                         0.00 |                                        0.00 |
| MySQL-1-2-1 |             2.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                          673.11 |              1485637.00 |          500509.00 |                            2063.00 |            499491.00 |                           3090431.00 |                         0.00 |                                        0.00 |
| MySQL-1-2-2 |             2.00 |    128.00 |  2048.00 |        2.00 |         0.00 |                          703.49 |              1421499.00 |          499440.00 |                            1988.00 |            500560.00 |                           8536063.00 |                         0.00 |                                        0.00 |
| MySQL-1-2-3 |             2.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                          636.65 |              1616421.00 |          499774.00 |                            1948.00 |            500226.00 |                           3301375.00 |                         0.00 |                                        0.00 |
| MySQL-1-2-4 |             2.00 |    128.00 |  2048.00 |       16.00 |         0.00 |                          754.92 |              1327367.00 |          499473.00 |                            2042.00 |            500519.00 |                           8011775.00 |                         8.00 |                                 50888703.00 |

### Tests
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
