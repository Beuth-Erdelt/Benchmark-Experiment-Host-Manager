## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2194s 
* Code: 1780047177
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-1-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-1-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-1-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-2-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.1G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-2-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.1G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-2-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.1G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-2-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.1G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

#### Planned

* DBMS MariaDB-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |     1087.00 |           1.00 |            0.00 |        525.00 |          561.00 |              0 |           1 |          | None           |             0 | False         |               52.99 |
| MariaDB-1-2 |                2 |   16 |     1087.00 |           1.00 |            0.00 |        525.00 |          561.00 |              0 |           1 |          | None           |             0 | False         |               52.99 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1 |             1.00 |      160.00 |  8192.00 |     1.00 |    1.00 | 120.00 |        43.00 |                         383.78 |                      377.61 |         0.00 |                                                     101269.00 |                                             294908.00 |
| MariaDB-1-1-2-1 |             1.00 |      160.00 |  8192.00 |     2.00 |    1.00 | 120.00 |        22.00 |                         187.88 |                      185.97 |         0.00 |                                                    3123314.00 |                                             850463.00 |
| MariaDB-1-1-2-2 |             1.00 |      160.00 |  8192.00 |     2.00 |    2.00 | 120.00 |        16.00 |                         215.47 |                      213.08 |         0.00 |                                                    2826271.00 |                                             740682.00 |
| MariaDB-1-1-3-1 |             1.00 |       80.00 |  4096.00 |     3.00 |    1.00 | 120.00 |         0.00 |                         150.78 |                      148.98 |         0.00 |                                                    2582112.00 |                                             530471.00 |
| MariaDB-1-1-3-2 |             1.00 |       80.00 |  4096.00 |     3.00 |    2.00 | 120.00 |         0.00 |                         148.27 |                      146.20 |         0.00 |                                                    2596819.00 |                                             534672.00 |
| MariaDB-1-1-4-1 |             1.00 |       80.00 |  4096.00 |     4.00 |    1.00 | 120.00 |       110.00 |                          91.65 |                       89.84 |         0.00 |                                                     424148.00 |                                             719005.00 |
| MariaDB-1-1-4-2 |             1.00 |       80.00 |  4096.00 |     4.00 |    2.00 | 120.00 |       100.00 |                          75.59 |                       74.33 |         0.00 |                                                     577066.00 |                                             972171.00 |
| MariaDB-1-1-4-3 |             1.00 |       80.00 |  4096.00 |     4.00 |    3.00 | 120.00 |        87.00 |                          79.75 |                       78.60 |         0.00 |                                                     477518.00 |                                             767402.00 |
| MariaDB-1-1-4-4 |             1.00 |       80.00 |  4096.00 |     4.00 |    4.00 | 120.00 |       104.00 |                          99.69 |                       97.74 |         0.00 |                                                     376222.00 |                                             640196.00 |
| MariaDB-1-2-1-1 |             2.00 |      160.00 |  8192.00 |     1.00 |    1.00 | 120.00 |        16.00 |                         453.26 |                      446.19 |         0.00 |                                                     146710.00 |                                             339082.00 |
| MariaDB-1-2-2-1 |             2.00 |      160.00 |  8192.00 |     2.00 |    1.00 | 120.00 |       126.00 |                         167.36 |                      165.06 |         0.00 |                                                     386348.00 |                                             887074.00 |
| MariaDB-1-2-2-2 |             2.00 |      160.00 |  8192.00 |     2.00 |    2.00 | 120.00 |       125.00 |                         219.01 |                      215.65 |         0.00 |                                                     281451.00 |                                             677863.00 |
| MariaDB-1-2-3-1 |             2.00 |       80.00 |  4096.00 |     3.00 |    1.00 | 120.00 |        52.00 |                         165.51 |                      162.98 |         0.00 |                                                     167209.00 |                                             340298.00 |
| MariaDB-1-2-3-2 |             2.00 |       80.00 |  4096.00 |     3.00 |    2.00 | 120.00 |        56.00 |                         186.93 |                      183.84 |         0.00 |                                                     148148.00 |                                             325543.00 |
| MariaDB-1-2-4-1 |             2.00 |       80.00 |  4096.00 |     4.00 |    1.00 | 120.00 |        63.00 |                          94.56 |                       93.07 |         0.00 |                                                     735346.00 |                                             665147.00 |
| MariaDB-1-2-4-2 |             2.00 |       80.00 |  4096.00 |     4.00 |    2.00 | 120.00 |        57.00 |                          84.19 |                       83.14 |         0.00 |                                                     768878.00 |                                             740456.00 |
| MariaDB-1-2-4-3 |             2.00 |       80.00 |  4096.00 |     4.00 |    3.00 | 120.00 |        54.00 |                          86.40 |                       85.23 |         0.00 |                                                     762651.00 |                                             725338.00 |
| MariaDB-1-2-4-4 |             2.00 |       80.00 |  4096.00 |     4.00 |    4.00 | 120.00 |        61.00 |                         105.37 |                      103.81 |         0.00 |                                                     710149.00 |                                             598917.00 |

