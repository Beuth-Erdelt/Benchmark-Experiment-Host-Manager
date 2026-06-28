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
  -lr 128Gi \
  -rr 128Gi \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_compare.log
```

yields (after ca. 120 minutes) something like

testcase_tpch_compare.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_postgresql_1.log
```

yields (after ca. 10 minutes) something like

testcase_tpch_postgresql_1.log
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
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_postgresql_2.log
```

yields (after ca. 15 minutes) something like

testcase_tpch_postgresql_2.log
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
  -rss 150Gi \
  -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_postgresql_3.log
```

yields (after ca. 15 minutes) something like

testcase_tpch_postgresql_3.log
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
  -rr 64Gi \
  -rst ramdisk \
  -rss 45Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_postgresql_ramdisk.log
```

yields (after ca. 15 minutes) something like

testcase_tpch_postgresql_ramdisk.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mysql_1.log
```

yields (after ca. 10 minutes) something like

testcase_tpch_mysql_1.log
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
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mysql_2.log
```

yields (after ca. 15 minutes) something like

testcase_tpch_mysql_2.log
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
  -rss 150Gi \
  -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mysql_3.log
```

yields (after ca. 15 minutes) something like

testcase_tpch_mysql_3.log
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
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mysql_ramdisk.log
```

yields (after ca. 15 minutes) something like

testcase_tpch_mysql_ramdisk.log
```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
* Type: tpch
* Duration: 1863s 
* Code: 1782406715
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
  * Experiment is limited to DBMS ['MySQL'].
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
* MySQL-1-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220477
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * eval_parameters
    * code:1782406715

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   10 |      968.00 |           2.00 |           16.00 |        143.00 |          803.00 |              8 |           0 |             | None           |             0 | False         |               37.19 |

### Execution

#### Per Connection

|                 | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| MySQL-1-1-1-1-1 | MySQL-1         | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        586 |           11.21 |             3262.50 |           1351.54 |          -1 | MySQL-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |    SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |        1 |               1 |           1 | 10.00 |               22 |        586 |           11.21 |             3262.50 |           1351.54 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MySQL-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |          77080.85 |
| Minimum Cost Supplier Query (TPC-H Q2)              |           1046.80 |
| Shipping Priority (TPC-H Q3)                        |          15651.20 |
| Order Priority Checking Query (TPC-H Q4)            |           4487.97 |
| Local Supplier Volume (TPC-H Q5)                    |          12609.95 |
| Forecasting Revenue Change (TPC-H Q6)               |          12032.87 |
| Volume Shipping Query (TPC-H Q7)                    |           8701.39 |
| National Market Share (TPC-H Q8)                    |          34697.33 |
| Product Type Profit Measure (TPC-H Q9)              |          24026.03 |
| Returned Item Reporting Query (TPC-H Q10)           |          16264.46 |
| Important Stock Identification (TPC-H Q11)          |           2368.88 |
| Shipping Modes and Order Priority (TPC-H Q12)       |          19935.53 |
| Customer Distribution (TPC-H Q13)                   |          78864.00 |
| Promotion Effect Query (TPC-H Q14)                  |          14272.63 |
| Top Supplier Query (TPC-H Q15)                      |         165623.67 |
| Parts/Supplier Relationship (TPC-H Q16)             |           3191.36 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |           3602.01 |
| Large Volume Customer (TPC-H Q18)                   |          19186.95 |
| Discounted Revenue (TPC-H Q19)                      |           1519.51 |
| Potential Part Promotion (TPC-H Q20)                |           3022.54 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |          58908.85 |
| Global Sales Opportunity Query (TPC-H Q22)          |           1635.99 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      3966.62 |      9.51 |          75.54 |                 75.54 |

### Loading phase: component data generator

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        25.07 |      0.30 |           0.03 |                  1.14 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       575.47 |      1.02 |          76.32 |                 76.32 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |        22.67 |      0.48 |           0.42 |                  0.42 |

### Application Metrics

#### Loading phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       1.33 |                     0.01 |                0.09 |                    0.00 |

#### Execution phase: SUT deployment

| DBMS          |   InnoDB Buffer Pool Hit Ratio |   Queries Per Second (QPS) |   Connection Usage Ratio |   Slow Queries Rate |   InnoDB Log Waits Rate |
|:--------------|-------------------------------:|---------------------------:|-------------------------:|--------------------:|------------------------:|
| MySQL-1-1-1-1 |                           1.00 |                       0.84 |                     0.00 |                0.03 |                    0.00 |

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
  -lr 128Gi \
  -rr 128Gi \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mariadb_1.log
```

yields (after ca. 10 minutes) something like

testcase_tpch_mariadb_1.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mariadb_2.log
```

yields (after ca. 15 minutes) something like

testcase_tpch_mariadb_2.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mariadb_3.log
```

yields (after ca. 15 minutes) something like

testcase_tpch_mariadb_3.log
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
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mariadb_ramdisk.log

```

yields (after ca. 15 minutes) something like

testcase_tpch_mariadb_ramdisk.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_compare.log
```

yields (after ca. 520 minutes) something like

testcase_tpcds_compare.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_postgresql_1.log
```

yields (after ca. 10 minutes) something like

testcase_tpcds_postgresql_1.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_postgresql_2.log
```

yields (after ca. 15 minutes) something like

testcase_tpcds_postgresql_2.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_postgresql_3.log
```

yields (after ca. 15 minutes) something like

testcase_tpcds_postgresql_3.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mysql_1.log
```

yields (after ca. 10 minutes) something like

testcase_tpcds_mysql_1.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mysql_2.log
```

yields (after ca. 15 minutes) something like

testcase_tpcds_mysql_2.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mysql_3.log
```

yields (after ca. 15 minutes) something like

testcase_tpcds_mysql_3.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mariadb_1.log
```

yields (after ca. 10 minutes) something like

testcase_tpcds_mariadb_1.log
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
  -lr 128Gi \
  -rr 128Gi \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mariadb_2.log
```

yields (after ca. 15 minutes) something like

testcase_tpcds_mariadb_2.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 4175s 
* Code: 1782408033
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
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
  * disk:225003
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408033

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |      659.00 |           2.00 |            1.00 |         63.00 |          586.00 |              8 |           0 |             | None           |             0 | False         |                5.46 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3222 |            1.00 |             3615.10 |            108.38 |          -1 | MariaDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3222 |            1.00 |             3615.10 |            108.38 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MariaDB-1-1-1-1-1 |
|:--------------|--------------------:|
| TPC-DS Q1     |               20.58 |
| TPC-DS Q2     |             5155.74 |
| TPC-DS Q3     |               17.24 |
| TPC-DS Q4     |            12760.85 |
| TPC-DS Q5     |             8530.52 |
| TPC-DS Q6     |              788.63 |
| TPC-DS Q7     |             3533.69 |
| TPC-DS Q8     |              364.70 |
| TPC-DS Q9     |             3826.11 |
| TPC-DS Q10    |               47.09 |
| TPC-DS Q11    |             8029.01 |
| TPC-DS Q12    |              249.82 |
| TPC-DS Q13    |             1138.95 |
| TPC-DS Q14a+b |            49164.50 |
| TPC-DS Q15    |              173.35 |
| TPC-DS Q16    |            11244.66 |
| TPC-DS Q17    |              803.62 |
| TPC-DS Q18    |             1934.76 |
| TPC-DS Q19    |              255.67 |
| TPC-DS Q20    |              437.01 |
| TPC-DS Q21    |            21254.04 |
| TPC-DS Q22    |            19635.03 |
| TPC-DS Q23a+b |            58108.26 |
| TPC-DS Q24a+b |             2072.30 |
| TPC-DS Q25    |              158.64 |
| TPC-DS Q26    |              898.32 |
| TPC-DS Q27    |             1680.10 |
| TPC-DS Q28    |             2833.70 |
| TPC-DS Q29    |               97.75 |
| TPC-DS Q30    |              103.69 |
| TPC-DS Q31    |             1445.23 |
| TPC-DS Q32    |               10.71 |
| TPC-DS Q33    |              204.18 |
| TPC-DS Q34    |             3192.23 |
| TPC-DS Q35    |             1189.62 |
| TPC-DS Q36    |             1688.02 |
| TPC-DS Q37    |             3737.26 |
| TPC-DS Q38    |             7163.57 |
| TPC-DS Q39a+b |             1324.60 |
| TPC-DS Q40    |              186.38 |
| TPC-DS Q41    |              413.10 |
| TPC-DS Q42    |              239.73 |
| TPC-DS Q43    |             1148.65 |
| TPC-DS Q44    |                2.52 |
| TPC-DS Q45    |              128.51 |
| TPC-DS Q46    |             3546.82 |
| TPC-DS Q47    |            13981.45 |
| TPC-DS Q48    |             1259.37 |
| TPC-DS Q49    |              114.33 |
| TPC-DS Q50    |               30.74 |
| TPC-DS Q51    |             7630.46 |
| TPC-DS Q52    |              224.42 |
| TPC-DS Q53    |              161.65 |
| TPC-DS Q54    |             1039.59 |
| TPC-DS Q55    |              218.12 |
| TPC-DS Q56    |              133.75 |
| TPC-DS Q57    |             6727.82 |
| TPC-DS Q58    |             5732.05 |
| TPC-DS Q59    |             9403.49 |
| TPC-DS Q60    |              663.03 |
| TPC-DS Q61    |              370.34 |
| TPC-DS Q62    |             1684.59 |
| TPC-DS Q63    |              152.48 |
| TPC-DS Q64    |              566.63 |
| TPC-DS Q65    |             5794.88 |
| TPC-DS Q66    |             1281.28 |
| TPC-DS Q67    |             7257.30 |
| TPC-DS Q68    |             3197.45 |
| TPC-DS Q69    |                3.45 |
| TPC-DS Q70    |             8595.11 |
| TPC-DS Q71    |              522.66 |
| TPC-DS Q72    |           406943.14 |
| TPC-DS Q73    |             2959.08 |
| TPC-DS Q74    |             6295.58 |
| TPC-DS Q75    |             5770.01 |
| TPC-DS Q76    |              845.91 |
| TPC-DS Q77    |             6337.57 |
| TPC-DS Q78    |             5962.35 |
| TPC-DS Q79    |             3277.33 |
| TPC-DS Q80    |              842.18 |
| TPC-DS Q81    |              316.31 |
| TPC-DS Q82    |             4404.48 |
| TPC-DS Q83    |              948.80 |
| TPC-DS Q84    |               59.16 |
| TPC-DS Q85    |              148.73 |
| TPC-DS Q86    |              980.04 |
| TPC-DS Q87    |             7542.86 |
| TPC-DS Q88    |            25828.87 |
| TPC-DS Q89    |             1677.75 |
| TPC-DS Q90    |              395.91 |
| TPC-DS Q91    |               28.21 |
| TPC-DS Q92    |               10.74 |
| TPC-DS Q93    |               44.28 |
| TPC-DS Q96    |             2678.46 |
| TPC-DS Q97    |             5174.98 |
| TPC-DS Q98    |              857.55 |
| TPC-DS Q99    |             4862.09 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
* TPC-DS Q94
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=61) Query execution was interrupted (max_statement_time exceeded)
* TPC-DS Q95
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=61) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |       752.71 |      4.40 |           8.68 |                  8.79 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         2.14 |      0.04 |           0.01 |                  0.76 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      3193.56 |      1.00 |           8.93 |                  9.04 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        20.80 |      0.02 |           0.30 |                  0.31 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
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
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 15Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mariadb_3.log
```

yields (after ca. 15 minutes) something like

