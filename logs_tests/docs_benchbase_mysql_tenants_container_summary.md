## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 1154s 
* Code: 1794856299
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [1, 1] times the number of benchmarking pods.
  * Number of tenants is 2, one container per tenant.
  * Experiment is run once.
  * Deployment parameter overrides: [({'kind': 'deployment', 'workload': 'bexhoma-deployment-mysql', 'config': '', 'container': 'dbms', 'param': 'innodb_buffer_pool_size', 'target': 'container'}, '32G')].
  * Distributed DBMS uses 1 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* mysql-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1278232
  * datadisk:33062
  * volume_size:49G
  * volume_used:33G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794856299
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1283036
  * datadisk:33066
  * volume_size:49G
  * volume_used:33G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794856299
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
* mysql-2-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1278232
  * datadisk:33062
  * volume_size:49G
  * volume_used:33G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794856299
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1
* mysql-2-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1283036
  * datadisk:33066
  * volume_size:49G
  * volume_used:33G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=32G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794856299
    * TENANT_BY:container
    * TENANT_NUM:2
    * TENANT_VOL:False
    * TENANT:1

### Ingestion
* MySQL-1: 1 of 1 units ok
* MySQL-2: 1 of 1 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794856299-5994b855cd-lpr86: 0
* bexhoma-sut-mysql-2-1794856299-79cc88f47f-snndn: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 2: benchbase (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MySQL-2 - Experiment 1 Client 2: benchbase (1 pods)

### Loading

#### Per Run

|                        |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads |   Throughput [SF/h] | loading_inherited   |
|:-----------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|--------------------:|:--------------------|
| 1794856299-MySQL-1-1-0 |                1 | container      | False         |             2 |           0 |    1 |       56.00 |           2.00 |            0.00 |         52.00 |            2.00 |              1 |         1 |               64.29 | False               |
| 1794856299-MySQL-2-1-1 |                1 | container      | False         |             2 |           1 |    1 |       55.00 |           2.00 |            0.00 |         51.00 |            2.00 |              1 |         1 |               65.45 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        10 |     1024 |          -1 | 300.00 |        0 |                           0.44 |                        0.44 |        93.08 |                                                      88294.00 |                                              31700.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |        10 |     1024 |          -1 | 300.00 |        0 |                           0.51 |                        0.50 |       105.68 |                                                      46235.00 |                                              16861.00 |
| mysql-2-1-1-1-1 | mysql-2-1-1 | mysql-2-1-1-1 |                1 |        1 |               1 |       1 |        10 |     1024 |          -1 | 300.00 |        0 |                           0.49 |                        0.49 |       102.88 |                                                      89744.00 |                                              27759.00 |
| mysql-2-1-2-1-1 | mysql-2-1-2 | mysql-2-1-2-1 |                1 |        2 |               1 |       1 |        10 |     1024 |          -1 | 300.00 |        0 |                           0.53 |                        0.53 |       111.28 |                                                      40786.00 |                                              15816.00 |

#### Per Phase

| DBMS           | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1--1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        10 |     1024 |          -1 | 300.00 |        0 |                           0.44 |                        0.44 |        93.08 |                                                      88294.00 |                                              31700.00 |
| mysql-1-1-2--1 | mysql-1-1-2 |                1 |        2 |               1 |           1 |        10 |     1024 |          -1 | 300.00 |        0 |                           0.51 |                        0.50 |       105.68 |                                                      46235.00 |                                              16861.00 |
| mysql-2-1-1--1 | mysql-2-1-1 |                1 |        1 |               1 |           1 |        10 |     1024 |          -1 | 300.00 |        0 |                           0.49 |                        0.49 |       102.88 |                                                      89744.00 |                                              27759.00 |
| mysql-2-1-2--1 | mysql-2-1-2 |                1 |        2 |               1 |           1 |        10 |     1024 |          -1 | 300.00 |        0 |                           0.53 |                        0.53 |       111.28 |                                                      40786.00 |                                              15816.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: efficiency contains no 0 or NaN
* TEST passed: Workflow as planned