#### Per Phase

| DBMS          |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 |             1.00 |      160.00 |  8192.00 |        1.00 | 120.00 |        43.00 |                         383.78 |                      377.61 |         0.00 |                                                     101269.00 |                                             294908.00 |
| MariaDB-1-1-2 |             1.00 |      320.00 | 16384.00 |        2.00 | 120.00 |        38.00 |                         403.36 |                      399.06 |         0.00 |                                                    3123314.00 |                                             795572.50 |
| MariaDB-1-1-3 |             1.00 |      160.00 |  8192.00 |        2.00 | 120.00 |         0.00 |                         299.06 |                      295.18 |         0.00 |                                                    2596819.00 |                                             532571.50 |
| MariaDB-1-1-4 |             1.00 |      320.00 | 16384.00 |        4.00 | 120.00 |       401.00 |                         346.68 |                      340.52 |         0.00 |                                                     577066.00 |                                             774693.50 |
| MariaDB-1-2-1 |             2.00 |      160.00 |  8192.00 |        1.00 | 120.00 |        16.00 |                         453.26 |                      446.19 |         0.00 |                                                     146710.00 |                                             339082.00 |
| MariaDB-1-2-2 |             2.00 |      320.00 | 16384.00 |        2.00 | 120.00 |       251.00 |                         386.37 |                      380.71 |         0.00 |                                                     386348.00 |                                             782468.50 |
| MariaDB-1-2-3 |             2.00 |      160.00 |  8192.00 |        2.00 | 120.00 |       108.00 |                         352.44 |                      346.82 |         0.00 |                                                     167209.00 |                                             332920.50 |
| MariaDB-1-2-4 |             2.00 |      320.00 | 16384.00 |        4.00 | 120.00 |       235.00 |                         370.52 |                      365.26 |         0.00 |                                                     768878.00 |                                             682464.50 |

### Monitoring

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       895.81 |     17.49 |           7.14 |                  7.24 |
| MariaDB-1-1-2 |       892.12 |      8.98 |           7.34 |                  7.44 |
| MariaDB-1-1-3 |       826.20 |     10.08 |           7.40 |                  7.50 |
| MariaDB-1-1-4 |      1818.95 |     25.62 |           7.50 |                  7.60 |
| MariaDB-1-2-1 |      5268.63 |     26.71 |           7.49 |                  7.59 |
| MariaDB-1-2-2 |      2695.60 |     35.03 |           7.49 |                  7.59 |
| MariaDB-1-2-3 |      1407.09 |     33.20 |           7.54 |                  7.64 |
| MariaDB-1-2-4 |      1527.22 |     21.28 |           7.65 |                  7.75 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       132.28 |      1.07 |           0.72 |                  0.72 |
| MariaDB-1-1-2 |        87.22 |      3.57 |           0.72 |                  0.72 |
| MariaDB-1-1-3 |        72.10 |      0.91 |           0.70 |                  0.70 |
| MariaDB-1-1-4 |       132.74 |      1.82 |           0.41 |                  0.41 |
| MariaDB-1-2-1 |       148.20 |      1.81 |           0.71 |                  0.71 |
| MariaDB-1-2-2 |       120.82 |      2.71 |           1.06 |                  1.06 |
| MariaDB-1-2-3 |       106.84 |      3.19 |           1.06 |                  1.06 |
| MariaDB-1-2-4 |       123.89 |      2.99 |           1.06 |                  1.06 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
