# Test Cases

There is a variety of combinations of options that can be tested.

We here list some more basic use cases to test the functionality of bexhoma.

See [repository](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/test.sh) for implementations.
You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):

```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

See also [more test cases](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/test-more.sh) for more and longer running test cases and other DBMS.

See the [log folder](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/logs_tests) for some demo test logs.
The folder also contains `\*_summary.txt` files containing only the result summary.


## TPC-H

### Compare

#### TPC-H Compare

```bash
bexhoma tpch \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_compare.log
```

yields (after ca. 120 minutes) something like

test_tpch_testcase_compare.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1432s 
* Code: 1782328952
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:261589
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782328952
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:231054
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782328952
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:261592
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782328952
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:232015
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782328952

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1    |                1 |    1 |      443.00 |           1.00 |           23.00 |         83.00 |          333.00 |              8 |           0 |             | None           |             0 | False         |                8.13 |
| MonetDB-1-1    |                1 |    1 |      234.00 |           2.00 |           18.00 |         31.00 |          181.00 |              8 |           0 |             | None           |             0 | False         |               15.38 |
| MySQL-1-1      |                1 |    1 |      301.00 |           2.00 |           21.00 |         28.00 |          246.00 |              8 |           0 |             | None           |             0 | False         |               11.96 |
| PostgreSQL-1-1 |                1 |    1 |      341.00 |           1.00 |           21.00 |         44.00 |          269.00 |              8 |           0 |             |                |             0 | False         |               10.56 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| MariaDB-1-1-1-1-1    | MariaDB-1       | MariaDB-1-1-1    | MariaDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |        112 |            1.12 |             3430.02 |            707.14 |          -1 | MariaDB-1-1-1-1-1    |
| MonetDB-1-1-1-1-1    | MonetDB-1       | MonetDB-1-1-1    | MonetDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |         84 |            0.11 |            39418.11 |            942.86 |          -1 | MonetDB-1-1-1-1-1    |
| MySQL-1-1-1-1-1      | MySQL-1         | MySQL-1-1-1      | MySQL-1-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               22 |         67 |            1.02 |             3685.84 |           1182.09 |          -1 | MySQL-1-1-1-1-1      |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         14 |            0.32 |            12056.34 |           5657.14 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1    | MariaDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |        112 |            1.12 |             3430.02 |            707.14 |          -1 |
| MonetDB-1-1-1    | MonetDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               22 |         84 |            0.11 |            39418.11 |            942.86 |          -1 |
| MySQL-1-1-1      | MySQL-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               22 |         67 |            1.02 |             3685.84 |           1182.09 |          -1 |
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         14 |            0.32 |            12056.34 |           5657.14 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |   MonetDB-1-1-1-1-1 |   MySQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|--------------------:|------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             8820.34 |              614.68 |           7905.24 |                1097.89 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              522.07 |               38.23 |            102.52 |                 249.21 |
| Shipping Priority (TPC-H Q3)                        |             1629.75 |               89.61 |           1370.22 |                 314.21 |
| Order Priority Checking Query (TPC-H Q4)            |              357.93 |              165.66 |            474.27 |                 153.04 |
| Local Supplier Volume (TPC-H Q5)                    |             1101.91 |               73.61 |           1014.53 |                 302.16 |
| Forecasting Revenue Change (TPC-H Q6)               |             1040.46 |               23.98 |           1167.47 |                 192.42 |
| Volume Shipping Query (TPC-H Q7)                    |             1132.46 |               51.69 |            814.53 |                 326.12 |
| National Market Share (TPC-H Q8)                    |             1935.03 |              348.10 |           2870.65 |                 191.40 |
| Product Type Profit Measure (TPC-H Q9)              |             2095.02 |               81.75 |           2291.24 |                 494.87 |
| Returned Item Reporting Query (TPC-H Q10)           |              896.21 |              128.73 |           1132.40 |                 592.82 |
| Important Stock Identification (TPC-H Q11)          |              167.13 |               24.36 |            158.33 |                  81.88 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3055.45 |               45.58 |           2003.53 |                 314.06 |
| Customer Distribution (TPC-H Q13)                   |             3098.81 |              252.96 |           3612.46 |                1170.01 |
| Promotion Effect Query (TPC-H Q14)                  |            12437.81 |               41.74 |           1487.79 |                 231.00 |
| Top Supplier Query (TPC-H Q15)                      |             1799.15 |               38.74 |          13742.99 |                 234.21 |
| Parts/Supplier Relationship (TPC-H Q16)             |              259.05 |               85.78 |            468.76 |                 281.65 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               58.79 |               54.63 |            302.97 |                 773.02 |
| Large Volume Customer (TPC-H Q18)                   |             2990.93 |              164.98 |           1727.31 |                2777.70 |
| Discounted Revenue (TPC-H Q19)                      |               94.40 |               99.96 |            141.71 |                  52.78 |
| Potential Part Promotion (TPC-H Q20)                |              208.96 |               44.33 |            288.36 |                 120.95 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            56730.98 |             1276.72 |           4682.39 |                 319.37 |
| Global Sales Opportunity Query (TPC-H Q22)          |              126.72 |               58.68 |            143.07 |                 100.69 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```


### PostgreSQL

#### TPC-H Simple

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_postgresql_1.log
```

yields (after ca. 10 minutes) something like

test_tpch_testcase_postgresql_1.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 555s 
* Code: 1782332834
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:265619
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782332834

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    1 |      241.00 |           1.00 |           20.00 |          7.00 |          209.00 |              8 |           0 |             |                |             0 | False         |               14.94 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         15 |            0.33 |            11626.62 |           5280.00 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         15 |            0.33 |            11626.62 |           5280.00 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                1147.95 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 275.59 |
| Shipping Priority (TPC-H Q3)                        |                 337.22 |
| Order Priority Checking Query (TPC-H Q4)            |                 148.22 |
| Local Supplier Volume (TPC-H Q5)                    |                 287.51 |
| Forecasting Revenue Change (TPC-H Q6)               |                 186.53 |
| Volume Shipping Query (TPC-H Q7)                    |                 339.46 |
| National Market Share (TPC-H Q8)                    |                 180.79 |
| Product Type Profit Measure (TPC-H Q9)              |                 476.76 |
| Returned Item Reporting Query (TPC-H Q10)           |                 535.35 |
| Important Stock Identification (TPC-H Q11)          |                  93.17 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 312.49 |
| Customer Distribution (TPC-H Q13)                   |                 954.68 |
| Promotion Effect Query (TPC-H Q14)                  |                 368.14 |
| Top Supplier Query (TPC-H Q15)                      |                 250.94 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 291.70 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                 809.24 |
| Large Volume Customer (TPC-H Q18)                   |                3603.30 |
| Discounted Revenue (TPC-H Q19)                      |                  53.53 |
| Potential Part Promotion (TPC-H Q20)                |                 147.53 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 299.18 |
| Global Sales Opportunity Query (TPC-H Q22)          |                  91.77 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```


#### TPC-H Monitoring

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_postgresql_2.log
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_postgresql_2.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 954s 
* Code: 1782333413
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:254316
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782333413

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   10 |      619.00 |           1.00 |           22.00 |         75.00 |          518.00 |              8 |           0 |             |                |             0 | False         |               58.16 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |         94 |            2.49 |            14860.42 |           8425.53 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |         94 |            2.49 |            14860.42 |           8425.53 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                5885.46 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                2817.11 |
| Shipping Priority (TPC-H Q3)                        |                3476.09 |
| Order Priority Checking Query (TPC-H Q4)            |                1092.58 |
| Local Supplier Volume (TPC-H Q5)                    |                2667.90 |
| Forecasting Revenue Change (TPC-H Q6)               |                1433.63 |
| Volume Shipping Query (TPC-H Q7)                    |                2433.04 |
| National Market Share (TPC-H Q8)                    |                1421.55 |
| Product Type Profit Measure (TPC-H Q9)              |                6231.35 |
| Returned Item Reporting Query (TPC-H Q10)           |                2514.16 |
| Important Stock Identification (TPC-H Q11)          |                 869.66 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                1972.85 |
| Customer Distribution (TPC-H Q13)                   |               11093.08 |
| Promotion Effect Query (TPC-H Q14)                  |                1839.57 |
| Top Supplier Query (TPC-H Q15)                      |                1805.42 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1387.64 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                7635.49 |
| Large Volume Customer (TPC-H Q18)                   |               24063.03 |
| Discounted Revenue (TPC-H Q19)                      |                 319.89 |
| Potential Part Promotion (TPC-H Q20)                |                3827.27 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                2487.12 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 444.12 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       703.73 |      4.45 |           5.76 |                 20.47 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        82.82 |      1.50 |           0.00 |                  0.93 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       301.30 |      3.52 |          16.21 |                 31.50 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        16.67 |      0.11 |           0.33 |                  0.33 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

#### TPC-H Throughput Test

```bash
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
```


```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_postgresql_3.log
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_postgresql_3.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 2173s 
* Code: 1782334451
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782334451
* PostgreSQL-1-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782334451
* PostgreSQL-1-1-2-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782334451
* PostgreSQL-1-2-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782334451
* PostgreSQL-1-2-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782334451
* PostgreSQL-1-2-2-1-2 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:27G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782334451

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   10 |     1058.00 |           3.00 |           31.00 |        278.00 |          741.00 |              8 |           0 |             |                |             0 | False         |               34.03 |
| PostgreSQL-1-2 |                2 |   10 |     1058.00 |           3.00 |           31.00 |        278.00 |          741.00 |              8 |           0 |             |                |             0 | False         |               34.03 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |         97 |            2.61 |            14166.28 |           8164.95 |           0 | PostgreSQL-1-1-1-1-1 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 10.00 |               22 |         97 |            2.51 |            14818.73 |           8164.95 |           0 | PostgreSQL-1-1-2-1-1 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1    | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |        2 |               1 |           1 | 10.00 |               22 |         96 |            2.51 |            14834.72 |           8250.00 |           0 | PostgreSQL-1-1-2-1-2 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1    | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |        237 |            4.11 |             9042.36 |           3341.77 |           0 | PostgreSQL-1-2-1-1-1 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 10.00 |               22 |         97 |            2.36 |            15746.08 |           8164.95 |           0 | PostgreSQL-1-2-2-1-1 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1    | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |        2 |               1 |           1 | 10.00 |               22 |         91 |            2.33 |            15921.19 |           8703.30 |           0 | PostgreSQL-1-2-2-1-2 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |         97 |            2.61 |            14166.28 |           8164.95 |           0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |        2 |               1 |           2 | 10.00 |               44 |         97 |            2.51 |            14826.72 |          16329.90 |           0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |        1 |               1 |           1 | 10.00 |               22 |        237 |            4.11 |             9042.36 |           3341.77 |           0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |        2 |               1 |           2 | 10.00 |               44 |         97 |            2.35 |            15833.39 |          16329.90 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |   PostgreSQL-1-1-2-1-1 |   PostgreSQL-1-1-2-1-2 |   PostgreSQL-1-2-1-1-1 |   PostgreSQL-1-2-2-1-1 |   PostgreSQL-1-2-2-1-2 |
|:----------------------------------------------------|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                5926.36 |                6531.76 |                6127.09 |               54526.81 |                5925.93 |                6040.47 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                2988.69 |                3379.46 |                2938.73 |               51102.35 |                2657.01 |                3039.43 |
| Shipping Priority (TPC-H Q3)                        |                3174.99 |                2675.75 |                2567.53 |               32686.61 |                2002.60 |                2181.31 |
| Order Priority Checking Query (TPC-H Q4)            |                1034.29 |                1014.10 |                1014.10 |                1178.37 |                 893.73 |                 802.55 |
| Local Supplier Volume (TPC-H Q5)                    |                2781.10 |                2396.17 |                2556.43 |                4513.11 |                2554.06 |                2157.31 |
| Forecasting Revenue Change (TPC-H Q6)               |                1392.03 |                1315.23 |                1405.32 |                1501.46 |                1221.00 |                1251.16 |
| Volume Shipping Query (TPC-H Q7)                    |                2324.60 |                2391.55 |                2388.02 |                2585.10 |                2232.32 |                2198.49 |
| National Market Share (TPC-H Q8)                    |                1525.71 |                1202.62 |                1240.08 |               12725.63 |                1136.64 |                1217.53 |
| Product Type Profit Measure (TPC-H Q9)              |                5772.25 |                5463.60 |                5423.10 |                5986.04 |                5517.99 |                5437.40 |
| Returned Item Reporting Query (TPC-H Q10)           |                2624.55 |                2460.89 |                2195.44 |                2487.83 |                2336.53 |                2386.97 |
| Important Stock Identification (TPC-H Q11)          |                1105.06 |                 883.79 |                 913.12 |                 992.60 |                 976.82 |                 819.32 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                2239.08 |                2236.89 |                1872.40 |                1962.66 |                1880.95 |                1843.78 |
| Customer Distribution (TPC-H Q13)                   |               11070.89 |               12422.30 |               12461.49 |               10733.74 |               10857.93 |               11053.31 |
| Promotion Effect Query (TPC-H Q14)                  |                2067.61 |                1988.61 |                2078.07 |                2006.54 |                1814.19 |                1950.73 |
| Top Supplier Query (TPC-H Q15)                      |                1982.54 |                1819.13 |                2147.15 |                1844.39 |                1888.51 |                1853.00 |
| Parts/Supplier Relationship (TPC-H Q16)             |                1516.21 |                1309.24 |                1607.68 |                1475.63 |                1422.98 |                1456.61 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                7925.07 |                7907.19 |                7454.49 |                7783.33 |                7338.59 |                6920.17 |
| Large Volume Customer (TPC-H Q18)                   |               25308.74 |               25380.95 |               25227.39 |               25541.17 |               29604.33 |               24955.05 |
| Discounted Revenue (TPC-H Q19)                      |                 335.50 |                 316.29 |                 321.96 |                 342.94 |                 316.74 |                 313.72 |
| Potential Part Promotion (TPC-H Q20)                |                4378.97 |                4356.45 |                3903.93 |                4257.82 |                3729.18 |                3515.04 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                2616.71 |                2911.91 |                2844.06 |                2628.06 |                2321.61 |                2447.35 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 512.99 |                 442.54 |                 484.28 |                 511.15 |                 477.77 |                 505.32 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       777.15 |      2.60 |           5.52 |                 25.13 |
| PostgreSQL-1-1-2-1 |       777.15 |      2.60 |           5.52 |                 25.13 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |
| PostgreSQL-1-1-2-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       112.16 |      1.65 |           0.01 |                  1.28 |
| PostgreSQL-1-1-2-1 |       112.16 |      1.65 |           0.01 |                  1.28 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       291.38 |      4.35 |          16.91 |                 33.82 |
| PostgreSQL-1-1-2-1 |       591.61 |     10.29 |          16.46 |                 33.17 |
| PostgreSQL-1-2-1-1 |      1782.80 |      3.60 |          21.37 |                 35.90 |
| PostgreSQL-1-2-2-1 |       567.27 |     11.08 |          15.53 |                 31.77 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        17.12 |      0.38 |           0.33 |                  0.34 |
| PostgreSQL-1-1-2-1 |        35.56 |      0.42 |           0.34 |                  0.34 |
| PostgreSQL-1-2-1-1 |        18.63 |      0.13 |           0.33 |                  0.33 |
| PostgreSQL-1-2-2-1 |        34.67 |      0.81 |           0.34 |                  0.34 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```


#### TPC-H RAM Disk Test

This loads TPC-H data (SF=3) into a database that is stored on a RAM disk.
The disk has size 50GB.
Make sure you have enough RAM.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ma \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rst ramdisk \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_ramdisk.log
```

yields (after ca. 15 minutes) something like

doc_tpch_testcase_ramdisk.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=3
* Type: tpch
* Duration: 526s 
* Code: 1782336718
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=3) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type ramdisk and size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:262129
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782336718

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |    3 |      214.00 |           1.00 |           20.00 |         17.00 |          173.00 |              8 |           0 |             |                |             0 | False         |               50.47 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         37 |            0.83 |            13810.53 |           6421.62 |           0 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 3.00 |               22 |         37 |            0.83 |            13810.53 |           6421.62 |           0 |

### Latency of Timer Execution [ms]
| Queries                                             |   PostgreSQL-1-1-1-1-1 |
|:----------------------------------------------------|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |                2605.43 |
| Minimum Cost Supplier Query (TPC-H Q2)              |                 711.95 |
| Shipping Priority (TPC-H Q3)                        |                1143.19 |
| Order Priority Checking Query (TPC-H Q4)            |                 344.25 |
| Local Supplier Volume (TPC-H Q5)                    |                 762.01 |
| Forecasting Revenue Change (TPC-H Q6)               |                 423.97 |
| Volume Shipping Query (TPC-H Q7)                    |                 938.71 |
| National Market Share (TPC-H Q8)                    |                 480.93 |
| Product Type Profit Measure (TPC-H Q9)              |                1338.47 |
| Returned Item Reporting Query (TPC-H Q10)           |                1430.88 |
| Important Stock Identification (TPC-H Q11)          |                 312.82 |
| Shipping Modes and Order Priority (TPC-H Q12)       |                 690.23 |
| Customer Distribution (TPC-H Q13)                   |                3185.49 |
| Promotion Effect Query (TPC-H Q14)                  |                 719.95 |
| Top Supplier Query (TPC-H Q15)                      |                 572.81 |
| Parts/Supplier Relationship (TPC-H Q16)             |                 569.23 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |                2096.00 |
| Large Volume Customer (TPC-H Q18)                   |               10342.04 |
| Discounted Revenue (TPC-H Q19)                      |                 105.74 |
| Potential Part Promotion (TPC-H Q20)                |                 424.53 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |                 729.71 |
| Global Sales Opportunity Query (TPC-H Q22)          |                 191.38 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       135.60 |      3.84 |          13.15 |                 13.15 |

### Loading phase: component data generator

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |         0.25 |      0.00 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        53.22 |      1.47 |          12.79 |                 12.79 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        13.23 |      0.00 |           0.25 |                  0.25 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        9.00 |                                    8.00 |

#### Execution phase: SUT deployment

| DBMS               |   Number of Idle Sessions |   Number of Idle-in-transaction Sessions |   Number of Idle-in-transaction Aborted Sessions |   Number of Active Sessions |   Number of Active Application Sessions |
|:-------------------|--------------------------:|-----------------------------------------:|-------------------------------------------------:|----------------------------:|----------------------------------------:|
| PostgreSQL-1-1-1-1 |                      1.00 |                                     0.00 |                                             0.00 |                        5.00 |                                    5.00 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```








### MySQL

#### TPC-H Simple

```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_mysql_1.log
```

yields (after ca. 10 minutes) something like

test_tpch_testcase_mysql_1.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 678s 
* Code: 1782332824
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
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
  * disk:265547
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782332824

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |    1 |      235.00 |           2.00 |           21.00 |         18.00 |          190.00 |              8 |           0 |             | None           |             0 | False         |               15.32 |

### Execution

#### Per Connection

|                 | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| MySQL-1-1-1-1-1 | MySQL-1         | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         52 |            1.01 |             3713.89 |           1523.08 |          -1 | MySQL-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |         52 |            1.01 |             3713.89 |           1523.08 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MySQL-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |           8498.18 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            125.34 |
| Shipping Priority (TPC-H Q3)                        |           1411.44 |
| Order Priority Checking Query (TPC-H Q4)            |            469.69 |
| Local Supplier Volume (TPC-H Q5)                    |           1073.29 |
| Forecasting Revenue Change (TPC-H Q6)               |           1202.28 |
| Volume Shipping Query (TPC-H Q7)                    |            763.35 |
| National Market Share (TPC-H Q8)                    |           2860.23 |
| Product Type Profit Measure (TPC-H Q9)              |           2027.72 |
| Returned Item Reporting Query (TPC-H Q10)           |           1140.93 |
| Important Stock Identification (TPC-H Q11)          |            167.67 |
| Shipping Modes and Order Priority (TPC-H Q12)       |           1912.12 |
| Customer Distribution (TPC-H Q13)                   |           3513.30 |
| Promotion Effect Query (TPC-H Q14)                  |           1378.28 |
| Top Supplier Query (TPC-H Q15)                      |          13242.41 |
| Parts/Supplier Relationship (TPC-H Q16)             |            390.39 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |            325.20 |
| Large Volume Customer (TPC-H Q18)                   |           1705.66 |
| Discounted Revenue (TPC-H Q19)                      |            139.85 |
| Potential Part Promotion (TPC-H Q20)                |            261.68 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           4691.05 |
| Global Sales Opportunity Query (TPC-H Q22)          |            143.28 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```


#### TPC-H Monitoring

```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_mysql_2.log
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_mysql_2.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 4927s 
* Code: 1782333525
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
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
  * disk:280818
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782333525

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   10 |      999.00 |           3.00 |           22.00 |        174.00 |          798.00 |              8 |           0 |             | None           |             0 | False         |               36.04 |