testcase_tpcds_mariadb_3.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=1
* Type: tpcds
* Duration: 16025s 
* Code: 1782408084
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
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
  * Database is persisted to disk of type shared and size 10Gi.
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
  * disk:225003
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084
* MariaDB-1-1-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220477
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084
* MariaDB-1-1-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220477
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084
* MariaDB-1-2-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220478
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084
* MariaDB-1-2-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220478
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084
* MariaDB-1-2-2-1-2 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220478
  * volume_size:10G
  * volume_used:4.5G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782408084

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpcds (2 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: tpcds (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: tpcds (2 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |    1 |     2391.00 |           5.00 |            1.00 |        464.00 |         1913.00 |              8 |           0 |             | None           |             0 | False         |                1.51 |
| MariaDB-1-2 |                2 |    1 |     2391.00 |           5.00 |            1.00 |        464.00 |         1913.00 |              8 |           0 |             | None           |             0 | False         |                1.51 |

### Execution

#### Per Connection

|                   | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MariaDB-1-1-1-1-1 | MariaDB-1       | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3190 |            1.03 |             3534.75 |            109.47 |          -1 | MariaDB-1-1-1-1-1 |
| MariaDB-1-1-2-1-1 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               97 |       3269 |            1.10 |             3286.12 |            106.82 |          -1 | MariaDB-1-1-2-1-1 |
| MariaDB-1-1-2-1-2 | MariaDB-1       | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |        2 |               1 |           1 | 1.00 |               97 |       3265 |            1.09 |             3332.89 |            106.95 |          -1 | MariaDB-1-1-2-1-2 |
| MariaDB-1-2-1-1-1 | MariaDB-1       | MariaDB-1-2-1 | MariaDB-1-2-1-1 |                2 |        1 |               1 |           1 | 1.00 |               97 |       3176 |            1.03 |             3536.56 |            109.95 |          -1 | MariaDB-1-2-1-1-1 |
| MariaDB-1-2-2-1-1 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               97 |       3309 |            1.16 |             3112.08 |            105.53 |          -1 | MariaDB-1-2-2-1-1 |
| MariaDB-1-2-2-1-2 | MariaDB-1       | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |        2 |               1 |           1 | 1.00 |               97 |       3310 |            1.13 |             3204.20 |            105.50 |          -1 | MariaDB-1-2-2-1-2 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               97 |       3190 |            1.03 |             3534.75 |            109.47 |          -1 |
| MariaDB-1-1-2 | MariaDB-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |              194 |       3269 |            1.10 |             3309.42 |            213.64 |          -1 |
| MariaDB-1-2-1 | MariaDB-1-2-1 |                2 |        1 |               1 |           1 | 1.00 |               97 |       3176 |            1.03 |             3536.56 |            109.95 |          -1 |
| MariaDB-1-2-2 | MariaDB-1-2-2 |                2 |        2 |               1 |           2 | 1.00 |              194 |       3310 |            1.15 |             3157.80 |            211.00 |          -1 |

### Latency of Timer Execution [ms]
| Queries       |   MariaDB-1-1-1-1-1 |   MariaDB-1-1-2-1-1 |   MariaDB-1-1-2-1-2 |   MariaDB-1-2-1-1-1 |   MariaDB-1-2-2-1-1 |   MariaDB-1-2-2-1-2 |
|:--------------|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|--------------------:|
| TPC-DS Q1     |               21.25 |               21.99 |               20.65 |              156.55 |               19.74 |               19.42 |
| TPC-DS Q2     |             4572.82 |             4580.97 |             4652.58 |             4663.55 |             4672.21 |             4425.77 |
| TPC-DS Q3     |               12.23 |               10.62 |               10.31 |               29.80 |                9.75 |               10.38 |
| TPC-DS Q4     |            11814.81 |            12501.07 |            12437.42 |            12102.38 |            12928.04 |            12800.08 |
| TPC-DS Q5     |             8366.21 |             9842.79 |             9910.66 |             9389.33 |            10867.63 |            10874.60 |
| TPC-DS Q6     |              739.85 |             1265.71 |              849.79 |              748.56 |             1320.35 |             1188.27 |
| TPC-DS Q7     |             3376.76 |             4458.41 |             4393.45 |             3429.95 |             5104.82 |             5209.71 |
| TPC-DS Q8     |              343.92 |              367.82 |              338.62 |              363.22 |              492.11 |              486.03 |
| TPC-DS Q9     |             3799.43 |             3882.50 |             3799.12 |             3794.98 |             3878.79 |             3896.92 |
| TPC-DS Q10    |               35.46 |               54.46 |               29.46 |               37.15 |               57.30 |               30.34 |
| TPC-DS Q11    |             8050.92 |             9397.69 |             9382.76 |             8350.30 |             9387.13 |             9359.84 |
| TPC-DS Q12    |              248.72 |              362.98 |              362.63 |              249.00 |              348.20 |              349.12 |
| TPC-DS Q13    |             1054.74 |             1461.56 |             1461.12 |             1191.68 |             1474.66 |             1474.37 |
| TPC-DS Q14a+b |            48552.25 |            62756.87 |            62759.34 |            48582.69 |            63169.03 |            62933.92 |
| TPC-DS Q15    |              163.26 |              196.61 |              181.96 |              177.04 |              166.73 |              180.11 |
| TPC-DS Q16    |            10847.69 |            14153.72 |            14151.81 |            10820.47 |            12814.62 |            13007.66 |
| TPC-DS Q17    |              728.31 |             1050.29 |             1050.16 |              767.33 |             1008.07 |              940.85 |
| TPC-DS Q18    |             1844.73 |             2495.47 |             2494.17 |             1850.02 |             2570.09 |             2592.19 |
| TPC-DS Q19    |              238.02 |              255.75 |              275.81 |              231.32 |              244.95 |              263.61 |
| TPC-DS Q20    |              458.56 |              591.78 |              601.10 |              442.84 |              568.52 |              571.26 |
| TPC-DS Q21    |            21074.79 |            33681.57 |            32755.89 |            21235.75 |            34368.12 |            34372.27 |
| TPC-DS Q22    |            19298.32 |            23518.30 |            22760.57 |            19338.94 |            24807.46 |            25263.17 |
| TPC-DS Q23a+b |            48300.77 |            60779.03 |            58433.79 |            47628.03 |            60414.22 |            60098.87 |
| TPC-DS Q24a+b |             2055.66 |             2286.62 |             2203.90 |             2019.86 |             2589.10 |             2494.32 |
| TPC-DS Q25    |              141.25 |              148.99 |              158.71 |              149.85 |              174.74 |              151.71 |
| TPC-DS Q26    |              831.80 |              833.36 |              875.27 |              873.59 |             1117.71 |             1120.46 |
| TPC-DS Q27    |             1652.02 |             1693.30 |             2310.39 |             1698.96 |             2212.60 |             2216.17 |
| TPC-DS Q28    |             2802.26 |             2788.12 |             2818.67 |             2791.98 |             2903.12 |             2926.11 |
| TPC-DS Q29    |               88.25 |               93.80 |               96.65 |               88.78 |              126.71 |              127.19 |
| TPC-DS Q30    |              102.43 |              139.73 |              108.13 |              105.74 |              127.20 |              129.53 |
| TPC-DS Q31    |             1396.46 |             1451.24 |             1466.10 |             1386.77 |             1709.62 |             1711.92 |
| TPC-DS Q32    |               10.50 |               10.73 |                9.95 |                9.58 |               10.85 |               10.44 |
| TPC-DS Q33    |              164.08 |              183.65 |              178.22 |              170.11 |              229.13 |              219.65 |
| TPC-DS Q34    |             2912.74 |             3104.45 |             2968.59 |             2874.04 |             3912.62 |             3927.87 |
| TPC-DS Q35    |             1133.96 |             1218.13 |             1243.14 |             1140.08 |             1648.53 |             1643.21 |
| TPC-DS Q36    |             1620.78 |             1799.61 |             1786.51 |             1645.18 |             2414.60 |             3016.97 |
| TPC-DS Q37    |             3538.03 |             3763.53 |             3979.29 |             3637.88 |             4191.12 |             5101.84 |
| TPC-DS Q38    |             7006.01 |             8248.53 |             8141.00 |             7148.33 |             8886.38 |             8664.93 |
| TPC-DS Q39a+b |             1168.31 |             1189.52 |             1202.60 |             1223.29 |             1203.41 |             1191.13 |
| TPC-DS Q40    |              175.99 |              180.18 |              237.27 |              180.80 |              183.92 |              203.87 |
| TPC-DS Q41    |              397.18 |              400.24 |              402.33 |              391.30 |              390.42 |              394.80 |
| TPC-DS Q42    |              223.24 |              233.10 |              246.26 |              216.27 |              232.34 |              263.56 |
| TPC-DS Q43    |             1152.75 |             1409.22 |             1312.66 |             1126.98 |             1276.68 |             1215.07 |
| TPC-DS Q44    |             1165.07 |             1181.96 |             1174.86 |             1154.83 |             1181.82 |             1146.20 |
| TPC-DS Q45    |              217.63 |              143.93 |              140.66 |              135.37 |              168.65 |              138.83 |
| TPC-DS Q46    |             5502.38 |             3800.02 |             4170.88 |             3534.17 |             4205.41 |             4251.95 |
| TPC-DS Q47    |            14345.68 |            13441.87 |            13457.65 |            12648.00 |            13383.53 |            13805.53 |
| TPC-DS Q48    |             1272.92 |             1339.87 |             1379.83 |             1206.61 |             1347.37 |             1324.44 |
| TPC-DS Q49    |              111.87 |               96.78 |              111.16 |              113.47 |              110.14 |               89.87 |
| TPC-DS Q50    |               34.56 |               37.21 |               35.83 |               34.25 |               51.22 |               34.18 |
| TPC-DS Q51    |             7653.39 |             8029.37 |             8192.90 |             7680.66 |             9296.93 |             8714.28 |
| TPC-DS Q52    |              246.52 |              264.49 |              249.46 |              239.00 |              238.53 |              279.04 |
| TPC-DS Q53    |              143.85 |              155.63 |              143.53 |              143.00 |              142.95 |              155.68 |
| TPC-DS Q54    |             1048.88 |             1048.92 |             1034.33 |             1034.47 |             1101.29 |             1060.13 |
| TPC-DS Q55    |              229.28 |              247.48 |              227.60 |              224.44 |              255.68 |              246.92 |
| TPC-DS Q56    |              187.73 |              195.42 |              186.39 |              183.33 |              204.72 |              195.20 |
| TPC-DS Q57    |             6036.70 |             6392.01 |             6499.07 |             6089.04 |             6472.27 |             6442.59 |
| TPC-DS Q58    |             5944.94 |             7312.86 |             6721.07 |             5767.65 |             7401.82 |             7508.00 |
| TPC-DS Q59    |            11047.43 |            10566.60 |            10791.14 |             9049.94 |            10927.35 |            10747.04 |
| TPC-DS Q60    |              832.57 |              622.17 |              609.61 |              586.81 |              605.42 |              626.48 |
| TPC-DS Q61    |              390.04 |              386.09 |              385.62 |              363.84 |              413.20 |              377.21 |
| TPC-DS Q62    |             2319.48 |             2007.23 |             1930.39 |             1674.97 |             1926.94 |             1942.67 |
| TPC-DS Q63    |              262.15 |              207.31 |              164.45 |              162.91 |              200.26 |              171.74 |
| TPC-DS Q64    |              992.38 |              572.70 |              573.98 |              581.89 |              617.66 |              577.34 |
| TPC-DS Q65    |             6354.56 |             7478.49 |             7259.60 |             5843.99 |             7971.14 |             7874.61 |
| TPC-DS Q66    |             1235.07 |             1197.58 |             1205.87 |             1191.99 |             1378.54 |             1305.24 |
| TPC-DS Q67    |             7011.01 |             7170.33 |             7799.37 |             7045.88 |             8046.68 |             7982.74 |
| TPC-DS Q68    |             3061.65 |             3885.38 |             3029.25 |             3057.08 |             4063.73 |             4067.12 |
| TPC-DS Q69    |                3.57 |                2.98 |                2.98 |                3.60 |                3.69 |                2.96 |
| TPC-DS Q70    |             9522.08 |             9712.56 |            10397.34 |             8257.08 |            10838.14 |            10661.19 |
| TPC-DS Q71    |              597.96 |              477.95 |              475.43 |              485.90 |              582.93 |              495.58 |
| TPC-DS Q72    |           395212.23 |           409650.17 |           409844.91 |           391651.39 |           433132.47 |           435601.07 |
| TPC-DS Q73    |             2878.01 |             3006.95 |             3124.16 |             2908.24 |             3292.84 |             3213.67 |
| TPC-DS Q74    |             6129.58 |             6673.63 |             6618.97 |             5944.10 |             6730.25 |             6691.07 |
| TPC-DS Q75    |             5740.42 |             6206.04 |             6408.75 |             5536.32 |             6355.60 |             6155.40 |
| TPC-DS Q76    |              477.30 |              483.95 |              464.51 |              436.51 |              476.69 |              482.97 |
| TPC-DS Q77    |             6169.36 |             7420.22 |             7319.68 |             6029.10 |             7686.24 |             7760.36 |
| TPC-DS Q78    |             5676.84 |             6071.62 |             6103.93 |             5591.84 |             6073.52 |             5978.85 |
| TPC-DS Q79    |             3413.31 |             3822.91 |             3841.43 |             3421.33 |             3922.41 |             3980.36 |
| TPC-DS Q80    |              523.73 |              562.09 |              652.70 |              534.16 |              662.63 |              563.60 |
| TPC-DS Q81    |              220.88 |              220.16 |              221.36 |              212.61 |              219.78 |              212.44 |
| TPC-DS Q82    |             3862.53 |             4060.44 |             4096.51 |             3763.48 |             4172.12 |             4060.20 |
| TPC-DS Q83    |              913.73 |             1526.93 |              943.23 |              886.67 |              934.27 |             1058.47 |
| TPC-DS Q84    |               56.86 |               58.31 |               58.37 |               56.50 |               60.29 |               57.42 |
| TPC-DS Q85    |              121.47 |              130.24 |              136.11 |              121.23 |              130.96 |              128.22 |
| TPC-DS Q86    |              903.70 |             1164.70 |              964.87 |              906.07 |             1017.96 |             1163.04 |
| TPC-DS Q87    |             6966.96 |             8403.44 |             8802.19 |             7092.20 |             8822.29 |             8679.90 |
| TPC-DS Q88    |            15895.84 |            18404.17 |            18551.36 |            15518.00 |            21083.81 |            21158.54 |
| TPC-DS Q89    |             1555.02 |             1577.60 |             1782.64 |             1584.78 |             1755.49 |             1539.85 |
| TPC-DS Q90    |              341.08 |              331.89 |              389.58 |              358.96 |              396.67 |              328.63 |
| TPC-DS Q91    |               16.67 |               16.61 |               17.02 |               19.73 |               21.68 |               16.29 |
| TPC-DS Q92    |               10.02 |                9.39 |                9.23 |                9.23 |                9.79 |                9.45 |
| TPC-DS Q93    |               38.31 |               38.44 |               40.50 |               44.05 |               44.03 |               37.44 |
| TPC-DS Q96    |              779.19 |              749.65 |              800.53 |              782.43 |              763.98 |              735.48 |
| TPC-DS Q97    |             5163.54 |             5996.10 |             5872.14 |             5179.33 |             6084.32 |             6250.16 |
| TPC-DS Q98    |              879.55 |             1046.87 |             1113.54 |              883.05 |             1178.87 |             1030.93 |
| TPC-DS Q99    |             4918.81 |             5354.58 |             5563.41 |             4911.81 |             5592.88 |             5456.76 |

### Errors (failed queries)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-1-2-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-1-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-2-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |
* TPC-DS Q94
  * MariaDB-1-1-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=140) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-1-2-1-2: numRun 1: : java.sql.SQLTimeoutException: (conn=141) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=8) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=83) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-2-1-2: numRun 1: : java.sql.SQLTimeoutException: (conn=65) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=64) Query execution was interrupted (max_statement_time exceeded)
* TPC-DS Q95
  * MariaDB-1-1-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=140) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-1-2-1-2: numRun 1: : java.sql.SQLTimeoutException: (conn=141) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=8) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-1-1-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=83) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-2-1-2: numRun 1: : java.sql.SQLTimeoutException: (conn=65) Query execution was interrupted (max_statement_time exceeded)
  * MariaDB-1-2-2-1-1: numRun 1: : java.sql.SQLTimeoutException: (conn=64) Query execution was interrupted (max_statement_time exceeded)

### Warnings (result mismatch)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| MariaDB-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-1-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-2-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |
| MariaDB-1-2-2-1-2 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      2090.86 |      2.86 |           8.74 |                  8.85 |
| MariaDB-1-1-2-1 |      2090.86 |      2.86 |           8.74 |                  8.85 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |
| MariaDB-1-1-2-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |         3.46 |      0.04 |           0.00 |                  0.00 |
| MariaDB-1-1-2-1 |         3.46 |      0.04 |           0.00 |                  0.00 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      3178.46 |      1.00 |           8.84 |                  8.94 |
| MariaDB-1-1-2-1 |      6509.84 |      2.00 |           9.32 |                  9.45 |
| MariaDB-1-2-1-1 |      3150.31 |      1.00 |           5.85 |                  5.89 |
| MariaDB-1-2-2-1 |      6573.27 |      2.00 |           6.18 |                  6.23 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |        21.13 |      0.41 |           0.32 |                  0.32 |
| MariaDB-1-1-2-1 |        27.56 |      0.07 |           0.33 |                  0.33 |
| MariaDB-1-2-1-1 |        20.90 |      0.38 |           0.31 |                  0.31 |
| MariaDB-1-2-2-1 |        26.77 |      0.06 |           0.33 |                  0.33 |

### Tests
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST failed: SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: Workflow as planned
```


### MonetDB

#### TPC-DS Simple

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nlp 8 \
  -nlt 1 \
  -xii -xic -xis \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 45Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_monetdb_1.log
```

yields (after ca. 15 minutes) something like

testcase_tpcds_monetdb_1.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 758s 
    Code: 1728673738
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:255699240
    datadisk:6065064
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                  76.88
TPC-DS Q2                 531.08
TPC-DS Q3                  56.28
TPC-DS Q4                3972.34
TPC-DS Q5                 967.40
TPC-DS Q6                 224.50
TPC-DS Q7                 128.69
TPC-DS Q8                 190.76
TPC-DS Q9                 143.71
TPC-DS Q10                142.15
TPC-DS Q11               1816.96
TPC-DS Q12                 49.89
TPC-DS Q13                156.28
TPC-DS Q14a+b            6943.98
TPC-DS Q15                 52.38
TPC-DS Q16                312.98
TPC-DS Q17                434.73
TPC-DS Q18                264.32
TPC-DS Q19                 73.88
TPC-DS Q20                 60.53
TPC-DS Q21                120.54
TPC-DS Q22               2664.17
TPC-DS Q23a+b            8569.72
TPC-DS Q24a+b             363.35
TPC-DS Q25                274.53
TPC-DS Q26                 60.79
TPC-DS Q27                353.54
TPC-DS Q28                182.72
TPC-DS Q29                343.25
TPC-DS Q30                 39.49
TPC-DS Q31                533.66
TPC-DS Q32                 41.02
TPC-DS Q33                 43.13
TPC-DS Q34                 48.97
TPC-DS Q35                186.25
TPC-DS Q37                115.68
TPC-DS Q38                578.45
TPC-DS Q39a+b            3895.54
TPC-DS Q40                 84.08
TPC-DS Q41                 12.36
TPC-DS Q42                 47.25
TPC-DS Q43                 93.87
TPC-DS Q44                 66.22
TPC-DS Q45                 39.91
TPC-DS Q46                 80.79
TPC-DS Q47                557.04
TPC-DS Q48                119.43
TPC-DS Q49                288.21
TPC-DS Q50                212.09
TPC-DS Q51               1817.76
TPC-DS Q52                 35.35
TPC-DS Q53                 55.80
TPC-DS Q54                139.88
TPC-DS Q55                 28.61
TPC-DS Q56                 54.76
TPC-DS Q57                160.48
TPC-DS Q58                116.64
TPC-DS Q59                263.77
TPC-DS Q60                 56.63
TPC-DS Q61                 66.36
TPC-DS Q62                 60.03
TPC-DS Q63                 46.83
TPC-DS Q64               1045.75
TPC-DS Q65                392.84
TPC-DS Q66                301.18
TPC-DS Q67               2346.23
TPC-DS Q68                 71.98
TPC-DS Q69                 75.61
TPC-DS Q71                 61.34
TPC-DS Q72                283.64
TPC-DS Q73                 42.26
TPC-DS Q74               1788.02
TPC-DS Q75               2708.57
TPC-DS Q76                 70.94
TPC-DS Q77                178.39
TPC-DS Q78               3220.20
TPC-DS Q79                102.33
TPC-DS Q80               1819.42
TPC-DS Q81                 53.07
TPC-DS Q82                177.85
TPC-DS Q83                 30.26
TPC-DS Q84                 90.80
TPC-DS Q85                 72.05
TPC-DS Q87                794.75
TPC-DS Q88                193.52
TPC-DS Q89                 77.79
TPC-DS Q90                 20.14
TPC-DS Q91                 30.77
TPC-DS Q92                 26.66
TPC-DS Q93                303.20
TPC-DS Q94                 75.19
TPC-DS Q95                172.45
TPC-DS Q96                 25.95
TPC-DS Q97                931.61
TPC-DS Q98                 84.55
TPC-DS Q99                103.49

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          287.0         9.0      124.0     428.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.19

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           62559.68

### Throughput@Size
                                              time [s]  count  SF  Throughput@Size [~GB/h]
DBMS            SF num_experiment num_client                                              
MonetDB-BHT-8-1 3  1              1                 71      1   3                  3346.48

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Workflow as planned
```

#### TPC-DS Monitoring

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nlp 8 \
  -nlt 1 \
  -xii -xic -xis \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 45Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_monetdb_2.log
```

yields (after ca. 15 minutes) something like

testcase_tpcds_monetdb_2.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 750s 
    Code: 1728674578
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:255699500
    datadisk:6065324
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1                  71.17
TPC-DS Q2                 450.88
TPC-DS Q3                  42.54
TPC-DS Q4                3994.92
TPC-DS Q5                 938.16
TPC-DS Q6                 230.07
TPC-DS Q7                 143.51
TPC-DS Q8                 179.85
TPC-DS Q9                 139.41
TPC-DS Q10                126.56
TPC-DS Q11               1928.03
TPC-DS Q12                 41.43
TPC-DS Q13                156.77
TPC-DS Q14a+b            7366.31
TPC-DS Q15                 50.87
TPC-DS Q16                316.28
TPC-DS Q17                462.37
TPC-DS Q18                264.26
TPC-DS Q19                 83.63
TPC-DS Q20                 52.60
TPC-DS Q21                139.23
TPC-DS Q22               2539.13
TPC-DS Q23a+b            9125.71
TPC-DS Q24a+b             329.99
TPC-DS Q25                268.20
TPC-DS Q26                 62.62
TPC-DS Q27                411.59
TPC-DS Q28                173.33
TPC-DS Q29                276.84
TPC-DS Q30                 38.25
TPC-DS Q31                537.96
TPC-DS Q32                 41.58
TPC-DS Q33                 45.19
TPC-DS Q34                 50.39
TPC-DS Q35                197.19
TPC-DS Q37                144.80
TPC-DS Q38                624.65
TPC-DS Q39a+b            2705.73
TPC-DS Q40                 92.95
TPC-DS Q41                  9.05
TPC-DS Q42                 38.56
TPC-DS Q43                 95.35
TPC-DS Q44                 66.62
TPC-DS Q45                 37.50
TPC-DS Q46                 73.56
TPC-DS Q47                589.54
TPC-DS Q48                138.58
TPC-DS Q49                250.68
TPC-DS Q50                222.02
TPC-DS Q51               1888.21
TPC-DS Q52                 36.24
TPC-DS Q53                 57.38
TPC-DS Q54                127.25
TPC-DS Q55                 29.13
TPC-DS Q56                 49.88
TPC-DS Q57                277.96
TPC-DS Q58                111.17
TPC-DS Q59                263.93
TPC-DS Q60                 51.83
TPC-DS Q61                 60.86
TPC-DS Q62                 50.67
TPC-DS Q63                 52.95
TPC-DS Q64               1104.19
TPC-DS Q65                350.95
TPC-DS Q66                298.67
TPC-DS Q67               2265.86
TPC-DS Q68                 76.28
TPC-DS Q69                 36.60
TPC-DS Q71                 63.73
TPC-DS Q72                308.22
TPC-DS Q73                 41.60
TPC-DS Q74                603.63
TPC-DS Q75               3349.52
TPC-DS Q76                 75.23
TPC-DS Q77                177.01
TPC-DS Q78               3180.86
TPC-DS Q79                 81.80
TPC-DS Q80               2156.84
TPC-DS Q81                 36.36
TPC-DS Q82                129.02
TPC-DS Q83                 27.41
TPC-DS Q84                102.74
TPC-DS Q85                 72.85
TPC-DS Q87                748.00
TPC-DS Q88                183.99
TPC-DS Q89                 70.10
TPC-DS Q90                 25.53
TPC-DS Q91                 25.37
TPC-DS Q92                 28.20
TPC-DS Q93                336.76
TPC-DS Q94                 64.51
TPC-DS Q95                180.87
TPC-DS Q96                 37.48
TPC-DS Q97                914.34
TPC-DS Q98                 83.00
TPC-DS Q99                 90.09

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1           1.0          286.0         9.0      121.0     424.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1           0.18

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1            64558.7

### Throughput@Size
                                              time [s]  count  SF  Throughput@Size [~GB/h]
DBMS            SF num_experiment num_client                                              
MonetDB-BHT-8-1 3  1              1                 70      1   3                  3394.29

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Ingestion - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      686.56     1.82          1.78                 7.68

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       57.45     0.21          1.18                 2.72

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1      143.76        0          4.72                10.28

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       12.61        0          0.25                 0.26

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Ingestion SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Ingestion Loader contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### TPC-DS Throughput Test

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nlp 8 \
  -nlt 1 \
  -xii -xic -xis \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 45Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_monetdb_3.log
