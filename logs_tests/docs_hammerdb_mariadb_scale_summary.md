## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 2808s 
* Code: 1794141725
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
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
  * disk:805270
  * datadisk:2417
  * volume_size:49G
  * volume_used:2.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-1-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805272
  * datadisk:2876
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
    * code:1794141725
* mariadb-1-1-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805275
  * datadisk:3491
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
    * code:1794141725
* mariadb-1-1-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805277
  * datadisk:3944
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
    * code:1794141725
* mariadb-1-2-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805280
  * datadisk:4520
  * volume_size:49G
  * volume_used:4.5G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-2-2-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805099
  * datadisk:4957
  * volume_size:49G
  * volume_used:4.9G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-2-3-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805450
  * datadisk:5527
  * volume_size:49G
  * volume_used:5.4G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725
* mariadb-1-2-4-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:805501
  * datadisk:5920
  * volume_size:49G
  * volume_used:5.8G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794141725

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MariaDB-1

### Data Parameters of Reused Volumes
* MariaDB-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794141725-6f59c979cd-6wkf9: 0
* bexhoma-sut-mariadb-1-1794141725-5dccfc64c5-v468k: 0

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

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1 |                1 |   16 |       75.00 |           5.00 |            0.00 |         65.00 |            5.00 |              0 |           8 |             | None           |             0 | False         |              768.00 | True                |
| MariaDB-1-2 |                2 |   16 |       75.00 |           5.00 |            0.00 |         65.00 |            5.00 |              0 |           8 |             | None           |             0 | False         |              768.00 | True                |

### Benchmarking

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:------------------|:--------------|:----------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| mariadb-1-1-1-1-1 | mariadb-1-1-1 | mariadb-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 113682 | 264347 |         0.00 |          2 |        0 |
| mariadb-1-1-2-1-1 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |       16 |        2 |               1 |       1 | 151453 | 352201 |         0.00 |          2 |        0 |
| mariadb-1-1-2-1-2 | mariadb-1-1-2 | mariadb-1-1-2-1 |                1 |       16 |        2 |               1 |       2 | 151446 | 352161 |         0.00 |          2 |        0 |
| mariadb-1-1-3-1-1 | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        8 |        3 |               1 |       1 | 110665 | 256934 |         0.00 |          2 |        0 |
| mariadb-1-1-3-1-2 | mariadb-1-1-3 | mariadb-1-1-3-1 |                1 |        8 |        3 |               1 |       2 | 110701 | 257077 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-1 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        8 |        4 |               1 |       1 | 141212 | 327672 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-2 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        8 |        4 |               1 |       2 | 141272 | 327803 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-3 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        8 |        4 |               1 |       3 | 141356 | 327980 |         0.00 |          2 |        0 |
| mariadb-1-1-4-1-4 | mariadb-1-1-4 | mariadb-1-1-4-1 |                1 |        8 |        4 |               1 |       4 | 141259 | 327792 |         0.00 |          2 |        0 |
| mariadb-1-2-1-1-1 | mariadb-1-2-1 | mariadb-1-2-1-1 |                2 |       16 |        1 |               1 |       1 | 106493 | 247611 |         0.00 |          2 |        0 |
| mariadb-1-2-2-1-1 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |       16 |        2 |               1 |       1 | 142715 | 331550 |         0.00 |          2 |        0 |
| mariadb-1-2-2-1-2 | mariadb-1-2-2 | mariadb-1-2-2-1 |                2 |       16 |        2 |               1 |       2 | 142765 | 331663 |         0.00 |          2 |        0 |
| mariadb-1-2-3-1-1 | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        8 |        3 |               1 |       1 |  97647 | 226790 |         0.00 |          2 |        0 |
| mariadb-1-2-3-1-2 | mariadb-1-2-3 | mariadb-1-2-3-1 |                2 |        8 |        3 |               1 |       2 |  97463 | 226348 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-1 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        8 |        4 |               1 |       1 | 145887 | 338205 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-2 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        8 |        4 |               1 |       2 | 145894 | 338265 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-3 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        8 |        4 |               1 |       3 | 145934 | 338335 |         0.00 |          2 |        0 |
| mariadb-1-2-4-1-4 | mariadb-1-2-4 | mariadb-1-2-4-1 |                2 |        8 |        4 |               1 |       4 | 145907 | 338220 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |      NOPM |       TPM |   duration |   errors |
|:--------------|:--------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|----------:|----------:|-----------:|---------:|
| mariadb-1-1-1 | mariadb-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 113682.00 | 264347.00 |          2 |        0 |
| mariadb-1-1-2 | mariadb-1-1-2 |                1 |       32 |        2 |               1 |           2 |         0.00 | 151449.50 | 352181.00 |          2 |        0 |
| mariadb-1-1-3 | mariadb-1-1-3 |                1 |       16 |        3 |               1 |           2 |         0.00 | 110683.00 | 257005.50 |          2 |        0 |
| mariadb-1-1-4 | mariadb-1-1-4 |                1 |       32 |        4 |               1 |           4 |         0.00 | 141274.75 | 327811.75 |          2 |        0 |
| mariadb-1-2-1 | mariadb-1-2-1 |                2 |       16 |        1 |               1 |           1 |         0.00 | 106493.00 | 247611.00 |          2 |        0 |
| mariadb-1-2-2 | mariadb-1-2-2 |                2 |       32 |        2 |               1 |           2 |         0.00 | 142740.00 | 331606.50 |          2 |        0 |
| mariadb-1-2-3 | mariadb-1-2-3 |                2 |       16 |        3 |               1 |           2 |         0.00 |  97555.00 | 226569.00 |          2 |        0 |
| mariadb-1-2-4 | mariadb-1-2-4 |                2 |       32 |        4 |               1 |           4 |         0.00 | 145905.50 | 338256.25 |          2 |        0 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       847.64 |      4.12 |           3.30 |                  3.30 |
| mariadb-1-1-2-1 |      1604.73 |      6.94 |           4.02 |                  4.02 |
| mariadb-1-1-3-1 |      1005.82 |      4.40 |           4.44 |                  4.44 |
| mariadb-1-1-4-1 |      1621.55 |      6.82 |           5.04 |                  5.05 |
| mariadb-1-2-1-1 |      1007.64 |      4.79 |           5.33 |                  5.34 |
| mariadb-1-2-2-1 |      1499.75 |      7.17 |           5.95 |                  5.95 |
| mariadb-1-2-3-1 |      1035.64 |      4.65 |           6.37 |                  6.37 |
| mariadb-1-2-4-1 |      1575.98 |      7.46 |           6.91 |                  6.91 |

### Benchmarking phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| mariadb-1-1-1-1 |       360.85 |      1.60 |           0.08 |                  0.08 |
| mariadb-1-1-2-1 |       459.24 |      2.13 |           0.08 |                  0.08 |
| mariadb-1-1-3-1 |       363.96 |      1.59 |           0.05 |                  0.05 |
| mariadb-1-1-4-1 |       435.64 |      1.97 |           0.05 |                  0.05 |
| mariadb-1-2-1-1 |       346.55 |      1.69 |           0.08 |                  0.08 |
| mariadb-1-2-2-1 |       398.65 |      1.80 |           0.08 |                  0.08 |
| mariadb-1-2-3-1 |       358.84 |      1.68 |           0.05 |                  0.05 |
| mariadb-1-2-4-1 |       460.80 |      2.03 |           0.05 |                  0.05 |

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
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