### Execution

#### Per Connection

|                 | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| MySQL-1-1-1-1-1 | MySQL-1         | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        583 |           11.12 |             3302.77 |           1358.49 |          -1 | MySQL-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        583 |           11.12 |             3302.77 |           1358.49 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MySQL-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          78397.68 |
| Minimum Cost Supplier Query (TPC-H Q2)              |           1132.37 |
| Shipping Priority (TPC-H Q3)                        |          15992.19 |
| Order Priority Checking Query (TPC-H Q4)            |           4625.08 |
| Local Supplier Volume (TPC-H Q5)                    |          13016.57 |
| Forecasting Revenue Change (TPC-H Q6)               |          11604.60 |
| Volume Shipping Query (TPC-H Q7)                    |           9224.89 |
| National Market Share (TPC-H Q8)                    |          36335.05 |
| Product Type Profit Measure (TPC-H Q9)              |          26303.56 |
| Returned Item Reporting Query (TPC-H Q10)           |          16749.76 |
| Important Stock Identification (TPC-H Q11)          |           2484.84 |
| Shipping Modes and Order Priority (TPC-H Q12)       |          18967.48 |
| Customer Distribution (TPC-H Q13)                   |          80492.53 |
| Promotion Effect Query (TPC-H Q14)                  |          15317.14 |
| Top Supplier Query (TPC-H Q15)                      |         163969.15 |
| Parts/Supplier Relationship (TPC-H Q16)             |           3084.69 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |           3258.76 |
| Large Volume Customer (TPC-H Q18)                   |          17093.37 |
| Discounted Revenue (TPC-H Q19)                      |           1373.38 |
| Potential Part Promotion (TPC-H Q20)                |           2822.47 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |          51820.62 |
| Global Sales Opportunity Query (TPC-H Q22)          |           1382.15 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      3755.41 |      9.06 |          25.92 |                 52.97 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        24.86 |      0.45 |           0.01 |                  1.14 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       568.65 |      1.02 |          26.65 |                 53.71 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        20.83 |      0.22 |           0.40 |                  0.41 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

#### TPC-H Throughput Test

```
kubectl delete pvc bexhoma-storage-mysql-tpch-1
```

```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_mysql_3.log
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_mysql_3.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 1241s 
    Code: 1748912641
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-BHT-8-1-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-1-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-1-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384432
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384416
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384420
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641
MySQL-BHT-8-2-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317384420
    datadisk:8286
    volume_size:30G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748912641

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MySQL-BHT-8-1-1-1  MySQL-BHT-8-1-2-1  MySQL-BHT-8-1-2-2  MySQL-BHT-8-2-1-1  MySQL-BHT-8-2-2-1  MySQL-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                                77.71              71.17             113.27              90.10              68.93              81.12
Minimum Cost Supplier Query (TPC-H Q2)                            4.07               3.44               3.64              16.93               4.26               3.92
Shipping Priority (TPC-H Q3)                                      2.18               1.87               2.57               3.00               1.75               2.78
Order Priority Checking Query (TPC-H Q4)                          1.64               1.53               3.12               3.66               1.49               2.79
Local Supplier Volume (TPC-H Q5)                                  1.87               1.74               3.57               2.56               1.77               3.41
Forecasting Revenue Change (TPC-H Q6)                             1.33               1.32               2.57               2.35               1.45               2.29
Forecasting Revenue Change (TPC-H Q7)                             1.90               2.24               3.55               2.75               1.87               2.75
National Market Share (TPC-H Q8)                                  3.18               1.92               3.07               3.26               2.51               2.98
Product Type Profit Measure (TPC-H Q9)                            1.94               1.69               2.81               2.76               1.92               2.73
Forecasting Revenue Change (TPC-H Q10)                            2.34               1.73               2.02               3.02               1.69               2.82
Important Stock Identification (TPC-H Q11)                        2.17               1.62               2.62               2.36               1.46               2.78
Shipping Modes and Order Priority (TPC-H Q12)                     2.92               1.41               3.14               2.75               1.71               2.73
Customer Distribution (TPC-H Q13)                                 2.79               1.47               2.62               2.19               1.32               2.65
Forecasting Revenue Change (TPC-H Q14)                            1.91               1.28               2.55               2.31               1.13               2.48
Top Supplier Query (TPC-H Q15)                                    4.25               2.78               4.84               5.21               3.27               4.68
Parts/Supplier Relationship (TPC-H Q16)                           2.79               1.84               3.10               2.31               2.02               3.30
Small-Quantity-Order Revenue (TPC-H Q17)                          2.13               1.24               5.14               2.00               1.73               2.81
Large Volume Customer (TPC-H Q18)                                 2.22               1.51               2.48               2.56               2.05               3.17
Discounted Revenue (TPC-H Q19)                                    2.26               1.71               2.63               2.48               2.09               2.37
Potential Part Promotion (TPC-H Q20)                              2.61               1.49               3.36               2.88               1.79               3.23
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               3.06               1.52               3.19               3.00               1.87               3.14
Global Sales Opportunity Query (TPC-H Q22)                        2.52               1.74               2.90               2.54               2.01               2.95

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-8-1-1-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-1-2-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-1-2-2           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-1-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-2-1           1.0            4.0         9.0       20.0      41.0
MySQL-BHT-8-2-2-2           1.0            4.0         9.0       20.0      41.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MySQL-BHT-8-1-1-1            0.0
MySQL-BHT-8-1-2-1            0.0
MySQL-BHT-8-1-2-2            0.0
MySQL-BHT-8-2-1-1            0.0
MySQL-BHT-8-2-2-1            0.0
MySQL-BHT-8-2-2-2            0.0

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MySQL-BHT-8-1-1-1         1287048.59
MySQL-BHT-8-1-2-1         1775137.53
MySQL-BHT-8-1-2-2         1003150.78
MySQL-BHT-8-2-1-1         1034211.47
MySQL-BHT-8-2-2-1         1630827.76
MySQL-BHT-8-2-2-2         1050194.94

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MySQL-BHT-8-1-1 1  1              1                  2      1   1          39600.0
MySQL-BHT-8-1-2 1  1              2                  3      2   1          52800.0
MySQL-BHT-8-2-1 1  2              1                  2      1   1          39600.0
MySQL-BHT-8-2-2 1  2              2                  3      2   1          52800.0

### Workflow

#### Actual
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        4.72     0.02         37.47                45.51
MySQL-BHT-8-1-2        4.72     0.02         37.47                45.51

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1           0        0           0.0                  0.0
MySQL-BHT-8-1-2           0        0           0.0                  0.0

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00     0.00         37.47                45.51
MySQL-BHT-8-1-2        1.35     0.00         37.75                45.78
MySQL-BHT-8-2-1      255.00     0.00         75.20                91.06
MySQL-BHT-8-2-2        0.00     0.02         37.46                45.29

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-1-2        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-2        0.03      0.0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```



#### TPC-H RAM Disk Test

This loads TPC-H data (SF=3) into a database that is stored on a RAM disk.
The disk has size 50GB.
Make sure you have enough RAM.

```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ma \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst ramdisk \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_mysql_ramdisk.log
```

yields (after ca. 15 minutes) something like

doc_tpch_testcase_mysql_ramdisk.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 1042s 
    Code: 1766132188
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 600.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.19.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type ramdisk and size 50Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:435020
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766132188
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:17.5
    RAM:541008486400
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-160-generic
    node:cl-worker11
    disk:435020
    cpu_list:0-63
    args:['-c', 'max_connections=1500', '-c', 'max_worker_processes=64', '-c', 'max_parallel_workers=64', '-c', 'max_parallel_workers_per_gather=64', '-c', 'max_parallel_maintenance_workers=64', '-c', 'shared_buffers=256GB', '-c', 'effective_cache_size=256GB', '-c', 'work_mem=32GB', '-c', 'maintenance_work_mem=4GB', '-c', 'temp_buffers=4GB', '-c', 'wal_buffers=1GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'fsync=on', '-c', 'wal_compression=on', '-c', 'synchronous_commit=on', '-c', 'max_wal_size=32GB', '-c', 'min_wal_size=32GB', '-c', 'checkpoint_timeout=12h', '-c', 'checkpoint_completion_target=1.0', '-c', 'effective_io_concurrency=64']
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1766132188

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-2-1-1
Pricing Summary Report (TPC-H Q1)                                   3608.47                 2349.00
Minimum Cost Supplier Query (TPC-H Q2)                               679.01                  455.46
Shipping Priority (TPC-H Q3)                                        1287.78                  748.13
Order Priority Checking Query (TPC-H Q4)                             609.06                  361.39
Local Supplier Volume (TPC-H Q5)                                     968.34                  676.62
Forecasting Revenue Change (TPC-H Q6)                               1245.02                  485.43
Forecasting Revenue Change (TPC-H Q7)                               1372.38                  785.18
National Market Share (TPC-H Q8)                                     666.39                  467.59
Product Type Profit Measure (TPC-H Q9)                              1887.53                 1152.69
Forecasting Revenue Change (TPC-H Q10)                              2114.77                 1199.52
Important Stock Identification (TPC-H Q11)                           184.23                  169.50
Shipping Modes and Order Priority (TPC-H Q12)                       1094.65                  702.00
Customer Distribution (TPC-H Q13)                                   2494.37                 2050.91
Forecasting Revenue Change (TPC-H Q14)                               745.60                  522.52
Top Supplier Query (TPC-H Q15)                                       772.18                  571.79
Parts/Supplier Relationship (TPC-H Q16)                              602.18                  587.03
Small-Quantity-Order Revenue (TPC-H Q17)                            3982.40                 2093.34
Large Volume Customer (TPC-H Q18)                                   7071.98                 7237.16
Discounted Revenue (TPC-H Q19)                                       135.60                  122.21
Potential Part Promotion (TPC-H Q20)                                 334.01                  323.48
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)                  803.02                  772.54
Global Sales Opportunity Query (TPC-H Q22)                           235.45                  233.40

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1          28.0            9.0         1.0      181.0     223.0
PostgreSQL-BHT-8-2-1-1          19.0            8.0         2.0      197.0     231.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           0.99
PostgreSQL-BHT-8-2-1-1           0.71

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            3773.16
PostgreSQL-BHT-8-2-1-1            5275.89

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                    time [s]  count   SF  Throughput@Size
DBMS                 SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1-1 1.0 1              1                 37      1  1.0          2140.54
PostgreSQL-BHT-8-2-1 1.0 2              1                 29      1  1.0          2731.03

### Workflow
                                   orig_name   SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-1  1.0     8               1           1       1766132604     1766132641
PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-1  1.0     8               2           1       1766133147     1766133176

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1], [1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```


### MariaDB

#### TPC-H Simple

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_mariadb_1.log
```

yields (after ca. 10 minutes) something like

test_tpch_testcase_mariadb_1.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 708s 
* Code: 1782332846
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:265547
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782332846

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |      367.00 |           1.00 |           25.00 |         36.00 |          302.00 |              8 |           0 |             | None           |             0 | False         |                9.81 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.15 |             3301.61 |            740.19 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.15 |             3301.61 |            740.19 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             8140.58 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              542.66 |
| Shipping Priority (TPC-H Q3)                        |             1629.37 |
| Order Priority Checking Query (TPC-H Q4)            |              372.68 |
| Local Supplier Volume (TPC-H Q5)                    |             1190.27 |
| Forecasting Revenue Change (TPC-H Q6)               |             1298.28 |
| Volume Shipping Query (TPC-H Q7)                    |             1265.87 |
| National Market Share (TPC-H Q8)                    |             2202.44 |
| Product Type Profit Measure (TPC-H Q9)              |             2062.75 |
| Returned Item Reporting Query (TPC-H Q10)           |              896.30 |
| Important Stock Identification (TPC-H Q11)          |              150.67 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3196.19 |
| Customer Distribution (TPC-H Q13)                   |             3191.68 |
| Promotion Effect Query (TPC-H Q14)                  |            12756.89 |
| Top Supplier Query (TPC-H Q15)                      |             2071.70 |
| Parts/Supplier Relationship (TPC-H Q16)             |              238.70 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               62.08 |
| Large Volume Customer (TPC-H Q18)                   |             3098.08 |
| Discounted Revenue (TPC-H Q19)                      |               97.96 |
| Potential Part Promotion (TPC-H Q20)                |              227.04 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            57943.45 |
| Global Sales Opportunity Query (TPC-H Q22)          |              130.66 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```


#### TPC-H Monitoring

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_mariadb_2.log
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_mariadb_2.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 725s 
* Code: 1782333577
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:254316
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782333577

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |      361.00 |           1.00 |           18.00 |         47.00 |          292.00 |              8 |           0 |             | None           |             0 | False         |                9.97 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.12 |             3444.13 |            740.19 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.12 |             3444.13 |            740.19 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             7826.42 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              508.07 |
| Shipping Priority (TPC-H Q3)                        |             1652.33 |
| Order Priority Checking Query (TPC-H Q4)            |              400.18 |
| Local Supplier Volume (TPC-H Q5)                    |             1065.60 |
| Forecasting Revenue Change (TPC-H Q6)               |              897.29 |
| Volume Shipping Query (TPC-H Q7)                    |             1131.93 |
| National Market Share (TPC-H Q8)                    |             2075.71 |
| Product Type Profit Measure (TPC-H Q9)              |             2037.49 |
| Returned Item Reporting Query (TPC-H Q10)           |              904.34 |
| Important Stock Identification (TPC-H Q11)          |              139.67 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3119.38 |
| Customer Distribution (TPC-H Q13)                   |             3115.70 |
| Promotion Effect Query (TPC-H Q14)                  |            12671.14 |
| Top Supplier Query (TPC-H Q15)                      |             1997.16 |
| Parts/Supplier Relationship (TPC-H Q16)             |              210.77 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               59.44 |
| Large Volume Customer (TPC-H Q18)                   |             3205.99 |
| Discounted Revenue (TPC-H Q19)                      |              106.26 |
| Potential Part Promotion (TPC-H Q20)                |              222.20 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            58675.88 |
| Global Sales Opportunity Query (TPC-H Q22)          |              127.26 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |       519.88 |      6.76 |           5.68 |                  5.78 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         2.75 |      0.05 |           0.00 |                  0.11 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        83.67 |      1.00 |           5.91 |                  6.02 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        14.63 |      0.46 |           0.30 |                  0.31 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```

#### TPC-H Throughput Test

```bash
kubectl delete pvc bexhoma-storage-mariadb-tpch-1
```

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_mariadb_3.log
```

yields (after ca. 15 minutes) something like

test_tpch_testcase_mariadb_3.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 2627s 
* Code: 1782334385
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-1-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-1-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-2-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220467
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-2-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253328
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385
* MariaDB-1-2-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253328
  * volume_size:50G
  * volume_used:2.1G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782334385

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpch (2 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpch (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpch (2 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |     1725.00 |           3.00 |           33.00 |        510.00 |         1172.00 |              8 |           0 |             | None           |             0 | False         |                2.09 |
| MariaDB-1-2 |                2 |    1 |     1725.00 |           3.00 |           33.00 |        510.00 |         1172.00 |              8 |           0 |             | None           |             0 | False         |                2.09 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        103 |            1.08 |             3525.92 |            768.93 |          -1 | MariaDB-1-1-1-1-1 |
| MariaDB-1-1-2-1-1 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |        121 |            1.17 |             3264.87 |            654.55 |          -1 | MariaDB-1-1-2-1-1 |
| MariaDB-1-1-2-1-2 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               22 |        119 |            1.18 |             3237.13 |            665.55 |          -1 | MariaDB-1-1-2-1-2 |
| MariaDB-1-2-1-1-1 | MariaDB-1       | MariaDB-1-2-1 | MariaDB-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.16 |             3324.21 |            740.19 |          -1 | MariaDB-1-2-1-1-1 |
| MariaDB-1-2-2-1-1 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               22 |        135 |            1.37 |             2770.37 |            586.67 |          -1 | MariaDB-1-2-2-1-1 |
| MariaDB-1-2-2-1-2 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               22 |        134 |            1.43 |             2674.87 |            591.04 |          -1 | MariaDB-1-2-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |        103 |            1.08 |             3525.92 |            768.93 |          -1 |
| MariaDB-1-1-2 | MariaDB-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               44 |        121 |            1.18 |             3250.97 |           1309.09 |          -1 |
| MariaDB-1-2-1 | MariaDB-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               22 |        107 |            1.16 |             3324.21 |            740.19 |          -1 |
| MariaDB-1-2-2 | MariaDB-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |               44 |        135 |            1.40 |             2722.20 |           1173.33 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |   MariaDB-1-1-2-1-1 |   MariaDB-1-1-2-1-2 |   MariaDB-1-2-1-1-1 |   MariaDB-1-2-2-1-1 |   MariaDB-1-2-2-1-2 |
|:----------------------------------------------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |             7835.73 |             7460.30 |             7576.32 |             7445.58 |             7798.95 |             7445.41 |
| Minimum Cost Supplier Query (TPC-H Q2)              |              445.24 |              413.40 |              452.21 |              562.07 |              698.00 |              629.33 |
| Shipping Priority (TPC-H Q3)                        |             1551.76 |             1716.63 |             1743.74 |             1536.82 |             2642.48 |             2428.26 |
| Order Priority Checking Query (TPC-H Q4)            |              339.95 |              350.44 |              357.45 |              351.30 |              398.86 |              386.22 |
| Local Supplier Volume (TPC-H Q5)                    |              966.73 |             1102.55 |             1067.68 |              965.93 |             1496.52 |             1452.50 |
| Forecasting Revenue Change (TPC-H Q6)               |              826.30 |              813.59 |              799.97 |              806.65 |              802.49 |              802.31 |
| Volume Shipping Query (TPC-H Q7)                    |             1078.50 |             1090.08 |             1134.41 |             1098.53 |             1394.57 |             1357.76 |
| National Market Share (TPC-H Q8)                    |             1828.43 |             2211.54 |             2201.69 |             1924.68 |             3119.33 |             3003.46 |
| Product Type Profit Measure (TPC-H Q9)              |             3999.56 |             4395.40 |             4387.79 |             4681.89 |             5739.51 |             5963.52 |
| Returned Item Reporting Query (TPC-H Q10)           |              927.14 |              925.49 |              928.07 |              925.57 |             1174.82 |             1175.41 |
| Important Stock Identification (TPC-H Q11)          |              134.54 |              147.96 |              141.73 |              146.11 |              217.12 |              218.17 |
| Shipping Modes and Order Priority (TPC-H Q12)       |             3029.25 |             3415.46 |             3422.66 |             3044.02 |             4549.91 |             4266.76 |
| Customer Distribution (TPC-H Q13)                   |             2995.40 |             3887.61 |             3889.33 |             3221.74 |             4031.94 |             3630.11 |
| Promotion Effect Query (TPC-H Q14)                  |            12074.97 |            14588.29 |            14297.04 |            14396.01 |            18364.82 |            17723.74 |
| Top Supplier Query (TPC-H Q15)                      |             1780.15 |             1809.90 |             1816.64 |             1751.99 |             1732.48 |             2195.46 |
| Parts/Supplier Relationship (TPC-H Q16)             |              220.32 |              221.36 |              206.89 |              213.05 |              234.73 |              226.32 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |               69.54 |               61.56 |               65.50 |               75.99 |               62.19 |               61.79 |
| Large Volume Customer (TPC-H Q18)                   |             2930.59 |             3922.40 |             3912.35 |             2979.81 |             3533.70 |             3592.21 |
| Discounted Revenue (TPC-H Q19)                      |               95.73 |              104.56 |              105.85 |              103.57 |               96.93 |              161.23 |
| Potential Part Promotion (TPC-H Q20)                |              206.68 |              235.15 |              220.62 |              242.60 |              218.74 |              385.86 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            55401.87 |            66972.36 |            65984.58 |            56422.19 |            71639.16 |            71949.04 |
| Global Sales Opportunity Query (TPC-H Q22)          |              113.79 |              115.17 |              139.42 |              144.84 |              158.60 |              159.10 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      1541.04 |      2.44 |           5.93 |                  6.04 |
| MariaDB-1-1-2-1 |      1541.04 |      2.44 |           5.93 |                  6.04 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| MariaDB-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         4.79 |      0.05 |           0.00 |                  0.13 |
| MariaDB-1-1-2-1 |         4.79 |      0.05 |           0.00 |                  0.13 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        69.86 |      0.99 |           5.99 |                  6.09 |
| MariaDB-1-1-2-1 |       205.20 |      2.00 |           6.00 |                  6.10 |
| MariaDB-1-2-1-1 |        92.51 |      1.00 |           3.72 |                  3.75 |
| MariaDB-1-2-2-1 |       224.20 |      2.00 |           3.73 |                  3.76 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        15.09 |      0.17 |           0.30 |                  0.30 |
| MariaDB-1-1-2-1 |        29.66 |      0.21 |           0.33 |                  0.34 |
| MariaDB-1-2-1-1 |        16.76 |      0.46 |           0.34 |                  0.35 |
| MariaDB-1-2-2-1 |        30.93 |      0.24 |           0.34 |                  0.35 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```







#### TPC-H RAM Disk Test

This loads TPC-H data (SF=3) into a database that is stored on a RAM disk.
The disk has size 50GB.
Make sure you have enough RAM.

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ma \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst ramdisk \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_mariadb_ramdisk.log

```

yields (after ca. 15 minutes) something like

doc_tpch_testcase_mariadb_ramdisk.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 3579s 
* Code: 1782340884
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=10) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type ramdisk and size 100Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225014
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782340884

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   10 |     2433.00 |           2.00 |           25.00 |        384.00 |         2018.00 |              8 |           0 |             | None           |             0 | False         |               14.80 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |       1148 |           12.78 |             2877.44 |            689.90 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |       1148 |           12.78 |             2877.44 |            689.90 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MariaDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            70985.56 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             5073.32 |
| Shipping Priority (TPC-H Q3)                        |            20450.51 |
| Order Priority Checking Query (TPC-H Q4)            |            21473.07 |
| Local Supplier Volume (TPC-H Q5)                    |            11632.52 |
| Forecasting Revenue Change (TPC-H Q6)               |             8384.30 |
| Volume Shipping Query (TPC-H Q7)                    |            12469.46 |
| National Market Share (TPC-H Q8)                    |            25097.32 |
| Product Type Profit Measure (TPC-H Q9)              |            23869.39 |
| Returned Item Reporting Query (TPC-H Q10)           |            10857.62 |
| Important Stock Identification (TPC-H Q11)          |             1819.67 |
| Shipping Modes and Order Priority (TPC-H Q12)       |            32846.25 |
| Customer Distribution (TPC-H Q13)                   |            42904.62 |
| Promotion Effect Query (TPC-H Q14)                  |           162749.93 |
| Top Supplier Query (TPC-H Q15)                      |            18011.23 |
| Parts/Supplier Relationship (TPC-H Q16)             |             2189.07 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              623.10 |
| Large Volume Customer (TPC-H Q18)                   |            39322.71 |
| Discounted Revenue (TPC-H Q19)                      |             1202.30 |
| Potential Part Promotion (TPC-H Q20)                |             3050.72 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           624716.37 |
| Global Sales Opportunity Query (TPC-H Q22)          |             1195.83 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      7280.38 |     11.95 |          74.05 |                 74.05 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.02 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        29.18 |      0.22 |           0.01 |                  1.31 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      1143.73 |      1.07 |          59.70 |                 59.70 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        18.50 |      0.09 |           0.34 |                  0.34 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component data generator contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
```













## TPC-DS

### Compare

#### TPC-DS Compare

```bash
bexhoma tpcds \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_compare.log
```

yields (after ca. 520 minutes) something like

test_tpcds_testcase_compare.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 5464s 
* Code: 1782340910
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:225014
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782340910
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP1
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:262263
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782340910
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:263247
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782340910
* PostgreSQL-1-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:259748
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1782340910

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1    |                1 |    1 |      685.00 |           1.00 |            1.00 |         62.00 |          616.00 |              8 |           0 |             | None           |             0 | False         |                5.26 |
| MonetDB-1-1    |                1 |    1 |      267.00 |           2.00 |            1.00 |         59.00 |          200.00 |              8 |           0 |             | None           |             0 | False         |               13.48 |
| MySQL-1-1      |                1 |    1 |      826.00 |           2.00 |            1.00 |         90.00 |          726.00 |              8 |           0 |             | None           |             0 | False         |                4.36 |
| PostgreSQL-1-1 |                1 |    1 |      302.00 |           1.00 |            1.00 |         49.00 |          243.00 |              8 |           0 |             | None           |             0 | False         |               11.92 |

### Execution

#### Per Connection

|                      | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| MariaDB-1-1-1-1-1    | MariaDB-1       | MariaDB-1-1-1    | MariaDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |       3220 |            1.01 |             3618.98 |            108.45 |          -1 | MariaDB-1-1-1-1-1    |
| MonetDB-1-1-1-1-1    | MonetDB-1       | MonetDB-1-1-1    | MonetDB-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |         22 |            0.06 |            60422.01 |          15872.73 |          -1 | MonetDB-1-1-1-1-1    |
| MySQL-1-1-1-1-1      | MySQL-1         | MySQL-1-1-1      | MySQL-1-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               97 |        517 |            0.84 |             4337.55 |            675.44 |          -1 | MySQL-1-1-1-1-1      |
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1    | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |        215 |            0.42 |             8799.20 |           1624.19 |          -1 | PostgreSQL-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1    | MariaDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |       3220 |            1.01 |             3618.98 |            108.45 |          -1 |
| MonetDB-1-1-1    | MonetDB-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               97 |         22 |            0.06 |            60422.01 |          15872.73 |          -1 |
| MySQL-1-1-1      | MySQL-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               97 |        517 |            0.84 |             4337.55 |            675.44 |          -1 |
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |        215 |            0.42 |             8799.20 |           1624.19 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MariaDB-1-1-1-1-1 |   MonetDB-1-1-1-1-1 |   MySQL-1-1-1-1-1 |   PostgreSQL-1-1-1-1-1 |
|:--------------|--------------------:|--------------------:|------------------:|-----------------------:|
| TPC-DS Q1     |               21.07 |               55.26 |             67.17 |                 152.02 |
| TPC-DS Q2     |             5803.54 |               99.61 |           5400.13 |                 318.81 |
| TPC-DS Q3     |               13.89 |               24.17 |             16.76 |                 187.35 |
| TPC-DS Q4     |            13724.83 |              591.97 |          28228.22 |                9527.46 |
| TPC-DS Q5     |             9699.03 |               82.07 |          12899.93 |                 512.05 |
| TPC-DS Q6     |              910.05 |               46.80 |          76171.86 |               58650.09 |
| TPC-DS Q7     |             4163.95 |               46.20 |            767.16 |                 384.39 |
| TPC-DS Q8     |              373.86 |               26.99 |            398.33 |                  71.92 |
| TPC-DS Q9     |             4233.44 |               47.19 |           4433.47 |                2453.94 |
| TPC-DS Q10    |               69.69 |               39.45 |             50.23 |                1241.57 |
| TPC-DS Q11    |             9526.71 |              290.42 |          18897.74 |                5740.73 |
| TPC-DS Q12    |              281.70 |               22.44 |            316.18 |                  70.59 |
| TPC-DS Q13    |             1242.60 |               42.27 |           1559.52 |                 669.91 |
| TPC-DS Q14a+b |            52023.38 |             1623.37 |          52238.94 |                2203.49 |
| TPC-DS Q15    |              168.84 |               25.55 |            199.70 |                 135.23 |
| TPC-DS Q16    |            11165.10 |               34.09 |             62.38 |                 196.40 |
| TPC-DS Q17    |              711.14 |               88.00 |            483.22 |                 310.12 |
| TPC-DS Q18    |             1970.04 |               54.44 |            954.09 |                 415.76 |
| TPC-DS Q19    |              240.11 |               38.34 |            335.27 |                 160.99 |
| TPC-DS Q20    |              465.63 |               27.99 |            588.79 |                 102.95 |
| TPC-DS Q21    |            21609.24 |               94.85 |          27884.28 |                 253.48 |
| TPC-DS Q22    |            19818.31 |              707.33 |           5119.50 |                3602.36 |
| TPC-DS Q23a+b |            53298.29 |              977.49 |          37681.68 |                4651.22 |
| TPC-DS Q24a+b |               25.72 |              221.42 |           1307.35 |                 687.98 |
| TPC-DS Q25    |              158.90 |               92.36 |            146.32 |                 319.96 |
| TPC-DS Q26    |              905.16 |               23.92 |           5428.34 |                 276.28 |
| TPC-DS Q27    |             1620.45 |               62.92 |            623.18 |                  35.32 |
| TPC-DS Q28    |             2887.82 |               41.03 |           3676.00 |                 880.69 |
| TPC-DS Q29    |               98.79 |               90.62 |             85.77 |                 350.02 |
| TPC-DS Q30    |              113.54 |               24.25 |            479.41 |               10200.61 |
| TPC-DS Q31    |             1481.64 |               95.09 |          12681.09 |                1858.14 |
| TPC-DS Q32    |               12.02 |               17.87 |            137.53 |                 118.79 |
| TPC-DS Q33    |              154.27 |               23.98 |            225.23 |                 446.59 |
| TPC-DS Q34    |             3114.09 |               29.74 |           1078.53 |                  37.94 |
| TPC-DS Q35    |             1221.68 |               72.71 |          15290.84 |                1451.16 |
| TPC-DS Q36    |             2938.42 |              103.00 |           2955.39 |                 429.56 |
| TPC-DS Q37    |             3727.47 |               63.45 |             14.13 |                 351.82 |
| TPC-DS Q38    |             7216.85 |              122.45 |           8440.30 |                1800.39 |
| TPC-DS Q39a+b |             1325.36 |              984.92 |           2256.26 |                2867.46 |
| TPC-DS Q40    |              177.18 |               59.73 |            182.75 |                 142.59 |
| TPC-DS Q41    |              433.50 |                8.30 |           1449.47 |                1274.81 |
| TPC-DS Q42    |              228.59 |               53.15 |             28.12 |                  99.66 |
| TPC-DS Q43    |             1161.45 |               40.72 |              2.47 |                  34.65 |
| TPC-DS Q44    |                2.80 |               27.29 |              2.84 |                   4.33 |
| TPC-DS Q45    |              123.79 |               15.95 |            129.26 |                 105.13 |
| TPC-DS Q46    |             3343.31 |               34.21 |            854.27 |                  48.80 |
| TPC-DS Q47    |            14000.60 |              173.92 |           7504.01 |                2290.67 |
| TPC-DS Q48    |             1213.90 |               33.09 |           1023.27 |                 816.02 |
| TPC-DS Q49    |               98.84 |               67.00 |            144.06 |                 570.17 |
| TPC-DS Q50    |               30.46 |               95.72 |             34.04 |                 522.41 |
| TPC-DS Q51    |             7726.22 |              298.44 |           6481.72 |                1212.11 |
| TPC-DS Q52    |              241.61 |               52.72 |             31.34 |                 100.63 |
| TPC-DS Q53    |              137.48 |               24.66 |            247.29 |                 125.98 |
| TPC-DS Q54    |             1041.57 |               25.03 |           2888.43 |                 110.26 |
| TPC-DS Q55    |              232.88 |               17.69 |             20.79 |                  97.20 |
| TPC-DS Q56    |              297.55 |               20.46 |            255.40 |                 515.70 |
| TPC-DS Q57    |             7031.33 |              102.55 |           3618.49 |                1217.90 |
| TPC-DS Q58    |             5844.27 |               53.04 |           6950.81 |                 485.39 |
| TPC-DS Q59    |             9224.35 |               97.24 |           6548.77 |                 522.90 |
| TPC-DS Q60    |              315.44 |               21.29 |            493.63 |                 455.90 |
| TPC-DS Q61    |              408.92 |               27.47 |              3.25 |                 200.50 |
| TPC-DS Q62    |             1694.59 |               33.87 |           3010.61 |                 136.49 |
| TPC-DS Q63    |              183.99 |               26.25 |            264.85 |                 130.30 |
| TPC-DS Q64    |              864.69 |              229.33 |            844.38 |                1077.57 |
| TPC-DS Q65    |             5950.28 |               84.82 |           7780.19 |                 788.41 |
| TPC-DS Q66    |             1201.54 |              102.77 |           1529.50 |                 260.41 |
| TPC-DS Q67    |             7342.74 |              227.18 |           8726.65 |                3833.80 |
| TPC-DS Q68    |             3129.20 |               33.12 |            358.69 |                  51.43 |
| TPC-DS Q69    |              408.21 |               50.25 |            491.36 |                 320.53 |
| TPC-DS Q70    |             8599.59 |               77.83 |          13044.67 |                 530.28 |
| TPC-DS Q71    |              467.25 |               27.97 |            548.84 |                 421.98 |
| TPC-DS Q72    |           402504.84 |              193.61 |          13769.05 |                1377.94 |
| TPC-DS Q73    |             2897.10 |               21.17 |           1109.43 |                  37.22 |
| TPC-DS Q74    |             5990.92 |               89.73 |           5425.75 |                1344.35 |
| TPC-DS Q75    |             5687.24 |              271.19 |           1794.57 |                1031.77 |
| TPC-DS Q76    |              470.49 |               32.05 |            454.91 |                 157.88 |
| TPC-DS Q77    |             6140.32 |               50.71 |           9968.00 |                 424.99 |
| TPC-DS Q78    |             5760.60 |              397.72 |          12489.20 |                2499.30 |
| TPC-DS Q79    |             3410.66 |               55.51 |           5240.94 |                 251.68 |
| TPC-DS Q80    |              534.09 |              293.81 |           9304.36 |                 586.29 |
| TPC-DS Q81    |              215.52 |               38.86 |           2210.80 |               51833.27 |
| TPC-DS Q82    |             3690.94 |               52.44 |             16.92 |                 371.25 |
| TPC-DS Q83    |              916.24 |               13.48 |            885.12 |                 123.44 |
| TPC-DS Q84    |               59.94 |               20.42 |             66.85 |                 105.39 |
| TPC-DS Q85    |              127.50 |              174.22 |            109.63 |                 402.61 |
| TPC-DS Q86    |              920.11 |               33.54 |           1198.13 |                 265.17 |
| TPC-DS Q87    |             7192.41 |              146.16 |           8526.64 |                1738.31 |
| TPC-DS Q88    |            23827.06 |               41.49 |           2029.98 |                3558.78 |
| TPC-DS Q89    |             1681.72 |               37.15 |            284.53 |                 164.21 |
| TPC-DS Q90    |              357.77 |               14.74 |            377.34 |                 154.39 |
| TPC-DS Q91    |               18.86 |               22.27 |             22.12 |                 177.27 |
| TPC-DS Q92    |               11.04 |               11.17 |             63.66 |                  64.48 |
| TPC-DS Q93    |               39.09 |               71.28 |             45.82 |                 197.28 |
| TPC-DS Q96    |             2703.00 |               16.61 |            159.09 |                 105.49 |
| TPC-DS Q97    |             5213.55 |              129.45 |           6318.19 |                 417.12 |
| TPC-DS Q98    |              871.98 |               43.38 |           1138.54 |                 182.52 |
| TPC-DS Q99    |             5054.21 |               48.56 |          12817.66 |                 179.08 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
* TPC-DS Q94
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=61) Query execution was interrupted (max_statement_time exceeded)
* TPC-DS Q95
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=61) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)

|                      |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:---------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1    |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MonetDB-1-1-1-1-1    |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |
| PostgreSQL-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
```


### PostgreSQL

#### TPC-DS Simple

```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_postgresql_1.log
```

yields (after ca. 10 minutes) something like

test_tpcds_testcase_postgresql_1.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 1119s 
    Code: 1750150367
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:399210064
    datadisk:5805
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750150367

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-8-1-1
TPC-DS Q1                    321.74
TPC-DS Q2                    854.14
TPC-DS Q3                    504.21
TPC-DS Q4                  15805.62
TPC-DS Q5                   1428.59
TPC-DS Q6                 218550.20
TPC-DS Q7                   1122.21
TPC-DS Q8                    146.75
TPC-DS Q9                   6133.30
TPC-DS Q10                  3109.86
TPC-DS Q11                 11850.95
TPC-DS Q12                   215.05
TPC-DS Q13                  1924.69
TPC-DS Q14a+b               7842.38
TPC-DS Q15                   344.82
TPC-DS Q16                   698.62
TPC-DS Q17                  1045.41
TPC-DS Q18                  1200.03
TPC-DS Q19                   487.97
TPC-DS Q20                   298.23
TPC-DS Q21                   693.68
TPC-DS Q22                 10040.65
TPC-DS Q23a+b              11247.33
TPC-DS Q24a+b                150.24
TPC-DS Q25                  1047.69
TPC-DS Q26                   755.48
TPC-DS Q27                   135.65
TPC-DS Q28                  4767.78
TPC-DS Q29                  1127.42
TPC-DS Q30                 29850.95
TPC-DS Q31                  6222.77
TPC-DS Q32                   236.63
TPC-DS Q33                  1141.41
TPC-DS Q34                    62.32
TPC-DS Q35                  3373.60
TPC-DS Q36                    59.33
TPC-DS Q37                   128.97
TPC-DS Q38                  3407.48
TPC-DS Q39a+b               7852.00
TPC-DS Q40                   346.34
TPC-DS Q41                  2049.37
TPC-DS Q42                   264.60
TPC-DS Q43                    61.84
TPC-DS Q44                  1369.90
TPC-DS Q45                   224.56
TPC-DS Q46                    59.90
TPC-DS Q47                  4255.90
TPC-DS Q48                  1845.05
TPC-DS Q49                  2153.64
TPC-DS Q50                   706.39
TPC-DS Q51                  2986.08
TPC-DS Q52                   261.93
TPC-DS Q53                   319.60
TPC-DS Q54                   203.32
TPC-DS Q55                   258.49
TPC-DS Q56                  1157.55
TPC-DS Q57                  2242.27
TPC-DS Q58                  1305.22
TPC-DS Q59                  1268.32
TPC-DS Q60                  1072.58
TPC-DS Q61                  4470.00
TPC-DS Q62                   296.18
TPC-DS Q63                   325.38
TPC-DS Q64                  2342.27
TPC-DS Q65                  1608.46
TPC-DS Q66                   623.51
TPC-DS Q67                  7069.65
TPC-DS Q68                    58.27
TPC-DS Q69                   717.44
TPC-DS Q70                  1226.45
TPC-DS Q71                   965.12
TPC-DS Q72                  2875.61
TPC-DS Q73                    62.40
TPC-DS Q74                  3730.10
TPC-DS Q75                  2373.77
TPC-DS Q76                   601.67
TPC-DS Q77                  5266.46
TPC-DS Q78                  3539.05
TPC-DS Q79                   503.51
TPC-DS Q80                  1472.34
TPC-DS Q81                125373.84
TPC-DS Q82                   926.16
TPC-DS Q83                   298.76
TPC-DS Q84                   256.94
TPC-DS Q85                   892.87
TPC-DS Q86                   484.80
TPC-DS Q87                  3366.65
TPC-DS Q88                  6745.89
TPC-DS Q89                   340.88
TPC-DS Q90                  2156.13
TPC-DS Q91                   422.71
TPC-DS Q92                  2174.54
TPC-DS Q93                   372.70
TPC-DS Q94                   460.10
TPC-DS Q95                  9591.05
TPC-DS Q96                   276.40
TPC-DS Q97                  1042.63
TPC-DS Q98                   500.53
TPC-DS Q99                   421.20

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0          130.0         1.0      145.0     284.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           1.07

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            3407.85

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                  time [s]  count   SF  Throughput@Size
DBMS               SF  num_experiment num_client                                       
PostgreSQL-BHT-8-1 1.0 1              1                596      1  1.0           597.99

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```


