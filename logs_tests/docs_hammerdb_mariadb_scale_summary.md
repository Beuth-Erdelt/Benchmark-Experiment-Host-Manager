## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: hammerdb
* Duration: 2993s 
* Code: 1794776720
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
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
  * disk:1053146
  * datadisk:2476
  * volume_size:49G
  * volume_used:2.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794776720
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1074259
  * datadisk:2901
  * volume_size:49G
  * volume_used:2.9G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794776720
* mariadb-1-1-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1094033
  * datadisk:3505
  * volume_size:49G
  * volume_used:3.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794776720
* mariadb-1-1-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1077768
  * datadisk:3965
  * volume_size:49G
  * volume_used:3.9G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794776720
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1079188
  * datadisk:4621
  * volume_size:49G
  * volume_used:4.6G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794776720
* mariadb-1-2-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1076178
  * datadisk:5050
  * volume_size:49G
  * volume_used:5.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794776720
* mariadb-1-2-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091402
  * datadisk:5653
  * volume_size:49G
  * volume_used:5.6G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794776720
* mariadb-1-2-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091351
  * datadisk:6086
  * volume_size:49G
  * volume_used:6.0G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794776720

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794776720-56595df9c8-h8gkl: 0
* bexhoma-sut-mariadb-1-1794776720-7d4dc6bff9-vbqgn: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: hammerdb (4 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: hammerdb (4 pods)

### Loading

#### Per Run

| DBMS        |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |       65.00 |           5.00 |            0.00 |         55.00 |            5.00 |              0 |         8 |             | None           |             0 | False         |              886.15 | True                |
| MariaDB-1-2 |                2 |   16 |       65.00 |           5.00 |            0.00 |         55.00 |            5.00 |              0 |         8 |             | None           |             0 | False         |              886.15 | True                |

### Benchmarking

#### Per Connection

| connection        | phase         | job             |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |
|:------------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |        1 |               1 |       1 |        16 | 101384 | 236116 |         0.00 |          2 |        0 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       1 |        16 | 149725 | 346828 |         0.00 |          2 |        0 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |        2 |               1 |       2 |        16 | 149562 | 346472 |         0.00 |          2 |        0 |
| mariadb-1-1-3-1-1 | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       1 |         8 | 110986 | 257824 |         0.00 |          2 |        0 |
| mariadb-1-1-3-1-2 | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        3 |               1 |       2 |         8 | 110770 | 257219 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-1 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       1 |         8 | 166950 | 387565 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-2 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       2 |         8 | 166952 | 387498 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-3 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       3 |         8 | 166943 | 387463 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-4 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        4 |               1 |       4 |         8 | 166926 | 387498 |         0.00 |          2 |        0 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |        1 |               1 |       1 |        16 | 107876 | 251079 |         0.00 |          2 |        0 |
| mariadb-1-2-2-1-1 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       1 |        16 | 148155 | 344432 |         0.00 |          2 |        0 |
| mariadb-1-2-2-1-2 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |        2 |               1 |       2 |        16 | 147892 | 343769 |         0.00 |          2 |        0 |
| mariadb-1-2-3-1-1 | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       1 |         8 | 111182 | 258497 |         0.00 |          2 |        0 |
| mariadb-1-2-3-1-2 | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        3 |               1 |       2 |         8 | 110928 | 258044 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-1 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       1 |         8 |  27432 |  63884 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-2 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       2 |         8 |  27323 |  63641 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-3 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       3 |         8 |  27390 |  63782 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-4 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        4 |               1 |       4 |         8 |  27455 |  63943 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   efficiency |      NOPM |       TPM |   duration |   errors |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|----------:|-------------:|----------:|----------:|-----------:|---------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |        1 |               1 |           1 |        16 |         0.00 | 101384.00 | 236116.00 |          2 |        0 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |        2 |               1 |           2 |        32 |         0.00 | 149643.50 | 346650.00 |          2 |        0 |
| mariadb-1-1-3 | mariadb-1-1-3 |                1 |        3 |               1 |           2 |        16 |         0.00 | 110878.00 | 257521.50 |          2 |        0 |
| mariadb-1-1-4 | mariadb-1-1-4 |                1 |        4 |               1 |           4 |        32 |         0.00 | 166942.75 | 387506.00 |          2 |        0 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |        1 |               1 |           1 |        16 |         0.00 | 107876.00 | 251079.00 |          2 |        0 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |        2 |               1 |           2 |        32 |         0.00 | 148023.50 | 344100.50 |          2 |        0 |
| mariadb-1-2-3 | mariadb-1-2-3 |                2 |        3 |               1 |           2 |        16 |         0.00 | 111055.00 | 258270.50 |          2 |        0 |
| mariadb-1-2-4 | mariadb-1-2-4 |                2 |        4 |               1 |           4 |        32 |         0.00 |  27400.00 |  63812.50 |          2 |        0 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |      1146.84 |      5.26 |           3.37 |                  3.38 |
| mariadb-1-1-2-1 |      1841.53 |      8.73 |           4.02 |                  4.03 |
| mariadb-1-1-3-1 |      1207.75 |      5.43 |           4.48 |                  4.48 |
| mariadb-1-1-4-1 |      1761.40 |      8.30 |           5.12 |                  5.12 |
| mariadb-1-2-1-1 |      1128.58 |      5.49 |           5.42 |                  5.42 |
| mariadb-1-2-2-1 |      1861.65 |      8.54 |           6.11 |                  6.11 |
| mariadb-1-2-3-1 |      1149.55 |      5.40 |           6.53 |                  6.54 |
| mariadb-1-2-4-1 |      1270.86 |      8.11 |           6.89 |                  6.89 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       370.27 |      1.73 |           0.08 |                  0.08 |
| mariadb-1-1-2-1 |       343.20 |      1.85 |           0.08 |                  0.08 |
| mariadb-1-1-3-1 |       235.55 |      1.48 |           0.05 |                  0.05 |
| mariadb-1-1-4-1 |       533.64 |      2.60 |           0.05 |                  0.05 |
| mariadb-1-2-1-1 |       249.94 |      1.54 |           0.08 |                  0.08 |
| mariadb-1-2-2-1 |       324.25 |      1.87 |           0.08 |                  0.08 |
| mariadb-1-2-3-1 |       288.21 |      1.64 |           0.05 |                  0.05 |
| mariadb-1-2-4-1 |       166.62 |      1.20 |           0.05 |                  0.05 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-1-1 (bexhoma-metrics-mariadb-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-2-1 (bexhoma-metrics-mariadb-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-3-1 (bexhoma-metrics-mariadb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-3-1 (bexhoma-metrics-mariadb-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-3-1 (bexhoma-metrics-mariadb-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-3-1 (bexhoma-metrics-mariadb-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-4-1 (bexhoma-metrics-mariadb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-4-1 (bexhoma-metrics-mariadb-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-1-4-1 (bexhoma-metrics-mariadb-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-1-4-1 (bexhoma-metrics-mariadb-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-1-1 (bexhoma-metrics-mariadb-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-2-1 (bexhoma-metrics-mariadb-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-3-1 (bexhoma-metrics-mariadb-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-3-1 (bexhoma-metrics-mariadb-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-3-1 (bexhoma-metrics-mariadb-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-3-1 (bexhoma-metrics-mariadb-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-4-1 (bexhoma-metrics-mariadb-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-4-1 (bexhoma-metrics-mariadb-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mariadb-1-2-4-1 (bexhoma-metrics-mariadb-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mariadb-1-2-4-1 (bexhoma-metrics-mariadb-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MariaDB-1)
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