```

yields (after ca. 20 minutes) something like

testcase_tpcds_monetdb_3.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=3
    Type: tpcds
    Duration: 995s 
    Code: 1728675428
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=3) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
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
MonetDB-BHT-8-1-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5486698
    volume_size:100G
    volume_used:5.3G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5558770
    volume_size:100G
    volume_used:5.3G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-1-2-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5558770
    volume_size:100G
    volume_used:5.3G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5558771
    volume_size:100G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5558197
    volume_size:100G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-2-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:5558197
    volume_size:100G
    volume_used:5.4G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
            MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-1-2-2  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1  MonetDB-BHT-8-2-2-2
TPC-DS Q1                  True                 True                 True                 True                 True                False
TPC-DS Q25                 True                 True                 True                 True                 True                False
TPC-DS Q34                 True                 True                 True                 True                 True                False
TPC-DS Q43                 True                 True                 True                 True                 True                False
TPC-DS Q44                 True                 True                 True                 True                 True                False
TPC-DS Q46                 True                 True                 True                 True                 True                False
TPC-DS Q54                 True                 True                 True                 True                 True                False
TPC-DS Q68                 True                 True                 True                 True                 True                False
TPC-DS Q73                 True                 True                 True                 True                 True                False

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1-1  MonetDB-BHT-8-1-2-1  MonetDB-BHT-8-1-2-2  MonetDB-BHT-8-2-1-1  MonetDB-BHT-8-2-2-1  MonetDB-BHT-8-2-2-2
TPC-DS Q1                  1457.90                55.71                52.77              1036.26                53.04                64.40
TPC-DS Q2                  8897.17               433.92               417.83              6701.04               416.75               425.14
TPC-DS Q3                  2492.94                43.05                33.73              1810.61                40.69                38.67
TPC-DS Q4                 12439.46              3795.57              3938.42             10047.81              4018.64              3859.93
TPC-DS Q5                  6301.59               740.40               634.56              3798.51               689.95               622.01
TPC-DS Q6                   582.82               217.37               175.64               486.61               155.69               150.46
TPC-DS Q7                  2761.20                96.81                82.15              2552.40                86.28               122.09
TPC-DS Q8                  1220.89               128.82               120.85              1012.07                95.54               119.90
TPC-DS Q9                   635.23               230.87               222.55               513.18               195.19               176.37
TPC-DS Q10                 1944.22                66.97                74.34              1442.27                64.76               115.25
TPC-DS Q11                 1995.57              1960.02              1840.68              1973.40              1940.35              1893.88
TPC-DS Q12                  901.53                37.77                39.34               811.98                32.13                36.08
TPC-DS Q13                  298.44               184.98               173.74               196.24               136.51               151.76
TPC-DS Q14a+b              7875.23              7310.76              6835.78              6959.55              6064.90              5986.83
TPC-DS Q15                  317.83                40.80                36.44               183.75                33.21                57.51
TPC-DS Q16                 1582.59               280.60               283.50              1249.30               284.59               274.86
TPC-DS Q17                 1246.26               329.36               365.05              1072.00               312.44               437.02
TPC-DS Q18                  949.22               220.84               266.57              1394.53               223.82               229.80
TPC-DS Q19                  163.75                82.94                77.59               125.20                81.99                86.57
TPC-DS Q20                   58.07                52.46                51.33                52.19                48.89                50.37
TPC-DS Q21                 7896.30                66.97                93.68              5718.54                93.54               103.29
TPC-DS Q22                 2789.12              2970.36              2736.95              2785.88              2820.73              2821.87
TPC-DS Q23a+b              6467.52              6817.87              7425.04              6773.74              6912.46              6692.53
TPC-DS Q24a+b               786.52               360.59               328.72               930.28               354.57               310.32
TPC-DS Q25                  390.95               382.50               379.47               832.69               378.67               372.53
TPC-DS Q26                  414.53                62.61               113.07               230.80                60.97               153.19
TPC-DS Q27                  391.67               336.29               388.75               485.71               368.16               340.48
TPC-DS Q28                  810.17               195.01               184.20               651.45               175.24               175.50
TPC-DS Q29                  348.06               408.32               421.04               349.08               362.12               466.38
TPC-DS Q30                  256.94                51.04                48.23               135.65                65.69                32.77
TPC-DS Q31                  853.96               411.53               457.30               899.25               449.57               464.16
TPC-DS Q32                   39.75                39.67                40.41                64.72                34.82                34.99
TPC-DS Q33                  158.07                56.13                49.50                92.59                53.07                53.46
TPC-DS Q34                  667.98                44.71                44.78               439.87                45.05                51.55
TPC-DS Q35                  193.79               227.84               208.86               223.47               218.79               191.00
TPC-DS Q37                  183.74                66.45               108.31               363.26                65.78                62.99
TPC-DS Q38                  559.49               612.53               612.32               649.48               577.21               605.82
TPC-DS Q39a+b              2795.62              2621.09              2604.48              2728.80              2441.65              2736.29
TPC-DS Q40                  454.41                84.46                95.53               672.49                81.85                82.76
TPC-DS Q41                    8.78                12.81                 8.59                 9.38                 9.06                 8.77
TPC-DS Q42                   36.26                38.52                89.67                37.75                50.32                46.54
TPC-DS Q43                   99.81               105.60                94.91               101.64               105.66               116.34
TPC-DS Q44                   67.60                65.70                80.38                70.85                78.03                63.74
TPC-DS Q45                   36.77                48.37                41.96                39.58                41.19                41.62
TPC-DS Q46                  293.60               112.61                80.49               126.50                72.92               107.04
TPC-DS Q47                  652.86               629.48               689.78               665.06               646.98               666.18
TPC-DS Q48                  129.64               126.69               134.31               453.37               129.62               150.58
TPC-DS Q49                  994.84               254.84               265.41               631.35               224.06               234.91
TPC-DS Q50                  411.80               257.95               239.26               331.69               232.09               340.69
TPC-DS Q51                 1810.95              1761.45              1819.17              1792.25              1836.54              1803.62
TPC-DS Q52                   38.61                37.25                37.28                73.31                36.40                38.77
TPC-DS Q53                   63.88                57.65                57.54                66.58                56.20                70.13
TPC-DS Q54                  295.37                36.98                43.54               232.27                41.14                46.92
TPC-DS Q55                   36.21                29.34                29.12                30.14                29.58                34.00
TPC-DS Q56                   65.69                45.06                46.22                42.60                57.03                43.49
TPC-DS Q57                  258.10               182.61               187.59               196.75               187.37               228.58
TPC-DS Q58                  120.90               118.55               131.27               118.36               118.08               142.61
TPC-DS Q59                  279.80               517.06               524.65               249.02               256.63               260.00
TPC-DS Q60                  173.97                58.92                58.14               182.61                62.58                60.17
TPC-DS Q61                  132.04                67.16                66.30                91.42               167.82                64.46
TPC-DS Q62                  729.19               283.22               281.48               559.81                52.02                46.38
TPC-DS Q63                   54.77                76.32                74.40                53.21                50.57                62.17
TPC-DS Q64                 1324.58               643.39               614.00              1151.97               582.28               597.60
TPC-DS Q65                  411.61               419.52               409.04               397.73               425.15               440.10
TPC-DS Q66                 1267.26               538.76               627.83               716.93               306.93               279.70
TPC-DS Q67                 2420.32              2473.85              2260.13              2270.07              2176.51              2418.12
TPC-DS Q68                  733.11                79.67                72.15               235.31                76.59                73.66
TPC-DS Q69                  286.03                71.44                76.99                80.09                76.24                83.76
TPC-DS Q71                  493.94                60.72                72.69               104.31                64.92               420.97
TPC-DS Q72                 2568.27              3801.24              3849.62              2638.45              3913.62              2981.85
TPC-DS Q73                   52.42                42.56                42.55                42.67                44.51                44.01
TPC-DS Q74                  553.73               613.68               598.28               553.55               564.35               579.13
TPC-DS Q75                 4278.21              2325.02              2354.85              3556.34              2403.58              2328.77
TPC-DS Q76                   72.60                76.63                73.81                67.52                83.05                72.04
TPC-DS Q77                  413.48               173.82               180.13               350.36               180.41               188.84
TPC-DS Q78                 3199.09              3134.83              3575.71              3106.40              2970.40              3732.60
TPC-DS Q79                  211.67                88.75                85.18               174.57                78.34                83.01
TPC-DS Q80                 2100.88              2233.29              2029.86              2173.84              2227.43              2372.94
TPC-DS Q81                  192.89                33.27                60.99                99.19                34.15                32.81
TPC-DS Q82                  544.84                69.25                72.32               437.80                76.63                67.48
TPC-DS Q83                  133.69                21.77                21.10               176.84                21.54                22.19
TPC-DS Q84                  335.91                16.58                14.86               364.21                16.59                15.92
TPC-DS Q85                  198.42                70.18                74.61                86.76                95.47                82.30
TPC-DS Q87                  750.08               777.95               754.70               755.24               754.57               751.73
TPC-DS Q88                  789.86               191.05               199.44               504.00               180.22               205.46
TPC-DS Q89                   83.55                81.68                75.47                77.83                80.40                75.74
TPC-DS Q90                  746.61                22.87                20.18               423.59                20.78                32.37
TPC-DS Q91                  189.19                26.79                25.40                69.64                27.00                27.08
TPC-DS Q92                   27.13                25.20                24.32                24.93                25.59                26.29
TPC-DS Q93                  353.73               446.38               438.20               335.19               328.46               317.22
TPC-DS Q94                  441.25                63.27                65.71               295.77                67.04                62.92
TPC-DS Q95                  200.01               255.47               252.36               193.54               186.92               208.63
TPC-DS Q96                   25.11                25.25                24.40                24.63                24.59                25.76
TPC-DS Q97                  888.44               955.01               970.64               865.66              1030.15               947.86
TPC-DS Q98                   85.35                83.53                86.75                86.76                87.75                89.26
TPC-DS Q99                   91.98               101.54                94.49                94.38                97.89                90.17

### Loading [s]
                     timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1-1           1.0          275.0         5.0      105.0     393.0
MonetDB-BHT-8-1-2-1           1.0          275.0         5.0      105.0     393.0
MonetDB-BHT-8-1-2-2           1.0          275.0         5.0      105.0     393.0
MonetDB-BHT-8-2-1-1           1.0          275.0         5.0      105.0     393.0
MonetDB-BHT-8-2-2-1           1.0          275.0         5.0      105.0     393.0
MonetDB-BHT-8-2-2-2           1.0          275.0         5.0      105.0     393.0

### Geometric Mean of Medians of Timer Run [s]
                     Geo Times [s]
DBMS                              
MonetDB-BHT-8-1-1-1           0.43
MonetDB-BHT-8-1-2-1           0.18
MonetDB-BHT-8-1-2-2           0.18
MonetDB-BHT-8-2-1-1           0.38
MonetDB-BHT-8-2-2-1           0.17
MonetDB-BHT-8-2-2-2           0.18

### Power@Size
                     Power@Size [~Q/h]
DBMS                                  
MonetDB-BHT-8-1-1-1           25917.90
MonetDB-BHT-8-1-2-1           64333.08
MonetDB-BHT-8-1-2-2           63407.94
MonetDB-BHT-8-2-1-1           30183.86
MonetDB-BHT-8-2-2-1           67882.00
MonetDB-BHT-8-2-2-2           64231.37

### Throughput@Size
                                                time [s]  count  SF  Throughput@Size [~GB/h]
DBMS              SF num_experiment num_client                                              
MonetDB-BHT-8-1-1 3  1              1                129      1   3                  1841.86
MonetDB-BHT-8-1-2 3  1              2                 68      2   3                  6988.24
MonetDB-BHT-8-2-1 3  2              1                114      1   3                  2084.21
MonetDB-BHT-8-2-2 3  2              2                 65      2   3                  7310.77

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 2], [1, 2]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 2], [1, 2]]

### Execution - SUT
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1      238.66     0.00          3.32                 8.23
MonetDB-BHT-8-1-2      565.72     9.99         16.86                22.39
MonetDB-BHT-8-2-1     1154.98     0.00          7.93                16.96
MonetDB-BHT-8-2-2      334.40     0.00          5.01                10.34

### Execution - Benchmarker
                   CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1-1       14.10     0.05          0.25                 0.26
MonetDB-BHT-8-1-2       34.05     0.33          0.75                 0.78
MonetDB-BHT-8-2-1       34.05     0.00          0.74                 0.77
MonetDB-BHT-8-2-2       27.37     0.00          0.73                 0.76

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### TPC-DS Power Test Large

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 100 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 1000Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_monetdb_4.log
```

yields (after ca. 110 minutes) something like

testcase_tpcds_monetdb_4.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 6331s 
    Code: 1728676629
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 300Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:249634108
    datadisk:162530732
    volume_size:300G
    volume_used:155G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1
TPC-DS Q1               21540.10
TPC-DS Q2              234536.17
TPC-DS Q3               52161.56
TPC-DS Q4              383862.53
TPC-DS Q5              130445.75
TPC-DS Q6               12467.55
TPC-DS Q7               73421.64
TPC-DS Q8               47626.63
TPC-DS Q9               35999.02
TPC-DS Q10              13875.78
TPC-DS Q11              87521.23
TPC-DS Q12               2813.57
TPC-DS Q13               7253.94
TPC-DS Q14a+b          410993.67
TPC-DS Q15              11345.34
TPC-DS Q16              20444.94
TPC-DS Q17             112165.36
TPC-DS Q18              24168.99
TPC-DS Q19               5743.73
TPC-DS Q20               1023.79
TPC-DS Q21              91704.61
TPC-DS Q22              86337.22
TPC-DS Q23a+b         2736895.84
TPC-DS Q24a+b            6107.79
TPC-DS Q25              20943.89
TPC-DS Q26               1762.98
TPC-DS Q27              28616.77
TPC-DS Q28              24479.10
TPC-DS Q29              14225.98
TPC-DS Q30               2905.96
TPC-DS Q31              22703.53
TPC-DS Q32                535.63
TPC-DS Q33              14858.80
TPC-DS Q34               2961.26
TPC-DS Q35               7629.06
TPC-DS Q37              34972.06
TPC-DS Q38              29446.64
TPC-DS Q39a+b           79446.39
TPC-DS Q40               5005.79
TPC-DS Q41                340.97
TPC-DS Q42               2261.78
TPC-DS Q43               2160.14
TPC-DS Q44               3335.84
TPC-DS Q45               1007.63
TPC-DS Q46               2493.34
TPC-DS Q47               5878.41
TPC-DS Q48               1175.38
TPC-DS Q49              38294.50
TPC-DS Q50               3741.81
TPC-DS Q51              50318.14
TPC-DS Q52               1265.41
TPC-DS Q53               2107.47
TPC-DS Q54               7608.31
TPC-DS Q55               2060.64
TPC-DS Q56              12970.61
TPC-DS Q57               2303.47
TPC-DS Q58               5467.10
TPC-DS Q59              11463.27
TPC-DS Q60               3737.78
TPC-DS Q61               4874.03
TPC-DS Q62               3992.80
TPC-DS Q63                950.49
TPC-DS Q64              45759.04
TPC-DS Q65              25361.62
TPC-DS Q66              21174.82
TPC-DS Q67             112971.25
TPC-DS Q68               9680.79
TPC-DS Q69               3257.94
TPC-DS Q71               4878.81
TPC-DS Q72              32102.01
TPC-DS Q73                322.64
TPC-DS Q74              24826.16
TPC-DS Q75             187073.16
TPC-DS Q76              14043.38
TPC-DS Q77               8627.66
TPC-DS Q78             191797.32
TPC-DS Q79               5074.40
TPC-DS Q80             117303.11
TPC-DS Q81               2790.04
TPC-DS Q82              28911.03
TPC-DS Q83               1952.11
TPC-DS Q84                879.36
TPC-DS Q85               3602.37
TPC-DS Q87              59126.34
TPC-DS Q88               3332.16
TPC-DS Q89               3645.28
TPC-DS Q90               1185.67
TPC-DS Q91               1299.77
TPC-DS Q92               2001.95
TPC-DS Q93              28101.76
TPC-DS Q94               2069.09
TPC-DS Q95              18037.05
TPC-DS Q96                119.80
TPC-DS Q97              42468.49
TPC-DS Q98               3413.94
TPC-DS Q99               1930.03

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1        4023.0         1362.0         6.0     2703.0    8096.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          10.34

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           35243.87

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               6117      1  100                  1294.75

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    20233.87     16.8        133.36               245.14

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       42.02     0.06          0.39                  0.4

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
```

#### TPC-DS Throughput Test Large

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 100 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -nc 2 \
  -ne 1,5 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 1000Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_monetdb_5.log
```

yields (after ca. 360 minutes) something like

