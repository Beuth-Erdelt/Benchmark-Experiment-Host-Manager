## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: hammerdb
* Duration: 3112s 
* Code: 1794699310
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
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
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1059097
  * datadisk:34995
  * volume_size:125G
  * volume_used:35G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794699310
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1044881
  * datadisk:35311
  * volume_size:125G
  * volume_used:35G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794699310
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045946
  * datadisk:35981
  * volume_size:125G
  * volume_used:36G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794699310
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046214
  * datadisk:36337
  * volume_size:125G
  * volume_used:36G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794699310
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1044921
  * datadisk:37051
  * volume_size:125G
  * volume_used:37G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794699310
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046272
  * datadisk:37387
  * volume_size:125G
  * volume_used:37G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794699310
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1047620
  * datadisk:38052
  * volume_size:125G
  * volume_used:38G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794699310
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1049357
  * datadisk:38400
  * volume_size:125G
  * volume_used:38G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794699310

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794699310-f958744c4-bg8zm: 0
* bexhoma-sut-mysql-1-1794699310-78d985c867-gj77k: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: hammerdb (4 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: hammerdb (4 pods)

### Loading

#### Per Run

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       65.00 |           5.00 |            0.00 |         55.00 |            5.00 |              0 |         8 |             | None           |             0 | False         |              886.15 | True                |
| MySQL-1-2 |                2 |   16 |       65.00 |           5.00 |            0.00 |         55.00 |            5.00 |              0 |         8 |             | None           |             0 | False         |              886.15 | True                |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   NOPM |    TPM |   efficiency |   duration |   errors |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|-------:|-------:|-------------:|-----------:|---------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        16 |  71608 | 166113 |         0.00 |          2 |        0 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |        16 | 147753 | 343876 |         0.00 |          2 |        0 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |        16 | 147497 | 343261 |         0.00 |          2 |        0 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       1 |         8 |  79662 | 184956 |         0.00 |          2 |        0 |
| mysql-1-1-3-1-2 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       2 |         8 |  79536 | 184715 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       1 |         8 | 159074 | 369350 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       2 |         8 | 158884 | 368910 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       3 |         8 | 158938 | 369042 |         0.00 |          2 |        0 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       4 |         8 | 159031 | 369241 |         0.00 |          2 |        0 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 |        16 |  76056 | 177175 |         0.00 |          2 |        0 |
| mysql-1-2-2-1-1 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       1 |        16 | 148324 | 344549 |         0.00 |          2 |        0 |
| mysql-1-2-2-1-2 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       2 |        16 | 148095 | 344007 |         0.00 |          2 |        0 |
| mysql-1-2-3-1-1 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       1 |         8 |  75656 | 175726 |         0.00 |          2 |        0 |
| mysql-1-2-3-1-2 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       2 |         8 |  75561 | 175466 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-1 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       1 |         8 | 153897 | 358167 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-2 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       2 |         8 | 154027 | 358495 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-3 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       3 |         8 | 153940 | 358268 |         0.00 |          2 |        0 |
| mysql-1-2-4-1-4 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       4 |         8 | 153984 | 358409 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|-------------:|----------:|----------:|-----------:|---------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        16 |         0.00 |  71608.00 | 166113.00 |          2 |        0 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 |        32 |         0.00 | 147625.00 | 343568.50 |          2 |        0 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        3 |               1 |           2 |        16 |         0.00 |  79599.00 | 184835.50 |          2 |        0 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        4 |               1 |           4 |        32 |         0.00 | 158981.75 | 369135.75 |          2 |        0 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 |        16 |         0.00 |  76056.00 | 177175.00 |          2 |        0 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |        2 |               1 |           2 |        32 |         0.00 | 148209.50 | 344278.00 |          2 |        0 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |        3 |               1 |           2 |        16 |         0.00 |  75608.50 | 175596.00 |          2 |        0 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |        4 |               1 |           4 |        32 |         0.00 | 153962.00 | 358334.75 |          2 |        0 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       681.13 |      3.03 |           4.71 |                  6.54 |
| mysql-1-1-2-1 |      1360.31 |      6.07 |           5.70 |                 11.43 |
| mysql-1-1-3-1 |       867.06 |      4.05 |           6.18 |                 13.98 |
| mysql-1-1-4-1 |      1580.98 |      7.19 |           6.92 |                 18.69 |
| mysql-1-2-1-1 |       855.74 |      3.88 |           5.39 |                  7.29 |
| mysql-1-2-2-1 |      1500.16 |      6.87 |           6.32 |                 12.03 |
| mysql-1-2-3-1 |       763.03 |      3.67 |           6.67 |                 14.25 |
| mysql-1-2-4-1 |      1608.32 |      7.47 |           7.43 |                 19.14 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       303.80 |      1.55 |           0.08 |                  0.08 |
| mysql-1-1-2-1 |       582.42 |      2.93 |           0.08 |                  0.08 |
| mysql-1-1-3-1 |       311.84 |      1.48 |           0.05 |                  0.05 |
| mysql-1-1-4-1 |       564.26 |      2.39 |           0.05 |                  0.05 |
| mysql-1-2-1-1 |       238.87 |      1.26 |           0.08 |                  0.08 |
| mysql-1-2-2-1 |       520.98 |      2.27 |           0.08 |                  0.08 |
| mysql-1-2-3-1 |       268.64 |      1.18 |           0.05 |                  0.05 |
| mysql-1-2-4-1 |       550.32 |      2.64 |           0.05 |                  0.05 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-2-1 (bexhoma-metrics-mysql-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-3-1 (bexhoma-metrics-mysql-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-4-1 (bexhoma-metrics-mysql-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-1-1 (bexhoma-metrics-mysql-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-2-1 (bexhoma-metrics-mysql-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-3-1 (bexhoma-metrics-mysql-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-2-4-1 (bexhoma-metrics-mysql-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: MySQL-1)
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
