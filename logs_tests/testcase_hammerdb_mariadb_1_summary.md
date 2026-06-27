## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 885s 
* Code: 1780052904
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:59776
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780052904

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1]]

#### Planned

* DBMS MariaDB-1 - Pods [[1]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      190.00 |           1.00 |            0.00 |         80.00 |          109.00 |              1 |           8 |          | None           |             0 | False         |              303.16 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   vusers |   client |   child |   NOPM |    TPM |   efficiency |   duration |   errors |
|:----------------|-----------------:|---------:|---------:|--------:|-------:|-------:|-------------:|-----------:|---------:|
| MariaDB-1-1-1-1 |                1 |       16 |        1 |       1 |  63390 | 147366 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS          |   experiment_run |   vusers |   client |   pod_count |   efficiency |     NOPM |       TPM |   duration |   errors |
|:--------------|-----------------:|---------:|---------:|------------:|-------------:|---------:|----------:|-----------:|---------:|
| MariaDB-1-1-1 |             1.00 |    16.00 |     1.00 |        1.00 |         0.00 | 63390.00 | 147366.00 |       5.00 |     0.00 |

### Tests
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
