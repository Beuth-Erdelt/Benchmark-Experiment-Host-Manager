## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 7175s 
* Code: 1780349271
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
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-1-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-1-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-1-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-2-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-2-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-2-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-2-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

#### Planned

* DBMS MariaDB-1 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

### Loading

#### Per Connection



#### Per Run



### Execution

#### Per Connection

| DBMS             | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1-1  | MariaDB-1       |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1002.46 |               997550.00 |             500951 |                            1455.00 |               499049 |                            143871.00 |
| MariaDB-1-1-2-1  | MariaDB-1       |                1 |        2 |       1 |        64 |     1024 |           2 |            0 |                         1023.09 |               488715.00 |             249284 |                            3319.00 |               250716 |                            299007.00 |
| MariaDB-1-1-2-2  | MariaDB-1       |                1 |        2 |       2 |        64 |     1024 |           2 |            0 |                         1023.08 |               488719.00 |             250286 |                            3287.00 |               249714 |                            299007.00 |
| MariaDB-1-1-3-2  | MariaDB-1       |                1 |        3 |       2 |         8 |      128 |           8 |            0 |                          127.95 |               976954.00 |              62348 |                            2089.00 |                62652 |                            304639.00 |
| MariaDB-1-1-3-7  | MariaDB-1       |                1 |        3 |       7 |         8 |      128 |           8 |            0 |                          127.95 |               976942.00 |              62564 |                            2325.00 |                62436 |                            305663.00 |
| MariaDB-1-1-3-6  | MariaDB-1       |                1 |        3 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976864.00 |              62447 |                            2407.00 |                62553 |                            304383.00 |
| MariaDB-1-1-3-5  | MariaDB-1       |                1 |        3 |       5 |         8 |      128 |           8 |            0 |                          127.92 |               977171.00 |              62548 |                            2335.00 |                62452 |                            303615.00 |
| MariaDB-1-1-3-4  | MariaDB-1       |                1 |        3 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976864.00 |              62396 |                            2413.00 |                62604 |                            305919.00 |
| MariaDB-1-1-3-1  | MariaDB-1       |                1 |        3 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976886.00 |              62623 |                            2353.00 |                62377 |                            310015.00 |
| MariaDB-1-1-3-3  | MariaDB-1       |                1 |        3 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976870.00 |              62348 |                            2393.00 |                62652 |                            305151.00 |
| MariaDB-1-1-3-8  | MariaDB-1       |                1 |        3 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976863.00 |              62610 |                            2303.00 |                62390 |                            306431.00 |
| MariaDB-1-1-4-15 | MariaDB-1       |                1 |        4 |      15 |         8 |      128 |          16 |            0 |                          127.88 |               488737.00 |              31204 |                            3049.00 |                31296 |                            406015.00 |
| MariaDB-1-1-4-16 | MariaDB-1       |                1 |        4 |      16 |         8 |      128 |          16 |            0 |                          127.87 |               488794.00 |              31355 |                            3041.00 |                31145 |                            413951.00 |
| MariaDB-1-1-4-14 | MariaDB-1       |                1 |        4 |      14 |         8 |      128 |          16 |            0 |                          127.91 |               488638.00 |              31159 |                            3261.00 |                31341 |                            416511.00 |
| MariaDB-1-1-4-4  | MariaDB-1       |                1 |        4 |       4 |         8 |      128 |          16 |            0 |                          127.91 |               488627.00 |              31470 |                            2983.00 |                31030 |                            424191.00 |
| MariaDB-1-1-4-2  | MariaDB-1       |                1 |        4 |       2 |         8 |      128 |          16 |            0 |                          127.91 |               488626.00 |              31261 |                            3121.00 |                31239 |                            431615.00 |
| MariaDB-1-1-4-8  | MariaDB-1       |                1 |        4 |       8 |         8 |      128 |          16 |            0 |                          127.91 |               488631.00 |              31232 |                            3163.00 |                31268 |                            403967.00 |
| MariaDB-1-1-4-5  | MariaDB-1       |                1 |        4 |       5 |         8 |      128 |          16 |            0 |                          127.89 |               488707.00 |              31283 |                            3075.00 |                31217 |                            404991.00 |
| MariaDB-1-1-4-13 | MariaDB-1       |                1 |        4 |      13 |         8 |      128 |          16 |            0 |                          127.91 |               488617.00 |              31291 |                            3079.00 |                31209 |                            406527.00 |
| MariaDB-1-1-4-11 | MariaDB-1       |                1 |        4 |      11 |         8 |      128 |          16 |            0 |                          127.91 |               488622.00 |              31249 |                            3075.00 |                31251 |                            412415.00 |
| MariaDB-1-1-4-1  | MariaDB-1       |                1 |        4 |       1 |         8 |      128 |          16 |            0 |                          127.91 |               488610.00 |              31250 |                            3179.00 |                31250 |                            415231.00 |
| MariaDB-1-1-4-3  | MariaDB-1       |                1 |        4 |       3 |         8 |      128 |          16 |            0 |                          127.91 |               488632.00 |              31171 |                            3411.00 |                31329 |                            418303.00 |
| MariaDB-1-1-4-6  | MariaDB-1       |                1 |        4 |       6 |         8 |      128 |          16 |            0 |                          127.87 |               488793.00 |              31242 |                            3169.00 |                31258 |                            417023.00 |
| MariaDB-1-1-4-10 | MariaDB-1       |                1 |        4 |      10 |         8 |      128 |          16 |            0 |                          127.89 |               488720.00 |              31154 |                            3255.00 |                31346 |                            406015.00 |
| MariaDB-1-1-4-12 | MariaDB-1       |                1 |        4 |      12 |         8 |      128 |          16 |            0 |                          127.91 |               488635.00 |              31241 |                            3187.00 |                31259 |                            400127.00 |
| MariaDB-1-1-4-9  | MariaDB-1       |                1 |        4 |       9 |         8 |      128 |          16 |            0 |                          127.91 |               488634.00 |              31322 |                            3125.00 |                31178 |                            397823.00 |
| MariaDB-1-1-4-7  | MariaDB-1       |                1 |        4 |       7 |         8 |      128 |          16 |            0 |                          127.91 |               488631.00 |              31173 |                            3031.00 |                31327 |                            398335.00 |
| MariaDB-1-2-4-8  | MariaDB-1       |                2 |        4 |       8 |         8 |      128 |          16 |            0 |                          127.91 |               488641.00 |              31555 |                            2179.00 |                30945 |                            276991.00 |
| MariaDB-1-2-4-14 | MariaDB-1       |                2 |        4 |      14 |         8 |      128 |          16 |            0 |                          127.79 |               489093.00 |              31258 |                            2339.00 |                31242 |                            289023.00 |
| MariaDB-1-2-4-2  | MariaDB-1       |                2 |        4 |       2 |         8 |      128 |          16 |            0 |                          127.78 |               489121.00 |              31369 |                            2251.00 |                31131 |                            278015.00 |
| MariaDB-1-2-4-13 | MariaDB-1       |                2 |        4 |      13 |         8 |      128 |          16 |            0 |                          127.91 |               488619.00 |              31472 |                            2311.00 |                31028 |                            274687.00 |
| MariaDB-1-2-4-6  | MariaDB-1       |                2 |        4 |       6 |         8 |      128 |          16 |            0 |                          127.91 |               488609.00 |              31370 |                            2107.00 |                31130 |                            271615.00 |
| MariaDB-1-2-4-7  | MariaDB-1       |                2 |        4 |       7 |         8 |      128 |          16 |            0 |                          127.91 |               488627.00 |              31332 |                            2243.00 |                31168 |                            277759.00 |
| MariaDB-1-2-4-11 | MariaDB-1       |                2 |        4 |      11 |         8 |      128 |          16 |            0 |                          127.91 |               488635.00 |              31340 |                            2271.00 |                31160 |                            276223.00 |
| MariaDB-1-2-4-3  | MariaDB-1       |                2 |        4 |       3 |         8 |      128 |          16 |            0 |                          127.91 |               488614.00 |              31296 |                            2323.00 |                31204 |                            273407.00 |
| MariaDB-1-2-4-5  | MariaDB-1       |                2 |        4 |       5 |         8 |      128 |          16 |            0 |                          127.91 |               488615.00 |              31224 |                            2247.00 |                31276 |                            275455.00 |
| MariaDB-1-2-4-10 | MariaDB-1       |                2 |        4 |      10 |         8 |      128 |          16 |            0 |                          127.92 |               488603.00 |              31133 |                            2235.00 |                31367 |                            277503.00 |
| MariaDB-1-2-4-16 | MariaDB-1       |                2 |        4 |      16 |         8 |      128 |          16 |            0 |                          127.91 |               488610.00 |              31219 |                            2261.00 |                31281 |                            282879.00 |
| MariaDB-1-2-4-12 | MariaDB-1       |                2 |        4 |      12 |         8 |      128 |          16 |            0 |                          127.91 |               488629.00 |              31060 |                            2203.00 |                31440 |                            288511.00 |
| MariaDB-1-2-4-15 | MariaDB-1       |                2 |        4 |      15 |         8 |      128 |          16 |            0 |                          127.91 |               488634.00 |              31091 |                            2049.00 |                31409 |                            260735.00 |
| MariaDB-1-2-4-1  | MariaDB-1       |                2 |        4 |       1 |         8 |      128 |          16 |            0 |                          127.91 |               488610.00 |              31096 |                            2295.00 |                31404 |                            269055.00 |
| MariaDB-1-2-1-1  | MariaDB-1       |                2 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1023.58 |               976960.00 |             499579 |                            1637.00 |               500421 |                            242303.00 |
| MariaDB-1-2-2-2  | MariaDB-1       |                2 |        2 |       2 |        64 |     1024 |           2 |            0 |                         1023.11 |               488708.00 |             249669 |                            2597.00 |               250331 |                            297727.00 |
| MariaDB-1-2-2-1  | MariaDB-1       |                2 |        2 |       1 |        64 |     1024 |           2 |            0 |                         1023.10 |               488713.00 |             249729 |                            2765.00 |               250271 |                            297215.00 |
| MariaDB-1-2-3-5  | MariaDB-1       |                2 |        3 |       5 |         8 |      128 |           8 |            0 |                          127.96 |               976858.00 |              62480 |                            1990.00 |                62520 |                            285439.00 |
| MariaDB-1-2-3-7  | MariaDB-1       |                2 |        3 |       7 |         8 |      128 |           8 |            0 |                          127.96 |               976874.00 |              62805 |                            1902.00 |                62195 |                            286207.00 |
| MariaDB-1-2-3-4  | MariaDB-1       |                2 |        3 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976866.00 |              62311 |                            1836.00 |                62689 |                            283135.00 |
| MariaDB-1-2-3-3  | MariaDB-1       |                2 |        3 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976866.00 |              62568 |                            1918.00 |                62432 |                            286975.00 |
| MariaDB-1-2-3-1  | MariaDB-1       |                2 |        3 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976881.00 |              62561 |                            1886.00 |                62439 |                            287743.00 |
| MariaDB-1-2-3-2  | MariaDB-1       |                2 |        3 |       2 |         8 |      128 |           8 |            0 |                          127.96 |               976860.00 |              62406 |                            1962.00 |                62594 |                            290047.00 |
| MariaDB-1-2-3-6  | MariaDB-1       |                2 |        3 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976867.00 |              62272 |                            1985.00 |                62728 |                            283391.00 |
| MariaDB-1-2-3-8  | MariaDB-1       |                2 |        3 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976843.00 |              62658 |                            1892.00 |                62342 |                            283135.00 |
| MariaDB-1-2-4-4  | MariaDB-1       |                2 |        4 |       4 |         8 |      128 |          16 |            0 |                          127.82 |               488982.00 |              31224 |                            2263.00 |                31276 |                            281343.00 |
| MariaDB-1-2-4-9  | MariaDB-1       |                2 |        4 |       9 |         8 |      128 |          16 |            0 |                          127.80 |               489064.00 |              31164 |                            2137.00 |                31336 |                            261759.00 |

