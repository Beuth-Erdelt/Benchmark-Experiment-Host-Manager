## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 3224s 
* Code: 1780054976
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
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
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-1-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-1-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-1-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

#### Planned

* DBMS MariaDB-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      700.00 |           1.00 |            0.00 |        335.00 |          364.00 |              0 |           8 |          | None           |             0 | False         |               82.29 |
| MariaDB-1-2 |                2 |   16 |      700.00 |           1.00 |            0.00 |        335.00 |          364.00 |              0 |           8 |          | None           |             0 | False         |               82.29 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   vusers |   client |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:----------------|-----------------:|---------:|---------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| MariaDB-1-1-1-1 |                1 |       16 |        1 |       1 |  12123 | 28299 |         0.00 |          2 |        0 |
| MariaDB-1-1-2-1 |                1 |       16 |        2 |       1 |   9914 | 22893 |         0.00 |          2 |        0 |
| MariaDB-1-1-2-1 |                1 |       16 |        2 |       1 |  10146 | 23427 |         0.00 |          2 |        0 |
| MariaDB-1-1-3-1 |                1 |        8 |        3 |       1 |   7436 | 17246 |         0.00 |          2 |        0 |
| MariaDB-1-1-3-1 |                1 |        8 |        3 |       1 |   7440 | 17252 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6528 | 15148 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6591 | 15283 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6535 | 15169 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6560 | 15217 |         0.00 |          2 |        0 |
| MariaDB-1-2-1-1 |                2 |       16 |        1 |       1 |   9101 | 21227 |         0.00 |          2 |        0 |
| MariaDB-1-2-2-1 |                2 |       16 |        2 |       1 |   9011 | 20796 |         0.00 |          2 |        0 |
| MariaDB-1-2-2-1 |                2 |       16 |        2 |       1 |   9077 | 20938 |         0.00 |          2 |        0 |
| MariaDB-1-2-3-1 |                2 |        8 |        3 |       1 |   8350 | 19461 |         0.00 |          2 |        0 |
| MariaDB-1-2-3-1 |                2 |        8 |        3 |       1 |   8295 | 19358 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8527 | 19937 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8431 | 19717 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8498 | 19865 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8431 | 19717 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS          |   experiment_run |   vusers |   client |   pod_count |   efficiency |     NOPM |      TPM |   duration |   errors |
|:--------------|-----------------:|---------:|---------:|------------:|-------------:|---------:|---------:|-----------:|---------:|
| MariaDB-1-1-1 |             1.00 |    16.00 |     1.00 |        1.00 |         0.00 | 12123.00 | 28299.00 |       2.00 |     0.00 |
| MariaDB-1-1-2 |             1.00 |    32.00 |     2.00 |        2.00 |         0.00 | 10030.00 | 23160.00 |       2.00 |     0.00 |
| MariaDB-1-1-3 |             1.00 |    16.00 |     3.00 |        2.00 |         0.00 |  7438.00 | 17249.00 |       2.00 |     0.00 |
| MariaDB-1-1-4 |             1.00 |    32.00 |     4.00 |        4.00 |         0.00 |  6553.50 | 15204.25 |       2.00 |     0.00 |
| MariaDB-1-2-1 |             2.00 |    16.00 |     1.00 |        1.00 |         0.00 |  9101.00 | 21227.00 |       2.00 |     0.00 |
| MariaDB-1-2-2 |             2.00 |    32.00 |     2.00 |        2.00 |         0.00 |  9044.00 | 20867.00 |       2.00 |     0.00 |
| MariaDB-1-2-3 |             2.00 |    16.00 |     3.00 |        2.00 |         0.00 |  8322.50 | 19409.50 |       2.00 |     0.00 |
| MariaDB-1-2-4 |             2.00 |    32.00 |     4.00 |        4.00 |         0.00 |  8471.75 | 19809.00 |       2.00 |     0.00 |

### Monitoring

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       585.20 |      2.97 |           6.84 |                  6.94 |
| MariaDB-1-1-2 |       871.45 |      6.59 |           6.95 |                  7.05 |
| MariaDB-1-1-3 |       506.27 |      4.93 |           6.98 |                  7.08 |
| MariaDB-1-1-4 |       940.30 |      5.49 |           7.06 |                  7.16 |
| MariaDB-1-2-1 |      3027.35 |      2.36 |           7.06 |                  7.16 |
| MariaDB-1-2-2 |       863.04 |      4.29 |           7.06 |                  7.16 |
| MariaDB-1-2-3 |       418.66 |      2.17 |           7.09 |                  7.19 |
| MariaDB-1-2-4 |       798.13 |      3.86 |           7.18 |                  7.28 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |        24.52 |      0.13 |           0.07 |                  0.07 |
| MariaDB-1-1-2 |        24.52 |      0.34 |           0.07 |                  0.07 |
| MariaDB-1-1-3 |        21.49 |      0.28 |           0.07 |                  0.07 |
| MariaDB-1-1-4 |        16.11 |      0.25 |           0.04 |                  0.05 |
| MariaDB-1-2-1 |        22.71 |      0.13 |           0.07 |                  0.07 |
| MariaDB-1-2-2 |        22.71 |      0.27 |           0.07 |                  0.07 |
| MariaDB-1-2-3 |        22.87 |      0.21 |           0.07 |                  0.07 |
| MariaDB-1-2-4 |        18.35 |      0.26 |           0.04 |                  0.05 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