#### TPC-DS Monitoring

```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_postgresql_2.log
```

yields (after ca. 15 minutes) something like

test_tpcds_testcase_postgresql_2.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=10
    Type: tpcds
    Duration: 7431s 
    Code: 1750151567
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:449714548
    datadisk:55281
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750151567

### Errors (failed queries)
            PostgreSQL-BHT-8-1-1
TPC-DS Q6                   True
TPC-DS Q30                  True
TPC-DS Q81                  True
TPC-DS Q6
PostgreSQL-BHT-8-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
TPC-DS Q30
PostgreSQL-BHT-8-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
TPC-DS Q81
PostgreSQL-BHT-8-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-8-1-1
TPC-DS Q1                   2634.37
TPC-DS Q2                   5235.23
TPC-DS Q3                   2870.39
TPC-DS Q4                 107415.41
TPC-DS Q5                   9899.03
TPC-DS Q7                   4716.17
TPC-DS Q8                   3664.65
TPC-DS Q9                  16777.37
TPC-DS Q10                  6345.62
TPC-DS Q11                 97696.55
TPC-DS Q12                  1134.51
TPC-DS Q13                  7455.15
TPC-DS Q14a+b              52583.06
TPC-DS Q15                  2239.03
TPC-DS Q16                  4575.63
TPC-DS Q17                  6970.03
TPC-DS Q18                  7033.56
TPC-DS Q19                  5036.13
TPC-DS Q20                  1963.22
TPC-DS Q21                  5690.08
TPC-DS Q22                111627.69
TPC-DS Q23a+b             118299.71
TPC-DS Q24a+b              11846.23
TPC-DS Q25                  7389.72
TPC-DS Q26                  3483.94
TPC-DS Q27                  5951.02
TPC-DS Q28                 13347.63
TPC-DS Q29                  7198.26
TPC-DS Q31                 16926.45
TPC-DS Q32                  1298.98
TPC-DS Q33                 10911.03
TPC-DS Q34                   774.52
TPC-DS Q35                  7675.22
TPC-DS Q36                  8382.58
TPC-DS Q37                  6053.16
TPC-DS Q38                 20623.60
TPC-DS Q39a+b              77756.41
TPC-DS Q40                  3311.95
TPC-DS Q41                 90664.06
TPC-DS Q42                  2884.14
TPC-DS Q43                  4509.95
TPC-DS Q44                  7515.71
TPC-DS Q45                  1348.52
TPC-DS Q46                  1392.16
TPC-DS Q47                 26127.03
TPC-DS Q48                  7030.54
TPC-DS Q49                 11863.25
TPC-DS Q50                  8076.05
TPC-DS Q51                 27973.61
TPC-DS Q52                  2840.38
TPC-DS Q53                  3151.07
TPC-DS Q54                  2620.48
TPC-DS Q55                  2704.18
TPC-DS Q56                  9956.28
TPC-DS Q57                 19399.61
TPC-DS Q58                  8875.07
TPC-DS Q59                  9449.10
TPC-DS Q60                 10445.78
TPC-DS Q61                  4459.86
TPC-DS Q62                  1866.80
TPC-DS Q63                  3101.14
TPC-DS Q64                 15865.04
TPC-DS Q65                 18222.22
TPC-DS Q66                 10258.60
TPC-DS Q67                 70472.91
TPC-DS Q68                  1451.97
TPC-DS Q69                  5116.28
TPC-DS Q70                 10512.15
TPC-DS Q71                  8546.26
TPC-DS Q72                 37283.95
TPC-DS Q73                   758.84
TPC-DS Q74                 25089.08
TPC-DS Q75                 22688.67
TPC-DS Q76                  6019.57
TPC-DS Q77                  8275.49
TPC-DS Q78                 45298.51
TPC-DS Q79                  5242.64
TPC-DS Q80                 11696.92
TPC-DS Q82                  6321.02
TPC-DS Q83                  1178.78
TPC-DS Q84                   510.23
TPC-DS Q85                  2914.20
TPC-DS Q86                  3898.90
TPC-DS Q87                 20672.32
TPC-DS Q88                 14858.10
TPC-DS Q89                  3587.25
TPC-DS Q90                  3761.34
TPC-DS Q91                   677.39
TPC-DS Q92                   721.17
TPC-DS Q93                  3704.76
TPC-DS Q94                  3875.99
TPC-DS Q95                 70045.35
TPC-DS Q96                  2127.91
TPC-DS Q97                  7919.80
TPC-DS Q98                  3728.64
TPC-DS Q99                  3033.00

### Loading [s]
                      timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1           1.0         1222.0         1.0      798.0    2030.0

### Geometric Mean of Medians of Timer Run [s]
                      Geo Times [s]
DBMS                               
PostgreSQL-BHT-8-1-1           7.01

### Power@Size ((3600*SF)/(geo times))
                      Power@Size [~Q/h]
DBMS                                   
PostgreSQL-BHT-8-1-1            5159.09

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                   time [s]  count    SF  Throughput@Size
DBMS               SF   num_experiment num_client                                        
PostgreSQL-BHT-8-1 10.0 1              1               5130      1  10.0           673.68

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1]]

### Ingestion - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1     3561.37     3.33         27.82                54.66

### Ingestion - Loader
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       57.09     0.07          5.31                11.39

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1     7478.18     3.51         29.49                56.24

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1       31.65     0.04           0.3                  0.3

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```

#### TPC-H Throughput Test

```bash
kubectl delete pvc bexhoma-storage-postgresql-tpcds-1
```


```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_postgresql_3.log
```

yields (after ca. 15 minutes) something like

test_tpcds_testcase_postgresql_3.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=10
    Type: tpcds
    Duration: 23147s 
    Code: 1750159279
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392867964
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393427956
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393427956
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279
PostgreSQL-BHT-8-2-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393519928
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279
PostgreSQL-BHT-8-2-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393442192
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279
PostgreSQL-BHT-8-2-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393442192
    datadisk:55265
    volume_size:100G
    volume_used:54G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750159279

### Errors (failed queries)
            PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
TPC-DS Q6                     True                    True                    True                    True                    True                    True
TPC-DS Q30                    True                    True                    True                    True                    True                    True
TPC-DS Q81                    True                    True                    True                    True                    True                    True
TPC-DS Q6
PostgreSQL-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
TPC-DS Q30
PostgreSQL-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
TPC-DS Q81
PostgreSQL-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request
PostgreSQL-BHT-8-2-2-2: numRun 1: : org.postgresql.util.PSQLException: ERROR: canceling statement due to user request

### Warnings (result mismatch)
               PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
TPC-DS Q39a+b                   False                    True                    True                    True                    True                    True

### Latency of Timer Execution [ms]
DBMS           PostgreSQL-BHT-8-1-1-1  PostgreSQL-BHT-8-1-2-1  PostgreSQL-BHT-8-1-2-2  PostgreSQL-BHT-8-2-1-1  PostgreSQL-BHT-8-2-2-1  PostgreSQL-BHT-8-2-2-2
TPC-DS Q1                     2456.38                 2469.70                 2436.25                14339.18                 2467.55                 2439.87
TPC-DS Q2                     5049.66                 5050.39                 5071.91                47856.75                 4967.57                 5007.34
TPC-DS Q3                     5393.67                 5399.32                 5500.10                60991.73                 5258.80                 5273.36
TPC-DS Q4                   106379.64               110400.24               109882.11               110941.69               110777.12               109492.45
TPC-DS Q5                     9715.65                 9824.82                 9795.04                15269.64                 9589.39                 9513.19
TPC-DS Q7                     4640.38                 4696.11                 4786.86                 7306.53                 4504.70                 4604.13
TPC-DS Q8                     3611.10                 3657.04                 3696.83                 3349.92                 3375.57                 3302.09
TPC-DS Q9                    16367.75                16607.21                16748.00                14669.80                15178.13                15319.21
TPC-DS Q10                    6205.78                 6306.41                 6421.02                 7149.30                 5924.31                 6126.72
TPC-DS Q11                   97335.50                99865.83               100436.26                99400.70                99768.93               101417.22
TPC-DS Q12                    1110.12                 1101.04                 1101.79                 1130.43                 1157.47                 1128.53
TPC-DS Q13                    7256.05                 7325.09                 7378.14                 7113.73                 7081.42                 7123.82
TPC-DS Q14a+b                53240.69                53277.69                53366.11                52731.43                52748.78                53242.74
TPC-DS Q15                    2161.79                 2220.80                 2180.87                 2119.54                 2064.19                 2169.26
TPC-DS Q16                    4440.83                 4448.57                 4475.16                 4777.87                 4305.09                 4395.52
TPC-DS Q17                    6894.15                 6918.78                 7181.62                 6891.69                 6655.20                 6827.13
TPC-DS Q18                    6977.89                 6970.12                 7077.19                 6961.44                 6865.14                 7023.47
TPC-DS Q19                    5155.43                 5121.34                 5161.84                 5065.43                 4996.37                 5216.50
TPC-DS Q20                    2009.70                 2048.48                 2014.79                 1916.81                 1903.29                 2007.40
TPC-DS Q21                    5734.20                 5777.55                 5763.22                40861.17                 5331.35                 5369.08
TPC-DS Q22                  107204.17               109667.97               108483.16               108665.23               108349.97               107861.67
TPC-DS Q23a+b                95240.69                94400.39                95100.04                95703.67                95149.35                95939.38
TPC-DS Q24a+b                11775.63                11725.45                11954.48                11438.44                11600.07                11661.13
TPC-DS Q25                    7256.25                 7203.60                 7380.91                 6870.98                 6930.24                 7000.26
TPC-DS Q26                    3409.14                 3417.37                 3478.92                 3284.86                 3371.43                 3405.56
TPC-DS Q27                    5777.23                 5911.11                 5865.82                 5654.66                 5634.64                 5779.77
TPC-DS Q28                   13170.80                13438.49                13399.34                12087.29                12268.11                12367.06
TPC-DS Q29                    7345.62                 7538.70                 7512.28                 6978.86                 7145.90                 7264.45
TPC-DS Q31                   16504.69                16534.17                16697.78                16084.99                16175.12                16674.65
TPC-DS Q32                    1208.37                 1231.37                 1304.67                 2455.93                 1020.34                 1048.53
TPC-DS Q33                   10815.68                10834.49                10814.61                10465.83                10496.43                10556.20
TPC-DS Q34                     767.72                  757.06                  755.25                  764.31                  766.85                  770.81
TPC-DS Q35                    7483.19                 7584.95                 7587.86                 7182.30                 7189.49                 7231.51
TPC-DS Q36                    1037.77                 1026.07                 1037.82                 1058.05                 1036.04                 1073.50
TPC-DS Q37                    6043.04                 6138.99                 6046.42                 5631.09                 5618.38                 5602.03
TPC-DS Q38                   20842.87                21005.73                20864.65                20046.23                21037.33                20612.58
TPC-DS Q39a+b                80141.48                78485.64                78597.98                78022.09                81625.12                80653.51
TPC-DS Q40                    3314.36                 3344.05                 3322.04                 3270.46                 3258.80                 3260.52
TPC-DS Q41                   96822.93                97363.95                80764.43                86282.49                75644.11                88283.96
TPC-DS Q42                    2853.15                 2868.44                 2879.45                 2596.81                 3098.62                 2582.16
TPC-DS Q43                    1856.21                 1826.80                 1845.28                 1835.52                 1876.18                 1901.62
TPC-DS Q44                       5.76                    7.57                    3.22                  135.84                    3.04                    3.32
TPC-DS Q45                    1334.80                 1320.33                 1300.07                 1353.10                 1380.78                 1381.54
TPC-DS Q46                    1346.64                 1343.02                 1339.49                 1349.18                 1373.64                 1395.91
TPC-DS Q47                   26977.24                26850.85                26890.46                25957.14                26443.93                25859.79
TPC-DS Q48                    7066.83                 7176.76                 7095.16                 6928.51                 6933.19                 7154.10
TPC-DS Q49                   11877.35                11996.67                12082.59                11656.19                11760.97                11722.23
TPC-DS Q50                    7855.17                 7871.39                 8243.97                 7852.53                 8222.55                 8030.90
TPC-DS Q51                   27814.01                28036.39                28289.29                27519.49                28684.01                27762.99
TPC-DS Q52                    2804.80                 2808.18                 2964.82                 2552.18                 2461.57                 2541.00
TPC-DS Q53                    3014.82                 3018.68                 2984.75                 2737.54                 2761.46                 2786.93
TPC-DS Q54                    2594.91                 2558.95                 2576.80                 2579.04                 2415.01                 2666.66
TPC-DS Q55                    2722.38                 2698.30                 2803.59                 2452.53                 2888.84                 2491.71
TPC-DS Q56                    9471.35                 9509.33                 9388.58                 9112.23                 9331.43                 9201.84
TPC-DS Q57                   19320.36                19817.78                19559.55                19176.14                19201.53                19122.27
TPC-DS Q58                    8701.34                 8742.50                 8752.68                 8259.98                 8443.12                 8632.24
TPC-DS Q59                    9460.51                 9527.66                 9557.54                 9232.88                 9474.46                 9504.37
TPC-DS Q60                   10473.95                10443.02                10452.93                10082.56                10348.60                10453.34
TPC-DS Q61                    4442.54                 4415.83                 4435.60                 4414.17                 4493.08                 4420.42
TPC-DS Q62                    1851.86                 1847.60                 1848.98                 1907.85                 1833.27                 1854.14
TPC-DS Q63                    3057.52                 3054.67                 3063.21                 2773.24                 2818.54                 2853.31
TPC-DS Q64                   15830.90                15808.64                15732.90                15484.14                15876.20                15640.85
TPC-DS Q65                   17628.63                17681.58                17655.14                16836.23                17331.19                17319.27
TPC-DS Q66                   10266.40                10859.64                10548.78                10405.56                10247.50                10393.38
TPC-DS Q67                   71277.38                71809.51                74044.88                72062.22                72215.31                72698.74
TPC-DS Q68                    1385.09                 1406.16                 1404.31                 1408.55                 1417.26                 1411.15
TPC-DS Q69                    3402.27                 3428.72                 3425.68                 3267.36                 3308.06                 3230.33
TPC-DS Q70                   10651.70                10609.08                10428.95                10533.59                10703.87                10700.89
TPC-DS Q71                    8567.70                 8514.67                 8537.76                 8266.18                 8710.74                 7993.84
TPC-DS Q72                   35531.09                35987.09                35561.93                36431.34                37070.27                36684.58
TPC-DS Q73                     761.73                  751.66                  743.09                  748.35                  776.28                  760.06
TPC-DS Q74                   28943.27                28408.24                28299.63                27872.92                28379.49                28293.25
TPC-DS Q75                   18924.05                18833.04                18701.12                18610.03                19559.28                18909.53
TPC-DS Q76                    5931.42                 6019.41                 6025.68                 5740.77                 5901.49                 5851.60
TPC-DS Q77                    8306.97                 8329.66                 8219.44                 8097.63                 8107.26                 8049.26
TPC-DS Q78                   46510.95                45380.78                45360.30                45047.98                45952.28                45614.67
TPC-DS Q79                    3822.18                 3892.09                 3824.00                 3579.99                 3577.15                 3643.18
TPC-DS Q80                   11727.05                11762.70                11612.15                11381.43                11719.36                11620.27
TPC-DS Q82                    6647.42                 6250.54                 6357.69                 5776.29                 5829.15                 5716.16
TPC-DS Q83                    1237.01                 1237.66                 1225.60                 1262.31                 1249.56                 1304.83
TPC-DS Q84                     512.32                  519.07                  514.22                  519.19                  533.34                  540.97
TPC-DS Q85                    2808.51                 2787.22                 2791.51                 2848.91                 2836.45                 2838.74
TPC-DS Q86                    3848.43                 3896.61                 3873.40                 3858.34                 3975.24                 3902.26
TPC-DS Q87                   20646.65                20908.22                21090.74                20384.72                20558.47                20614.03
TPC-DS Q88                   14823.44                14959.21                14815.70                13398.07                13687.19                13632.84
TPC-DS Q89                    3420.34                 3462.11                 3494.72                 3153.51                 3247.32                 3198.66
TPC-DS Q90                    3799.15                 3743.38                 3828.34                 3784.38                 3927.32                 3837.19
TPC-DS Q91                     686.73                  690.33                  697.87                  729.45                  727.77                  688.24
TPC-DS Q92                     722.18                  713.35                  723.12                 1173.13                  688.30                  686.60
TPC-DS Q93                    3593.74                 3660.69                 3646.92                 3310.12                 3363.69                 3425.67
TPC-DS Q94                    3914.82                 3873.85                 3887.48                 3927.99                 3905.84                 3889.10
TPC-DS Q95                   70692.91                71640.36                70953.25                71752.03                70697.33                69742.99
TPC-DS Q96                    2152.99                 2151.27                 2128.89                 1896.57                 1909.24                 1925.46
TPC-DS Q97                    8033.35                 7949.67                 7901.25                 7452.92                 7356.08                 7488.79
TPC-DS Q98                    3839.45                 3919.02                 3840.59                 3657.33                 3905.85                 3739.45
TPC-DS Q99                    2989.43                 2960.68                 3020.03                 2856.30                 2826.11                 2928.22

### Loading [s]
                        timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
PostgreSQL-BHT-8-1-1-1           1.0         1151.0         2.0      771.0    1931.0
PostgreSQL-BHT-8-1-2-1           1.0         1151.0         2.0      771.0    1931.0
PostgreSQL-BHT-8-1-2-2           1.0         1151.0         2.0      771.0    1931.0
PostgreSQL-BHT-8-2-1-1           1.0         1151.0         2.0      771.0    1931.0
PostgreSQL-BHT-8-2-2-1           1.0         1151.0         2.0      771.0    1931.0
PostgreSQL-BHT-8-2-2-2           1.0         1151.0         2.0      771.0    1931.0

### Geometric Mean of Medians of Timer Run [s]
                        Geo Times [s]
DBMS                                 
PostgreSQL-BHT-8-1-1-1           6.24
PostgreSQL-BHT-8-1-2-1           6.28
PostgreSQL-BHT-8-1-2-2           6.23
PostgreSQL-BHT-8-2-1-1           7.02
PostgreSQL-BHT-8-2-2-1           6.08
PostgreSQL-BHT-8-2-2-2           6.09

### Power@Size ((3600*SF)/(geo times))
                        Power@Size [~Q/h]
DBMS                                     
PostgreSQL-BHT-8-1-1-1            5794.75
PostgreSQL-BHT-8-1-2-1            5756.52
PostgreSQL-BHT-8-1-2-2            5804.72
PostgreSQL-BHT-8-2-1-1            5146.08
PostgreSQL-BHT-8-2-2-1            5950.47
PostgreSQL-BHT-8-2-2-2            5937.28

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                     time [s]  count    SF  Throughput@Size
DBMS                 SF   num_experiment num_client                                        
PostgreSQL-BHT-8-1-1 10.0 1              1               5091      1  10.0           678.85
PostgreSQL-BHT-8-1-2 10.0 1              2               5099      2  10.0          1355.56
PostgreSQL-BHT-8-2-1 10.0 2              1               5226      1  10.0           661.31
PostgreSQL-BHT-8-2-2 10.0 2              2               5078      2  10.0          1361.17

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS PostgreSQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1      3413.3     3.32         25.83                52.93
PostgreSQL-BHT-8-1-2      3413.3     3.32         25.83                52.93

### Ingestion - Loader
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1        57.4     0.04          5.28                11.39
PostgreSQL-BHT-8-1-2        57.4     0.04          5.28                11.39

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1     7397.68     4.04         30.20                57.62
PostgreSQL-BHT-8-1-2    14691.20     9.55         35.28                62.70
PostgreSQL-BHT-8-2-1    25579.81     4.06         30.85                62.50
PostgreSQL-BHT-8-2-2    14415.45     6.74         27.47                43.45

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       31.37     0.02          0.29                 0.30
PostgreSQL-BHT-8-1-2       38.04     0.04          0.80                 0.81
PostgreSQL-BHT-8-2-1       32.66     0.04          0.30                 0.32
PostgreSQL-BHT-8-2-2       38.16     0.55          0.80                 0.84

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
```







