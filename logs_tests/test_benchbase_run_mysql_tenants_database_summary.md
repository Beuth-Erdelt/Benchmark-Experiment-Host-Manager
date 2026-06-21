## Show Summary

### Workload
Benchbase Workload tpcc SF=1
* Type: benchbase
* Duration: 1689s 
* Code: 1781986123
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 1. Target is based on multiples of '1024'. Factors for benchmarking are [1]. Benchmarking has keying and thinking times activated. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.17.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type cephcsi and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [10] threads, split into [1] pods.
  * Benchmarking is run as [2, 2] times the number of benchmarking pods.
  * Number of tenants is 2, one database per tenant.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214906
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781986123
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False
* MySQL-1-1-2-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:214906
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1781986123
    * TENANT_BY:database
    * TENANT_NUM:2
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (2 pods)
* DBMS MySQL-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|                        |   experiment_run | type_tenants   | vol_tenants   |   num_tenants |   tenant_id |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals |   Throughput [SF/h] |
|:-----------------------|-----------------:|:---------------|:--------------|--------------:|------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|--------------------:|
| 1781986123-MySQL-1-1-0 |                1 | database       | False         |             2 |           0 |    1 |      305.00 |           3.00 |            0.00 |        305.00 |          340.00 |              2 |           1 |               11.80 |
| 1781986123-MySQL-1-1-1 |                1 | database       | False         |             2 |           1 |    1 |      304.00 |           3.00 |            0.00 |        304.00 |          340.00 |              2 |           1 |               11.84 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       1 |           0 | 300.00 |            0 |                           0.52 |                        0.52 |       109.18 |                                                     143480.00 |                                              51822.00 |
| MySQL-1-1-1-1-2 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |          10 |     1024 |        1 |               1 |       2 |           1 | 300.00 |            0 |                           0.46 |                        0.45 |        95.18 |                                                     124306.00 |                                              50234.00 |
| MySQL-1-1-2-1-1 | MySQL-1-1-2 | MySQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       1 |           0 | 300.00 |            0 |                           0.45 |                        0.45 |        94.48 |                                                     277352.00 |                                              85770.00 |
| MySQL-1-1-2-1-2 | MySQL-1-1-2 | MySQL-1-1-2-1 |                1 |          10 |     1024 |        2 |               1 |       2 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        95.88 |                                                     188749.00 |                                              83242.00 |

#### Per Phase

| DBMS          | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1-0 | MySQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.52 |                        0.52 |       109.18 |                                                     143480.00 |                                              51822.00 |
| MySQL-1-1-1-1 | MySQL-1-1-1 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.46 |                        0.45 |        95.18 |                                                     124306.00 |                                              50234.00 |
| MySQL-1-1-2-0 | MySQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           0 | 300.00 |            0 |                           0.45 |                        0.45 |        94.48 |                                                     277352.00 |                                              85770.00 |
| MySQL-1-1-2-1 | MySQL-1-1-2 |                1 |          10 |     1024 |               1 |           1 |           1 | 300.00 |            0 |                           0.46 |                        0.46 |        95.88 |                                                     188749.00 |                                              83242.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