testcase_tpcds_monetdb_5.log
```markdown
## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 20752s 
    Code: 1729497306
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 300Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1, 5, 5] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250321764
    datadisk:288744504
    volume_size:300G
    volume_used:276G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322104
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-3 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-4 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-5 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-3 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-4 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-5 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
               MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
TPC-DS Q23a+b              False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q24a+b              False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q25                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q26                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q27                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q28                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q29                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q30                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q31                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q32                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q33                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q34                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q35                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q37                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q38                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q39a+b              False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q40                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q41                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q42                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q43                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q44                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q45                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q46                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q47                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q48                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q49                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q50                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q51                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q52                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q53                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q54                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q55                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q56                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q57                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q58                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q59                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q60                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q61                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q62                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q63                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q64                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q65                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q66                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q67                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q68                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q69                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q71                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q72                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q73                 False              False               True               True               True              False              False              False               True               True               True              False
TPC-DS Q74                 False              False               True               True               True              False              False              False               True               True               True              False
TPC-DS Q75                 False              False               True               True               True              False              False              False               True               True               True               True
TPC-DS Q76                 False              False               True               True               True              False              False               True               True               True               True               True
TPC-DS Q77                 False              False               True               True               True              False              False               True               True               True               True               True
TPC-DS Q78                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q79                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q80                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q81                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q82                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q83                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q84                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q85                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q87                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q88                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q89                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q90                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q91                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q92                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q93                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q94                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q95                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q96                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q97                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q98                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q99                 False              False               True               True               True               True               True               True               True               True               True               True

### Warnings (result mismatch)
            MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
TPC-DS Q1                True               True               True              False               True               True               True               True               True               True               True               True
TPC-DS Q34               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q46               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q54               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q68               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q69               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q71               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q72               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q73               True               True              False              False              False               True               True               True              False              False              False               True
TPC-DS Q74               True               True              False              False              False               True               True               True              False              False              False               True
TPC-DS Q75               True               True              False              False              False               True               True               True              False              False              False              False
TPC-DS Q76               True               True              False              False              False               True               True              False              False              False              False              False
TPC-DS Q77               True               True              False              False              False               True               True              False              False              False              False              False
TPC-DS Q78               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q79               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q80               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q81               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q82               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q83               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q84               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q85               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q87               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q88               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q89               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q90               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q91               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q92               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q93               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q94               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q95               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q96               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q97               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q98               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q99               True               True              False              False              False              False              False              False              False              False              False              False

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
TPC-DS Q1               27370.75            2398.34            3427.48            3548.13            2621.80            3349.98            2533.30           42994.62           43099.49           42921.18           42831.04           42908.51
TPC-DS Q2              290821.48           12968.89           42420.72           43545.27           43077.55           42017.09           43019.55          587520.51          587142.92          589163.04          587448.87          588656.35
TPC-DS Q3              113297.32            2534.75            2226.94            1311.94            2827.32            2754.30            2898.16          126104.75          126592.93          124695.38          126524.33          125210.92
TPC-DS Q4              419012.49          151417.82          841027.33          841979.72          771544.18          758497.43          987181.05          863825.28          842226.46          875548.69          841795.93          864986.88
TPC-DS Q5              152472.27           25913.86           38700.56           38704.71           75992.76           89474.50           35704.63          280847.09          302657.12          272871.72          309269.37          290256.00
TPC-DS Q6               10465.72            6148.11            8494.14            8372.64           20295.71           19794.75           10755.25           39960.65           38099.00           35536.35           36848.37           32571.94
TPC-DS Q7               85464.02            1717.00             656.49             659.43           14569.19           14941.80             779.82          125905.42          127393.38          126724.35          122928.01          123021.42
TPC-DS Q8               31537.49            2868.56           51567.86           50598.40           57879.85           57629.18            4131.33           37375.11           37821.85           37375.05           37374.59           37374.76
TPC-DS Q9               24558.10            2959.41            9601.51            7915.98            8954.79            8555.44            2609.90           39832.01           37006.15           39783.22           39745.52           39686.99
TPC-DS Q10               4798.43            1708.85           10055.94           12059.05           11024.65           11410.25            1068.77            8830.09           11203.75            8863.00            8856.28            8982.50
TPC-DS Q11              74948.80           74442.53          127970.28          129086.83          119531.67          127820.74           98889.67          128465.69          116448.46          123230.43          115624.77          126471.84
TPC-DS Q12               1922.56             586.98             489.47             429.42            8194.10             615.13             359.98             302.72             711.24            3474.69            1657.43             523.10
TPC-DS Q13               2705.39            1601.06            3541.62            2587.14            4190.26            3541.01             356.11             335.97            8615.20             375.12            8625.05             414.59
TPC-DS Q14a+b          331389.83          274582.58          495565.35          450771.53          450517.42          450518.97          498161.82          544996.30          520469.11          543487.22          534403.23          570664.29
TPC-DS Q15              11234.26            1133.29             539.39            3274.29            3533.18            3535.34             704.67             639.50           14143.56             606.52             869.53            1274.78
TPC-DS Q16              25139.98             863.51             783.43            5917.83            5936.80            5181.27             795.14           43898.62           57727.55           46832.57           57696.69           19303.74
TPC-DS Q17              57273.54           34438.89          136125.32          173456.87          179543.43          175108.63           85005.01          218938.52          223817.53          219048.18          220848.61          219440.73
TPC-DS Q18              26480.21            8663.66           22465.62           22848.76           15768.86           21216.73           21039.15           51344.16           46580.72           51222.66           49248.84           50783.59
TPC-DS Q19               2424.20            2259.17            6801.66            6127.00            6794.42            6798.48            6977.89            9677.23            9660.20            9704.29            9707.72            9694.76
TPC-DS Q20                941.11             498.07             859.07             876.10            1179.98            1178.25            1177.47             731.59             729.09             735.39             730.50             730.95
TPC-DS Q21             115406.12             950.95            6428.35            6422.47            6412.70            6404.55            6426.69          142631.61          142621.07          142619.30          142613.04          142602.51
TPC-DS Q22              91135.38           81955.21           97082.60          112905.33          112828.09          107411.61           97016.26           97696.66          110253.74           97281.24           91222.80          121667.95

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-2-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-2        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-3        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-4        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-5        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-2        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-3        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-4        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-5        4023.0         1362.0         6.0     2703.0    8096.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          29.76
MonetDB-BHT-8-2-1           5.57
MonetDB-BHT-8-3-1          11.35
MonetDB-BHT-8-3-2          13.07
MonetDB-BHT-8-3-3          19.37
MonetDB-BHT-8-3-4          17.48
MonetDB-BHT-8-3-5           7.76
MonetDB-BHT-8-4-1          35.40
MonetDB-BHT-8-4-2          49.88
MonetDB-BHT-8-4-3          39.40
MonetDB-BHT-8-4-4          44.92
MonetDB-BHT-8-4-5          36.51

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           12115.25
MonetDB-BHT-8-2-1           64912.63
MonetDB-BHT-8-3-1           31815.26
MonetDB-BHT-8-3-2           27619.23
MonetDB-BHT-8-3-3           18609.96
MonetDB-BHT-8-3-4           20642.87
MonetDB-BHT-8-3-5           46558.91
MonetDB-BHT-8-4-1           10194.85
MonetDB-BHT-8-4-2            7229.98
MonetDB-BHT-8-4-3            9147.06
MonetDB-BHT-8-4-4            8024.32
MonetDB-BHT-8-4-5            9884.43

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               6889      1  100                  1149.66
MonetDB-BHT-8-2 100 1              2               3711      1  100                  2134.20
MonetDB-BHT-8-3 100 1              3               4040      5  100                  9801.98
MonetDB-BHT-8-4 100 1              4               5477      5  100                  7230.24

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 5, 5]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 5, 5]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    21745.36    17.29        173.03               283.57
MonetDB-BHT-8-2    18120.57    20.21        188.28               290.39
MonetDB-BHT-8-3    43989.47    42.21        461.98               484.15
MonetDB-BHT-8-4    50356.12    45.19        457.93               484.00

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       39.84     0.10          0.38                 0.41
MonetDB-BHT-8-2       39.84     0.01          0.63                 0.66
MonetDB-BHT-8-3       80.27     0.03          1.58                 1.62
MonetDB-BHT-8-4      126.49     0.12          1.78                 1.82

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_postgresql_1.log
```

yields (after ca. 10 minutes) something like

testcase_benchbase_postgresql_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 847s 
* Code: 1782361771
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:261336
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782361771
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      333.00 |           1.00 |            0.00 |        139.00 |          193.00 |              1 |           1 |             |                |             0 | False         |              172.97 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |           0 | 300.00 |           56 |                        4792.09 |                     4717.51 |         0.00 |                                                     112400.00 |                                              32132.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |     8192 |               1 |           1 |           0 | 300.00 |           56 |                        4792.09 |                     4717.51 |         0.00 |                                                     112400.00 |                                              32132.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_postgresql_2.log
```

yields (after ca. 10 minutes) something like

testcase_benchbase_postgresql_2.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 824s 
* Code: 1782362661
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 1 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:244255
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782362661
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253332
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782362661
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      749.00 |           1.00 |            0.00 |        348.00 |          400.00 |              0 |           1 |             |                |             0 | False         |               76.90 |
| PostgreSQL-1-2 |                2 |   16 |      749.00 |           1.00 |            0.00 |        348.00 |          400.00 |              0 |           1 |             |                |             0 | False         |               76.90 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |           0 |  60.00 |            0 |                         225.15 |                      225.35 |         0.00 |                                                    2749686.00 |                                             707141.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |         160 |     8192 |        1 |               1 |       1 |           0 |  60.00 |            0 |                         548.00 |                      545.47 |         0.00 |                                                    1122286.00 |                                             290238.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |     8192 |               1 |           1 |           0 |  60.00 |            0 |                         225.15 |                      225.35 |         0.00 |                                                    2749686.00 |                                             707141.00 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |         160 |     8192 |               1 |           1 |           0 |  60.00 |            0 |                         548.00 |                      545.47 |         0.00 |                                                    1122286.00 |                                             290238.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_postgresql_3.log
```

yields (after ca. 10 minutes) something like

testcase_benchbase_postgresql_3.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 798s 
* Code: 1782363495
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:261715
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782363495
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      276.00 |           1.00 |            0.00 |        113.00 |          162.00 |              1 |           1 |             |                |             0 | False         |              208.70 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |           0 | 300.00 |           83 |                        8172.76 |                     8052.75 |         0.00 |                                                      50599.00 |                                              15381.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |     8192 |               1 |           1 |           0 | 300.00 |           83 |                        8172.76 |                     8052.75 |         0.00 |                                                      50599.00 |                                              15381.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       329.45 |      5.91 |           2.05 |                  3.69 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      1244.38 |     13.91 |           0.25 |                  0.25 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      4782.46 |     17.72 |           5.83 |                  9.53 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |      3821.02 |     14.14 |           0.91 |                  0.91 |

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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_postgresql_4.log
```

yields (after ca. 30 minutes) something like

testcase_benchbase_postgresql_4.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2471s 
* Code: 1782364325
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222623
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:223817
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-2-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False
* PostgreSQL-1-2-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364325
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: benchbase (4 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: benchbase (4 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      749.00 |           1.00 |            0.00 |        348.00 |          400.00 |              0 |           1 |             |                |             0 | False         |               76.90 |
| PostgreSQL-1-2 |                2 |   16 |      749.00 |           1.00 |            0.00 |        348.00 |          400.00 |              0 |           1 |             |                |             0 | False         |               76.90 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:---------------------|:-----------------|:-------------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |           0 | 120.00 |            0 |                         636.60 |                      630.76 |         0.00 |                                                    1090371.00 |                                             249829.00 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       1 |           0 | 120.00 |            1 |                         477.71 |                      473.88 |         0.00 |                                                    1685708.00 |                                             332123.00 |
| PostgreSQL-1-1-2-1-2 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       2 |           0 | 120.00 |            0 |                         485.80 |                      481.89 |         0.00 |                                                    1652145.00 |                                             326588.00 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       1 |           0 | 120.00 |            0 |                         505.12 |                      500.57 |         0.00 |                                                     641983.00 |                                             157003.00 |
| PostgreSQL-1-1-3-1-2 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       2 |           0 | 120.00 |            0 |                         494.12 |                      489.75 |         0.00 |                                                     658908.00 |                                             161178.00 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       1 |           0 | 120.00 |            1 |                         204.44 |                      203.08 |         0.00 |                                                    1848759.00 |                                             386955.00 |
| PostgreSQL-1-1-4-1-2 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       2 |           0 | 120.00 |            0 |                         210.92 |                      209.42 |         0.00 |                                                    1797703.00 |                                             374969.00 |
| PostgreSQL-1-1-4-1-3 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       3 |           0 | 120.00 |            0 |                         208.47 |                      207.16 |         0.00 |                                                    1882198.00 |                                             380525.00 |
| PostgreSQL-1-1-4-1-4 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       4 |           0 | 120.00 |            1 |                         205.55 |                      204.31 |         0.00 |                                                    1848898.00 |                                             384630.00 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |         160 |     8192 |        1 |               1 |       1 |           0 | 120.00 |            0 |                         489.02 |                      485.34 |         0.00 |                                                    1401511.00 |                                             326610.00 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       1 |           0 | 120.00 |            0 |                         588.40 |                      583.32 |         0.00 |                                                    1262257.00 |                                             269739.00 |
| PostgreSQL-1-2-2-1-2 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       2 |           0 | 120.00 |            0 |                         580.57 |                      575.71 |         0.00 |                                                    1278093.00 |                                             272905.00 |
| PostgreSQL-1-2-3-1-1 | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       1 |           0 | 120.00 |            0 |                         616.69 |                      611.22 |         0.00 |                                                     461185.00 |                                             129369.00 |
| PostgreSQL-1-2-3-1-2 | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       2 |           0 | 120.00 |            0 |                         616.21 |                      610.55 |         0.00 |                                                     457243.00 |                                             129474.00 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       1 |           0 | 120.00 |            0 |                         204.86 |                      203.47 |         0.00 |                                                    1865151.00 |                                             387985.00 |
| PostgreSQL-1-2-4-1-2 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       2 |           0 | 120.00 |            0 |                         209.17 |                      207.83 |         0.00 |                                                    1812033.00 |                                             381303.00 |
| PostgreSQL-1-2-4-1-3 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       3 |           0 | 120.00 |            0 |                         205.87 |                      204.22 |         0.00 |                                                    1825412.00 |                                             385903.00 |
| PostgreSQL-1-2-4-1-4 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       4 |           0 | 120.00 |            0 |                         212.42 |                      211.01 |         0.00 |                                                    1775657.00 |                                             374683.00 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:-----------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |         160 |     8192 |               1 |           1 |           0 | 120.00 |            0 |                         636.60 |                      630.76 |         0.00 |                                                    1090371.00 |                                             249829.00 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |         320 |    16384 |               1 |           2 |           0 | 120.00 |            1 |                         963.51 |                      955.77 |         0.00 |                                                    1685708.00 |                                             329355.50 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |         160 |     8192 |               1 |           2 |           0 | 120.00 |            0 |                         999.23 |                      990.32 |         0.00 |                                                     658908.00 |                                             159090.50 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |         320 |    16384 |               1 |           4 |           0 | 120.00 |            2 |                         829.38 |                      823.97 |         0.00 |                                                    1882198.00 |                                             381769.75 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |         160 |     8192 |               1 |           1 |           0 | 120.00 |            0 |                         489.02 |                      485.34 |         0.00 |                                                    1401511.00 |                                             326610.00 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |         320 |    16384 |               1 |           2 |           0 | 120.00 |            0 |                        1168.97 |                     1159.03 |         0.00 |                                                    1278093.00 |                                             271322.00 |
| PostgreSQL-1-2-3 | PostgreSQL-1-2-3 |                2 |         160 |     8192 |               1 |           2 |           0 | 120.00 |            0 |                        1232.90 |                     1221.77 |         0.00 |                                                     461185.00 |                                             129421.50 |
| PostgreSQL-1-2-4 | PostgreSQL-1-2-4 |                2 |         320 |    16384 |               1 |           4 |           0 | 120.00 |            0 |                         832.32 |                      826.52 |         0.00 |                                                    1865151.00 |                                             382468.50 |

### Monitoring

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       236.54 |      2.99 |           2.46 |                  3.76 |
| PostgreSQL-1-1-2-1 |       564.62 |      5.99 |           3.89 |                  5.51 |
| PostgreSQL-1-1-3-1 |       516.64 |      5.85 |           3.32 |                  5.23 |
| PostgreSQL-1-1-4-1 |       551.32 |      6.39 |           4.54 |                  6.64 |
| PostgreSQL-1-2-1-1 |      2029.18 |      3.83 |           2.47 |                  4.59 |
| PostgreSQL-1-2-2-1 |       928.13 |      8.71 |           3.88 |                  5.48 |
| PostgreSQL-1-2-3-1 |       782.87 |      7.32 |           3.40 |                  5.33 |
| PostgreSQL-1-2-4-1 |       579.57 |      6.13 |           4.51 |                  6.64 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       107.31 |      1.48 |           0.65 |                  0.65 |
| PostgreSQL-1-1-2-1 |       164.51 |      2.76 |           0.70 |                  0.70 |
| PostgreSQL-1-1-3-1 |       150.72 |      2.63 |           0.70 |                  0.70 |
| PostgreSQL-1-1-4-1 |       175.11 |      2.44 |           0.41 |                  0.41 |
| PostgreSQL-1-2-1-1 |        80.68 |      1.15 |           0.65 |                  0.65 |
| PostgreSQL-1-2-2-1 |       159.50 |      3.15 |           0.68 |                  0.68 |
| PostgreSQL-1-2-3-1 |       177.14 |      3.20 |           0.68 |                  0.68 |
| PostgreSQL-1-2-4-1 |       156.33 |      3.24 |           0.41 |                  0.41 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mysql_1.log
```

yields (after ca. 10 minutes) something like

testcase_benchbase_mysql_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 945s 
* Code: 1782361781
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:267301
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782361781
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   16 |      340.00 |           2.00 |            0.00 |        148.00 |          190.00 |              1 |           1 |             |                |             0 | False         |              169.41 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        5342.18 |                     5259.56 |         0.00 |                                                      88779.00 |                                              28617.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 300.00 |            0 |                        5342.18 |                     5259.56 |         0.00 |                                                      88779.00 |                                              28617.00 |

### Tests
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST passed: Workflow as planned
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mysql_2.log
```

yields (after ca. 10 minutes) something like

testcase_benchbase_mysql_2.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mysql_3.log
```

yields (after ca. 10 minutes) something like

testcase_benchbase_mysql_3.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 977s 
* Code: 1782363268
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1-1 uses docker image mysql:8.4.0
  * RAM:540492877824
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:260482
  * cpu_list:0-127
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782363268
    * TENANT_VOL:False

### Workflow

#### Actual

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MySQL-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MySQL-1-1 |                1 |   16 |      355.00 |           2.00 |            0.00 |        159.00 |          194.00 |              1 |           1 |             |                |             0 | False         |              162.25 |

### Execution

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1-1-1 | MySQL-1-1-1 | MySQL-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        5472.97 |                     5384.40 |         0.00 |                                                      81681.00 |                                              29194.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MySQL-1-1-1 | MySQL-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 300.00 |            0 |                        5472.97 |                     5384.40 |         0.00 |                                                      81681.00 |                                              29194.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |       414.07 |      7.90 |           9.58 |                 12.83 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      1724.24 |     14.72 |           0.55 |                  0.55 |

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      6946.42 |     26.99 |          11.03 |                 16.00 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1-1 |      5191.00 |     21.74 |           1.36 |                  1.36 |

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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mysql_4.log
```

yields (after ca. 30 minutes) something like

testcase_benchbase_mysql_4.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mariadb_1.log
```

yields (after ca. 10 minutes) something like

testcase_benchbase_mariadb_1.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 835s 
* Code: 1782361791
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:261844
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782361791

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      265.00 |           2.00 |            0.00 |        114.00 |          149.00 |              1 |           1 |             | None           |             0 | False         |              217.36 |

### Execution

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1-1 | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        6489.12 |                     6382.97 |         0.00 |                                                      68949.00 |                                              21665.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 300.00 |            0 |                        6489.12 |                     6382.97 |         0.00 |                                                      68949.00 |                                              21665.00 |

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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mariadb_2.log
```

yields (after ca. 10 minutes) something like

testcase_benchbase_mariadb_2.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1331s 
* Code: 1782362666
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 1 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253332
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782362666
* MariaDB-1-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:260794
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782362666

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: benchbase (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      761.00 |           2.00 |            0.00 |        356.00 |          403.00 |              1 |           1 |             | None           |             0 | False         |               75.69 |
| MariaDB-1-2 |                2 |   16 |      761.00 |           2.00 |            0.00 |        356.00 |          403.00 |              1 |           1 |             | None           |             0 | False         |               75.69 |

### Execution

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1-1 | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 |  60.00 |            0 |                        1143.50 |                     1127.18 |         0.00 |                                                     542141.00 |                                             137600.00 |
| MariaDB-1-2-1-1-1 | MariaDB-1-2-1 | MariaDB-1-2-1-1 |                2 |         160 |     8192 |        1 |               1 |       1 |          -1 |  60.00 |            0 |                        1116.67 |                     1101.28 |         0.00 |                                                     250549.00 |                                             130235.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 |  60.00 |            0 |                        1143.50 |                     1127.18 |         0.00 |                                                     542141.00 |                                             137600.00 |
| MariaDB-1-2-1 | MariaDB-1-2-1 |                2 |         160 |     8192 |               1 |           1 |          -1 |  60.00 |            0 |                        1116.67 |                     1101.28 |         0.00 |                                                     250549.00 |                                             130235.00 |

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
  -lr 64Gi \
  -rr 64Gi \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mariadb_3.log
```