### MySQL

#### TPC-DS Simple

```bash
bexhoma tpcds \
  -dbms MySQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_mysql_1.log
```

yields (after ca. 10 minutes) something like

test_tpcds_testcase_mysql_1.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 1233s 
* Code: 1782320326
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.0.
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
  * disk:258698
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782320326

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |    1 |      861.00 |           2.00 |            1.00 |         89.00 |          762.00 |              8 |           0 |             | None           |             0 | False         |                4.18 |

### Execution

#### Per Connection

|                 | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| MySQL-1-1-1-1-1 | MySQL-1         | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |                3 |         24 |            0.20 |            19181.42 |            450.00 |          -1 | MySQL-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |                3 |         24 |            0.20 |            19181.42 |            450.00 |          -1 |

### Latency of Timer Execution [ms]
| Queries   |   MySQL-1-1-1-1-1 |
|:----------|------------------:|
| TPC-DS Q1 |             67.99 |
| TPC-DS Q2 |           5271.93 |
| TPC-DS Q3 |             18.44 |

### Errors (failed queries)

|                 |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:----------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MySQL-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        1.00 |        1.00 |        1.00 |        1.00 |        1.00 |        1.00 |         1.00 |         1.00 |         1.00 |         1.00 |            1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |            1.00 |            1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |            1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |         1.00 |
bexhoma : Traceback (most recent call last):
In Zeile:1 Zeichen:1
+ bexhoma tpcds `
+ ~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\tpcds.py", line 250, in <module>
    experiment.process()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\base.py", line 291, in process
    self.show_summary()
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\experiments\dbmsbenchmarker.py", line 120, in 
show_summary
    primary.show_summary(self)
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 170, in show_summary
    extra_context = self._show_extra_sections(experiment, df_aggregated_reduced)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\benchmarks\base.py", line 290, in 
_show_extra_sections
    list_errors = self.evaluator.evaluation.get_error(numQuery)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\dbmsbenchmarker\inspector.py", line 450, in get_error
    return self.benchmarks.getError(numQuery, connection)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Patrick\anaconda3\envs\bexhoma\Lib\site-packages\dbmsbenchmarker\benchmarker.py", line 1926, in getError
    return self.protocol['query'][str(query)]['errors']
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
KeyError: 'ySQL-1-1-1-1-1'
```


#### TPC-DS Monitoring

```bash
bexhoma tpcds \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_mysql_2.log
```

yields (after ca. 15 minutes) something like

test_tpcds_testcase_mysql_2.log
```markdown
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
```

#### TPC-DS Throughput Test

```
kubectl delete pvc bexhoma-storage-mysql-tpcds-1
```

```bash
bexhoma tpcds \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_mysql_3.log
```

yields (after ca. 15 minutes) something like

test_tpcds_testcase_mysql_3.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=10
    Type: tpcds
    Duration: 1381s 
    Code: 1750148746
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 100Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-BHT-8-1-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393510268
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746
MySQL-BHT-8-1-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393510692
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746
MySQL-BHT-8-1-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393510692
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746
MySQL-BHT-8-2-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393512176
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746
MySQL-BHT-8-2-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393220484
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746
MySQL-BHT-8-2-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393220484
    datadisk:8289
    volume_size:100G
    volume_used:8.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750148746

### Errors (failed queries)
No errors

### Warnings (result mismatch)
               MySQL-BHT-8-1-1-1  MySQL-BHT-8-1-2-1  MySQL-BHT-8-1-2-2  MySQL-BHT-8-2-1-1  MySQL-BHT-8-2-2-1  MySQL-BHT-8-2-2-2
TPC-DS Q39a+b               True               True               True               True              False               True

### Latency of Timer Execution [ms]
DBMS           MySQL-BHT-8-1-1-1  MySQL-BHT-8-1-2-1  MySQL-BHT-8-1-2-2  MySQL-BHT-8-2-1-1  MySQL-BHT-8-2-2-1  MySQL-BHT-8-2-2-2
TPC-DS Q1                  93.99              80.91              87.56             229.54              91.51              82.45
TPC-DS Q2                   9.65               8.10               7.65              18.15               7.36               7.91
TPC-DS Q3                   2.49               2.68               3.18              14.24               2.90               2.79
TPC-DS Q4                  18.67              21.01              18.71              18.88              20.74              21.40
TPC-DS Q5                  10.73              11.70              11.91              13.84              15.50              11.75
TPC-DS Q6                   2.09               2.88               3.41              21.14               2.73               2.87
TPC-DS Q7                   2.17               3.76               3.30              28.42               2.83               2.91
TPC-DS Q8                   3.91               5.85               5.75               7.36               4.98               5.28
TPC-DS Q9                   2.88               3.92               4.34              12.08               3.63               3.89
TPC-DS Q10                  3.56               5.69               5.96               7.50               5.58               6.53
TPC-DS Q11                  8.66              10.95              10.72              10.28              10.66              11.25
TPC-DS Q12                  2.60               3.63               3.35               2.71               3.02               3.15
TPC-DS Q13                  2.74               3.91               3.55              19.57               3.78               3.87
TPC-DS Q14a+b              21.01              17.50              23.73              30.14              21.51              23.72
TPC-DS Q15                  2.32               2.82               2.87               2.35               2.54               2.84
TPC-DS Q16                  2.69               3.32               3.53               3.98               2.71               2.71
TPC-DS Q17                  2.96               3.86               3.95               3.36               3.48               4.39
TPC-DS Q18                  2.69               3.66               3.74               3.01               3.13               4.14
TPC-DS Q19                  2.49               2.78               2.78               2.21               2.27               3.24
TPC-DS Q20                  2.17               3.03               2.70               2.02               2.20               2.48
TPC-DS Q21                  2.71               3.39               3.43              11.40               2.16               2.43
TPC-DS Q22                  2.32               2.87               2.35               1.90               1.76               1.97
TPC-DS Q23a+b              12.75              13.30              12.55              10.45              10.11              12.37
TPC-DS Q24a+b               8.26               9.59               8.68               7.60               6.97               7.95
TPC-DS Q25                  3.35               3.39               2.97               2.46               2.30               2.57
TPC-DS Q26                  2.36               2.37               2.50               1.94               1.94               2.29
TPC-DS Q27                  3.02               2.91               3.44               2.17               1.94               2.61
TPC-DS Q28                  3.69               3.72               4.31               3.21               3.05               3.55
TPC-DS Q29                  4.49               3.01               3.06               2.57               2.25               2.48
TPC-DS Q30                  4.68               4.73               5.06               3.58               3.26               3.06
TPC-DS Q31                  7.68               7.21               8.02               7.31               6.03               5.80
TPC-DS Q32                  2.24               2.18               2.88               1.98               1.49               1.81
TPC-DS Q33                  6.22               5.85               6.61               7.57               4.26               4.28
TPC-DS Q34                  3.50               2.73               2.92               2.50               2.00               2.35
TPC-DS Q35                  4.29               3.90               4.18               3.36               2.81               3.18
TPC-DS Q36                  3.22               2.80               3.12               2.21               2.00               2.20
TPC-DS Q37                  2.58               2.48               2.70               1.73               1.71               1.64
TPC-DS Q38                  3.14               2.88               2.77               1.91               2.77               2.79
TPC-DS Q39a+b               9.48               6.11               9.11               7.42               6.66               7.38
TPC-DS Q40                  2.86               2.59               2.96               2.14               2.21               2.58
TPC-DS Q41                  2.80               2.60               3.02               2.25               2.38               2.49
TPC-DS Q42                  2.65               2.05               2.26               2.31               1.73               2.10
TPC-DS Q43                  2.97               2.31               2.89               1.84               2.82               2.30
TPC-DS Q44                  3.03               2.84               2.82               3.55               2.86               2.62
TPC-DS Q45                  2.81               3.06               2.45               2.94               2.17               1.95
TPC-DS Q46                  2.75               3.32               3.11               2.75               2.20               2.15
TPC-DS Q47                  6.13               6.32               6.53               7.54               5.35               4.99
TPC-DS Q48                  2.64               2.81               2.46               2.91               2.04               2.02
TPC-DS Q49                  8.06               4.90               4.77               4.95               3.74               5.79
TPC-DS Q50                  3.09               2.88               3.29               3.19               2.09               2.63
TPC-DS Q51                  4.56               4.02               4.34               5.11               3.63               3.92
TPC-DS Q52                  2.54               1.98               2.29               2.47               1.65               1.70
TPC-DS Q53                  2.92               3.05               2.66               2.66               2.06               1.95
TPC-DS Q54                  4.58               3.68               4.05               3.82               3.17               3.28
TPC-DS Q55                  2.52               1.79               2.55               1.84               1.48               1.89
TPC-DS Q56                  5.00               4.45               4.72               4.69               3.85               3.99
TPC-DS Q57                  5.75               5.44               5.32               5.77               4.53               4.31
TPC-DS Q58                  5.38               4.91               4.90               8.15               3.75               3.73
TPC-DS Q59                  4.86               4.35               7.21               4.27               3.46               3.40
TPC-DS Q60                  4.62               4.87               4.33               4.00               3.50               3.91
TPC-DS Q61                  3.11               3.02               2.80               2.86               2.79               2.57
TPC-DS Q62                  3.37               3.31               3.70               8.59               2.56               2.48
TPC-DS Q63                  3.00               2.66               3.31               2.16               2.07               1.95
TPC-DS Q64                  7.05               7.23               7.41               8.12               5.85               5.78
TPC-DS Q65                  2.74               2.89               2.83               2.22               1.90               2.70
TPC-DS Q66                  5.81               5.82               5.90              22.32              10.37               5.56
TPC-DS Q67                  2.41               2.70               2.82               2.27               2.20               2.37
TPC-DS Q68                  3.09               2.73               2.61               2.44               2.29               2.90
TPC-DS Q69                  2.53               3.09               2.90               2.36               2.50               2.52
TPC-DS Q70                  3.08               5.55               2.51               2.27               2.19               2.36
TPC-DS Q71                  2.85               3.15               3.32               2.57               2.13               2.32
TPC-DS Q72                  3.32               2.42               2.74               2.37               2.20               2.77
TPC-DS Q73                  2.38               2.88               2.51               2.19               2.05               2.33
TPC-DS Q74                  5.54               5.39               4.92               8.53               4.43               4.61
TPC-DS Q75                  5.30               5.42               5.17               4.74               4.26               4.38
TPC-DS Q76                  2.79               3.07               2.80               3.18               1.99               2.22
TPC-DS Q77                  5.83               6.05               5.84               5.90               4.74               4.57
TPC-DS Q78                  4.20               4.18               4.06               4.36               3.28               3.46
TPC-DS Q79                  2.47               2.28               3.43               2.97               1.85               2.03
TPC-DS Q80                  4.35               4.08               5.06               5.22               3.54               3.84
TPC-DS Q81                  3.34               3.07               3.32               4.68               2.35               2.49
TPC-DS Q82                  2.46               1.96               2.31               2.17               1.59               1.50
TPC-DS Q83                  3.82               3.62               3.81               5.89               3.01               2.73
TPC-DS Q84                  2.28               2.36               2.45               1.82               1.54               1.64
TPC-DS Q85                  3.38               3.52               3.48               3.09               2.37               2.47
TPC-DS Q86                  2.66               3.04               2.15               3.28               1.74               1.69
TPC-DS Q87                  2.73               2.91               2.75               2.01               1.82               1.92
TPC-DS Q88                  6.07               6.06               5.47               5.06               5.53               5.68
TPC-DS Q89                  3.12               3.12               2.48               1.86               2.03               2.23
TPC-DS Q90                  2.78               2.68               2.51               1.86               1.76               1.89
TPC-DS Q91                  2.44               2.93               2.46               4.06               1.95               1.92
TPC-DS Q92                  2.25               2.40               2.34               2.17               1.61               1.56
TPC-DS Q93                  2.62               2.65               2.54               2.39               1.73               7.51
TPC-DS Q94                  2.92               2.62               2.60               2.32               1.78               2.32
TPC-DS Q95                  3.23               3.13               3.46               2.70               2.34               2.80
TPC-DS Q96                  2.33               2.14               1.99               1.34               1.89               1.78
TPC-DS Q97                  3.17               3.42               3.79               3.30               3.00               2.81
TPC-DS Q98                  2.63               2.72               2.70               1.56               2.45               2.15
TPC-DS Q99                  2.69               2.69               2.80               1.59               2.31               2.18

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MySQL-BHT-8-1-1-1           0.0           26.0        21.0      253.0     308.0
MySQL-BHT-8-1-2-1           0.0           26.0        21.0      253.0     308.0
MySQL-BHT-8-1-2-2           0.0           26.0        21.0      253.0     308.0
MySQL-BHT-8-2-1-1           0.0           26.0        21.0      253.0     308.0
MySQL-BHT-8-2-2-1           0.0           26.0        21.0      253.0     308.0
MySQL-BHT-8-2-2-2           0.0           26.0        21.0      253.0     308.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MySQL-BHT-8-1-1-1            0.0
MySQL-BHT-8-1-2-1            0.0
MySQL-BHT-8-1-2-2            0.0
MySQL-BHT-8-2-1-1            0.0
MySQL-BHT-8-2-2-1            0.0
MySQL-BHT-8-2-2-2            0.0

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MySQL-BHT-8-1-1-1         9592942.85
MySQL-BHT-8-1-2-1         9429060.52
MySQL-BHT-8-1-2-2         9236386.35
MySQL-BHT-8-2-1-1         8773386.10
MySQL-BHT-8-2-2-1        11741502.08
MySQL-BHT-8-2-2-2        10964590.31

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                time [s]  count    SF  Throughput@Size
DBMS            SF   num_experiment num_client                                        
MySQL-BHT-8-1-1 10.0 1              1                  7      1  10.0        509142.86
MySQL-BHT-8-1-2 10.0 1              2                 17      2  10.0        419294.12
MySQL-BHT-8-2-1 10.0 2              1                  4      1  10.0        891000.00
MySQL-BHT-8-2-2 10.0 2              2                  4      2  10.0       1782000.00

### Workflow

#### Actual
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MySQL-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1      188.77     1.11         37.69                45.73
MySQL-BHT-8-1-2      188.77     1.11         37.69                45.73

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1           0        0           0.0                  0.0
MySQL-BHT-8-1-2           0        0           0.0                  0.0

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00     0.00         37.69                45.73
MySQL-BHT-8-1-2        1.71     0.00         37.70                45.73
MySQL-BHT-8-2-1      475.11     0.00         75.15                91.12
MySQL-BHT-8-2-2        0.00     0.02         37.47                45.41

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-1-2        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-1        0.00      0.0           0.0                  0.0
MySQL-BHT-8-2-2        0.03      0.0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Workflow as planned
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
```






### MariaDB

#### TPC-DS Simple

```bash
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_mariadb_1.log
```

yields (after ca. 10 minutes) something like

test_tpcds_testcase_mariadb_1.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
    Type: tpcds
    Duration: 24711s 
    Code: 1750183466
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.8.
    Experiment is limited to DBMS ['MariaDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-BHT-8-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:398969780
    datadisk:4560
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750183466

### Errors (failed queries)
            MariaDB-BHT-8-1-1
TPC-DS Q72               True
TPC-DS Q94               True
TPC-DS Q95               True
TPC-DS Q72
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=308) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q94
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=308) Query execution was interrupted (max_statement_time exceeded)
TPC-DS Q95
MariaDB-BHT-8-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=308) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MariaDB-BHT-8-1-1
TPC-DS Q1                 138.07
TPC-DS Q2             1031952.02
TPC-DS Q3               10970.49
TPC-DS Q4              141559.69
TPC-DS Q5               84722.06
TPC-DS Q6               36477.14
TPC-DS Q7               16159.63
TPC-DS Q8               26581.17
TPC-DS Q9               12795.33
TPC-DS Q10              36886.47
TPC-DS Q11              60153.03
TPC-DS Q12                942.88
TPC-DS Q13               3921.43
TPC-DS Q14a+b          254359.72
TPC-DS Q15                544.75
TPC-DS Q16             147909.07
TPC-DS Q17              72031.27
TPC-DS Q18               7311.15
TPC-DS Q19               9326.05
TPC-DS Q20               1776.94
TPC-DS Q21             832438.22
TPC-DS Q22            1189542.81
TPC-DS Q23a+b          274616.02
TPC-DS Q24a+b            5296.89
TPC-DS Q25              15158.39
TPC-DS Q26              22734.26
TPC-DS Q27              17158.39
TPC-DS Q28               9198.41
TPC-DS Q29               7359.12
TPC-DS Q30                683.79
TPC-DS Q31              44905.40
TPC-DS Q32                 24.03
TPC-DS Q33              12044.36
TPC-DS Q34              12164.81
TPC-DS Q35              33395.67
TPC-DS Q36              10215.46
TPC-DS Q37              13556.69
TPC-DS Q38              26178.26
TPC-DS Q39a+b            4775.12
TPC-DS Q40              13216.42
TPC-DS Q41                180.67
TPC-DS Q42               9073.49
TPC-DS Q43              14420.94
TPC-DS Q44                  2.06
TPC-DS Q45               7270.04
TPC-DS Q46              12534.97
TPC-DS Q47              62184.13
TPC-DS Q48               6665.26
TPC-DS Q49              24937.90
TPC-DS Q50                694.73
TPC-DS Q51              26402.20
TPC-DS Q52               9496.63
TPC-DS Q53               4616.10
TPC-DS Q54              23855.73
TPC-DS Q55               8819.64
TPC-DS Q56              11613.84
TPC-DS Q57              20204.02
TPC-DS Q58              25970.53
TPC-DS Q59              36009.89
TPC-DS Q60              12341.48
TPC-DS Q61              14507.27
TPC-DS Q62               7047.47
TPC-DS Q63               4763.82
TPC-DS Q64               2027.84
TPC-DS Q65              22476.62
TPC-DS Q66               6350.39
TPC-DS Q67              25235.48
TPC-DS Q68              12212.56
TPC-DS Q69              27459.51
TPC-DS Q70              32717.91
TPC-DS Q71              11922.45
TPC-DS Q73              11311.98
TPC-DS Q74              59872.46
TPC-DS Q75              16557.24
TPC-DS Q76               1644.38
TPC-DS Q77              22336.18
TPC-DS Q78              32677.73
TPC-DS Q79              12277.58
TPC-DS Q80              16885.87
TPC-DS Q81                763.47
TPC-DS Q82               3064.38
TPC-DS Q83               2916.39
TPC-DS Q84                458.59
TPC-DS Q85                424.49
TPC-DS Q86               3913.42
TPC-DS Q87              26083.75
TPC-DS Q88              96013.42
TPC-DS Q89               4551.46
TPC-DS Q90               5255.21
TPC-DS Q91                 91.43
TPC-DS Q92               6653.20
TPC-DS Q93                153.25
TPC-DS Q96               9766.81
TPC-DS Q97              19185.91
TPC-DS Q98               5837.43
TPC-DS Q99              20435.34

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1           1.0          618.0         5.0    14777.0   15408.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MariaDB-BHT-8-1-1            9.7

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MariaDB-BHT-8-1-1             371.68

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                               time [s]  count   SF  Throughput@Size
DBMS            SF  num_experiment num_client                                       
MariaDB-BHT-8-1 1.0 1              1               8978      1  1.0            38.49

### Workflow

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MariaDB-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
```