#### Per Phase

| DBMS          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1002.46 |               997550.00 |          500951.00 |                            1455.00 |            499049.00 |                            143871.00 |
| MariaDB-1-1-2 |             1.00 |    128.00 |  2048.00 |        2.00 |         0.00 |                         2046.17 |               488719.00 |          499570.00 |                            3319.00 |            500430.00 |                            299007.00 |
| MariaDB-1-1-3 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                         1023.62 |               977171.00 |          499884.00 |                            2413.00 |            500116.00 |                            310015.00 |
| MariaDB-1-1-4 |             1.00 |    128.00 |  2048.00 |       16.00 |         0.00 |                         2046.39 |               488794.00 |          500057.00 |                            3411.00 |            499943.00 |                            431615.00 |
| MariaDB-1-2-1 |             2.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1023.58 |               976960.00 |          499579.00 |                            1637.00 |            500421.00 |                            242303.00 |
| MariaDB-1-2-2 |             2.00 |    128.00 |  2048.00 |        2.00 |         0.00 |                         2046.20 |               488713.00 |          499398.00 |                            2765.00 |            500602.00 |                            297727.00 |
| MariaDB-1-2-3 |             2.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                         1023.68 |               976881.00 |          500061.00 |                            1990.00 |            499939.00 |                            290047.00 |
| MariaDB-1-2-4 |             2.00 |    128.00 |  2048.00 |       16.00 |         0.00 |                         2046.11 |               489121.00 |          500203.00 |                            2339.00 |            499797.00 |                            289023.00 |

### Tests
* TEST failed: Loading Phase: [OVERALL].Throughput(ops/sec) contains 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