yields (after ca. 10 minutes) something like

testcase_benchbase_mariadb_3.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 893s 
* Code: 1782364006
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222370
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364006

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      332.00 |           2.00 |            0.00 |        142.00 |          188.00 |              1 |           1 |             | None           |             0 | False         |              173.49 |

### Execution

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1-1 | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        8191.94 |                     8102.43 |         0.00 |                                                      10659.00 |                                               5096.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 300.00 |            0 |                        8191.94 |                     8102.43 |         0.00 |                                                      10659.00 |                                               5096.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |       267.20 |      3.31 |           3.79 |                  3.89 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      1835.23 |     15.32 |           0.24 |                  0.24 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      5273.25 |     18.16 |           5.49 |                  5.60 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      4183.33 |     14.61 |           1.67 |                  1.67 |

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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mariadb_4.log
```

yields (after ca. 30 minutes) something like

testcase_benchbase_mariadb_4.log
```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 2495s 
* Code: 1782364932
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [8]. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [160] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-1-2-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-1-3-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-1-4-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:2.0G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-2-1-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:2.3G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-2-2-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:2.3G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-2-3-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:2.3G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932
* MariaDB-1-2-4-1 uses docker image mariadb:11.4.7
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:2.3G
  * cpu_list:0-127
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364932

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: benchbase (4 pods)

#### Planned