#### TPC-DS Monitoring

```bash
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_mariadb_2.log
```

yields (after ca. 15 minutes) something like

test_tpcds_testcase_mariadb_2.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 2482s 
    Code: 1748916422
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-BHT-8-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:319525344
    datadisk:2091
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748916422

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1
Pricing Summary Report (TPC-H Q1)                             26007.81
Minimum Cost Supplier Query (TPC-H Q2)                         1424.68
Shipping Priority (TPC-H Q3)                                   5752.96
Order Priority Checking Query (TPC-H Q4)                       1470.50
Local Supplier Volume (TPC-H Q5)                               3638.64
Forecasting Revenue Change (TPC-H Q6)                          3132.16
Forecasting Revenue Change (TPC-H Q7)                          3854.64
National Market Share (TPC-H Q8)                               6830.26
Product Type Profit Measure (TPC-H Q9)                         6253.92
Forecasting Revenue Change (TPC-H Q10)                         2856.04
Important Stock Identification (TPC-H Q11)                      422.14
Shipping Modes and Order Priority (TPC-H Q12)                 11440.37
Customer Distribution (TPC-H Q13)                             10250.61
Forecasting Revenue Change (TPC-H Q14)                        30218.01
Top Supplier Query (TPC-H Q15)                                 6329.73
Parts/Supplier Relationship (TPC-H Q16)                         647.58
Small-Quantity-Order Revenue (TPC-H Q17)                        159.29
Large Volume Customer (TPC-H Q18)                             11382.62
Discounted Revenue (TPC-H Q19)                                  368.73
Potential Part Promotion (TPC-H Q20)                            734.58
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)          196513.50
Global Sales Opportunity Query (TPC-H Q22)                      459.38

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1           1.0          259.0         2.0     1520.0    1790.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MariaDB-BHT-8-1-1            3.5

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
MariaDB-BHT-8-1-1            1062.48

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                              time [s]  count  SF  Throughput@Size
DBMS            SF num_experiment num_client                                      
MariaDB-BHT-8-1 1  1              1                335      1   1           236.42

### Workflow

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MariaDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1     1526.26     2.02          9.69                  9.7

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1        7.86     0.02          0.52                 1.16

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1      321.09      1.0          9.81                 9.82

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1       14.85     0.05          0.26                 0.26

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### TPC-DS Throughput Test

```bash
kubectl delete pvc bexhoma-storage-mariadb-tpcds-1
```

```bash
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_mariadb_3.log
```

yields (after ca. 15 minutes) something like

test_tpcds_testcase_mariadb_3.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
    Type: tpch
    Duration: 6081s 
    Code: 1748919033
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=1) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 1200.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MariaDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MariaDB-BHT-8-1-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515964
    datadisk:2090
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-1-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515968
    datadisk:2090
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-1-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515968
    datadisk:2090
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-2-1-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515956
    datadisk:2095
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-2-2-1 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515960
    datadisk:2095
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033
MariaDB-BHT-8-2-2-2 uses docker image mariadb:11.4.7
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317515960
    datadisk:2095
    volume_size:30G
    volume_used:2.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1748919033

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 MariaDB-BHT-8-1-1-1  MariaDB-BHT-8-1-2-1  MariaDB-BHT-8-1-2-2  MariaDB-BHT-8-2-1-1  MariaDB-BHT-8-2-2-1  MariaDB-BHT-8-2-2-2
Pricing Summary Report (TPC-H Q1)                               25974.35             24684.85             24739.11             25744.04             25961.78             25820.11
Minimum Cost Supplier Query (TPC-H Q2)                           1453.22              1677.86              1703.46              1762.40              1618.89              1619.03
Shipping Priority (TPC-H Q3)                                     5221.88              6529.53              6493.69              7216.41              6423.40              6417.20
Order Priority Checking Query (TPC-H Q4)                         1075.72              1336.18              1341.60              1323.22              1288.26              1287.75
Local Supplier Volume (TPC-H Q5)                                 3287.17              3783.79              3852.58              3482.38              3748.09              3748.27
Forecasting Revenue Change (TPC-H Q6)                            2801.76              3999.80              3944.80              3313.50              2961.49              2943.89
Forecasting Revenue Change (TPC-H Q7)                            3639.82              3945.00              4008.61              3805.95              4300.03              4300.00
National Market Share (TPC-H Q8)                                 6468.87              7603.58              7262.87              6879.16              7697.18              7697.15
Product Type Profit Measure (TPC-H Q9)                           5802.95              6661.06              6938.45              6114.94              6373.02              6372.93
Forecasting Revenue Change (TPC-H Q10)                           2955.81              2928.45              2966.85              2984.05              3205.20              3202.19
Important Stock Identification (TPC-H Q11)                        382.23               442.78               435.66               413.34               494.31               498.47
Shipping Modes and Order Priority (TPC-H Q12)                   11413.65             12428.21             12536.94             11768.67             12604.75             12604.79
Customer Distribution (TPC-H Q13)                                9852.55             11791.98             12055.63              9988.15             11283.96             11281.52
Forecasting Revenue Change (TPC-H Q14)                          31100.58             36921.43             40084.43             30354.96             35245.42             35245.52
Top Supplier Query (TPC-H Q15)                                   6228.19              6508.01              6396.66              6582.36              6575.85              6504.29
Parts/Supplier Relationship (TPC-H Q16)                           629.99               643.59               623.90               671.43               665.07               664.95
Small-Quantity-Order Revenue (TPC-H Q17)                          160.92               150.71               153.73               146.73               151.15               150.50
Large Volume Customer (TPC-H Q18)                               10162.65             11347.40             11718.83             10464.66             11239.03             11334.00
Discounted Revenue (TPC-H Q19)                                    264.98               285.77               294.18               287.03               272.64               275.01
Potential Part Promotion (TPC-H Q20)                              527.27               577.32               685.68               586.09               634.04               635.37
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)            194454.66            222543.33            222766.92            197089.34            213727.42            213737.84
Global Sales Opportunity Query (TPC-H Q22)                        402.35               395.79               372.82               397.17               442.14               441.05

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MariaDB-BHT-8-1-1-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-1-2-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-1-2-2           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-2-1-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-2-2-1           1.0          696.0         5.0     3089.0    3797.0
MariaDB-BHT-8-2-2-2           1.0          696.0         5.0     3089.0    3797.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MariaDB-BHT-8-1-1-1           3.22
MariaDB-BHT-8-1-2-1           3.59
MariaDB-BHT-8-1-2-2           3.64
MariaDB-BHT-8-2-1-1           3.44
MariaDB-BHT-8-2-2-1           3.58
MariaDB-BHT-8-2-2-2           3.60

### Power@Size ((3600*SF)/(geo times))
                     Power@Size [~Q/h]
DBMS                                  
MariaDB-BHT-8-1-1-1            1154.15
MariaDB-BHT-8-1-2-1            1035.86
MariaDB-BHT-8-1-2-2            1022.45
MariaDB-BHT-8-2-1-1            1080.60
MariaDB-BHT-8-2-2-1            1036.64
MariaDB-BHT-8-2-2-2            1036.84

### Throughput@Size ((queries*streams*3600*SF)/(span of time))
                                                time [s]  count  SF  Throughput@Size
DBMS              SF num_experiment num_client                                      
MariaDB-BHT-8-1-1 1  1              1                328      1   1           241.46
MariaDB-BHT-8-1-2 1  1              2                376      2   1           421.28
MariaDB-BHT-8-2-1 1  2              1                338      1   1           234.32
MariaDB-BHT-8-2-2 1  2              2                363      2   1           436.36

### Workflow

#### Actual
DBMS MariaDB-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MariaDB-BHT-8 - Pods [[1, 2], [1, 2]]

### Ingestion - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1     2263.77     2.11          9.81                 9.84
MariaDB-BHT-8-1-2     2263.77     2.11          9.81                 9.84

### Ingestion - Loader
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1        7.69     0.01           0.5                 1.16
MariaDB-BHT-8-1-2        7.69     0.01           0.5                 1.16

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1      318.25      1.0          9.88                 9.91
MariaDB-BHT-8-1-2      678.67      2.0          9.89                 9.92
MariaDB-BHT-8-2-1     3375.23      1.0         12.41                12.63
MariaDB-BHT-8-2-2      650.38      2.0          2.56                 2.81

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MariaDB-BHT-8-1-1       14.94     0.00          0.26                 0.26
MariaDB-BHT-8-1-2       25.00     0.01          0.72                 0.74
MariaDB-BHT-8-2-1       14.09     0.01          0.25                 0.27
MariaDB-BHT-8-2-2       31.69     0.06          0.75                 0.78

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```


















## Benchbase

### PostgreSQL

#### Benchbase Simple

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_postgresql_1.log
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_postgresql_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 801s 
    Code: 1749126830
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:363141144
    datadisk:4324
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749126830

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0           0                       1838.93                    1830.73         0.0                                                      19784.0                                               8693.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      166.0        1.0   1.0         346.987952

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Benchbase Persistency


Make sure, the database does not exist:
```bash
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 10
```

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 1 \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_postgresql_2.log
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_postgresql_2.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 676s 
    Code: 1749127700
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 1 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358233172
    datadisk:9476
    volume_size:30G
    volume_used:9.3G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749127700
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358233600
    datadisk:8733
    volume_size:30G
    volume_used:8.6G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1749127700

### Execution
                         experiment_run  terminals  target  pod_count  time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1         16    8192          1  60.0           0                        769.17                     765.82         0.0                                                      32679.0                                              20781.0
PostgreSQL-1-1-1024-2-1               2         16    8192          1  60.0           0                        877.26                     873.60         0.0                                                      30925.0                                              18222.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1], [1]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1-1      175.0        1.0   1.0         329.142857
PostgreSQL-1-1-1024-2-1      175.0        1.0   1.0         329.142857

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Benchbase Monitoring

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_postgresql_3.log
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_postgresql_3.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 858s 
    Code: 1749128420
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-1-1-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:362668492
    datadisk:4324
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749128420

### Execution
                       experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1               1         16    8192          1  300.0           0                       1838.63                    1830.43         0.0                                                      20064.0                                               8695.0

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1]]

### Loading
                       time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1      173.0        1.0   1.0         332.947977

### Ingestion - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      527.31     6.71          3.98                 5.37

### Ingestion - Loader
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1592.36        0          0.98                 0.98

### Execution - SUT
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1     1961.93     7.15          4.66                 6.75

### Execution - Benchmarker
                       CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1      980.15     3.38          1.42                 1.42

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### Benchbase Complex

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 2 \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_postgresql_4.log
```

yields (after ca. 30 minutes) something like

test_benchbase_testcase_postgresql_4.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1936s 
    Code: 1749129321
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 2 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [8] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-1-1-1024-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358240476
    datadisk:7963
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358240992
    datadisk:8051
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-1-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358241380
    datadisk:8217
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-1-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358241172
    datadisk:8331
    volume_size:30G
    volume_used:7.8G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358490124
    datadisk:8476
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358491144
    datadisk:8551
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358491472
    datadisk:8712
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
                code:1749129321
PostgreSQL-1-1-1024-2-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358245748
    datadisk:8821
    volume_size:30G
    volume_used:8.3G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
                code:1749129321

### Execution
                         experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
PostgreSQL-1-1-1024-1-1               1          8    8192          1  120.0           0                        856.82                     853.06         0.0                                                      15454.0                                              9325.00
PostgreSQL-1-1-1024-1-2               1         16   16384          2  120.0           1                       1650.73                    1635.38         0.0                                                      21337.0                                              9683.50
PostgreSQL-1-1-1024-1-3               1          8    8192          2  120.0           0                       1144.57                    1133.88         0.0                                                      14775.0                                              6976.50
PostgreSQL-1-1-1024-1-4               1         16   16384          4  120.0           2                       1488.36                    1466.36         0.0                                                      23439.0                                             10734.75
PostgreSQL-1-1-1024-2-1               2          8    8192          1  120.0           0                        733.64                     730.11         0.0                                                      21145.0                                             10892.00
PostgreSQL-1-1-1024-2-2               2         16   16384          2  120.0           0                       1622.52                    1607.08         0.0                                                      20943.0                                              9848.00
PostgreSQL-1-1-1024-2-3               2          8    8192          2  120.0           1                       1091.28                    1080.81         0.0                                                      15040.0                                              7317.00
PostgreSQL-1-1-1024-2-4               2         16   16384          4  120.0           1                       1434.22                    1412.25         0.0                                                      23812.0                                             11140.50

### Workflow

#### Actual
DBMS PostgreSQL-1-1-1024 - Pods [[4, 2, 2, 1], [2, 4, 2, 1]]

#### Planned
DBMS PostgreSQL-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                         time_load  terminals  pods  Throughput [SF/h]
PostgreSQL-1-1-1024-1-1      175.0        1.0   1.0         329.142857
PostgreSQL-1-1-1024-1-2      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-1-3      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-1-4      175.0        1.0   4.0         329.142857
PostgreSQL-1-1-1024-2-1      175.0        1.0   1.0         329.142857
PostgreSQL-1-1-1024-2-2      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-2-3      175.0        1.0   2.0         329.142857
PostgreSQL-1-1-1024-2-4      175.0        1.0   4.0         329.142857

### Execution - SUT
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      329.70     0.76          3.23                 7.68
PostgreSQL-1-1-1024-1-2      691.98     6.95          3.72                 8.37
PostgreSQL-1-1-1024-1-3      448.58     3.44          3.89                 8.68
PostgreSQL-1-1-1024-1-4      727.81     5.49          4.17                 9.10
PostgreSQL-1-1-1024-2-1     2460.89     0.06          6.37                11.45
PostgreSQL-1-1-1024-2-2      631.05     0.00          3.66                 8.72
PostgreSQL-1-1-1024-2-3      349.81     0.00          3.87                 9.06
PostgreSQL-1-1-1024-2-4      545.74     6.33          4.17                 9.50

### Execution - Benchmarker
                         CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-1-1-1024-1-1      166.09     2.02          0.58                 0.58
PostgreSQL-1-1-1024-1-2      394.05     1.60          1.75                 1.75
PostgreSQL-1-1-1024-1-3      242.09     2.05          1.91                 1.91
PostgreSQL-1-1-1024-1-4      284.79     1.82          2.47                 2.47
PostgreSQL-1-1-1024-2-1       77.49     0.00          0.32                 0.32
PostgreSQL-1-1-1024-2-2      281.63     1.62          1.21                 1.21
PostgreSQL-1-1-1024-2-3      197.94     0.00          1.59                 1.59
PostgreSQL-1-1-1024-2-4      222.02     0.75          1.97                 1.98

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```











### MySQL

#### Benchbase Simple

```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_mysql_1.log
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mysql_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
    Type: benchbase
    Duration: 763s 
    Code: 1767873545
    Intro: Benchbase runs a TPC-C experiment.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker21.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [160] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-1-1-1024-1 uses docker image mysql:8.4.0
    RAM:608117153792
    Cores:64
    host:6.8.0-90-generic
    node:cl-worker21
    disk:165887
    datadisk:35712
    cpu_list:0-63
    args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=300', '--innodb-io-capacity_max=600', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1767873545
                TENANT_VOL:False

### Execution

#### Per Pod
                    experiment_run  terminals  target  client  child   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
connection_pod                                                                                                                                                                                                                                                                
MySQL-1-1-1024-1-1               1        160    8192       1      1  300.0           0                   5553.136283                5461.042956         0.0                                                      56047.0                                              28802.0

#### Aggregated Parallel
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1        160    8192          1  300.0           0                       5553.14                    5461.04         0.0                                                      56047.0                                              28802.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1      156.0        1.0   1.0         369.230769

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Benchbase Persistency


Make sure, the database does not exist:
```bash
kubectl delete pvc bexhoma-storage-mysql-benchbase-16
sleep 10
```

```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 1 \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_mysql_2.log
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mysql_2.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 8930s 
    Code: 1748934307
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 1 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-1-1-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590004
    datadisk:11132
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748934307
MySQL-1-1-1024-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590184
    datadisk:11165
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1748934307

### Execution
                    experiment_run  terminals  target  pod_count  time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1-1               1         16    8192          1  60.0           0                          1.00                       1.23         0.0                                                   47671586.0                                            8847058.0
MySQL-1-1-1024-2-1               2         16    8192          1  60.0           0                          4.52                       4.78         0.0                                                   15558733.0                                            3001960.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1], [1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1], [1]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1-1     7641.0        1.0   1.0            7.53828
MySQL-1-1-1024-2-1     7641.0        1.0   1.0            7.53828

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Workflow as planned
```


#### Benchbase Monitoring

```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_mysql_3.log
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mysql_3.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 1530s 
    Code: 1748943250
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 5 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-1-1-1024-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:328989148
    datadisk:11132
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748943250

### Execution
                  experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1               1         16    8192          1  300.0           0                        112.58                     112.09         0.0                                                     438246.0                                             142078.0

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1]]

### Loading
                  time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1      765.0        1.0   1.0          75.294118

### Ingestion - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1542.16     2.22         37.43                37.47

### Ingestion - Loader
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1     1341.21     3.77          1.33                 1.33

### Execution - SUT
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1      436.01     1.81         23.42                27.21

### Execution - Benchmarker
                  CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1      167.69     0.59          0.82                 0.82

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### Benchbase Complex

```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 2 \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_mysql_4.log
```

yields (after ca. 30 minutes) something like

test_benchbase_testcase_mysql_4.log
```markdown
## Show Summary

### Workload
Benchbase Workload SF=16
    Type: benchbase
    Duration: 2183s 
    Code: 1748944810
    Benchbase runs the TPC-C benchmark.
    This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
    Benchbase data is generated and loaded using several threads.
    Benchmark is 'tpcc'. Scaling factor is 16. Benchmarking runs for 2 minutes. Target is based on multiples of '1024'. Factors for benchmarking are [8].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [1] threads, split into [1] pods.
    Benchmarking is tested with [8] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-1-1-1024-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590204
    datadisk:11187
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-1-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590204
    datadisk:11220
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-1-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590208
    datadisk:11256
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-1-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590208
    datadisk:11308
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590216
    datadisk:11339
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590216
    datadisk:11374
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590220
    datadisk:11458
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
                code:1748944810
MySQL-1-1-1024-2-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:317590396
    datadisk:11489
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
                code:1748944810

### Execution
                    experiment_run  terminals  target  pod_count   time  num_errors  Throughput (requests/second)  Goodput (requests/second)  efficiency  Latency Distribution.95th Percentile Latency (microseconds)  Latency Distribution.Average Latency (microseconds)
MySQL-1-1-1024-1-1               1          8    8192          1  120.0           0                         36.02                      35.85         0.0                                                     610937.0                                            220741.00
MySQL-1-1-1024-1-2               1         16   16384          2  120.0           0                         39.64                      39.47         0.0                                                     820427.0                                            285537.50
MySQL-1-1-1024-1-3               1          8    8192          2  120.0           0                         69.92                      69.46         0.0                                                     394377.0                                            114272.50
MySQL-1-1-1024-1-4               1         16   16384          4  120.0           0                         37.22                      36.94         0.0                                                    1876083.0                                            429714.25
MySQL-1-1-1024-2-1               2          8    8192          1  120.0           0                         45.04                      44.85         0.0                                                     500014.0                                            177493.00
MySQL-1-1-1024-2-2               2         16   16384          2  120.0           0                        106.22                     105.62         0.0                                                     483418.0                                            150073.00
MySQL-1-1-1024-2-3               2          8    8192          2  120.0           0                         39.84                      39.67         0.0                                                     952677.0                                            200600.50
MySQL-1-1-1024-2-4               2         16   16384          4  120.0           0                         49.48                      49.02         0.0                                                     940977.0                                            213649.25

### Workflow

#### Actual
DBMS MySQL-1-1-1024 - Pods [[1, 2, 2, 4], [4, 2, 2, 1]]

