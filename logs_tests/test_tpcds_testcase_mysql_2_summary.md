## Show Summary

### Workload
TPC-DS Queries SF=10
* Type: tpcds
* Duration: 683s 
* Code: 1782321594
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database uses ephemeral storage of size 10Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:297170
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782321594

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   10 |      373.00 |           1.00 |            1.00 |        129.00 |          236.00 |              8 |           0 |             | None           |             0 | False         |               96.51 |

### Execution

#### Per Connection


#### Per Phase



### Latency of Timer Execution [ms]

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       703.91 |     10.56 |          15.38 |                 16.00 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.31 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        17.43 |      0.13 |           0.01 |                  0.80 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.00 |      7.33 |          15.38 |                 16.00 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
* TEST failed: Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]
* TEST failed: Geo Times [s] contains 0 or NaN
* TEST failed: Power@Size [~Q/h] contains 0 or NaN
* TEST failed: Throughput@Size contains 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
