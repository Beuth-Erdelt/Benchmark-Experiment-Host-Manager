# Test Cases

The examples of this documentation are produced by test scripts.
Each script runs a sequence of bexhoma experiments, writes their logs to `logs_tests/` and extracts the summaries, which the pages show.
The [log folder](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/logs_tests) contains the logs and `*_summary.md` files of the last runs.

You will have to change the node selectors in [testfunctions.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/testfunctions.sh) / [testfunctions.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/testfunctions.ps1) to names of nodes that exist in your cluster, or leave out the corresponding parameters.

## Test Scripts

| Group | Test script | Page |
|---|---|---|
| Benchmarks | [test-docs-tpch.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-tpch.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-tpch.ps1) | [Example-TPC-H](Example-TPC-H.md) |
| Benchmarks | [test-docs-tpcds.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-tpcds.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-tpcds.ps1) | [Example-TPC-DS](Example-TPC-DS.md) |
| Benchmarks | [test-docs-ssb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-ssb.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-ssb.ps1) | [Example-SSB](Example-SSB.md) |
| Benchmarks | [test-docs-ycsb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-ycsb.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-ycsb.ps1) | [Example-YCSB](Example-YCSB.md) |
| Benchmarks | [test-docs-benchbase.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-benchbase.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-benchbase.ps1) | [Example-Benchbase](Example-Benchbase.md) |
| Benchmarks | [test-docs-benchbase-others.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-benchbase-others.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-benchbase-others.ps1) | [Example-Benchbase-Others](Example-Benchbase-Others.md) |
| Benchmarks | [test-docs-hammerdb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-hammerdb.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-hammerdb.ps1) | [Example-HammerDB](Example-HammerDB.md) |
| Benchmarks | [test-docs-hardware.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-hardware.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-hardware.ps1) | [Example-Hardware](Example-Hardware.md) |
| DBMS | [test-docs-monetdb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-monetdb.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-monetdb.ps1) | [Example-MonetDB](Example-MonetDB.md) |
| DBMS | [test-docs-mysql.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mysql.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mysql.ps1) | [Example-MySQL](Example-MySQL.md) |
| DBMS | [test-docs-mariadb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadb.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadb.ps1) | [Example-MariaDB](Example-MariaDB.md) |
| DBMS | [test-docs-mariadbcs.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadbcs.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-mariadbcs.ps1) | [Example-MariaDBCS](Example-MariaDBCS.md) |
| DBMS | [test-docs-pgduckdb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-pgduckdb.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-pgduckdb.ps1) | [Example-PgDuckDB](Example-PgDuckDB.md) |
| DBMS | [test-docs-pgbouncer.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-pgbouncer.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-pgbouncer.ps1) | [Example-PGBouncer](Example-PGBouncer.md) |
| DBMS | [test-docs-citus.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-citus.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-citus.ps1) | [Example-Citus](Example-Citus.md) |
| DBMS | [test-docs-yugabytedb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-yugabytedb.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-yugabytedb.ps1) | [Example-YugaByteDB](Example-YugaByteDB.md) |
| DBMS | [test-docs-cockroachdb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cockroachdb.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cockroachdb.ps1) | [Example-CockroachDB](Example-CockroachDB.md) |
| DBMS | [test-docs-tidb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-tidb.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-tidb.ps1) | [Example-TiDB](Example-TiDB.md) |
| DBMS | [test-docs-clickhouse.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-clickhouse.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-clickhouse.ps1) | [Example-ClickHouse](Example-ClickHouse.md) |
| DBMS | [test-docs-redis.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-redis.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-redis.ps1) | [Example-Redis](Example-Redis.md) |
| DBMS | [test-docs-dragonfly.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-dragonfly.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-dragonfly.ps1) | [Example-Dragonfly](Example-Dragonfly.md) |
| DBMS | [test-docs-valkey.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-valkey.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-valkey.ps1) | [Example-Valkey](Example-Valkey.md) |
| DBMS | [test-docs-garnet.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-garnet.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-garnet.ps1) | [Example-Garnet](Example-Garnet.md) |
| DBMS | [test-docs-cassandra.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cassandra.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cassandra.ps1) | [Example-Cassandra](Example-Cassandra.md) |
| DBMS | [test-docs-databaseservice.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-databaseservice.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-databaseservice.ps1) | [Example-CloudDatabase](Example-CloudDatabase.md) |
| DBMS | [test-docs-cedardb.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cedardb.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cedardb.ps1) | [Example-Other-DBMS](Example-Other-DBMS.md) |
| Features | [test-docs-appmetrics.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-appmetrics.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-appmetrics.ps1) | [Example-Metrics](Example-Metrics.md) |
| Features | [test-docs-collector.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-collector.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-collector.ps1) | [Example-Collectors](Example-Collectors.md) |
| Features | [test-docs-multitenant.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-multitenant.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-multitenant.ps1) | [Example-Multi-Tenant](Example-Multi-Tenant.md) |
| Features | [test-docs-modes.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-modes.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-modes.ps1) | - |
| Features | [test-docs-reset.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-reset.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-reset.ps1) | [Test-Reset](Test-Reset.md) |
| Features | [test-docs-durability.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-durability.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-durability.ps1) | [Test-Durability](Test-Durability.md) |
| Features | [test-docs-cases.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cases.sh), [.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cases.ps1) | [TestCases](TestCases.md) |

The runs of a script are in the order of its page.
`scripts/replace-docs.py` puts the summaries of `logs_tests/` into the pages, `scripts/scan-docs.py` lists the logs every page refers to, with experiment code, duration, version and failed tests.

This page has the runs that compare several DBMS in one experiment.

## TPC-H

### Compare

Without `-dbms`, the experiment runs all DBMS that TPC-H runs by default (PostgreSQL, MonetDB, MySQL, MariaDB), one after the other, on the same data.

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
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_compare.log
```

yields (after ca. 120 minutes) something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_compare_summary.md" target="_blank" rel="noopener">docs_tpch_compare.log</a></summary>

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

</details>

## TPC-DS

### Compare

The same for TPC-DS.

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
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_compare.log
```

yields (after ca. 520 minutes) something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpcds_compare_summary.md" target="_blank" rel="noopener">docs_tpcds_compare.log</a></summary>

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

</details>