#### Planned
DBMS MySQL-1-1-1024 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                    time_load  terminals  pods  Throughput [SF/h]
MySQL-1-1-1024-1-1     7641.0        1.0   1.0            7.53828
MySQL-1-1-1024-1-2     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-1-3     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-1-4     7641.0        1.0   4.0            7.53828
MySQL-1-1-1024-2-1     7641.0        1.0   1.0            7.53828
MySQL-1-1-1024-2-2     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-2-3     7641.0        1.0   2.0            7.53828
MySQL-1-1-1024-2-4     7641.0        1.0   4.0            7.53828

### Execution - SUT
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1-1       50.42     0.79         37.96                45.81
MySQL-1-1-1024-1-2       78.16     0.28         38.17                46.08
MySQL-1-1-1024-1-3       86.48     0.10         38.23                46.20
MySQL-1-1-1024-1-4       49.59     0.73         38.27                46.26
MySQL-1-1-1024-2-1       51.82     0.00         37.95                45.98
MySQL-1-1-1024-2-2      112.04     1.48         38.17                46.30
MySQL-1-1-1024-2-3      100.06     0.47         38.21                46.40
MySQL-1-1-1024-2-4      123.16     1.35         38.26                46.51

### Execution - Benchmarker
                    CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-1-1-1024-1-1       33.15     0.00          0.28                 0.28
MySQL-1-1-1024-1-2       61.65     0.00          0.80                 0.80
MySQL-1-1-1024-1-3       33.28     0.00          1.19                 1.19
MySQL-1-1-1024-1-4       38.84     0.08          1.45                 1.45
MySQL-1-1-1024-2-1       35.98     0.00          0.30                 0.30
MySQL-1-1-1024-2-2       87.11     0.37          0.97                 0.97
MySQL-1-1-1024-2-3       35.98     0.07          1.18                 1.18
MySQL-1-1-1024-2-4      117.93     0.51          4.46                 4.47

### Tests
TEST passed: Throughput (requests/second) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```











### MariaDB

#### Benchbase Simple

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_mariadb_1.log
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mariadb_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 881s 
* Code: 1780043924
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:59980
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780043924

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1]]

#### Planned

* DBMS MariaDB-1 - Pods [[1]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      360.00 |           1.00 |            0.00 |        159.00 |          200.00 |              1 |           1 |          | None           |             0 | False         |              160.00 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1 |             1.00 |      160.00 |  8192.00 |     1.00 |    1.00 | 300.00 |         0.00 |                        2245.07 |                     2203.18 |         0.00 |                                                     280943.00 |                                              71237.00 |

#### Per Phase

| DBMS          |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 |             1.00 |      160.00 |  8192.00 |        1.00 | 300.00 |         0.00 |                        2245.07 |                     2203.18 |         0.00 |                                                     280943.00 |                                              71237.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```


#### Benchbase Persistency


Make sure, the database does not exist:
```bash
kubectl delete pvc bexhoma-storage-mariadb-benchbase-16
sleep 10
```

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 1 \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_mariadb_2.log
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mariadb_2.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1501s 
* Code: 1780044810
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 1 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780044810
* MariaDB-1-2-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780044810

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1], [1]]

#### Planned

* DBMS MariaDB-1 - Pods [[1], [1]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |     1087.00 |           1.00 |            0.00 |        525.00 |          561.00 |              1 |           1 |          | None           |             0 | False         |               52.99 |
| MariaDB-1-2 |                2 |   16 |     1087.00 |           1.00 |            0.00 |        525.00 |          561.00 |              1 |           1 |          | None           |             0 | False         |               52.99 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1 |             1.00 |      160.00 |  8192.00 |     1.00 |    1.00 |  60.00 |         0.00 |                         480.55 |                      475.38 |         0.00 |                                                     294087.00 |                                             330964.00 |
| MariaDB-1-2-1-1 |             2.00 |      160.00 |  8192.00 |     1.00 |    1.00 |  60.00 |        10.00 |                         560.95 |                      552.80 |         0.00 |                                                     222509.00 |                                             246026.00 |

#### Per Phase

| DBMS          |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 |             1.00 |      160.00 |  8192.00 |        1.00 |  60.00 |         0.00 |                         480.55 |                      475.38 |         0.00 |                                                     294087.00 |                                             330964.00 |
| MariaDB-1-2-1 |             2.00 |      160.00 |  8192.00 |        1.00 |  60.00 |        10.00 |                         560.95 |                      552.80 |         0.00 |                                                     222509.00 |                                             246026.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```


#### Benchbase Monitoring

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_mariadb_3.log
```

yields (after ca. 10 minutes) something like

test_benchbase_testcase_mariadb_3.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 835s 
* Code: 1780046317
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:59976
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780046317

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1]]

#### Planned

* DBMS MariaDB-1 - Pods [[1]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      324.00 |           1.00 |            0.00 |        155.00 |          168.00 |              1 |           1 |          | None           |             0 | False         |              177.78 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1 |             1.00 |      160.00 |  8192.00 |     1.00 |    1.00 | 300.00 |         0.00 |                        2253.50 |                     2211.06 |         0.00 |                                                     276887.00 |                                              70937.00 |

#### Per Phase

| DBMS          |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 |             1.00 |      160.00 |  8192.00 |        1.00 | 300.00 |         0.00 |                        2253.50 |                     2211.06 |         0.00 |                                                     276887.00 |                                              70937.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       544.89 |     10.43 |           6.98 |                  7.08 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |      1670.60 |     14.66 |           0.24 |                  0.24 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |      5665.73 |     20.59 |           7.64 |                  7.74 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |      1056.45 |      4.00 |           0.79 |                  0.79 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```

#### Benchbase Complex

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 2 \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_testcase_mariadb_4.log
```

yields (after ca. 30 minutes) something like

test_benchbase_testcase_mariadb_4.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2194s 
* Code: 1780047177
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-1-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-1-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-1-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-2-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.1G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-2-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.1G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-2-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.1G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177
* MariaDB-1-2-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:2.1G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780047177

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

#### Planned

* DBMS MariaDB-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |     1087.00 |           1.00 |            0.00 |        525.00 |          561.00 |              0 |           1 |          | None           |             0 | False         |               52.99 |
| MariaDB-1-2 |                2 |   16 |     1087.00 |           1.00 |            0.00 |        525.00 |          561.00 |              0 |           1 |          | None           |             0 | False         |               52.99 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   terminals |   target |   client |   child |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|-----------------:|------------:|---------:|---------:|--------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1 |             1.00 |      160.00 |  8192.00 |     1.00 |    1.00 | 120.00 |        43.00 |                         383.78 |                      377.61 |         0.00 |                                                     101269.00 |                                             294908.00 |
| MariaDB-1-1-2-1 |             1.00 |      160.00 |  8192.00 |     2.00 |    1.00 | 120.00 |        22.00 |                         187.88 |                      185.97 |         0.00 |                                                    3123314.00 |                                             850463.00 |
| MariaDB-1-1-2-2 |             1.00 |      160.00 |  8192.00 |     2.00 |    2.00 | 120.00 |        16.00 |                         215.47 |                      213.08 |         0.00 |                                                    2826271.00 |                                             740682.00 |
| MariaDB-1-1-3-1 |             1.00 |       80.00 |  4096.00 |     3.00 |    1.00 | 120.00 |         0.00 |                         150.78 |                      148.98 |         0.00 |                                                    2582112.00 |                                             530471.00 |
| MariaDB-1-1-3-2 |             1.00 |       80.00 |  4096.00 |     3.00 |    2.00 | 120.00 |         0.00 |                         148.27 |                      146.20 |         0.00 |                                                    2596819.00 |                                             534672.00 |
| MariaDB-1-1-4-1 |             1.00 |       80.00 |  4096.00 |     4.00 |    1.00 | 120.00 |       110.00 |                          91.65 |                       89.84 |         0.00 |                                                     424148.00 |                                             719005.00 |
| MariaDB-1-1-4-2 |             1.00 |       80.00 |  4096.00 |     4.00 |    2.00 | 120.00 |       100.00 |                          75.59 |                       74.33 |         0.00 |                                                     577066.00 |                                             972171.00 |
| MariaDB-1-1-4-3 |             1.00 |       80.00 |  4096.00 |     4.00 |    3.00 | 120.00 |        87.00 |                          79.75 |                       78.60 |         0.00 |                                                     477518.00 |                                             767402.00 |
| MariaDB-1-1-4-4 |             1.00 |       80.00 |  4096.00 |     4.00 |    4.00 | 120.00 |       104.00 |                          99.69 |                       97.74 |         0.00 |                                                     376222.00 |                                             640196.00 |
| MariaDB-1-2-1-1 |             2.00 |      160.00 |  8192.00 |     1.00 |    1.00 | 120.00 |        16.00 |                         453.26 |                      446.19 |         0.00 |                                                     146710.00 |                                             339082.00 |
| MariaDB-1-2-2-1 |             2.00 |      160.00 |  8192.00 |     2.00 |    1.00 | 120.00 |       126.00 |                         167.36 |                      165.06 |         0.00 |                                                     386348.00 |                                             887074.00 |
| MariaDB-1-2-2-2 |             2.00 |      160.00 |  8192.00 |     2.00 |    2.00 | 120.00 |       125.00 |                         219.01 |                      215.65 |         0.00 |                                                     281451.00 |                                             677863.00 |
| MariaDB-1-2-3-1 |             2.00 |       80.00 |  4096.00 |     3.00 |    1.00 | 120.00 |        52.00 |                         165.51 |                      162.98 |         0.00 |                                                     167209.00 |                                             340298.00 |
| MariaDB-1-2-3-2 |             2.00 |       80.00 |  4096.00 |     3.00 |    2.00 | 120.00 |        56.00 |                         186.93 |                      183.84 |         0.00 |                                                     148148.00 |                                             325543.00 |
| MariaDB-1-2-4-1 |             2.00 |       80.00 |  4096.00 |     4.00 |    1.00 | 120.00 |        63.00 |                          94.56 |                       93.07 |         0.00 |                                                     735346.00 |                                             665147.00 |
| MariaDB-1-2-4-2 |             2.00 |       80.00 |  4096.00 |     4.00 |    2.00 | 120.00 |        57.00 |                          84.19 |                       83.14 |         0.00 |                                                     768878.00 |                                             740456.00 |
| MariaDB-1-2-4-3 |             2.00 |       80.00 |  4096.00 |     4.00 |    3.00 | 120.00 |        54.00 |                          86.40 |                       85.23 |         0.00 |                                                     762651.00 |                                             725338.00 |
| MariaDB-1-2-4-4 |             2.00 |       80.00 |  4096.00 |     4.00 |    4.00 | 120.00 |        61.00 |                         105.37 |                      103.81 |         0.00 |                                                     710149.00 |                                             598917.00 |

#### Per Phase

| DBMS          |   experiment_run |   terminals |   target |   pod_count |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|-----------------:|------------:|---------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 |             1.00 |      160.00 |  8192.00 |        1.00 | 120.00 |        43.00 |                         383.78 |                      377.61 |         0.00 |                                                     101269.00 |                                             294908.00 |
| MariaDB-1-1-2 |             1.00 |      320.00 | 16384.00 |        2.00 | 120.00 |        38.00 |                         403.36 |                      399.06 |         0.00 |                                                    3123314.00 |                                             795572.50 |
| MariaDB-1-1-3 |             1.00 |      160.00 |  8192.00 |        2.00 | 120.00 |         0.00 |                         299.06 |                      295.18 |         0.00 |                                                    2596819.00 |                                             532571.50 |
| MariaDB-1-1-4 |             1.00 |      320.00 | 16384.00 |        4.00 | 120.00 |       401.00 |                         346.68 |                      340.52 |         0.00 |                                                     577066.00 |                                             774693.50 |
| MariaDB-1-2-1 |             2.00 |      160.00 |  8192.00 |        1.00 | 120.00 |        16.00 |                         453.26 |                      446.19 |         0.00 |                                                     146710.00 |                                             339082.00 |
| MariaDB-1-2-2 |             2.00 |      320.00 | 16384.00 |        2.00 | 120.00 |       251.00 |                         386.37 |                      380.71 |         0.00 |                                                     386348.00 |                                             782468.50 |
| MariaDB-1-2-3 |             2.00 |      160.00 |  8192.00 |        2.00 | 120.00 |       108.00 |                         352.44 |                      346.82 |         0.00 |                                                     167209.00 |                                             332920.50 |
| MariaDB-1-2-4 |             2.00 |      320.00 | 16384.00 |        4.00 | 120.00 |       235.00 |                         370.52 |                      365.26 |         0.00 |                                                     768878.00 |                                             682464.50 |

### Monitoring

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       895.81 |     17.49 |           7.14 |                  7.24 |
| MariaDB-1-1-2 |       892.12 |      8.98 |           7.34 |                  7.44 |
| MariaDB-1-1-3 |       826.20 |     10.08 |           7.40 |                  7.50 |
| MariaDB-1-1-4 |      1818.95 |     25.62 |           7.50 |                  7.60 |
| MariaDB-1-2-1 |      5268.63 |     26.71 |           7.49 |                  7.59 |
| MariaDB-1-2-2 |      2695.60 |     35.03 |           7.49 |                  7.59 |
| MariaDB-1-2-3 |      1407.09 |     33.20 |           7.54 |                  7.64 |
| MariaDB-1-2-4 |      1527.22 |     21.28 |           7.65 |                  7.75 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       132.28 |      1.07 |           0.72 |                  0.72 |
| MariaDB-1-1-2 |        87.22 |      3.57 |           0.72 |                  0.72 |
| MariaDB-1-1-3 |        72.10 |      0.91 |           0.70 |                  0.70 |
| MariaDB-1-1-4 |       132.74 |      1.82 |           0.41 |                  0.41 |
| MariaDB-1-2-1 |       148.20 |      1.81 |           0.71 |                  0.71 |
| MariaDB-1-2-2 |       120.82 |      2.71 |           1.06 |                  1.06 |
| MariaDB-1-2-3 |       106.84 |      3.19 |           1.06 |                  1.06 |
| MariaDB-1-2-4 |       123.89 |      2.99 |           1.06 |                  1.06 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
```
















## HammerDB

### PostgreSQL

#### HammerDB Simple

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_testcase_postgresql_1.log
```

yields (after ca. 10 minutes)

test_hammerdb_testcase_postgresql_1.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 774s 
    Code: 1750142683
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.8.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:398454216
    datadisk:3298
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750142683

### Execution
                      experiment_run  vusers  client  pod_count  efficiency    NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1         0.0  8000.0  24608.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1       90.0        1.0   1.0                      640.0

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```


#### HammerDB Monitoring

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_testcase_postgresql_2.log
```

yields (after ca. 15 minutes)

test_hammerdb_testcase_postgresql_2.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 661s 
    Code: 1750143493
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-BHT-8-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394908464
    datadisk:2943
    volume_size:30G
    volume_used:2.9G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750143493

### Execution
                      experiment_run  vusers  client  pod_count  efficiency     NOPM      TPM  duration  errors
PostgreSQL-BHT-8-1-1               1      16       1          1         0.0  11601.0  35640.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1]]

### Loading
                      time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1      105.0        1.0   1.0                 548.571429

### Execution - SUT
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1     24707.9    61.33          4.91                 7.08

### Execution - Benchmarker
                      CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1       31.53     0.09          0.07                 0.07

### Tests
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```

#### HammerDB Complex

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 2 \
  -nlt 8 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_testcase_postgresql_3.log
```

yields (after ca. 60 minutes)

