## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 1178s 
* Code: 1794855113
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
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.
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
  * disk:1268627
  * datadisk:33226
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
    * code:1794855113
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* mysql-1-1-2-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1269829
  * datadisk:33238
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
    * code:1794855113
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False

### Ingestion
* MySQL-1: 2 of 2 units ok

### SUT Container Restarts
* bexhoma-sut-mysql-1-1794855113-5cf97887c9-7ffw5: 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                        |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads |   Throughput [SF/h] | loading_inherited   |
|:-----------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|--------------------:|:--------------------|
| 1794855113-MySQL-1-1-0 |                1 | database       | False         |             2 |           0 |    1 |       20.00 |           3.00 |            0.00 |         20.00 |            3.00 |              2 |         1 |              180.00 | False               |
| 1794855113-MySQL-1-1-1 |                1 | database       | False         |             2 |           1 |    1 |       19.00 |           3.00 |            0.00 |         19.00 |            3.00 |              2 |         1 |              189.47 | False               |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-1-1 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.44 |                        0.44 |        91.68 |                                                      54946.00 |                                              21145.00 |
| mysql-1-1-1-1-2 | mysql-1-1-1 | mysql-1-1-1-1 |                1 |        1 |               1 |       2 |        10 |     1024 |           1 | 300.00 |        0 |                           0.46 |                        0.45 |        94.48 |                                                      44942.00 |                                              19190.00 |
| mysql-1-1-2-1-1 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.53 |                        0.53 |       110.58 |                                                      85011.00 |                                              30320.00 |
| mysql-1-1-2-1-2 | mysql-1-1-2 | mysql-1-1-2-1 |                1 |        2 |               1 |       2 |        10 |     1024 |           1 | 300.00 |        0 |                           0.49 |                        0.49 |       103.58 |                                                      69356.00 |                                              26579.00 |

#### Per Phase

| DBMS          | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   tenant_id |   time |   errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|------------:|-------:|---------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| mysql-1-1-1-0 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.44 |                        0.44 |        91.68 |                                                      54946.00 |                                              21145.00 |
| mysql-1-1-1-1 | mysql-1-1-1 |                1 |        1 |               1 |           1 |        10 |     1024 |           1 | 300.00 |        0 |                           0.46 |                        0.45 |        94.48 |                                                      44942.00 |                                              19190.00 |
| mysql-1-1-2-0 | mysql-1-1-2 |                1 |        2 |               1 |           1 |        10 |     1024 |           0 | 300.00 |        0 |                           0.53 |                        0.53 |       110.58 |                                                      85011.00 |                                              30320.00 |
| mysql-1-1-2-1 | mysql-1-1-2 |                1 |        2 |               1 |           1 |        10 |     1024 |           1 | 300.00 |        0 |                           0.49 |                        0.49 |       103.58 |                                                      69356.00 |                                              26579.00 |

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
