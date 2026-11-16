## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 1031s 
* Code: 1794767516
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
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091500
  * datadisk:38374
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767516
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091501
  * datadisk:38374
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767516
* mysql-1-1-3-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091502
  * datadisk:38374
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767516
* mysql-1-1-4-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1091504
  * datadisk:38374
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794767516

### Ingestion
* MySQL-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794767516-676b47d8b7-tx4nd: 0

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

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| mysql-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7919.91 |                47349.00 |            375000.00 |                              7763.00 | 3.00 |              228.09 |
| mysql-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7949.46 |                47173.00 |            375000.00 |                              7631.00 | 3.00 |              228.94 |
| mysql-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7998.29 |                46885.00 |            375000.00 |                              8147.00 | 3.00 |              230.35 |
| mysql-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7961.45 |                47102.00 |            375000.00 |                              7739.00 | 3.00 |              229.29 |
| mysql-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7965.50 |                47078.00 |            375000.00 |                              7803.00 | 3.00 |              229.41 |
| mysql-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7960.43 |                47108.00 |            375000.00 |                              7751.00 | 3.00 |              229.26 |
| mysql-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7977.70 |                47006.00 |            375000.00 |                              7671.00 | 3.00 |              229.76 |
| mysql-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         7979.91 |                46993.00 |            375000.00 |                              7747.00 | 3.00 |              229.82 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 3.00 |              228.09 |                        63712.67 |                47349.00 |           3000000.00 |                              7781.50 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    32768 |        0 |                        32109.26 |                93431.00 |            1500261 |                             725.00 |              1499739 |                              4223.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |         8 |     4096 |        0 |                         4038.51 |                92856.00 |             187467 |                             795.00 |               187533 |                              4435.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |         8 |     4096 |        0 |                         4034.90 |                92939.00 |             187710 |                             884.00 |               187290 |                              4467.00 |
| mysql-1-1-2-1-3 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       3 |         8 |     4096 |        0 |                         4038.51 |                92856.00 |             188040 |                             817.00 |               186960 |                              4435.00 |
| mysql-1-1-2-1-4 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       4 |         8 |     4096 |        0 |                         4039.69 |                92829.00 |             187682 |                             778.00 |               187318 |                              4391.00 |
| mysql-1-1-2-1-5 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       5 |         8 |     4096 |        0 |                         4053.62 |                92510.00 |             187428 |                             774.00 |               187572 |                              4427.00 |
| mysql-1-1-2-1-6 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       6 |         8 |     4096 |        0 |                         4038.69 |                92852.00 |             187551 |                             809.00 |               187449 |                              4455.00 |
| mysql-1-1-2-1-7 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       7 |         8 |     4096 |        0 |                         4046.57 |                92671.00 |             187704 |                             768.00 |               187296 |                              4411.00 |
| mysql-1-1-2-1-8 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       8 |         8 |     4096 |        0 |                         4049.11 |                92613.00 |             187978 |                             794.00 |               187022 |                              4387.00 |
| mysql-1-1-3-1-1 | mysql-1-1-3 | mysql-1-1-3-1 |                1 |        3 |               1 |       1 |        64 |    49152 |        0 |                        45293.27 |                66235.00 |            1499362 |                             652.00 |              1500638 |                              4863.00 |
| mysql-1-1-4-1-1 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       1 |         8 |     6144 |        0 |                         5968.96 |                62825.00 |             187720 |                             738.00 |               187280 |                              4061.00 |
| mysql-1-1-4-1-2 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       2 |         8 |     6144 |        0 |                         5977.14 |                62739.00 |             187527 |                             804.00 |               187473 |                              4073.00 |
| mysql-1-1-4-1-3 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       3 |         8 |     6144 |        0 |                         5953.42 |                62989.00 |             187287 |                             803.00 |               187713 |                              4091.00 |
| mysql-1-1-4-1-4 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       4 |         8 |     6144 |        0 |                         5997.70 |                62524.00 |             187349 |                             838.00 |               187651 |                              4127.00 |
| mysql-1-1-4-1-5 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       5 |         8 |     6144 |        0 |                         5995.40 |                62548.00 |             187883 |                             801.00 |               187117 |                              4069.00 |
| mysql-1-1-4-1-6 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       6 |         8 |     6144 |        0 |                         5988.02 |                62625.00 |             187154 |                             821.00 |               187846 |                              4119.00 |
| mysql-1-1-4-1-7 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       7 |         8 |     6144 |        0 |                         5975.81 |                62753.00 |             187401 |                             771.00 |               187599 |                              4099.00 |
| mysql-1-1-4-1-8 | mysql-1-1-4 | mysql-1-1-4-1 |                1 |        4 |               1 |       8 |         8 |     6144 |        0 |                         6004.90 |                62449.00 |             187224 |                             792.00 |               187776 |                              4063.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| mysql-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        64 |    32768 |        0 |                        32109.26 |                93431.00 |            1500261 |                             725.00 |              1499739 |                              4223.00 |
| mysql-1-1-2 | mysql-1-1-2 |                1 |        2 |               1 |           8 |        64 |    32768 |        0 |                        32339.59 |                92939.00 |            1501560 |                             884.00 |              1498440 |                              4467.00 |
| mysql-1-1-3 | mysql-1-1-3 |                1 |        3 |               1 |           1 |        64 |    49152 |        0 |                        45293.27 |                66235.00 |            1499362 |                             652.00 |              1500638 |                              4863.00 |
| mysql-1-1-4 | mysql-1-1-4 |                1 |        4 |               1 |           8 |        64 |    49152 |        0 |                        47861.35 |                62989.00 |            1499545 |                             838.00 |              1500455 |                              4127.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       483.22 |      9.87 |           8.92 |                 14.62 |
| mysql-1-1-2-1 |       483.22 |      9.87 |           8.92 |                 14.62 |
| mysql-1-1-3-1 |       483.22 |      9.87 |           8.92 |                 14.62 |
| mysql-1-1-4-1 |       483.22 |      9.87 |           8.92 |                 14.62 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       182.14 |      0.00 |           1.04 |                  1.05 |
| mysql-1-1-2-1 |       182.14 |      0.00 |           1.04 |                  1.05 |
| mysql-1-1-3-1 |       182.14 |      0.00 |           1.04 |                  1.05 |
| mysql-1-1-4-1 |       182.14 |      0.00 |           1.04 |                  1.05 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       408.66 |      6.15 |           8.06 |                 14.30 |
| mysql-1-1-2-1 |       421.50 |      6.52 |           8.09 |                 15.09 |
| mysql-1-1-3-1 |       282.09 |      5.22 |           8.12 |                 15.97 |
| mysql-1-1-4-1 |       308.63 |      6.09 |           8.15 |                 16.78 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| mysql-1-1-1-1 |       297.62 |      6.46 |           0.90 |                  0.90 |
| mysql-1-1-2-1 |       522.89 |      8.82 |           0.32 |                  0.32 |
| mysql-1-1-3-1 |       304.00 |      4.92 |           1.31 |                  1.31 |
| mysql-1-1-4-1 |       346.66 |      6.84 |           0.30 |                  0.31 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection mysql-1-1-1-1 (bexhoma-metrics-mysql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
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
| mysql-1-1-1-1 |                                  1.00 |                         15500.86 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                         15500.86 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-3-1 |                                  1.00 |                         15500.86 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-4-1 |                                  1.00 |                         15500.86 |                            0.04 |                            0.00 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio [0..1] |   Queries Per Second [queries/s] |   Connection Usage Ratio [0..1] |   Slow Queries Rate [queries/s] |   InnoDB Log Waits Rate [waits/s] |
|:--------------|--------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|----------------------------------:|
| mysql-1-1-1-1 |                                  1.00 |                         18544.15 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-2-1 |                                  1.00 |                         20979.49 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-3-1 |                                  1.00 |                         22226.56 |                            0.04 |                            0.00 |                              0.00 |
| mysql-1-1-4-1 |                                  1.00 |                         22519.92 |                            0.04 |                            0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
