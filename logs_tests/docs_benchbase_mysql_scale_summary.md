## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1984s 
* Code: 1794063742
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806436
  * datadisk:35509
  * volume_size:49G
  * volume_used:35G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806437
  * datadisk:36192
  * volume_size:49G
  * volume_used:36G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806437
  * datadisk:37564
  * volume_size:49G
  * volume_used:37G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806477
  * datadisk:38236
  * volume_size:49G
  * volume_used:38G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812183
  * datadisk:39605
  * volume_size:49G
  * volume_used:39G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812250
  * datadisk:40593
  * volume_size:49G
  * volume_used:40G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:812335
  * datadisk:41853
  * volume_size:49G
  * volume_used:41G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:806547
  * datadisk:42565
  * volume_size:49G
  * volume_used:42G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * eval_parameters
    * code:1794063742
    * TENANT_VOL:False

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794063742-d655899d5-jlltd: 0
* bexhoma-sut-mysql-1-1794063742-85c7c79b4d-kb2d2: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: benchbase (4 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS MySQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 2 Client 4: benchbase (4 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       85.00 |           5.00 |            0.00 |         75.00 |            5.00 |              0 |           1 |             |                |             0 | False         |              677.65 | True                |
| MySQL-1-2 |                2 |   16 |       85.00 |           5.00 |            0.00 |         75.00 |            5.00 |              0 |           1 |             |                |             0 | False         |              677.65 | True                |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 120.00 |            0 |                        8191.74 |                     8110.19 |         0.00 |                                                      16022.00 |                                               9500.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       1 |          -1 | 120.00 |            0 |                        8165.72 |                     8049.73 |         0.00 |                                                      30679.00 |                                              13936.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       2 |          -1 | 120.00 |            0 |                        8192.67 |                     8074.90 |         0.00 |                                                      30434.00 |                                              13718.00 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       1 |          -1 | 120.00 |            0 |                        4095.73 |                     4054.95 |         0.00 |                                                      16151.00 |                                               9066.00 |
| mysql-1-1-3-1-2 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       2 |          -1 | 120.00 |            0 |                        4095.76 |                     4055.55 |         0.00 |                                                      16225.00 |                                               9027.00 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       1 |          -1 | 120.00 |            0 |                        4000.13 |                     3937.68 |         0.00 |                                                      42761.00 |                                              19984.00 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       2 |          -1 | 120.00 |            0 |                        4075.22 |                     4010.99 |         0.00 |                                                      42496.00 |                                              19617.00 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       3 |          -1 | 120.00 |            0 |                        4029.27 |                     3965.83 |         0.00 |                                                      42724.00 |                                              19840.00 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       4 |          -1 | 120.00 |            0 |                        3999.28 |                     3935.51 |         0.00 |                                                      42789.00 |                                              19987.00 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |         160 |     8192 |        1 |               1 |       1 |          -1 | 120.00 |            0 |                        8191.11 |                     8101.74 |         0.00 |                                                      17712.00 |                                               9672.00 |
| mysql-1-2-2-1-1 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       1 |          -1 | 120.00 |            0 |                        7476.89 |                     7354.32 |         0.00 |                                                      47518.00 |                                              21347.00 |
| mysql-1-2-2-1-2 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       2 |          -1 | 120.00 |            0 |                        7581.75 |                     7456.69 |         0.00 |                                                      47093.00 |                                              21055.00 |
| mysql-1-2-3-1-1 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       1 |          -1 | 120.00 |            0 |                        4096.07 |                     4049.67 |         0.00 |                                                      17439.00 |                                               9137.00 |
| mysql-1-2-3-1-2 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       2 |          -1 | 120.00 |            0 |                        4095.65 |                     4050.10 |         0.00 |                                                      17505.00 |                                               9162.00 |
| mysql-1-2-4-1-1 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       1 |          -1 | 120.00 |            0 |                        4095.76 |                     4027.08 |         0.00 |                                                      38943.00 |                                              17006.00 |
| mysql-1-2-4-1-2 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       2 |          -1 | 120.00 |            0 |                        4095.73 |                     4027.20 |         0.00 |                                                      38823.00 |                                              16828.00 |
| mysql-1-2-4-1-3 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       3 |          -1 | 120.00 |            0 |                        4095.77 |                     4026.72 |         0.00 |                                                      38890.00 |                                              16925.00 |
| mysql-1-2-4-1-4 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       4 |          -1 | 120.00 |            0 |                        4096.30 |                     4028.72 |         0.00 |                                                      38907.00 |                                              17012.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 120.00 |            0 |                        8191.74 |                     8110.19 |         0.00 |                                                      16022.00 |                                               9500.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |         320 |    16384 |               1 |           2 |          -1 | 120.00 |            0 |                       16358.39 |                    16124.63 |         0.00 |                                                      30679.00 |                                              13827.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |         160 |     8192 |               1 |           2 |          -1 | 120.00 |            0 |                        8191.49 |                     8110.49 |         0.00 |                                                      16225.00 |                                               9046.50 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |         320 |    16384 |               1 |           4 |          -1 | 120.00 |            0 |                       16103.89 |                    15850.01 |         0.00 |                                                      42789.00 |                                              19857.00 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |         160 |     8192 |               1 |           1 |          -1 | 120.00 |            0 |                        8191.11 |                     8101.74 |         0.00 |                                                      17712.00 |                                               9672.00 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |         320 |    16384 |               1 |           2 |          -1 | 120.00 |            0 |                       15058.64 |                    14811.01 |         0.00 |                                                      47518.00 |                                              21201.00 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |         160 |     8192 |               1 |           2 |          -1 | 120.00 |            0 |                        8191.71 |                     8099.77 |         0.00 |                                                      17505.00 |                                               9149.50 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |         320 |    16384 |               1 |           4 |          -1 | 120.00 |            0 |                       16383.55 |                    16109.71 |         0.00 |                                                      38943.00 |                                              16942.75 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1443.99 |     13.53 |           5.85 |                  8.21 |
| mysql-1-1-2-1 |      2672.84 |     28.19 |           7.50 |                 13.92 |
| mysql-1-1-3-1 |      1273.62 |     12.89 |           8.43 |                 17.86 |
| mysql-1-1-4-1 |      2802.09 |     30.50 |           9.76 |                 23.43 |
| mysql-1-2-1-1 |      1652.65 |     15.40 |           7.59 |                 10.13 |
| mysql-1-2-2-1 |      3168.05 |     31.51 |           9.89 |                 16.74 |
| mysql-1-2-3-1 |      1677.23 |     14.59 |          10.91 |                 20.66 |
| mysql-1-2-4-1 |      3703.97 |     31.16 |          12.55 |                 27.14 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1205.44 |     12.28 |           1.43 |                  1.43 |
| mysql-1-1-2-1 |      1624.34 |     21.87 |           1.57 |                  1.57 |
| mysql-1-1-3-1 |      1097.18 |     15.53 |           1.31 |                  1.31 |
| mysql-1-1-4-1 |      2528.81 |     21.74 |           1.08 |                  1.08 |
| mysql-1-2-1-1 |      1239.97 |     12.45 |           1.87 |                  1.87 |
| mysql-1-2-2-1 |      2264.94 |     26.46 |           1.49 |                  1.49 |
| mysql-1-2-3-1 |      1370.28 |     12.73 |           1.09 |                  1.09 |
| mysql-1-2-4-1 |      2017.65 |     21.09 |           0.96 |                  0.96 |

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
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