* DBMS MariaDB-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 3: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 1 Client 4: benchbase (4 pods)
* DBMS MariaDB-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS MariaDB-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 3: benchbase (2 pods)
* DBMS MariaDB-1 - Experiment 2 Client 4: benchbase (4 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MariaDB-1-1 |                1 |   16 |      761.00 |           2.00 |            0.00 |        356.00 |          403.00 |              0 |           1 |             | None           |             0 | False         |               75.69 |
| MariaDB-1-2 |                2 |   16 |      761.00 |           2.00 |            0.00 |        356.00 |          403.00 |              0 |           1 |             | None           |             0 | False         |               75.69 |

### Execution

#### Per Connection

| DBMS              | phase         | job             |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------------|:--------------|:----------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1-1-1 | MariaDB-1-1-1 | MariaDB-1-1-1-1 |                1 |         160 |     8192 |        1 |               1 |       1 |          -1 | 120.00 |            0 |                         967.06 |                      952.57 |         0.00 |                                                     492745.00 |                                             164974.00 |
| MariaDB-1-1-2-1-1 | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       1 |          -1 | 120.00 |            0 |                         320.49 |                      316.64 |         0.00 |                                                    2093763.00 |                                             494056.00 |
| MariaDB-1-1-2-1-2 | MariaDB-1-1-2 | MariaDB-1-1-2-1 |                1 |         160 |     8192 |        2 |               1 |       2 |          -1 | 120.00 |            0 |                         242.21 |                      239.85 |         0.00 |                                                    2804421.00 |                                             659793.00 |
| MariaDB-1-1-3-1-1 | MariaDB-1-1-3 | MariaDB-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       1 |          -1 | 120.00 |            0 |                         451.47 |                      445.15 |         0.00 |                                                     135576.00 |                                             169888.00 |
| MariaDB-1-1-3-1-2 | MariaDB-1-1-3 | MariaDB-1-1-3-1 |                1 |          80 |     4096 |        3 |               1 |       2 |          -1 | 120.00 |            0 |                         425.37 |                      419.38 |         0.00 |                                                     141231.00 |                                             179604.00 |
| MariaDB-1-1-4-1-1 | MariaDB-1-1-4 | MariaDB-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       1 |          -1 | 120.00 |            0 |                         210.65 |                      208.06 |         0.00 |                                                    1383547.00 |                                             379692.00 |
| MariaDB-1-1-4-1-2 | MariaDB-1-1-4 | MariaDB-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       2 |          -1 | 120.00 |            0 |                         232.05 |                      229.02 |         0.00 |                                                    1189542.00 |                                             343797.00 |
| MariaDB-1-1-4-1-3 | MariaDB-1-1-4 | MariaDB-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       3 |          -1 | 120.00 |            0 |                         213.38 |                      210.43 |         0.00 |                                                    1355253.00 |                                             374383.00 |
| MariaDB-1-1-4-1-4 | MariaDB-1-1-4 | MariaDB-1-1-4-1 |                1 |          80 |     4096 |        4 |               1 |       4 |          -1 | 120.00 |            0 |                         225.12 |                      222.47 |         0.00 |                                                    1238071.00 |                                             353898.00 |
| MariaDB-1-2-1-1-1 | MariaDB-1-2-1 | MariaDB-1-2-1-1 |                2 |         160 |     8192 |        1 |               1 |       1 |          -1 | 120.00 |            0 |                         920.43 |                      906.26 |         0.00 |                                                     571446.00 |                                             172230.00 |
| MariaDB-1-2-2-1-1 | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       1 |          -1 | 120.00 |            0 |                         427.24 |                      421.13 |         0.00 |                                                    1017372.00 |                                             372815.00 |
| MariaDB-1-2-2-1-2 | MariaDB-1-2-2 | MariaDB-1-2-2-1 |                2 |         160 |     8192 |        2 |               1 |       2 |          -1 | 120.00 |            0 |                         357.92 |                      353.82 |         0.00 |                                                    1227140.00 |                                             445660.00 |
| MariaDB-1-2-3-1-1 | MariaDB-1-2-3 | MariaDB-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       1 |          -1 | 120.00 |            0 |                         379.06 |                      373.49 |         0.00 |                                                     917359.00 |                                             199443.00 |
| MariaDB-1-2-3-1-2 | MariaDB-1-2-3 | MariaDB-1-2-3-1 |                2 |          80 |     4096 |        3 |               1 |       2 |          -1 | 120.00 |            0 |                         348.27 |                      343.62 |         0.00 |                                                     987067.00 |                                             216431.00 |
| MariaDB-1-2-4-1-1 | MariaDB-1-2-4 | MariaDB-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       1 |          -1 | 120.00 |            0 |                         200.48 |                      197.60 |         0.00 |                                                    1357630.00 |                                             397247.00 |
| MariaDB-1-2-4-1-2 | MariaDB-1-2-4 | MariaDB-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       2 |          -1 | 120.00 |            0 |                         220.92 |                      217.98 |         0.00 |                                                    1163093.00 |                                             360457.00 |
| MariaDB-1-2-4-1-3 | MariaDB-1-2-4 | MariaDB-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       3 |          -1 | 120.00 |            0 |                         202.23 |                      199.54 |         0.00 |                                                    1305829.00 |                                             395153.00 |
| MariaDB-1-2-4-1-4 | MariaDB-1-2-4 | MariaDB-1-2-4-1 |                2 |          80 |     4096 |        4 |               1 |       4 |          -1 | 120.00 |            0 |                         207.67 |                      205.04 |         0.00 |                                                    1262583.00 |                                             384669.00 |

#### Per Phase

| DBMS          | phase         |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:--------------|:--------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| MariaDB-1-1-1 | MariaDB-1-1-1 |                1 |         160 |     8192 |               1 |           1 |          -1 | 120.00 |            0 |                         967.06 |                      952.57 |         0.00 |                                                     492745.00 |                                             164974.00 |
| MariaDB-1-1-2 | MariaDB-1-1-2 |                1 |         320 |    16384 |               1 |           2 |          -1 | 120.00 |            0 |                         562.70 |                      556.49 |         0.00 |                                                    2804421.00 |                                             576924.50 |
| MariaDB-1-1-3 | MariaDB-1-1-3 |                1 |         160 |     8192 |               1 |           2 |          -1 | 120.00 |            0 |                         876.85 |                      864.53 |         0.00 |                                                     141231.00 |                                             174746.00 |
| MariaDB-1-1-4 | MariaDB-1-1-4 |                1 |         320 |    16384 |               1 |           4 |          -1 | 120.00 |            0 |                         881.21 |                      869.98 |         0.00 |                                                    1383547.00 |                                             362942.50 |
| MariaDB-1-2-1 | MariaDB-1-2-1 |                2 |         160 |     8192 |               1 |           1 |          -1 | 120.00 |            0 |                         920.43 |                      906.26 |         0.00 |                                                     571446.00 |                                             172230.00 |
| MariaDB-1-2-2 | MariaDB-1-2-2 |                2 |         320 |    16384 |               1 |           2 |          -1 | 120.00 |            0 |                         785.17 |                      774.95 |         0.00 |                                                    1227140.00 |                                             409237.50 |
| MariaDB-1-2-3 | MariaDB-1-2-3 |                2 |         160 |     8192 |               1 |           2 |          -1 | 120.00 |            0 |                         727.33 |                      717.11 |         0.00 |                                                     987067.00 |                                             207937.00 |
| MariaDB-1-2-4 | MariaDB-1-2-4 |                2 |         320 |    16384 |               1 |           4 |          -1 | 120.00 |            0 |                         831.32 |                      820.17 |         0.00 |                                                    1357630.00 |                                             384381.50 |

### Monitoring

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |      2031.17 |     28.21 |           4.00 |                  4.10 |
| MariaDB-1-1-2-1 |      1322.28 |     18.92 |           4.23 |                  4.33 |
| MariaDB-1-1-3-1 |      1209.81 |     13.68 |           4.33 |                  4.43 |
| MariaDB-1-1-4-1 |      1048.15 |     11.39 |           4.49 |                  4.59 |
| MariaDB-1-2-1-1 |      1304.29 |     14.17 |           4.26 |                  4.36 |
| MariaDB-1-2-2-1 |      1065.69 |     15.92 |           4.55 |                  4.65 |
| MariaDB-1-2-3-1 |       926.95 |     10.39 |           4.62 |                  4.72 |
| MariaDB-1-2-4-1 |      1001.09 |     12.19 |           4.80 |                  4.90 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1-1 |       194.52 |      2.35 |           0.70 |                  0.70 |
| MariaDB-1-1-2-1 |       168.41 |      2.97 |           0.74 |                  0.74 |
| MariaDB-1-1-3-1 |       213.01 |      3.25 |           0.74 |                  0.74 |
| MariaDB-1-1-4-1 |       253.99 |      3.43 |           0.50 |                  0.50 |
| MariaDB-1-2-1-1 |       197.18 |      2.65 |           0.71 |                  0.71 |
| MariaDB-1-2-2-1 |       228.81 |      4.92 |           0.79 |                  0.79 |
| MariaDB-1-2-3-1 |       171.83 |      4.99 |           0.79 |                  0.79 |
| MariaDB-1-2-4-1 |       235.27 |      4.42 |           0.49 |                  0.49 |

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
  -lr 64Gi \
  -rr 64Gi \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_postgresql_1.log
```

yields (after ca. 10 minutes)

testcase_hammerdb_postgresql_1.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 867s 
* Code: 1782362075
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:271027
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782362075

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      200.00 |           2.00 |            0.00 |         80.00 |          118.00 |              1 |           8 |             | None           |             0 | False         |              288.00 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |     TPM |   efficiency |   duration |   errors |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|--------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       16 |        1 |               1 |       1 | 461948 | 1061903 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |      NOPM |        TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|----------:|-----------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 461948.00 | 1061903.00 |          5 |        0 |

### Tests
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_postgresql_2.log
```

yields (after ca. 15 minutes)

testcase_hammerdb_postgresql_2.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 997s 
* Code: 1782362983
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:253332
  * volume_size:30G
  * volume_used:3.3G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782362983

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      364.00 |           2.00 |            0.00 |        165.00 |          197.00 |              1 |           8 |             | None           |             0 | False         |              158.24 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       16 |        1 |               1 |       1 |  14626 | 33661 |         0.00 |          5 |        0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |     NOPM |      TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|---------:|---------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 14626.00 | 33661.00 |          5 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        84.21 |      0.73 |           1.69 |                  3.22 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       253.02 |      4.30 |           0.09 |                  0.09 |

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       360.15 |      1.28 |           2.14 |                  3.93 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        35.38 |      0.11 |           0.07 |                  0.07 |

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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_postgresql_3.log
```

yields (after ca. 60 minutes)

testcase_hammerdb_postgresql_3.log
```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 3463s 
* Code: 1782364015
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 2 minutes.
  * Experiment uses bexhoma version 0.10.0.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker38.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* PostgreSQL-1-1-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:277941
  * volume_size:30G
  * volume_used:4.1G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-1-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:222745
  * volume_size:30G
  * volume_used:4.1G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-1-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:4.1G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-1-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:4.1G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-2-1-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:4.8G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-2-2-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:4.8G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-2-3-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220472
  * volume_size:30G
  * volume_used:4.8G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015
* PostgreSQL-1-2-4-1 uses docker image postgres:18.3
  * RAM:540492877824
  * CPU:Intel(R) Xeon(R) Gold 6430
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker38
  * disk:220471
  * volume_size:30G
  * volume_used:4.8G
  * cpu_list:0-127
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1782364015

### Workflow

#### Actual

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: hammerdb (4 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 4: hammerdb (4 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 3: hammerdb (2 pods)
* DBMS PostgreSQL-1 - Experiment 2 Client 4: hammerdb (4 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| PostgreSQL-1-1 |                1 |   16 |      364.00 |           2.00 |            0.00 |        165.00 |          197.00 |              0 |           8 |             | None           |             0 | False         |              158.24 |
| PostgreSQL-1-2 |                2 |   16 |      364.00 |           2.00 |            0.00 |        165.00 |          197.00 |              0 |           8 |             | None           |             0 | False         |              158.24 |

### Execution

#### Per Connection

| DBMS                 | phase            | job                |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |   TPM |   efficiency |   duration |   errors |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|------:|-------------:|-----------:|---------:|
| PostgreSQL-1-1-1-1-1 | PostgreSQL-1-1-1 | PostgreSQL-1-1-1-1 |                1 |       16 |        1 |               1 |       1 |  13209 | 30504 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |       16 |        2 |               1 |       1 |  15790 | 36578 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-2-1-1 | PostgreSQL-1-1-2 | PostgreSQL-1-1-2-1 |                1 |       16 |        2 |               1 |       1 |  15782 | 36339 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |        8 |        3 |               1 |       1 |  11178 | 25963 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-3-1-1 | PostgreSQL-1-1-3 | PostgreSQL-1-1-3-1 |                1 |        8 |        3 |               1 |       1 |  11180 | 25823 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |        8 |        4 |               1 |       1 |  13528 | 31357 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |        8 |        4 |               1 |       1 |  13555 | 31424 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |        8 |        4 |               1 |       1 |  13558 | 31395 |         0.00 |          2 |        0 |
| PostgreSQL-1-1-4-1-1 | PostgreSQL-1-1-4 | PostgreSQL-1-1-4-1 |                1 |        8 |        4 |               1 |       1 |  13582 | 31502 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-1-1-1 | PostgreSQL-1-2-1 | PostgreSQL-1-2-1-1 |                2 |       16 |        1 |               1 |       1 |   8849 | 20432 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |       16 |        2 |               1 |       1 |  13977 | 32490 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-2-1-1 | PostgreSQL-1-2-2 | PostgreSQL-1-2-2-1 |                2 |       16 |        2 |               1 |       1 |  13912 | 32276 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-3-1-1 | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 |                2 |        8 |        3 |               1 |       1 |  11789 | 27254 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-3-1-1 | PostgreSQL-1-2-3 | PostgreSQL-1-2-3-1 |                2 |        8 |        3 |               1 |       1 |  11806 | 27287 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |        8 |        4 |               1 |       1 |  14962 | 34299 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |        8 |        4 |               1 |       1 |  14852 | 33988 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |        8 |        4 |               1 |       1 |  14883 | 34103 |         0.00 |          2 |        0 |
| PostgreSQL-1-2-4-1-1 | PostgreSQL-1-2-4 | PostgreSQL-1-2-4-1 |                2 |        8 |        4 |               1 |       1 |  14925 | 34225 |         0.00 |          2 |        0 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   efficiency |     NOPM |      TPM |   duration |   errors |
|:-----------------|:-----------------|-----------------:|---------:|---------:|----------------:|------------:|-------------:|---------:|---------:|-----------:|---------:|
| PostgreSQL-1-1-1 | PostgreSQL-1-1-1 |                1 |       16 |        1 |               1 |           1 |         0.00 | 13209.00 | 30504.00 |          2 |        0 |
| PostgreSQL-1-1-2 | PostgreSQL-1-1-2 |                1 |       32 |        2 |               1 |           2 |         0.00 | 15786.00 | 36458.50 |          2 |        0 |
| PostgreSQL-1-1-3 | PostgreSQL-1-1-3 |                1 |       16 |        3 |               1 |           2 |         0.00 | 11179.00 | 25893.00 |          2 |        0 |
| PostgreSQL-1-1-4 | PostgreSQL-1-1-4 |                1 |       32 |        4 |               1 |           4 |         0.00 | 13555.75 | 31419.50 |          2 |        0 |
| PostgreSQL-1-2-1 | PostgreSQL-1-2-1 |                2 |       16 |        1 |               1 |           1 |         0.00 |  8849.00 | 20432.00 |          2 |        0 |
| PostgreSQL-1-2-2 | PostgreSQL-1-2-2 |                2 |       32 |        2 |               1 |           2 |         0.00 | 13944.50 | 32383.00 |          2 |        0 |
| PostgreSQL-1-2-3 | PostgreSQL-1-2-3 |                2 |       16 |        3 |               1 |           2 |         0.00 | 11797.50 | 27270.50 |          2 |        0 |
| PostgreSQL-1-2-4 | PostgreSQL-1-2-4 |                2 |       32 |        4 |               1 |           4 |         0.00 | 14905.50 | 34153.75 |          2 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |       165.55 |      0.82 |           1.26 |                  2.95 |
| PostgreSQL-1-1-2-1 |       135.36 |      1.02 |           1.82 |                  3.76 |
| PostgreSQL-1-1-3-1 |       325.31 |      1.74 |           2.19 |                  4.24 |
| PostgreSQL-1-1-4-1 |      1809.44 |     11.38 |           2.74 |                  4.91 |
| PostgreSQL-1-2-1-1 |      2484.00 |      5.72 |           2.15 |                  4.34 |
| PostgreSQL-1-2-2-1 |      2138.16 |     11.27 |           2.27 |                  4.59 |
| PostgreSQL-1-2-3-1 |      1298.34 |      7.16 |           2.18 |                  4.59 |
| PostgreSQL-1-2-4-1 |      2151.17 |     12.22 |           2.72 |                  5.27 |

### Execution phase: component benchmarker

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| PostgreSQL-1-1-1-1 |        13.46 |      0.08 |           0.07 |                  0.07 |
| PostgreSQL-1-1-2-1 |        13.82 |      0.20 |           0.07 |                  0.07 |
| PostgreSQL-1-1-3-1 |        21.41 |      0.19 |           0.07 |                  0.07 |
| PostgreSQL-1-1-4-1 |        18.60 |      0.28 |           0.04 |                  0.05 |
| PostgreSQL-1-2-1-1 |         9.53 |      0.05 |           0.07 |                  0.07 |
| PostgreSQL-1-2-2-1 |        13.03 |      0.12 |           0.07 |                  0.07 |
| PostgreSQL-1-2-3-1 |        21.69 |      0.14 |           0.07 |                  0.07 |
| PostgreSQL-1-2-4-1 |        17.99 |      0.24 |           0.04 |                  0.05 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: NOPM contains no 0 or NaN
* TEST passed: Workflow as planned
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mysql_1.log
```

yields (after ca. 10 minutes)

testcase_hammerdb_mysql_1.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mysql_2.log
```

yields (after ca. 15 minutes)

testcase_hammerdb_mysql_2.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mysql_3.log
```

yields (after ca. 60 minutes)

testcase_hammerdb_mysql_3.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mariadb_1.log
```

yields (after ca. 10 minutes)

testcase_hammerdb_mariadb_1.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mariadb_2.log
```

yields (after ca. 15 minutes)

testcase_hammerdb_mariadb_2.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mariadb_3.log
```

yields (after ca. 60 minutes)

testcase_hammerdb_mariadb_3.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_postgresql_1.log
```

yields (after ca. 15 minutes) something like

testcase_ycsb_postgresql_1.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_postgresql_2.log
```

yields (after ca. 10 minutes) something like

testcase_ycsb_postgresql_2.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_postgresql_3.log
```

yields (after ca. 15 minutes) something like

testcase_ycsb_postgresql_3.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_postgresql_4.log
```

yields (after ca. 5 minutes) something like

testcase_ycsb_postgresql_4.log
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_postgresql_5.log
```

yields (after ca. 10 minutes) something like

testcase_ycsb_postgresql_5.log
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


### MySQL

#### YCSB Loader Test for Scaling the Driver

```bash
bexhoma ycsb \
  -dbms MySQL \
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mysql_1.log
```

yields (after ca. 165 minutes) something like

testcase_ycsb_mysql_1.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 9694s 
* Code: 1780391716
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 4 and 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Loading is tested with [32, 64] threads, split into [4, 8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:94107
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780391716
* MySQL-2-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:94075
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780391716
* MySQL-3-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:94108
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780391716
* MySQL-4-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:94080
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780391716

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1]]
* DBMS MySQL-2 - Pods [[1]]
* DBMS MySQL-3 - Pods [[1]]
* DBMS MySQL-4 - Pods [[1]]

#### Planned

* DBMS MySQL-1 - Pods [[1]]
* DBMS MySQL-2 - Pods [[1]]
* DBMS MySQL-3 - Pods [[1]]
* DBMS MySQL-4 - Pods [[1]]

### Loading

#### Per Connection

| connection    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-0-1 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          254.24 |               983341.00 |            250000.00 |                             16495.00 |
| MySQL-1-1-0-2 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          254.41 |               982675.00 |            250000.00 |                             16559.00 |
| MySQL-1-1-0-3 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          254.31 |               983041.00 |            250000.00 |                             16335.00 |
| MySQL-1-1-0-4 |             1.00 |      8.00 |   256.00 |        4.00 |         0.00 |                          254.21 |               983433.00 |            250000.00 |                             16511.00 |
| MySQL-2-1-0-1 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977335.00 |            125000.00 |                             16127.00 |
| MySQL-2-1-0-2 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977360.00 |            125000.00 |                             16135.00 |
| MySQL-2-1-0-3 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977383.00 |            125000.00 |                             16119.00 |
| MySQL-2-1-0-4 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977431.00 |            125000.00 |                             16079.00 |
| MySQL-2-1-0-5 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977384.00 |            125000.00 |                             16383.00 |
| MySQL-2-1-0-6 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977356.00 |            125000.00 |                             16255.00 |
| MySQL-2-1-0-7 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.90 |               977329.00 |            125000.00 |                             16231.00 |
| MySQL-2-1-0-8 |             1.00 |      4.00 |   128.00 |        8.00 |         0.00 |                          127.89 |               977377.00 |            125000.00 |                             15999.00 |
| MySQL-3-1-0-1 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          254.10 |               983854.00 |            250000.00 |                             16447.00 |
| MySQL-3-1-0-2 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          254.26 |               983244.00 |            250000.00 |                             16703.00 |
| MySQL-3-1-0-3 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          254.17 |               983604.00 |            250000.00 |                             16575.00 |
| MySQL-3-1-0-4 |             1.00 |     16.00 |   256.00 |        4.00 |         0.00 |                          254.06 |               984030.00 |            250000.00 |                             16447.00 |
| MySQL-4-1-0-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977529.00 |            125000.00 |                             16575.00 |
| MySQL-4-1-0-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977501.00 |            125000.00 |                             16927.00 |
| MySQL-4-1-0-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977470.00 |            125000.00 |                             16303.00 |
| MySQL-4-1-0-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977549.00 |            125000.00 |                             16287.00 |
| MySQL-4-1-0-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977536.00 |            125000.00 |                             16327.00 |
| MySQL-4-1-0-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.87 |               977566.00 |            125000.00 |                             16143.00 |
| MySQL-4-1-0-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.88 |               977473.00 |            125000.00 |                             16623.00 |
| MySQL-4-1-0-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          127.85 |               977696.00 |            125000.00 |                             16167.00 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     32.00 |  1024.00 |        4.00 |         0.00 |                         1017.17 |               983433.00 |           1000000.00 |                             16475.00 |
| MySQL-2-1 |             1.00 |     32.00 |  1024.00 |        8.00 |         0.00 |                         1023.15 |               977431.00 |           1000000.00 |                             16166.00 |
| MySQL-3-1 |             1.00 |     64.00 |  1024.00 |        4.00 |         0.00 |                         1016.59 |               984030.00 |           1000000.00 |                             16543.00 |
| MySQL-4-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                         1022.98 |               977696.00 |           1000000.00 |                             16419.00 |

### Execution

#### Per Connection

| DBMS          | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1022.03 |               978441.00 |             499891 |                            1225.00 |               500109 |                             14967.00 |
| MySQL-2-1-1-1 | MySQL-2         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1022.07 |               978404.00 |             498987 |                            1218.00 |               501013 |                             15103.00 |
| MySQL-3-1-1-1 | MySQL-3         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1022.21 |               978274.00 |             499498 |                            1215.00 |               500502 |                             15111.00 |
| MySQL-4-1-1-1 | MySQL-4         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1021.89 |               978579.00 |             500273 |                            1174.00 |               499727 |                             15015.00 |

#### Per Phase

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1022.03 |               978441.00 |          499891.00 |                            1225.00 |            500109.00 |                             14967.00 |
| MySQL-2-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1022.07 |               978404.00 |          498987.00 |                            1218.00 |            501013.00 |                             15103.00 |
| MySQL-3-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1022.21 |               978274.00 |          499498.00 |                            1215.00 |            500502.00 |                             15111.00 |
| MySQL-4-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1021.89 |               978579.00 |          500273.00 |                            1174.00 |            499727.00 |                             15015.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

#### YCSB Loader Test for Persistency

```bash
bexhoma ycsb \
  -dbms MySQL \
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mysql_2.log
```

yields (after ca. 310 minutes) something like

testcase_ycsb_mysql_2.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 18369s 
* Code: 1780401423
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MySQL-1-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:36G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780401423
* MySQL-1-2-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:37G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780401423

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1], [1]]

#### Planned

* DBMS MySQL-1 - Pods [[1], [1]]

### Loading

#### Per Connection

| connection    |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-0-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13859599.00 |            125000.00 |                          15671295.00 |
| MySQL-1-1-0-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13859976.00 |            125000.00 |                          15704063.00 |
| MySQL-1-1-0-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13859372.00 |            125000.00 |                          15302655.00 |
| MySQL-1-1-0-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13860975.00 |            125000.00 |                          15597567.00 |
| MySQL-1-1-0-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.03 |             13838752.00 |            125000.00 |                          15359999.00 |
| MySQL-1-1-0-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.03 |             13850251.00 |            125000.00 |                          15376383.00 |
| MySQL-1-1-0-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13859977.00 |            125000.00 |                          15278079.00 |
| MySQL-1-1-0-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                            9.02 |             13861550.00 |            125000.00 |                          15294463.00 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                           72.17 |             13861550.00 |           1000000.00 |                          15448063.00 |

### Execution

#### Per Connection

| DBMS          | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                          870.36 |              1148951.00 |             500404 |                            1849.00 |               499596 |                           2787327.00 |
| MySQL-1-2-1-1 | MySQL-1         |                2 |        1 |       1 |        64 |     1024 |           1 |            0 |                          721.94 |              1385149.00 |             500619 |                            2027.00 |               499381 |                           3078143.00 |

#### Per Phase

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                          870.36 |              1148951.00 |          500404.00 |                            1849.00 |            499596.00 |                           2787327.00 |
| MySQL-1-2-1 |             2.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                          721.94 |              1385149.00 |          500619.00 |                            2027.00 |            499381.00 |                           3078143.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

#### YCSB Execution for Scaling and Repetition

```bash
bexhoma ycsb \
  -dbms MySQL \
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mysql_3.log
```

yields (after ca. 240 minutes) something like

testcase_ycsb_mysql_3.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 14280s 
* Code: 1780419828
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MySQL-1-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:38G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-1-2 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:39G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-1-3 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:40G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-1-4 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:41G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-2-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58111
  * volume_size:50G
  * volume_used:42G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-2-2 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:43G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-2-3 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:45G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828
* MySQL-1-2-4 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:46G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780419828

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

#### Planned

* DBMS MySQL-1 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

### Execution

#### Per Connection

| DBMS           | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:---------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|-----------------------------:|--------------------------------------------:|
| MySQL-1-1-1-1  | MySQL-1         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                          799.12 |              1251370.00 |             499858 |                            3715.00 |               500142 |                           2648063.00 |                            0 |                                        0.00 |
| MySQL-1-1-2-1  | MySQL-1         |                1 |        2 |       1 |        64 |     1024 |           2 |            0 |                          317.95 |              1572571.00 |             249489 |                            1995.00 |               250511 |                          10338303.00 |                            0 |                                        0.00 |
| MySQL-1-1-2-2  | MySQL-1         |                1 |        2 |       2 |        64 |     1024 |           2 |            0 |                          317.75 |              1573578.00 |             249971 |                            2020.00 |               250029 |                          10264575.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-6  | MySQL-1         |                1 |        3 |       6 |         8 |      128 |           8 |            0 |                           86.87 |              1438964.00 |              62549 |                            2001.00 |                62451 |                           3461119.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-5  | MySQL-1         |                1 |        3 |       5 |         8 |      128 |           8 |            0 |                           86.65 |              1442551.00 |              62392 |                            2019.00 |                62608 |                           3383295.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-4  | MySQL-1         |                1 |        3 |       4 |         8 |      128 |           8 |            0 |                           86.71 |              1441583.00 |              62464 |                            1996.00 |                62536 |                           3477503.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-3  | MySQL-1         |                1 |        3 |       3 |         8 |      128 |           8 |            0 |                           86.71 |              1441629.00 |              62683 |                            2003.00 |                62317 |                           3522559.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-1  | MySQL-1         |                1 |        3 |       1 |         8 |      128 |           8 |            0 |                           87.12 |              1434739.00 |              62433 |                            1967.00 |                62567 |                           3463167.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-7  | MySQL-1         |                1 |        3 |       7 |         8 |      128 |           8 |            0 |                           86.74 |              1441125.00 |              62557 |                            2067.00 |                62443 |                           3471359.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-2  | MySQL-1         |                1 |        3 |       2 |         8 |      128 |           8 |            0 |                           86.83 |              1439515.00 |              62275 |                            2027.00 |                62725 |                           3309567.00 |                            0 |                                        0.00 |
| MySQL-1-1-3-8  | MySQL-1         |                1 |        3 |       8 |         8 |      128 |           8 |            0 |                           86.64 |              1442721.00 |              62417 |                            1967.00 |                62583 |                           3383295.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-15 | MySQL-1         |                1 |        4 |      15 |         8 |      128 |          16 |            0 |                           44.02 |              1419810.00 |              31207 |                            1996.00 |                31293 |                           9428991.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-12 | MySQL-1         |                1 |        4 |      12 |         8 |      128 |          16 |            0 |                           44.06 |              1418399.00 |              31251 |                            1992.00 |                31249 |                           9297919.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-14 | MySQL-1         |                1 |        4 |      14 |         8 |      128 |          16 |            0 |                           44.01 |              1420260.00 |              31367 |                            2003.00 |                31133 |                           9150463.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-16 | MySQL-1         |                1 |        4 |      16 |         8 |      128 |          16 |            0 |                           43.91 |              1423264.00 |              31373 |                            2010.00 |                31127 |                           9191423.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-7  | MySQL-1         |                1 |        4 |       7 |         8 |      128 |          16 |            0 |                           43.87 |              1424547.00 |              31150 |                            1932.00 |                31350 |                           9576447.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-6  | MySQL-1         |                1 |        4 |       6 |         8 |      128 |          16 |            0 |                           43.94 |              1422349.00 |              31287 |                            1985.00 |                31213 |                           9093119.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-8  | MySQL-1         |                1 |        4 |       8 |         8 |      128 |          16 |            0 |                           43.87 |              1424554.00 |              31353 |                            1924.00 |                31147 |                           9347071.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-13 | MySQL-1         |                1 |        4 |      13 |         8 |      128 |          16 |            0 |                           43.81 |              1426530.00 |              31151 |                            1978.00 |                31349 |                           9682943.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-2  | MySQL-1         |                1 |        4 |       2 |         8 |      128 |          16 |            0 |                           43.92 |              1422925.00 |              31166 |                            2025.00 |                31334 |                           9510911.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-10 | MySQL-1         |                1 |        4 |      10 |         8 |      128 |          16 |            0 |                           43.91 |              1423479.00 |              31278 |                            2003.00 |                31222 |                           9650175.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-11 | MySQL-1         |                1 |        4 |      11 |         8 |      128 |          16 |            0 |                           43.95 |              1422210.00 |              31181 |                            1981.00 |                31319 |                           9428991.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-3  | MySQL-1         |                1 |        4 |       3 |         8 |      128 |          16 |            0 |                           43.92 |              1423130.00 |              31370 |                            1924.00 |                31130 |                           9437183.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-1  | MySQL-1         |                1 |        4 |       1 |         8 |      128 |          16 |            0 |                           43.97 |              1421566.00 |              31036 |                            1974.00 |                31464 |                           9535487.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-5  | MySQL-1         |                1 |        4 |       5 |         8 |      128 |          16 |            0 |                           43.82 |              1426251.00 |              31139 |                            1990.00 |                31361 |                           9347071.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-4  | MySQL-1         |                1 |        4 |       4 |         8 |      128 |          16 |            0 |                           44.14 |              1415857.00 |              31329 |                            1977.00 |                31171 |                           9355263.00 |                            0 |                                        0.00 |
| MySQL-1-1-4-9  | MySQL-1         |                1 |        4 |       9 |         8 |      128 |          16 |            0 |                           43.97 |              1421577.00 |              31304 |                            1916.00 |                31196 |                           9347071.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-6  | MySQL-1         |                2 |        4 |       6 |         8 |      128 |          16 |            0 |                           47.23 |              1323341.00 |              31286 |                            1927.00 |                31214 |                           7749631.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-10 | MySQL-1         |                2 |        4 |      10 |         8 |      128 |          16 |            0 |                           47.09 |              1327367.00 |              30946 |                            2001.00 |                31553 |                           7737343.00 |                            1 |                                 50102271.00 |
| MySQL-1-2-4-11 | MySQL-1         |                2 |        4 |      11 |         8 |      128 |          16 |            0 |                           47.12 |              1326408.00 |              31134 |                            1946.00 |                31365 |                           7688191.00 |                            1 |                                 50888703.00 |
| MySQL-1-2-4-4  | MySQL-1         |                2 |        4 |       4 |         8 |      128 |          16 |            0 |                           47.31 |              1321003.00 |              31401 |                            1920.00 |                31098 |                           7692287.00 |                            1 |                                 50888703.00 |
| MySQL-1-2-4-12 | MySQL-1         |                2 |        4 |      12 |         8 |      128 |          16 |            0 |                           47.33 |              1320481.00 |              31286 |                            1999.00 |                31214 |                           7647231.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-16 | MySQL-1         |                2 |        4 |      16 |         8 |      128 |          16 |            0 |                           47.15 |              1325516.00 |              31368 |                            2042.00 |                31132 |                           8011775.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-13 | MySQL-1         |                2 |        4 |      13 |         8 |      128 |          16 |            0 |                           47.14 |              1325750.00 |              31170 |                            1972.00 |                31330 |                           7647231.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-5  | MySQL-1         |                2 |        4 |       5 |         8 |      128 |          16 |            0 |                           47.18 |              1324636.00 |              31034 |                            1946.00 |                31466 |                           7827455.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-1  | MySQL-1         |                2 |        4 |       1 |         8 |      128 |          16 |            0 |                           47.14 |              1325850.00 |              31057 |                            1946.00 |                31443 |                           7622655.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-7  | MySQL-1         |                2 |        4 |       7 |         8 |      128 |          16 |            0 |                           47.18 |              1324723.00 |              31258 |                            1944.00 |                31241 |                           7651327.00 |                            1 |                                 50167807.00 |
| MySQL-1-2-4-8  | MySQL-1         |                2 |        4 |       8 |         8 |      128 |          16 |            0 |                           47.20 |              1324175.00 |              31333 |                            2021.00 |                31167 |                           7778303.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-3  | MySQL-1         |                2 |        4 |       3 |         8 |      128 |          16 |            0 |                           47.22 |              1323649.00 |              30973 |                            1989.00 |                31526 |                           7770111.00 |                            1 |                                 50102271.00 |
| MySQL-1-2-4-2  | MySQL-1         |                2 |        4 |       2 |         8 |      128 |          16 |            0 |                           47.24 |              1323105.00 |              31411 |                            1912.00 |                31089 |                           7757823.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-9  | MySQL-1         |                2 |        4 |       9 |         8 |      128 |          16 |            0 |                           47.11 |              1326685.00 |              31164 |                            1924.00 |                31333 |                           7704575.00 |                            3 |                                 50364415.00 |
| MySQL-1-2-1-1  | MySQL-1         |                2 |        1 |       1 |        64 |     1024 |           1 |            0 |                          673.11 |              1485637.00 |             500509 |                            2063.00 |               499491 |                           3090431.00 |                            0 |                                        0.00 |
| MySQL-1-2-2-1  | MySQL-1         |                2 |        2 |       1 |        64 |     1024 |           2 |            0 |                          351.74 |              1421499.00 |             249566 |                            1984.00 |               250434 |                           8437759.00 |                            0 |                                        0.00 |
| MySQL-1-2-2-2  | MySQL-1         |                2 |        2 |       2 |        64 |     1024 |           2 |            0 |                          351.75 |              1421453.00 |             249874 |                            1988.00 |               250126 |                           8536063.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-1  | MySQL-1         |                2 |        3 |       1 |         8 |      128 |           8 |            0 |                           77.33 |              1616421.00 |              62630 |                            1859.00 |                62370 |                           3301375.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-6  | MySQL-1         |                2 |        3 |       6 |         8 |      128 |           8 |            0 |                           79.69 |              1568582.00 |              62561 |                            1917.00 |                62439 |                           3235839.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-7  | MySQL-1         |                2 |        3 |       7 |         8 |      128 |           8 |            0 |                           80.53 |              1552262.00 |              62129 |                            1912.00 |                62871 |                           3102719.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-2  | MySQL-1         |                2 |        3 |       2 |         8 |      128 |           8 |            0 |                           80.40 |              1554681.00 |              62478 |                            1911.00 |                62522 |                           3170303.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-5  | MySQL-1         |                2 |        3 |       5 |         8 |      128 |           8 |            0 |                           80.05 |              1561613.00 |              62351 |                            1923.00 |                62649 |                           3207167.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-4  | MySQL-1         |                2 |        3 |       4 |         8 |      128 |           8 |            0 |                           79.21 |              1578158.00 |              62447 |                            1878.00 |                62553 |                           3235839.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-3  | MySQL-1         |                2 |        3 |       3 |         8 |      128 |           8 |            0 |                           79.12 |              1579887.00 |              62739 |                            1873.00 |                62261 |                           3223551.00 |                            0 |                                        0.00 |
| MySQL-1-2-3-8  | MySQL-1         |                2 |        3 |       8 |         8 |      128 |           8 |            0 |                           80.33 |              1556101.00 |              62439 |                            1948.00 |                62561 |                           3172351.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-14 | MySQL-1         |                2 |        4 |      14 |         8 |      128 |          16 |            0 |                           47.18 |              1324659.00 |              31349 |                            1887.00 |                31151 |                           7749631.00 |                            0 |                                        0.00 |
| MySQL-1-2-4-15 | MySQL-1         |                2 |        4 |      15 |         8 |      128 |          16 |            0 |                           47.10 |              1326985.00 |              31303 |                            1909.00 |                31197 |                           7770111.00 |                            0 |                                        0.00 |

#### Per Phase

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |   [UPDATE-FAILED].Operations |   [UPDATE-FAILED].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|-----------------------------:|--------------------------------------------:|
| MySQL-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                          799.12 |              1251370.00 |          499858.00 |                            3715.00 |            500142.00 |                           2648063.00 |                         0.00 |                                        0.00 |
| MySQL-1-1-2 |             1.00 |    128.00 |  2048.00 |        2.00 |         0.00 |                          635.70 |              1573578.00 |          499460.00 |                            2020.00 |            500540.00 |                          10338303.00 |                         0.00 |                                        0.00 |
| MySQL-1-1-3 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                          694.28 |              1442721.00 |          499770.00 |                            2067.00 |            500230.00 |                           3522559.00 |                         0.00 |                                        0.00 |
| MySQL-1-1-4 |             1.00 |    128.00 |  2048.00 |       16.00 |         0.00 |                          703.09 |              1426530.00 |          499942.00 |                            2025.00 |            500058.00 |                           9682943.00 |                         0.00 |                                        0.00 |
| MySQL-1-2-1 |             2.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                          673.11 |              1485637.00 |          500509.00 |                            2063.00 |            499491.00 |                           3090431.00 |                         0.00 |                                        0.00 |
| MySQL-1-2-2 |             2.00 |    128.00 |  2048.00 |        2.00 |         0.00 |                          703.49 |              1421499.00 |          499440.00 |                            1988.00 |            500560.00 |                           8536063.00 |                         0.00 |                                        0.00 |
| MySQL-1-2-3 |             2.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                          636.65 |              1616421.00 |          499774.00 |                            1948.00 |            500226.00 |                           3301375.00 |                         0.00 |                                        0.00 |
| MySQL-1-2-4 |             2.00 |    128.00 |  2048.00 |       16.00 |         0.00 |                          754.92 |              1327367.00 |          499473.00 |                            2042.00 |            500519.00 |                           8011775.00 |                         8.00 |                                 50888703.00 |

### Tests
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
```

#### YCSB Execution Different Workload

```bash
bexhoma ycsb \
  -dbms MySQL \
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mysql_4.log
```

yields (after ca. 35 minutes) something like

testcase_ycsb_mysql_4.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2060s 
* Code: 1780434280
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'E'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:47G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780434280

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[8]]

#### Planned

* DBMS MySQL-1 - Pods [[8]]

### Execution

#### Per Connection

| DBMS          | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:--------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| MySQL-1-1-1-6 | MySQL-1         |                1 |        1 |       6 |         8 |      128 |           8 |            0 |                          120.68 |              1035758.00 |                 6204 |                            500991.00 |             118796 |                            9911.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-8 | MySQL-1         |                1 |        1 |       8 |         8 |      128 |           8 |            0 |                          120.76 |              1035129.00 |                 6294 |                            499199.00 |             118706 |                           10063.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-2 | MySQL-1         |                1 |        1 |       2 |         8 |      128 |           8 |            0 |                          120.68 |              1035786.00 |                 6163 |                            520703.00 |             118837 |                            9663.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |       1 |         8 |      128 |           8 |            0 |                          120.92 |              1033741.00 |                 6156 |                            499199.00 |             118844 |                            9575.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-4 | MySQL-1         |                1 |        1 |       4 |         8 |      128 |           8 |            0 |                          120.61 |              1036361.00 |                 6206 |                            506623.00 |             118794 |                           10783.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-5 | MySQL-1         |                1 |        1 |       5 |         8 |      128 |           8 |            0 |                          120.80 |              1034731.00 |                 6250 |                            503295.00 |             118666 |                           10231.00 |                           84 |                                     8019.00 |
| MySQL-1-1-1-3 | MySQL-1         |                1 |        1 |       3 |         8 |      128 |           8 |            0 |                          120.77 |              1035015.00 |                 6185 |                            516607.00 |             118815 |                           10183.00 |                            0 |                                        0.00 |
| MySQL-1-1-1-7 | MySQL-1         |                1 |        1 |       7 |         8 |      128 |           8 |            0 |                          120.68 |              1035769.00 |                 6250 |                            502527.00 |             118678 |                           10631.00 |                           72 |                                    17871.00 |

#### Per Phase

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| MySQL-1-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                          965.92 |              1036361.00 |             49708.00 |                            520703.00 |          950136.00 |                           10783.00 |                       156.00 |                                    17871.00 |

### Tests
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
```

#### YCSB Execution Monitoring

```bash
bexhoma ycsb \
  -dbms MySQL \
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mysql_5.log
```

yields (after ca. 70 minutes) something like

testcase_ycsb_mysql_5.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 4009s 
* Code: 1780436349
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MySQL'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MySQL-1-1-1 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:47G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780436349
* MySQL-1-1-2 uses docker image mysql:8.4.0
  * RAM:541006622720
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58112
  * volume_size:50G
  * volume_used:48G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--local-infile=1', '--mysql-native-password=ON', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=96G', '--innodb-buffer-pool-instances=16', '--innodb-buffer-pool-chunk-size=2G', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--innodb-flush-log-at-trx-commit=2', '--innodb-change-buffer-max-size=50', '--innodb-doublewrite=0', '--tmpdir=/mysqltmp']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * eval_parameters
    * code:1780436349

### Workflow

#### Actual

* DBMS MySQL-1 - Pods [[1, 8]]

#### Planned

* DBMS MySQL-1 - Pods [[1, 8]]

### Execution

#### Per Connection

| DBMS          | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1-1 | MySQL-1         |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                          652.25 |              1533148.00 |             500318 |                           46815.00 |               499682 |                           3174399.00 |
| MySQL-1-1-2-8 | MySQL-1         |                1 |        2 |       8 |         8 |      128 |           8 |            0 |                           81.87 |              1526776.00 |              62363 |                            1977.00 |                62637 |                           3074047.00 |
| MySQL-1-1-2-2 | MySQL-1         |                1 |        2 |       2 |         8 |      128 |           8 |            0 |                           81.80 |              1528065.00 |              62418 |                            1949.00 |                62582 |                           3078143.00 |
| MySQL-1-1-2-4 | MySQL-1         |                1 |        2 |       4 |         8 |      128 |           8 |            0 |                           81.97 |              1524923.00 |              62545 |                            1914.00 |                62455 |                           3176447.00 |
| MySQL-1-1-2-6 | MySQL-1         |                1 |        2 |       6 |         8 |      128 |           8 |            0 |                           82.01 |              1524218.00 |              62333 |                            1935.00 |                62667 |                           3194879.00 |
| MySQL-1-1-2-1 | MySQL-1         |                1 |        2 |       1 |         8 |      128 |           8 |            0 |                           81.97 |              1525016.00 |              62588 |                            1965.00 |                62412 |                           3112959.00 |
| MySQL-1-1-2-3 | MySQL-1         |                1 |        2 |       3 |         8 |      128 |           8 |            0 |                           81.88 |              1526538.00 |              62284 |                            1931.00 |                62716 |                           3258367.00 |
| MySQL-1-1-2-5 | MySQL-1         |                1 |        2 |       5 |         8 |      128 |           8 |            0 |                           82.03 |              1523873.00 |              62546 |                            1947.00 |                62454 |                           3299327.00 |
| MySQL-1-1-2-7 | MySQL-1         |                1 |        2 |       7 |         8 |      128 |           8 |            0 |                           81.85 |              1527182.00 |              62627 |                            1922.00 |                62373 |                           3217407.00 |

#### Per Phase

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MySQL-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                          652.25 |              1533148.00 |          500318.00 |                           46815.00 |            499682.00 |                           3174399.00 |
| MySQL-1-1-2 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                          655.38 |              1528065.00 |          499704.00 |                            1977.00 |            500296.00 |                           3299327.00 |

### Monitoring

### Execution phase: SUT deployment

| DBMS        |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1 |       934.57 |      1.20 |           9.66 |                 42.24 |
| MySQL-1-1-2 |       887.17 |      1.20 |           9.68 |                 43.42 |

### Execution phase: component benchmarker

| DBMS        |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------|-------------:|----------:|---------------:|----------------------:|
| MySQL-1-1-1 |       213.59 |      0.21 |           0.17 |                  0.17 |
| MySQL-1-1-2 |       213.59 |      0.79 |           0.16 |                  0.16 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```


### MariaDB

#### YCSB Loader Test for Scaling the Driver

```bash
bexhoma ycsb \
  -dbms MariaDB \
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mariadb_1.log
```

yields (after ca. 45 minutes) something like

testcase_ycsb_mariadb_1.log
```markdown
## Show Summary

### Workload
YCSB SF=1
    Type: ycsb
    Duration: 2456s 
    Code: 1767887403
    Intro: YCSB driver runs the experiment.
    This experiment compares run time and resource consumption of YCSB queries.
    Workload is 'A'.
    Number of rows to insert is 1000000.
    Ordering of inserts is hashed.
    Number of operations is 1000000.
    Batch size is ''.
    Target is based on multiples of '1024'.
    Factors for loading are [1].
    Factors for benchmarking are [1].
    Experiment uses bexhoma version 0.8.20.
    Experiment is limited to DBMS ['MariaDB'].
    Import is handled by 4 and 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker21.
    Loading is tested with [32, 64] threads, split into [4, 8] pods.
    Benchmarking is tested with [64] threads, split into [1] pods.
    Benchmarking is run as [1] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MariaDB-32-4-1024-1 uses docker image mariadb:11.4.7
    RAM:608117153792
    CPU:AMD EPYC 7542 32-Core Processor
    Cores:64
    host:6.8.0-90-generic
    node:cl-worker21
    disk:137746
    datadisk:1794
    cpu_list:0-63
    args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1767887403
MariaDB-32-8-1024-1 uses docker image mariadb:11.4.7
    RAM:608117153792
    CPU:AMD EPYC 7542 32-Core Processor
    Cores:64
    host:6.8.0-90-generic
    node:cl-worker21
    disk:137746
    datadisk:1770
    cpu_list:0-63
    args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1767887403
MariaDB-64-4-1024-1 uses docker image mariadb:11.4.7
    RAM:608117153792
    CPU:AMD EPYC 7542 32-Core Processor
    Cores:64
    host:6.8.0-90-generic
    node:cl-worker21
    disk:137746
    datadisk:1794
    cpu_list:0-63
    args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1767887403
MariaDB-64-8-1024-1 uses docker image mariadb:11.4.7
    RAM:608117153792
    CPU:AMD EPYC 7542 32-Core Processor
    Cores:64
    host:6.8.0-90-generic
    node:cl-worker21
    disk:137746
    datadisk:1770
    cpu_list:0-63
    args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
    requests_cpu:4
    requests_memory:16Gi
    client:1
    numExperiment:1
    eval_parameters
        code:1767887403

### Loading
                   experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [INSERT].Return=OK  [INSERT].99thPercentileLatency(us)
MariaDB-32-4-1024               1       32    1024          4           0                    1023.703077               976855.0             1000000                             2736.50
MariaDB-64-4-1024               1       64    1024          4           0                    1023.675307               976880.0             1000000                             2816.50
MariaDB-32-8-1024               1       32    1024          8           0                    1023.715915               976848.0             1000000                             3304.50
MariaDB-64-8-1024               1       64    1024          8           0                    1023.679236               976881.0             1000000                             3643.75

### Execution
                     experiment_run  threads  target  pod_count  exceptions  [OVERALL].Throughput(ops/sec)  [OVERALL].RunTime(ms)  [READ].Return=OK  [READ].99thPercentileLatency(us)  [UPDATE].Return=OK  [UPDATE].99thPercentileLatency(us)
MariaDB-32-4-1024-1               1       64    1024          1           0                        1023.59               976957.0            500781                             415.0              499219                               431.0
MariaDB-32-8-1024-1               1       64    1024          1           0                        1023.55               976996.0            500435                             409.0              499565                               422.0
MariaDB-64-4-1024-1               1       64    1024          1           0                        1023.58               976966.0            499977                             397.0              500023                               402.0
MariaDB-64-8-1024-1               1       64    1024          1           0                        1023.57               976969.0            500456                             400.0              499544                               405.0

### Workflow

#### Actual
DBMS MariaDB-64-4-1024 - Pods [[1]]
DBMS MariaDB-32-4-1024 - Pods [[1]]
DBMS MariaDB-64-8-1024 - Pods [[1]]
DBMS MariaDB-32-8-1024 - Pods [[1]]

#### Planned
DBMS MariaDB-32-4-1024 - Pods [[1]]
DBMS MariaDB-32-8-1024 - Pods [[1]]
DBMS MariaDB-64-4-1024 - Pods [[1]]
DBMS MariaDB-64-8-1024 - Pods [[1]]

### Tests
TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
TEST passed: Workflow as planned
TEST passed: Execution Phase: contains no FAILED column
```

#### YCSB Loader Test for Persistency

```bash
bexhoma ycsb \
  -dbms MariaDB \
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mariadb_2.log
```

yields (after ca. 70 minutes) something like

testcase_ycsb_mariadb_2.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 4065s 
* Code: 1780345196
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780345196
* MariaDB-1-2-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780345196

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1], [1]]

#### Planned

* DBMS MariaDB-1 - Pods [[1], [1]]

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-0-1 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.16 |              1177492.00 |            125000.00 |                           1288191.00 |
| MariaDB-1-1-0-2 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.11 |              1177978.00 |            125000.00 |                           1309695.00 |
| MariaDB-1-1-0-3 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.17 |              1177394.00 |            125000.00 |                           1287167.00 |
| MariaDB-1-1-0-4 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.13 |              1177808.00 |            125000.00 |                           1286143.00 |
| MariaDB-1-1-0-5 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.10 |              1178188.00 |            125000.00 |                           1304575.00 |
| MariaDB-1-1-0-6 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.16 |              1177486.00 |            125000.00 |                           1298431.00 |
| MariaDB-1-1-0-7 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.12 |              1177939.00 |            125000.00 |                           1311743.00 |
| MariaDB-1-1-0-8 |             1.00 |      8.00 |   128.00 |        8.00 |         0.00 |                          106.07 |              1178413.00 |            125000.00 |                           1309695.00 |

#### Per Run

| DBMS        |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                          849.01 |              1178413.00 |           1000000.00 |                           1299455.00 |

### Execution

#### Per Connection

| DBMS            | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1-1 | MariaDB-1       |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1023.26 |               977266.00 |             499819 |                            1833.00 |               500181 |                            229759.00 |
| MariaDB-1-2-1-1 | MariaDB-1       |                2 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1023.44 |               977094.00 |             499534 |                            1602.00 |               500466 |                            212863.00 |

#### Per Phase

| DBMS          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1023.26 |               977266.00 |          499819.00 |                            1833.00 |            500181.00 |                            229759.00 |
| MariaDB-1-2-1 |             2.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1023.44 |               977094.00 |          499534.00 |                            1602.00 |            500466.00 |                            212863.00 |

### Tests
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

#### YCSB Execution for Scaling and Repetition

```bash
bexhoma ycsb \
  -dbms MariaDB \
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mariadb_3.log
```

yields (after ca. 120 minutes) something like

testcase_ycsb_mariadb_3.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 7175s 
* Code: 1780349271
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run 2 times.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-1-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-1-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-1-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-2-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-2-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-2-3 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271
* MariaDB-1-2-4 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780349271

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

#### Planned

* DBMS MariaDB-1 - Pods [[1, 2, 8, 16], [1, 2, 8, 16]]

### Loading

#### Per Connection



#### Per Run



### Execution

#### Per Connection

| DBMS             | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1-1  | MariaDB-1       |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1002.46 |               997550.00 |             500951 |                            1455.00 |               499049 |                            143871.00 |
| MariaDB-1-1-2-1  | MariaDB-1       |                1 |        2 |       1 |        64 |     1024 |           2 |            0 |                         1023.09 |               488715.00 |             249284 |                            3319.00 |               250716 |                            299007.00 |
| MariaDB-1-1-2-2  | MariaDB-1       |                1 |        2 |       2 |        64 |     1024 |           2 |            0 |                         1023.08 |               488719.00 |             250286 |                            3287.00 |               249714 |                            299007.00 |
| MariaDB-1-1-3-2  | MariaDB-1       |                1 |        3 |       2 |         8 |      128 |           8 |            0 |                          127.95 |               976954.00 |              62348 |                            2089.00 |                62652 |                            304639.00 |
| MariaDB-1-1-3-7  | MariaDB-1       |                1 |        3 |       7 |         8 |      128 |           8 |            0 |                          127.95 |               976942.00 |              62564 |                            2325.00 |                62436 |                            305663.00 |
| MariaDB-1-1-3-6  | MariaDB-1       |                1 |        3 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976864.00 |              62447 |                            2407.00 |                62553 |                            304383.00 |
| MariaDB-1-1-3-5  | MariaDB-1       |                1 |        3 |       5 |         8 |      128 |           8 |            0 |                          127.92 |               977171.00 |              62548 |                            2335.00 |                62452 |                            303615.00 |
| MariaDB-1-1-3-4  | MariaDB-1       |                1 |        3 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976864.00 |              62396 |                            2413.00 |                62604 |                            305919.00 |
| MariaDB-1-1-3-1  | MariaDB-1       |                1 |        3 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976886.00 |              62623 |                            2353.00 |                62377 |                            310015.00 |
| MariaDB-1-1-3-3  | MariaDB-1       |                1 |        3 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976870.00 |              62348 |                            2393.00 |                62652 |                            305151.00 |
| MariaDB-1-1-3-8  | MariaDB-1       |                1 |        3 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976863.00 |              62610 |                            2303.00 |                62390 |                            306431.00 |
| MariaDB-1-1-4-15 | MariaDB-1       |                1 |        4 |      15 |         8 |      128 |          16 |            0 |                          127.88 |               488737.00 |              31204 |                            3049.00 |                31296 |                            406015.00 |
| MariaDB-1-1-4-16 | MariaDB-1       |                1 |        4 |      16 |         8 |      128 |          16 |            0 |                          127.87 |               488794.00 |              31355 |                            3041.00 |                31145 |                            413951.00 |
| MariaDB-1-1-4-14 | MariaDB-1       |                1 |        4 |      14 |         8 |      128 |          16 |            0 |                          127.91 |               488638.00 |              31159 |                            3261.00 |                31341 |                            416511.00 |
| MariaDB-1-1-4-4  | MariaDB-1       |                1 |        4 |       4 |         8 |      128 |          16 |            0 |                          127.91 |               488627.00 |              31470 |                            2983.00 |                31030 |                            424191.00 |
| MariaDB-1-1-4-2  | MariaDB-1       |                1 |        4 |       2 |         8 |      128 |          16 |            0 |                          127.91 |               488626.00 |              31261 |                            3121.00 |                31239 |                            431615.00 |
| MariaDB-1-1-4-8  | MariaDB-1       |                1 |        4 |       8 |         8 |      128 |          16 |            0 |                          127.91 |               488631.00 |              31232 |                            3163.00 |                31268 |                            403967.00 |
| MariaDB-1-1-4-5  | MariaDB-1       |                1 |        4 |       5 |         8 |      128 |          16 |            0 |                          127.89 |               488707.00 |              31283 |                            3075.00 |                31217 |                            404991.00 |
| MariaDB-1-1-4-13 | MariaDB-1       |                1 |        4 |      13 |         8 |      128 |          16 |            0 |                          127.91 |               488617.00 |              31291 |                            3079.00 |                31209 |                            406527.00 |
| MariaDB-1-1-4-11 | MariaDB-1       |                1 |        4 |      11 |         8 |      128 |          16 |            0 |                          127.91 |               488622.00 |              31249 |                            3075.00 |                31251 |                            412415.00 |
| MariaDB-1-1-4-1  | MariaDB-1       |                1 |        4 |       1 |         8 |      128 |          16 |            0 |                          127.91 |               488610.00 |              31250 |                            3179.00 |                31250 |                            415231.00 |
| MariaDB-1-1-4-3  | MariaDB-1       |                1 |        4 |       3 |         8 |      128 |          16 |            0 |                          127.91 |               488632.00 |              31171 |                            3411.00 |                31329 |                            418303.00 |
| MariaDB-1-1-4-6  | MariaDB-1       |                1 |        4 |       6 |         8 |      128 |          16 |            0 |                          127.87 |               488793.00 |              31242 |                            3169.00 |                31258 |                            417023.00 |
| MariaDB-1-1-4-10 | MariaDB-1       |                1 |        4 |      10 |         8 |      128 |          16 |            0 |                          127.89 |               488720.00 |              31154 |                            3255.00 |                31346 |                            406015.00 |
| MariaDB-1-1-4-12 | MariaDB-1       |                1 |        4 |      12 |         8 |      128 |          16 |            0 |                          127.91 |               488635.00 |              31241 |                            3187.00 |                31259 |                            400127.00 |
| MariaDB-1-1-4-9  | MariaDB-1       |                1 |        4 |       9 |         8 |      128 |          16 |            0 |                          127.91 |               488634.00 |              31322 |                            3125.00 |                31178 |                            397823.00 |
| MariaDB-1-1-4-7  | MariaDB-1       |                1 |        4 |       7 |         8 |      128 |          16 |            0 |                          127.91 |               488631.00 |              31173 |                            3031.00 |                31327 |                            398335.00 |
| MariaDB-1-2-4-8  | MariaDB-1       |                2 |        4 |       8 |         8 |      128 |          16 |            0 |                          127.91 |               488641.00 |              31555 |                            2179.00 |                30945 |                            276991.00 |
| MariaDB-1-2-4-14 | MariaDB-1       |                2 |        4 |      14 |         8 |      128 |          16 |            0 |                          127.79 |               489093.00 |              31258 |                            2339.00 |                31242 |                            289023.00 |
| MariaDB-1-2-4-2  | MariaDB-1       |                2 |        4 |       2 |         8 |      128 |          16 |            0 |                          127.78 |               489121.00 |              31369 |                            2251.00 |                31131 |                            278015.00 |
| MariaDB-1-2-4-13 | MariaDB-1       |                2 |        4 |      13 |         8 |      128 |          16 |            0 |                          127.91 |               488619.00 |              31472 |                            2311.00 |                31028 |                            274687.00 |
| MariaDB-1-2-4-6  | MariaDB-1       |                2 |        4 |       6 |         8 |      128 |          16 |            0 |                          127.91 |               488609.00 |              31370 |                            2107.00 |                31130 |                            271615.00 |
| MariaDB-1-2-4-7  | MariaDB-1       |                2 |        4 |       7 |         8 |      128 |          16 |            0 |                          127.91 |               488627.00 |              31332 |                            2243.00 |                31168 |                            277759.00 |
| MariaDB-1-2-4-11 | MariaDB-1       |                2 |        4 |      11 |         8 |      128 |          16 |            0 |                          127.91 |               488635.00 |              31340 |                            2271.00 |                31160 |                            276223.00 |
| MariaDB-1-2-4-3  | MariaDB-1       |                2 |        4 |       3 |         8 |      128 |          16 |            0 |                          127.91 |               488614.00 |              31296 |                            2323.00 |                31204 |                            273407.00 |
| MariaDB-1-2-4-5  | MariaDB-1       |                2 |        4 |       5 |         8 |      128 |          16 |            0 |                          127.91 |               488615.00 |              31224 |                            2247.00 |                31276 |                            275455.00 |
| MariaDB-1-2-4-10 | MariaDB-1       |                2 |        4 |      10 |         8 |      128 |          16 |            0 |                          127.92 |               488603.00 |              31133 |                            2235.00 |                31367 |                            277503.00 |
| MariaDB-1-2-4-16 | MariaDB-1       |                2 |        4 |      16 |         8 |      128 |          16 |            0 |                          127.91 |               488610.00 |              31219 |                            2261.00 |                31281 |                            282879.00 |
| MariaDB-1-2-4-12 | MariaDB-1       |                2 |        4 |      12 |         8 |      128 |          16 |            0 |                          127.91 |               488629.00 |              31060 |                            2203.00 |                31440 |                            288511.00 |
| MariaDB-1-2-4-15 | MariaDB-1       |                2 |        4 |      15 |         8 |      128 |          16 |            0 |                          127.91 |               488634.00 |              31091 |                            2049.00 |                31409 |                            260735.00 |
| MariaDB-1-2-4-1  | MariaDB-1       |                2 |        4 |       1 |         8 |      128 |          16 |            0 |                          127.91 |               488610.00 |              31096 |                            2295.00 |                31404 |                            269055.00 |
| MariaDB-1-2-1-1  | MariaDB-1       |                2 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1023.58 |               976960.00 |             499579 |                            1637.00 |               500421 |                            242303.00 |
| MariaDB-1-2-2-2  | MariaDB-1       |                2 |        2 |       2 |        64 |     1024 |           2 |            0 |                         1023.11 |               488708.00 |             249669 |                            2597.00 |               250331 |                            297727.00 |
| MariaDB-1-2-2-1  | MariaDB-1       |                2 |        2 |       1 |        64 |     1024 |           2 |            0 |                         1023.10 |               488713.00 |             249729 |                            2765.00 |               250271 |                            297215.00 |
| MariaDB-1-2-3-5  | MariaDB-1       |                2 |        3 |       5 |         8 |      128 |           8 |            0 |                          127.96 |               976858.00 |              62480 |                            1990.00 |                62520 |                            285439.00 |
| MariaDB-1-2-3-7  | MariaDB-1       |                2 |        3 |       7 |         8 |      128 |           8 |            0 |                          127.96 |               976874.00 |              62805 |                            1902.00 |                62195 |                            286207.00 |
| MariaDB-1-2-3-4  | MariaDB-1       |                2 |        3 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976866.00 |              62311 |                            1836.00 |                62689 |                            283135.00 |
| MariaDB-1-2-3-3  | MariaDB-1       |                2 |        3 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976866.00 |              62568 |                            1918.00 |                62432 |                            286975.00 |
| MariaDB-1-2-3-1  | MariaDB-1       |                2 |        3 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976881.00 |              62561 |                            1886.00 |                62439 |                            287743.00 |
| MariaDB-1-2-3-2  | MariaDB-1       |                2 |        3 |       2 |         8 |      128 |           8 |            0 |                          127.96 |               976860.00 |              62406 |                            1962.00 |                62594 |                            290047.00 |
| MariaDB-1-2-3-6  | MariaDB-1       |                2 |        3 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976867.00 |              62272 |                            1985.00 |                62728 |                            283391.00 |
| MariaDB-1-2-3-8  | MariaDB-1       |                2 |        3 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976843.00 |              62658 |                            1892.00 |                62342 |                            283135.00 |
| MariaDB-1-2-4-4  | MariaDB-1       |                2 |        4 |       4 |         8 |      128 |          16 |            0 |                          127.82 |               488982.00 |              31224 |                            2263.00 |                31276 |                            281343.00 |
| MariaDB-1-2-4-9  | MariaDB-1       |                2 |        4 |       9 |         8 |      128 |          16 |            0 |                          127.80 |               489064.00 |              31164 |                            2137.00 |                31336 |                            261759.00 |

#### Per Phase

| DBMS          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1002.46 |               997550.00 |          500951.00 |                            1455.00 |            499049.00 |                            143871.00 |
| MariaDB-1-1-2 |             1.00 |    128.00 |  2048.00 |        2.00 |         0.00 |                         2046.17 |               488719.00 |          499570.00 |                            3319.00 |            500430.00 |                            299007.00 |
| MariaDB-1-1-3 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                         1023.62 |               977171.00 |          499884.00 |                            2413.00 |            500116.00 |                            310015.00 |
| MariaDB-1-1-4 |             1.00 |    128.00 |  2048.00 |       16.00 |         0.00 |                         2046.39 |               488794.00 |          500057.00 |                            3411.00 |            499943.00 |                            431615.00 |
| MariaDB-1-2-1 |             2.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1023.58 |               976960.00 |          499579.00 |                            1637.00 |            500421.00 |                            242303.00 |
| MariaDB-1-2-2 |             2.00 |    128.00 |  2048.00 |        2.00 |         0.00 |                         2046.20 |               488713.00 |          499398.00 |                            2765.00 |            500602.00 |                            297727.00 |
| MariaDB-1-2-3 |             2.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                         1023.68 |               976881.00 |          500061.00 |                            1990.00 |            499939.00 |                            290047.00 |
| MariaDB-1-2-4 |             2.00 |    128.00 |  2048.00 |       16.00 |         0.00 |                         2046.11 |               489121.00 |          500203.00 |                            2339.00 |            499797.00 |                            289023.00 |

### Tests
* TEST failed: Loading Phase: [OVERALL].Throughput(ops/sec) contains 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

#### YCSB Execution Different Workload

```bash
bexhoma ycsb \
  -dbms MariaDB \
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mariadb_4.log
```

yields (after ca. 25 minutes) something like

testcase_ycsb_mariadb_4.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1317s 
* Code: 1780356598
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'E'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.8G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780356598

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[8]]

