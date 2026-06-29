## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1347s 
* Code: 1782626077
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.2.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database uses ephemeral storage of size 16Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:1077381271552
  * Cores:256
  * host:6.8.0-111-generic
  * node:cl-worker27
  * disk:1407972
  * cpu_list:0-255
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782626077

### SUT Container Restarts
* bexhoma-sut-mysql-1-1782626077-58dcb6d95-bkq4d: 0 0

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   16 |      257.00 |          14.00 |            0.00 |         85.00 |          158.00 |              1 |           8 |             | None           |             0 | False         |              224.12 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:----------------|:------------|:--------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 181106 | 421095 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |      NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|----------:|----------:|-----------:|---------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 181106.00 | 421095.00 |          5 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
