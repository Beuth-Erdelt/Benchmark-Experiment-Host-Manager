## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2047s 
* Code: 1794695341
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
  * disk:1046889
  * datadisk:35512
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1049775
  * datadisk:36204
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1049931
  * datadisk:37576
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1045222
  * datadisk:38260
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-2-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1048100
  * datadisk:39568
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-2-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1048807
  * datadisk:40565
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-2-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1049406
  * datadisk:41825
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
    * code:1794695341
    * TENANT_VOL:False
* mysql-1-2-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1043976
  * datadisk:42521
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
    * code:1794695341
    * TENANT_VOL:False

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: MySQL-1

### Data Parameters of Reused Volumes
* MySQL-1: loading values of the volume: script=Schema, indexing=Checks

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794695341-6cf7f55896-67xn2: 0
* bexhoma-sut-mysql-1-1794695341-8568d65c57-44psq: 0

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

| DBMS      |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MySQL-1-1 |                1 |   16 |       81.00 |           4.00 |            0.00 |         72.00 |            5.00 |              0 |         1 |             |                |             0 | False         |              711.11 | True                |
| MySQL-1-2 |                2 |   16 |       81.00 |           4.00 |            0.00 |         72.00 |            5.00 |              0 |         1 |             |                |             0 | False         |              711.11 | True                |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        8192.15 |                     8106.06 |         0.00 |                                                      17513.00 |                                               9574.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        8176.36 |                     8054.58 |         0.00 |                                                      38179.00 |                                              16578.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |       160 |     8192 |          -1 | 120.00 |        0 |                        8191.60 |                     8067.66 |         0.00 |                                                      38157.00 |                                              16437.00 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        4095.82 |                     4051.65 |         0.00 |                                                      17601.00 |                                               8914.00 |
| mysql-1-1-3-1-2 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        4095.41 |                     4052.27 |         0.00 |                                                      17521.00 |                                               8873.00 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        3888.92 |                     3828.38 |         0.00 |                                                      44730.00 |                                              20557.00 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        3933.24 |                     3871.41 |         0.00 |                                                      44529.00 |                                              20327.00 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       3 |        80 |     4096 |          -1 | 120.00 |        0 |                        3912.59 |                     3851.14 |         0.00 |                                                      44578.00 |                                              20435.00 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       4 |        80 |     4096 |          -1 | 120.00 |        0 |                        3897.09 |                     3835.52 |         0.00 |                                                      44720.00 |                                              20515.00 |
| mysql-1-2-1-1-1 | mysql-1-2-1 | mysql-1-2-1-1 |                2 |        1 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        8191.84 |                     8095.09 |         0.00 |                                                      22259.00 |                                              11410.00 |
| mysql-1-2-2-1-1 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       1 |       160 |     8192 |          -1 | 120.00 |        0 |                        7456.47 |                     7331.72 |         0.00 |                                                      44388.00 |                                              21437.00 |
| mysql-1-2-2-1-2 | mysql-1-2-2 | mysql-1-2-2-1 |                2 |        2 |               1 |       2 |       160 |     8192 |          -1 | 120.00 |        0 |                        7606.34 |                     7477.68 |         0.00 |                                                      43846.00 |                                              21013.00 |
| mysql-1-2-3-1-1 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        4096.14 |                     4052.36 |         0.00 |                                                      17273.00 |                                               9066.00 |
| mysql-1-2-3-1-2 | mysql-1-2-3 | mysql-1-2-3-1 |                2 |        3 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        4095.81 |                     4050.75 |         0.00 |                                                      16957.00 |                                               8870.00 |
| mysql-1-2-4-1-1 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       1 |        80 |     4096 |          -1 | 120.00 |        0 |                        3992.49 |                     3925.28 |         0.00 |                                                      42551.00 |                                              20025.00 |
| mysql-1-2-4-1-2 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       2 |        80 |     4096 |          -1 | 120.00 |        0 |                        4042.53 |                     3974.39 |         0.00 |                                                      42220.00 |                                              19777.00 |
| mysql-1-2-4-1-3 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       3 |        80 |     4096 |          -1 | 120.00 |        0 |                        4001.26 |                     3934.53 |         0.00 |                                                      42475.00 |                                              19981.00 |
| mysql-1-2-4-1-4 | mysql-1-2-4 | mysql-1-2-4-1 |                2 |        4 |               1 |       4 |        80 |     4096 |          -1 | 120.00 |        0 |                        3992.10 |                     3924.74 |         0.00 |                                                      42533.00 |                                              20027.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |       160 |     8192 |          -1 | 120.00 |        0 |                        8192.15 |                     8106.06 |         0.00 |                                                      17513.00 |                                               9574.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           2 |       320 |    16384 |          -1 | 120.00 |        0 |                       16367.95 |                    16122.24 |         0.00 |                                                      38179.00 |                                              16507.50 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        3 |               1 |           2 |       160 |     8192 |          -1 | 120.00 |        0 |                        8191.23 |                     8103.93 |         0.00 |                                                      17601.00 |                                               8893.50 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        4 |               1 |           4 |       320 |    16384 |          -1 | 120.00 |        0 |                       15631.84 |                    15386.46 |         0.00 |                                                      44730.00 |                                              20458.50 |
| mysql-1-2-1 | mysql-1-2-1 |                2 |        1 |               1 |           1 |       160 |     8192 |          -1 | 120.00 |        0 |                        8191.84 |                     8095.09 |         0.00 |                                                      22259.00 |                                              11410.00 |
| mysql-1-2-2 | mysql-1-2-2 |                2 |        2 |               1 |           2 |       320 |    16384 |          -1 | 120.00 |        0 |                       15062.81 |                    14809.40 |         0.00 |                                                      44388.00 |                                              21225.00 |
| mysql-1-2-3 | mysql-1-2-3 |                2 |        3 |               1 |           2 |       160 |     8192 |          -1 | 120.00 |        0 |                        8191.95 |                     8103.11 |         0.00 |                                                      17273.00 |                                               8968.00 |
| mysql-1-2-4 | mysql-1-2-4 |                2 |        4 |               1 |           4 |       320 |    16384 |          -1 | 120.00 |        0 |                       16028.38 |                    15758.94 |         0.00 |                                                      42551.00 |                                              19952.50 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1605.82 |     16.03 |           5.80 |                  7.97 |
| mysql-1-1-2-1 |      3824.36 |     32.57 |           7.75 |                 15.08 |
| mysql-1-1-3-1 |      1404.63 |     14.93 |           8.38 |                 17.68 |
| mysql-1-1-4-1 |      3417.61 |     31.55 |           9.88 |                 23.96 |
| mysql-1-2-1-1 |      1990.19 |     16.91 |           7.66 |                 10.39 |
| mysql-1-2-2-1 |      3749.29 |     32.10 |          10.01 |                 17.25 |
| mysql-1-2-3-1 |      1702.90 |     14.53 |          10.88 |                 20.60 |
| mysql-1-2-4-1 |      3539.39 |     31.89 |          12.40 |                 26.55 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |      1433.26 |     13.95 |           1.41 |                  1.41 |
| mysql-1-1-2-1 |      2027.18 |     19.09 |           1.45 |                  1.45 |
| mysql-1-1-3-1 |      1440.33 |     12.66 |           1.16 |                  1.16 |
| mysql-1-1-4-1 |      2145.25 |     21.01 |           1.01 |                  1.01 |
| mysql-1-2-1-1 |      1403.71 |     12.75 |           1.38 |                  1.38 |
| mysql-1-2-2-1 |      1889.48 |     19.70 |           1.57 |                  1.57 |
| mysql-1-2-3-1 |      1051.35 |     11.44 |           1.26 |                  1.26 |
| mysql-1-2-4-1 |      1892.67 |     21.76 |           1.05 |                  1.05 |

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
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