#### Planned

* DBMS MariaDB-1 - Pods [[8]]

### Loading

#### Per Connection



#### Per Run



### Execution

#### Per Connection

| DBMS            | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| MariaDB-1-1-1-7 | MariaDB-1       |                1 |        1 |       7 |         8 |      128 |           8 |            0 |                          127.96 |               976885.00 |                 6177 |                            182399.00 |             118823 |                            2427.00 |                            0 |                                        0.00 |
| MariaDB-1-1-1-8 | MariaDB-1       |                1 |        1 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976879.00 |                 6352 |                            159743.00 |             118648 |                            2379.00 |                            0 |                                        0.00 |
| MariaDB-1-1-1-6 | MariaDB-1       |                1 |        1 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976871.00 |                 6143 |                            172927.00 |             118857 |                            2359.00 |                            0 |                                        0.00 |
| MariaDB-1-1-1-3 | MariaDB-1       |                1 |        1 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976861.00 |                 6250 |                            154367.00 |             118695 |                            2339.00 |                           55 |                                     1623.00 |
| MariaDB-1-1-1-4 | MariaDB-1       |                1 |        1 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976863.00 |                 6250 |                            174463.00 |             118559 |                            2399.00 |                          191 |                                     1504.00 |
| MariaDB-1-1-1-1 | MariaDB-1       |                1 |        1 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976859.00 |                 6250 |                            155135.00 |             118605 |                            2363.00 |                          145 |                                     1684.00 |
| MariaDB-1-1-1-5 | MariaDB-1       |                1 |        1 |       5 |         8 |      128 |           8 |            0 |                          127.96 |               976869.00 |                 6250 |                            168703.00 |             118748 |                            2437.00 |                            2 |                                     7987.00 |
| MariaDB-1-1-1-2 | MariaDB-1       |                1 |        1 |       2 |         8 |      128 |           8 |            0 |                          127.96 |               976866.00 |                 6232 |                            171647.00 |             118768 |                            2281.00 |                            0 |                                        0.00 |