test_hammerdb_testcase_postgresql_3.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 3091s 
    Code: 1750144214
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['PostgreSQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-BHT-8-1-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394907432
    datadisk:3142
    volume_size:30G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394903564
    datadisk:3244
    volume_size:30G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-1-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394903164
    datadisk:3755
    volume_size:30G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-1-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394902924
    datadisk:4198
    volume_size:30G
    volume_used:3.1G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394895944
    datadisk:4605
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:394895792
    datadisk:4680
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-2-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393679948
    datadisk:4780
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214
PostgreSQL-BHT-8-1-2-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393680844
    datadisk:4854
    volume_size:30G
    volume_used:4.5G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750144214

### Execution
                        experiment_run  vusers  client  pod_count  efficiency     NOPM       TPM  duration  errors
PostgreSQL-BHT-8-1-1-1               1      16       1          1         0.0  11155.0  34338.00         2       0
PostgreSQL-BHT-8-1-1-2               1      32       2          2         0.0  10683.5  31413.50         2       0
PostgreSQL-BHT-8-1-1-3               1      16       3          2         0.0   9245.5  29545.50         2       0
PostgreSQL-BHT-8-1-1-4               1      32       4          4         0.0   9827.0  28375.75         2       0
PostgreSQL-BHT-8-1-2-1               2      16       1          1         0.0   8843.0  28338.00         2       0
PostgreSQL-BHT-8-1-2-2               2      32       2          2         0.0   9867.0  29033.50         2       0
PostgreSQL-BHT-8-1-2-3               2      16       3          2         0.0   8184.0  26391.00         2       0
PostgreSQL-BHT-8-1-2-4               2      32       4          4         0.0   9192.0  26915.75         2       0

Warehouses: 16

### Workflow

#### Actual
DBMS PostgreSQL-BHT-8-1 - Pods [[2, 2, 4, 1], [4, 2, 1, 2]]

#### Planned
DBMS PostgreSQL-BHT-8-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                        time_load  terminals  pods  Imported warehouses [1/h]
PostgreSQL-BHT-8-1-1-1      105.0        1.0   1.0                 548.571429
PostgreSQL-BHT-8-1-1-2      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-1-3      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-1-4      105.0        1.0   4.0                 548.571429
PostgreSQL-BHT-8-1-2-1      105.0        1.0   1.0                 548.571429
PostgreSQL-BHT-8-1-2-2      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-2-3      105.0        1.0   2.0                 548.571429
PostgreSQL-BHT-8-1-2-4      105.0        1.0   4.0                 548.571429

### Execution - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1    14210.81    61.39          4.88                 7.15
PostgreSQL-BHT-8-1-1-2    16329.58    62.06          5.66                 8.06
PostgreSQL-BHT-8-1-1-3    14599.86    61.88          5.34                 7.81
PostgreSQL-BHT-8-1-1-4    16248.56    62.80          5.90                 8.42
PostgreSQL-BHT-8-1-2-1    62554.21    61.99          9.53                14.73
PostgreSQL-BHT-8-1-2-2    15525.44    62.00          5.87                 8.62
PostgreSQL-BHT-8-1-2-3    15185.24    61.07          5.77                 8.60
PostgreSQL-BHT-8-1-2-4    15832.79    61.88          6.14                 9.03

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-BHT-8-1-1-1       16.73     0.08          0.07                 0.07
PostgreSQL-BHT-8-1-1-2       14.05     0.09          0.21                 0.22
PostgreSQL-BHT-8-1-1-3       22.81     0.07          0.23                 0.23
PostgreSQL-BHT-8-1-1-4       16.87     0.04          0.26                 0.27
PostgreSQL-BHT-8-1-2-1       14.48     0.06          0.09                 0.09
PostgreSQL-BHT-8-1-2-2       14.92     0.04          0.21                 0.22
PostgreSQL-BHT-8-1-2-3       19.10     0.03          0.23                 0.23
PostgreSQL-BHT-8-1-2-4       11.94     0.05          0.26                 0.27

### Tests
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```





### MySQL

#### HammerDB Simple

```bash
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_testcase_mysql_1.log
```

yields (after ca. 10 minutes)

test_hammerdb_testcase_mysql_1.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 1229s 
    Code: 1750089430
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.8.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-8-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:403932404
    datadisk:10864
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750089430

### Execution
                 experiment_run  vusers  client  pod_count  efficiency    NOPM     TPM  duration  errors
MySQL-BHT-8-1-1               1      16       1          1         0.0  2499.0  5772.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MySQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-8-1 - Pods [[1]]

### Loading
                 time_load  terminals  pods  Imported warehouses [1/h]
MySQL-BHT-8-1-1      375.0        1.0   1.0                      153.6

### Tests
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```


#### HammerDB Monitoring

```bash
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_testcase_mysql_2.log
```

yields (after ca. 15 minutes)

test_hammerdb_testcase_mysql_2.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 8027s 
    Code: 1750090720
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MySQL-BHT-8-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392960236
    datadisk:10860
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750090720

### Execution
                 experiment_run  vusers  client  pod_count  efficiency    NOPM     TPM  duration  errors
MySQL-BHT-8-1-1               1      16       1          1         0.0  1288.0  3024.0         5       0

Warehouses: 16

### Workflow

#### Actual
DBMS MySQL-BHT-8-1 - Pods [[1]]

#### Planned
DBMS MySQL-BHT-8-1 - Pods [[1]]

### Loading
                 time_load  terminals  pods  Imported warehouses [1/h]
MySQL-BHT-8-1-1     6604.0        1.0   1.0                   8.721987

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1      869.56     0.44         37.45                 45.5

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1      361.33      0.2           0.1                  0.1

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1      194.44     1.47         22.97                32.18

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1        8.52     0.06          0.07                 0.07

### Tests
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```

#### HammerDB Complex

```bash
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -xsd 2 \
  -nlt 8 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_testcase_mysql_3.log
```

yields (after ca. 60 minutes)

test_hammerdb_testcase_mysql_3.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
    Type: tpcc
    Duration: 3902s 
    Code: 1750098823
    HammerDB runs the benchmark.
    This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
    TPC-C data is generated and loaded using several threads.
    Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
    Experiment uses bexhoma version 0.8.8.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['MySQL'].
    Import is handled by 1 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 30Gi.
    Loading is tested with [8] threads, split into [1] pods.
    Benchmarking is tested with [16] threads, split into [1, 2] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
MySQL-BHT-8-1-1-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392962848
    datadisk:11037
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750098823
MySQL-BHT-8-1-1-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:392965728
    datadisk:11230
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750098823
MySQL-BHT-8-1-1-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393131856
    datadisk:11531
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750098823
MySQL-BHT-8-1-1-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393133892
    datadisk:11702
    volume_size:30G
    volume_used:11G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750098823
MySQL-BHT-8-1-2-1 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393140456
    datadisk:12083
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750098823
MySQL-BHT-8-1-2-2 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393141932
    datadisk:12259
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750098823
MySQL-BHT-8-1-2-3 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393149976
    datadisk:12569
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750098823
MySQL-BHT-8-1-2-4 uses docker image mysql:8.4.0
    RAM:541008568320
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:393150500
    datadisk:12729
    volume_size:30G
    volume_used:12G
    requests_cpu:4
    requests_memory:16Gi
    eval_parameters
        code:1750098823

### Execution
                   experiment_run  vusers  client  pod_count  efficiency    NOPM       TPM  duration  errors
MySQL-BHT-8-1-1-1               1      16       1          1         0.0  2752.0   6382.00         2       0
MySQL-BHT-8-1-1-2               1      32       2          2         0.0  4722.5  10913.00         2       0
MySQL-BHT-8-1-1-3               1      16       3          2         0.0  1650.0   3857.50         2       0
MySQL-BHT-8-1-1-4               1      32       4          4         0.0  7990.5  18509.75         2       0
MySQL-BHT-8-1-2-1               2      16       1          1         0.0  2395.0   5645.00         2       0
MySQL-BHT-8-1-2-2               2      32       2          2         0.0  3964.0   9193.00         2       0
MySQL-BHT-8-1-2-3               2      16       3          2         0.0  2639.5   6071.50         2       0
MySQL-BHT-8-1-2-4               2      32       4          4         0.0  4926.0  11356.25         2       0

Warehouses: 16

### Workflow

#### Actual
DBMS MySQL-BHT-8-1 - Pods [[4, 2, 1, 2], [2, 4, 1, 2]]

#### Planned
DBMS MySQL-BHT-8-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading
                   time_load  terminals  pods  Imported warehouses [1/h]
MySQL-BHT-8-1-1-1     6604.0        1.0   1.0                   8.721987
MySQL-BHT-8-1-1-2     6604.0        1.0   2.0                   8.721987
MySQL-BHT-8-1-1-3     6604.0        1.0   2.0                   8.721987
MySQL-BHT-8-1-1-4     6604.0        1.0   4.0                   8.721987
MySQL-BHT-8-1-2-1     6604.0        1.0   1.0                   8.721987
MySQL-BHT-8-1-2-2     6604.0        1.0   2.0                   8.721987
MySQL-BHT-8-1-2-3     6604.0        1.0   2.0                   8.721987
MySQL-BHT-8-1-2-4     6604.0        1.0   4.0                   8.721987

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1-1      482.55     1.39         38.37                46.48
MySQL-BHT-8-1-1-2      490.84     2.18         38.66                47.15
MySQL-BHT-8-1-1-3      308.68     1.21         38.73                47.36
MySQL-BHT-8-1-1-4      499.53     1.67         38.95                47.92
MySQL-BHT-8-1-2-1     2618.47     1.74         77.01                94.82
MySQL-BHT-8-1-2-2      477.33     1.67         38.66                47.99
MySQL-BHT-8-1-2-3      347.58     1.74         38.81                48.26
MySQL-BHT-8-1-2-4      443.20     1.76         38.92                48.66

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MySQL-BHT-8-1-1-1       12.44     0.03          0.07                 0.07
MySQL-BHT-8-1-1-2       12.86     0.05          0.21                 0.22
MySQL-BHT-8-1-1-3       19.67     0.02          0.23                 0.23
MySQL-BHT-8-1-1-4       19.70     0.09          0.26                 0.27
MySQL-BHT-8-1-2-1       11.75     0.04          0.07                 0.07
MySQL-BHT-8-1-2-2       16.38     0.06          0.21                 0.22
MySQL-BHT-8-1-2-3       22.10     0.05          0.23                 0.23
MySQL-BHT-8-1-2-4       11.96     0.04          0.26                 0.27

### Tests
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: NOPM contains no 0 or NaN
TEST passed: Workflow as planned
```




### MariaDB

#### HammerDB Simple

```bash
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_testcase_mariadb_1.log
```

yields (after ca. 10 minutes)

test_hammerdb_testcase_mariadb_1.log
```markdown
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
```


#### HammerDB Monitoring

```bash
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_testcase_mariadb_2.log
```

yields (after ca. 15 minutes)

test_hammerdb_testcase_mariadb_2.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1155s 
* Code: 1780053795
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
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
  * disk:58089
  * volume_size:30G
  * volume_used:1.7G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780053795

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1]]

#### Planned

* DBMS MariaDB-1 - Pods [[1]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      700.00 |           1.00 |            0.00 |        335.00 |          364.00 |              1 |           8 |          | None           |             0 | False         |               82.29 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   vusers |   client |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:----------------|-----------------:|---------:|---------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| MariaDB-1-1-1-1 |                1 |       16 |        1 |       1 |   9805 | 22794 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS          |   experiment_run |   vusers |   client |   pod_count |   efficiency |    NOPM |      TPM |   duration |   errors |
|:--------------|-----------------:|---------:|---------:|------------:|-------------:|--------:|---------:|-----------:|---------:|
| MariaDB-1-1-1 |             1.00 |    16.00 |     1.00 |        1.00 |         0.00 | 9805.00 | 22794.00 |       5.00 |     0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       845.08 |      3.35 |           7.06 |                  7.16 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       271.99 |      1.16 |           0.10 |                  0.10 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       947.62 |      3.68 |           7.16 |                  7.26 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |        40.35 |      0.15 |           0.07 |                  0.07 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```

#### HammerDB Complex

```bash
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -xsd 2 \
  -nlt 8 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_testcase_mariadb_3.log
```

yields (after ca. 60 minutes)

test_hammerdb_testcase_mariadb_3.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 3224s 
* Code: 1780054976
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-1-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-1-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-1-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976
* MariaDB-1-2-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58089
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780054976

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

#### Planned

* DBMS MariaDB-1 - Pods [[1, 2, 2, 4], [1, 2, 2, 4]]

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:---------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      700.00 |           1.00 |            0.00 |        335.00 |          364.00 |              0 |           8 |          | None           |             0 | False         |               82.29 |
| MariaDB-1-2 |                2 |   16 |      700.00 |           1.00 |            0.00 |        335.00 |          364.00 |              0 |           8 |          | None           |             0 | False         |               82.29 |

### Execution

#### Per Connection

| DBMS            |   experiment_run |   vusers |   client |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:----------------|-----------------:|---------:|---------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| MariaDB-1-1-1-1 |                1 |       16 |        1 |       1 |  12123 | 28299 |         0.00 |          2 |        0 |
| MariaDB-1-1-2-1 |                1 |       16 |        2 |       1 |   9914 | 22893 |         0.00 |          2 |        0 |
| MariaDB-1-1-2-1 |                1 |       16 |        2 |       1 |  10146 | 23427 |         0.00 |          2 |        0 |
| MariaDB-1-1-3-1 |                1 |        8 |        3 |       1 |   7436 | 17246 |         0.00 |          2 |        0 |
| MariaDB-1-1-3-1 |                1 |        8 |        3 |       1 |   7440 | 17252 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6528 | 15148 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6591 | 15283 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6535 | 15169 |         0.00 |          2 |        0 |
| MariaDB-1-1-4-1 |                1 |        8 |        4 |       1 |   6560 | 15217 |         0.00 |          2 |        0 |
| MariaDB-1-2-1-1 |                2 |       16 |        1 |       1 |   9101 | 21227 |         0.00 |          2 |        0 |
| MariaDB-1-2-2-1 |                2 |       16 |        2 |       1 |   9011 | 20796 |         0.00 |          2 |        0 |
| MariaDB-1-2-2-1 |                2 |       16 |        2 |       1 |   9077 | 20938 |         0.00 |          2 |        0 |
| MariaDB-1-2-3-1 |                2 |        8 |        3 |       1 |   8350 | 19461 |         0.00 |          2 |        0 |
| MariaDB-1-2-3-1 |                2 |        8 |        3 |       1 |   8295 | 19358 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8527 | 19937 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8431 | 19717 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8498 | 19865 |         0.00 |          2 |        0 |
| MariaDB-1-2-4-1 |                2 |        8 |        4 |       1 |   8431 | 19717 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS          |   experiment_run |   vusers |   client |   pod_count |   efficiency |     NOPM |      TPM |   duration |   errors |
|:--------------|-----------------:|---------:|---------:|------------:|-------------:|---------:|---------:|-----------:|---------:|
| MariaDB-1-1-1 |             1.00 |    16.00 |     1.00 |        1.00 |         0.00 | 12123.00 | 28299.00 |       2.00 |     0.00 |
| MariaDB-1-1-2 |             1.00 |    32.00 |     2.00 |        2.00 |         0.00 | 10030.00 | 23160.00 |       2.00 |     0.00 |
| MariaDB-1-1-3 |             1.00 |    16.00 |     3.00 |        2.00 |         0.00 |  7438.00 | 17249.00 |       2.00 |     0.00 |
| MariaDB-1-1-4 |             1.00 |    32.00 |     4.00 |        4.00 |         0.00 |  6553.50 | 15204.25 |       2.00 |     0.00 |
| MariaDB-1-2-1 |             2.00 |    16.00 |     1.00 |        1.00 |         0.00 |  9101.00 | 21227.00 |       2.00 |     0.00 |
| MariaDB-1-2-2 |             2.00 |    32.00 |     2.00 |        2.00 |         0.00 |  9044.00 | 20867.00 |       2.00 |     0.00 |
| MariaDB-1-2-3 |             2.00 |    16.00 |     3.00 |        2.00 |         0.00 |  8322.50 | 19409.50 |       2.00 |     0.00 |
| MariaDB-1-2-4 |             2.00 |    32.00 |     4.00 |        4.00 |         0.00 |  8471.75 | 19809.00 |       2.00 |     0.00 |

### Monitoring

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       585.20 |      2.97 |           6.84 |                  6.94 |
| MariaDB-1-1-2 |       871.45 |      6.59 |           6.95 |                  7.05 |
| MariaDB-1-1-3 |       506.27 |      4.93 |           6.98 |                  7.08 |
| MariaDB-1-1-4 |       940.30 |      5.49 |           7.06 |                  7.16 |
| MariaDB-1-2-1 |      3027.35 |      2.36 |           7.06 |                  7.16 |
| MariaDB-1-2-2 |       863.04 |      4.29 |           7.06 |                  7.16 |
| MariaDB-1-2-3 |       418.66 |      2.17 |           7.09 |                  7.19 |
| MariaDB-1-2-4 |       798.13 |      3.86 |           7.18 |                  7.28 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |        24.52 |      0.13 |           0.07 |                  0.07 |
| MariaDB-1-1-2 |        24.52 |      0.34 |           0.07 |                  0.07 |
| MariaDB-1-1-3 |        21.49 |      0.28 |           0.07 |                  0.07 |
| MariaDB-1-1-4 |        16.11 |      0.25 |           0.04 |                  0.05 |
| MariaDB-1-2-1 |        22.71 |      0.13 |           0.07 |                  0.07 |
| MariaDB-1-2-2 |        22.71 |      0.27 |           0.07 |                  0.07 |
| MariaDB-1-2-3 |        22.87 |      0.21 |           0.07 |                  0.07 |
| MariaDB-1-2-4 |        18.35 |      0.26 |           0.04 |                  0.05 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
```
















## YCSB


### YCSB Loader Test for Scaling the Driver

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 4,8 \
  -nlt 32,64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_ycsb_testcase_postgresql_1.log
```

yields (after ca. 15 minutes) something like

test_ycsb_testcase_postgresql_1.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 2293s 
    Code: 1749133596
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '1024'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 4 and 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [32, 64] threads, split into [4, 8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-32-4-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:360804960
    datadisk:2393
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749133596

### Loading
                      experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-32-4-1024               1       32    1024          4           0                    1023.706483               976849.0             1000000                               744.5

### Execution
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-32-4-1024-1               1       64    1024          1           0                        1023.48               977063.0            500067                             676.0              499933                               825.0

### Workflow

#### Actual
DBMS PostgreSQL-32-4-1024 - Pods [[1]]

#### Planned
DBMS PostgreSQL-32-4-1024 - Pods [[1]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```

### YCSB Loader Test for Persistency

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_ycsb_testcase_postgresql_2.log
```

yields (after ca. 10 minutes) something like

test_ycsb_testcase_postgresql_2.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 3600s 
    Code: 1749135967
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '1024'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-64-8-1024-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358550148
    datadisk:2393
    volume_size:50G
    volume_used:2.4G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749135967
PostgreSQL-64-8-1024-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:358855468
    datadisk:2822
    volume_size:50G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1749135967

### Loading
                      experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
PostgreSQL-64-8-1024               1       64    1024          8           0                     1023.69024               976892.0             1000000                             792.875

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-1024-1-1               1       64    1024          1           0                        1023.44               977095.0            500089                             658.0              499911                               802.0
PostgreSQL-64-8-1024-2-1               2       64    1024          1           0                        1023.51               977026.0            500749                             710.0              499251                               837.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-1024 - Pods [[1], [1]]

#### Planned
DBMS PostgreSQL-64-8-1024 - Pods [[1], [1]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```


### YCSB Execution for Scaling and Repetition

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_ycsb_testcase_postgresql_3.log
```

yields (after ca. 15 minutes) something like

test_ycsb_testcase_postgresql_3.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 6873s 
    Code: 1749139628
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '1024'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1, 2] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
PostgreSQL-64-8-1024-1-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359045052
    datadisk:2846
    volume_size:50G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-1-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359049596
    datadisk:2853
    volume_size:50G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-1-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359050772
    datadisk:2856
    volume_size:50G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:1
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-1-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359225168
    datadisk:2923
    volume_size:50G
    volume_used:2.8G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:1
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-2-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359238984
    datadisk:3046
    volume_size:50G
    volume_used:3.0G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:2
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-2-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359247344
    datadisk:3048
    volume_size:50G
    volume_used:3.0G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:2
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-2-3 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359247068
    datadisk:3050
    volume_size:50G
    volume_used:3.0G
    requests_cpu:4
    requests_memory:16Gi
    client:3
    numExperiment:2
    eval_parameters
        code:1749139628
PostgreSQL-64-8-1024-2-4 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359247796
    datadisk:3052
    volume_size:50G
    volume_used:3.0G
    requests_cpu:4
    requests_memory:16Gi
    client:4
    numExperiment:2
    eval_parameters
        code:1749139628

### Execution
                          experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-1024-1-1               1       64    1024          1           0                        1023.49               977047.0            500515                             703.0              499485                               822.0
PostgreSQL-64-8-1024-1-3               1       64    1024          8           0                        1023.68               976894.0            499822                             736.0              500178                               847.0
PostgreSQL-64-8-1024-1-2               1      128    2048          2           0                        2046.08               488745.0            500438                             675.0              499562                               778.0
PostgreSQL-64-8-1024-1-4               1      128    2048         16           0                        2046.67               488620.0            500818                             707.0              499182                               883.0
PostgreSQL-64-8-1024-2-1               2       64    1024          1           0                        1023.51               977030.0            500306                             681.0              499694                               780.0
PostgreSQL-64-8-1024-2-3               2       64    1024          8           0                        1023.68               976913.0            499483                             742.0              500517                               861.0
PostgreSQL-64-8-1024-2-2               2      128    2048          2           0                        2046.10               488748.0            500244                             698.0              499756                               799.0
PostgreSQL-64-8-1024-2-4               2      128    2048         16           0                        2046.71               488605.0            500349                             770.0              499651                               908.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-1024 - Pods [[16, 8, 2, 1], [8, 16, 2, 1]]

#### Planned
DBMS PostgreSQL-64-8-1024 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```


### YCSB Execution Different Workload

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl e \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_ycsb_testcase_postgresql_4.log
```

yields (after ca. 5 minutes) something like

test_ycsb_testcase_postgresql_4.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 1302s 
    Code: 1749146590
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'E'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '1024'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.8.7.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359248556
    datadisk:3047
    volume_size:50G
    volume_used:3.0G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749146590

### Execution
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)  [SCAN].Return=OK  [SCAN].99thPercentileLatency(us)  [INSERT-FAILED].Operations  [INSERT-FAILED].99thPercentileLatency(us)
PostgreSQL-64-8-1024-1               1       64    1024          8           0                        1023.69               976884.0               49901                              1124.0            949867                            2323.0                         232                                    15863.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-1024 - Pods [[8]]

#### Planned
DBMS PostgreSQL-64-8-1024 - Pods [[8]]

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
TEST failed: Result contains FAILED column
```

### YCSB Execution Monitoring

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_ycsb_testcase_postgresql_5.log
```

yields (after ca. 10 minutes) something like

test_ycsb_testcase_postgresql_5.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 2342s 
    Code: 1749147910
    YCSB tool runs the benchmark.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '1024'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.8.7.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['PostgreSQL'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [64] threads, split into [8] pods.
    Benchmarking is tested with [64] threads, split into [1, 8] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
PostgreSQL-64-8-1024-1 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359249228
    datadisk:2752
    volume_size:50G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1749147910
PostgreSQL-64-8-1024-2 uses docker image postgres:16.1
    RAM:541008568320
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-140-generic
    node:cl-worker11
    disk:359249624
    datadisk:2754
    volume_size:50G
    volume_used:2.7G
    requests_cpu:4
    requests_memory:16Gi
    client:2
    numExperiment:1
    eval_parameters
        code:1749147910

### Execution
                        experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
PostgreSQL-64-8-1024-1               1       64    1024          1           0                        1023.48               977059.0            499742                             690.0              500258                               814.0
PostgreSQL-64-8-1024-2               1       64    1024          8           0                        1023.69               976880.0            500373                             722.0              499627                               852.0

### Workflow

#### Actual
DBMS PostgreSQL-64-8-1024 - Pods [[8, 1]]

#### Planned
DBMS PostgreSQL-64-8-1024 - Pods [[1, 8]]

### Execution - SUT
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-1024-1      233.34     0.26          4.05                 5.60
PostgreSQL-64-8-1024-2      220.71     0.24          4.01                 5.58

### Execution - Benchmarker
                        CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
PostgreSQL-64-8-1024-1      229.65     0.35          0.57                 0.57
PostgreSQL-64-8-1024-2      227.59     0.25          2.48                 2.50

### Tests
TEST passed: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
TEST passed: Result contains no FAILED column
```




