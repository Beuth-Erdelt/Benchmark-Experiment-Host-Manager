## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 2044s 
* Code: 1792326913
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 3000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [2, 3].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size'}, '32G')].
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:860668
  * volume_size:1.8T
  * volume_used:841G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792326913
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:860671
  * volume_size:1.8T
  * volume_used:841G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792326913
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:801738
  * volume_size:1.8T
  * volume_used:783G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792326913
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:860678
  * volume_size:1.8T
  * volume_used:841G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1792326913

### SUT Container Restarts
* bexhoma-sut-mysql-1-1792326913-6f7877696f-9qkjh: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: ycsb (8 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: ycsb (8 pods)
* DBMS MySQL-1 - Experiment 1 Client 3: ycsb (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 4: ycsb (8 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8002.39 |                46861.00 |            375000.00 |                              8155.00 | 3.00 |              230.47 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8020.88 |                46753.00 |            375000.00 |                              8039.00 | 3.00 |              231.00 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8008.71 |                46824.00 |            375000.00 |                              7967.00 | 3.00 |              230.65 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7997.61 |                46889.00 |            375000.00 |                              8055.00 | 3.00 |              230.33 |
| mysql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8031.01 |                46694.00 |            375000.00 |                              8079.00 | 3.00 |              231.29 |
| mysql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7994.88 |                46905.00 |            375000.00 |                              7967.00 | 3.00 |              230.25 |
| mysql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7988.07 |                46945.00 |            375000.00 |                              7987.00 | 3.00 |              230.06 |
| mysql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8018.82 |                46765.00 |            375000.00 |                              8063.00 | 3.00 |              230.94 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 3.00 |              230.06 |                        64062.37 |                46945.00 |           3000000.00 |                              8039.00 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 | MySQL-1         |                1 |        1 |               1 |       1 |        64 |    32768 |           1 |            0 |                        32140.56 |                93340.00 |            1500802 |                             661.00 |              1499198 |                               631.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       1 |         8 |     4096 |           8 |            0 |                         4048.15 |                92635.00 |             187475 |                             707.00 |               187525 |                               653.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       2 |         8 |     4096 |           8 |            0 |                         4055.63 |                92464.00 |             187746 |                             746.00 |               187254 |                               692.00 |
| mysql-1-1-2-1-3 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       3 |         8 |     4096 |           8 |            0 |                         4060.77 |                92347.00 |             187439 |                             737.00 |               187561 |                               677.00 |
| mysql-1-1-2-1-4 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       4 |         8 |     4096 |           8 |            0 |                         4051.38 |                92561.00 |             187657 |                             644.00 |               187343 |                               592.00 |
| mysql-1-1-2-1-5 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       5 |         8 |     4096 |           8 |            0 |                         4051.86 |                92550.00 |             187108 |                             646.00 |               187892 |                               583.00 |
| mysql-1-1-2-1-6 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       6 |         8 |     4096 |           8 |            0 |                         4048.15 |                92635.00 |             187507 |                             701.00 |               187493 |                               654.00 |
| mysql-1-1-2-1-7 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       7 |         8 |     4096 |           8 |            0 |                         4048.93 |                92617.00 |             187395 |                             661.00 |               187605 |                               606.00 |
| mysql-1-1-2-1-8 | mysql-1-1-2 | mysql-1-1-2-1 | MySQL-1         |                1 |        2 |               1 |       8 |         8 |     4096 |           8 |            0 |                         4052.65 |                92532.00 |             187489 |                             643.00 |               187511 |                               587.00 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 | MySQL-1         |                1 |        3 |               1 |       1 |        64 |    49152 |           1 |            0 |                        47409.84 |                63278.00 |            1499277 |                             859.00 |              1500723 |                               954.00 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       1 |         8 |     6144 |           8 |            0 |                         6039.33 |                62093.00 |             187778 |                             667.00 |               187222 |                               594.00 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       2 |         8 |     6144 |           8 |            0 |                         6054.64 |                61936.00 |             187583 |                             736.00 |               187417 |                               657.00 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       3 |         8 |     6144 |           8 |            0 |                         6063.84 |                61842.00 |             187048 |                             754.00 |               187952 |                               667.00 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       4 |         8 |     6144 |           8 |            0 |                         6033.30 |                62155.00 |             187471 |                             760.00 |               187529 |                               690.00 |
| mysql-1-1-4-1-5 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       5 |         8 |     6144 |           8 |            0 |                         6055.03 |                61932.00 |             187619 |                             736.00 |               187381 |                               655.00 |
| mysql-1-1-4-1-6 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       6 |         8 |     6144 |           8 |            0 |                         6033.40 |                62154.00 |             187654 |                             670.00 |               187346 |                               595.00 |
| mysql-1-1-4-1-7 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       7 |         8 |     6144 |           8 |            0 |                         6048.78 |                61996.00 |             187414 |                             711.00 |               187586 |                               633.00 |
| mysql-1-1-4-1-8 | mysql-1-1-4 | mysql-1-1-4-1 | MySQL-1         |                1 |        4 |               1 |       8 |         8 |     6144 |           8 |            0 |                         6056.01 |                61922.00 |             187413 |                             771.00 |               187587 |                               677.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        64 |    32768 |               1 |           1 |            0 |                        32140.56 |                93340.00 |            1500802 |                             661.00 |              1499198 |                               631.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        64 |    32768 |               1 |           8 |            0 |                        32417.53 |                92635.00 |            1499816 |                             746.00 |              1500184 |                               692.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        64 |    49152 |               1 |           1 |            0 |                        47409.84 |                63278.00 |            1499277 |                             859.00 |              1500723 |                               954.00 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        64 |    49152 |               1 |           8 |            0 |                        48384.32 |                62155.00 |            1499980 |                             771.00 |              1500020 |                               690.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       379.19 |      8.50 |           8.82 |                 14.52 |
| mysql-1-1-2-1 |       379.19 |      8.50 |           8.82 |                 14.52 |
| mysql-1-1-3-1 |       379.19 |      8.50 |           8.82 |                 14.52 |
| mysql-1-1-4-1 |       379.19 |      8.50 |           8.82 |                 14.52 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       370.08 |     11.52 |           1.05 |                  1.05 |
| mysql-1-1-2-1 |       370.08 |     11.52 |           1.05 |                  1.05 |
| mysql-1-1-3-1 |       370.08 |     11.52 |           1.05 |                  1.05 |
| mysql-1-1-4-1 |       370.08 |     11.52 |           1.05 |                  1.05 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       270.75 |      3.89 |           7.95 |                 14.22 |
| mysql-1-1-2-1 |       298.68 |      3.84 |           8.00 |                 15.10 |
| mysql-1-1-3-1 |       261.91 |      5.18 |           8.04 |                 15.87 |
| mysql-1-1-4-1 |       239.05 |      4.88 |           8.08 |                 16.64 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       303.82 |      3.12 |           1.39 |                  1.40 |
| mysql-1-1-2-1 |       282.42 |      6.28 |           1.39 |                  1.40 |
| mysql-1-1-3-1 |       229.11 |      8.40 |           1.37 |                  1.38 |
| mysql-1-1-4-1 |       331.08 |      8.14 |           1.37 |                  1.38 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loading.log, expected: series exists only while non-zero)
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

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                         12460.07 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                         12460.07 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-3-1 |                                  1.00 |                         12460.07 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-4-1 |                                  1.00 |                         12460.07 |                            0.04 |                            0.00 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                          9908.63 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                          8558.24 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-3-1 |                                  1.00 |                          7206.84 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-4-1 |                                  1.00 |                          9368.60 |                            0.04 |                            0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