#### Per Phase

| DBMS          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   [SCAN].Return=OK |   [SCAN].99thPercentileLatency(us) |   [INSERT-FAILED].Operations |   [INSERT-FAILED].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-------------------:|-----------------------------------:|-----------------------------:|--------------------------------------------:|
| MariaDB-1-1-1 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                         1023.68 |               976885.00 |             49904.00 |                            182399.00 |          949703.00 |                            2437.00 |                       393.00 |                                     7987.00 |

### Tests
* TEST failed: Loading Phase: [OVERALL].Throughput(ops/sec) contains 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST failed: Execution Phase: contains FAILED column
```

#### YCSB Execution Monitoring

```bash
bexhoma ycsb \
  -dbms MariaDB \
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
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mariadb_5.log
```

yields (after ca. 45 minutes) something like

testcase_ycsb_mariadb_5.log
```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 2404s 
* Code: 1780357927
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '1024'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Experiment uses bexhoma version 0.9.9.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MariaDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker3.
  * Database is persisted to disk of type shared and size 30Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* MariaDB-1-1-1 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780357927
* MariaDB-1-1-2 uses docker image mariadb:11.4.7
  * RAM:541006622720
  * CPU:AMD Opteron(tm) Processor 6378
  * Cores:64
  * host:6.8.0-111-generic
  * node:cl-worker3
  * disk:58107
  * volume_size:30G
  * volume_used:1.9G
  * cpu_list:0-63
  * args:['--max_connections=1500', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=256G', '--innodb-buffer-pool-chunk-size=2G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--innodb-flush-log-at-trx-commit=2', '--sync-binlog=0', '--tmp-table-size=1G', '--max-heap-table-size=1G', '--innodb-doublewrite=0']
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1780357927

### Workflow

#### Actual

* DBMS MariaDB-1 - Pods [[1, 8]]

#### Planned

* DBMS MariaDB-1 - Pods [[1, 8]]

### Loading

#### Per Connection



#### Per Run



### Execution

#### Per Connection

| DBMS            | configuration   |   experiment_run |   client |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1-1 | MariaDB-1       |                1 |        1 |       1 |        64 |     1024 |           1 |            0 |                         1023.41 |               977124.00 |             499187 |                            1738.00 |               500813 |                            271103.00 |
| MariaDB-1-1-2-6 | MariaDB-1       |                1 |        2 |       6 |         8 |      128 |           8 |            0 |                          127.96 |               976875.00 |              62590 |                            2109.00 |                62410 |                            342783.00 |
| MariaDB-1-1-2-2 | MariaDB-1       |                1 |        2 |       2 |         8 |      128 |           8 |            0 |                          127.96 |               976849.00 |              62447 |                            2097.00 |                62553 |                            340479.00 |
| MariaDB-1-1-2-8 | MariaDB-1       |                1 |        2 |       8 |         8 |      128 |           8 |            0 |                          127.96 |               976868.00 |              62478 |                            2187.00 |                62522 |                            343807.00 |
| MariaDB-1-1-2-1 | MariaDB-1       |                1 |        2 |       1 |         8 |      128 |           8 |            0 |                          127.96 |               976861.00 |              62654 |                            2149.00 |                62346 |                            343039.00 |
| MariaDB-1-1-2-4 | MariaDB-1       |                1 |        2 |       4 |         8 |      128 |           8 |            0 |                          127.96 |               976854.00 |              62596 |                            2063.00 |                62404 |                            345087.00 |
| MariaDB-1-1-2-3 | MariaDB-1       |                1 |        2 |       3 |         8 |      128 |           8 |            0 |                          127.96 |               976867.00 |              62520 |                            2129.00 |                62480 |                            337407.00 |
| MariaDB-1-1-2-5 | MariaDB-1       |                1 |        2 |       5 |         8 |      128 |           8 |            0 |                          127.96 |               976862.00 |              62215 |                            2243.00 |                62785 |                            346111.00 |
| MariaDB-1-1-2-7 | MariaDB-1       |                1 |        2 |       7 |         8 |      128 |           8 |            0 |                          127.96 |               976856.00 |              62386 |                            2161.00 |                62614 |                            346111.00 |

#### Per Phase

| DBMS          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| MariaDB-1-1-1 |             1.00 |     64.00 |  1024.00 |        1.00 |         0.00 |                         1023.41 |               977124.00 |          499187.00 |                            1738.00 |            500813.00 |                            271103.00 |
| MariaDB-1-1-2 |             1.00 |     64.00 |  1024.00 |        8.00 |         0.00 |                         1023.69 |               976875.00 |          499886.00 |                            2243.00 |            500114.00 |                            346111.00 |

### Monitoring

### Execution phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       607.29 |      2.85 |           6.86 |                  6.96 |
| MariaDB-1-1-2 |       545.60 |      0.72 |           6.86 |                  6.96 |

### Execution phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| MariaDB-1-1-1 |       143.19 |      0.37 |           0.13 |                  0.13 |
| MariaDB-1-1-2 |       143.19 |      0.63 |           0.13 |                  0.13 |

### Tests
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Loading Phase: [OVERALL].Throughput(ops/sec) contains 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```




